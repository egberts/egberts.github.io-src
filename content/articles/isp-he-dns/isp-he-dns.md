title: Hurricane Electric DNS as a Secondary Nameserver
date: 2022-04-15 13:29
status: published
tags: ISP, DNS
category: HOWTO
summary: How to add Hurricane Electric as a secondary name server
slug: isp-he-dns-secondary
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

# Validate DNS Transfer

To validate that secondary DNS is actually receiving from your master nameserver, 
we need to start logging this `info` severity level for any and all AXFR/IXFR 
transfer activities.

## Finding Channel Name

To locate this `severity` setting in `/etc/bind/named.conf` (or `/etc/bind/logging-named.conf`, in my case), we need to find the correct logging category. 
This depends on whether you used the `category xfer-in` statement or not.

## Category `xfer-in` Used

If the `category xfer-in` statement is found, then note the names of logging channel
inside its curly-braces block.

```nginx
   category xfer-in { xfer-in_file };
```

In this example, `xfer-in_file` is the lone channel name.


## Category `default` Used

If the `xfer-in` category is not being used (nor found) amongst the config files,
then `category default` is our focus for this logging of DNS zone transfers.

```nginx
   category default { default_file };
```

## Channel Name

Once you identified the channel name (`xfer-in_file` or `default-file`), 
locate the `channel xfer-in_file` (or `channel default_file`, 
if `xfer-in` is not found).

In your selected `channel` statement, there should be a `severity` option
in that curly-braces block.  If not, add a `severity notice` option.

```nginx
    channel xfer-in_file {
        file "/var/log/named/xfer-in";
        severity notice;
        print-time yes;
        print-severity true;
        print-category true;
        };
```

Restart `named` daemon, if a change was made there.

In the `/var/log/named`, 
Then check out the log files for the following log message:

```console
17-Sep-2020 09:15:51.377 xfer-out: info: client @0x7fa60c03c1b0 216.218.133.2#55905/key <YOUR-KEY-NAME> (example.test): view public: transfer of 'example.test/IN': AXFR started: TSIG <YOUR-KEY-NAME> secondary (serial 2020091852)
```
The example log message above shows that the Hurricane Electric secondary nameserver
has successfully retrieved your master zone data file for `example.test`.

Congratulations, you have a working secondary nameserver now.

