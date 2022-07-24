title: Split-Horizon, Bind9-style
date: 2021-10-15 08:13
status: published
tags: Bind9, DNS, split-horizon
category: research
lang: en
private: False

What is Split-Horizon DNS?
--------------------------
Split-horizon DNS is providing two different answers to a DNS query, depending on where the request is coming from; the public-side or the private-side of its network.

Note: There is multi-horizon DNS which is used for different answers based on
the client's geographical location.  Multi-horizon DNS is not covered here.

Variants of Split-Horizon DNS
-----------------------------
There are several variants of split-horizon DNS:

* Multi-View, one named, multiple `view` clauses
* Two(2) named daemons, each with a unique `view` clause.
* Multi-Daemon, different types of nameservers (stub, mirror, forwarding,
  caching)
* based on client's geographical location (as determined by its source IP)

This article focus on two or multiple `named` daemons.

Downsides of 'Multi-View'
-------------------------
The multi-view approach has several shortcomings:

* Cannot reuse same zone file in different views (multi-writer, multi-reader design limitation)
* Single point of failure (single daemon)
* No clear demarcation between private/public zone files (same directory).
 
By using a single nameserver (`named`) daemon and multiple `view` clauses in its `named.conf` configuration file, split horizon DNS is considered inherently insecured.  It only takes one vulnerability to obtain both sides of the horizon and their corresponding caching and file data, using the single-daemon approach.  Using chroot would not fix this shortcoming.

Also most configuration setups want to reuse the zone file on private and public side.  This is useful when dealing with corporate mergers, partner-sharing of zone, and work from home scenarios.

For Bind9, zone files cannot be reused in different `view` clauses.  This would result in unsynchronized write operations by same daemon and will cause loss of the zone file.

Furthermore, having the 'outside' and 'inside' zone files in the same directory,
the sysadmin is liable to insert an A/AAAA record into the wrong side.  A
separate directory would help minimize this likelihood.

A Better Split-Horizon
----------------------
To fix this shortcoming of this "Multi-View Split-Horizon", multiple
`named` daemons are started.  This article demonstrates two `named`.

Let us leverage the new [Bind9 Systemd] here.

For handling multiple-instance of named and its config file, the organizational approach was either using a:

* one-sysconfdir, flat-directory: `/etc/bind` with `named-internal.conf`/`named-public.conf` or
* one-sysconfdir, tree-directory: `/etc/bind` with `keys`, `dynamic`, `zones` 
* many-sysconfdir, flat-directory: `/etc/bind/internal/`/`/etc/bind/public/` using just `named.conf`.
* many-sysconfdir, tree-directory, combo of aboves


With the many-sysconfdir, tree-directory approach, the directory tree would look like:
```
/etc/bind
/etc/bind/internal
/etc/bind/public
/etc/bind/keys     # holds RNDC keys
/run/bind/internal/named.pid
/run/bind/public/named.pid
/var/cache/bind/internal/named.secroots
/var/lib/bind/internal/master
/var/lib/bind/internal/slave
/var/lib/bind/internal/keys
/var/lib/bind/internal/dynamics
/var/lib/bind/public/master
/var/lib/bind/public/slave
/var/lib/bind/public/keys
/var/lib/bind/public/dynamics
```
Multi-subdirectory approaches keeps the `named.conf` out of the `/etc/bind` which is good.
Also they both support `include "<config-file>"` clauses so that is better
compartmentalization and easier management.

After using all (and a mixture of many), I've been leaning toward a clean directory partitions using the 'multi-subdirectory multi-sysconfdir' approach.  Subdirectory can keep files separately from other horizons.  I like the fact that `named.conf` wasn't bastardized, otherwise most tools can use any filename for a named.conf.


/etc/default
------------
Default (`/etc/default`) subdirectory is used to configure startups of various services and its settings.  Nearly all files found under default directory are stored as UNIX text file.
Each default file is named after its SysV service.  `bind9` is that service name.  Used to be `named`, but maintainers are going to be a maintainer.

Each default file can have a comment line or a statement line.  Comment line
begins with '#' symbol.  Statement line is formatted as `NAME=value`.

For Bind9, `OPTIONS` and `RESOLVCONF` environment name are used to configure startup of its services.  

Legacy `RESOLVCONF` setting is for a one-shot service setting and is used only by SysV/s6/OpenRC.  Instead, systemd uses 'bind9-resolvconf.service' whose granularity control is done by `systemctl enable bind9-resolvconf.service` command.

A new `RNDC_OPTIONS` introduces support for different configuration files for
each instance of systemd unit.  It is common to use different port number, keys, configuration, and server address to control a particular instance of many named daemons.

The easiest approach is to use the `rndc.conf` to hold all three
settings (plus its location of private symmetric key).

The preferred example is to use the `/etc/default/bind9` only for the busiest (or most revealing) nameserver, typically the internal/private ones:

An example instance of a default would contain a portion of this:

File: `/etc/default/bind9-public`
```bash
RNDC_OPTIONS="-c /etc/bind/named-<instance>.conf"
```

Control Port to Named
---------------------
To interact with an instance of named daemon, a control port is opened and
defaults to 953/tcp.  `rndc` is provided as a CLI to named.  `rndc` provides
control of daemon, zones, statistics, and dumps.

`rndc` uses `/etc/bind/rndc.conf` as its default config file.  `rndc` config
file contains the symmetric crypto key, server address, port number, and label
name of the key.

