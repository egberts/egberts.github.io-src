title: Dual NICs, same IP subnet
date: 2021-12-1 21:00
status: published
tags: Linux, network, IP, subnet, NIC
category: HOWTO
summary: How to make multiple IP addresses of same subnet work across different
netdev interfaces: a Linux route table exercise.
lang: en
private: False

Requirement
===========
Requires Linux 4.19.0 or Linux 5.11.1 and 

One of the following network managers:

* ifupdown (v0.8.35)
* systemd (v247)
* NetworkManager (v1.14.6)

Prelude
=======
I got two Ethernet ports to share the same IP subnet and they properly
ping out and in to their respective IP address.  Wasn't hard, but
certainly not easy.

Various internet searches for "same subnet, multiple interfaces" have all 
said about the same thing: "Not a good idea", "don't do it", 
"Linux isn't that strong of a router type".

Well, I'm doing it. And got it to work with the latest Linux kernel v5.15.

Why do this crazy stuff despite tremendous chorus of Internet nay-sayers?  
Because Linux Route Tables are powerful stuff and needs to be tamed.

Besides, having a management port makes it easier to:

1. troubleshoot the non-management traffic (no foot-gun in case of firewall
   tweak failures)
2. Filter management traffic to a specific netdev interface.  (security separation)
3. if the router goes down, management port will still be accessible
   (robustness, readiness, availability)
4. container/LXC/Docker/VM network traffic are separate
   (main traffic performance, terminal responsiveness)

Not entirely undoable.  But not entirely un-orthodox either.

The most common yet simplistic way to do this, two different IP addresses 
of the same subnet amongst different NIC netdevs on the same box, has
pretty much always resulted in network traffic going out only the 
netdev interface having a gateway.

NOTE: Assigning multiple gateway to different netdev interfaces always
results in a failure ... without additional assist from Linux route tables.

To ACTUALLY be able to ping out and receive at their respective NIC, 
these steps will actually show you how (to do this with advanced Linux 
networking).

EXPERT NOTE: We borrowed a trick from
[VVRP](https://en.wikipedia.org/wiki/Virtual_Router_Redundancy_Protocol).

We also found out that our trick (of using multiple IP address of the same 
subnet across multiple netdev interfaces) also lends itself and 
works very well toward multiple VLANs.   

Preparation
===========

Choose an integer between 1 and 32767 to be your new table ID.  We will need
two tables; that is, two unique integers.

Consult `/etc/iproute2/rt_tables` as a guide to ensure that your desired
number has not already been taken.

Leave `rt_tables` file UNCHANGED as your distro maintainer most likely will
overwrite them at your next packages update.

Alias Name
----------
Cannot remember the number?  Slap a name of your choice on it.  Route table
supports alias, or name equivalent of your integer choices.

To map an alias name of your route table ID, create a config file under 
`/etc/iproute2/rt_tables.d` subdirectory.

File: `/etc/iproute2/rt_tables.d/my_networks.conf`
```ini
# This article created two new route table aliases
# whose integers are unique and not reserved earlier 
# by other /etc/iproute2/rt_tables[.d/*]

512 my_mgmt
513 my_data
```

Now we have `my_mgmt` and `my_data` route table aliases: more strong-typing,
less memorization.

NOTE: Much like `/etc/host` or `/etc/services`, the `rt_tables` is a CLI-helper
and is not used beyond command lines: just to obtain the ID of the desired route
table or to pretty-print outputs of route tables by route-related tools.

How are Route Tables Made
-------------------------
Route tables are created ONLY through the `table XXXX` argument options 
of `ip route add`.

    ip route add 999.999.999.999 .... table XXXXX

Table argument can be an integer or a pre-defined alias name provided by
`/etc/iproute2/rt_tables[.d]*` file(s).


STEPS to Multiple Same-Subnet IP Addresses on Different Netdevs
===============================================================

Define the route pathways to the `eth0` interface:
```bash
ip route add 10.1.0.0/16 dev eth0 src 10.1.1.12 table my_mgmt
ip route add default via 10.1.1.1 dev eth0 table my_mgmt

# See what we put in
ip -4 -o route show table my_mgmt
```

For route pathways inbounding to the `eth1` interface:
```bash
ip route add 10.1.0.0/16 dev eth1 src 10.1.1.13 table my_data
ip route add default via 10.1.1.1 dev eth1 table my_data

# See what we put in
ip -4 -o route show table my_data
```

For rules on outbound IP from the `eth0` interface
```bash
ip rule add table my_mgmt from 10.1.1.12
# or
ip rule add from 10.1.1.12 table my_mgmt 
```

For rules on outbound IP from the `eth1` interface
```console
ip rule add table my_data from 10.1.1.13
# or 
ip rule add from 10.1.1.13 table my_data
```


Some kernel sysctl settings required are to be placed in `/etc/sysctl.d`
subdirectory.

```ini
net.ipv4.conf.all.arp_filter = 1
net.ipv4.conf.default.arp_filter = 1
net.ipv4.conf.all.arp_announce = 2
net.ipv4.conf.default.arp_announce = 2

net.ipv4.conf.default.rp_filter = 2
net.ipv4.conf.all.rp_filter = 2
net.ipv4.conf.eth0.rp_filter = 2
net.ipv4.conf.eth1.rp_filter = 2
```

Your network manager setup
==========================

Make both `eth0` and `eth1` have the following characteristics
with your choice of network manager:
NetworkManager, ifupdown, systemd-network.  Sorry, SysV, conman, s6 and OpenRC.

* Type: Ethernet
* Boot: IP static
* Default route: no
* Onboot: yes
* Gateway: (only for eth0)
* Disable other choices of NM: yes
* enable 'ignore-carrier' option (systemd has 'RequiredForOnline=')


ifupdown Setup
--------------
File: `/etc/network/interfaces.d/eth0.conf`
```ini
auto eth0
iface eth0 inet manual
    no-auto-down
    address 10.1.1.12
    netmask 255.255.255.0
    gateway 10.1.1.1
```

File: `/etc/network/interfaces.d/eth1.conf`
```ini
auto eth1
iface eth1 inet manual
    no-auto-down
    address 10.1.1.13
    netmask 255.255.255.0
    gateway 10.1.1.1
```

If using OTHER network manager to manage this eth0/eth1 interface as well as 
ifupdown for other interfaces), these eth0/eth1 MUST be DELETED (or commented
out) from
its applicable section of its `interfaces[.d/*.conf]` file, as a minimum.

