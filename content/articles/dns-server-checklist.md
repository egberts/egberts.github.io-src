title: DNS server checklist
date: 2022-04-30 10:35
status: published
tags: DNS
category: HOWTO
summary: How to checkout your DNS server
slug: dns-server-checklist
lang: en
private: False

So your DNS server is up and running.  What to do next?

There is always online test tools to ensure that the DNS server
is properly confgured, at least from the network level.

This article only covers the network part of DNS and its interaction
from the Internet (or real world).  It does not details aspects 
on hardening or strengthening of your DNS server 

# First Thing First

The very first test you should perform is:

    Is recursion turned off in my DNS server?

Go visit the [OpenResolver.com](https://openresolver.com/) and plug in 
the IP address of your public-facing authoritative DNS server.


# Scripting the Test

You can also script the test to ensure that you didn't break the
nameserver after changing its configuration:

```bash
dig +short test.openresolver.com TXT @1.2.3.4
```



# References

* [https://openresolver.com/](https://openresolver.com/)
* [https://dnscheck.tools/#advanced](https://dnscheck.tools/#advanced)
