title: Hidden Master Using Non-Standard DNS Port
date: 2022-05-01 06:09
status: published
tags: DNS, Bind9
category: HOWTO
summary: How to free up a port 53 on your hidden primary/master nameserver so that your other instances of named daemon can claim it using ISC Bind9 `named`.
slug: dns-bind9-hidden-primary-port53-not
lang: en
private: False

This article details the narrowing of a communicaton channel of the 
hidden-primary (formerly called hidden-master) to just one 
TCP/UDP port number so that its DNS default port 53 can be 
reused by other instance of nameserver.

If you are like me, you have squeezed a bunch of `named` daemons 
running side-by-side on your home gateway.  
Each instance of `named` should all have been are `chroot`'d, jailed, 
dockerized, containerized and/or QEMU'd apart; if not, they should be by now.

Each instance of a nameserver (`named`) daemon is now competing for the right
to serve that precious port 53/udp (and even more so now port 53/tcp).  

ICYMI: Port 53/tcp is becoming more and more prevelant due to DoH, DoT, 
and even IP tunneling.

# 53/tcp Blocker

My hidden-primary was using that last vestigate of precious 
internet-facing port 53/tcp for its localhost testing of 
`allow-query`/`allow-recursion-on` and allowing
the public-facing primary nameserver to test and exercise query
against this hidden-primary: this is not needed anymore.

And with a bunch of pending DNS expansions looming ahead, 
the demand has risen for that port 53/tcp (and alongside with 
its 53/udp) again, just on the public-side.  

Some "looming" requirements for this public 53/tcp are:

* whitelab DNSSEC
* DoT
* DoH
* IP Tunneling

So, Hidden Master, it is time to move aside.

# Internet-facing vs. public-facing

Internet-facing is the host that has its netdev device facing toward the 
internet gateway (often toward the default gateway as listed in the host's
route table).

Public-facing is the DNS nameserver that will serve 
all the queries of your domain zone data.

Hidden-primary will not answer any DNS query of your domain but it
will perform DNSSEC key pre-signings so that your 
public-facing nameserver can focus on just answering queries.  

This is why the `MNAME` part of
your domain's `SOA` is pointing toward your public-facing nameserver
and not toward your hidden-primary nameserver.

This is probably the only scenario where is intentionally lied there 
about where the master zone database file is located at;  `SOA` normally
tells us where the master zone database file is located ... often, but not
here.

```dns
mydomain.example  SOA  ns.mydomain.example  root.mydomain.example ( ... )
```

`MNAME` is the `ns.mydomain.example`.  Again, `MNAME` tells use where is the 
primary nameserver for this domain name, just not necessarily where the
zone database file is located at.

# Planning

Since hidden-primary was already using a unique port number 
for its AXFR/IXFR transfer of zone data, reuse 
that port number for its querying needs.

Some example values used in this articles are:

* AXFR/IXFR port number is `1234`.
* TSIG key name is `key_hidden_primary_to_public_primary`.

[jtable]
host, value, description
public primary, `999.999.999.999`, internet-facing IP address
public primary, `ns1.mydomain.example`, internet-facing hostname
public primary, `
acl_public_primary_nameserver_gateway_facing_ip
`, ACL name
hidden-primary, `888.888.888.888`, internet-facing IP address
hidden-primary, `5432.dynip.myisp.com`, internet-facing hostname
hidden-primary, `acl_hidden_primary_nameserver_gateway_facing_ip`, ACL name
[/jtable]


# Relocation Effort

To relocate the tcp/53 port for the communication 
between hidden-primary and public primary nameserver pair,
two sets of configuration files will be tweaked on the:

* hidden-primary nameserver
* public-facing primary nameserver

Our effort is to increase the usage of the pre-existing `port 1234` 
already used for the existing AXFR/IXFR transfer connection 
between two nameservers listed above and use that for 
authenticated (pre-approved) querying as well.

# New Key

I always (re-)generate a unique key when (re-)working between two nameservers.

This key should not be reused elsewhere.

Downside of having a new key is the increased complexity of 
DNS administration.  But if a key should becomes compromised, you 
are limited to just within the nameservers
that are impacted by such that compromised key.

NOTE: Often times, it makes even more sense to name such key
as `key_hidden_primary_to_public_primary_egbert_net` but
our readers are presumed to be a small-time DNS administrator
and such hidden-primary often targets one zone/one domain.

```bash
cd /etc/bind/keys

tsig-confgen -a HMAC-SHA512 key_hidden_primary_to_public_primary \
    > key_hidden_primary_to_public_primary-named.conf

# for Debian/Devuan, use 'bind:bind" in `chown`.
chown named:named key_hidden_primary_to_public_primary-named.conf
chmod 0750 key_hidden_primary_to_public_primary-named.conf
```

Include the new key into `named.conf` (or inside its 
`key-named.conf` file, if in multi-file config mode)
using the `include` pragma:

```nginx
# inside `named.conf`
include "/etc/bind/keys/key_hidden_primary_to_public_primary-named.conf";
```

# Public-Facing Primary Nameserver

Head over to the public-facing primary nameserver.  That's the
one opposite the hidden-primary.

In the `acl` clauses section of `named.conf`, add another ACL label (or
reuse a pre-existing ACL to replace our 
`acl_public_primary_nameserver_gateway_facing_ip` 
example) for the IP address of this public-facing nameserver:

