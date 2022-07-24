title: SSHFP DNS resource record
date: 2022-03-24 09:54
modified: 2022-07-24 10:13
status: published
tags: DNS, SSHFP
category: HOWTO
summary: How to use SSHFP RR in DNS with OpenSSH?
slug: dns-rr-sshfp
lang: en
private: False

You ever get the following pesky prompts during an initial SSH login?

```console
$ ssh portal.mydomain.example
The authenticity of host 'portal.mydomain.example (192.168.1.2)' can't be established.
ECDSA key fingerprint is SHA256:X15/p/zsUBNKRAg3jSLkmEiFiIlrE6uIvNvDgzWTJzE.
Are you sure you want to continue connecting (yes/no)? ^C
```
What if you can make that go away and protect yourself from any future
man-in-the-middle SSH attack?

If you have your domain zone database protected by DNSSEC enabled and properly deployed, this protection too can be done.

To do this:

* Insert a SSH-fingerprint DNS resource record into your `mydomain.example` DNS zone database file
* tweak the SSH client config a bit

and that's all to it. (Well, of course, you would need to reload/restart the nameserver, after all is said and done).

The tweak part of SSH client is the `VerifyHostKeyDNS yes` option.  You can put that option
into one of the following files, depending on your blast radius. 

[jtable]
SSH Client File, Description
`$HOME/.ssh/config`, impacts only the `$HOME` login account
`/etc/ssh/ssh_config`, impacts all users on that host
`/etc/ssh/ssh_config.d/670-hostkey-verify-dns.conf`, multi-file config approach; useful when you do not want the setting overwritten by future package upgrades.
[/jtable]

You could even temporarily try it out from a command line using `-oVerifyHostKeyDNS=yes` CLI option, as in:

```bash
ssh -oVerifyHostKeyDNS=yes portal.mydomain.example
```

I have always taken the multi-file config approach because package upgrades
makes me "lose it".

File: `/etc/ssh/ssh_config.d/670-hostkey-verify-dns.conf`
```ini
#
# File: 670-hostkey-verify-dns.conf
# Path: /etc/ssh/ssh_config.d
# Title: Consult SSHFP for matching host fingerprint
# Description:
#   VerifyHostKeyDNS specifies whether to verify the 
#   remote key using DNS and SSHFP resource 
#   records.  
#
#   If this option is set to 'yes', the client will 
#   implicitly trust keys that match a secure 
#   fingerprint from DNS.  Insecure fingerprints 
#   will be handled as if this option was set to 
#   'ask'.  
#
#   If this option is set to 'ask', information on 
#   fingerprint match will be displayed, but the 
#   user will still need to confirm new host keys 
#   according to the 'StrictHostKeyChecking' option.  
#
#   The default is 'no'.  
#
#   See also VERIFYING HOST KEYS in ssh(1).
#
# VerifyHostKeyDNS no  # default
# VerifyHostKeyDNS ask
# VerifyHostKeyDNS yes

VerifyHostKeyDNS yes

```

<p></p>

# What are SSHFP records?

SSHFP records are DNS records that contain fingerprints of public keys used with SSH protocol. They're mostly used in companion with DNSSEC-enabled domains. 

When an SSH client connects to a SSH server, that server checks for that corresponding SSHFP record to ensure that this is the correct SSH server to talk to.

## What does SSHFP records look like?

SSHFP records consist of three things:

* Public key algorithm
* Fingerprint hash type
* Fingerprint hash value (in hex)

<p></p>

## Public key algorithm

There are currently five different algorithms defined in SSHFP as of 2021. Each algorithm is represented by an integer. The algorithms are:

[jtable]
Algorithm ID (AlgoID) , Algorithm Name
1 , RSA
2 , DSA
3 , ECDSA
4 , Ed25519
6 , Ed448
[/jtable]

<p></p>

## Fingerprint Hash type

Two fingerprint hash types are currently supported in SSHFP as of 2012. Each fingerprint type is represented by an integer. These are:

