#!/usr/bin/env python3

import os, time

# Installing dependencies
os.system('sudo apt install conntrack nload htop tcpdump -y')

# Snax Youtube Tutorial Mitagation Settings For (Vultr)
# - The OpenVPN BPF filter was provided by Courvix. (newer ones aren't needed for the purpose of this setup).
# - These rules are quite basic and are meant to help against basic DDoS attacks on their low mitagation capable network.
# - Credits to Courvix's research on NEW state tracked OpenVPN Connections with Pritunl. (https://github.com/Courvix/OpenVPN-DDoS-Protection).

os.system("clear")
home_ip = input('Please enter your home IP so I can whitelist it for your ssh and web services: ')
os.system("clear")
server_ip = input('Please enter your server\'s IPv4 address: ')
os.system("clear")
openvpn_port = input('Please specify your OpenVPN port: ')

# Prerouting filters, Change the '-s' source IP to your home connection's IPv4 address. Change the '-d' destination IP to your servers IPv4 address. Change the connection port if you'd like. or follow documentation on Courvix's github and his explanation of a new OpenVPN connection.
os.system(f'iptables -A PREROUTING -t mangle -d {server_ip}/32 -p udp -m conntrack --ctstate NEW -m comment --comment "openvpn bpf" -m bpf --bytecode "18,48 0 0 0,84 0 0 240,21 0 14 64,48 0 0 9,21 0 12 17,40 0 0 6,69 10 0 8191,177 0 0 0,80 0 0 8,21 0 7 56,64 0 0 37,21 0 5 1,80 0 0 45,21 0 3 0,64 0 0 46,21 0 1 0,6 0 0 65535,6 0 0 0" --dport {openvpn_port} -j ACCEPT')
os.system(f'iptables -A PREROUTING -t mangle -d {server_ip}/32 -p tcp -m conntrack --ctstate NEW -m comment --comment "ssh,pritunl" -s {home_ip}/32 --syn -m multiport --dports 22,443 -j ACCEPT')
os.system('iptables -A PREROUTING -t mangle -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
os.system('iptables -A PREROUTING -t mangle -i tun+ -j ACCEPT')
os.system('iptables -A PREROUTING -t mangle -i lo -j ACCEPT')

# Default policy change to 'DROP'.
os.system('iptables -t mangle -P PREROUTING DROP')

# Kernel settings to optimize performance against some attacks.
os.system('/sbin/sysctl -w net.ipv4.icmp_ignore_bogus_error_responses=1 > /dev/null')
os.system('/sbin/sysctl -w net.netfilter.nf_conntrack_max=250000000 > /dev/null')
os.system('/sbin/sysctl -w net/netfilter/nf_conntrack_tcp_loose=0 > /dev/null')
os.system('/sbin/sysctl -w net.ipv4.icmp_echo_ignore_broadcasts=1 > /dev/null')
os.system('/sbin/sysctl -w net.ipv4.conf.default.rp_filter=1 > /dev/null')
os.system('/sbin/sysctl -w net.ipv4.icmp_echo_ignore_all=1 > /dev/null')
os.system('/sbin/sysctl -w net.ipv4.conf.all.rp_filter=1 > /dev/null')
os.system('/sbin/sysctl -w net/ipv4/tcp_timestamps=1 > /dev/null')
os.system('/sbin/sysctl -w net.ipv4.tcp_syncookies=1 > /dev/null')

# firewalls.py script put together by Snax.