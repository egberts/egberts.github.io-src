title: Hurricane Electric DNS as a Slave
date: 2022-04-15 13:29
status: draft
tags: ISP, DNS
category: HOWTO
summary: How to add Hurricane Electric as a secondary name server
lang: en
private: False

This article details how to incorporate Hurricane Electric (HE.NET) DNS as the secondary name servers to your public authoritative name server.

In this article, all instances of `example.test` can be replaced with your domain name.

# Generate TSIG Key 

TSIG stands for Transaction SIGnature and is defined in [IETF RFC 2845](https://datatracker.ietf.org/doc/html/rfc8945).

First, generate the TSIG key that HE.NET will need to access the zone data via AXFR transfer from your primary authoritative name server.

NOTE: Older Bind9 versions used `ddns-confgen` tool, but now it is `tsig-keygen`.

```bash
$ tsig-keygen -a hmac-sha512 public-master-to-public-secondary
```

Edit the configuration file for Bind9 named daemon (typically `/etc/bind/named.conf`).

# ACL Clauses

For the following lines, insert at the beginning of the config file, probably after the last `acl` clause.  (Typically, ACL clauses are bunched together and placed firstly in the config file.)

```nginx
// allow-transfer to the requester (secondary name servers)
acl acl_grant_axfr_to_trusted_3rd_party_downstream_secondaries {
        216.218.133.2;  # current slave.dns.he.net
        };
```

The ACL clause defined  allows AXFR records to be sent to the desired HE.NET secondary name server) upon requests.


# Key Clauses

Copy the output created by `tsig-keygen` containing the 'key' clause into the named config (`/etc/bind/named.conf`) and place it after the last of any `acl` clauses at the beginning of the file.

```nginx
key "axfr-request-to-primary-server-from-public-secondaries" {
    algorithm hmac-sha512;
    secret "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX==";
};
```

This shared secret key value and `hmac-sha512` will also later on go into HE.NET web dialog of DNS SLAVE setup forms.


# Allow AXFR to HE.NET SLAVES

Insert/update/replace the following `allow-transfer` statement into this same `zone` clause.

```nginx
allow-transfer {
    !{
        !acl_grant_axfr_to_trusted_3rd_party_downstream_secondaries;
        any;
        };
    // only trusted downstream secondary name servers go past this point
    key "axfr-request-to-primary-server-from-public-secondaries";
    none;
};
```

# Allow AXFR to other (Bin9) secondary name servers

If there are other secondary name servers that runs Bind9, you can insert the following in their `/etc/bind/named.conf` file.


```nginx
server 10.1.2.3 {
    keys { 
        "axfr-request-to-primary-server-from-public-secondaries";
    };
};
```
