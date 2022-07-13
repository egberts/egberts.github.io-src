title: Use subjectAltName (SAN) in OpenSSL
date: 2022-03-20 11:37
modified: 2022-04-04 10:28
status: published
tags: OpenSSL, X509v3
category: HOWTO
summary: How to use `subjectAltName` correctly in a OpenSSL configuration file.
slug: openssl-subjectAltName
lang: en
private: False

Alternative Subject Name
========================

Alternative Subject Name (ASN) is a X509v3 extension field used during issuing of PKI certificates.

In X509v3 parlance, the attribute name is `subjectAltName`.

`subjectAltName` attributes are defined only under the scope of `[req]` section or its `req`-related sections, preferably under its own renamed `req` section.


Who Uses SAN?
=============

`subjectAltName` is frequently used by `serverAuth` and `clientAuth` (non-CA) certificates.  

`serverAuth` and `clientAuth` are extended key usages and are found in `extKeyUsage` of the certificate or `openssl.cnf` config file.

To find such extended key usages of a certificate, execute:
```command
$ openssl x509 -noout -text -in <your_PEM_file>
```
and look for `Extended X509v3 Key Usage:`.  If it is missing, there is no `serverAuth`.

`serverAuth` and `clientAuth` certificates are used by web servers and any endpoint communications that needs a TLS protocol cover (email, REST API, IM).



What Goes Into SAN?
===================

The `subjectAltName` extension (if declared) MUST contain at least one entry; this is only true for any certificate that is using `serverAuth` (or `clientAuth`) such as a "web servers". 

`serverAuth` Certificates
-------------------------

For `serverAuth` certificates, at most one declaration of `altServerName` extension is permitted.

`altServerName` must have at least one entry, and separated by a comma symbol if more than.

`altServerName` only takes two types of entry:

* `iPAddress` (or simply `IP`)
* `dNSName` (or simply `DNS`)

`IP` MUST have an iPAddress containing the IP address of a server.  IP address shall not be a reserved IP address.

A tentative list of reserved IPv4 addresses not to use are: `0.0.0.0/8`, `10.0.0.0/8`, `100.64.0.0/10`, `127.0.0.0/8`, `169.254.0.0/16`, `172.16.0.0/12`, `192.0.0.0/24`, `192.0.2.0/24`, `192.88.99.0/24`, `192.168.0.0/16`, `198.18.0.0/15`, `198.51.100.0/24`, `203.0.113.0/24`, `224.0.0.0/4`, `233.252.0.0/24`, `240.0.0.0/4`, `255.255.255.255/32`.

For reserved IPv6 addresses not to use are: `::/0`, `::/128`, `::1/128`, `::ffff:0:0/96`, `::ffff:0:0:0/96`, `64:ff9b::/96`, `64:ff9b:1::/48`, `100::/64`, `2001:0000::/32`, `2001:20::/28`, `2001:db8::/32`, `2002::/16`, `fc00::/7`, `fe80::/64` from `fe80::/10`, `ff00::/8`.

`DNS` MUST contain the Fully‐Qualified Domain Name (FQDN).   They do not have to be resolvable nor online (useful for bringing up new websites).

Entries in the `DNS` MUST be in the "preferred name syntax", as specified in RFC 5280, and thus MUST NOT contain an underscore character ("`_`").  (this means no SVC domain names).

DNS also MUST NOT have any of the following: 

* `localhost`, `invalid`, `example`, `test` as a standalone word in any parts of the domain name, or 
* any reserved IP address mapped to `.in-addr.arpa.` or `.ip6.arpa.`.


CA Certificates
---------------

CA certificate should not use `subjectAltName`; It didn't say MUST NOT, so they can and have been used.  

`subjectAltName` for CA certificates are not used in the same way that "web servers" expect them to be used.  

Often times, it is just a simply description inserted by CA administrator of their own choosing.

Other Certificates
------------------

Other certificates NOT having the `serverAuth` nor `clientAuth` in their `extKeyUsage=` MAY use the `subjectAltName` at their discretion.  

It is much like a `nsComment` where short notation describing the function of the certificate might be helpful to others.

Using SAN
=========

SAN can be inserted and used in the following ways:

* at command line interface (CLI) using various CLI options
* in `openssl.cnf` configuration file

SAN at `openssl` CLI
--------------------

```console
$ openssl req -new -subj "/C=GB/CN=foo" \
                  -addext "subjectAltName = DNS:foo.co.uk" \
                  -addext "certificatePolicies = 1.2.3.4" \
                  -newkey rsa:2048 -keyout key.pem -out req.pem
```

SAN in Configuration File
-------------------------
Plainest way to specify a SAN:

```ini
[req]
req_extension = req_ext

[req_ext]
subjectAltName = DNS:alt.example.text
```

NOTE: if you let `req_extensions=XXXX` attribute get assigned under
its `[ req ]` section, then `-addext` CLI argument option would completely get ignored.

That is why `req_extensions=` should be under their own section name rather than under '[ req ]' section (but that's rarely done, except maybe for Root CA).

So, break out those sections to insulate yourself from this seemingly quirk.


Tricks with SAN (subjectAltName)
================================

Duplicating commonName into subjectAltName
-------------------------------------------
Using '`${req_dn::commonName}`' to reference the '`[ req_dn ]`' section
(containing distinguished names for `openssl req` command) being set as a FQDN
string value, you can then also copy that into the `DNS.1` part of `subjectAltName`

```ini
[ req_ext ]
    
subjectAltName = @alt_names
    
[alt_names]
DNS.1 = ${req_dn::commonName}
DNS.2 = alt.example.test
```

This trick would save the effort of having to perform a duplicate data entry within a script language.


Another trick
-------------
By appending custom attribute settings to the end of openssl.cnf,
you can introduce various settings this way, even overwriting
pre-existing setting too!

```console
$ openssl req -new -sha256 \
    -key domain.key \
    -subj "/C=US/ST=CA/O=Acme, Inc./CN=example.com" \
    -reqexts SAN \
    -config <(cat /etc/ssl/openssl.cnf \
        <(printf "\n[SAN]\nsubjectAltName=DNS:example.com,DNS:www.example.com")) \
    -out domain.csr
```


Leverage -extfile for adding to a read-only OpenSSL.cnf file.
-------------------------------------------------------------

```console
    openssl genrsa -out ca.key 2048
    openssl req -new -x509 -days 365 -key ca.key \
        -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=Acme Root CA" -out ca.crt
    openssl req -newkey rsa:2048 -nodes -keyout server.key \
        -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=*.example.com" -out server.csr

    openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
        -extfile <(printf "subjectAltName=DNS:example.com,DNS:www.example.com")\
        -days 365 -out server.crt
```

References
==========
* [Reserved IP addresses (Wikipedia)](https://en.wikipedia.org/wiki/Reserved_IP_addresses)
