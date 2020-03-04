Title: Bind9 DNSSEC Root
status: published
Date: 2020-01-28 16:14
Modified: 2020-03-04 18:00
status: published
tags: bind9, dnssec
category: research
summary: Setting up Root DNSSEC for internal use

How to set up a Root ("`.`", or top-level) DNSSEC for white-lab use.

WHY DO THIS?
============
My air-gapped (no Internet) white-lab DNS infrastructure needs a DNSSEC for internal testing.

White-Lab Description
---------------------
White-lab has its own IPv4/v6 subnet, nameservers, as well as its own DHCP, Kerberos, web, messaging, SMTP, IMAP4, and various other servers.  DNS records are populated with these servers' host address and name.

To support a full-featured DNS for such a standalone white-lab network, it must maintain its own cloned set of 13 Root DNS servers.

Furthermore, this white-lab needs integrity protection of its DNS records, hence it's time to activate DNSSEC on this private network.

Integrity of a DNS network starts at the top of the DNS tree, which is Root Servers (or "`.`").

Various DNS records also needs DNSSEC protection like `SSHFP`, `IPSECKEY`, `CERT`, `DKIM`, and `TLSA`, to name a few:  These records have public keys.  Public Key too needs that proper DNS protection from against DNS spoofing, misdirection, cache poisoning.

I'm most familiar with ISC Bind 4.8 to 9.15 (and some 10 betas), so familiar that I wrote a complete Python parser to read in the entire configuration of ISC Bind syntax from version 4.8 to 10.0, complete with documentations;  DNSSEC, not so much.

Hence this ongoing individual trial being documented here.

Of all the DNSSEC tools I've encountered, I've settled on ISC `delv`
(which is essentially a `dig` replacement.  Also, I'm recreating the
dnssec-analyzer.verisignlabs.com DNSSEC validation in Python as well.

Working examples of DNSSEC are:

```bash
dig @9.9.9.9 +dnssec +nocd +all egbert.net.
dig +dnssec @156.154.70.1 +dnssec +nocd +all egbert.net.
# Look for 'a'uthenticated 'd'ata ('ad') flag in:
# flags: qr rd ra ad; QUERY: 1, ANSWER: 3, AUTHORITY: 4, ADDITIONAL: 4

delv @9.9.9.9 +dnssec +nocd +all egbert.net.
# Look for 'fully validated'
```

Below are all the ISC Bind9.15 options available.  They are organized from
top-nested down to bottom-nested clause options and many are usable in multiple
clauses:

```nginx
# Option clause:
    managed-keys-directory <dirspec>;
    max-rsa-exponent-size  <0,35-4096>;
    root-delegation-only; // options/view clauses
    root-delegation-only exclude "whitelab"; // options/view clauses
    secroots-file <filespec>;
    session-keyfile <filespec>;
    session-keyalg [hmac-sha1|hmac-sha224|hmac-sha256|hmac-sha384|hmac-sha512|hmac-md5];
    sit-secret <hex-value-string>;
    trusted-anchor-telemetry [yes|no];

#  Option/View clauses:
    disable-algorithms <algorithm_list>;
    disable-ds-digests <digest_list>;
    dns64 [no|yes];
    dns64-contact <str>;
    dns64-server <str>;
    dnssec-accept-expired [no|yes];
    dnssec-enable [no|yes];
    dnssec-lookaside [auto|no|domain <trust-anchor> <domain-name>]
    dnssec-must-be-secure [yes|no]
    dnssec-validation [no|yes|auto];
    filter-aaaa-on-v4 [yes|no|break-dnssec];
    filter-aaaa-on-v6 [yes|no|break-dnssec];

#  Option/View/Zone clauses:
    auto-dnssec [off|allow];
    dnssec-dnskey-kskonly [no|yes];
    dnssec-loadkey-interval <1-1440>; // minute-interval
    dnssec-secure-to-insecure [yes|no];
    dnssec-update-mode [maintain|no-resign|external];
    key-directory <filespec>;
    max-zone-ttl  [unlimited|<0-65535>]
    session-keyname <keyname>;
    sig-signing-nodes <1-1024>;
    sig-signing-signatures <1-1024>;
    sig-validity-interval  <1-1024>;
    update-check-ksk [yes|no];

#  Zone clause:
    inline-signing [yes|no];
    auto-dnssec [off|maintained|allow];
    delegation-only [yes|no]; // hint/stub zones
```

Enabling DNSSEC
===============
Let us turn on DNSSEC in `/etc/bind/named.conf` with:

```cfg
  options {
      // ...
      dnssec-enable yes;
      // ...
  };
```

TLD zone and DNSSEC
-------------------
Now for the custom `whitelab` top-level domain (TLD) name.

Create the custom TLD zone database file in
`/var/lib/bind/db.whitelab`:

```named-zone
    $TTL 86400
    whitelab.                  86400 IN SOA a.myroot-servers.whitelab. (
                                                hostmaster 1 1d 2h 41d 1h )
    whitelab.                  86400 IN NS  a.myroot-servers.whitelab.
    a.myroot-servers.whitelab. 86400 IN A   @MY_ROOT_DNS_SERVER_IP@
```

The custom TLD zone database file wll also be signed as well:

```bash
dnssec-keygen -a rsasha256 -b 2048 -n ZONE whitelab
```

This `options` contains the following options:

```cfg
    options {
        dnssec-enable yes;

        // ... following new options
        directory "/var/lib/bind";  // absolute path
        key-directory "keys";       // "directory" + relative path
        dnssec-enable yes;
        dnssec-validation auto;
        dnssec-lookaside auto;
        recursion no;
        // ...
    };
```

This `zone "root"` contains the following options:

```nginx
    zone "." {
        type master;
        file "root/db.whitelab";  // not in master subdirectory for security
        update-policy local;
        auto-dnssec maintain;
    };
```
This `zone whitelab` contains the following options:

```cfg
zone "whitelab" {
        type master;
        file "master/db.whitelab";
        update-policy local;
        auto-dnssec maintain;
};
```
Back to Root, let's start with the top-most (or first
encountered) Bind9 options associated with Root, particularly private root:

