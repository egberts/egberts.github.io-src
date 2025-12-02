title: Gateway Setup using Gentoo (as a QEMU guest)
date: 2022-08-02 07:00
modified: 2025-07-13 01:56
status: published
tags: gateway, router, Gentoo
category: HOWTO
summary: How to set up a gateway using a cheap PC and Gentoo Linux OS.
slug: gateway-os-gentoo-setup
lang: en
private: False

If wanting to be running a Gentoo Gateway within a QEMU, see [installation of Gentoo Linux OS]({filename}gentoo-qemu-setup.md) firstly.


Then check for existing services:

```console
$ rc-status
$ rc-update show
$ eselect rc list default
```

Audit
----
```console
touch /var/log/sulog
chmod 0640 /var/log/sulog
```


Services
----

Disable unneeded services:
```bash
rc-update delete netmount
rc-update delete systemd-tmpfiles-setup boot
``` 
