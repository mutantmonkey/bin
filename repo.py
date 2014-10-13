#!/usr/bin/python3

import argparse
import glob
import os.path
import pyalpm
import requests
import subprocess
import sys
import tarfile


class Package(object):
    def __init__(self, name, ver=None):
        if ver is not None:
            self.name = name
            self.ver = ver
        else:
            self.name = name[0]
            self.ver = name[1]

    def __lt__(self, other):
        # FIXME: also compare version
        return self.name < other.name

    def __gt__(self, other):
        # FIXME: also compare version
        return self.name > other.name

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.name, self.ver))

    def __repr__(self):
        return "{name} {ver}".format(name=self.name, ver=self.ver)


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


def list_installed():
    pkgs = set()
    # TODO: consider using pyalpm instead of pacman directly
    out = subprocess.check_output(['/usr/bin/pacman', '-Qn']).decode('utf-8')
    for line in out.splitlines():
        if line[0] == ' ':
            continue

        line = line.split(' ', 1)
        line += line.pop().split('-', 1)
        pkgs.add(Package(line))

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
            if pyalpm.vercmp(aurpkg['Version'], pkg.ver) > 0:
                yield pkg, aurpkg['Version']
    else:
        for pkg in all_pkgs:
            r = requests.get(
                'https://aur.archlinux.org/rpc.php?type=info&arg={}'.format(
                    pkg.name))
            data = r.json()
            if type(data['results']) == dict:
                aur_version = data['results']['Version']
                if pyalpm.vercmp(aur_version, pkg.ver) > 0:
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
    parser.add_argument('--pkgonly', action='store_true',
                        help="Do not include version in package lists")
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
        for pkg in sorted(list_packages(args.repo) - list_installed()):
            if args.pkgonly:
                print(pkg.name)
            else:
                print(pkg)
    elif args.check_updates:
        for pkg, ver in check_updates(args.repo):
            # emulate the cower -b format to allow for parsing by other scripts
            print(":: {pkg} -> {ver}".format(pkg=pkg, ver=ver))
