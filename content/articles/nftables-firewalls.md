title: nftables and firewalls
date: 2022-09-10 09:09
modified: 2022-09-21 15:58
status: published
tags: nftables, firewalls, libvirt, firewalld
category: research
summary: Summary of nftables and its coexistence with firewalls
lang: en
private: False

This article details my running notes the analysis of latest `nftables` and its integration into various firewalls.

My goal is to use `virt-manager` (a GUI front-end), `libvirt` and `nftables` ... all together. 

The problem with this goal is that XML is required for formatting additional ruleset for inclusion by `nwfilter` (a part of Libvirt network firewall).  Did I mention that I vehemently hate XML?

Where am I going to put some 538 rules into `nftables`? And in firewall DEFAULT-DENY scenario?  Surely, I am going to type up some 4,786 lines of new firewalls lines ... in XML, NOT!

So, this requires me studying various firewalls and its ability to co-exist together.

The integration of nftables and its various firewalls having been reviewed here are:

* nwfilter (libvirt/libvirtd)
* firewalld (RedHat)
* systemd nftables.service
* Shorewall (Perl-based)

`ufw` is not reviewed here as it is not nftables-friendly.

So, let's start looking at firewalls.




# Overview of coexistence with nftables 

The basic aspect a firewall being able to be coexisting with `libvirt` (and `nftables`) boils down to:

* who is in control (start/restart/stop) overall
* who can control the nftable policy
* who can control segregation by netdev interfaces (common FW chaining organizational technique)
* who can insert FW rules effortlessly into an existing FW ruleset without corrupting other ruleset.

None of this matter to my goal if you simply take out the `default` Virtual Network from `virt-manager`.

But I am determined to make it work with `virt-manager` and a firewall of MY choice.

If you're happy with `virt-manager` but want 100% control of your `nftables` ruleset, then execute:

```bash
virsh net-autostart --disable default
virsh net-destroy default
```

then stop reading this article: the `/etc/nftables.conf` config file is 100% yours to play with.  I was there, I used to do that, but I wanted MOAR!

I do NOT want 100% control of my `nftables`. But I wanted different applications to play fair and SOMEHOW share this `nftables` ruleset/tables/chain/rules.

I do want `virt-manager`/`libvirt` to automatically insert custom firewall settings on a per-VM/container basis using painful XML typing, so that is what the rest of this article is about: partial-control and sharing of `nftables` control between my own `/etc/nftables.conf` and `libvirt`/`nwfilter`.

And I get to keep using my favorite `virt-manager` within a supremely complex firewall environment.

`virt-manager`, `libvirt`, and my `nftables` ... all together; the way it should be.


## virt-manager

virt-manager is a Python3 front-end script to both `libvirt` and `qemu-system-x86_64`.  Works on KDE and Gnome equally; also leverages `gnome-keyring` and `kwalletcli` for proper password storage.

`virt-manager` is not very flexible enough to handle complex network scenario outside of multiple sets of simple bridge, NAT, routed, and closed-net.  We will be keeping the 'Virtual Network' capability of this GUI but we ditch the `default` one.

`virt-manager` cannot customize firewall rules directly at GUI-level but would let you edit (should I say, bastardize) the XML-formatted `/etc/libvirt/network/your-virtual-network-name.xml` file and insert zany XML prose's.  With my 538 rules times 8-9 lines required for each rule to type up, I'd say "no thanks" to +4,800 lines.

virt-manager does NOT remove whatever table/chain it created under 'Virtual Network' after first/last VM gets removed.  That's the job of `libvirt` and its API.  And `libvirt` does not remove chains either.


## libvirt

