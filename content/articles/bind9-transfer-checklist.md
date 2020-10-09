title: Bind9 XFER Checklist
date: 2020-06-07 09:46
status: published
tags: bind9, axfr, ixfr, checklist
category: HOWTO
summary: Troubleshooting Bind9 AXFR and IXFR

My hidden master nameserver was diligently updating the publicly exposed
master nameserver for sometime.

But no new DNS record information were being pushed out by the hidden master
to any of my public master nameserver.

Yet, there is no discernable error in my hidden master log files.

Initial Confirmation of Failure
===============================

To quickly prove that an update failure is occuring (other than
no fresh DNS records), I checked the serial number in both the hidden
and the public nameserver.

```bash
named-checkzone -j egbert.net /var/lib/bind/public/master/db.egbert.net 
```
and got back
```console
zone egbert.net/IN: loaded serial 2020060601
OK
```

Then over at the public name server,
```bash
named-checkzone -j egbert.net /var/lib/bind/public/master/db.egbert.net 
```
and got this result:
```console
zone egbert.net/IN: loaded serial 2020051350
OK
```

The serial numbers `2020060601` and `2020051350` do not match.

And according to the datestamp method used within the DNS serial number,
it has been some 24 days elapsed since the failure began.  (Make note to
add another monitoring point of failure here).

At this point, we have a failure of DNS transfer.  It may be an AXFR or IXFR,
but there is definitely a DNS record transfer failure.

Initial Log Check - Hidden Master
=================================
In this article, master is my hidden master nameserver.  
Slave is my public master nameserver.

There are two ways to do transfers of new DNS records from master to slave.

1.  Slave to perform transfer at an interval 
2.  Master get QUERY-SOA notified to do a forced transfer

Since we haven't done any forced transfer, we will look for errors during
the interval update.

You may have a general purpose log file for your named daemon, but I have
split my log files out into individual logging channels and thusly
into multiple log files.  ISC Bind v9.16 (at this writing) has 
20 `category` in which to split logs with. 

I wouldn't recommend starting to be splitting out log files unless 
you have a firm grasp of each leg of this DNS protocol down pat.  
Don't do that 
log splitting all at once, do one or two splitting of log files based on
what you know about DNS protocol firstly.  Because splitting out
ALL category logs will make your troubleshooting very difficult without
these understanding of DNS protocols.

The category name to look for is `xfer-out`.  I mapped `xfer-out` to my
own channel name (because your channel name would most likely will be
in a different name).

File: `/etc/bind/public/logging-named.conf`:
```nginx
logging {
   # ...
    category xfer-out { xfer-out_channel; };
   # ...
};
```

My channel name (e.g., `xfer-in_channel`) contains 
a `file` configuration in which to receives all logs related to 
outbound (`xfer-out`) transfers.

```nginx
logging {
    # ...
    channel xfer-out_channel {
        # ...
        file "/var/log/named/public/xfer-out.log" versions 3 size 5m;
        severity debug 6;
        print-time yes;
        print-severity true;
        print-category true;
        # ...
    };
    # ...
```

In above settings, my log files are in text-format UNIX log with 
configured UNIX datetimestamp, severity and category name to be
written out to a maximum of 5 megabytes before creating and
rotating the log file names up to 3 versions.  I've also
configured it for `debug 6` which is rather chatty.

Examination of my outbound transfer log file shows no error message
on this master.

Note:  Expanding to `debug 8` only reveals that it was building a DNS 
message from reading the master's zone file, and at a
time interval that implies that such regular interval were being used.

Hence begins the troubleshooting article here.

Notify
======
Perhaps the notification was failing, the regular interval notification.

I rechecked my `allow-transfer` in my `named.conf` (actually, it's 
`/etc/bind/public/mz.egbert.net`, after the Swede model of Bind9 file layout).

I like my config files heavily commented and annotated from other
people's experiences.
```nginx
zone "egbert.net" IN 
{
# ...
    //// allow-transfer defines a match list e.g. IP address(es) 
    //// that are allowed to transfer (copy) the zone information 
    //// from the server (master or slave for the zone). 
    //// The default behavior is to allow zone transfers to any host. 
    //// While on its face this may seem an excessively friendly 
    //// default, DNS data is essentially public (that's why its 
    //// there) and the bad guys can get all of it anyway. 
    //// However if the thought of anyone being able to transfer 
    //// your precious zone file is repugnant, or (and this is 
    //// far more significant) you are concerned about possible 
    //// DoS attack initiated by AXFR requests, then use the 
    //// following policy.
    ////
    //// In short, an ACL for allowing other nameservers to extract
    //// resource records from this server, usually downstream or
    //// slave nameservers (or ... gasp ... applications).
    allow-transfer {
        // Why? trusted_residential_network_acl; // allow XFER from homenet

        // we blindly allow secondary nameservers to receive AXFR from us
        //  TODO: Need a better system than blindly follow sec_ns

        //  TBD: Thankfully, this isn't the modification route
        //  NOTE: Leakage is limited to red view/zone
        // only allow zone transfers from those who have a special key,
        //  or our secondary DNS provider.

        //  Only trusted_downstream_nameservers and localhost get past
        !{ !{trusted_downstream_nameservers_acl; localhost; }; any; };
        key ddns-sha256-arca-a-key; // TODO tighten this down
        key Xy4jLa01;               // used by ns1.egbert.net only

        // Only localhost get past this point
        !{ !localhost; any; };
        key master-to-slave-key; // only localhost can use key
        localhost; // not so useful for unsecured RNDC uses
        };
        # ...
    };
    # ...
};

```

