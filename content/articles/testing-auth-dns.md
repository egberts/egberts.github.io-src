title: Testing Authoritative DNS Server
date: 2020-06-14 11:00
status: published
tags: DNS
category: HOWTO
summary: How to test your authoritative DNS server

After your authoritative DNS server is set up and running, 
there are a couple of online tester to check things out
and ensure that it is correct.

Do It Yourself EDNS Test
========================

Some of the commands to try for EDNS checkout are:
```bash
SERVER="ns1.example.local"
ZONE="example.local"
    dig +norec +noedns soa ${ZONE} @${SERVER}
    dig +norec +edns=0 soa ${ZONE} @${SERVER}
    dig +norec +edns=100 +noednsneg soa ${ZONE} @${SERVER}
    dig +norec +ednsopt=100 soa ${ZONE} @${SERVER}
    dig +norec +ednsflags=0x80 soa ${ZONE} @${SERVER}
    dig +norec +dnssec soa ${ZONE} @${SERVER}
    dig +norec +dnssec +bufsize=512 +ignore dnskey ${ZONE} @${SERVER}
    dig +norec +edns=100 +noednsneg +ednsopt=100 soa ${ZONE} @${SERVER}
```
Check all outputs  for the line that begins with "`; EDNS:`" and
monitor the byte size after "`udp: `".
```console
;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;example.invalid.
```

Detailed test explanations are:

Plain DNS
---------
```bash
dig +norec +noedns soa zone @server
```
expect: SOA record in the ANSWER section of the query response
expect: status is NOERROR

Plain EDNS
----------
```bash
dig +norec +edns=0 soa zone @server
```
expect: SOA record in the ANSWER section of the query response
expect: status is NOERROR
expect: OPT record with EDNS version set to 0
See RFC6891

EDNS - Unknown Version
----------------------
```bash
dig +norec +edns=100 +noednsneg soa zone @server
```
expect: status is `BADVERS`
expect: OPT record with EDNS version set to 0
expect: not to see SOA record in the ANSWER section of the query response
See RFC6891, 6.1.3. OPT Record TTL Field Use

EDNS - Unknown Option
---------------------
```bash
dig +norec +ednsopt=100 soa zone @server
```
expect: SOA record in the ANSWER section of the query response
expect: status is `NOERROR`
expect: OPT record with EDNS version set to 0
expect: that the EDNS option will not be present in response
See RFC6891, 6.1.2 Wire Format
+ednsopt and +ednsflags require BIND 9.11.0 or later.

EDNS - Unknown Flag
-------------------
```bash
dig +norec +ednsflags=0x80 soa zone @server
```
expect: SOA record in the ANSWER section of the query response
expect: status is `NOERROR`
expect: OPT record with EDNS version set to 0
expect: Z bits to be clear in response
See RFC6891, 6.1.4 Flags
\_+ednsopt and +ednsflags require BIND 9.11.0 or later. _


EDNS - DO=1 (DNSSEC)
--------------------
```bash
dig +norec +dnssec soa zone @server
```
expect: SOA record in the ANSWER section of the query response
expect: status is `NOERROR`
expect: OPT record with EDNS version set to 0
expect: DO flag set in response if RRSIG is present in response
See RFC3225

EDNS - Truncated Response
-------------------------
```bash
dig +norec +dnssec +bufsize=512 +ignore dnskey zone @server
```
expect: status is `NOERROR`
expect: OPT record with EDNS version set to 0
This is an opportunistic test only
We can't test a zone for the ability to indicate that an answer was truncated (setting the TC flag in a response) unless we know which query to send it that will definitely result in a large response. If you are testing your own zone, you know what RRsets you have in it, so may be able to create a better test query. The reason our test uses DNSKEY and +dnssec is that there is a very good chance that the query response for a DNSSEC-signed zone will exceed 512 bytes

See RFC6891, 7. Transport Considerations

EDNS - Unknown Version with Unknown Option
------------------------------------------
```bash
dig +norec +edns=100 +noednsneg +ednsopt=100 soa zone @server
```
expect: status is `BADVERS`
expect: OPT record with EDNS version set to 0
expect: not to see SOA in the ANSWER section of the query response
expect: that the EDNS option will not be present in response
See RFC6891

The above expectations are based on the following preconditions:

* Only EDNS version 0 is defined currently.
* EDNS option 100 is not yet defined.
* The only EDNS flag defined is DNSSEC OK (DO).
* When EDNS version 1 is defined we expect to see:
* OPT record with version set to 0 or 1 (this is because EDNS compliance includes indicating which version the server supports in a server response).

When sending EDNS versions other than zero, you expect to see 
`BADVERS` or an EDNS version greater than or equal to the version 
you send in the response. If the version is less than the version 
you send and the status is `NOERROR`, `NXDOMAIN`, or `YXDOMAIN`, the 
server is non-compliant.


EDNS Compliance
===============
EDNS is an add-on to the DNS protocol and pertains to 
conveying LARGE DNS-RESPONSE answers back to the 
requester.

Historically, DNS worked for single answer which often
fits within 512-byte-sized UDP packet.  Specification
of DNS was limited to 512-byte UDP packet at the most.

As more and more RDATA get packed for a single question,
it soon overran the 512-byte limit.

EDNS came to the rescue with a support for even larger
 answer section.  It works up to 4K over UDP and 
falls back to TCP to go bigger than 4K (in case some
wonky firewall threw a fit over large UDP packets).

Visit this EDNS Compliance site to ensure your server works.
Be sure to fill in both the zone AND your DNS Server address 
(even though Server says 'optional', do it anyway).

URL: [https://ednscomp.isc.org/ednscomp](https://ednscomp.isc.org/ednscomp)

References
==========
* [EDNS Compliance](https://ednscomp.isc.org/ednscomp/)
