#!/bin/sh
################################################################################
# iptables_setup_base.sh - iptables base setup
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

IFACE="eth0"
IPT=$(which iptables)
IP6T=$(which ip6tables)

# Flush existing rules and set default policies {{{
$IPT -P INPUT DROP
$IPT -P FORWARD DROP
$IPT -P OUTPUT ACCEPT
$IPT -F
$IPT -X

$IP6T -P INPUT DROP
$IP6T -P FORWARD DROP
$IP6T -P OUTPUT ACCEPT
$IP6T -F
$IP6T -X
# }}}

# Create custom chains {{{
$IPT -N open
$IPT -N interfaces

$IP6T -N open
$IP6T -N interfaces
# }}}

# INPUT rules {{{

# Accept all packets belonging to established connections
$IPT -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
$IP6T -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT

# Add rule for our custom chains
$IPT -A INPUT -j interfaces
$IPT -A INPUT -j open

$IP6T -A INPUT -j interfaces
$IP6T -A INPUT -j open

# Specific deny cases for TCP and UDP packets
$IPT -A INPUT -p tcp -j REJECT --reject-with tcp-reset
$IPT -A INPUT -p udp -j REJECT --reject-with icmp-port-unreachable

$IP6T -A INPUT -p tcp -j REJECT --reject-with tcp-reset
$IP6T -A INPUT -p udp -j REJECT --reject-with icmp6-port-unreachable

# Accept all traffic from trusted interfaces
$IPT -A interfaces -i lo -j ACCEPT
$IP6T -A interfaces -i lo -j ACCEPT

# IPv6 Rules {{{
# Based upon http://www.cert.org/downloads/IPv6/ip6tables_rules.txt

# Drop packets with RH0 headers
$IP6T -A INPUT -m rt --rt-type 0 -j DROP
$IP6T -A FORWARD -m rt --rt-type 0 -j DROP
$IP6T -A OUTPUT -m rt --rt-type 0 -j DROP

# Allow some inbound ICMPv6 packets
$IP6T -A INPUT -p icmpv6 --icmpv6-type destination-unreachable -j ACCEPT
$IP6T -A INPUT -p icmpv6 --icmpv6-type packet-too-big -j ACCEPT
$IP6T -A INPUT -p icmpv6 --icmpv6-type time-exceeded -j ACCEPT
$IP6T -A INPUT -p icmpv6 --icmpv6-type parameter-problem -j ACCEPT

# Allow pings, but rate limit
$IP6T -A INPUT -p icmpv6 --icmpv6-type echo-request -m limit --limit 900/min -j ACCEPT
$IP6T -A INPUT -p icmpv6 --icmpv6-type echo-reply -m limit --limit 900/min -j ACCEPT

# Drop multicast pings (only useful for detecting alive hosts on a subnet)
$IP6T -A INPUT -p icmpv6 --icmpv6-type echo-request -d ff02::1 -j DROP

# Allow some outbound ICMPv6 packets
$IP6T -A OUTPUT -p icmpv6 --icmpv6-type destination-unreachable -j ACCEPT
$IP6T -A OUTPUT -p icmpv6 --icmpv6-type packet-too-big -j ACCEPT
$IP6T -A OUTPUT -p icmpv6 --icmpv6-type time-exceeded -j ACCEPT
$IP6T -A OUTPUT -p icmpv6 --icmpv6-type parameter-problem -j ACCEPT

# Limit NDP messages to local network
$IP6T -A OUTPUT -p icmpv6 --icmpv6-type neighbour-solicitation -m hl --hl-eq 255 -j ACCEPT
$IP6T -A OUTPUT -p icmpv6 --icmpv6-type neighbour-advertisement -m hl --hl-eq 255 -j ACCEPT
$IP6T -A OUTPUT -p icmpv6 --icmpv6-type router-solicitation -m hl --hl-eq 255 -j ACCEPT

# Accept all other inbound ICMPv6 packets
$IP6T -A INPUT -p icmpv6 -j ACCEPT

# }}}

# IPv4 Rules {{{

# Allow pings, but rate limit
$IPT -A INPUT -p icmp --icmp-type echo-request -m limit --limit 900/min -j ACCEPT
$IPT -A INPUT -p icmp --icmp-type echo-reply -m limit --limit 900/min -j ACCEPT

# Drop ICMP packets that we don't care about
$IPT -I INPUT -p icmp --icmp-type redirect -j DROP
$IPT -I INPUT -p icmp --icmp-type router-advertisement -j DROP
$IPT -I INPUT -p icmp --icmp-type router-solicitation -j DROP
$IPT -I INPUT -p icmp --icmp-type address-mask-request -j DROP
$IPT -I INPUT -p icmp --icmp-type address-mask-reply -j DROP

# Accept all inbound ICMP packets
$IPT -A INPUT -p icmp -j ACCEPT

# }}}

# Protection against common attacks {{{

# Drop new incoming TCP connections that aren't SYN packets
$IPT -A INPUT -p tcp ! --syn -m state --state NEW -j DROP
$IP6T -A INPUT -p tcp ! --syn -m state --state NEW -j DROP

# Drop incoming malformed XMAS packets
$IPT -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
$IP6T -A INPUT -p tcp --tcp-flags ALL ALL -j DROP

# Drop incoming malformed NULL packets
$IPT -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
$IP6T -A INPUT -p tcp --tcp-flags ALL NONE -j DROP

# }}}

# }}}

# Save rules {{{

/etc/rc.d/iptables save
/etc/rc.d/ip6tables save

# }}}

