#!/bin/sh
################################################################################
# block_eui64.sh - block all traffic on EUI-64 generated address
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

IF=$1
IPADDR=$(ip -6 addr show $IF | grep "scope global dynamic" | sed 's/^.*inet6 \(.*\)\/.*$/\1/')
ip6tables -I INPUT -d $IPADDR -j DROP
ip6tables -I OUTPUT -s $IPADDR -j DROP