```named.conf
  view "local_view" {
    root-delegation-only;  // not at global option clause, but view
  }
```

Then we add the Root (".") zone:

```named.conf
  view "local_view" {
    root-delegation-only;  // not at global option clause, but view

    zone "." {
      type hint;
      delegation-only yes;
    };

  };
```

At this point, we want to see that root zone is getting picked up, specifically
DNSKEY RRs.

```pytb
#0  ns__query_start (qctx=qctx@entry=0x7ffff51ecf20) at query.c:5296
#1  0x0000555555617758 in query_setup (client=<optimized out>,
    qtype=qtype@entry=0x30) at query.c:5141
#2  0x000055555561a709 in ns_query_start (client=client@entry=0x7fffec03a320)
    at query.c:11172
#3  0x00005555555fabaa in ns__client_request (task=<optimized out>,
    event=<optimized out>) at client.c:2992
#4  0x00005555557c4029 in dispatch (threadid=<optimized out>,
    manager=0x7ffff7f94010) at task.c:1134
#5  run (queuep=<optimized out>) at task.c:1303
#6  0x00007ffff761bfa3 in start_thread ()
```

```pytb
#0  ns_query_done (qctx=qctx@entry=0x7ffff49ebf20) at query.c:10670
#1  0x0000555555613d91 in query_nxdomain (qctx=qctx@entry=0x7ffff49ebf20,
    empty_wild=empty_wild@entry=0x0) at query.c:8576
#2  0x0000555555614c57 in query_gotanswer (qctx=qctx@entry=0x7ffff49ebf20,
    res=res@entry=0x30003) at query.c:6769
#3  0x0000555555616bfa in query_lookup (qctx=qctx@entry=0x7ffff49ebf20)
    at query.c:5545
#4  0x0000555555617082 in ns__query_start (qctx=qctx@entry=0x7ffff49ebf20)
    at query.c:5420
#5  0x0000555555617758 in query_setup (client=<optimized out>,
    qtype=qtype@entry=0x30) at query.c:5141
#6  0x000055555561a709 in ns_query_start (client=client@entry=0x7fffec0403d0)
    at query.c:11172
#7  0x00005555555fabaa in ns__client_request (task=<optimized out>,
    event=<optimized out>) at client.c:2992
#8  0x00005555557c4029 in dispatch (threadid=<optimized out>,
    manager=0x7ffff7f94010) at task.c:1134
#9  run (queuep=<optimized out>) at task.c:1303
#10 0x00007ffff761bfa3 in start_thread ()
```

Then we add our whitelab TLD zone:

```cfg
  view "local\_view" {
    root-delegation-only;  // not at global option clause, but view
    zone "." {
      type hint;
      delegation-only yes;
    };

    zone "whitelab." {
      type master;
      delegation-only no; // this time, it's not a delegation, but a referral
    };

  };
```

Now, to corral DNS query to `local_view` to just the root for local clients;
we want any attempt to query the XXXX.local. to just thie `local_view`
view.

Root zone and DNSSEC
====================

NOTE: Substitute the `MY_ROOT_DNS_SERVER_IP` with the IP address of your DNS server.

