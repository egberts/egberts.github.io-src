title: SSHFP DNS resource record
date: 2022-03-24 10:54
status: published
tags: DNS, SSHFP
category: HOWTO
summary: How to use SSHFP RR in DNS with OpenSSH?
slug: dns-rr-sshfp
lang: en
private: False


What are SSHFP records?
=======================

SSHFP records are DNS records that contain fingerprints for public keys used for SSH. They're mostly used with DNSSEC enabled domains. When an SSH client connects to a server it checks the corresponding SSHFP record. If the records fingerprint matches the servers, the server is legit and it's safe to connect.

What does SSHFP records look like?
----------------------------------

SSHFP records consist of three things:

    Public key algorithm
    Fingerprint type
    Fingerprint (in hex)

Public key algorithm
--------------------

There are five different algorithms defined in SSHFP as of 2021. Each algorithm is represented by an integer. The algorithms are:

    1 - RSA
    2 - DSA
    3 - ECDSA
    4 - Ed25519
    6 - Ed448

Fingerprint type
----------------

Two fingerprint types are defined in SSHFP as of 2012. Each fingerprint type is represented by an integer. These are:

    1 - SHA-1
    2 - SHA-256

How do I generate SSHFP records?
================================

You can use ssh-keygen to generate the records using the -r parameter, followed by the hostname (which does not affect the fingerprints so you can specify whatever you like instead)
Example

Using ssh-keygen and CentOS:

```
[root@localhost ~]# ssh-keygen -r my.domain.com
my.domain.com IN SSHFP 1 1 450c7d19d5da9a3a5b7c19992d1fbde15d8dad34
my.domain.com IN SSHFP 2 1 72d30d211ce8c464de2811e534de23b9be9b4dc4
```

Note: Sometimes `ssh-keygen` will ask for the location of the public certificate. If it asks, you will have to run `ssh-keygen` multiple times and every time specify a different certificate to make sure that you generate all necessary SSHFP records. Your public keys are usually located in `/etc/ssh`.

Security Consideration
======================
Protection of SSHFP is only assured by a properly signed resource record by DNSSEC but, But ... BUT most people (and many ISPs) do not instruct their DNS resolver to only return back a valid DNS record as determined by DNSSEC; having mentioned that, the possibility of SSHFP being hijacked remains.

Reference
=========
* [Using Ed25519 in SSHFP resource records (RFC7479)](https://datatracker.ietf.org/doc/html/rfc7479)
* [Using DNS to Securely Publish Secure Shell Key Fingerprints](https://datatracker.ietf.org/doc/html/rfc4255)
* [Use of SHA-256 Algorithm with RSA, DSA and ECDSA in SSHFP Resource Records](https://datatracker.ietf.org/doc/html/draft-os-ietf-sshfp-ecdsa-sha2)
* [Using DNS to Securely Publish Secure Shell Key Fingerprints](https://datatracker.ietf.org/doc/html/rfc4255)
