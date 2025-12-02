title: Port Knocking for Netfilter
date: 2021-09-26 08:00
status: published
tags: netfilter, firewall, security
category: HOWTO
lang: en
private: False

This article details the implementation of port knocking using Netfilter.
Port knocking can be used for SSH protection (but also for 
REST-based API as well).

WARNING: If you intend on using port knocking to obscure the SSH port, make sure
you have an alternative access method (i.e., physical terminal console via tty1 or ttyS0, or accessible by VNC, SPICE, IPMI, or AMT protocol), which will come in handy if you accidentally lock yourself out.

INFO: You should already be practicing and enforcing pubkey-only authentication for your SSH servers; because port knocking is literally "security through obscurity" and should not be that only method on which to rely on for your security needs.

INTRO
=====
Netfilter is the latest generation IP filtering for Linux platform, supplanting
`iptables` and its ancestor, `ipfilter`.

A quick check to see if your OS supports Netfilter is to run:

```
   $ nft -v
```
and the response should be something like
```
nftables v0.9.8 (E.D.S.)
```

Design Approaches
=================
The different design approaches for performing port-knocking are:

* Log monitoring, via detection of syslog files
* Packet monitoring, via tap port (or libpcap)
* NETLINK monitoring
* Stateful network filtering, by chaining
* Stateful network filtering, by event tracking

Log Monitoring
--------------
Log monitoring approach is to start a daemon that reads the log file, that were written by syslog daemon who in turn monitors the UNIX sockets (ie., /proc/kmsg, /run/systemd/journal/syslog), for any log message written by netfilter kernel module.

String and regex patterns are used to look for certain log messages reported by
P filter (such as `iptables` or `nftables`) kernel modules.

A daemon would then watch for a certain sequence of port numbers in its log file and determine its accessibility of the secured port in question.

Its advantages are that it can allow maximum flexibility in what user can write
their shell script to dispatch. 

Downside is that this approach is prone to breakage, most
notably the fixed text pattern as reported by kernel modules and detected by such daemon are subjected to their respective upgrades.
Not many port knocking package that are the log monitoring approach have appropriate unit test to ensure that such text matching are properly aligned and working between its kernel and the daemon.  

Anecdote:  While remotely logged in using SSH, an OS upgrade may appear to have completed normally, but a reboot can lock the SSH login down.

SECURITY: Protection against malicious local user would require that its daemon's configuration file and /var/log/<files> need to be locked down.  Drop the file permission of the `lsof` and `ss` binaries to 0750 and change the file's group ID to something like `adm` or `staff`.

`fail2ban` is package that does this method.
`knockd` by ZeroFlux is another package that does this method.

Packet Monitoring
-----------------
The design approach for packet monitoring comes in two flavors:

* network interface (netdev) device monitoring
* multiple BSD sockets

Promiscuous network interface is an interface that will receive any and ALL network packets from its netdev interface (whether it matches its own IP address or not).

It leverages PCAP `libpcap` library for examination of network packets that comes in on the selected network interface (netdev) device.  This one takes the most CPU overhead of any design approaches.


Packet Monitoring approach offers the most flexibility via shell scripting in responding to customized scenario.  Whereas, Netfilter cannot dispatch to a shell script.

Using a daemon approach in which to open NETLINK\_NETFILTER BSD raw sockets does reveal which ports are being listened to from within the OS (ie., `lsof -i -n`  or `ss -l`).

Stateful Network Filtering
--------------------------
Stateful Network Filtering is the act of making decision on packets within its
network filters.   

Netfilter (and iptables) have supports for registering, tracking, and responding
to events, which all that makes for a stateful firewall.

In stateful network filtering, the filter ruleset is communicated through a NETLINK\_NETFILTER BSD raw sockets 


NETLINK Monitoring
------------------
fwknop?

/proc/net/xt\_recent


Port Sequences
==============
There are a several methods of setting up Netfilter-based port knocking:

* Single-port, same port number for open/close
* Single-port, separate port number for open/close
* Port sequence, same sequence for open-close
* Port sequence, separate sequence for open/close 
* One-Time-Port, list-modulo-based
* One-Time-Port, time-based
* One-Time-Port, pseudo-random with pre-established random seed

Some side features are:

* Manual open/close switch
* Expiration timer, no new UDP connections
* Expiration timer, brute force cut-off.
* Faux UDP data payload (canned or custom)

This article will start at the port sequence using separate port sequences for each for open condition and close condition.

Port Sequence, Separate Open/Close Sequences
--------------------------------------------