libvirt is an API library that can manage virtual machines and containers (QEMU, Xen, LXC, Docker).  `libvirt` can also crafts firewall rules for its many network segmentation (`virt-manager`'s 'Virtual Network') needed by different groups of virtual machines.  Unrelatedly, `libvirt` handles storage too.

Ease of configuration with `libvirt` is considered extremely hostile toward user-friendliness and [poorly documented](https://avdv.github.io/libvirt/formatnetwork.html#examplesBridge): it uses XML-formatted config files; totally devoid of working examples.

This inability to clean up stray chains after dying itself is the dangling artifact of libvirt/libvirtd.  And this lingering effect of `nft list ruleset` really becomes problematic when it comes to expansion of custom FW rules and maintaining co-existence with other firewall daemons. 


## libvirtd

libvirtd is a daemon that facilitates the `virsh` CLI and `virt-manager` GUI.  Handles nearly everything VM, network, and storage.

Sad thing is `libvirtd` does read and store configuration files but in XML-format ... only.

Killing the `libvirtd` does not clean up after itself; much less affect the entire `nftables`; it is the latter that matters most.

Restarting the `libvirtd` DOES create new chains, lots of chains, lots and lots of chains.  Purported SIGHUP signal to `libvirtd` supposedly reloads the firewall rules, but that has been disabled as of `libvirt v7.0` on Debian 11.

Also, to those who are in the "DEFAULT-DENY" firewall camp, your `nftables` ruleset requires a delta-one priority-wrapper ruleset around the following nftables chain names that got defined by `libvirtd` daemon:

* ip filter `LIBVIRT_INP`
* ip filter `INPUT`
* ip filter `LIBVIRT_OUT`
* ip filter `OUTPUT`
* ip filter `LIBVIRT_FWD`
* ip filter `FORWARD`
* ip filter `LIBVIRT_FWI`
* ip filter `LIBVIRT_FWX`
* ip nat `LIBVIRT_PRT`
* ip nat `POSTROUTING`
* ip mangle `LIBVIRT_PRT`
* ip mangle `POSTROUTING`

I am only thankful that the `libvirtd` is only creating chain policy of `accept`.  This makes it easier to wrap around each chain that is required with a `drop` (DEFAULT-DENY) policy scenarios.

As a default, `libvirtd` daemon inserts its own type/hooks/priority/policy into the nftables.  This makes co-existence slightly more difficult with other firewall (and is considered a part of the RedHat walled garden strategy).  An easy workaround is for your custom `nftables` ruleset to bump its priority ([more negative value](https://egbert.net/blog/articles/netfilter-priority-levels.html)) to a higher priority than `libvirt`'s filter (0) priority:  a priority value of +1 should suffice in performing ruleset before `libvirt` and a priority value of -1 should suffice in performing ruleset after `libvirt`.  Not many firewall daemons would let you set this priority (Shorewall, UFW, firewalld).

Disabling libvirt network is still not recommended given their power to handle opening and closing pin-holes via builtin `libvirt` API (or you could also do it with `/etc/libvirt/hooks/qemu.d` scripting).  This auto-pin-holing further cements the zeal to get both `libvirt` and `nftables.service` working ... TOGETHER.


# Comparing a firewall with nftables

## Shorewall

Shorewall (much like systemd `nftables.service`) is a one-shot daemon-less Perl-script that reads various text-based configuration files covering domain, network segments, physical interfaces, masquerading, static route.  Shorewall remains the excellent tool for a default-deny firewall setup.

Shorewall does entire replacement of ruleset, including overriding any existing  nftables ruleset.  This makes co-existence with all firewall daemon problematic.

Dynamic pinhole (port forwarding) support is not there.

Shorewall has not been upgraded to use nftables, so setting priority level on a chain is not supported.  Shorewall however does make use of `iptables-nft` but still cannot set priority level +/-1 to co-exist with libvirt.

Shorewall is basically dead-on-arrival unless you are not using `libvirt`.


## firewalld

firewalld is a daemon that is a RedHat walled-garden approach to administering host firewall.  Its design is complicated by several things:

* all configurations are in unfriendly multiple-line XML format for each setting
* octopus out into D-Bus communication pipe (for desktop-initiated FW pinholing)
* not usable for complex firewall environments.
* cannot support default-deny firewall setups.
* crushes Docker firewall settings

I am biased toward the K.I.S.S. and that I think one thing should do one thing well, and this `firewalld` is anathema to this KISS principle.


## systemd nftables.service

`nftables.service` is a systemd unit service file that performs a one-shot daemon-less configuration of Linux `nftables` firewall using `nft` CLI tool and `/etc/nftables.conf` as its initial setup.

No other systemd service depends on `nftables.service`.

Note: this is the end-of-the-line for `nftables.service`; I assert that this is a mistake.  More on this later.


Default `nftables.service`  firewall ruleset is:

```
table inet filter {
	chain input {
		type filter hook input priority filter; policy accept;
	}

	chain forward {
		type filter hook forward priority filter; policy accept;
	}

	chain output {
		type filter hook output priority filter; policy accept;
	}
}
```
as derived from `/etc/nftables.conf`.


Reiterating, `libvirtd` creates the following FW chains:

* ip filter `LIBVIRT_INP`
* ip filter `INPUT`
* ip filter `LIBVIRT_OUT`
* ip filter `OUTPUT`
* ip filter `LIBVIRT_FWD`
* ip filter `FORWARD`
* ip filter `LIBVIRT_FWI`
* ip filter `LIBVIRT_FWO`
* ip filter `LIBVIRT_FWX`
* ip nat `LIBVIRT_PRT`
* ip nat `POSTROUTING`
* ip mangle `LIBVIRT_PRT`
* ip mangle `POSTROUTING`

Noticed the lowercase `input` and uppercase `INPUT` chain name?  Yeah, no relation; just separate chains.

Note: Another mistake is not leveraging priority level to distinguish between `libvirtd`-generated ruleset and `nftables.service` ruleset.  More on this in section Re-prioritization.

As a default, `systemctl start nftables.service` flushes the entire `nftables` and reconstructs the FW ruleset from `/etc/nftables.conf` file.  This basically blows away any possibility of co-existing with any other firewall daemons or libvirt, as-is.


### systemd with nwfilter/libvirt

Removal of `nft flush ruleset` from `/etc/nftables.conf` is highly recommended when using with libvirtd daemon.  

`libvirtd` daemon can be made to NOT touch the `nftables` ruleset.  Disabling libvirt network is still not recommended given `libvirtd` insightful power to handle the opening/closing of pin-holes for each container/VM.

possible, but it requires changes to `/etc/systemd/system/nftables.service` to split the 'restart/reload' as to be able to perform this extra table/chain-specific flushing from a separate `/etc/nftables-flush.nft` file as not to touch other subsystem's firewall settings, none that are provided by Redhat.

 The only thing to remember during crafting FW rules is to execute:

```bash
systemctl stop libvirtd.service
# yeah, not an optimal step here (stopping all VMs/containers)
systemctl stop nftables.service
systemctl start nftables.service
systemctl start libvirtd.service
```

As you can see, the above steps kills the VMs/containers but only during each crafting of initial firewall settings.

`/etc/nftables-libvirt-flush.nft` contains:
```
flush chain systemd_filter SYSD_INPUT
flush chain systemd_filter SYSD_OUTPUT
flush chain systemd_filter SYSD_FORWARD
```

Also, there should be some kind of reloading of libvirtd network firewall from the `systemctl reload libvirt.service` approach.  Not seeing RedHat as being eager to implement this.

And that in systemd-parlance, the `libvirt.service` should be dependent on this `nftables.service` as being successful before starting itself up.  Again, not in RedHat's walled-garden design either.


# Final Consideration

By choosing both `libvirt` and `nftables.service` together, we should be able to  get the best of both complex firewall setup as well as the VM-specific `nwfilter` part of `libvirt`.

This `flush rulset` line must be edited out from `/etc/nftables.conf` and replaced with the following multi-line:

```nft
flush chain ip nat PREROUTING
flush chain ip nat OUTPUT
flush chain ip nat POSTROUTING
# the name of table 'filter' is controlled by libvirt
flush chain ip filter LIBVIRT_INP
flush chain ip filter LIBVIRT_OUT
flush chain ip filter LIBVIRT_FWD
flush chain ip filter LIBVIRT_FWI
flush chain ip filter LIBVIRT_FWX
# the name of chain 'INPUT' is also controlled by libvirt
# to get around that, we make our nftables.service use a different name
# and prioritize it before this 'INPUT' chain
flush chain filter INPUT
flush chain filter OUTPUT
```

By leveraging the `nwfilter` ruleset of `libvirt`, `virt-manager` can do extra Virtual Network filtering things on a per-VM/container basis but admin would require crafting the rules in XML format.

By leveraging the `/etc/libvirt/hooks` subdirectory for VM/contain-specific firewall needs (such as pin-hole, port forwarding), we cover the bit of VM/container-specific actions using any scripting language (Bash and Python are two most popular ones here).

# Re-prioritization

Ideally, the `nftables.service` should have a priority level of `filter` (0) and `libvirt` should be using -1/1 for its priority level.

Since the libvirt is defaulting to `filter` (0) priority level, we have a choice of changing the entire `/etc/libvirt/nwfilter` to incorporate -1 and 1 priority level (is deemed impractical) or we can look to our own `nftables.conf` and "hijack" the ordering of Linux `nftables` by using -1/1 priority level as a "wrapper" around `nwfilter`/`libvirt`.


Let's do that: our own `/etc/nftables.conf` does the wrapping around `libvirt`.

As the default install of `libvirtd` and `nftables.service`, the `nftables` gets first dibs (by the virtue of being declared firstly at boot-up time before `libvirtd.service` got started.

This is not good enough.  We must be able to block after `libvirt` as well as check firstly before `libvirt` for our insanely complex firewall setup.

We will extend the lower case 'input' chain name into two separate chains, `input_first`, and `input_last`.

# Reference

* [Jamie Ngyuen Libvirt Networking Handbook](https://jamielinux.com/docs/libvirt-networking-handbook/)
* [libvirt: Firewall and networking filtering in libvirt](http://epic-beta.kavli.tudelft.nl/share/doc/libvirt-devel-0.10.2/firewall.html)
