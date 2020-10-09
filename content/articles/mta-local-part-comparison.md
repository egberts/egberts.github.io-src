title: Comparison of Local Part in MTAs
date: 2020-09-06 18:22
status: published
tags: mta, exim, sendmail, opensmtpd, postfix
category: research
summary: Comparison of MTAs with regard to Local Part of Email Address

Rationale
=========

The objective is to prevent (and track) email harvesting of my email address
through selective usage of username and local-part of its address.

So, I set out to compare the various open-source MTAs (smtp server, mail server,
mail transport agent) and how they
can handle the "local part" and the "addr-spec" ([RFC 822 Section 6.1](https://tools.ietf.org/html/rfc822#section-6.1)) of a email address.

The open-source MTAs covered and reviewed for this article are:

* [sendmail](sendmail.org)
* [exim](exim.com)
* [postfix](postfix.org)
* [OpenSMTPd](opensmtpd.org)


Ideally, my selected email server (MTA, mail transport agent)
would be able to handle and break down this "local part" of the email address.

Specifically the local part being after the '+' (or '-') 
symbol but before the '@' symbol:

```
    local-part@domain.tld
```


Definitions
-----------
With regard to the 'local-part' portion of the email address, I'm sadden 
to say that the official definitions of 'local-part' has been muddled by
various open source MTAs.   More on this
[here](https://wordtothewise.com/2017/08/local-part-semantics/).

I'll tabulate their current terms and you'll see:

[jtable]
IETF terms, postfix, exim, sendmail, opensmtpd, Google
addr-spec, address, address, address, address, address
domain, domain, domain, domain, domain, domain
username, user, username, user, username, user
other local part, local\_part, local-part, detail, n/a, address extension
separator, recipient\_delimiter, , , , 
separator used, [+-=_!%$], +, +, +/-/=, +
[/jtable]


In [RFC 5321 Section Local-Part](https://tools.ietf.org/html/rfc5321#section-4.5.3.1.1), the parts of the email address is broken down as:
```
local-part@domain.tld
```
* Local-part contains the user name and optionally this other local-part.  
* Domain can be a domain name or IP address.
* TLD is the top-level domain name.

Local-Part Subdefinition
--------------------
Furthermore, the general trend of today's email and its local-part can 
be constructed as:
```
username+otherlocalpart@domain.tld (ie., Google, Apple)
username-otherlocalpart@domain.tld (ie., Yahoo)
```
For awhile, some MTAs have changable separator symbol between username
and other local part such as period or underscore.  The downside 
of this configurable separator is that many website cannot validate
this unique non-positive/non-negative separator symbol.

CRITERIA
========
I have this unique criteria for local part handling of my email address:

* Ability to use period ('.') symbol as the separator (instead of -/+).
* Ability to allow valid username with local part but to reject username alone
* Ability to use local part as a prefix to the username (and not normally as a
  suffix)
* Ability to find the multiple consecutive period symbols in a local-part and 
  be able to condense into a singular period, like Google mail can.

I just need one or the other, but both is preferable.

Period Separator
----------------
The ability to use period '.' as the separator between username and
local part would enable me to pursue the following email addresses:

```
john.facebook@domain.tld
john.twitter@domain.tld
```
And receive all emails to username 'john'.

Reject the valid username 
-------------------------

But the following would get rejected:
```
john@domain.tld
```

Prefix Local Part
-----------------

To use the local part as a prefix instead of a suffix.  Normally,
the local part would be used as a suffix form:


