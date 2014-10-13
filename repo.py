#!/usr/bin/python3

import argparse
import glob
import pyalpm
import requests
import sys
import tarfile


class Package(object):
    def __init__(self, name, version=None):
        if version is not None:
            self.name = name
            self.version = version
        else:
            self.name = name[0]
            self.version = name[1]

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
            if tarinfo.isdir():
                comps = tarinfo.name.rsplit('-', 2)
                comps[1] += '-' + comps[2]
                pkgs.add(Package(comps))

    return pkgs


def print_orphaned(repo):
    pkgs = list_packages(repo)
    for f in glob.glob('*.pkg.tar.*'):
        comps = f.rsplit('-', 3)
        comps += comps.pop().split('.', 1)
        comps[1] += '-' + comps[2]
        pkg = Package(comps[:2])
        if pkg not in pkgs:
            print(f)


def list_installed(path):
    pkgs = set()
    h = pyalpm.Handle(path, path)
    db = h.get_localdb()
    for pkg in db.pkgcache:
        pkgs.add(Package(pkg.name, pkg.version))

    return pkgs


def check_updates(repo, batch=False):
    all_pkgs = sorted(list_packages(repo))

    if batch:
        pkg_map = {}
        params = ['type=multiinfo']
        for pkg in all_pkgs:
            pkg_map[pkg.name] = pkg
            params.append('arg[]={}'.format(pkg.name))

        r = requests.get('https://aur.archlinux.org/rpc.php?{}'.format(
            '&'.join(params)))
        data = r.json()

        for aurpkg in data['results']:
            pkg = pkg_map[aurpkg['Name']]
            if pyalpm.vercmp(aurpkg['Version'], pkg.version) > 0:
                yield pkg, aurpkg['Version']
    else:
        for pkg in all_pkgs:
            r = requests.get(
                'https://aur.archlinux.org/rpc.php?type=info&arg={}'.format(
                    pkg.name))
            data = r.json()
            if type(data['results']) == dict:
                aur_version = data['results']['Version']
                if pyalpm.vercmp(aur_version, pkg.version) > 0:
                    yield pkg, aur_version
            else:
                print("warning: {} is not in the AUR".format(pkg.name),
                      file=sys.stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Arch repository helper")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list-orphaned', '-o', action='store_true')
    group.add_argument('--list-packages', '-l', action='store_true')
    group.add_argument('--list-uninstalled', '-u', action='store_true')
    group.add_argument('--check-updates', action='store_true')
    parser.add_argument(
        '--dbpath', '-b',
        type=str,
        default='/var/lib/pacman',
        help="Specify an alternative pacman database location.")
    parser.add_argument('--pkgonly', action='store_true',
                        help="Do not include version in package lists.")
    parser.add_argument('repo')

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
            # emulate the cower -b format to allow for parsing by other scripts
            print(":: {pkg} -> {version}".format(pkg=pkg, version=version))