systemd-network Setup
---------------------
Four configuration files are used:

- eth0.link
- eth1.link
- eth0.network
- eth1.network

File: `/etc/systemd/network/35-eth0.link`
```ini
[Match]
Type=lan
Virtualization=no

[Link]
Name=eth0
RequiredForOnline=no
WakeOnLan=off
```

File: `/etc/systemd/network/36-eth1.link`
```ini
[Match]
Type=lan
Virtualization=no

[Link]
Name=eth1
RequiredForOnline=no
WakeOnLan=off
```

NOTE: There are no `.netdev` for Ethernet-type netdev interfaces.

File: `/etc/systemd/network/45-eth0.network
```ini
[Match]
Name=eth0

[Network]
DHCP=no
Address=10.1.1.12

DNS=10.1.1.1
Gateway=10.1.1.1
Unmanaged=no

# DHCPServer=0
```

NetworkManager Setup
--------------------
File: `/etc/systemd/network/46-eth1.network
```ini
[Match]
Name=eth1

[Network]
DHCP=no
Address=10.1.1.13

DNS=10.1.1.1
# No 'Gateway=' here
Unmanaged=no

# DHCPServer=0
```

If using OTHER network manager to manage this interface as well as 
systemd-network (for other interfaces), the
`Unmanaged=yes` item must be in its `*.network` file, as a minimum.

NetworkManager Setup
--------------------

If using OTHER network manager to manage this interface as well as 
systemd-network (for other interfaces), the
`Unmanaged=yes` item must be in its `*.network` file, as a minimum.

Ignore Ethernet Carrier
=======================

NOTE: Option to ignore Ethernet carrier is somewhat important part because
during a failover, a virtual bridge will go OFFLINE when the 'last-man
standing' physical bridge-slave Ethernet port goes OFFLINE.  

To prevent a virtual bridge from going into OFFLINE state
and continue to facilitate network traffic between VMs, each physical 
slave-port of a bridge must have its carrier status ignored.

Final Act
=========

Reboot the box.

Verification
------------
Verify the setup:

```console
sudo -s

# ip route show table my_mgmt
default via 10.1.1.1 dev eth0 
10.1.0.0/16 dev eth0 scope link src 10.1.1.12 

# ip route show table my_data
default via 10.1.1.1 dev eth1 
10.1.0.0/16 dev eth1 scope link src 10.1.1.13 

# ip route show
10.1.1.0/24 dev eth0 proto kernel scope link src 10.1.1.12 
10.1.1.0/24 dev eth1 proto kernel scope link src 10.1.1.13 
169.254.0.0/16 dev eth0 scope link metric 1002 
169.254.0.0/16 dev eth1 scope link metric 1003 
```

Validation
----------
Then validate the connectivity

```console
# ping -I 10.1.1.12 8.8.8.8
PING 8.8.8.8 (8.8.8.8) from 10.1.1.12 : 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=61 time=10.6 ms

# ping -I 10.1.1.13 8.8.8.8
PING 8.8.8.8 (8.8.8.8) from 10.1.1.13 : 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=61 time=10.5 ms

Ping form hypervisor to VM IP's works now.

# ping 10.1.1.12
PING 10.1.1.12 (10.1.1.12) 56(84) bytes of data.
64 bytes from 10.1.1.12: icmp_seq=1 ttl=64 time=0.223 ms

# ping 10.1.1.13
PING 10.1.1.13 (10.1.1.13) 56(84) bytes of data.
64 bytes from 10.1.1.13: icmp_seq=1 ttl=64 time=0.189 ms
```

Enjoy.


References
==================
* [Iqonda blog](https://blog.iqonda.net/linux-routing-two-interfaces-on-same-subnet/)
* [Anders Brownworth blog](https://andersbrownworth.com/cms/258)

