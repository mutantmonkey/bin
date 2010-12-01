#!/bin/sh
reflector -c %own% -l 8 -f --grep http > /tmp/mirrorlist
sudo mv /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak
sudo mv /tmp/mirrorlist /etc/pacman.d/mirrorlist

