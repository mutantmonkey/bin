#!/usr/bin/python3

import argparse
import glob
import hashlib
import os.path
import pyalpm
import requests
import sys
import tarfile
import zstandard
from contextlib import contextmanager
from srcinfo.parse import parse_srcinfo


class Package(object):
    def __init__(self, name, version=None, filename=None):
        if version is not None:
            self.name = name
            self.version = version
        else:
            self.name = name[0]
            self.version = name[1]

        self.filename = filename

    def __lt__(self, other):
        # FIXME: also compare version
        return self.name < other.name

    def __gt__(self, other):
        # FIXME: also compare version
        return self.name > other.name

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.name, self.version))

    def __repr__(self):
        return "{name} {version}".format(name=self.name, version=self.version)


def list_packages(repo):
    pkgs = set()
    with tarfile.open(repo) as tar:
        for tarinfo in tar:
            if tarinfo.name[-5:] == '/desc':
                pkg_data = {}
                next_line_key = None
                contents = tar.extractfile(tarinfo)
                for line in contents.readlines():
                    line = line.decode('utf-8').rstrip('\n')
                    if line == '%FILENAME%':
                        next_line_key = 'filename'
                    elif line == '%NAME%':
                        next_line_key = 'name'
                    elif line == '%VERSION%':
                        next_line_key = 'version'
                    else:
                        if next_line_key is not None:
                            pkg_data[next_line_key] = line.rstrip()
                        next_line_key = None

                pkgs.add(Package(**pkg_data))

    return pkgs


def print_orphaned(repo):
    pkgs = list_packages(repo)
    expected_filenames = [pkg.filename for pkg in pkgs]
    for f in glob.glob('*.pkg.tar.*'):
        # signature filenames are the package filename + .sig
        check_filename = f.rsplit('.sig', 1)[0]
        if check_filename not in expected_filenames:
            print(f)


def list_installed(dbpath):
    pkgs = set()
    h = pyalpm.Handle('/', dbpath)
    db = h.get_localdb()
    for pkg in db.pkgcache:
        pkgs.add(Package(pkg.name, pkg.version))

    return pkgs


def check_updates(repo, batch=True):
    all_pkgs = sorted(list_packages(repo))

    if batch:
        pkg_map = {}
        params = ['v=5', 'type=info']
        for pkg in all_pkgs:
            pkg_map[pkg.name] = pkg
            params.append('arg[]={}'.format(pkg.name))
        remaining_pkgs = set(pkg_map.keys())

        r = requests.get('https://aur.archlinux.org/rpc/?{}'.format(
            '&'.join(params)))
        data = r.json()

        for aurpkg in data['results']:
            pkg = pkg_map[aurpkg['Name']]
            if pyalpm.vercmp(aurpkg['Version'], pkg.version) > 0:
                yield pkg, aurpkg['Version']
            remaining_pkgs.remove(aurpkg['Name'])

        for pkg in remaining_pkgs:
            print("warning: {} is not in the AUR".format(pkg),
                  file=sys.stderr)
    else:
        for pkg in all_pkgs:
            r = requests.get(
                'https://aur.archlinux.org/rpc/?v=5&type=info&arg[]={}'.format(
                    pkg.name))
            data = r.json()
            if len(data['results']) == 1:
                aur_version = data['results'][0]['Version']
                if pyalpm.vercmp(aur_version, pkg.version) > 0:
                    yield pkg, aur_version
            else:
                print("warning: {} is not in the AUR".format(pkg.name),
                      file=sys.stderr)


def print_pkg(pkg, pkgonly=False):
    if pkgonly:
        print(pkg.name)
    else:
        print(pkg)


def has_vcs_suffix(pkgname):
    return pkgname.endswith('-bzr') \
            or pkgname.endswith('-git') \
            or pkgname.endswith('-hg') \
            or pkgname.endswith('-svn')


# https://github.com/indygreg/python-zstandard/issues/64#issuecomment-647811500
@contextmanager
def open_tar_zst(path_tar_zst):
    """Decompress and open a .tar.zst file"""
    with open(path_tar_zst, 'rb') as fh:
        dctx = zstandard.ZstdDecompressor()
        with dctx.stream_reader(fh) as stream:
            yield tarfile.TarFile(fileobj=stream)


