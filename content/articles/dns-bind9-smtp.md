title: Setting up Bind9 for a Mail Server
date: 2022-04-16 14:24
status: published
tags: Bind9, DNS
category: HOWTO
summary: How to Set Up a Bind9 for a Mail Transport Agent on Debian Bullseye
slug: dns-bind9-smtp
lang: en
private: False

This part covers Postfix Setup as a Mail Transport Agent (MTA, or SMTP server) on Debian Bullseye.

This is the first of 12-part series of setting up a fully secured Mail Server.

Second part is [Postfix Setup for SMTP Server]({filename}smtp-postfix.md).

This article has heavily annotated settings to protect against
accidential `tweaking` by readers/end-users who do not
fully understand the ramification of their action.

By extracting many documentations and placing it next to their
settings, along with all my Earthly knowledge about each
quirks and nannies, I put them all in there as well for your
enjoyment, safety, and peace-of-mind.


# Templates for Your Domain Name

[jtable]
FQDN, template description
`example.test`, your domain name in these article series.
`ns1.example.test`, your authoritative name server.
`mx1.example.test`, your mail server hostname.
[/jtable]


# Installing Bind9 

```console
apt install bind9-host bind9-libs bind9-dnsutils dnsutils
```

# DNS Authoritative Server

All settings for Bind9 `named` daemon are presumed to be located in `/etc/bind`.  (Older OS distros use `/etc/named`.)

