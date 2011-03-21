#!/bin/sh
ffver=`firefox -v | cut -d ' ' -f 3`

sudo rm -f /usr/lib/libnssckbi.so
sudo rm -f /usr/lib/firefox-${ffver}/libnssckbi.so
