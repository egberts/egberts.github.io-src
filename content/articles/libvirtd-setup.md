title: Set up libvirtd daemon
date: 2022-07-20 08:18
status: published
tags: libvirt, libvirtd
category: HOWTO
slug: libvirtd-setup
lang: en
private: False
summary: How to setup libvirtd daemon in Debian 11

So, Debian apt packaging threw me in for a curve.

My entire `libvirtd` somehow had been disabled and removed from my installed list.

A simple `apt install libvirt-daemon` did NOT fix the problem anymore.

Debian introduced about 8 more packages that are required to properly run a `libvirtd`.

* `libnetfilter-cthelper0`
* `libvirt-daemon-system-systemd`
* `libip6tc2`
* `libvirt-daemon-config-nwfilter`
* `libvirt-daemon-config-network`
* `jq`
* `libjq1`
* `mdevctl`

I am quite sure that I did not do a correct install of libvirtd, et. al. by using the
proper package name.  If I had only a clue as to what this correct package name is.

Anyway, those are the missing packages needed by `virt-manager`.

