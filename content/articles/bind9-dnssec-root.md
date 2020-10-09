Title: Bind9 DNSSEC Root Server
status: published
Date: 2020-01-28 16:14
Modified: 2020-06-06 18:05
tags: bind9, dnssec
category: research
summary: Setting up Root DNSSEC for internal use

How to set up a Root ("`.`", or top-level) DNSSEC for white-lab use.
This article is also good for setting up a custom-selected TLD for private
home use (such as DNSSEC'ized '.local').

WHY DO THIS?
============
My air-gapped (no Internet) white-lab DNS infrastructure needs a 
DNSSEC for internal testing.  

White-Lab Description
---------------------
White-lab has its own Internet infrastructure with IPv4/v6 subnet, 
DNS nameservers, as well as its own DHCP, Kerberos, web, messaging, 
SMTP, IMAP4, and various other servers.  
DNS records are populated with these servers' host names and IP addresses.

To support a full-featured DNS for such a standalone white-lab network, 
it must maintain its own cloned set of 13 Root DNS servers.

Furthermore, this white-lab needs integrity protection of its DNS 
records, hence it's time to activate DNSSEC on this private network.

Integrity of a DNS network starts at the top of the DNS tree, 
which is Root Servers (or "`.`").

Various DNS records also needs DNSSEC protection like `SSHFP`, 
`IPSECKEY`, `CERT`, `DKIM`, and `TLSA`, to name a few:  
These DNS RDATA records have accompanying public keys.  
Public Key too needs that proper DNS protection from against 
DNS spoofing, misdirection, and cache poisoning.

I'm most familiar with ISC Bind 4.8 to 9.17 (and some 10 betas), so 
familiar that I wrote a complete Python parser to [read in the 
entire configuration of ISC Bind syntax](https://github.com/egberts/bind9_parser)
 from version 4.8 to 
10.0, complete with documentations;  DNSSEC, not so much.

Hence this ongoing individual trial are being documented here using
ISC Bind 9.15.8.

Of all the DNSSEC utility tools I've encountered, I've settled on ISC `delv`
(which is essentially a `dig` replacement.  Also, I'm recreating the
dnssec-analyzer.verisignlabs.com DNSSEC validation in Python as well.

Examples working command of DNSSEC are:

```bash
dig @9.9.9.9 +dnssec +nocd +all egbert.net.
dig +dnssec @156.154.70.1 +dnssec +nocd +all egbert.net.
# Look for 'a'uthenticated 'd'ata ('ad') flag in:
# flags: qr rd ra ad; QUERY: 1, ANSWER: 3, AUTHORITY: 4, ADDITIONAL: 4

delv @9.9.9.9 +dnssec +nocd +all egbert.net.
# Look for 'fully validated'
```

Below are all the DNSSEC-specific option settings found in ISC Bind9.15.8.
These options are organized from top-nested down to bottom-nested clause 
options and many are re-usable in multiple clauses:

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
Getting Started
===============
Debian 9 only has Bind v9.11.  We need an upgrade there.  Ditch the old Bind.

First, uninstall any and all Bind-related packages:
```bash
apt remove bind9 bind9-dyndb-ldap bind9-host bind9utils 
apt remove libbind9-161 libbind9-90 
apt remove bindtools
```

Cloning ISC Bind
----------------
Then clone the ISC Bind9 repository:
```bash
git clone https://github.com/isc-projects/bind9.git
...
```
Go into the repo and checkout v9.15.8:
```bash
cd bind9
git tag --list  # view all available tags
git checkout v9_15_8
```

Building Bind9 on Debian 9
--------------------------
Configure the Bind9:
```bash
export ACLOCAL_PATH=/usr/share/aclocal
autogen.sh  # if you don't have it, pull it off the net.
# v9.15.8
./configure \
	--localstatedir=/var \
	--sysconfdir=/etc/bind \
	--enable-full-report \
	--with-tuning=default \
	--enable-querytrace \
	--enable-geoip \
	--prefix=/usr \
# or --prefix=/usr/local
```
Then build and install the Bind9:
```bash
make -j4
make install
```

Build Documentation
-------------------
It wouldn't be complete without documentation, so let us build that too:
```bash
cd doc
make doc
```

Once installed, you have an equivalence of the following Debian packages
installed into `/usr`:

* bind9
* bind9utils
* dnsutils
* bind9-dev
* bind9-doc

Directory Layout
================
Create all the subdirectories, as needed:

```bash
mkdir /etc/bind
mkdir /etc/bind/internal
mkdir /etc/bind/private-hint
mkdir /etc/bind/keys
mkdir /var/cache/bind
mkdir /var/cache/bind/internal
mkdir /var/cache/bind/private-hint
mkdir /var/lib/bind
mkdir /var/lib/bind/internal
mkdir /var/lib/bind/internal/primary
mkdir /var/lib/bind/internal/secondary
mkdir /var/lib/bind/internal/dynamic
mkdir /var/lib/bind/private-hint
mkdir /var/lib/bind/private-hint/primary
mkdir /var/lib/bind/private-hint/secondary
mkdir /var/lib/bind/private-hint/dynamic
mkdir /var/log/named
mkdir /var/log/named/internal
mkdir /var/log/named/private-hint
mkdir /var/run/bind
mkdir /var/run/bind/internal
mkdir /var/run/bind/private-hint

chmod 2755 /etc/bind
chown root:bind /etc/bind

chmod 2750 /etc/bind/internal
chmod 2750 /etc/bind/private-hint
chmod 4750 /etc/bind/keys
chown root:bind /etc/bind/private-hint
chown root:bind /etc/bind/internal
chown bind:bind /etc/bind/keys   # root shouldn't need keys/

chmod 2750 /var/cache/bind
chown bind:root /var/cache/bind

chmod 2750 /var/cache/bind/private-hint
chmod 2750 /var/cache/bind/internal
chown bind:root /var/cache/bind/internal   # root doesn't need access
chown bind:root /var/cache/bind/private-hint   # root doesn't need access

chmod 2755 /var/lib/bind
chown root:bind /var/lib/bind

chmod 3750 /var/lib/bind/internal
chown bind:root /var/lib/bind/internal

chmod 3750 /var/lib/bind/internal/primary
chmod 3750 /var/lib/bind/internal/secondary
chmod 3750 /var/lib/bind/internal/dynamic
chown bind:root /var/lib/bind/internal/primary
chown bind:root /var/lib/bind/internal/secondary
chown bind:root /var/lib/bind/internal/dynamic

chmod 3750 /var/lib/bind/private-hint
chown root:bind /var/lib/bind/private-hint

chmod 2750 /var/lib/bind/private-hint/primary
chmod 2750 /var/lib/bind/private-hint/secondary
chmod 2750 /var/lib/bind/private-hint/dynamic
chown bind:root /var/lib/bind/private-hint/primary
chown bind:root /var/lib/bind/private-hint/secondary
chown bind:root /var/lib/bind/private-hint/dynamic

chmod 2750 /var/log/named   # 2xxx because named generates named_stats.txt
chown root:bind /var/log/named

# Nothing we can do about bind-user's write-ability so let them have it.
# But we can block bind-group's write-ability; so, root-group, it is.
chmod 0750 /var/log/named/internal
chmod 0750 /var/log/named/private-hint
chown bind:root /var/log/named/internal
chown bind:root /var/log/named/private-hint

chmod 2750 /var/run/bind
chown root:bind /var/run/bind

# allow bind-group writeability (so they can restart named daemons)
chmod 2750 /var/run/bind/internal
chmod 2750 /var/run/bind/private-hint
chown bind:bind /var/run/bind/internal
chown bind:bind /var/run/bind/private-hint
```

Default Settings
----------------
Need to create default files:
```bash
vim /etc/default/bind9-internal
```
then fill that `bind9-internal` file with
```bash
# run resolvconf?
RESOLVCONF=no

# startup options for the server
# OPTIONS="-u bind -d 4095"
OPTIONS="-u bind -c /etc/bind/named-internal.conf"
```

Systemd setting
---------------
Need to create systemd file:
```bash
vim /etc/systemd/system/bind9-internal.service
```
and fill it with:
```systemd
# File: /etc/systemd/system/bind9-internal.service
#
# Internal-facing web server
#
# Not to be confused with default bind9.service

#
# The unit files have no installation config 
#  (WantedBy=, RequiredBy=, Also=, Alias= settings in 
#  the [Install] section, and DefaultInstance= for template
#   units). 
# This means they are not meant to be enabled using systemctl.

#
[Unit]
Description=BIND Domain Name Server (Internal)
Documentation=man:named(8)

# DHCLIENT SCRIPT will be activating this systemd unit service
# No dependencies nor startup
# After=network.target
# Wants=nss-lookup.target
# Before=nss-lookup.target

# If a unit has a Conflicts= setting on another unit, starting 
# the former will stop the latter and vice versa. 
Conflicts=bind9.service

[Service]
EnvironmentFile=/etc/default/bind9-internal
ExecStart=/usr/sbin/named -f $OPTIONS
ExecReload=/usr/sbin/rndc -p 953 reload
ExecStop=/usr/sbin/rndc -p 953 stop
PIDfile=/run/bind/named-internal.pid
KillMode=process
Restart=on-failure
# named needs: CAP_NET_BIND_SERVICE,CAP_SYS_CHROOT,CAP_SETUID,CAP_SETGID,CAP_DAC_READ_SEARCH,CAP_SYS_RESOURCE,CAP_CHOWN
# # Tried combinations of those:
#CapabilityBoundingSet=CAP_NET_BIND_SERVICE
#Capabilities=CAP_NET_BIND_SERVICE+ep
SecureBits=keep-caps
AmbientCapabilities=CAP_NET_BIND_SERVICE,CAP_SYS_CHROOT,CAP_SETUID,CAP_SETGID,CAP_DAC_READ_SEARCH,CAP_SYS_RESOURCE,CAP_CHOWN
# Capabilities=CAP_IPC_LOCK+ep
# CapabilityBoundingSet=CAP_SYSLOG CAP_IPC_LOCK
NoNewPrivileges=yes

[Install]
WantedBy=multi-user.target
```

Deactivate any old bind9 service:
```bash
systemctl stop bind9
systemctl disable bind9
systemctl masked bind9
```
and enable our stuff
```bash
systemctl enable bind9-internal
# We will start it later in this article
```

AppArmor setting
----------------
Need to fill in AppArmor settings:
```bash
vim /etc/apparmor.d/local/usr.sbin.named
```
and prepend or fill it with:
```
  # See /usr/share/doc/bind9/README.Debian.gz
  /etc/bind/internal/** r,
  /etc/bind/private-hint/** r,

  /var/lib/bind/internal/** rw,
  /var/lib/bind/private-hint/** rw,

  /var/lib/bind/internal/ rw,
  /var/lib/bind/private-hint/ rw,
  /var/lib/bind/ rw,

  /var/cache/bind/private-hint/** lrw,
  /var/cache/bind/internal/** lrw,

  /var/cache/bind/private-hint/ rw,
  /var/cache/bind/internal/ rw,

  # Database file used by allow-new-zones
  /var/cache/bind/internal/_default.nzd-lock rwk,
  /var/cache/bind/private-hint/_default.nzd-lock rwk,

  /run/bind/internal/named.pid rw,
  /run/bind/private-hint/named.pid rw,
```

Log files
---------
Need to do auto-rotation of log files:
```bash
vim /etc/logrotate.d/named
```
and fill it with:
```
/var/log/bind/internal/*.log
{
  rotate 30
  daily
  dateext
  dateformat _%Y-%m-%d
  missingok
  su bind bind
  create 0660 root bind
  delaycompress
  compress
  notifempty
  postrotate
    /bin/systemctl reload bind9-internal
  endscript
}
```

Temporary files
---------------
Need to create temporary files, create a tmpfile config file:
```bash
vim /etc/tmpfiles.d/bind9.conf
```
and fill that file with:
```console
#Type Path                 Mode User Group Age Argument

# We set the 2xxx part (g+s) of directories' chmod so
# that when named/bind9 daemon creates 
# the PID file, its ownership would be bind:bind.

d  /run/named          0750 root bind  - -
d  /run/bind           2770 root bind  - -
d  /run/bind/private-hint    2770 root bind  - -
d  /run/bind/internal  2770 root bind  - -
```

```bash
# to do after all files created
chmod 0640      /var/lib/bind/internal/*/*
chown bind:root /var/lib/bind/internal/*/*
```

Creating Keys
=============
It's time to create keys!

Start with RNDC to enable any user with group id 'bind' to use `rndc` utility.
```bash
rndc-confgen -a -A HMAC-SHA512 -k rndc-key -c /etc/bind/keys/rndc.key
```

Creating Bind9 Configurations
=============================
Lastly, the Bind9 configuration files.

Master configuration file
-------------------------
Execute
```bash
vim /etc/bind/named-internal.conf
```
and fill it with:
```nginx
// File: /etc/bind/internal/named.conf
//
// Bind9 configuration
//
// Custom settings for internal network
//
// This is the primary configuration file for the BIND DNS server named.
//

// 'include' statement must have an absolute filespec or it will
// read from current directory ($CWD).

// Please read /usr/share/doc/bind9/README.Debian.gz for information on the 
// structure of BIND configuration files in Debian, *BEFORE* you customize 
// this configuration file.
//
// If you are just adding zones, please do that in /etc/bind/named.conf.local

//  We can share the ACL amongst private/public zones because it's consistent
include "/etc/bind/internal/acl-named.conf";
//
include "/etc/bind/internal/options-named.conf";
include "/etc/bind/internal/statistics-named.conf";
include "/etc/bind/internal/logging-named.conf";
include "/etc/bind/internal/masters-named.conf";
include "/etc/bind/internal/local-named.conf";

//  If you used views in local-named.conf/named.conf.local, 
//  no default-zones needed
////include "/etc/bind/internal/default_zones-named.conf";

include "/etc/bind/internal/keys/keys-named.conf";

include "/etc/bind/internal/controls-named.conf";
include "/etc/bind/internal/servers-named.conf";

include "/etc/bind/internal/dnssec-keys-named.conf";
```

Access Control List
-------------------
For access control list (ACL), we started out with:
```bash
vim /etc/bind/internal/acl-named.conf
```
and fill it with:
```nginx
# localnet
acl localnet_acl {
        127.0.0.0/8;
};

# dmz
acl trusted_real_dmz_acl {
        172.29.1.0/24;
        };
# dmz2
acl trusted_residential_network_dmz_acl {
        172.28.128.0/24;
        };
# blue
acl trusted_residential_network_blue_acl {
        172.28.129.0/24;
        };
# special, single-host, GATEWAY
acl trusted_residential_gateway_acl {
        172.28.130.1;
        };
# green
acl trusted_residential_network_green_acl {
        172.28.130.0/24;
        };
# white
acl trusted_residential_network_white_acl {
        172.28.131.0/24;
        };
# vmnet
acl trusted_residential_network_vmnet_acl {
        192.168.122.0/24;
        };
# rvpn
acl trusted_remote_vpn_acl {
        172.30.0.0/16;
        };

acl trusted_residential_network_acl {
        trusted_residential_network_dmz_acl;
        trusted_residential_network_blue_acl;
        trusted_residential_network_green_acl;
        trusted_residential_network_white_acl;
        trusted_residential_network_vmnet_acl;
        };

acl trusted_all_acl {
        trusted_real_dmz_acl;
        trusted_residential_network_dmz_acl;
        trusted_residential_network_blue_acl;
        trusted_residential_network_green_acl;
        trusted_residential_network_white_acl;
        trusted_residential_network_vmnet_acl;
        trusted_cablesupport_acl;
        localnet_acl;
};
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
`/var/lib/bind/private-hint/db.whitelab`:

```named-zone
    $TTL 86400
    whitelab.                  86400 IN SOA a.myroot-servers.whitelab. (
                                                hostmaster 1 1d 2h 41d 1h )
    whitelab.                  86400 IN NS  a.myroot-servers.whitelab.
    a.myroot-servers.whitelab. 86400 IN A   @MY_ROOT_DNS_SERVER_IP@
```

The custom TLD zone database file wll also be signed as well:

```bash
dnssec-keygen -P -a rsasha256 -b 2048 -n ZONE whitelab
dnssec-keygen -P -a rsasha512 -b 2048 -n ZONE whitelab
dnssec-keygen -f KSK -r /dev/urandom -a RSASHA512 -b 4096 -n ZONE leo
```

Then populated the "white" zone data file with content from
/etc/bind/internal/keys/K


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

```nginx
  view "local_view" {
    root-delegation-only;  // not at global option clause, but view
  }
```

Then we add the Root (".") zone:

```nginx
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

```ini
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
`/etc/bind`, `directory`, directory is a quoted string defining the absolute path for the server e.g. &quot;/var/named&quot;. All subsequent relative paths use this base directory. If no directory options is specified the directory from which BIND was loaded is used. This option may only be specified in a 'global' options statement.
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

Managing Large Private Networks
===============================
If you are hosting multiple internal TLDs, then
[OpenDNSSEC](https://www.opendnssec.org/) software may
be useful to you.

References
==========
* [a local augumented root-zone with DNSSEC](https://dnsworkshop.de/local-augmented-root-zone.html)
* [OpenDNSSEC.org](https://www.opendnssec.org/)

