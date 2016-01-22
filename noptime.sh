#!/bin/sh
set -e
/usr/bin/python3 $HOME/code/mmhome/scheme.py -d 100 all_off
/usr/bin/systemctl poweroff
