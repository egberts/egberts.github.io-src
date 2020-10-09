title: Migrating to trusted-keys in Bind9
date: 2020-09-07 12:18
status: published
tags: bind9, dnssec
category: HOWTO
summary: How to migrate from managed-keys to trusted-keys in Bind9

Bind  9.6.2 and above have shifted to `trusted-keys` clause keyword
and made `managed-keys` largely obsoleted.

Here's how to migrate to the new clause keyword:


BIND 9.6.2 and above
====================

In your BIND `named.conf` configuration, add the following lines:
 
```nginx
trusted-keys {
  . 257 3 8 
  "AwEAAagAIKlVZrpC6Ia7gEzahOR+9W29euxhJhVVLOyQbSEW0O8gcCjF
     FVQUTf6v58fLjwBd0YI0EzrAcQqBGCzh/RStIoO8g0NfnfL2MTJRkxoX
     bfDaUeVPQuYEhg37NZWAJQ9VnMVDxP/VHL496M/QZxkjf5/Efucp2gaD
     X6RS6CXpoY68LsvPVjR0ZSwzz1apAzvN9dlzEheX7ICJBBtuA6G3LQpz
     W5hOA2hzCTMjJPJ8LbqF6dsV6DoBQzgul0sGIcGOYl7OyQdXfZ57relS
     Qageu+ipAdTTJ25AsRTAoub8ONGcLmqrAmRLKBP1dfwhYB4N7knNnulq
     QxA+Uk1ihz0=";

};

options 
  dnssec-validation yes;
};
```

and restart the BIND DNS Server.

BIND 9.7.x
==========
Starting with BIND 9.7.0, the trusted keys can be managed by 
RFC 5011 (RFC 5011 - Automated Updates of DNS 
Security (DNSSEC) Trust Anchors)

In BIND `named.conf`, add the following:

```nginx
managed-keys {
   "." initial-key 257 3 8
    "AwEAAagAIKlVZrpC6Ia7gEzahOR+9W29euxhJhVVLOyQbSEW0O8gcCjF
     FVQUTf6v58fLjwBd0YI0EzrAcQqBGCzh/RStIoO8g0NfnfL2MTJRkxoX
     bfDaUeVPQuYEhg37NZWAJQ9VnMVDxP/VHL496M/QZxkjf5/Efucp2gaD
     X6RS6CXpoY68LsvPVjR0ZSwzz1apAzvN9dlzEheX7ICJBBtuA6G3LQpz
     W5hOA2hzCTMjJPJ8LbqF6dsV6DoBQzgul0sGIcGOYl7OyQdXfZ57relS
     Qageu+ipAdTTJ25AsRTAoub8ONGcLmqrAmRLKBP1dfwhYB4N7knNnulq
     QxA+Uk1ihz0=";
}; 
```

and restart the BIND DNS Server. 
