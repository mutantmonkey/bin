#!/bin/bash
################################################################################
# vt_staticipv6.sh - static IPv6 routes for the Virginia Tech Network
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

IF=$1

if [ "$IF" == "" ]; then
    echo "Usage: vt_staticipv6.sh <interface>"
    exit 1
fi

sysctl -w net.ipv6.conf.$IF.accept_ra_defrtr=0
sysctl -w net.ipv6.conf.$IF.accept_redirects=0

# block all router advertisements by default
#ip6tables -A INPUT -p icmpv6 --icmpv6-type router-advertisement -j DROP

function add_route {
    #ip6tables -I INPUT -p icmpv6 --icmpv6-type router-advertisement -s $1 -j ACCEPT
    ping6 -I $IF -c 1 $1 >/dev/null
    if [ $? -eq 0 ]; then
        ip -6 route add default via $1 dev $IF proto kernel metric 1024
        ip -6 neigh replace $1 dev $IF lladdr $2 nud permanent
        exit 0
    fi
}

add_route   fe80::224:f9ff:fec3:2400    00:24:f9:c3:24:00
add_route   fe80::224:f9ff:fec3:2800    00:24:f9:c3:28:00
