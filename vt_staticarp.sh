#!/bin/bash
################################################################################
# vt_staticarp.sh - static ARP for the Virginia Tech network
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

IF=$1

function add_arp {
    route=$(ip route get 8.8.8.8 | head -n1 | awk '{print $3}')
    my_ip=$(ip route get 8.8.8.8 | head -n1 | awk '{print $7}')
    if [ "$route" == "$1" ]; then
        ip -4 neigh replace $1 lladdr $2 dev $IF
        arping -q -I $IF -U -c 2 -s $my_ip $1
    fi
}

function add_neigh6 {
    ip -6 neigh replace $1 dev $IF lladdr $2 nud permanent
}

# cas-6509-1
add_neigh6  fe80::224:f9ff:fec3:2400    00:24:f9:c3:24:00

# cas-6509-2
add_neigh6  fe80::224:f9ff:fec3:2800    00:24:f9:c3:28:00

# cas-6509-2
add_arp     172.31.8.1      00:24:f9:c3:28:00
add_arp     172.31.16.1     00:24:f9:c3:28:00
add_arp     172.31.24.1     00:24:f9:c3:28:00
add_arp     172.31.32.1     00:24:f9:c3:28:00
add_arp     172.31.40.1     00:24:f9:c3:28:00
add_arp     172.31.48.1     00:24:f9:c3:28:00
add_arp     172.31.56.1     00:24:f9:c3:28:00
add_arp     172.31.64.1     00:24:f9:c3:28:00
add_arp     172.31.72.1     00:24:f9:c3:28:00
add_arp     172.31.160.1    00:24:f9:c3:28:00
add_arp     172.31.168.1    00:24:f9:c3:28:00
add_arp     172.31.176.1    00:24:f9:c3:28:00
add_arp     172.31.184.1    00:24:f9:c3:28:00

# cas-6509-3
add_arp     172.31.80.1     00:24:f9:c3:14:00
add_arp     172.31.88.1     00:24:f9:c3:14:00
add_arp     172.31.96.1     00:24:f9:c3:14:00
add_arp     172.31.104.1    00:24:f9:c3:14:00
add_arp     172.31.112.1    00:24:f9:c3:14:00
add_arp     172.31.120.1    00:24:f9:c3:14:00
add_arp     172.31.128.1    00:24:f9:c3:14:00
add_arp     172.31.136.1    00:24:f9:c3:14:00
add_arp     172.31.144.1    00:24:f9:c3:14:00
add_arp     172.31.152.1    00:24:f9:c3:14:00
add_arp     172.31.192.1    00:24:f9:c3:14:00
add_arp     172.31.200.1    00:24:f9:c3:14:00
add_arp     172.31.208.1    00:24:f9:c3:14:00
add_arp     172.31.216.1    00:24:f9:c3:14:00
