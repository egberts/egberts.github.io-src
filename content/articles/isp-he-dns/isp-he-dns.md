title: Hurricane Electric DNS as a Slave Nameserver
date: 2022-04-15 13:29
status: published
tags: ISP, DNS
category: HOWTO
summary: How to add Hurricane Electric as a secondary name server
lang: en
private: False

This article details how to incorporate Hurricane Electric (HE.NET) DNS as the secondary name servers for your public authoritative name server.

In this article, all instances of `example.test` can be replaced with your domain name.  Graphical screenshots may have `egbert.net`, of which you too can replace with your domain name.

# Generate TSIG Key 

TSIG stands for Transaction SIGnature and is defined in [IETF RFC 2845](https://datatracker.ietf.org/doc/html/rfc8945).

First, generate the TSIG key that HE.NET will need to access the zone data via AXFR transfer from your primary authoritative name server.

NOTE: Older Bind9 versions used `ddns-confgen` tool, but now it is `tsig-keygen`.

```bash
$ tsig-keygen -a hmac-sha512 axfr-request-to-primary-server-from-public-secondaries
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

# Secondary DNS Providers

## Hurricane Electric

Visit [Hurricane Electric](http://he.net/) and select "Free DNS" in right-side navigation panel.


Create an account (if haven't got one yet) and login:

<div class="m-image">

  <img src="{attach}/articles/isp-he-dns/images/isp-he-dns-0.png"
       link="{attach}/articles/isp-he-dns/images/isp-he-dns-0.png"
      class="m-image"
      alt="Account Creation - Hurricane Electric"
      max-height=100% max-width=100% />
</div>

To add a new HE.NET DNS slave nameserver, in the left navigation panel,
click on `Add a new slave`.

<div class="m-image">

  <img src="{attach}/articles/isp-he-dns/images/isp-he-dns-1.png"
       link="{attach}/articles/isp-he-dns/images/isp-he-dns-1.png"
      class="m-image"
      alt="Adding A Secondary Nameserver - Hurricane Electric"
      max-height=100% max-width=100% />
</div>


A new dialog box appears asking for your:

* Domain Name
* Master #1
* Master #2 (optional)
* Master #3 (optional)
* TSIG Hash Algorithm
* TSIG Key Name
* TSIG Secret Hash

Enter in all info (except for the optional ones).

Click the green "Add Slave" button.


<div class="m-image">

  <img src="{attach}/articles/isp-he-dns/images/isp-he-dns-2.png"
       link="{attach}/articles/isp-he-dns/images/isp-he-dns-2.png"
      class="m-image"
      alt="Entering in Slave Info - Hurricane Electric"
      max-height=100% max-width=100% />
</div>


Now you have a secondary nameserver to your primary (authoritative) nameserver.

<div class="m-image">

  <img src="{attach}/articles/isp-he-dns/images/isp-he-dns-3.png"
       link="{attach}/articles/isp-he-dns/images/isp-he-dns-3.png"
      class="m-image"
      alt="Domain added - Hurricane Electric"
      max-height=100% max-width=100% />
</div>


To get the current status of this newly-added slave zone nameserver 
of your domain name, hover your mouse over the blue "i"nformation icon.

When the mouse hovers over blue "i", a tooltip appears showing
the phrase "Click for slave zone information".

Click the blue "i" icon button.

<div class="m-image">

  <img src="{attach}/articles/isp-he-dns/images/isp-he-dns-4.png"
       link="{attach}/articles/isp-he-dns/images/isp-he-dns-4.png"
      class="m-image"
      alt="Account - Hurricane Electric"
      max-height=100% max-width=100% />
</div>


It takes about 3600 seconds to fully sync up.

Click on the green "validate" botton.

WARNING: Do not click on the BLUE BUTTON.  If you do, you would need to delete the entire settings of your domain and start all over again.  Yeah, be careful there.

<div class="m-image">

  <img src="{attach}/articles/isp-he-dns/images/isp-he-dns-5.png"
       link="{attach}/articles/isp-he-dns/images/isp-he-dns-5.png"
      class="m-image"
      alt="Account - Hurricane Electric"
      max-height=100% max-width=100% />
</div>

You should have a working secondary nameserver now.

