#!/bin/bash
################################################################################
# block_eui64.sh - block all traffic on EUI-64 generated address
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

IF=$1
IPADDR=$(ip -6 addr show $IF | grep "scope global dynamic" | sed 's/^.*inet6 \(.*\)\/.*$/\1/')
IP6T=$(which ip6tables)

[ -z "$IPADDR" ] && exit 0

$IP6T -C INPUT -d $IPADDR -j DROP 2>/dev/null
[ $? != 0 ] && $IP6T -I INPUT -d $IPADDR -j DROP

$IP6T -C OUTPUT -s $IPADDR -j DROP 2>/dev/null
[ $? != 0 ] && $IP6T -I OUTPUT -s $IPADDR -j DROP
