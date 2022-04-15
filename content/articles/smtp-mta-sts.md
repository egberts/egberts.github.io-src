title: Disabling MTA-STS for Your Mail Server
date: 2022-04-14 11:13
status: draft
tags: MTA-STA, SMTP, mail
category: research
summary: Was curious about MTA-STS and how it is used for a SMTP mail transport agent (MTA).
slug: smtp-mta-sts
lang: en
private: False

This article details the decreasingly use of `mta-sts` in SMTP mail transport agent.  And why we should set this up just to then disable this 'mta-sts'.


# Brief History of Secured SMTP

For a while, SMTP Mail Transport Agent (MTA, or mail server) were using STARTTLS to ensure that encryption are being used in an "opportunist" manner.

This means that the TCP connection for SMTP is not always encrypted, depending on how the receiving MTA can handle encryption.

Furthermore, it became apparent that STARTTLS is falling out of favor.  There is even a [command injection exploit for STARTTLS](https://blog.apnic.net/2021/11/18/vulnerabilities-show-why-starttls-should-be-avoided-if-possible/).

What was commonly used is called 'Implicit TLS' (using STARTTLS mechanism):  IMAP4, POP3, and few other protocols make uses of STARTTLS.

What we should be using is 'Explicit TLS' (just do it; TLS, directly; do not bother with plaintext protocol).

# mta-sts

Now to smooth the confusion of MTA mass-upgrade/mass-deployment between implicit TLS and explicit TLS, DNS has comes to the rescue once again.

DNS record now details how TLS are to be used for MTA traffic for your domain; this is called MTA-STS.

[IETF RFC 8461](https://datatracker.ietf.org/doc/html/rfc8461) defines MTA-STS as:
```
SMTP MTA Strict Transport Security (MTA-STS) is a 
mechanism enabling mail service providers (SPs) to 
declare their ability to receive Transport Layer 
Security (TLS) secure SMTP connections and to specify 
whether sending SMTP servers should refuse to deliver 
to MX hosts that do not offer TLS with a trusted 
server certificate.
```

Also, MTA-STS is a TXT record that has settings governing how secured MTA should be.  No fancy DNS record type needed here.

Oh, did I mention, MTA-STS only details whether your MTA can support STARTTLS or not?

This is what we do not want anymore: 'implicit TLS', no more.

Even given the recent IETF RFC submission in 2018, this one feature should have been a dead-on-arrival specs.

Hence, this article details how to proactively disable MTA-STS.


# Disabling MTA-STS

Next, we disable the MTA-STS.

It is very much like DMARC and SPF config settings.  A one-liner in your domain's DNS settings.  

If you operate the name server of your domain, locate the text-based DNS zone file having the origin of your domain name, edit the file.  For Bind9 admins, this primary zone file is specified in your domain's `zone` clause `file` statement of `/etc/named.conf` or roughly under `/var/lib/bind/master/` subdirectory.

At any rate, insert the following DNS record into your domain's DNS zone file
```dns
_mta-sts	TXT	"v=STS1; mode=none;"
```

## Test the DNS Records

Just before exiting that `$EDITOR` session of your `example.test` zone file, do not forget to bump up the serial number found in that domain's `SOA` record (near the beginning of the file).

Then reload (or restart) your name server daemon.

Recap:  `_mta-sts.example.test` is the FQDN of this MTA-STS TXT record.  One of the TXT records will be the set of MTA-STS settings and also point to a web server containing your MTA-STS policy file.

Check out the newly created TXT record.

### Unsecured DNS Query

In examples below, replace the `ns1.example.test` with your domain's authoritative (DNS) name server.

```console
$ nslookup -query=TXT _mta-sts.example.test.  ns1.example.test.
$ dig @ns1.example.test _mta-sts.example.test. TXT
```

Condensed output should have following relevant details:
```dns
_mta-sts.example.test. TXT	"v=STSv1; mode=none;"
```

We are done.



#