```nginx
acl acl_public_primary_nameserver_gateway_facing_ip { 999.999.999.999; };
acl acl_hidden_primary_nameserver_gateway_facing_ip { 888.888.888.888; };
```
and replace the `999.999.999.999` with your public-facing IP address: it
is probably the only one IP address (and should be the only one, other
than 127.0.0.1, unless you're an expert and have IP tunnels).

Inside the `options` clause, add another port listener:

```nginx
listen-on port 1234 {
    acl_public_primary_nameserver_gateway_facing_ip;
    };
```

Inside the `zone` clause, insert the following:

```nginx
    primaries primaries_list_upstream_authoritative_nameservers;
```

Add or update the `primaries` (formerly called `masters`) clause where 
the declaration for the hidden master is located:

```nginx
primaries primaries_list_hidden_primaries {
    888.888.888.888 key key_hidden_primary_to_public_primary;
    };
```
Replace the `888.888.888.888` with the Internet-facing IP address of your hidden-primary.


# Hidden Primary Nameserver

The hidden-primary nameserver (formerly called hidden-master) also 
has a checklist to ensure that all queries are now being done over
this new `port 1234`.

## SOA Check

Head over to `/var/lib/bind/primaries/` directory and
view the zone `db.mydomain.example` database file of 
your domain name.

Ensure that the `MNAME` portion of its `SOA` is pointing 
toward your public-facing primary (`ns1.mydomain.example`) nameserver.
And that this `MNAME` portion does NOT point to itself
such as (`54321.myip.myisp.com`).

```nginx
acl acl_public_primary_nameserver_gateway_facing_ip { 999.999.999.999; };
acl acl_hidden_primary_nameserver_gateway_facing_ip { 888.888.888.888; };
acl acl_trusted_downstream_nameservers {
    acl_public_primary_nameserver_gateway_facing_ip;
    };

## Why do we have `acl_` simply tacked on?
## so that in the future, we can change the keyname
## but not the ACL label.
## ICYMI: Key name are sent in the clear over DNS protocol
acl acl_key_hidden_primary_to_public_primary { 
    key key_hidden_primary_to_public_primary;
    };
```

Inside the `options` clause, ensure that the following statement exists
and is enabled:

```nginx
    notify no;
    notify-to-soa yes;
```

# Primaries Check

In `primaries` (formerly known as `masters`) clause, check to 
ensure the following:

```nginx
primaries primaries_list_downstream_public_primary_nameservers {
    999.999.999.999 port 1234 key key_hidden_primary_to_public_primary;
};
```

NOTE: Unfortunately, ACL cannot be used around `primaries`(/`masters`)
hence the prefix notation of `masters_list_*` used here, instead of `acl_*`.


## Zone Check

```
## * If `notify` is set to 'explicit' NOTIFY is only sent to those IP(s) 
##   listed in an `also-notify` statement.
## Again, ACL cannot be used within `also-notify`, only `masters` labels.
notify explicit;
also-notify port 1234 {
    masters_list_downstream_public_primary_nameservers;
    };
```

## Transfer Check


Inside the `zone` statement (under a view), ensure that the following
exist:

```nginx
allow-query {
    acl_trusted_downstream_nameservers;
    acl_hidden_primary_nameserver_gateway_facing_ip; // for localhost testing
    };

allow-query-on {
    acl_hidden_primary_nameserver_gateway_facing_ip; // for localhost testing
    };

allow-transfer {
    !{ !{acl_host_trusted_downstream_nameservers; 127.0.0.1;}; any; };
    ##  Only trusted_downstream_nameservers and localhost get past

    acl_key_hidden_primary_to_public_primary;

    none;
    };

    auto-dnssec maintain;
```


# Verification

## Simple test

On the public primary side, execute:

```bash
dig -b 999.999.999.999#1234 -p 1234 @888.888.888.888 mydomain.example soa
```

You should get an answer to `SOA` resource record type.

```console
; <<>> DiG 9.17.4 <<>> -b 999.999.999.999#1234 -p1234 @888.888.888.888 mydomain.example soa
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 33622
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 07c6e8c15232839601000000626eadedb82896263fa00cc9 (good)
;; QUESTION SECTION:
;mydomain.example.		IN	SOA

;; ANSWER SECTION:
mydomain.example.		86400	IN	SOA	ns1.mydomain.example. admin.mydomain.example. 2022042010 1200 180 1209600 10800

;; Query time: 11 msec
;; SERVER: 888.888.888.888#1234(888.888.888.888)
;; WHEN: Sun May 01 11:57:33 EDT 2022
;; MSG SIZE  rcvd: 113
```

Note the success notation of `status: NOERROR`.


## By Debug Log

You can flip on the `debug` for:

* `xfer-out.log` in hidden-primary
* `xfer-in.log` in public-primary

On each platform, edit the config file and head over 
to `category` under `logging` clause, and identify
the channel name used for `xfer-in`

An example setting looks like:
```nginx
logging {
...
    category xfer-in { xfer-in_channel; };
    category xfer-out { xfer-out_channel; };
...
```

With the user-definable channel name identified as `xfer-in_channel`
and `xfer-out_channel`, head toward its channel names:

An example settings for logging channels:
```nginx
    channel xfer-in_channel {
        file "/var/log/named/hidden/xfer-in.log" versions 3 size 5m;
        ## severity dynamic;
        severity debug 3;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel xfer-out_channel {
        file "/var/log/named/hidden/xfer-out.log" versions 3 size 5m;
        ## severity dynamic;
        severity debug 6;
        print-time yes;
        print-severity true;
        print-category true;
    };
...
};
```

On the public-primary side, change the `severity` settings to `debug 3` for `xfer-in`.

On the hidden-primary side, change the `severity` settings to `debug 6` for `xfer-out` on both sides.

Restart the nameserver on both sides.

Then tail the log file

on the hidden-primary side:
```bash
tail -f /var/log/named/xfer-out.log
```

on the public-primary side:
```bash
tail -f /var/log/named/xfer-in.log
```
and wait up to  30 minutes for logged activities.

There should be no failure.



## By Network Packets

Execute on both sides:

```bash
tcpdump -v -vv  port 1234
```