All settings for the zone file containing your domain records shall reside in `/var/lib/bind/primary/db.example.test`.  (It used to be under `/var/lib/bind/master`.

## Zone Data File

First, do the zone data files.  Call the first filename as `db.example.test`.

This filespec is `/var/lib/bind/master/db.example.test` and contains the following:

```dns
;;; we get our $ORIGIN setting automatically 
;;; from the `zone "example.test" IN { ...};` statement
;;; in `/etc/named/named.conf`
$TTL 1d  ; ttl is 1 day
@              IN    SOA      dns1.example.test. dns.example.test. (
                              2022041700  ; serial (date & version)
                              8h          ; refresh every 8 hours
                              20m         ; retry after 20 minutes
                              4w          ; expire after 4 weeks
                              20m         ; negative caching ttl is 20 minutes
                              )

; DNS name servers
               IN    NS       dns1.example.test.  ; primary name server
;;;;           IN    NS       dns2.example.test.  ; secondary name server

; SMTP mail gateways
               IN    MX       10 mx.example.test.            ; MX gateway

;;;;           IN    MX       100 fallback-mx.example.test.  ; fallback MX gateway

; hosts
               IN    A        192.168.10.1           ; server
;;;;           IN    AAAA     2001:db8:1192::a:1     ; server (IPv6)
www            IN    CNAME    example.test.          ; WWW server
git            IN    CNAME    example.test.          ; FTP server
git            IN    CNAME    example.test.          ; FTP server
mx             IN    A        192.168.10.1           ; mail gateway
;;;;mx         IN    AAAA     2001:db8:1192::a:1     ; mail gateway (IPv6)
mail           IN    A        192.168.10.1           ; mail server
;;;;mail       IN    AAAA     2001:db8:1192::a:1     ; mail server (IPv6)
imap           IN    A        192.168.10.1           ; IMAP server
;;;;imap       IN    AAAA     2001:db8:1192::a:1     ; IMAP server (IPv6)
smtp           IN    A        192.168.10.1           ; SMTP gateway
;;;;smtp       IN    AAAA     2001:db8:1192::a:1     ; SMTP gateway (IPv6)

; exterior hosts
dns1           IN    A        192.168.1.1            ; primary name server
;;;;dns1       IN    AAAA     2001:db8:1192::a:1     ; primary name server (IPv6)
;;;;dns2       IN    A        198.68.1.1             ; secondary name server
;;;;dns2       IN    AAAA     2001:db8:1192::a:1     ; secondary name server (IPv6)
;;;;fallback-mx IN   A        198.51.100.106         ; fallback mail gateway
;;;;fallback-mx IN   AAAA     2001:db8:1192::a:1     ; fallback mail gateway (IPv6)
```

Records with IPv6 (`AAAA`) have been commented out; or you can switch these `A` records with corresponding `AAAA` ones if your scenario calls for it.

## `named.conf` Configuration File

To make it much easier to edit configuration files now and in the future, the `named.conf` makes use of `include` pragma to include clause-based settings.

This filespec is `/etc/bind/named.conf` and contains the following:

```nginx
# 
# File: named.conf
# Path: /etc/bind
# Title: primary configuration file for an authoritative DNS server.
# 
# example.test TLD: Authoritative Name Server (master)
# 
# Please read /usr/share/doc/bind9/README.Debian.gz for information on the 
# structure of BIND configuration files in Debian, *BEFORE* you customize 
# this configuration file.
# 
# If you are just adding zones, please do that in /etc/bind/named.conf.zones
# 
#  Only include statement or clause keywords goes in here.
# 

# Access Control Lists. 
# Defines one of more access control lists, groups of hosts or 
# users identified by keys, that may be referenced in view and 
# other clauses or statements.
include "/etc/bind/acl-named.conf";

# 
# key
# key clause defines shared keys used to control and authenticate 
# operations such as Dynamic DNS (DDNS) and the remote control 
# channel (the controls clause), and authorize transfer of 
# zone data to other (secondary) name server(s).
# 
# key may also be nested within a view or server clause.
# 
include "/etc/bind/key-named.conf";

# Logging channels
# Configures the location, level and type of logging that 
# BIND performs. Unless you are using syslog you need a 
# logging statement for BIND.
# 
# This logging section describes the logging clause which prior to 
# BIND 9 needed to appear first in the named.conf file. This no 
# longer the case and it may appear anywhere convenient. BIND 
# uses syslogd before a valid logging clause is available so 
# named.conf parse errors and other information will appear in 
# /var/log/messages (depending on syslog.conf) prior to, or in 
# the absence of, a valid logging clause. In the case of windows 
# parse errors are written to the Event Log. Only one logging 
# clause can be defined but multiple channels may be defined 
# to stream logs.
include "/etc/bind/logging-named.conf";

# Named daemon Options
# Groups statements that control generic or global behavior and 
# that have scope for all zones and views unless overridden 
# within a zone, views or other clause
# 
# Exactly one 'options' clause must be defined.  
include "/etc/bind/options-named.conf";

# Control channel
# Describes and controls access to the control channel used by 
# the remote administrator when using the rndc utility.
include "/etc/bind/controls-named.conf";

# Masters
# Defines a list of one or more masters that may be 
# referenced from a masters statement in a zone clause of 
# type slave or an also-notify statement in a zone clause 
# of type master. Note: Somewhat confusing because the 
# name, masters, is used for both the free-standing clause 
# and a statement within a zone clause.
# 
# 'masters' is commented out as this here is a primary 
# (master) DNS server
# 
#include "/etc/bind/masters-named.conf";

# zone is not used as a clause here, but as a zone statement
# within 'view' clause(s).

# view
# Controls BIND functionality and behaviour based on the host address(es).
# 
# Most commonly used to setup "split-horizon" serving of DNS records:
#     Serve up a set of records on one external interface while serving
#     up a different value of this same DNS record on an internal interface.
# 
include "/etc/bind/views-named.conf";

# statistics-channels
# Defines access to XML (browser) statistics.
# CISecurity recommends totally-disabling 
# statistics-channels in production mode.
# 
#include "/etc/bind/statistics-named.conf";
```

Recap: The sets of config files in `/etc/bind` subdirectory are:

[jtable]
filespec, description
`named.conf`, main configuration file for the `named` daemon.
`acl-named.conf`, All ACLs goes under `acl` clauses within this file.
`key-named.conf`, All keys goes under `key` clauses.
`logging-named.conf`, All ACLs goes under `acl` clauses.
`options-named.conf`, All top-level (all-views/all-zones/all-servers) settings goes under the mandatory but lone `options` clause.
`controls-named.conf`, All connections for CLI-based or remote tools to this authoritative name server are detailed and opened under `controls` clause.
`server-named.conf`, All non-primary/non-master server may get detailed, most notably incompatible non-Bind9 DNS servers goes under their own `server` clause, if any.
`masters-named.conf`, List of all name servers that are expected to receive a NOTIFY from or send an AXFR/IXFR requests to.
`view-named.conf`, All View files are included under this file.
`statistics-named.conf`, Perform statistic collection during pre-production, QA, IT, or unit tests.
[/jtable]

## Bind9 `key` Clause

This filespec is `/etc/bind/key-named.conf` and contains the following:

```nginx
# File: key-named.conf
# Path: /etc/bind
# Title: Keys settings for ISC Bind9 `named` daemon
# 
# Defines shared keys used to control and authenticate operations 
# such as Dynamic DNS (DDNS) and the remote control channel (the 
# controls clause). 
# May be nested and used repeatedly within a view clause.
# 
# Most common keys are given below as example:
# 
# DDNS_UPDATER key
# used with isc-dhcpd or DHCP server for dynamic DNS updating
# 
#     key DDNS_UPDATER {
#             algorithm hmac-md5;
#             secret "abcdefghijklmnopqrstuv==";
#             };

# NOTE: not recommended, used "rndc-confgen -a" and rndc.key file instead.
# 
#     # counterpart key is frequently stored in rndc.conf (i.e., webmin)
#     key "rndc-key" {
#             algorithm hmac-md5;
#             secret "abcdefghijklmnopqrstuv==";
#             };

# rndc-remote key
# used by remote (or local) `rndc` CLI command
# Note: do not forget to add additional remote access to controls clause.
#       `controls` clause is in controls-named.conf file.
# 
#         key "rndc-remote" {
#             algorithm hmac-md5;
#             secret "OmItW1lOyLVUEuvv+Fme+Q==";
#         };
# 
# Note: The keys clause above would normally be placed in a 
# separate secure file and included into one of the named.conf file group.


# for use with "local-ddns" key (a default for session-based queries like
# sftdyn), we declare:
# 
#    session-keyname "local-ddns";
#    session-keyfile "/var/cache/bind/session.key";
# 
# in options group/clause within /etc/bind/options-named.conf instead
# Then keys are made automatically at `named` daemon startup.

# rndc-key key is defined in /etc/bind/keys/rndc.key
# rndc.key file is auto-generated by "rndc-confgen -a" command
# rndc.key file gets included in both named's named.conf 
#     and rndc's rndc.conf files.

# keyname: rndc-key
# Limit 'rndc-key' to 'localhost'/127.0.0.1 for use with 'rndc' utility
# It got placed under `/var/lib` as this key may change often
include "/var/lib/bind/keys/rndc.sha512.key";

# keyname: public-master-to-public-secondary
# For this public-master to send DNS update to public-secondaries
include "/var/lib/bind/keys/public-master-to-public-secondary.sha512.key";
```

Recap: Key Files
[jtable]
filespec, description
`/var/lib/bind/keys/rndc.sha512.key`, Key for `rndc` tool to access and update with.
`/var/lib/bind/keys/zone-transfer-public-master-to-public-secondary.sha512.key`, allows secondaries to receive the transfer of any updated zone data files from this authoritative name server.
[/jtable]

## Bind9 `acl` Clause

This filespec is `/etc/bind/acl-named.conf` and contains the following:

```nginx
# 
# File: acl-named.conf
# Path: /etc/bind
# Title: Access Control Lists settings for ISC Bind9 `named` daemon
# 
# The acl clause allows fine-grained control over what hosts or 
# users may perform what operations on the name server.
# 
# Defines one of more access control lists, groups of hosts 
# or users identified by keys, that may be referenced in view 
# and other clauses or statements.
# 
# Only acl keywords goes here.
# 
#
# acl's define a address_match_list e.g. IP address(es), which 
# can then be referenced (used) in a number of statements and 
# the view clause(s). acl's MUST be defined before they are 
# referenced in any statement or clause. For this reason they 
# are usually defined first in the named.conf file. 'acl-name' 
# is an arbitrary (but unique) quoted string defining the 
# specific list. The 'acl-name' is the method used to 
# subsequently reference the particular list. Any number of 
# acl's may be defined.
# 
# The following special acl-name values are built into BIND:
# 
#    "none" - matches no hosts
# 
#    "any" - matches all hosts
# 
#    "localhost" - matches all the IP address(es) of the 
#                  server on which BIND is running e.g. if the 
#                  server has a single interface with an IP 
#                  address of 192.168.2.3 then localhost will 
#                  match 192.168.2.3 and 127.0.0.1 (the 
#                  loopback address is always present).
# 
#    "localnets" - matches all the IP address(es) and subnetmasks 
#                  of the server on which BIND is running i.e. if 
#                  the server has a single interface with an IP 
#                  address of 192.168.2.3 and a netmask of 
#                  255.255.255.0 (or 192.168.2.2/24) then 
#                  localnets will match 192.168.2.0 to 
#                  192.168.2.255 and 127.0.0.1 (the loopback is 
#                  assumed to be a single address). Some systems 
#                  do not provide a way to determine the prefix 
#                  lengths of local IPv6 addresses. In such a case, 
#                  localnets only matches the local IPv6 addresses, 
#                  just like localhost.
# 
# acl clause syntax:
# 
#    acl acl-name { 
#        address_match_list;
#    };

acl localhost_direct_acl { 127.0.1.1; ::1:1; };
acl localhost_subnet_acl { 127.0.0.0/8; };

# Only Hurricane Electric ISP Only
# Interesting thing about Hurricane Electric offering 
# of their free five secondary DNS servers is this:
#
# They have a special standalone slave server that 
# is hidden from public.
#
# When your primary server feels a need to push out 
# a notify (due to zone data being updated or DNSSEC 
# rekeyed), it will send a NOTIFY message to the 
# secondary name server.  
#
# Then HE.NET has a special slave that does the 
# requests for zone data transfer from your primary 
# server and handles all of your zone data transfer 
# (AXFR/IXFR) requests.
#
# Sequences are:
# *  our primary server sends the NOTIFY only to 
#    the 'ns1.he.net' and then a few seconds later,
#
# *  our primary server receives AXFR/IXFR requests 
#    ONLY from 'slave.dns.he.net'.

# used by `allow-transfer` option in `view "public" { zone "example.test"`
#
acl acl_grant_axfr_to_trusted_3rd_party_downstream_secondaries {
        key public-master-to-public-secondary;
        216.218.133.2;  # slave.dns.he.net
        };

# cannot be used by `also-notify` option but listed here for completeness
#
acl acl_notify_only_to_trusted_3rd_party_downstream_secondaries {
        key public-master-to-public-secondary;
        216.218.130.2;  # ns1.he.net
        };

###################################################
# Empty placeholder(s) (for future expansion)
###################################################

# Define `acl_public_master_nameserver` if this
# host is being used as a `secondary` or `slave`
# nameserver.
acl acl_public_master_nameserver { };

# Define `acl_bastion_internal_nameserver` if this 
# host is being used as an external bastion DNS 
# nameserver if and only if an internal bastion DNS
# exists and is up and running.
#
acl acl_bastion_internal_nameserver { };

# Define `acl_hidden_master_nameserver` if this host 
# is being used as a public (master) authoritative 
# nameserver if and only if a hidden master exists 
# and is up and running.
#
acl acl_hidden_master_nameserver { };

# Define `acl_dhcp_server_for_ddns_support` if this 
# host is being used as a Dynamic DNS server (has an 
# ISC dhcpd daemon up and running).
#
acl acl_dhcp_server_for_ddns_support { };
```


## Bind9 `logging` Clause

This filespec is `/etc/bind/logging-named.conf` and contains the following:

```nginx
# 
# File: logging-named.conf
# Path: /etc/bind
# Title: Logging settings for ISC Bind9 `named` daemon
# 
# Configures the location, level and type of logging that 
# BIND performs. Unless you are using syslog you need a 
# logging statement for BIND.
# 
# This section describes the logging clause which prior to 
# BIND 9 needed to appear first in the named.conf file. This 
# no longer the case and it may appear anywhere convenient. 
# BIND uses syslogd before a valid logging clause is available 
# so named.conf parse errors and other information will appear 
# in /var/log/messages (depending on syslog.conf) prior to, 
# or in the absence of, a valid logging clause. In the case 
# of windows parse errors are written to the Event Log. Only 
# one logging clause can be defined but multiple channels 
# may be defined to stream logs.

# logging Clause Syntax
# 
# BIND provides comprehensive logging features. 
# type below are keywords;
# 
# logging {
#    [ channel channel_name {
#      ( file path name
#          [ versions ( number | unlimited ) ]
#          [ size size_spec ]
#        | syslog syslog_facility
#        | stderr
#        | null );
#      [ severity (critical | error | warning | notice |
#                  info | debug [ level ] | dynamic ); ]
#      [ print-category yes | no; ]
#      [ print-severity yes | no; ]
#      [ print-time yes | no; ]
#    }; ]
#    [ category category_name {
#      channel_name ; [ channel_name ; ... ]
#    }; ]
#    ...
# };

# The following notes describe the various fields and values:
#   channel channel_name  BIND will accept multiple channel definitions 
#                         in a single logging statement. 'channel_name' is 
#                         normally written as a non-space name, for 
#                         instance, my_channel but it can be written as a 
#                         quoted string, for instance, "my channel". It is 
#                         an arbitrary but unique name used to associate 
#                         the category statement with this channel 
#                         definition or it may take one of the standard 
#                         (pre-defined) values below:
# 
#                         "default_syslog"   log everything to syslog 
#                                              (default logging destination)
#                         "default_debug" 
#                         "default_stderr"   output to stderr 
#                                              (normally the console)
#                         "null"             discard all log entries 
#                                              (write to /dev/null)
#   file 'path_name' is a quoted string defining the absolute path to 
#                    the logging file, for example, 
#                    "/var/log/named/namedlog.log". From the grammar 
#                    above 'file', 'syslog', 'stderr' and 'null' are 
#                    mutually exclusive for a 'channel'.
#   versions   'versions' may take the parameter 'number' or 'unlimited' 
#              and defines the number of file versions that should be 
#              kept by BIND. Version files are created by BIND by 
#              appending .0, .1 etc to the file named defined by the 
#              file parameter. Files are 'rolled' (renamed or 
#              overwritten) so .0 will always contain the last log 
#              information prior to commencing the new log., .1 the next 
#              and so on. 'unlimited' currently implies 'versions 99'. 
#              Unless a size parameter is used new log versions will only 
#              be 'rolled' when BIND is restarted. If no versions 
#              statement is defined a single log file of unlimited size 
#              is used and on restart new data is appended to the defined 
#              file. This can get to be a very big file.
#   size size_spec 'size' allows you to define a limit to the file size 
#                  created. A numeric only size_spec value is assumed to 
#                  be the size in bytes, you may use the short forms k 
#                  or K, m or M, g or G e.g. 25m = 25000000. size and 
#                  versions are related in the following way:
# 
#                      1. If you specify a size value and NO versions 
#                         parameter when the size limit is reached BIND 
#                         will stop logging until the file size is reduced 
#                         to below the threshold defined i.e. by deleting 
#                         or truncating the file.
#                      2. If you specify a size AND a versions parameter 
#                         the log files will be 'rolled' (renamed and 
#                         overwritten as defined in the versions section 
#                         above) when the size limit is reached.
#                      3. If you specify NO size AND a versions parameter 
#                         the log files will be 'rolled' (renamed and 
#                         overwritten as defined in the versions section 
#                         above) only when BIND is restarted.
# 
#   syslog syslog_facility 'syslog' indicates that this channel will use 
#                          syslogd logging features (as defined in 
#                          syslog.conf). The syslog_facility is the 
#                          facility definition for 'syslog' and may be 
#                          found in syslog's man pages. From the grammar 
#                          above 'file', 'syslog', 'stderr' and 'null' 
#                          are mutually exclusive for a 'channel'.
#   stderr    'stderr' writes to the current standard out and would 
#             typically be only used for debug purposes. From the 
#             grammar above 'file', 'syslog', 'stderr' and 'null' 
#             are mutually exclusive for a 'channel'.
# 
#   null     'null' writes to /dev/null - the bit bucket, nowhere. 
#             It does not produce a log. From the grammar above 'file', 
#             'syslog', 'stderr' and 'null' are mutually exclusive for 
#             a 'channel'.
# 
#   severity  Controls the logging levels and may take the values defined. 
#             Logging will occur for any message equal to or higher than 
#             the level specified (=>) lower levels will not be logged.
# 
#             Severity     Description
#             critical     only critical errors.
#             error        error and above.
#             warning      warning and above.
#             notice       notice and above.
#             info         info and above - log starting to get chatty.
#             debug        debug and above. Various debug levels can be 
#                            defined with 'debug 0' meaning no debugging.
#             dynamic      debug and above. Means assume the global debug 
#                            level defined by either the command line 
#                            parameter -d or by running rndc trace
# 
#   print-time yes | no     Controls whether the date and time are written 
#                           to the output channel (yes) or not (no). The 
#                           default is 'no'.
#   print-severity yes | no     Controls whether the severity level is 
#                               written to the output channel (yes) or 
#                               not (no). The default is 'no'.
#   print-category yes | no     Controls whether the severity level is 
#                               written to the output channel (yes) or 
#                               not (no). The default is 'no'.
#   category category_name     Controls what categories are logged to 
#                              the various defined or default 
#                              'channel_names'. The category_name (a 
#                              quoted string, for example, "default") may 
#                              take one of the following values:
# 
#              Category     Description
#              client       Processing of client requests.
#              config       Configuration file parsing and processing.
#              database     Messages relating to the databases used 
#                           internally by the name server to store zone 
#                           and cache data.
#              default     Logs all values which are not explicitly 
#                           defined in category statements i.e. if this 
#                           is the only category defined it will log all 
#                           categories listed in this table with the 
#                           exception of queries which are not turned 
#                           on by default.
#              delegation-only     Logs queries that have returned 
#                           NXDOMAIN as the result of a delegation-only 
#                           zone or a delegation-only statement in a 
#                           hint or stub zone declaration.
#              dispatch     Dispatching of incoming packets to the server 
#                           modules where they are to be processed.
#              dnssec     DNSSEC and TSIG protocol processing.
#              general     Anything that is not classified as any other 
#                           item in this list defaults to this category..
#              lame-servers     Lame servers. Mis-configuration in the 
#                           delegation of domains discovered by BIND 9 
#                           when trying to authoritative answers. If 
#                           the volume of these messages is high many 
#                           users elect to send them to the null 
#                           channel e.g. category lame-servers {null;}; 
#                           statement.
#              network     Logs all network operations.
#              notify     Logs all NOTIFY operations.
#              queries     Logs all query transactions. The querylog 
#                           statement may be used to override this 
#                           category statement. This entry can generate 
#                           a substantial volume of data very quickly. 
#                           This category is not turned on by default 
#                           and hence the default type above will not 
#                           log this information.
#              resolver     Name resolution including recursive lookups 
#                           performed on behalf of clients by a caching 
#                           name server.
#              rpz     All operations related to Response Policy Zone 
#                           (RPZ) processing. Even when RPZ zones are 
#                           disabled (using policy disabled parameter 
#                           in the response-policy statement) the 
#                           operation is completed, logged then discarded 
#                           (the real response is returned to the user).
#              rate-limit     All operations related to one or more 
#                           rate-limit statements in the options or 
#                           view clauses.
#              security     Approval and denial of requests.
#              unmatched     No matching view clause or unrecognized 
#                           class value. A one line summary is also 
#                           logged to the client category. By default 
#                           this category is sent to the null channel.
#              update     Logging of all dynamic update (DDNS) transactions.
#              update-security     Approval and denial of update 
#                           requests used with DDNS.
#              xfer-in     Details of zone transfers the server is receiving.
#              xfer-out     Details of zone transfers the server is sending.


logging {
    channel default_file {
        # It's /var/log/named due to immense legacy presense of many log tools
        # Ideally, it would have been /var/log/bind, but carpa diem.
        file "/var/log/named/default.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel general_file {
        file "/var/log/named/general.log" versions 3 size 5m;
        # severity dynamic;
        severity debug 1;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel database_file {
        file "/var/log/named/database.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel security_file {
        file "/var/log/named/security.log" versions 3 size 5m;
        # severity dynamic;
        severity debug 63;
        print-time yes;
        print-severity true;
        # print-category true;
        };
    channel config_file {
        file "/var/log/named/config.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel resolver_file {
        file "/var/log/named/resolver.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel xfer-in_file {
        file "/var/log/named/xfer-in.log" versions 3 size 5m;
        severity notice;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel xfer-out_file {
        file "/var/log/named/xfer-out.log" versions 3 size 5m;
        severity notice;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel notify_file {
        file "/var/log/named/notify.log" versions 3 size 5m;
        severity warning;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel client_file {
        file "/var/log/named/client.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel unmatched_file {
        file "/var/log/named/unmatched.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel queries_file {
        file "/var/log/named/queries.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel query-errors_file {
        file "/var/log/named/query-errors.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel network_file {
        file "/var/log/named/network.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel update_file {
        file "/var/log/named/update.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel update-security_file {
        file "/var/log/named/update-security.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel dispatch_file {
        file "/var/log/named/dispatch.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel dnssec_file {
        file "/var/log/named/dnssec.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel lame-servers_file {
        file "/var/log/named/lame-servers.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel delegation-only_file {
        file "/var/log/named/delegation-only.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };
    channel rate-limit_file {
        file "/var/log/named/rate-limit.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
        };

    category default { default_file; };
    category general { general_file; };
    category database { database_file; };
    category security { security_file; };
    category config { config_file; };
    category resolver { resolver_file; };
    category xfer-in { xfer-in_file; };
    category xfer-out { xfer-out_file; };
    category notify { notify_file; };
    category client { client_file; };
    category unmatched { unmatched_file; };
    category queries { queries_file; };
    category query-errors { query-errors_file; };
    category network { network_file; };
    category update { update_file; };
    category update-security { update-security_file; };
    category dispatch { dispatch_file; };
    category dnssec { dnssec_file; };
    category lame-servers { lame-servers_file; };
    category delegation-only { delegation-only_file; };
    category rate-limit { rate-limit_file; };
    };
```


## Bind9 `options` Clause

This filespec is `/etc/bind/options-named.conf` and contains the following:

```nginx
# 
# File: options-named.conf
# Path: /etc/bind
# Title: General options settings for ISC Bind9 named daemon
# 
# Groups statements that control generic or global behavior and that 
# have scope for all zones and views unless overridden within a 
# zone, views or other clause.
# 
# The options clause group together statements that have global 
# scope - the statements apply to all zones or views unless overridden 
# by the same statement in a view or zone clause. Only one options 
# clause should be defined in a named.conf file. The options clause 
# can take a serious list of statements.
# 

# If there is a firewall between you and nameservers you want
# to talk to, you may need to fix the firewall to allow multiple
# ports to talk.  See http:#www.kb.cert.org/vuls/id/800113

# If your ISP provided one or more IP addresses for stable 
# nameservers, you probably want to use them as forwarders.  
# Uncomment the following block, and insert the addresses replacing 
# the all-0's placeholder.

options {

    # version specifies the string that will be returned to 
    # a version.bind query when using the chaos class only. 
    # version_string is a quoted string, for example, "get lost" 
    # or something equally to the point. We tend to use it in 
    # all named.conf files to avoid giving out a version number 
    # such that an attacker can exploit known version-specific 
    # weaknesses. This statement may only be used in a global 
    # options clause
    #
    version "Funky DNS v1.1";

    # managed-keys-directory (new since Bind 9.11)
    #
    managed-keys-directory "/var/lib/bind/dynamic";

    # directory is a quoted string defining the absolute path for 
    # the server e.g. "/var/named". All subsequent relative paths 
    # use this base directory. If no directory options is specified 
    # the directory from which BIND was loaded is used. This option 
    # may only be specified in a 'global' options statement.
    # Do not fight with yourself on this, use absolute dirpath ... always
    #
    directory "/var/cache/bind";

    #========================================================================
    # If BIND logs error messages about the root key being expired,
    # you will need to update your keys.  See https:#www.isc.org/bind-keys
    # yes = use built-in DLV keys
    # auto = use built-in DLV keys
    # no = use bind.keys file
    #========================================================================
    # dnssec-validation indicates that a resolver (a caching or 
    # caching-only name server) will attempt to validate replies 
    # from DNSSEC enabled (signed) zones. To perform this task the 
    # server also needs either a valid trusted-keys clause (containing 
    # one or more trusted-anchors or a managed-keys clause. 
    # Since 9.5 the default value is dnssec-validation yes;. 
    # This statement may be used in a view or global options clause.
    #
    dnssec-validation yes;

    # bindkeys-file (new since Bind 9.11)
    # bindkeys-file "/etc/bind/named.iscdlv.key"; Obsoleted 9.16

    # listen-on defines the port and IP address(es) on which 
    # BIND will listen for incoming queries. The default is 
    # port 53 on all server interfaces. Multiple listen-on 
    # statements are allowed. This statement may only be used 
    # in a global options clause.
    # 
    # Note: on a multi-homed host, you might want to tell named
    # to listen for queries only on certain interfaces
    #/listen-on-v6 { none; };
    #
    listen-on-v6 port 53 { 2604:db8:0:201::1; };

    # listen-on-v6 turns on BIND to listen for IPv6 queries. If 
    # this statement is not present and the server supports IPv6 
    # (only or in dual stack mode) the server will listen for 
    # IPv6 on port 53 on all server interfaces. If the OS supports 
    # RFC 3493 and RFC 3542 compliant IPv6 sockets and the 
    # address_match_list uses the special any name then a single 
    # listen is issued to the wildcard address. If the OS does not 
    # support this feature a socket is opened for every required 
    # address and port. The port default is 53. Multiple 
    # listen-on-v6 statements are allowed. This statement may only 
    # be used in a global options clause. Do not try to start bind 
    # with the -4 argument when you use this statement.
    #
    listen-on port 53 {
            192.168.10.1;
        };

    # If recursion is set to 'yes' (the default) the server will 
    # always provide recursive query behaviour if requested by the 
    # client (resolver). If set to 'no' the server will only 
    # provide iterative query behaviour - normally resulting in a 
    # referral. If the answer to the query already exists in the 
    # cache it will be returned irrespective of the value of this 
    # statement. This statement essentially controls caching 
    # behaviour in the server. The allow-recursion statement and the 
    # view clauses can provide fine-grained control. This statement 
    # may be used in a view or a global options clause.
    # NOTE: Always set 'recursion no' at global option and selectively
    # enable 'recursion yes' in certain zones AND either with 
    # 'allow recursion { localhost;};' on badguy/public view OR
    # 'allow recursion { any;};' on internal/safe view.
    # 
    # CISecurity says all public-facing interfaces should 
    # not support recursion.
    # recursion yes;
    # 
    # Note: says public-facing authoritative-only server (used in
    #    hidden-master configuration or what nots) cannot do recursion.
    #
    recursion no;

    # notify behaviour is applicable to both master zones (with 
    # 'type master;') and slave zones (with 'type slave;') and if 
    # set to 'yes' (the default) then, when a zone is loaded or 
    # changed, for example, after a zone transfer, NOTIFY messages 
    # are sent to the name servers defined in the NS records for 
    # the zone (except itself and the 'Primary Master' name server 
    # defined in the SOA record) and to any IPs listed in any 
    # also-notify statement.
    # 
    # If set to 'no' NOTIFY messages are not sent.
    # 
    # If set to 'explicit' NOTIFY is only sent to those IP(s) listed 
    # in an also-notify statement.
    # 
    # If a global notify statement is 'no' an also-notify statement may 
    # be used to override it for a specific zone, and conversely if 
    # the global options contain an also-notify list, setting notify 
    # 'no' in the zone will override the global option. This 
    # statement may be specified in zone, view clauses or in a 
    # global options clause.
    # 
    # options {
    # ....
    # also-notify {10.1.0.15; 192.168.1.7;}; # all zones
    # ....
    # };
    # ....
    # zone "example.com in{
    # ....
    # # NS RRs and global also-notify
    # notify yes; 
    # ....
    # };
    # zone "example.net in{
    # ....
    # # no NOTIFY to NS RRs
    # # NOTIFY to also-notify IPs above
    # notify explicit; 
    # ....
    # };
    # 
    # Notes:
    # NOTIFY does not indicate that the zone data has changed, but 
    # rather that the zone data may have changed. The receiver of 
    # the NOTIFY message should query the zone SOA directly from 
    # the IP(s) defined in the zone's masters statement.
    # 
    # Even if the implementation includes the zone's SOA in the 
    # NOTIFY message (allowed for in the standards) the receiver 
    # is mandated NOT to use this data (by RFC 1996). Instead the 
    # receiving server must query the zone's SOA from the IP(s) 
    # defined in the masters statement.
    # 
    # By default, after a slave has transferred a zone it will 
    # also send out NOTIFY messages to all the zone's NS RRs (except 
    # itself obviously). This behavior can be inhibited by using a 
    # 'notify no;' statement in the slave's zone clause.
    # 
    # do not generate notify messages for all zones on a restart.
    # override for authorative zones
    # Prevent DoS attacks by generating bogus zone transfer
    # requests.  This will result in slower updates to the
    # slave servers (e.g. they will await the poll interval
    # before checking for updates).
    #
    notify yes;

    # allow-update defines an address_match_list of hosts that 
    # are allowed to submit dynamic updates for master 
    # zones, and thus this statement enables Dynamic DNS. 
    # The default in BIND 9 is to disallow updates from 
    # all hosts, that is, DDNS is disabled by default. 
    # This statement is mutually exclusive with update-policy 
    # and applies to master zones only. The example shows 
    # DDNS for three zones: the first disables DDNS 
    # explicitly, the second uses an IP-based list, and 
    # the third references a key clause. The allow-update 
    # in the first zone clause could have been omitted 
    # since it is the default behavior. 
    # 
    # Many people like to be cautious in case the default mode changes.
    # 
    # Note: Always say 'none' at global option level, then relax it
    #      at view or zone option level.
    #
    allow-update { none; };

    # allow-transfer is allow-transfer defines a match list e.g. 
    # IP address(es) that are allowed to transfer (copy) the 
    # zone information from the server (master or slave for the 
    # zone). The default behaviour is to allow zone transfers to 
    # any host. While on its face this may seem an excessively 
    # friendly default, DNS data is essentially public (that's 
    # why its there) and the bad guys can get all of it anyway. 
    # However if the thought of anyone being able to transfer 
    # your precious zone file is repugnant, or (and this is far 
    # more significant) you are concerned about possible DoS 
    # attack initiated by XFER requests, then use the 
    # following policy:
    # 
    # options {
    #    ....
    #    # ban everyone by default
    #    allow-transfer {"none";};
    # };
    # ...
    # zone "example.com" in{
    #   ....
    #   # explicity allow the slave(s) in each zone
    #   allow-transfer {192.168.0.3;};
    # };
    # 
    # This statement may be used in a zone, view or global options clause.
    # sets BINDs default behaviour to refuse all zone transfers. 
    # Without setting this option, anyone can transfer any zone.
    # Zone tranfers limited to members of the "xfer" ACL.
    # ban everyone by default
    # 
    # Note:: We say 'none' at global option level, but relax it more
    #      something else at view option level (preferably 
    #      not at zone level).
    #
    allow-transfer { none; };

    # allow-query defines an match list of IP address(es) which 
    # are allowed to issue queries to the server. If not specified 
    # all hosts are allowed to make queries (defaults to 
    # allow-query {any;};).
    # 
    # allow-query may be used in a zone, view or a global options clause.
    #
    allow-query { any; };

    # allow-query-cache, since BIND 9.4 allow-query-cache (or its 
    # default) controls access to the cache and thus effectively 
    # determines recursive behavior. This was done to limit the 
    # number of, possibly inadvertant, OPEN DNS resolvers. 
    # allow-query-cache defines an address_match_list of IP 
    # address(es) which are allowed to issue queries that access 
    # the local cache - without access to the local cache 
    # recursive queries are effectively useless so, in effect, 
    # this statement (or its default) controls recursive behavior. 
    # Its default setting depends on:
    # 
    #   If recursion no; present, defaults to 
    #       allow-query-cache {none;};. No local cache access permitted.
    # 
    #   If recursion yes; (default) then, if allow-recursion present, 
    #       defaults to the value of allow-recursion. Local cache 
    #       access permitted to the same address_match_list as 
    #       allow-recursion.
    # 
    #   If recursion yes; (default) then, if allow-recursion is NOT 
    #       present, defaults to 
    #       allow-query-cache {localnets; localhost;};. 
    #       Local cache access permitted to localnets and localhost only.
    # 
    # Both allow-query-cache and allow-recursion statements are allowed 
    # - this is a recipe for conflicts and a debuggers dream come true. 
    # Use either statement consistently - by preference allow-recursion.
    # 
    # These statements may be used in a view or a global options clause.
    # allow-query-cache { any; };

    # allow-recursion defines a address_match_list of IP 
    # address(es) which are allowed to issue recursive queries to 
    # the server. When allow-recursion is present allow-query-cache 
    # defaults to the same values. If allow-recursion is NOT present 
    # the allow-query-cache default is assumed (localnets, 
    # localhost only). Meaning that only localhost (the server's 
    # host) and hosts connected to the local LAN (localnets) are 
    # permitted to issue recursive queries.
    # 
    # allow-recursion-on defines the server interface(s) from 
    # which recursive queries are accepted and can be useful 
    # where a server is multi-homed, perhaps in conjunction with 
    # a view clause. Defaults to allow-recursion-on {any;}; 
    # meaning that recursive queries are accepted on any server 
    # interface.
    # 
    # allow-recursions is only relevant if recursion yes; is present 
    # or defaulted.
    # 
    # NOTE: Always set 'recursion no' at global option and selectively
    # enable 'recursion yes' in certain zones AND either with 
    # 'allow recursion { localhost;};' on badguy/public view OR
    # 'allow recursion { any;};' on internal/safe view.
    # 
    # These statements may be used in a view or a global options clause.
    # 
    # Note: says public-facing authoritative-only server (used in
    #    hidden-master configuration or what nots) should not do recursion.
    #
    allow-recursion { none; };

    # dnssec-enable indicates that a secure DNS service is being used 
    # which may be one, or more, of TSIG (for securing zone 
    # transfers or DDNS updates), SIG(0) (for securing DDNS 
    # updates) or DNSSEC. Since BIND9.5 the default value is 
    # dnssec-enable yes;. This statement may be used in a view 
    # or global options clause.
    # dnssec-enable yes; # OBSOLETED
    #/dnssec-lookaside auto;   OBSOLETED in 9.15

    # dnssec-accept-expired is new since Bind 9.11, probably want this as yes.
    dnssec-accept-expired no;

    # dnssec-lookaside (obsoleted since 9.16+, introduced 9.11+)
    #    auto - automatically determines methods
    #    <root> trust-anchor dlv.isc.org.
    # dnssec-lookaside . trust-anchor dlv.isc.org.;  OBSOLETED since 9.16

    # auth-nxdomain: If auth-nxdomain is 'yes' allows the server to 
    # answer authoritatively (the AA bit is set) when returning 
    # NXDOMAIN (domain does not exist) answers, if 'no' (the 
    # default) the server will not answer authoritatively. 
    # NOTE: This changes the previous BIND 8 default setting. 
    # This statement may be used in a view or a global options clause.
    # conforms to RFC1035
    # Note:  You might remember your ISP provider responding with 
    #        fake landing page of their own design when you mistype
    #        a website name: THIS.
    #
    auth-nxdomain no;

    # key-directory is a quoted string defining the absolute path, for 
    # example, "/var/named/keys" where the keys used in the dynamic 
    # update of secure zones may be found. Only required if this 
    # directory is different from that defined by a directory 
    # option. This statement may only be used in a global options clause.
    # typical name for this subdirectory would be 'keys', 'key', 'dynamic'.
    #
    key-directory "/var/lib/bind/dynamic";

    # The ID the server will return via a query for ID.SERVER with 
    # type TXT, under class CH (CHAOS). Specifying none disables 
    # processing of the queries otherwise it will return id-string. 
    # The default is none. This statement may only be used in 
    # a global options clause.
    #
    server-id none;    # Ignore EDNS0/NSID

    # blackhole defines a address_match_list of hosts that the 
    # server will NOT respond to, or answer queries for. 
    # The default is 'none' (all hosts are responded to). 
    # This statement may only be used in a global options clause.
    #
    blackhole {
        # Private RFC 1918 addresses
        10/8; 192.168/16; 172.28/24;
        # Multicast
        224/8;
        # Link Local
        169.254/16;
    };

    # query-source: Defines the IP address (IPv4 or IPv6) and 
    # optional port to be used as the source for outgoing queries 
    # from the server. The BIND default is any server interface 
    # IP address and a random unprivileged port (1024 to 65535). 
    # The optional port is only used to control UDP operations. 
    # avoid-v4-udp-ports and avoid-v6-udp-ports can be used to 
    # prevent selection of certain ports. 
    # This statement may be used in a view or a global options clause.
    # 
    # Health Warning: Use of this option to define a fixed port 
    # number is extremely dangerous and can quickly lead to 
    # cache poisoning when used with any caching DNS server 
    # definition. An attacker normally has to guess both the 
    # transaction ID and the port number (both 16 bit values). 
    # If the port is fixed the bad guys have only to guess the 
    # transaction ID. You just made their job a lot easier. 
    # Don't do it.
    # CISecurity says do not use 'query-source'

    # pid-file file contains the process id when named/bind is running
    # pid-file is a quoted string and allows you to define where 
    # the pid (Process Identifier) used by BIND is written. 
    # If not present it is distribution or OS specific 
    # typically /var/run/named.pid or /etc/named.pid. It may be 
    # defined using an absolute path or relative to the directory 
    # parameter. 
    # `pid-file` statement may only be used in a global options clause.
    #
    pid-file "/var/run/named/named.pid";

    # `statistics-file` is the (should-be-absolute) 
    # file path specification of the file that the 
    # server appends statistics to when instructed 
    # to do so using `rndc stats`. 
    # If not specified, the default is `named.stats` in the 
    # server's current directory. 
    # This option may only be specified in a 'global' options statement.
    #
    statistics-file "/var/log/bind/named_stats.txt";

    # `zone-statistics`:  if set to 'yes', the server 
    # will collect statistical data on all zones (unless 
    # specifically turned off on a per-zone basis by specifying 
    # `zone-statistics no` in the `zone` statement). These statistics 
    # may be accessed using `rndc stats`, which will dump them to 
    # the file listed in the `statistics-file` options. 
    # This option may be specified in a `zone` 
    # statement or a `options` clause.
    #
    zone-statistics no;

    # `dump-file` is a quoted string defining the absolute path 
    # where BIND dumps the database (cache) in response to a 
    # `rndc dumpdb`. If not specified, the default is 
    # `named_dump.db` in the location specified by a `directory` option. 
    # This option may only be specified in a `options` clause.
    #
    dump-file "/var/cache/bind/cache_dump.db";

    check-names response fail;
    check-names secondary fail;
    check-names master fail;
    check-dup-records fail;
    check-mx fail;
    check-wildcard yes;
    check-integrity yes;
    check-mx-cname fail;
    check-srv-cname fail;
    check-sibling yes;
    check-spf warn;

    minimal-any yes;

    max-cache-size unlimited;
    };
```


## Bind9 `controls` Clause

This filespec is `/etc/bind/controls-named.conf` and contains the following:

```nginx
# 
# File: controls-named.conf
# Path: /etc/bind
# Title: Administrative Channel settings for ISC Bind9 named daemon
# 
# Describes and controls access to the control channel used 
# by the remote administrator when using the `rndc` utility.
# 
# The `controls` clause is used to define access information 
# and controls when using remote administration services, for 
# example, the `rndc` utility. The `controls` clause takes a 
# single inet statement type, though more than one inet 
# statement may be defined. Full list of statements.
# 
# controls clause syntax:
# 
#    controls {
#       inet inet_spec [inet_spec]  ;
#    };
# 
# A `controls` clause is always defaulted and generates a TCP listen 
# on port 953 (the default control port) of the loopback address 
# for either or both of IPv4 and IPv6 (127.0.0.1 and/or ::1). If 
# the remote administration will not be used, that is the `rndc`
# utility will not be used this control interface should be 
# explicitly disabled by defining an empty controls clause as shown 
# below:
# 
#     controls {};
# 
# The primary access control method for remote administration, for 
# example rndc in BIND 9, is via the use of keys defined within 
# the inet statement (see below). To retain compatibility with 
# previous versions of BIND or to run without a user generated key, 
# a default key may be generated using the following command:
# 
#     rndc-confgen -a
# 
# This command will create a file called `rndc.key` containing a 
# default key clause with the name "rndc-key' in same directory as 
# the `named.conf` file for the version of BIND being used and which 
# is used for subsequent access to the control channel. If this 
# command is not executed before BIND is loaded the following 
# message will appear:
# 
#     named [39248] none:0: open: /path/to/default/rndc.key: file not found
# 
# BIND will continue to run in this state but the control channel 
# will not be operable. For full configuration of the inet statement 
# and examples of its use in the controls clause see inet statements below.
# 
#     inet
# 
# The `inet` statement defines a method to control access to the rndc 
# (remote administration) utility. More than one `inet` statement may 
# be included in a controls clause.
# 
#     inet inet_spec [inet_spec] ..;
# 
# Each `inet_spec` parameter has the following format:
# 
#    inet_spec = ( ip_addr | * ) [ port ip_port ] \
#                    allow {  address_match_list  } keys {  key_list  };
# 
# The ip_address parameter defines the IP address of the local 
# server interface on which rndc connections will be accepted. 
# The wildcard value ("*") will allow connection on any of the 
# server's IP addresses including the loopback address. The 
# optional ip_port parameter allows a specific port to be 
# nominated for use by rndc connections. The address_match_list 
# defines the permitted hosts that can connect to the rndc 
# channel. The key_list parameter contains a reference to one or 
# more key clauses containing the list of permitted users who are 
# allowed access. While address_match_lists can include a key 
# parameter if one is present in the referenced 
# address_match_list it is ignored, only keys defined in the 
# key_list of the inet statement are permitted access. The 
# key_list can be omitted in which case the file rndc.key in 
# the same directory as named.conf and which contains a default 
# key clause with the name rndc-key will be used to provide 
# default access. The rndc.key file is created by running 
# the command:
# 
#     rndc-confgen -a
# 
# The following example shows that a user on the loopback address 
# can use the default key for access while all other users must 
# use the rndc-remote key, in all cases localhost will use port 953 
# (the default) and external connection port 7766. An acl clause 
# is used as the source of the address_match_list:
# 
#     # named.conf fragment
#     acl "rndc-users" {
#         10.0.15.0/24;
#         !10.0.16.1/24; # negated
#         2001:db8:0:27::/64; # any address in subnet
#         };
#         ....
#         key "rndc-remote" {
#             algorithm hmac-md5;
#             secret "OmItW1lOyLVUEuvv+Fme+Q==";
#         };
#     controls {
#         # local host - default key
#         inet 127.0.0.1 allow {localhost;};
#         inet * port 7766 allow {"rndc-users";} keys {"rndc-remote";};
#         };
# 
# Note: The keys clause above would normally be placed in a 
# separate secure file and included into the named.conf file.


controls {

    inet 127.0.0.1 port 953 allow { 127.0.0.1; } keys { rndc-key; };

    # example below for remote rndc access via port 7766
    # inet * port 7766 allow {"rndc-user";} keys { "rndc-remote"; };
    # need to add two ACLs: rndc-user and rndc-remote to named.conf.acl

    # An example below for non-Internet-based UNIX-socket access by `rndc` utility
    # most useful for hardened authoritative DNS server as it
    # disables everything remotely administrative to your `named`.
    # This would mean you must log into this host to use `rndc`.  
    # Most practical for non-enterprise SMB types.
    #
    # controls {
    #    unix "/var/run/named/resolver.sock" 
    #    perm 0750 
    #    owner 11 
    #    group 101 
    #    keys { 
    #        rndc-key; 
    #        }; 
    #    }; 

};

# End of named.conf
```


## Bind9 `view` Clause

This filespec is `/etc/bind/view-named.conf` and contains the following:

```nginx
# 
# File: views-named.conf
# Path: /etc/bind
# Title: View Perspective settings for ISC Bind9 named daemon
# 
# The view statement is a powerful feature of BIND 9 that 
# lets a name server answer a DNS query differently depending 
# on who is asking. It is particularly useful for 
# implementing split DNS setups without having to run 
# multiple servers.

# Views are class specific. If no class is given, class IN is 
# assumed. Note that all non-IN views must contain a hint 
# zone, since only the IN class has compiled-in default hints. 

# Zones defined within a view statement will only be 
# accessible to clients that match the view. By defining 
# a zone of the same name in multiple views, different 
# zone data can be given to different clients, for 
# example, "internal" and "external" clients in a split 
# DNS setup. 

# view is class dependent but the default class is IN 
# (or 'in' - not case dependent) and has been omitted.

# Each view statement defines a view of the DNS namespace 
# that will be seen by a subset of clients. A client matches 
# a view if its source IP address matches the 
# address_match_list of the view's match-clients clause and 
# its destination IP address matches the address_match_list of 
# the view's match-destinations clause. If not specified, both 
# match-clients and match-destinations default to matching all 
# addresses. In addition to checking IP addresses 
# match-clients and match-destinations can also take keys 
# which provide an mechanism for the client to select the view. 
# A view can also be specified as match-recursive-only, which 
# means that only recursive requests from matching clients 
# will match that view. The order of the view statements is 
# significant a client request will be resolved in the context 
# of the first view that it matches. 

# Consider adding the 1918 zones here, if they are not being used in your
# organization

# Only include zones inside views

# If there are no view statements in the config file, a default 
# view that matches any client is automatically created in 
# class IN. Any zone statements specified on the top level of 
# the configuration file are considered to be part of this 
# default view, and the options statement will apply to the 
# default view. If any explicit view statements are present, 
# all zone statements must occur inside view statements. 

# view clauses are processed in the order in which they appear 
# in the named.conf file. 
# Pay attention to match-clients between views, because first
# matching rule stops in that view.  Ideally, you put most
# restrictive view (e.g., internal view) firstly and
# public view (e.g., external view) lastly.

# While the two view clauses is used here, any number of view 
# clauses may be present.

# If none of the matching conditions in view clauses matches 
# then BIND will return a server error.

# While it may seem like a statement of the obvious, the zone 
# files defined in each view for the same domain name do not 
# need to be the same, nor do all zones defined in one view 
# require to be present in all views. For example, it is 
# possible to have private zones that are only visible within 
# an Intranet or private network.

# The required zone files may differ in each view, for example, 
# there is no need to provide localhost zones in the "badguys" view.

# The zone files for "example.com" are different allowing 'hiding' 
# of non-public hosts in the "trusted" view.

# Recursion has been removed in the "badguys" view for performance 
# and security reasons.

# 'slave' servers for each zone will see a single 'zone' based on 
# their IP address, for instance, "trusted" or "badguys". 
# However, if you multi-home or 'alias' the IP address on the 
# 'slave' server you could get both views.

# Slave DNS Servers with View Clause When using a Slave server 
# with view clauses it is important to recall that, even when 
# NOTIFY is used, the Slave always initiates the zone tranfer 
# operation using an INCOMING DNS operation (TCP on Port 53 
# normally). To ensure the correct zone file is transferred the 
# match-clients and/or match-destinations statements associated 
# with the views must ensure that the requesting Slave server's 
# IP is directed to the view containing the zone file that 
# should be tranferred.

# Note: Early versions of BIND 9 allowed default zones to be 
# defined outside the scope of view clauses. Current versions 
# of BIND will refuse to load such configurations. If 
# incoming queries are not matched to a particular view then 
# Server Error is typically returned. To avoid such problems 
# the last view defined should use:
# 
#    match-clients {any};
#    # or if you enjoy living dangerously omit the statment 
#    # (see defaults below)

include "/etc/bind/view-local-named.conf";
include "/etc/bind/view-chaos-named.conf";
include "/etc/bind/view-red-named.conf";
```


## Bind9 `statistics` Clause

This filespec is `/etc/bind/statistics-named.conf` and contains the following:

```nginx
# 
# File: statistics-named.conf
# Path: /etc/bind
# Title: Defines access to XML (browser) statistics.

# CISecurity says do not use 'statistics-channel' in production
#
# statistics-channels {
#        inet 127.0.0.1 port 8053;
# };
```

# Views - Chaos

This filespec is `/etc/bind/view-chaos-named.conf` and contains the following:

```nginx
#
# File: view-chaos-named.conf
# Path: /etc/bind
# Title: DNS RR for CHAOS class
#
view "chaos" CH {
    match-clients { any; };
    zone "bind" CH {
        type master;
        file "/etc/bind/zones/db.ch.bind.version";
        allow-update { none; };
        allow-transfer { none; };
        };
    };
```

# Views - Local

This filespec is `/etc/bind/view-local-named.conf` and contains the following:

```nginx
#
# File: view-local-named.conf
# Path: /etc/bind
# Title: this server's localhost and localnets
# 
view "local"
{
    # match-clients
    # A view clause matches when either or both of its match-clients 
    # and match-destinations statements match and when the 
    # match-recursive-only condition is met. If either or both 
    # of match-clients and match-destinations are missing they 
    # default to any (all hosts match). The match-clients 
    # statement defines the address_match_list for the source 
    # IP address of the incoming messages. Any IP which matches 
    # will use the defined view clause. 
    # match-clients statement may only be used in a view clause.
    #
    match-clients { localhost; };

    # A view clause matches when either or both of its match-clients 
    # and match-destinations statements match and when the 
    # match-recursive-only condition is met. If either or both 
    # of match-clients and match-destinations are missing they 
    # default to any (all hosts match). The match-destination 
    # statement defines the address_match_list for the destination 
    # IP address of the incoming messages. Any IP which matches 
    # will use the defined view clause. 
    # match-destination statement may only be used in a view clause.
    #
    match-destinations { localhost; };

    # A view clause matches when either or both of its 
    # match-clients and match-destinations statements match and 
    # when the match-recursive-only condition is met. 
    # If either or both of match-clients and match-destinations 
    # are missing they default to any (all hosts match). 
    # The match-recursive-only can be used in conjunction with 
    # match-clients and match-destinations or on its own if 
    # that is sufficient differentiation. 
    # The default is no. 
    # match-recursive-only statement may only be used in a view clause.
    #
    match-recursive-only yes;

    # allow-query defines an match list of IP address(es) which are 
    # allowed to issue queries to the server. If not specified all 
    # hosts are allowed to make queries (defaults to allow-query {any;};).
    # 
    # allow-query-on defines the server interface(s) from which 
    # queries are accepted and can be useful where a server 
    # is multi-homed, perhaps in conjunction with a view clause. 
    # Defaults to allow-query-on {any;};) meaning that queries 
    # are accepted on any server interface.
    # 
    # allow-query statements may be used in a zone, view or 
    # a global options clause.
    #
    allow-query { localhost; };

    # Many of the options given in the options statement can also 
    # be used within a view statement, and then apply only when 
    # resolving queries with that view. When no view-specific 
    # value is given, the value in the options statement is used 
    # as a default. Also, zone options can have default values 
    # specified in the view statement; these view-specific 
    # defaults take precedence over those in the options 
    # statement. 
    #
    recursion yes;

    # allow-recursion is only relevant if recursion yes; is present 
    # or defaulted.
    # 
    # allow-recursion defines a address_match_list of IP address(es) 
    # which are allowed to issue recursive queries to the server. 
    # When allow-recursion is present allow-query-cache defaults 
    # to the same values. If allow-recursion is NOT present the 
    # allow-query-cache default is assumed (localnets, localhost 
    # only). Meaning that only localhost (the server's host) and 
    # hosts connected to the local LAN (localnets) are permitted 
    # to issue recursive queries.
    # 
    # allow-recursion-on defines the server interface(s) from which 
    # recursive queries are accepted and can be useful where a 
    # server is multi-homed, perhaps in conjunction with a view 
    # clause. Defaults to allow-recursion-on {any;}; meaning that 
    # recursive queries are accepted on any server interface.
    # 
    # NOTE: Always set 'recursion no' at global option and selectively
    # enable 'recursion yes' in certain zones AND either with 
    # 'allow recursion { localnets;localhost;};' on badguy/public view OR
    # 'allow recursion { any;};' on internal/safe view.
    # 
    # These statements may be used in a view or a global options clause.
    #
    allow-recursion { localhost; };

    # allow-query-cache, since BIND 9.4 allow-query-cache (or its
    # default) controls access to the cache and thus effectively
    # determines recursive behavior. This was done to limit the
    # number of, possibly inadvertant, OPEN DNS resolvers.
    # allow-query-cache defines an address_match_list of IP
    # address(es) which are allowed to issue queries that access
    # the local cache - without access to the local cache
    # recursive queries are effectively useless so, in effect,
    # this statement (or its default) controls recursive behavior.
    # Its default setting depends on:
    # 
    #   If recursion no; present, defaults to
    #       allow-query-cache {none;};. No local cache access permitted.
    # 
    #   If recursion yes; (default) then, if allow-recursion present,
    #       defaults to the value of allow-recursion. Local cache
    #       access permitted to the same address_match_list as
    #       allow-recursion.
    # 
    #   If recursion yes; (default) then, if allow-recursion is NOT
    #       present, defaults to
    #       allow-query-cache {localnets; localhost;};.
    #       Locaquery-cache {localnets; localhost;};.
    #       Local cache access permitted to localnets and localhost only.
    # 
    # Both allow-query-cache and allow-recursion statements are allowed
    # - this is a recipe for conflicts and a debuggers dream come true.
    # Use either statement consistently - by preference allow-recursion.
    # 
    # These statements may be used in a view or a global options clause.
    #
    allow-query-cache {
        localhost;
    };

    # allow-update may or may not be obsoleted (it wasn't in Bind 9.10)
    # 'allow-update' on a "locally" view is essential for
    # communication such as:
    #    - between DHCP and BIND9
    #    - between sftdyn and BIND9
    #
    allow-update { none; };

    # empty-zones-enable, by default, is set to yes which means that 
    # reverse queries for IPv4 and IPv6 addresses covered by RFCs 
    # 1918, 4193, 5737 and 6598 (as well as IPv6 local address 
    # (locally assigned), IPv6 link local addresses, the IPv6 
    # loopback address and the IPv6 unknown address) but which 
    # is not not covered by a locally defined zone clause will 
    # automatically return an NXDOMAIN response from the local 
    # name server. This prevents reverse map queries to such 
    # addresses escaping to the DNS hierarchy where they are 
    # simply noise and increase the already high level of query 
    # pollution caused by mis-configuration. The empty-zone feature 
    # may be turned off entirely by specifying 
    # empty-zones-enable no; or selectively by using one or more 
    # disable-empty-zone statements. 
    # empty-zones-enable statement may appear in a global options 
    # clause or a view clause.
    # 
    # Note: An empty zone contains only an SOA and a single NS RR.
    empty-zones-enable no;

    # disable-empty-zone by default is set to yes which means that 
    # reverse queries for IPv4 and IPv6 addresses covered by RFCs 
    # 1918, 4193, 5737 and 6598 (as well as IPv6 local address 
    # (locally assigned), IPv6 link local addresses, the IPv6 
    # loopback address and the IPv6 unknown address) but which is 
    # not covered by a locally defined zone clause will 
    # automatically return an NXDOMAIN response from the local name 
    # server. This prevents reverse map queries to such addresses 
    # escaping to the DNS hierarchy where they are simply noise and 
    # increase the already high level of query pollution caused by 
    # mis-configuration. disable-empty-zone may be used to 
    # selectively turn off empty zone responses for any particular 
    # zone in which case the query will escape to the DNS hierarchy. 
    # To turn off more than one empty-zone, multiple 
    # disable-empty-zone statements must be defined. There is no 
    # need to turn off empty-zones for which the user has defined 
    # a local zone clause since BIND automatically detects this, 
    # similarly if the name server forwards all queries, the 
    # empty-zone process is automatically inhibited. Other than 
    # name servers which delegate to the IN-ADDR.ARPA or IP6.ARPA 
    # domains, it is not clear who would want to use this statement. 
    # Perhaps more imaginative readers can see uses. 
    # disable-empty-zone statement may appear in a global options 
    # clause or a view clause.
    # 
    # Note: An empty zone contains only an SOA and a single NS RR.
    disable-empty-zone yes;

    # Consider adding the 1918 zones here, if they are not used in your
    # organization.
    # WARNING: Badguys should not be using your DNS server to resolve localhost
    #include "/etc/bind/zones.rfc1918";
    #include "/etc/bind/default-zones-named.conf";

};
```

# Views - Public/Red/Hot

This filespec is `/etc/bind/view-public-named.conf` and contains the following:

```nginx
#
# File: view-public-named.conf
# Path: /etc/bind
# Title: The bad guy's view or public IP.
# 
view "public"
{
    # match-clients
    # A view clause matches when either or both of its match-clients 
    # and match-destinations statements match and when the 
    # match-recursive-only condition is met. If either or both 
    # of match-clients and match-destinations are missing they 
    # default to any (all hosts match). The match-clients 
    # statement defines the address_match_list for the source 
    # IP address of the incoming messages. Any IP which matches 
    # will use the defined view clause. 
    # match-clients statement may only be used in a view clause.
    # match-clients { any; };  # default
    # match-destinations { any; };  # default
    match-recursive-only no;

    allow-recursion-on { none; };

    # allow-query defines an match list of IP address(es) which are 
    # allowed to issue queries to the server. If not specified all 
    # hosts are allowed to make queries (defaults to allow-query {any;};).
    # 
    # allow-query-on defines the server interface(s) from which 
    # queries are accepted and can be useful where a server 
    # is multi-homed, perhaps in conjunction with a view clause. 
    # Defaults to allow-query-on {any;};) meaning that queries 
    # are accepted on any server interface.
    # 
    # allow-query statements may be used in a zone, view or 
    # a global options clause.
    # 
    allow-query {
        # This is an authoritative name server so allow 'any;' here.
        # do not insert 'any;' here unless all forms of recursion is disabled
        any;
    };

    # Many of the options given in the options statement can also 
    # be used within a view statement, and then apply only when 
    # resolving queries with that view. When no view-specific 
    # value is given, the value in the options statement is used 
    # as a default. Also, zone options can have default values 
    # specified in the view statement; these view-specific 
    # defaults take precedence over those in the options 
    # statement. 
    # 
    recursion no;

    # `allow-recursion` is only relevant if `recursion` 
    # is set to `yes`, is present, or defaulted as `yes` 
    # by omission of `allow-recursion`.

    allow-recursion { none; };
    allow-query-cache { none; };

    # allow-update may or may not be obsoleted (it wasn't in Bind 9.10)
    # 'allow-update' on a "locally" view is essential for
    # communication such as:
    #    - between DHCP and BIND9
    #    - between sftdyn and BIND9
    #    - with a master DNS server (hidden or not)
    allow-update { 
        acl_public_master_nameserver;  # this host being a secondary/slave server
        acl_dhcp_server_for_ddns_support;  # to be used by their DHCP server
        acl_hidden_master_nameserver;  # this host being an public-master
        acl_bastion_internal_nameserver;  # this host being a external-bastion
        none;
    };


    # forwarders
    # Example syntax:
    #     forwarders { ip_addr [port ip_port] ; 
    #                [ ip_addr [port ip_port] ; ... ] };
    #     forwarders { 10.2.3.4; 192.168.2.5; };
    # forwarders defines a list of IP address(es) (and optional port 
    # numbers) to which queries will be forwarded. Only relevant when 
    # used with the related forward statement. 
    # This statement may be used in a zone, view or a global options clause.
    # WARNING: badguy never needs recursion support, neither does the public
    forwarders { none; };

    # empty-zones-enable, by default, is set to yes which means that 
    # reverse queries for IPv4 and IPv6 addresses covered by RFCs 
    # 1918, 4193, 5737 and 6598 (as well as IPv6 local address 
    # (locally assigned), IPv6 link local addresses, the IPv6 
    # loopback address and the IPv6 unknown address) but which 
    # is not not covered by a locally defined zone clause will 
    # automatically return an NXDOMAIN response from the local 
    # name server. This prevents reverse map queries to such 
    # addresses escaping to the DNS hierarchy where they are 
    # simply noise and increase the already high level of query 
    # pollution caused by mis-configuration. The empty-zone feature 
    # may be turned off entirely by specifying 
    # empty-zones-enable no; or selectively by using one or more 
    # disable-empty-zone statements. 
    # empty-zones-enable statement may appear in a global options 
    # clause or a view clause.
    # 
    # Note: An empty zone contains only an SOA and a single NS RR.
    # 
    # Authoritative name server does not serve 'empty-zones'.
    # 
    empty-zones-enable no;

    # disable-empty-zone by default is set to yes which means that 
    # reverse queries for IPv4 and IPv6 addresses covered by RFCs 
    # 1918, 4193, 5737 and 6598 (as well as IPv6 local address 
    # (locally assigned), IPv6 link local addresses, the IPv6 
    # loopback address and the IPv6 unknown address) but which is 
    # not covered by a locally defined zone clause will 
    # automatically return an NXDOMAIN response from the local name 
    # server. This prevents reverse map queries to such addresses 
    # escaping to the DNS hierarchy where they are simply noise and 
    # increase the already high level of query pollution caused by 
    # mis-configuration. disable-empty-zone may be used to 
    # selectively turn off empty zone responses for any particular 
    # zone in which case the query will escape to the DNS hierarchy. 
    # To turn off more than one empty-zone, multiple 
    # disable-empty-zone statements must be defined. There is no 
    # need to turn off empty-zones for which the user has defined 
    # a local zone clause since BIND automatically detects this, 
    # similarly if the name server forwards all queries, the 
    # empty-zone process is automatically inhibited. Other than 
    # name servers which delegate to the IN-ADDR.ARPA or IP6.ARPA 
    # domains, it is not clear who would want to use this statement. 
    # Perhaps more imaginative readers can see uses. 
    # disable-empty-zone statement may appear in a global options 
    # clause or a view clause.
    # 
    # Note: An empty zone contains only an SOA and a single NS RR.
    #
    disable-empty-zone yes;

    # Consider adding the 1918 zones here, if they are not used in your
    # organization.
    # WARNING: Badguys should not use your DNS server to resolve localhost
    # include "/etc/bind/zones.rfc1918";
    # include "/etc/bind/named.conf.default-zones";


include "/etc/bind/mz-example.test-named.conf";

    # Ask someone else to map reverse IP to ns1.example.test
    };
```


# Zone Settings

This filespec is `/etc/bind/mz-example.test-named.conf` and contains the following:

When dealing with tens of thousands of zones, the filename notation is derived from `.se` TLD.

`pz.` - Primary Zone
`sz.` - Secondary Zone
`mirror.` - Mirror Zone
`stub.` - Secondary Zone
`mz.` - Master Zone

And is still suffixed with `-named.conf` (as there are many text editor tools out there who still do syntax-highlighting based on filename `*named.conf`.)


```nginx
# File: mz-example.test-named.conf
# Path: /etc/bind
# Title: MASTER zone example.test
# Description:
#   zone example.test is the world-view of example.test network topology

zone "example.test" IN 
{
    # type master is the server reads the zone data direct from 
    # local storage (a zone file) and provides authoritative 
    # answers for the zone.
    #
    type master;

    allow-query { any; };

    # file statement defines the file used by the zone in 
    # quoted string format, for instance, "slave/example.com" - 
    # or whatever convention you use. The file entry is 
    # mandatory for master and hint and 
    # optional - but highly recommended - for slave and 
    # not required for forward zones. 
    # The file may be an absolute path or relative to directory.
    #
    # Note: If a type Slave has a file statement then any zone 
    # transfer will cause it to update this file. If the slave 
    # is reloaded then it will read this file and immediately 
    # start answering queries for the domain. If no file is 
    # specified it will immediately try to contact the Master 
    # and initiate a zone transfer. For obvious reasosn the 
    # Slave cannot to zone queries until this zone transfer 
    # is complete. If the Master is not available or the Slave 
    # fails to contact the Master, for whatever reason, the 
    # zone may be left with no effective Authoritative Name Servers.

    file "/var/lib/bind/master/db.example.test";

    key-directory "/var/lib/bind/keys/example.test";

    # allow-update defines an address_match_list of hosts that 
    # are allowed to submit dynamic updates for master zones, 
    # and thus this statement enables Dynamic DNS. The default 
    # in BIND 9 is to disallow updates from all hosts, that is, 
    # DDNS is disabled by default. This statement is mutually 
    # exclusive with update-policy and applies to master zones 
    # only. The example shows DDNS for three zones: the first 
    # disables DDNS explicitly, the second uses an IP-based 
    # list, and the third references a key clause. The 
    # allow-update in the first zone clause could have been 
    # omitted since it is the default behavior. 
    # Many people like to be cautious in case the default mode changes.
    #     allow-update {none;}; # no DDNS by default
    #     allow-update {10.0.1.2;}; # DDNS this host only
    #     allow-update {key "update-key";};
    # In the example.org zone, the reference to the key clause 
    # "update-key" implies that the application that performs 
    # the update, say nsupdate, is using TSIG and must also 
    # have the same shared secret with the same key-name. 
    # allow-update statement may be used in a zone, view or an 
    # options clause.
    # allow-update { 172.28.130.1; };
    # allow-update may or may not be obsoleted (it wasn't in Bind 9.10)
    # 'allow-update' on a "locally" view is essential for
    # communication such as:
    #    - between DHCP and BIND9
    # allow-update { 
    #     # no one can update except localhost RNDC
    #     !{ !localhost; any; };
    #     # only localhost got past this point here
    #     key "rndc-key"; # only RNDC on localhost 
    # };

    # At the momemt, no one can update this master server.
    # Can only edit the /var/lib/bind/db.example.test file
    # and restart daemon to affect any changes here.


    journal "/var/cache/bind/example.test-master.jnl";

    # allow-transfer defines a match list e.g. IP address(es) 
    # that are allowed to transfer (copy) the zone information 
    # from the server (master or slave for the zone). 
    # The default behaviour is to allow zone transfers to any host. 
    # While on its face this may seem an excessively friendly 
    # default, DNS data is essentially public (that's why its 
    # there) and the bad guys can get all of it anyway. 
    # However if the thought of anyone being able to transfer 
    # your precious zone file is repugnant, or (and this is 
    # far more significant) you are concerned about possible 
    # DoS attack initiated by AXFR requests, then use the 
    # following policy.
    #
    # In short, an ACL for allowing other nameservers to extract
    # resource records from this server, usually downstream or
    # slave nameservers (or ... gasp ... applications).
    allow-transfer { 

        !{
            !{
                acl_grant_axfr_to_trusted_3rd_party_downstream_secondaries;
                localhost;
                };
            any;
            };

        #  Only trusted_downstream_nameservers and localhost get past here
        key public-master-to-public-secondary;

        !{ !{ localhost; }; any; };
        # Only localhost get past this point here

        key rndc-key;  # only `rndc` can use localhost via rndc-key key

        none;
        };

    # notify behaviour is applicable to both master zones 
    # (with 'type master;') and slave zones (with 'type slave;') 
    # and if set to 'yes' (the default) then, when a zone is 
    # loaded or changed, for example, after a zone transfer, 
    # NOTIFY messages are sent to the name servers defined in 
    # the NS records for the zone (except itself and the 
    # 'Primary Master' name server defined in the SOA record) 
    # and to any IPs listed in any also-notify statement.
    # 
    # * If set to 'no' NOTIFY messages are not sent.
    # * If set to 'explicit' NOTIFY is only sent to those IP(s) 
    #   listed in an also-notify statement.
    # If a global notify statement is 'no' an also-notify 
    # statement may be used to override it for a specific zone, 
    # and conversely if the global options contain an 
    # also-notify list, setting notify 'no' in the zone will 
    # override the global option. 
    #
    # This statement may be specified in zone, view clauses or 
    # in a global options clause.  Global notify is none.
    #
    # In short, push any changes that this server here made to
    # its zone databases toward other nameservers (most commonly
    # slave or downstream ones, rarely toward hidden-masters)
    notify explicit;

    # also-notify { <ip-list|masters-list>; };
    #
    # who to notify when zones get updated
    # send NOTIFY messages to secondary DNS provider when the zone changes
    also-notify port 345 { 
        # cannot use ACL here, only 'masters_list_*' in masters {} list
        # We do not need `masters` here.
        216.218.130.2;  # ns1.he.net
        };

    #  auto-dnssec < allow | maintain >
    #
    # if auto-dnssec is not defined, you must rollover your keys
    # as they expired... manually.
    # if auto-dnssec is maintain option, named does rollover for you.
    # if auto-dnssec is allow option, you must used "rndc sign"
    #
    # To enable automatic signing, add the auto-dnssec 
    # option to the zone statement in named.conf. 
    # auto-dnssec has two possible arguments: allow or maintain.
    #
    # With auto-dnssec allow, named can search the key 
    # directory for keys matching the zone, insert them 
    # into the zone, and use them to sign the zone. 
    # It will do so only when it receives an rndc sign <zonename>.
    # 
    # auto-dnssec maintain includes the above functionality, 
    # but will also automatically adjust the zone's DNSKEY 
    # records on schedule according to the keys' timing 
    # metadata. (See dnssec-keygen(8) and dnssec-settime(8) 
    # for more information.)
    # 

    # 
    # If keys are present in the key directory the first 
    # time the zone is loaded, the zone will be signed 
    # immediately, without waiting for an rndc sign or 
    # rndc loadkeys command. (Those commands can still be 
    # used when there are unscheduled key changes, however.)
    # 
    # When new keys are added to a zone, the TTL is set to 
    # match that of any existing DNSKEY RRset. If there is 
    # no existing DNSKEY RRset, then the TTL will be set to 
    # the TTL specified when the key was created (using the 
    # dnssec-keygen -L option), if any, or to the SOA TTL.
    # 
    # If you wish the zone to be signed using NSEC3 instead 
    # of NSEC, submit an NSEC3PARAM record via dynamic 
    # update prior to the scheduled publication and 
    # activation of the keys. If you wish the NSEC3 chain to 
    # have the OPTOUT bit set, set it in the flags field of 
    # the NSEC3PARAM record. The NSEC3PARAM record will not 
    # appear in the zone immediately, but it will be stored 
    # for later reference. When the zone is signed and the 
    # NSEC3 chain is completed, the NSEC3PARAM record will 
    # appear in the zone.
    # 
    # Using the auto-dnssec option requires the zone to be 
    # configured to allow dynamic updates, by adding an 
    # allow-update or update-policy statement to the zone 
    # configuration. If this has not been done, the 
    # configuration will fail.
    #
    # "rndc loadkeys" requires "auto-dnssec maintain"
    #
    # https:#kb.isc.org/docs/aa-00626#
    #
    auto-dnssec maintain;

    # DO NOT use inline DNSSEC signing on master, only on slave(s)
    # Taking another stab at inline signing on master. TODO
    #
    inline-signing yes;
};
```


# `db.ch.bind.version` Zone file

I like faking things so make this authoritative name server not what it seems to be.

```nginx
;
; File: mz-chaos-named.conf
; Path: /etc/bind
; Title: CHAOS class

$TTL 3600
@    86400    CH    SOA    localhost. root.localhost. ( 
                2013050803 ; serial 
                3600       ; refresh 
                3600       ; retry 
                1209600    ; expire (2 week, RFC1912)
                86400 )    ; minimum 
;  
@        CH    NS    localhost.

version        CH    TXT    "Microsoft DNS 6.0.6100 (2AEF76E)" 
authors        CH    TXT    "Microsoft" 
```

# Key for RNDC Utility

Now for the `rndc` utility, create the keys for the administrative control channel
so that only `rndc` can control the ISC Bind9 `named` daemon.

Execute:

```
cd /var/lib/bind
rndc-confkey -A hmac-sha512 -b 512 arca.example.test
```
The output is in three parts/sections:

* Cut-n-paste the `rndc.conf` portion into `/etc/bind/rndc.conf`.
* Cut-n-paste the `key` clause portion into `/etc/bind/key-named.conf`.
* Cut-n-paste the `controls` clause portion into `/etc/bind/controls-named.conf`.


# Key for AXFR/IXFR Zone Data Transfers

Create the keys that will be used to authenticate the AFXR/IFXR zone data transfer from this master to your secondary name servers.

```bash
dnssec-keygen -a HMAC-SHA512 -b 512 -n USER arca.egbert.net.
```

# Files And Directories

```bash
#!/bin/bash
MYFQDN="example.test"
mkdir /etc/bind
mkdir /var/lib/bind/keys
mkdir /var/lib/bind/keys/$MYFQDN
mkdir /var/lib/bind/primary
mkdir /var/lib/bind/secondary
mkdir /var/lib/bind/dynamic
mkdir /var/log/named

chmod 0755 /etc/bind
chmod 0750 /var/lib/bind/keys
chmod 0750 /var/lib/bind/keys/$MYFQDN
chmod 0755 /var/lib/bind/primary
chmod 0755 /var/lib/bind/secondary
chmod 0755 /var/lib/bind/dynamic
chmod 0750 /var/log/named

DNS_USER="bind"  # I've seen 'named' in older Linux distros, 'bind9' in others
DNS_GROUP="bind"

cd /etc/bind
# rndc utility can only be run from root account
# The rndc-key needs file protection in this rndc.conf file.
chmod 0640 rndc.conf
chown root:${DNS_GROUP} rndc.conf

chmod 0640 named.conf
chown root:${DNS_GROUP} named.conf

chmod 0640 acl-named.conf
chown root:${DNS_GROUP} acl-named.conf

chmod 0640 controls-named.conf
chown root:${DNS_GROUP} controls-named.conf

chmod 0640 keys-named.conf
chown root:${DNS_GROUP} keys-named.conf

chmod 0640 local-named.conf
chown root:${DNS_GROUP} local-named.conf

chmod 0640 logging-named.conf
chown root:${DNS_GROUP} logging-named.conf

chmod 0640 masters-named.conf
chown root:${DNS_GROUP} masters-named.conf

chmod 0640 options-named.conf
chown root:${DNS_GROUP} options-named.conf

chmod 0640 servers-named.conf
chown root:${DNS_GROUP} servers-named.conf

chmod 0640 statistics-named.conf
chown root:${DNS_GROUP} statistics-named.conf

chmod 0640 mz.${MYFQDN}-named.conf
chown root:${DNS_GROUP} mz.${MYFQDN}-named.conf


```