In short, the uncommented portion of `allow-transfer` looks like
```nginx
zone "egbert.net" IN
{
    # ...
    allow-transfer {
        !{ !{trusted_downstream_nameservers_acl; localhost; }; any; };
        key ddns-sha256-arca-a-key;
        key Xy4jLa01;
        !{ !localhost; any; };
        key master-to-slave-key;
        localhost;
    # ...
};
```

Looks like a rat-nest of permission that is in need of re-verification, no?

And it looks like I may have not gotten the mastery of 
this NOT-AND-BUT-NO-OR logic yet.  It's time to revert to my
electronic engineering of piecemealing partial logic together again.

Do It Loosely
=============

We need to get those transfers going again, so it is time to toss 
that shackle of restriction.

```nginx
zone "egbert.net" IN
{
    # ...
    allow-transfer {
        # trusted_downstream_nameservers_acl; 
        # localhost;
        any;
};
```
Now anyone can do transfer.

But I'm still getting the same message which is no error at Bind9 level.

Time to go network analyzing.

Network Analyzing AXFR
======================

I started two sets of tcpdump session, one at the master and one at the slave.

```bash
tcpdump -s 0 -i eth0 -w /tmp/axfr.pcap port 53 or port 567
```
567 is the unique port number used by hidden master inside my home network
to communicate with the slave out there.  A non-53 port is used
to ensure that ISP router does not intercept my port 53 traffic
(and they usually do ... and nefariously so).

Let the tcpdump ran for a bit (or 8 hours, while I slept).

Rise and shine, copied the PCAP file back to be Wireshark'd.

While reviewing the slave-side Wireshark pcap file, I noticed that the 
slave Bind9 is correctly sending
DNS-QUERY-SOA UDP packets, each with TSIG type upstream toward the master
(home gateway router):
```wireshark
Domain Name System (query)
    Transaction ID: 0x3283
    Flags: 0x0000 Standard query
        0... .... .... .... = Response: Message is a query
        .000 0... .... .... = Opcode: Standard query (0)
        .... ..0. .... .... = Truncated: Message is not truncated
        .... ...0 .... .... = Recursion desired: Don't do query recursively
        .... .... .0.. .... = Z: reserved (0)
        .... .... ...0 .... = Non-authenticated data: Unacceptable
    Questions: 1
    Answer RRs: 0
    Authority RRs: 0
    Additional RRs: 1
    Queries
        egbert.net: type SOA, class IN
    Additional records
        xy4jla01: type TSIG, class ANY
            Name: xy4jla01
            Type: TSIG (Transaction Signature) (250)
            Class: ANY (0x00ff)
            Time to live: 0
            Data length: 93
            Algorithm Name: hmac-sha512
            Time Signed: Jun  9, 2020 04:58:46.000000000 EDT
            Fudge: XXX
            MAC Size: XX
            MAC
                [Expert Info (Warning/Undecoded): No dissector for algorithm:hmac-sha512]
                    [No dissector for algorithm:hmac-sha512]
                    [Severity level: Warning]
                    [Group: Undecoded]
            Original Id: 12931
            Error: No error (0)
            Other Len: 0
```
and the DNS-QUERY packet looks good coming from the slave side.

But none of the corresponding UDP reply emitted from the (hidden) master.

Also, I see that TCP 3-way connection was being attempted by this same slave
but immediately TCP-RESET'd by (hidden) master.

So, it's either the hidden master's access control list or its network reject, 
of some kind.

Other Side of PCAP
------------------
Wireshark'd the (hidden) master's PCAP.   I see nearly the same characteristics
of DNS packet exchanges as described earlier: that DNS-QUERY UDP are 
being seen, and no TCP 3-way.   Whew.  It's not my ISP's firewall.

Perusal of Master
-----------------
Back to the (hidden) master server, trying to find any semblance of activities
associated with this leg of the DNS protocol exchange.

It's important to note that on the master side, tcpdump noticed these
receiving of DNS-QUERY-SOA packet on its own OS-network side, but 
its `named` daemon does not "appear" to be receiving it.

Also that this leg of the DNS protocol would be logged firstly in 
the `query` category of Bind9 logging channels, on (hidden) master side.
But nothing occurred within 5 minutes around that timestamp.

Nuts, it's my master's own DEFAULT-DENY firewall.  And it is related
to my having newly added this custom port number 567.  Don't you hate that?


References
==========
* [Initial AXFR/IXFR checklist](http://www.microhowto.info/howto/configure_bind_as_a_slave_dns_server.html)
