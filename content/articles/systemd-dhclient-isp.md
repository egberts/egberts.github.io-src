Title: Systemd and ISC DHCP Client
Date: 2018-10-14T16:23
Modified: 2022-02-24 12:13
Status: published
Tags: dhclient, DHCP, systemd, ISP
Category: research
Summary: How to integrate ISC DHCP client into a systemd-based workstation.

This page is about using ISC DHCP client (\`dhclient\`) in
[systemd](systemd "wikilink") environment.

I must be one of the surviving user that uses both ISC dhclient and
systemd.

Primarily because systemd DHCP cannot handle DHCP-Options (not options,
but Options). The ones that Juniper JunOS DHCP server requires for
Verizon FiOS.

So, here begins the long saga of a blog (that I might break up in
several blogs)...

First thing first, to do an analysis of systemd unit inter-dependencies,
I executed:

```bash
systemd-analyze dot --order \
    nginx.service network-pre.target network-online.target \
    network.target system-dhclient.slice \
    sys-subsystem-net-devices-eth1.device \
    networking.service nss-lookup.target shorewall.service bind9.service \
    dhclient@eth1.service  ddclient.service resolvconf.service \
    system-dhclient.slice  \
    > /tmp/custom.gv
```

As one can see that most people don't have dhclient@eth0.service systemd
unit file.

We are going to create a .gv file and convert it to SVG as shown below:

```bash
dot -Tsvg < /tmp/custom.gv > /tmp/custom.svg
firefox /tmp/custom.svg
```

ISC DHCP CLient
---------------

And I finally got my very own Linux gateway to be hooked up to the
Verizon HFC network, instead of using ActionTek wireless broadband
router.

Details in here: [Github egberts/systemd-dhclient](https://github.com/egberts/systemd-dhclient)

<code>/etc/systemd/network/dhclient$.service<code>
--------------------------------------------

It is also possible to explicitly tell systemd-networkd to ignore a link
by using Unmanaged=yes option, see systemd.network(5).
