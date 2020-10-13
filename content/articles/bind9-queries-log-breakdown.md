title: ISC Bind9 Queries Log Breakdown
date: 2020-10-09 14:00
status: published
tags: bind9, dns
category: HOWTO
summary: How to interpret ISC Bind9 queries.log files 

This article details how the ISC Bind9 queries log file is formatted.

PRIOR
=====
If you are attempting to find the queries log for your Bind9 DNS servers,
you can start with the `category queries` in your `/etc/bind/named.conf`.
This might be in another file if `named.conf` uses `include` statement(s).
You probably can find it inside the `logging` statement.

After finding this `category queries` amongst the `named.conf` files:
```nginx
...
    category queries { queries_file; };
...
```
Take the identifier (that denotes the channel name) inside the curly braces 
and search for it again amongst the `named.conf`, et. al.
In my example, `queries_file` is the channel name.

```nginx
    channel queries_file {
        file "/var/log/named/queries.log" versions 3 size 5m;
        severity dynamic;
        print-time yes;
        print-severity true;
        print-category true;
    };
```
And the location of the query files is in `/var/log/named/queries.log`.

FORMAT-TIME
===========

My real world (but sanitized) examples are given below:

```log
10-Oct-2020 14:34:41.118 queries: info: client @0x7f599c018c70 1.111.11.111#45672 (EGbert.NEt): view red: query: EGbert.NEt IN DNSKEY -E(0)DC (104.218.48.116)
10-Oct-2020 14:52:37.222 queries: info: client @0x7f599c018c70 111.111.111.111#60654 (egbert.net): view red: query: egbert.net IN SOA -E(0)D (104.218.48.116)
10-Oct-2020 14:53:13.725 queries: info: client @0x7f599c018c70 111.111.111.1#13749/key public-master-to-public-secondary (egbert.net): view red: query: egbert.net IN SOA -SE(0)D (104.218.48.116)
```

Fields explained based on the example above :

[jtable]
Field Value, Type, Description 
`10-Oct-2020`, date, the date that the log was made on (dd-Mmm-yyyy)
`14:34:41.118`, time, the time that the log was made on (hh:mm:ss.ms) in this server's timezone.
`queries:`, category, logging category name
`info:`, severity, the degree of error severity
`client @0x7f599c018c70`, worker ID, the context number of a subworker subprocess of `named` that is processing this DNS query
`1.111.11.111`, src-ip, IP address of the source
`4567:`, port, port number of the transport protocol over IP (see field code for transport type)
`(egbert.net):`, query, the query question of DNS name
`view red:`, view, name of the view clause in which is processing this query (red).  This field only occurs if `view` clause is used in Bind9
`query: egbert.net`, query, same as query
`IN:`, class, DNS Class name (Internet) that query is asking for
`SOA:`, type, DNS Type name (SOA = Start Of Authority) that query is asking for.
`-SE(0)DC`, flags, compressed form of indicators (see Query Flags table below)
`(104.218.48.116)`, dst-ip, the IP address of the server in which this DNS packet was received through.
[/jtable]

The query flag field `[+-]SETDC` code break down is:

[jtable caption="Query Flags"]
flag, name, description
'`+`' or '`-`', RD, , whether recursion desired (RD) is wanted by client or not; '+' want recursion; '-' otherwise [RFC1035](http://www.rfc-archive.org/getrfc.php?rfc=1035)
'`S`', signature, whether a transaction signature (TSIG) is given or not
'`E`', EDNS, whether an extension mechanism for DNS is used or not; useful for stating that client can large UDP packets
'`(0)`', version, the version of EDNS used and requested.  [RFC6891](http://www.rfc-archive.org/getrfc.php?rfc=6891)
'`T`', transport, the type of IP transport used during this query; T for TCP or nothing for otherwise (UDP).
'D', [DO](http://www.rfc-archive.org/getrfc.php?rfc=6891), DNSSEC answer must be OK [RFC 4035](http://www.rfc-archive.org/getrfc.php?rfc=4035) [RFC 3225](http://www.rfc-archive.org/getrfc.php?rfc=3225) [RFC 6840](http://www.rfc-archive.org/getrfc.php?rfc=6840) [RFC Errata 4928](http://www.rfc-archive.org/getrfc.php?rfc=4928)
'C', no-check, Checking Disable (CD) bit 11 means no checking of DNSSEC is wanted by the client.
[/jtable]	


