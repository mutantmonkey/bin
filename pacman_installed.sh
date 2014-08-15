#!/bin/sh
################################################################################
# pacman_installed.sh - Print installed Pacman packages
################################################################################

IFS='
'
for line in `pacman -Q`; do
	packages=${packages}" "${line% *}
done

echo $packages