DNSSEC Key Subdirectory
-----------------------
Key subdirectory must be writeable by its UNIX owner of `named` daemon. Move to the key subdirectory:

```bash
mkdir -p /var/lib/bind/keys
chown bind:root /var/lib/bind/keys
chmod 0750 /var/lib/bind/keys
cd /var/lib/bind/keys
```
Creating root-zone key files
----------------------------
Create a new Zone-Signing-Key (ZSK) and Key-Signing-Key (KSK) for the Root ('.') zone:

```bash
dnssec-keygen -a RSASHA256 -b 2048 -n ZONE .
dnssec-keygen -a RSASHA256 -b 4096 -n ZONE -f KSK .
ls -lC1 K*key
```

Creating root-zone database file
--------------------------------
Copy keys to the `db.root` zone file:

```bash
cat K.+008+*.key > db.root
```

Create Root zone file
---------------------

Root zone file contains the DNS records for its root zone.
Populate the  `/var/lib/bind/db.root` file, add the
following records:

```named.zone
    .                          86400  IN SOA a.myroot-servers.whitelab.
                                             hostmaster.whitelab.
                                             2013122200 1800 900 604800 86400
    .                          518400 IN NS  a.myroot-servers.whitelab.
    whitelab.                  86400  IN NS  a.myroot-servers.whitelab.
    a.myroot-servers.whitelab. 86400  IN A   @MY_ROOT_DNS_SERVER_IP@
```

Sign our own root zone
----------------------

Now we can sign our own root ('.') zone.  Origin (`-o`) is root '.' zone.  Statistics `-t` get displayed at the end. Remove (`-R`) any old signatures.  Smart-Signing (`-S`) is being performed:

```bash
dnssec-signzone -o . -t -R -S  /var/lib/bind/db.root
```

This completes the standalone Root DNSSEC aspect.


Checking all our works
----------------------
It is time to check all of our works:

```bash
named-checkconf -z
echo $?
# For a successful check, echo output should be 0.
```

Restarting DNS daemon
---------------------

```bash
systemctl stop bind9.service
systemctl start bind9.service
# or
killall -KILL named
/usr/sbin/named -u bind -f -c /etc/bind/named.conf
```

Authoritative Only check with -a.
=================================

Only perform shorter authoritative check; check SOA + DNSKEY validation.This will allow confirmation that signing works at the Authoritative DNS server level before actually publishing the DS record and making DNSSEC 'public'

Grab SOA record and RRSIGs, direct from authoritative NS

```bash
delv @1.1.1.1 . SOA
dig @1.1.1.1 . SOA
dig @1.1.1.1 . RRSIG
```

Grab DNSKEY for domain, direct from authoritative NS
```bash
delv @1.1.1.1 . DNSKEY
```
Validates the above

Further validation beyond the authority is not required here

Full check (default, without -a)
================================

(not implemented) Performs full DNSSEC chain validation starting from the root

* (not implemented) current_domain=. (root)
* (not implemented) Loop1: while current_domain != checked_domain;
* (not implemented) Using NS of current_domain, grab DS record of child zone
* (not implemented) Grab DNSKEY assosicated with the DS record's RRSIG's
* (not implemented) Validate DNSKEY(child)
* (not implemented) Validate DS and DNSKEY(child)
* (not implemented) current_domain = child, child = new_child(current_domain)
* (not implemented) If: current_domain = child; break
* (not implemented) Perform check similar to authoratative (-a), above

Bind9 directories
=================
[jtable]
directory name, named.conf keyword, description
/etc/bind, directory, directory is a quoted string defining the absolute path for the server e.g. &quot;/var/named&quot;. All subsequent relative paths use this base directory. If no directory options is specified the directory from which BIND was loaded is used. This option may only be specified in a 'global' options statement.
`/etc/bind`, `file`, zone files
`/etc/bind/keys`, `key-directory`, "key-directory is a quoted string defining the absolute path, for example, &quot;/var/lib/bind/dynamic&quot; where the keys used in the dynamic update of secure zones may be found. Only required if this directory is different from that defined by a directory option. This statement may only be used in a global options clause. `rndc` `loadkeys` and `rndc` `sign` reads from this directory. "
`/var/lib/bind`, ,
`/var/lib/bind/dynamic`, `managed-keys-directory`, Zone files; filetype is typically `*.mkeys`.
`/etc/default/bind`, , Default systemd settings for `named` daemon startup (<a href="bind9.service" class="uri" title="wikilink">bind9.service</a>)
`/var/cache/bind`, `key-directory`, Dynamically created keyfiles
`/var/log/bind`, , logging for DNS `named` daemon
[/jtable]


