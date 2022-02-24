Title: ISC Bind9 Logging
Date: 2018-10-17 10:41
Modified: 2022-02-24 08:24
Tags: logging, bind9
status: published
Category: research
summary: Logging Files Used By ISC Bind9

Editing Bind9 logging Bind9 logging is controlled and ferrated into several channels.

Functional Log
--------------
Bind9 log channel categories.
[jtable]
category name, source files
`NS_LOGCATEGORY_CLIENT`, `client.c`
`DNS_LOGCATEGORY_DATABASE`, `lwdclient.c`
`NS_LOGCATEGORY_GENERAL`, "`lwdclient.c`, `lwresd.c`, `main.c`, `server.c`, `statschannel.c`, `tkeyconf.c`"
`NS_LOGCATEGORY_NETWORK`, `interfacemgr.c`
`NS_LOGCATEGORY_NOTIFY`, `notify.c`
`DNS_LOGCATEGORY_DNSSEC`, `query.c`
`NS_LOGCATEGORY_QUERIES`, `query.c`
`NS_LOGCATEGORY_QUERY_EERRORS`, "`client.c`, `query.c`"
`NS_LOGCATEGORY_RPZ`, `query.c`
`DNS_LOGCATEGORY_RRL`, `query.c`
`DNS_LOGCATEGORY_SECURITY`, `query.c`
`NS_LOGCATEGORY_UNMATCHED`, `client.c`
`NS_LOGCATEGORY_UPDATE`, `update.c`
`NS_LOGCATEGORY_UPDATESECURITY`, `update.c`
`DNS_LOGCATEGORY_XFER_OUT`, `xferout.c`
[/jtable]


Log modules
-----------
Bind9 log channel modules

[jtable]
module name, source files
`NS_LOGMODULE_ADB`, `lwdclient.c`
`NS_LOGMODULE_CLIENT`, `client.c`
`NS_LOGMODULE_INTERFACEMGR`, `interfacemgr.c`
`NS_LOGMODULE_MAIN`, `main.c`
`NS_LOGMODULE_NOTIFY`, `notify.c`
`NS_LOGMODULE_QUERY`, `query.c`
`NS_LOGMODULE_SERVER`, `main.c`
`NS_LOGMODULE_UPDATE`, `update.c`
`NS_LOGMODULE_XFER_OUT`, `xferout.c`
[/jtable]

Ideal Configuration
--------------------
Ideal logging configuration for ISC Bind9 is:
```nginx
logging {
    channel named_file {
        file "/var/log/bind/named.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel database_file {
        file "/var/log/bind/database.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel security_file {
        file "/var/log/bind/security.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel resolver_file {
        file "/var/log/bind/resolver.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel transfer_file {
        file "/var/log/bind/transfer.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel client_file {
        file "/var/log/bind/client.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel unmatched_file {
        file "/var/log/bind/unmatched.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel queries_file {
        file "/var/log/bind/queries.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel query-errors_file {
        file "/var/log/bind/query-errors.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel network_file {
        file "/var/log/bind/network.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel update_file {
        file "/var/log/bind/update.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel update-security_file {
        file "/var/log/bind/update-security.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel dispatch_file {
        file "/var/log/bind/dispatch.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel dnssec_file {
        file "/var/log/bind/dnssec.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel lame-servers_file {
        file "/var/log/bind/lame-servers.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel delegation-only_file {
        file "/var/log/bind/delegation-only.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
    channel rate-limit_file {
        file "/var/log/bind/rate-limit.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };

    category default { default_syslog; named_file; };
    category general { default_syslog; named_file; };
    category database { database_file; };
    category security { security_file; };
    category queries { queries_file; };
    category config { named_file; };

    category xfer-in { transfer_file; };
    category xfer-out { transfer_file; };
    category notify { transfer_file; };

    category resolver { resolver_file; };
    category client { client_file; };
    category unmatched { unmatched_file; };
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
