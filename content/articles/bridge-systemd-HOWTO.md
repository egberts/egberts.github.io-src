title: Setting up Bridge using Systemd in Debain9
date: 2020-07-10 14:35
modified: 2022-07-24 10:02
status: published
tags: bridge, systemd, debian9
slug: howto-bridge-systemd-debian9
category: HOWTO
summary: How to set up a bridge using Systemd in Debian 9

This article is for setting up a bridge using systemd on a Debian 9 platform.

Checklist
---------
Note: This article assumes that Predictable Network Interface Device Name is 
not enabled yet.  Check if `/etc/systemd/network/99-default.link` exists)

A bridge requires at least two Ethernet interfaces of any combination of the
following types:

* physical Ethernet (`ethX`)
* wireless Ethernet (`wlan0`)
* PPP (`ppp0`)
* VirtualBox host (`vboxnet0`)
* PAN (`pan0`)
* VMWare Network Bus (`vmnet1`, `vmnet8`)
* IP Tunnel (`tun0`)
* IPsec (`ipsec0`)
* IP-to-IP  (`ipip0`)
* Docker (`docker0`)
* loopback (`lo`)

General Design
--------------
Bridging in systemd are broken into three different kinds of configuration,
each representing an abstraction layer:

* network
* netdev
* link

Location of Config Files
------------------------
The location of systemd configuration files for networking are in:
```bash
cd etc/systemd/network
```
directory.

Naming Convention of `systemd/network/*` Config Files
--------------------------------
Since systemd is reading multiple files in the `/etc/systemd/network` 
subdirectory, some ordering is required to read all of these files.

The read order is by sorted by ASCII order: digits before alphabet letters.

Debian convention requires that all files in /etc/systemd/network must 
start with 2 digits and a dash symbol.

Number sequence is user-definable to achieve this sequence read ordering
of network interfaces.

**Note:** Any user-supplied *`.link`* **must** have a lexically earlier 
file name than the default config `99-default.link` in order to be 
considered at all. 
For example, name the file `10-ethusb0.link` works and ignores
`ethusb0.link`.

Load Ordering of Config Files
------------------------

Configuration files are located and loaded in the following priority order.  

1. the local administration network directory `/etc/systemd/network/` 
2. the volatile runtime network directory `/run/systemd/network/` and 
3. `/usr/lib/systemd/network/` 

There are three types of configuration files. They all use a 
format similar to systemd unit (or INI) files.