def compare_with_sources_pkgver(repo, srcpath, skip_vcs_suffix=False):
    source_packages = set([])

    for srcinfo_file in glob.glob(os.path.join(srcpath,
                                               '*/.SRCINFO')):
        with open(srcinfo_file) as f:
            result, errors = parse_srcinfo(f.read())
            pkgver = '{0}-{1}'.format(result['pkgver'], result['pkgrel'])
            if result.get('epoch', None) is not None:
                pkgver = '{0}:{1}'.format(result['epoch'], pkgver)

                for pkgname in result['packages']:
                    if not skip_vcs_suffix or not has_vcs_suffix(pkgname):
                        source_packages.add(Package(pkgname, pkgver))

    for pkg in sorted(source_packages - list_packages(repo)):
        yield pkg


def compare_with_sources_sha256sum(repo, srcpath):
    pkgbuild_sha256sums = {}

    for srcinfo_file in glob.glob(os.path.join(srcpath,
                                               '*/.SRCINFO')):
        with open(srcinfo_file) as f:
            result, errors = parse_srcinfo(f.read())
            with open(srcinfo_file.replace('.SRCINFO', 'PKGBUILD'),
                      'rb') as p:
                h = hashlib.sha256()
                h.update(p.read())

            for pkgname in result['packages']:
                pkgbuild_sha256sums[pkgname] = h.hexdigest()

    for pkg in list_packages(repo):
        expected_pkgbuild_sha256sum = pkgbuild_sha256sums[pkg.name]

        if pkg.filename.endswith('.zst'):
            with open_tar_zst(pkg.filename) as tar:
                for tarinfo in tar:
                    if tarinfo.name[-5:] == '/.BUILDINFO':
                        contents = tar.extractfile(tarinfo)
                        for line in contents.readlines():
                            if line.startswith('pkgbuild_sha256sum'):
                                _, v = line.split('=', 1)

                                if v.strip() != expected_pkgbuild_sha256sum:
                                    yield pkg


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Arch repository helper")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list-orphaned', '-o', action='store_true',
                       help="list files that look like packages in the "
                            "current directory that are not found in the "
                            "repository database")
    group.add_argument('--list-packages', '-l', action='store_true',
                       help="list packages in the repository")
    group.add_argument('--list-uninstalled', '-u', action='store_true',
                       help="list packages in the repository that are not "
                            "installed on the local system")
    group.add_argument('--check-updates', action='store_true',
                       help="check packages in the repository for updates")
    group.add_argument('--compare-with-sources', action='store_true',
                       help="compare packages with those found in a package "
                            "source directory")
    parser.add_argument('--dbpath', '-b', type=str, default='/var/lib/pacman',
                        help="specify an alternative pacman database location")
    parser.add_argument('--pkgonly', action='store_true',
                        help="do not include version in package lists")
    parser.add_argument('--srcpath', type=str,
                        help="path to package source directory")
    group2 = parser.add_mutually_exclusive_group(required=False)
    group2.add_argument('--compare-pkgbuild', action='store_true',
                        help="compare PKGBUILD instead of package version "
                             "when using --compare-with-sources")
    group2.add_argument('--skip-vcs-suffix', action='store_true',
                        help="skip packages that use a common VCS suffix "
                             "(e.g. -git) when using --compare-with-sources")
    parser.add_argument('repo', help="path to repository database file")

    args = parser.parse_args()

    if args.list_orphaned:
        print_orphaned(args.repo)
    elif args.list_packages:
        for pkg in sorted(list_packages(args.repo)):
            print_pkg(pkg, args.pkgonly)
    elif args.list_uninstalled:
        for pkg in sorted(list_packages(args.repo) -
                          list_installed(args.dbpath)):
            print_pkg(pkg, args.pkgonly)
    elif args.check_updates:
        for pkg, version in check_updates(args.repo):
            if args.pkgonly:
                print(pkg.name)
            else:
                # emulate the cower -b format
                print(":: {pkg} -> {version}".format(pkg=pkg, version=version))
    elif args.compare_with_sources:
        if args.srcpath is None or len(args.srcpath) <= 0:
            print("fatal: a --srcpath must be provided.", file=sys.stderr)
            sys.exit(1)

        if args.compare_pkgbuild:
            for pkg in compare_with_sources_sha256sum(args.repo, args.srcpath):
                print_pkg(pkg, args.pkgonly)
        else:
            for pkg in compare_with_sources_pkgver(args.repo, args.srcpath,
                                                   args.skip_vcs_suffix):
                print_pkg(pkg, args.pkgonly)