Bind9 files
===========
[jtable]
file name, named.conf keyword, description
`/var/run/named/named.pid`, `pid-file`, "PID number of the master named process in text-format. pid-file is a quoted string and allows you to define where the pid (Process Identifier) used by BIND is written. If not present it is distribution or OS specific typically /var/run/named.pid or /etc/named.pid. It may be defined using an absolute path or relative to the directory parameter. This statement may only be used in a global options clause. "
`/etc/bind/rndc.conf`, , "Used by `rndc` utility. Manually created and often formatted like:</p> `   # Start of rndc.conf`<br /> `   include &quot;/etc/bind/rndc.key&quot;;`<br /> `   options {`<br /> `       default-key &quot;rndc-key&quot;;`<br /> `       default-server 127.0.0.1;`<br /> `       default-port 953;`<br /> `   };`<br /> `   # End of rndc.conf`"
`/etc/bind/rndc.key`, , its key is created using `rndc-confgen` `-a` looking like this:</p> <p>`   key &quot;rndc-key&quot; {`<br /> `       algorithm hmac-md5;`<br /> `       secret &quot;XbAxWyZPL74rN1Ti3dTV9a==&quot;;`<br /> `   };`
`/var/cache/bind/&#42.jnl`, `journal`, Keeps track of changes being made to the zone databases
`/var/cache/bind/cache_dump.db`, `dump-file`, "Dumps the DNS cache database into a text file. dump-file is a quoted string defining the absolute path where BIND dumps the database (cache) in response to a rndc dumpdb. If not specified the default is named_dump.db in the location specified by a directory option. This option may only be specified in a 'global' options statement. "
`/var/log/bind/named_stats.txt`, `statistics-file`, Dumps the statistics into a file. This statement defines the file-name to which data will be written when the command rndc stats is issued. May be an absolute or relative (to directory) path. If the parameter is not present the information is written to named.stats in the path defined by directory or its default. This statement may only be used in a global options clause.
`/var/log/mem-statistics.log` , `memstatistics-file` , This statement defines the file-name to which BIND memory usage statistics will be written when it exits. May be an absolute or relative (to directory) path. If the parameter is not present the stats are written to `named.memstats` in the path defined by directory or its default. This statement may only be used in a global options clause.
`/etc/bind/named.iscdlv.key` , `bindkeys-file` , OBSOLETED. Holds the DLV (now discontinued as of Feb 2017). Used to be `/etc/bind.keys`
[/jtable]

Bind9 logging channels
======================
[jtable]
directory name, channel name , description
`/var/log/bind/default.log` , `default_file` , Default events get logged into this file
`/var/log/bind/general.log` , `general_file` , General events get logged into this file.
`/var/log/bind/database.log` , `database_file` , Database events get logged into this file.
`/var/log/bind/security.log` , `security_file` , Security events get logged into this file.
`/var/log/bind/config.log` , `config_file` , Configuration and any misconfiguration events get logged into this file.
`/var/log/bind/resolver.log` , `resolver_file` , Resolver events get logged into this file.
`/var/log/bind/xfer-in.log` , `xfer-in_file` , Transfer DNS records inbound events get logged into this file.
`/var/log/bind/xfer-out.log` , `xfer-out_file` , Transfer DNS records outbound events get logged into this file.
`/var/log/bind/notify.log` , `notify_file` , Notify events get logged into this file.
`/var/log/bind/unmatched.log` , `client_file` , Client events get logged into this file.
`/var/log/bind/client.log` , `unmatched_file` , Unmatched events get logged into this file.
`/var/log/bind/unmatched.log` , `unmatched_file` , Unmatched events get logged into this file.
`/var/log/bind/queries.log` , `queries_file` , Query events get logged into this file.
`/var/log/bind/query-errors.log` , `query-errors_file` , Query ERROR events get logged into this file.
`/var/log/bind/network.log` , `network_file` , "Network events get logged into this file. open() close() dropped or downed network interface."
`/var/log/bind/update.log` , `update_file` , Update events get logged into this file.
`/var/log/bind/update-security.log` , `update-security_file` , Security update events get logged into this file.
`/var/log/bind/dispatch.log` , `dispatch_file` , Dispatch events get logged into this file.
`/var/log/bind/dnssec.log` , `dnssec_file` , DNSSEC events get logged into this file.
`/var/log/bind/lame-servers.log` , `lame-servers_file` , Lame server events get logged into this file.
`/var/log/bind/delegation-only.log` , `delegation-only_file` , Delegation events get logged into this file.
`/var/log/bind/rate-limit.log` , `rate-limit_file` , Rate limiting events get logged into this file.
[/jtable]
