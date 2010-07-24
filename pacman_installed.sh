#!/bin/sh
################################################################################
# pacman_installed.sh - Print installed Pacman packages
#
# author: mutantmonkey <mutantmonkey@gmail.com>
################################################################################

IFS='
'
for line in `pacman -Q`; do
	packages=${packages}" "${line% *}
done

echo $packages
