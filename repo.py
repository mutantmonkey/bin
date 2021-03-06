#!/usr/bin/python3

import argparse
import glob
import pyalpm
import requests
import sys
import tarfile


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
    parser.add_argument('--dbpath', '-b', type=str, default='/var/lib/pacman',
                        help="specify an alternative pacman database location")
    parser.add_argument('--pkgonly', action='store_true',
                        help="do not include version in package lists")
    parser.add_argument('repo', help="path to repository database file")

    args = parser.parse_args()

    if args.list_orphaned:
        print_orphaned(args.repo)
    elif args.list_packages:
        for pkg in sorted(list_packages(args.repo)):
            if args.pkgonly:
                print(pkg.name)
            else:
                print(pkg)
    elif args.list_uninstalled:
        for pkg in sorted(list_packages(args.repo) -
                          list_installed(args.dbpath)):
            if args.pkgonly:
                print(pkg.name)
            else:
                print(pkg)
    elif args.check_updates:
        for pkg, version in check_updates(args.repo):
            if args.pkgonly:
                print(pkg.name)
            else:
                # emulate the cower -b format
                print(":: {pkg} -> {version}".format(pkg=pkg, version=version))
