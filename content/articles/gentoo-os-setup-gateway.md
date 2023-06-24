title: Gateway setup in Gentoo OS
date: 2022-09-08 09:56
status: published
tags: Gentoo
category: HOWTO
summary: How to set up Gentoo OS for a gateway
slug: gentoo-setup-gateway
lang: en
private: False


Download the Gentoo minimal install CD
Burn the CD
Boot the CD


== Partition ==

Partition the hard drive, using LVM approach:

Two physical partitions shall be created:

* OS and 
* logging data

This complies with CISecurity.

```bash
fdisk /dev/sda
```
Create four physical partitions on hard drive /dev/sda:

* `/dev/sda1`, ext4, boot, 2GB
* `/dev/sda2`, swap, twice the size of installed physical RAM
* `/dev/sda3`, ext4, root, remainder of hard drive space
* `/dev/sda4`, ext4, log, 60GB

Change the partition types as well:

* `/dev/sda1`, type 82 (Linux)
* `/dev/sda2`, type 83 (swap)
* `/dev/sda3`, type 8e (Linux LVM)
* `/dev/sda4`, type 8e (Linux LVM)

Exit `fstab` by entering 'w'rite menu option.


== Create logical partitions ==

```bash
pvcreate /dev/sda3
pvcreate /dev/sda4

vgcreate vg_root /dev/sda3
vgcreate vg_log /dev/sda4
vgchange -l5 -p1 vg_root 
vgchange -l3 -p1 vg_log 

lvcreate -L48G -nlv_root vg_root
lvcreate -L24G -nlv_tmp vg_root
lvcreate -L80G -nlv_var vg_root
lvcreate -L256G -nlv_usr vg_root
lvcreate -L456G -nlv_home vg_root

lvcreate -L24G -nlv_var_log vg_log
lvcreate -L50G -nlv_var_log_audit vg_log
lvcreate -L50G -nlv_var_tmp vg_log
```

== Format partitions ==

```bash
mkfs.ext4 /dev/sda1

mkswap /dev/sda2

mkfs.ext4 /dev/vg_root/lv_root
mkfs.ext4 /dev/vg_root/lv_tmp
mkfs.ext4 /dev/vg_root/lv_var
mkfs.ext4 /dev/vg_root/lv_usr
mkfs.ext4 /dev/vg_root/lv_home

mkfs.ext4 /dev/vg_log/lv_var_log
mkfs.ext4 /dev/vg_log/lv_var_log_audit
mkfs.ext4 /dev/vg_log/lv_var_tmp
```

== Networking ==

Setup networking using DHCP client (this assumes a working DHCP server on the local LAN):

```bash
net-setup enp0s25
```

Follow instruction



== Post Bootup ==
=== Networking ===
==== IP forwarding ====

for all virtual and private LAN to NAT out to the public network:
```bash
echo "ip.ipv4.ip_forward = 1" > /etc/sysctl.d/10-ip_router_forwarding.conf
echo "ip.ipv4.conf.all.ip_forwarding = 1" > /etc/sysctl.d/10-ip_router_forwarding.conf
```

for certain virtual and private LAN to NAT out to the public network:
```bash
echo "ip.ipv4.ip_forward = 1" > /etc/sysctl.d/10-ip_router_forwarding.conf
echo "ip.ipv4.conf.private_br0.ip_forwarding = 1" > /etc/sysctl.d/10-ip_router_forwarding_gateway_nat.conf
echo "ip.ipv4.conf.virtual_virbr15.ip_forwarding = 1" > /etc/sysctl.d/10-ip_router_forwarding_gateway_virtual_net.conf
```
