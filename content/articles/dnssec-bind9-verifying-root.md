title: How to verify DNS Root's DNSSEC
date: 2020-09-07 12:16
status: published
tags: dnssec, bind9, verification
category: HOWTO
summary: How to verify DNSSEC of a DNS Root Server

Manually verifying the keys
---------------------------
You should never blindly trust cryptographic keys published on websites 
like this (The editor of the webpage could have made a typo, the 
server hosting the site may be hacked ...).

To verify the key material, use the sequence below:

```bash
dig dnskey . @a.root-servers.net +noall +answer > root-zone-dnssec.key 
```

This command  will give you the root zones DNSKEY in the file 
"root-zone-dnssec.key". Compare the key in the file with the 
key material in your BIND configuration file. It should match.  

```bash
dnssec-dsfromkey -2 root-zone-dnssec.key
```
This command (you need "dnssec-dsfromkey" version 9.6.2 or better) will 
generate the delegation signer "DS" record for the DNSKEY from the 
root zone. The DS Record is a hash over the DNSKEY. Compare this 
DS record with the hash available from the official IANA 
Website ( http://data.iana.org/root-anchors/ )

The hash you find in the file(s) for the root-anchor on the IANA 
website must match the DS record data generated from the 
root-zones DNSKEY.

