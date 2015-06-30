#!/bin/sh
set -e
/usr/bin/python3 $HOME/code/mmhome/scheme.py -i 10.42.18.2 -d 100 all_off
/usr/bin/systemctl poweroff
