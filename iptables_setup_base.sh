#!/bin/sh
################################################################################
# iptables_setup_base.sh - iptables base setup
#
# author: mutantmonkey <mutantmonkey@gmail.com>
################################################################################

IFACE="eth0"

# Default rules for when a packet does not match our settings {{{
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
iptables -F
iptables -X

ip6tables -P INPUT DROP
ip6tables -P FORWARD DROP
ip6tables -P OUTPUT ACCEPT
ip6tables -F
ip6tables -X

# }}}


# Create custom chains {{{
iptables -N open
iptables -N interfaces

ip6tables -N open
ip6tables -N interfaces
# }}}


# INPUT rules {{{

# Accept all packets belonging to established connections
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
ip6tables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT

# Add rule for our custom chains
iptables -A INPUT -j interfaces
iptables -A INPUT -j open

ip6tables -A INPUT -j interfaces
ip6tables -A INPUT -j open

# Specific deny cases for TCP and UDP packets
iptables -A INPUT -p tcp -j REJECT --reject-with tcp-reset
iptables -A INPUT -p udp -j REJECT --reject-with icmp-port-unreachable

ip6tables -A INPUT -p tcp -j REJECT --reject-with tcp-reset
ip6tables -A INPUT -p udp -j REJECT --reject-with icmp6-port-unreachable

# Accept all traffic from trusted interfaces
iptables -A interfaces -i lo -j ACCEPT
ip6tables -A interfaces -i lo -j ACCEPT

# IPv6 Rules {{{
# Based upon http://www.cert.org/downloads/IPv6/ip6tables_rules.txt

# Drop packets with RH0 headers
ip6tables -A INPUT -m rt --rt-type 0 -j DROP
ip6tables -A FORWARD -m rt --rt-type 0 -j DROP
ip6tables -A OUTPUT -m rt --rt-type 0 -j DROP

# Allow some inbound ICMPv6 packets
ip6tables -A INPUT -p icmpv6 --icmpv6-type destination-unreachable -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type packet-too-big -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type time-exceeded -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type parameter-problem -j ACCEPT

# Block inbound pings
#ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-request -i $IFACE -j DROP

# Allow pings, but rate limit
ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-request -m limit --limit 900/min -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-reply -m limit --limit 900/min -j ACCEPT

# Allow some outbound ICMPv6 packets
ip6tables -A OUTPUT -p icmpv6 --icmpv6-type destination-unreachable -j ACCEPT
ip6tables -A OUTPUT -p icmpv6 --icmpv6-type packet-too-big -j ACCEPT
ip6tables -A OUTPUT -p icmpv6 --icmpv6-type time-exceeded -j ACCEPT
ip6tables -A OUTPUT -p icmpv6 --icmpv6-type parameter-problem -j ACCEPT

# Limit NDP messages to local network
ip6tables -A OUTPUT -p icmpv6 --icmpv6-type neighbour-solicitation -m hl --hl-eq 255 -j ACCEPT
ip6tables -A OUTPUT -p icmpv6 --icmpv6-type neighbour-advertisement -m hl --hl-eq 255 -j ACCEPT
ip6tables -A OUTPUT -p icmpv6 --icmpv6-type router-solicitation -m hl --hl-eq 255 -j ACCEPT

# Accept all other inbound ICMPv6 packets
ip6tables -A INPUT -p icmpv6 -j ACCEPT

# }}}


# IPv4 Rules {{{

# Accept all inbound ICMP packets
iptables -A INPUT -p icmp -j ACCEPT

# Block inbound pings
iptables -A INPUT -p icmp --icmp-type echo-request -i $IFACE -j DROP

# Drop useless ICMP packets (well, not useless for routers)
iptables -I INPUT -p icmp --icmp-type redirect -j DROP
iptables -I INPUT -p icmp --icmp-type router-advertisement -j DROP
iptables -I INPUT -p icmp --icmp-type router-solicitation -j DROP
iptables -I INPUT -p icmp --icmp-type address-mask-request -j DROP
iptables -I INPUT -p icmp --icmp-type address-mask-reply -j DROP

# }}}


# Protection against common attacks {{{

# Drop new incoming TCP connections that aren't SYN packets
iptables -A INPUT -p tcp ! --syn -m state --state NEW -j DROP
ip6tables -A INPUT -p tcp ! --syn -m state --state NEW -j DROP

# Drop incoming packets with fragments
iptables -A INPUT -f -j DROP
#ip6tables -A INPUT -f -j DROP

# Drop incoming malformed XMAS packets
iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
ip6tables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP

# Drop incoming malformed NULL packets
iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
ip6tables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP

# }}}

# }}}


# Save rules {{{

/etc/rc.d/iptables save
/etc/rc.d/ip6tables save

# }}}