For split-horizon, create both instances of RNDC configuration files:

File: `bind9-rndc-setup-multi-instances.sh`
```bash
cd /etc/bind
mkdir keys
chown root:bind keys
chmod 0750 keys

PORT=953
rndc-confgen -A hmac-sha512 \
    -c /etc/bind/rndc-internal.key \
    -s 127.0.0.1 \
    -p $PORT \
    -u bind \
    -k /etc/bind/keys/rndc-internal.key
mv rndc.conf rndc-internal.conf
chown root:bind rndc-internal.conf
chmod 0640 rndc-internal.conf

PORT=((PORT+=1)
rndc-confgen -A hmac-sha512 \
    -c /etc/bind/rndc-public.key \
    -s 127.0.0.1 \
    -p $PORT \
    -u bind \
    -k /etc/bind/keys/rndc-internal.key
mv rndc.conf rndc-public.conf
chown root:bind rndc-public.conf
chmod 0640 rndc-public.conf

# Since RNDC is keyed by port and its key, there is no longer a default RNDC config file
```

Now whenever the command `rndc` gets (accidentially) evoked, you will get an
error message:
```
rndc: neither /etc/bind/rndc.conf nor /etc/bind/rndc.key was found
```

There is a reason for this breakage of `rndc`, there is no easy way to determine
which instance of the many named daemon that are running.

For a new sets of `rndc` commands to denote which is which side of the horizon.  `<instance>` name shall be used here.

Also to assist `systemd` with communicating with the correct instance, 
the `/etc/default/bind9` get copied and modified into:

File: `/etc/default/bind9-internal`
```bash
OPTIONS="-c /etc/bind/internal/named.conf"
RNDC_OPTIONS="-c /etc/bind/internal/rndc.conf"
```

File: `/etc/default/bind9-public`
```bash
OPTIONS="-c /etc/bind/public/named.conf"
RNDC_OPTIONS="-c /etc/bind/public/rndc.conf"
```


Multi-RNDC 
----------
Create a bash script to deal with the (many) other instances of `named` daemon:

File: `rndc-internal`
```bash
#!/bin/bash
# Could uses default /etc/bind/rndc.conf with just `rndc`
rndc -c /etc/bind/rndc-internal.conf $1 $2 $3 $4 $5 $6 $7 $8 $9
```

File: `rndc-public`:
```bash
#!/bin/bash
# Does NOT use default /etc/bind/rndc.conf
rndc -c /etc/bind/rndc-public.conf $1 $2 $3 $4 $5 $6 $7 $8 $9
```
Then tighten up file permissions:

```bash
# chmod 0750 rndc-*.conf
# chown $USER:bind rndc-*.conf   # required but only if enforcing 'bind' group.
```

Stick above script into your ~/bin (or `/usr/local/sbin`).

Systemd Bind9.service
---------------------
Package name gets the service name.

That package name is `bind9`; not `bind`, `named`, `name`, nor `isc-bind` (or that infernal `isc-dhcp-server`); once again, package name is `bind9`.  Systemd unit name (both .service and .socket) for bind9 shall be `bind9.service`.

If a server-class package requires more than one unit, then its unit name get lengthened with a '-<function>' suffix.  The original and first unit name does not need to be lengthened.

Bind9 has only has two primary and lesser functions, so only needs one unique name for a systemd unit: so it is `bind9.service` and `bind9-resolvconf.service`.

Unfortunately, all maintainers/distros' current `named.service` only supports one daemon/server.  Furthermore, distro maintainers only supplied one service file, typically in `/lib/systemd/system/named.service`.

Hence, for this expansion and correctness, focus on using 'bind9.service' as the current systemd unit name for this ISC Bind9 named daemon.  Templating this new `bind9.service` unit then follows easily afterward.

To do multi-daemon split-horizon, systemd needs to use these different-horizon configuration files.  Systemd comes to the rescue and provides a unit template.  Our current unit file for Bind9 is `bind9.service`.  Templating unit files are denoted by '@' symbol in its template filename like `bind9@.service`.
t

New systemd unit template file for Bind9 is shown below:

File: `/etc/systemd/system/bind9@.service`
```ini
[Unit]
Description=BIND Domain Name Server (for %I)
Documentation=man:named(8)
After=network.target
Wants=nss-lookup.target
Before=nss-lookup.target

[Service]
# EnvironmentFile is mandatory now
# Example is '/etc/default/bind9-public' from 'bind9@public.service'
EnvironmentFile=/etc/default/%p-%I
ExecStart=/usr/sbin/named -f $OPTIONS
ExecReload=/usr/sbin/rndc $RNDC\_OPTIONS reload
ExecStop=/usr/sbin/rndc $RNDC\_OPTIONS stop
Restart=on-failure

[Install]
WantedBy=multi-user.target
DefaultInstance=default
Alias=named.service
```


Named Configuration Organization
--------------------------------
For multiple `named` , it makes sense to have separate subdirectories to hold all its configuration files.  



Default Directories
-------------------
I cannot stress the confusion made by different distros' maintainers of bind9,
especially toward the following default settings:

* `prefix` (autotool)
* `sysconfdir` (autotool)
* `localstatedir` (autotool)

These three are all over the map and highly inconsistent across distros.  ARGH!

Our new `bind9.service` shall assumes the account's `$HOME` and
`/etc/default/[named|bind9]` for all of Bind9 default settings.

