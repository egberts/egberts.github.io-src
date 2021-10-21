title: Using complex dhclient in NetworkManager
date: 2021-09-22 08:00
status: published
tags: HOWTO, NetworkManager, dhclient
category: research
lang: en
private: False

So your DHCP client is running as PXE boot server or
got some fancy multi-home laptop that can be at work,
work from home or just be at home.

NetworkManager doesn't even seem to handle your highly-customized
DHCP (`dhclient`) client configurations.

But it can, for the most part; and I will show you how.  And I 
made it work directly and rather well with my ISP finicky 
(Verizon FiOS) Juniper DHCP server.


Some caveats here:

* DHCP configuration cannot use 'include' statement to include another
dhclient-related configuration file.  This is somewhat problematic of 
large enterprise.  But for a very-complex HomeLAB or replacing an 
ISP cablerouter, this is not an issue.

* You just cannot use nor expect the all keywords supported by ISC
DHCP client within the `dhclient[-*].conf` file.

WHERE'S THE CONFIG
==================

First thing, first. The `dhclient[-*].conf` are still located in `/etc/dhcp`.
This is where all your customization should end up in, even if you
use NetworkManager.

Naming convention of this DHCP client config file is strict.

* Default is `dhclient.conf`.  It will be used for any and all 
  netdev interfaces.
* Other supported filespec is `dhclient-<netdev>.conf` where
  <netdev> can be the likes of `eth0` or `enp5s0`. This is the
  preferred method.

Above filespec convention are used by both `dhclient` and `NetworkManager`.

I MEANT NETWORKMANAGER.CONF
===========================

Hold on.  A bit last thing about `dhclient-<netdev>.conf` and its 
locations, as in more than one.

When its netdev connection is coming up, NetworkManager will notice the 
word `method=auto` in one of those `/etc/NetworkManager/system-connections/`
files.  Once `auto` gets detected, NM then fires up the `dhclient` daemon 
but made to use with NM's very own configuration
file located in `/var/lib/NetworkManager/dhclient-eth0.conf`.

Yeah, during pre-up link state, this customized 
`/etc/dhcp/dhclient-eth0.conf` will get 'grep' for certain exclusion 
and inclusion of DHCP configuration keywords plus
forcibly tacking on whatever DHCP client options that NM "thinks" that 
you need.

After such radical flat-file suppositions made on your `dhclient-eth0.conf`
by NetworkManager and written into `/var/lib/NetworkManager` subdirectory,

WARNING: If you made a typo of this `dhclient-*.conf`, and restarted the
NetworkManager service, getting it unstuck often requires DELETING the
misnamed file from `/var/lib/NetworkManager/dhclient*` and doing it again.


BACK TO NETWORKMANAGER.CONF
===========================
In the `[main]` section of `/etc/NetworkManager/NetworkManager.conf`, 
you will need to have the following setting(s):

```
[main]
dhcp=dhclient
```
Failure to do that will result in revert back to NM's default of using
their own-brand of overly-simplistic internal (and PXE-less) DHCP client.  


What keywords cannot I use?
===========================
In the DHCP client configuration file (`/etc/dhcp/dhclient-*.conf`)...

The following settings are actively being stripped out by the NetworkManager:

 * `alias` block - Entire blocks are 100% ignored; nothing lifte nor gleaned
 * `lease` block - Entire blocks are 100% ignored; nothing lifte nor gleaned
 * `also request` - strips it out
 * `timeout`
 * `retry`
 * `reboot`
 * `reject`
 * `retry`  - nmtui/nmcli-configurable
 * `hostname = gethostname()` - strips out the function, not the keyword. And
   lets NM sets its hostname.

What keyword can I set?
=======================

Some useful keywords that NetworkManager allows in your `dhclient-*.conf`
file are:

 * `initial-timeout` - nmtui/nmcli-configurable
 * `select-timeout`
 * `backoff-cutoff`
 * `initial-interval`
 * `initial-delay`
 * `server-name` - Selects WHICH dhcp server to use.
 * `do-forward-requests` - Good if you're also running ISC DHCP 'server'
    in which that DNS server can be configured to take the DHCP 
    hostname update(s).  This ISC-DHCP-to-ISC-BIND9 arrangement is 
    actually a safer method, security-wise.
 * `bootp` - Use the PXE boot approach (only useful within initrd/initramfs)
 * `interface`  - Another PXE boot setting
 * `filename` - Another PXE boot setting
 * `scripts` - provide your own DHCP dispatch handler or revert it back 
   to dhclient's very own `/sbin/dhclient-script` for a true ISC DHCP 
   client experience;
   You might lose D-BUS support for dynamic network state (CAT-5 disconnect)
   this way unless you copy these script files over from 
   `/etc/NetworkManager/dispatcher.d/*` and
   into the `/etc/dhcp/dhclient-enter.d` and `/etc/dhcp/dhclient-exit.d`;
   dont forget to check the shell arguments and compensate for this.
   DHCP dispatch only uses `$1` for its own full-filepath and nothing else.
   (In case you're wondering, `$0` is `/sbin/dhclient-dispatch`)

Imposing Keywords
=================
Some other DHCP keywords used by `dhclient` that are forcibly imposed by
NetworkManager are:

* `wpad` keyword is one nasty imposition.  I cannot get rid of it.  And it has
  caused problem with some public WiFi.  I filed a bug report,
  they won't fix it.
* `rfc3442-classless-static-route` is another.  I can forsee a few
scenario that needs to get rid of this but it is very rare.
* `ms-classless-static-route` - Also needed only by Microsoft DHCP servers.
Totally useless otherwise.  Is very problematic when some other DHCP 
server rejects your DHCP-request because of this.  Just take the lump.
* `root-path` - Should not have been included here as it is only used
with PXE-boot hosts.


Summary
=======

After all, NetworkManager is just a desktop network connection manager, 
albiet a full-blown one, if you call it that.

I now can enjoy the rich DHCP networking experience that 
`systemd-networkd`, SysV initd, OpenRC, and s6 cannot 
offer (notice I didn't say ConMan).
