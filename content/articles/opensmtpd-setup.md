title: OpenSMTPD, Dovecot, Debian
date: 2020-09-01 08:01
modified: 2022-04-04 10:35
status: published
tags: OpenSMTPd, Dovecot, Debian
category: HOWTO
summary: How to set up OpenSMTPD  with Dovecot on Debian 10.4.
note: Aborted in favor of exim4

Preparation
===========
* Installation
* Wireguard version check
* Selection of IP subnet for tunneling (10.9.1.1/30)
 
Installation
=============

```console
apt install opensmtpd opensmtpd-extras
```
It will enter into `dpkg-reconfigure` stage and prompt you with two questions:

* System mail name (i.e. example.tld)
* Root and postmaster mail recipient(s)

User Group
---------------
Add two users  and one group for maximum security.
* `_smtpd` is the daemon
* `_smtpq` is for user who wish to execute `mqueue` and examine mail queues.

```bash
mkdir /var/empty
useradd -c "SMTP Daemon" -d /var/empty -s /sbin/nologin _smtpd
useradd -c "SMTPD Queue" -d /var/empty -s /sbin/nologin _smtpq
```

Systemd Setup - Server-side
===========================

Systemd NetDev - Server-side
----------------------------
Create `/etc/systemd/network/98-wireguard.netdev` config file:
```ini
#
# File: /etc/systemd/network/98-wireguard.netdev
[NetDev]
Name=wg0
Kind=wireguard
Description=WireGuard tunnel wg0

[WireGuard]
ListenPort=51000
PrivateKey=MY_PRIVATE_KEY_ENDING_WITH_EQUAL_SYMBOL
```

Systemd Network - Server-side
-----------------------------
Create `/etc/systemd/system/network/98-wireguard.network`:
```ini
#
# File: /etc/systemd/network/98-wireguard.network
[Match]
Name=wg0

[Network]
# Choose the first address within the rnage, and mark the subnet
Address=10.9.1.1/30
```

Then start it up
```bash
sudo systemctl restart systemd-networkd
ip a | tail -d
sudo wg
```
It's up, but no traffic yet.

Netfilter - Server-side
-----------------------

```bash
sudo nft add rule inet filter input udp dport 51000 accept
```

Systemd Setup - Client-side
===========================

Systemd NetDev - Client-side
----------------------------
Create `/etc/systemd/network/98-wireguard.netdev` config file:
```ini
#
# File: /etc/systemd/network/98-wireguard.netdev
#
# Client
[NetDev]
Name=wg0
Kind=wireguard
Description=WireGuard tunnel wg0 (client-side)

[WireGuard]
ListenPort=51000
PrivateKey=SERVER_S_PRIVATE_KEY_ENDING_WITH_EQUAL_SYMBOL

#[WireGuardPeer]
## Public key of other peer, used ffor secure authorization between them
PublicKey=SERVER_S_PUBLIC_KEY_ENDING_WITH_EQUAL_SYMBOL
## a list of comma-separated IP addresses that should be routed through this peer
#AllowedIPs=10.91.0.2
## Endpoint is where to find the peer.  Once other peer sends an authenticated
## packet, this will be updated to the correct address, but it is still
## required ffor an initial meeting point
# Endpoint=your-vpn.example.tld:51001
```

Systemd Network - Server-side
-----------------------------
Create `/etc/systemd/system/network/98-wireguard.network`:
```ini
#
# File: /etc/systemd/network/98-wireguard.network
[Match]
Name=wg0

[Network]
# Choose the first address within the rnage, and mark the subnet
Address=10.9.1.1/30
```

Then start it up
```bash
sudo systemctl daemon-reload
sudo systemctl restart systemd-networkd
ip a | tail -d
sudo wg
```
It's up, but no traffic yet.

Netfilter - Server-side
-----------------------

```bash
sudo nft add rule inet filter input udp dport 51000 accept
```


References
==========
* https://bertptrs.nl/2020/08/15/setting-up-wireguard-vpn.html

References
==========
* https://bertptrs.nl/2020/08/15/setting-up-wireguard-vpn.html

