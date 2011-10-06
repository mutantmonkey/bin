#!/bin/sh
################################################################################
# vt_staticarp.sh - static ARP for the Virginia Tech network
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

function add_entry {
    route=$(ip route get $1 | head -n1 | awk '{print $2}')
    if [ "$route" == "dev" ]; then
        arp -s $1 $2
    fi
}

# cas-6509-2
add_entry   172.31.8.1      00:24:f9:c3:28:00
add_entry   172.31.16.1     00:24:f9:c3:28:00
add_entry   172.31.24.1     00:24:f9:c3:28:00
add_entry   172.31.32.1     00:24:f9:c3:28:00
add_entry   172.31.40.1     00:24:f9:c3:28:00
add_entry   172.31.48.1     00:24:f9:c3:28:00
add_entry   172.31.56.1     00:24:f9:c3:28:00
add_entry   172.31.64.1     00:24:f9:c3:28:00
add_entry   172.31.72.1     00:24:f9:c3:28:00
add_entry   172.31.160.1    00:24:f9:c3:28:00
add_entry   172.31.168.1    00:24:f9:c3:28:00
add_entry   172.31.176.1    00:24:f9:c3:28:00
add_entry   172.31.184.1    00:24:f9:c3:28:00

# cas-6509-3
add_entry   172.31.80.1     00:24:f9:c3:14:00
add_entry   172.31.88.1     00:24:f9:c3:14:00
add_entry   172.31.96.1     00:24:f9:c3:14:00
add_entry   172.31.104.1    00:24:f9:c3:14:00
add_entry   172.31.112.1    00:24:f9:c3:14:00
add_entry   172.31.120.1    00:24:f9:c3:14:00
add_entry   172.31.128.1    00:24:f9:c3:14:00
add_entry   172.31.136.1    00:24:f9:c3:14:00
add_entry   172.31.144.1    00:24:f9:c3:14:00
add_entry   172.31.152.1    00:24:f9:c3:14:00
add_entry   172.31.192.1    00:24:f9:c3:14:00
add_entry   172.31.200.1    00:24:f9:c3:14:00
add_entry   172.31.208.1    00:24:f9:c3:14:00
add_entry   172.31.216.1    00:24:f9:c3:14:00