* **`.network`** files. They will apply a network configuration for 
a *matching* device
* **`.netdev`** files. They will create a *virtual network device* for a *matching environment*
* **`.link`** files. When a network device appears, [`udev`](https://wiki.archlinux.org/index.php/Udev) will look for the first *matching `.link`* file.

They all follow the same rules:

* If **all** conditions in the `[Match]` section are matched, the profile will be activated
* an empty `[Match]` section means the profile will apply in any case (can be compared to the `*` wildcard)
* all configuration files are collectively sorted and processed in lexical order, regardless of the directory in which they live
* files with identical name replace each other

Ideally, the load ordering of `network` config files are:

1. link - interface
2. link - bridge
3. netdev
4. network


Link Layer - Interfaces
=======================
For the following examples, two physical Ethernet interfaces shall be used.

The two ethernet interface names are `eth0` and `eth1`.  If you had
"Predictable Network Interface Device Names" turned on, then the link
name would be something like `enp3s0` and `enp3s1` as an example.

To set the default gateway interface to be on the first interface, this example uses `eth0`.

First Ethernet Link
-------------------

For `eth0`, create the config file named `10-eth0-wired-802.3.link`.
The file type must ends with `.link`.

The content of the `10-eth0-wired-802.3.link` would look like:

```ini
# File: /etc/systemd/network/10-eth0-wired-802.3.link
# Custom-made for you

[Match]
Path=pci-0000:03:00.0-*
Virtualization=no
Type=lan

[Link]
Name=eth0
MACAddress=00:1a:a0:b2:e3:9e
BitsPerSecond=1G

# WakeOnLan options: off, on, magic
WakeOnLan=magic
```

In the above example, an Ethernet PCI card in PCI 3 Slot 0 will be loaded
as a physical card with LAN type.  It's link name will be `eth0`
and have a custom MAC address and force setted to 1Gbps.  Also
the NIC card will be on standby to watch for any Wake-On-LAN magic value.


Second Ethernet Link
--------------------
For `eth1`, create the config file named `10-eth0-wired-802.3.link`.
The file type must ends with `.link`.

The content of the `13-eth1-wired-802.3.link` would look like:

```ini
# File: /etc/systemd/network/13-eth1-wired-802.3.link
# Custom-made for you

[Match]
Path=pci-0000:04:02.0-*
Virtualization=no

# If running as replacement to cable router, don't set MACAddress here, 
#    we're updating MACAddress at /etc/rc.local time.
# Otherwise, following must match before this link go active
##### MACAddress=00:0e:0c:00:c2:19
##### Host=my-laptop
##### Architecture=x86-64
##### Driver=brcmsmac
Type=lan

[Link]
Name=eth1
MACAddress=f8:e4:1c:4e:a0:02   # fake cable modem's MAC here
BitsPerSecond=1G
WakeOnLan=off
#### MTUBytes=1450
#### MACAddressPolicy=persistent
#### MACAddressPolicy=random
#### NamePolicy=keep
#### NamePolicy=kernel
```

netdev Config File
==================

netdev Bridge interface
----------------

First, create a virtual bridge interface that will tell systemd to create a 
device named `br0` to function as an ethernet bridge.

`vim /etc/systemd/network/30-bridge-br0.netdev`
and fill file with:
```ini
# File: /etc/systemd/network/30-bridge-br0.netdev
# These files will create network devices. They have two 
# sections: [Match] and [NetDev]. Below are commonly configured 
# keys for each section. See systemd.netdev(5) for more 
# information and examples.

[NetDev]
Name=br0
Kind=bridge
```

On host and container:

```console
$ ip a

3: br0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default 
    link/ether ae:bd:35:ea:0c:c9 brd ff:ff:ff:ff:ff:ff
```

Note that the interface br0 is listed but is still DOWN at this stage. 

Bind Ethernet to Bridge
-----------------------
The next step is to add to the newly created bridge a network 
interface. An interface that matches 
the name `en*` into the bridge br0 is being added below:

```bash
vim /etc/systemd/network/50-bind-br0-slave-eth0.network
```
and fill with:
```ini
# File: /etc/systemd/network/50-bind-br0-eth0.network

[Match]
Name=eth0

[Network]
Bridge=br0

# Gets rid of pesky 'degraded' state in networkctl tool.
LinkLocalAddressing=no
```

All ethernet interfaces binded to `br0` must not have DHCP or an 
IP address associated as the bridge requires an interface to 
bind to with no IP:, modify the 
corresponding /etc/systemd/network/MyEth.network 
accordingly to remove such IP addressing. 

Bridge Network
--------------
Now that the bridge has been created and has been bound to an 
existing network interface, the IP configuration of the bridge 
interface must be specified. 
This is defined in a third `.network` file, the example below uses DHCP.

`/etc/systemd/network/60-bridge-br0.network`
```ini
# File: /etc/systemd/network/60-bridge-br0.network
[Match]
Name=br0

[Network]
DHCP=ipv4
### or use IPAddress= for static IP
```

Boot Container to br0
---------------------
Add option to boot the container

To give a separate IP for host and container, one needs to Disconnect networking of the container from the host. To do this, add this option `--network-bridge=br0` to your container boot command.

```bash
systemd-nspawn --network-bridge=br0 -bD /path_to/my_container
```



Restart systemd-networkd.service to have systemd create the bridge. 
```bash
systemctl restart systemd-networkd.service
```

Link Diagnosis
--------------
Use following command to diagnosis link issues
```bash
udevadm test-builtin net_setup_link /sys/path/to/network/device
```

References
===========

* [systemd networkd config files](https://wiki.archlinux.org/index.php/Systemd-networkd#link_files)
* [systemd udev](https://wiki.archlinux.org/index.php/Udev)
