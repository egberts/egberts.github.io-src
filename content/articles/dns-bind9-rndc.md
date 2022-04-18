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

ISC Bind9 `named` daemon can be interacted with using their `rndc` admin utility.

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
        read-only False; 
    };
```

`read-only` if `True` will restrict the `rndc` to the following commands:

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

# Configuration of `rndc.conf`

`rndc.conf(5)` manpage details the option settings, but in reality, you
most likely only need to use `-s <label>`.

Manpage will state that `-s` holds the server name; it also
supports `label` as well.  In this article, we use `-s` 
for our labeled needs and let the `rndc.conf` config select the 
nameserver IP or hostname ... by its server label.


## Clause `key`

`key` clause in `rndc.conf` is exactly the same as `key` clause in
`named.conf`.  All `key` clauses follow the same pattern of config
settings and are easily created using the `rndc-confgen` utility:

```nginx
#
# Created by:
#   rndc-confgen -a \
#       -k rndc-internal-key \
#       -A hmac-sha512 \
#       -b 512 -a \
#       -c /var/lib/bind/keys/rndc.hmac-sha512.key
#
key "rndc-internal-key" {
    algorithm hmac-sha512;
    secret "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX==";
};
```

To generate a new key for `rndc`, execute:

```bash
rndc-confgen -a \
    -c /var/lib/bind/keys/rndc.hmac-sha512.key \
    -k rndc-key \
    -A hmac-sha512 \
    -b 512
```
Do not forget to update both `rndc.conf` and `named.conf` to use
the new key.

`rndc.conf`
```nginx
server localhost {
    addresses { 127.0.0.1; };
    port 953;
    key rndc-internal-key;
};
```

`keys-named.conf`
```nginx
controls { inet 127.0.0.1 port 953 allow { 127.0.0.1; } read-only false };
```
and restart the `named` daemon/service.


## Clause `options`

Add to further confusion, the `rndc.conf` `options` clause has
its own set of options and syntax that is entirely different
than the `named.conf` `options` clause.

The `rndc.conf(5)` manpage details all their very own option settings, 
distinctively on their own (and separately from `named.conf`).


### Default Settings - Clause `options`

The `options` clause (`rndc.conf`) at the moment only
offers various default settings:

```nginx
options {
    default-server localhost;
    default-port   953;
    default-key    rndc-key;
    };
```

These default settings are most useful toward executing an `rndc` command
without any options; commands like this one below:

```
rndc status
```

Absence any of these `options` default settings 
in `/etc/bind/rndc.conf`, the above command will 
contact the `named` daemon using 127.0.0.1:953/udp and 
the `rndc-key` found in both `/etc/bind/rndc.key` and 
`controls` clause of `named.conf` that were created
by `rndc-confgen` with no CLI arguument.


### Server Settings - Clause `options`

To assign admin-definable labels to different remote nameservers or 
different `named` daemons, `rndc.conf` has a `server` clause.

```nginx
server localhost {
    ...
};
```


# Multiple Scenarios of `rndc`

There are several scenarios where the `rndc.conf` can be set up to do:

* central DNS controller
* split-horizon
* bastion DNS


## Centralized DNS Controller

For this central DNS controller scenario, one host can have its `rndc` to remotely
access one or more remote DNS nameservers, as well as its local 
nameserver.

Port 953 would be this same port number for all of 
these remote (and its local) nameservers being under 
control by this `rndc` "controller".


For the scenario of a centralized DNS controller, 
`rndc.conf` file would have multiple `server` labels.

```nginx
server localhost {
    addresses { 127.0.0.1; };
    port 953;
    key rndc-key;
    };
server internal {
    addresses { 192.168.1.1; };
    port 953;
    key rndc-internal-key;
    };
server dmz {
    addresses { 10.1.1.1; };
    port 953;
    key rndc-dmz-key;
    };
```

Using the same `rndc` command, different remote nameservers and localhost
 can be administratively accessed from its host.

An example interaction CLI of a Centralized DNS Controller would look like:
```bash
rndc status
rndc -s localhost status  # same as previous command
rndc -s internal status
rndc -s dmz status
```


# Multiple Instantiation scenario

Multiple Instantiation scenario comprises of multiple `named` daemon
running within the same host.

For multiple instantiation scenario of `named` daemons, one
can interact with following DNS setups:

* DNS split-horizon, 
* bastion DNS, 
* closed-net standalone DNS, or
* DNS caching add-on

Accesses to different nameserver daemon processes
can still be easily accessible just using a single `rndc`.

Most multi-instantiation scenarios have their `controls` clause
fixed to the `localhost` (127.0.0.1) and not allow any
external network have access to these multiple nameservers within
the same host.  In the case of a whitelab environment, some 
`named may have remote access enabled as well.

Different port numbers are used to separate these accesses of
each nameserver within the same `localhost` address.


# Multiple-Instantiation of `named`

The switchable CLI options is `-s`.  This `-s` option is for selecting 
an arbitrary name (called server label).

This server label enables a default setting as well.

`/etc/bind/rndc.conf`
```nginx
# always use `include rndc.key` to protect its `secret` value
# along with `chmod 0600 rndc.key` file permission setting.
include "/etc/bind/rndc-internal.hmac-md5.key"
include "/etc/bind/rndc-public.hmac-sha512.key"
include "/etc/bind/rndc-dmz.hmac-sha256.key"

options {
    default-server internal;
    # notice no `default-key`?  
    #    `server internal` provided an unique `secret` key value
    #    we use different key with each nameserver
    # notice no `default-port`?  
    #    `server internal` provided an explicit port setting
    #    we use different port with each nameserver
};

# default `rndc` usage
# or `rndc -s internal status`
server internal {
    key "rndc-internal-key";
    port 953;
    addresses { 127.0.0.1; };
    };

# `rndc -s public status`
server public {
    key "rndc-public-key";
    port 954;
    addresses { 127.0.0.1; };
    };

# `rndc -s dmz status`
server dmz {
    key "rndc-dmz-key";
    port 955;
    addresses { 127.0.0.1; };
    };

# `rndc -s whitelab status`
server whitelab {
    key "rndc-whitelab-key";
    port 953;
    addresses { 172.28.1.1; };
    };
```

In the example above, we used a single default `/etc/bind/rndc.conf`
config file to hold all nameservers for use with
`rndc` utility.

The above scenario obviates the need to craft separate shell script
with different `-p 953  -s 127.0.0.1` CLI options for
different nameservers and keeps the use of the same
`rndc` command and select them using `-s label`.

