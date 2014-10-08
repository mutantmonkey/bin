#!/usr/bin/python3

import argparse
import glob
import os.path
import subprocess
import tarfile


class Package(object):
    def __init__(self, name, ver=None, rel=None):
        if ver is not None and rel is not None:
            self.name = name
            self.ver = ver
            self.rel = rel
        else:
            self.name = name[0]
            self.ver = name[1]
            self.rel = name[2]

    def __lt__(self, other):
        # FIXME: also compare version and release
        return self.name < other.name

    def __gt__(self, other):
        # FIXME: also compare version and release
        return self.name > other.name

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.name, self.ver, self.rel))

    def __repr__(self):
        return "{name} {ver}-{rel}".format(name=self.name, ver=self.ver,
                                           rel=self.rel)


def list_packages(repo):
    pkgs = set()
    with tarfile.open(repo) as tar:
        for tarinfo in tar:
            if tarinfo.isdir():
                comps = tarinfo.name.rsplit('-', 2)
                pkgs.add(Package(comps))

    return pkgs


def print_orphaned(repo):
    pkgs = list_packages(repo)
    for f in glob.glob('*.pkg.tar.*'):
        comps = f.rsplit('-', 3)
        comps += comps.pop().split('.', 1)
        pkg = Package(comps[:3])
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Arch repository helper")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list-orphaned', '-o', action='store_true')
    group.add_argument('--list-packages', '-l', action='store_true')
    group.add_argument('--list-uninstalled', '-u', action='store_true')
    parser.add_argument('repo')

    args = parser.parse_args()

    if args.list_orphaned:
        print_orphaned(args.repo)
    elif args.list_packages:
        for pkg in sorted(list_packages(args.repo)):
            print(pkg)
    elif args.list_uninstalled:
        for pkg in sorted(list_packages(args.repo) - list_installed()):
            print(pkg)
