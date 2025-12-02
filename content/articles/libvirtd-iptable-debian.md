title: Debian 11 SNAFU with virt-manager
date: 2022-07-20 08:32
modified: 2025-07-13 02:05
status: published
tags: libvirt, Bullseye, Debian, nftables
category: HOWTO
summary: 
slug: virt-manager-debian-11-snafu
lang: en
private: False

So I get this cryptic error message from `libvirt` while running `virt-manager`:

```
libvirt.libvirtError: internal error: 
  Failed to apply firewall rules /usr/sbin/iptables -w --table nat --list-rules: 
    iptables v1.8.7 (nf_tables): table `nat' is incompatible, use 'nft' tool. 
```

And I google-fu the heck out of that error message, and NONE provided a suitable answer.

After a code review of libvirt, it turns out NOT to be a bug.

# NOT A BUG?

Yeah, not a bug for any software, except in the admin's mind where that error occurred.

# HOW?

It is actually a poor choice of wording in the error message:

```
  (nf_tables): table `nat' is incompatible, use 'nft' tool.
```

There is a duke'm-out going on over between:

* system administrator
* virt-manager

over the table name 'nat'.


As a system administrator, just rename the NFT table 'nat' name to something else.  `libvirt` library (via `virt-manager`) already laid claim to the table name `nat`.  Do not fight against this one.  Save yourself some headaches.

One can find the unneeded but competing table name declaration in one of the following files:

* `/etc/nftables.conf`
* `/etc/nftables.d/*.conf`


# Conclusion

Stupid error message wordings.

The hazard of implementing different blogs' NAT-bridge setup for virt-manager.

Problem-solved.

# Cooling Off Period

Could have reworded to as:

```
'nat' table name has been defined already; rename it.
```

"Rename it" to be meaning that `libvirt` laid claim to the name.



