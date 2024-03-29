Title: DNSSEC Algorithm IDs
Date: 2020-02-03 06:14
Modified: 2020-09-16 11:40
status: published
slug: dnssec-algorithm-ids
tags: bind9, dnssec, algorithm
category: research
summary: How to use each DNSSEC algorithms

WHY DO THIS?
============
I've got a white-lab network with a standalone DNSSEC.  Plus it's an exercise for me.


What are the algorithms?
========================

IETF maintains a list of algorithms for DNSSEC which currently (at publication time) are:

DNSSEC algorithm table
[jtable separator=","]
<code>Number</code>, Bind Version, <code>Description</code>, Mnemonic, Zone <p>Signing, Transaction<p>Security, References
0, ???, Delete DS, `DELETE`, N , N , [RFC4034](https://tools.ietf.org/html/rfc4034)[RFC4398](https://tools.ietf.org/html/rfc4398)[RFC8078](https://tools.ietf.org/html/rfc8078)
1, v9.0-9.13, RSA/MD5 (deprecated see 5), `RSAMD5`, N , Y , [RFC3110](https://tools.ietf.org/html/rfc3110)[RFC4034](https://tools.ietf.org/html/rfc4034)
2, "v9.0-9.6,9.17.4", Diffie-Hellman, `DH`, N, Y, [RFC2539 proposed standard](https://tools.ietf.org/html/rfc2539) [RFC3755 proposed standard](https://tools.ietf.org/html/rfc3755)[RFC2536 proposed standard](https://tools.ietf.org/html/rfc2536)[Federal Information Processing Standards Publication (FIPS PUB) 186](https://doi.org/10.6028/NIST.FIPS.186-4)
3, v9.0-9.13, DSA/SHA1, `DSA`, Y, Y, [Signature Standard; 18 May 1994; Federal Information Processing Standards Publication (FIPS PUB) 180-1; Secure Hash Standard; 17 April 1995. (Supersedes FIPS PUB 180 dated 11 May 1993.)](https://doi.org/10.6028/NIST.FIPS.180-4)
4, , Reserved, , , , [RFC6725](https://tools.ietf.org/html/rfc6725)
5, v9.3-v9.17?, RSA/SHA-1, `RSASHA1`, Y, Y, [RFC3110](https://tools.ietf.org/html/rfc3110)[RFC4034](https://tools.ietf.org/html/rfc4034)
6, v9.6-v9.13, DSA-NSEC3-SHA1, `NSEC3DSA`, Y, Y, [RFC5155 proposed standard](https://tools.ietf.org/html/rfc5155)
7, v9.6-v9.17?, RSASHA1-NSEC3-SHA1, `NSEC3RSASHA1`, Y, Y, [RFC5155 proposed standard](https://tools.ietf.org/html/rfc5155)
8, v9.6-v9.17?, RSA/SHA-256, `RSASHA256`, Y, \*, [RFC5702 proposed standard](https://tools.ietf.org/html/rfc5702)
9, , Reserved, , , , [RFC6725](https://tools.ietf.org/html/rfc6725)
10, v9.6-v9.17?, RSA/SHA-512, `RSASHA512`, Y, \*, [RFC5702 proposed standard](https://tools.ietf.org/html/rfc5702)
11, , Reserved, , , , [RFC6725](https://tools.ietf.org/html/rfc6725)
12, v9.8-v9.12, GOST R 34.10-2001, `ECC-GOST`, Y, \*, [RFC5933 standards track](https://tools.ietf.org/html/rfc5933)
13, v9.8-v9.17?, ECDSA Curve P-256 with SHA-256, `ECDSAP256SHA256`, Y, \*, [RFC6605 standards track](https://tools.ietf.org/html/rfc6605)
14, v9.8-v9.17?, ECDSA Curve P-384 with SHA-384, `ECDSAP384SHA384`, Y, \*, [RFC6605][standards track]
15, v9.9-v9.17?, Edwards-curve Digital Security Algorithm (EdDSA) 128-bit security level, `ED25519`, Y, \*, [RFC8080][standards track]
16, v9.9-v9.17?, Edwards-Curve Digital Security Algorithm (EdDSA) 224-bit security, `ED448`, Y, \*, [RFC8080][standards track]
17-122, , , , , , Unassigned
123-251, , Reserved, , , , [RFC4034][RFC6014]
252, , Reserved for Indirect Keys, `INDIRECT`, N, N, [RFC4034][proposed standard]
253, , private algorithm, `PRIVATEDNS`, Y, Y, [RFC4034]
254, , private algorithm OID, `PRIVATEOID`, Y, Y, [RFC4034]
255, , Reserved, , , , [RFC4034][proposed standard]
[/jtable]

Where Is Algorithm ID Found At?
-------------------------------
DNSSEC algorithms ID are found in DNS record files and DNSSEC packets.

Example DNS record file below:

```cfg
    dig upenn.edu DNSKEY;; ANSWER SECTION:
    upenn.edu.              7200 IN DNSKEY 256 3 5 (
                                    AwEAAcDt107stSjvoBA/YVPr+2gvB3v33tXr7ROZ/Jqm
                                    WtNLraxQPzgXM1AhwjtdEqwCAnk01V7+Fw7K94sh6jpI
                                    5bFofS7MGtd0VvNyq52bgRnusgbm1ME2Lx9+o3fy9ppv
                                    7C6bahGrV3aiq9wNVPj/ccJn5AnZCOsi3grVsj6izCYH
                                    ) ; key id = 46752
```

In the RRDATA portion, after the DNSKEY keyword, there are three numbers:

* The number <code>256</code> (after <code>DNSKEY</code>) in the RRDATA portion is a decimal integer value whose bit representations are:
* The number <code>3</code> represents DNSSEC.
* Using the <code>dig</code> utility, the ID defaults to the number <code>5</code> represents RSA-SHA1 algorithm.  Newer <code>delv</code> also defaults to RSA-SHA1 algorithm.  Number <code>5</code>


    bit  - description
    1    - SEP flag
    7    - zone flag
    8    - Revoke


How To Create Algorithm-specific Keys
=====================================

Utility <code>dnssec-keygen</code> can use most of the following algorithms:

    RSA | RSAMD5 | DSA | RSASHA1 | NSEC3RSASHA1 | NSEC3DSA |
    RSASHA256 | RSASHA512 | ECCGOST |
    ECDSAP256SHA256 | ECDSAP384SHA384 |
    ED25519 | ED448 | DH |
    HMAC-MD5 | HMAC-SHA1 | HMAC-SHA224 | HMAC-SHA256 |
    HMAC-SHA384 | HMAC-SHA512

Note: To support and generate GOST algorithm, both Bind9 and OpenSSL packages must be compiled with <code>-with-gost</code> option.

Common Algorithms Used Today
----------------------------

* 5 - RSA/SHA1 (default in BIND 9)
* 6 - DSA-NSEC3-SHA1
* 7 - RSA-NSEC3-SHA1
* 8 - RSA/SHA256
* 10 - RSA/SHA512
* 12 - ECC-GOST
* 13 - ECDSA Curve P-256 SHA256
* 14 - ECDSA Curve P-384 SHA384

Creating algorithm keys
-----------------------

```bash
dnssec-keygen -f KSK -T DNSKEY
```

Creating algorithm-specific keys
--------------------------------

Default flags for <code>dnssec-keygen</code> are:

  ;; -n defaults to ZONE
  ;; -c defaults to IN class
  ;; -p defaults to 3 (DNSSEC protocol)
  ;; -T defaults to DNSKEY (otherwise used for TSIG)
  ;; -t defaults to AUTHCONF

To sign a zone like ".", "net.", or "example.net.", <code>dnssec-keygen</code>
CLI flags are:

```bash
dnssec-keygen -f KSK -a RSASHA1 -b 512 . # Root DNS
dnssec-keygen -f KSK -a RSASHA1 -b 512 net.
dnssec-keygen -f KSK -a RSASHA1 -b 512 example.net.
dnssec-keygen -f KSK -a RSAMD5 -b 512   # other DNSSEC algorithms
```

To sign a TSIG key to be used for transfers between DNS servers as well as with <code>rndc</code> utility:

```bash
dnssec-keygen -n HOST -T KEY -a HMAC-MD5 -b 512 ns1-to-ns2-tsig
```

References
==========

* http://www.iana.org/assignments/dns-sec-alg-numbers
* http://www.huque.com/talks/2013-11-dnssec-tutorial-huque.pdf

