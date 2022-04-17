title: Bind9 `rndc` Administration Control Channel
date: 2022-04-17 11:16
status: published
tags: Bind9, DNS
category: HOWTO
summary: How to set up `rndc` control channel for proper local and remote administration of Bind9 `named` daemon. 
slug: dns-bind9-rndc
lang: en
private: False


# Intro

ISC Bind9 `named` daemon can be interacted with using their `rndc` utility.

With `rndc`, you can do read-only operation to obtain statistics, 
zone info, recursion list, dump SEC Roots, trace daemon activities,
server uptime, reliability, and performance data, to name a few.

Also with `rndc`, you can do update/write/delete operation to 
stop a daemon, add/modify/delete/reload a zone, 
create/close a dnstap file, dump database, flush
server cache, freeze/sync/thaw zone data/journal files, reload keys,
notify downstream nameservers, negate a trust zone,
reload config file(s), retransfer a zone, scan interfaces, validation.

This article details how to properly configure the RNDC for a wide-variety of
setups so that an administrator can enforce the following security boundaries:

* By user/group
* By read/write function
* By different instantiation of `named` daemons

The basic of `rndc` is covered here firstly.

# Key Generation

## Default - Key Generation

## Custom - Key Generation


# Control Channel

`controls` clause in `/etc/bind/named.conf` file details how the `rndc` is to communicate with the `named` daemon.

For Bind9 split-file configuration mode, the `controls` clause can be found elsewhere
in a different file (ie., `/etc/bind/controls-named.conf`).

At this writing, the methods to communicate 
with the `named` daemon are:

* disabled
* `inet` - IPv4/IPv6 network channel
* `unix` - UNIX file-based channel (not used by `rndc`; used by `nsupdate`)

Only `rndc` uses `inet` method.


## Disable `rndc` Channel

To completely disable this `rndc` utility, insert into `controls` clause the following:

```
controls { };
```

Failure to include above settings will have `named` daemon perform an opening of the network port to only 127.0.0.1 port 953/udp.  This above setting is useful for Internet-bordering host.  Such public-facing host is where an admin really should be logging into this host before talking with its `named` daemon and should not be accessing this host from a faraway place.

It is useful as a security precaution to disable `rndc` especially if the name server is not going to be visited frequently.


## IP-based - Control Channel

First way for `rndc` to communicate with `named` is over `inet` network socket.

Two different `inet` are supported here:  IPv4 and IPv6.  
You can use IPv4, IPv6, or both.


### Localhost - IP-based - Control Channel

The accessible of its network outreach can be restricted by using 
`localhost`/`127.0.0.1` or not.

There are two ways to do this `localhost`/`127.0.0.1`:

* Do not include any `controls` clause in the `named` config file(s). (default)
* Explicitly define the `controls` clause.

To explicitly defined `rndc` to be restrict to just the `localhost` for 
only observational purpose:

```nginx
# This is the `named.conf` default setting if `controls` clause is missing
include "/etc/bind/rndc.key"  # if any

controls {
    inet 127.0.0.1 port 953
        allow {
            127.0.0.1; 
            } 
        keys { 
            rndc-key; 
            }
        read-only True; 
    };
```

`read-only` if true will restrict the `rndc` to the following commands:

* `nta-dump`, 
* `null`, 
* `status`, 
* `showzone`, 
* `testgen`, and 
* `zonestatus`

Adding more keys will enable a finer revocability of a single-key made to each of the issued administrator/lab-users.

Of course, any other or additional IPv4 address or IPv6 address will merely expand the `rndc` reachablility remotely.


## UNIX-Socket-based - Control Channel

UNIX-based BSD socket is not used by `rndc`.  However, `nsupdate` makes good
use of this BSD socket here.  So this slightly unrelated section details how its configured for `nsupdate`
and other ISC-related tools.

An example of a `named` setting for this no-network access to `named` daemon.
```nginx
controls { 
    unix "/var/run/named/resolver.sock" 
        perm 0750 
        owner 11 
        group 101 
        keys { 
          key-to-admin-team-shift-a; 
          local-ddns;
        }
        read-only true; 
    };
```