1. SHA-1
2. SHA-256

Do not worry too much about the strength of the hash algorithm here
because the DNSSEC secures this field with multi-chaining of at least
RSA2048/SHA256.

<p></p>

# How do I generate SSHFP records?

The `ssh-keygen` utility generates the records using the `-r` parameter, followed by the hostname (which does not affect the fingerprints so you can specify whatever you like instead)
Example

To generate the RR data for SSHFP, use `ssh-keygen` utility that comes with the SSH package:

```console
# ssh-keygen -r portal.mydomain.example
portal.mydomain.example IN SSHFP 1 1 450c7d19d5da9a3a5b7c19992d1fbde15d8dad34
portal.mydomain.example IN SSHFP 2 1 72d30d211ce8c464de2811e534de23b9be9b4dc4
```

Note: Sometimes `ssh-keygen` will ask for the location of the public certificate. If it asks, you will have to run `ssh-keygen` multiple times and every time specify a different certificate to make sure that you generate all necessary SSHFP records. Your public keys are usually located in `/etc/ssh`.

# Security Consideration

Of course, you do do have DNSSEC up and running?  

Protection of SSHFP is only assured by a properly signed resource record by DNSSEC but, But ... BUT most people (and many ISPs) do not instruct their DNS resolver to only return back a valid DNS record as determined by DNSSEC; having mentioned that, the possibility of SSHFP being hijacked remains.

The problem here is not the confidentiality of the public key (it isn’t confidential).

The problem here is the integrity of the dns record is holding this public key, publicly.

If not distributed securely (via DNSSEC), such SSHFP DNS records can be tampered with or replaced with another key. 

If a faked SSH CA server has the wrong public key configured (whose private key is in the hands of someone else), the client ends up by trusting that someone else.

Caution: Improper use of SSHFP records can have serious security consequences; follow these rules to avoid creating security vulnerabilities:

* Do not create SSHFP records in a zone that is not DNSSEC-secured.
* Never configure SSH clients to use SSHFP for a domain that is not DNSSEC-secured.
* Never configure SSH clients to use SSHFP unless they validate DNSSEC or use a validating resolver, such as Google Public DNS.
* MOST IMPORTANTLY, always, always perform `delv ssh.domain.tld.` and check that first line for `; fully validated` output.  


Not following these rules could allow adversaries to create spoofed SSHFP records for your servers to impersonate them, making SSH connections to the servers insecure and vulnerable to attacks.

You can avoid the "always perform `delv ssh.domain.tld` for `; fully validated`) by having glibc perform this at resolve time.  If you must require absolute DNSSEC verified queries for all your DNS needs, you could insert the following into your `/etc/resolv.conf` (if you have glibc v2.38 or later):

File: `/etc/resolv.conf`
```
.
.
.
options edns0
options trust-ad
.
.
.
```

# Reference

* [Using Ed25519 in SSHFP resource records (RFC7479)](https://datatracker.ietf.org/doc/html/rfc7479)
* [Using DNS to Securely Publish Secure Shell Key Fingerprints](https://datatracker.ietf.org/doc/html/rfc4255)
* [Use of SHA-256 Algorithm with RSA, DSA and ECDSA in SSHFP Resource Records](https://datatracker.ietf.org/doc/html/draft-os-ietf-sshfp-ecdsa-sha2)
* [Using DNS to Securely Publish Secure Shell Key Fingerprints](https://datatracker.ietf.org/doc/html/rfc4255)
* [Google Cloud DNS/SSHFP](https://cloud.google.com/dns/docs/dnssec-advanced)
* [Weber Blog - SSHFP: Authenticate SSH Fingerprints via DNSSEC](https://weberblog.net/sshfp-authenticate-ssh-fingerprints-via-dnssec/)
* [SSHFP tutorial: how to get SSHFP records, DNSSEC, and VerifyHostKeyDNS=yes to work](https://fanf.livejournal.com/130577.html)
