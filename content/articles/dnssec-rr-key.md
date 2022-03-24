title: DNS KEY Record (obsoleted by DNSKEY and IPSECKEY record)
date: 2022-03-23 11:31
status: published
tags: DNS
category: research
summary: Details on the DNS KEY record.
slug: dns-rr-key
lang: en
private: False


This article details the DNS KEY record type.

The DNS resource record (RR) type ID is 25dec, 19hex, 031oct.


Used only for SIG(0) (RFC 2931) and TKEY (RFC 2930).

RFC 3445 eliminated their use for application keys and limited their use to DNSSEC.

RFC 3755 designates DNSKEY as the replacement within DNSSEC.

RFC 4025 designates IPSECKEY as the replacement for use with IPsec.

Bind 9.17 SIG(0) can still be used with HMAC-SHA512 with the `dnssec-gen -T KEY -n HOST -p AAAAA` where AAAAA the choices of algorithm names are: 

* `hmac-md5`, 
* `hmac-sha1` .
* `hmac-sha224.
* `hmac-sha256.
* `hmac-sha384.
* `hmac-sha512.

An example generation of `hmac-sha512` is executed as:

```console
dnssec-keygen -T KEY -a hmac-sha512 -n HOST 
# tsig-keygen -a hmac-sha512
key "tsig-key" {
    algorithm hmac-sha512;
    secret "tdFtdMrHXhq11pZyGciDbtsXhsvhcGnf293c1Z/bUZCqDwqoLIQJZrY8RZccjZP8ZWkN91FQRJGaSfb39WX54Q==";
};

```


KEY Record Format
=================

```
mykeyname. IN KEY 0 3 5 AwEAAalkfPrFH6zq4nTDtZQHAKitJ+rcwtfs4zqC4nsfRCeQ65vPd8tm Ve7JQWgbFtpmHhnhd4YPttPO3wBsuQUBZozkjS2Lc5oe94UumFJDsL76 sgMPKh01we5nS/ItH4es+FCDobsa4SNnKJgipZBqiF/Vock1dE+YS/vf 1AkOFyiR
```

Also used directly with `nsupdate` command in `nsupdate` interactive CLI prompt.

* Hostname
* Class is always `IN` for Internet
* Record name is always `KEY` for this DNS record type
* Key Type is an 8-bit number
* Protocol Type  (3=DNSSEC)
* Number 3
* Public Key in base64 DNS-ZONE-break encoding.

Only the `dnssec-keygen` can generate SIG(0) keys needed by the DNS KEY record.

```bash
dnssec-keygen -T KEY -N xxx  my-key-name
```

Key ID used in KEY record:
[jtable]
`dnssec-keygen -N`, Key ID
`USER`, 0
`ZONE`, 255
`ENTITY` or `HOST`, 512
[/jtable]

Protocol Type used in KEY record:
[jtable]
`dnssec-keygen -p X`, Protocol
0, reserved
1, TLS
2, email
3, DNSSEC
4, IPSEC
255, any
[/jtable]

Algorithm
[jtable]
`dnssec-keygen -a X`, Protocol
     0,     reserved
     1,     RSA/MD5 [RFC 2537] - recommended
     2,     Diffie-Hellman [RFC 2539] - optional, key only
     3,     DSA [RFC 2536] - MANDATORY
     4,     reserved for elliptic curve crypto
     5,     RSA-SHA1
     6,     DSA-NSEC3-SHA1 (seldom used)
     7,     RSA-SHA1-NSEC3-SHA1 (seldom used)
     8,     RSA-SHA256; old current standard
     9,     reserved
    10,     RSA-SHA512; ideal standard (but seldom used)
    12,     ECC-GOST; GOST-R-34.10-2001
    13,     ECDSA-P256-SHA256  (current standard)
    14,     ECDSA-P384-SHA384  (future standard)
    15,     ED25519
    16,     ED448
   17-251,   available
   252,     reserved for indirect keys (INDIRECT)
   253,     private - domain name  (PRIVATEDNS)
   254,     private - OID (PRIVATEQID)
   255,     reserved
[/jtable]

Currently the Bind9 v9.17.4 DNS key generator `tsig-keygen` no longer makes SIG(0); but `dnssec-keygen` still does it.


Security Consideration
======================

Using SIG(0) or TKEY, the public key is stored in DNS safely IF and only IF the DNS record is also protected by DNSSEC.

The key thing to overall securedness is the lack of host resolver adherence to "strong" resolving their DNS queries into ensuring that the answer containing its answer has been DNSSEC-validated.

Key thing is that nearly 99% of the resolvers out there do not bother to check whether the DNSSEC is valid or not.

Despite the near perfect strength of the DNS record protection by DNSSEC, the weakness of the resolvers has undermined the usefulness of DNS KEY (and subsequentially TKEY and DNSKEY) record.

Your Bind9 DNS should have in the `options` clause the following settings:

```nginx
    disable-algorithms "mydomain.test." { 
        RSAMD5;              // 1
        DH;                  // DH;      // 2 - current standard
        DSA;                 // DSA/SHA1;
        4; 
        RSASHA1;             // RSA/SHA-1
        6;                   // DSA-NSEC3-SHA1
        7;                   // RSASHA1-NSEC3-SHA1
                             // RSASHA256;  // 8 - current standard
        9;                   // reserved
                             // RSASHA512;  // 10 - ideal standard
        11;                  // reserved
        12;                  // ECC-GOST; // GOST-R-34.10-2001
                             // ECDSAP256SHA256; // 13 - best standard
                             // ECDSAP384SHA384; // 14 - bestest standard
                             // ED25519; // 15
                             // ED448; // 16
        INDIRECT; 
        PRIVATEDNS; 
        PRIVATEOID; 
        255;
        };

    //  Delegation Signer Digest Algorithms [DNSKEY-IANA] [RFC7344]
    //  https://tools.ietf.org/id/draft-ietf-dnsop-algorithm-update-01.html
    disable-ds-digests "mydomain.test" {
        0;           // 0
        SHA-1;       // 1 - Must deprecate 
                     // SHA-256; // Widespread use, EGBERT.NET deprecates this
        GOST;        // 3 - has been deprecated by RFC6986
                     // SHA-384;  // 4 - Recommended
        };

    // disables the SHA-256 digest for .net TLD only.
    disable-ds-digests "net" { "SHA-256"; };

    max-rsa-exponent-size 4096;
```


References
===========

* [IANA Database](https://www.iana.org/assignments/dns-key-rr/dns-key-rr.xhtml#dns-key-rr-1)
* [RFC 2535](https://datatracker.ietf.org/doc/html/rfc2535#section-4.1)
* [RFC 2930 - TKEY]()
* [RFC 2931 Section 2.4. SIG(0) on the other hand, uses public key authentication, where the public keys are stored in DNS as KEY RRs and a private key is stored at the signer]()
* [RFC 3445 Section 1. DNSSEC will be the only allowable sub-type for the KEY RR ,,,]()
* [RFC 3755 Section 3. DNSKEY will be the replacement for KEY, with the mnemonic indicating that these keys are not for application use, per RFC3445. RRSIG (Resource Record SIGnature) will replace SIG, and NSEC (Next SECure) will replace NXT. These new types completely replace the old types, except that SIG(0) RFC2931 and TKEY RFC2930 will continue to use SIG and KEY.]()
* [RFC 4025 Abstract. This record replaces the functionality of the sub-type #4 of the KEY Resource Record, which has been obsoleted by RFC 3445.]()
* [RFC 2537]()


