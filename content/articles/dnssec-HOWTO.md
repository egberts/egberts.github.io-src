title: How to setup DNSSEC
date: 2018-11-15 11:00
status: published
tags: dnssec, bind9
category: HOWTO
summary: How to set up the DNSSEC server (expert-level)

About DNSSEC
------------

Really, you can read up on DNSSEC here.

DNSSEC Resource Records
-----------------------

DNSSEC introduced several resource records (RR):

* DNSKEY Holds the public key which resolvers use to verify.
* RRSIG Exists for each RR and contains the digital signature of a record.
* DS - Delegation Signer – this record exists in the TLD’s nameservers. So if example.tld was your domain name, the TLD is “com” and its nameservers are a.gtld-servers.net., b.gtld-servers.net. up to m.gtld-servers.net.. The purpose of this record is to verify the authenticity of the DNSKEY itself.

Obtaining Additional Information
--------------------------------
This article requires that you obtain the following information in advance:

* Your domain name
* Your primary nameserver (NS), both IP and fully-qualified domainname (FQDN).
* Your secondary NS, both IP and FQDN.
* Your domain name registrar website, webpage to your 
account-\>DNS-\>Advanced-DNS-\>DS-keys.
* Your host provider website, webpage to your DNS settings

Note: Primary NS used to be called Master NS.  And Secondary NS used to be
called Slave NS: not anymore.

Setup Environment
-----------------

Domain Name: example.tld

This article will use `example.tld` to represent your domain name that 
you wish to enable DNSSEC with.

Article also assumes the following faked values:

* Primary NS:
    - IP Address: 1.1.1.1
    - Hostname: primary.example.tld  (could be `ns1.example.tld`)
    - OS: Debian 10
* Secondary NS:
    - IP Address: 2.2.2.2
    - Hostname: secondary.example.tld  (could be `ns2.example.tld`)
    - OS: Debian 10

File locations and names
------------------------

The names and locations of configuration and zone files of BIND 
different according to the Linux distribution used. Here, we use 
Debian 10 (Buster) and Bind v9.16.1.

[jtable]
Description, Detail
Service name, `bind9`
named configuration file, `/etc/bind/named.conf`
named Options clause config file, `/etc/bind/named.conf.options`
named View clause config file, `/etc/bind/named.conf.local`
named zone record research (RR) files, `/var/lib/bind/primary/db.example.tld`
named cached data directory, `/var/cache/bind/`
[/jtable]

These may change if you’re using `bind-chroot`. 

For this tutorial, I’ve used Debian for both the Primary NS and Secondary NS, 
so change it according to your distribution.

DNSSEC Primary NS Configuration
----------------------------

Enable DNSSEC by adding the following named configuration directives 
inside the `options { };` clause.

```bash
vim /etc/bind/named.conf.options
```

```nginx
dnssec-enable yes;
dnssec-validation yes;
dnssec-lookaside auto;
```

It is possible that these are already added in some distributions. 

Next, navigate to the location of your zone's resource record files:

```bash
cd /var/lib/bind/primary
# Clear out old key files keeping the last 2 sets of keys
let keep=0
for oldkey in `ls -1t Kexample.tld*.key`; do
    if $keep -gt 4; then
        rm $oldkey
    fi
    (($keep++))
done
```

Create a Zone Signing Key(ZSK) with the following command:

```
dnssec-keygen -a ECDSAP386SHA386 -n ZONE example.tld
```

If you have installed haveged, it’ll take only a few seconds for 
this key to be generated; otherwise it’ll take a very long time. 

```console
root@ns1:/var/cache/bind# dnssec-keygen -a ECDSAP386SHA386 -n ZONE example.tld
Generating key pair..................+++ .............+++
Kexample.tld.+007+40400
```

Create a Key Signing Key(KSK) with the following command:

```bash
dnssec-keygen -f KSK -a ECDSAP386SHA386 -n ZONE example.tld
```

Sample output.
```console
root@ns1:/var/cache/bind# dnssec-keygen -f KSK -a ECDSAP386SHA386 -n ZONE example.tld
Generating key pair......................++ .............................................................................................................................................................................................................++
Kexample.tld.+007+62910
```

The directory will now have 4 keys - private/public pairs of ZSK and KSK. 
We have to add the public keys which contain the DNSKEY record to the 
zone file. The following for loop will do this.

```
for key in `ls Kexample.tld*.key`
do
    cat $key >> dnskeys.example.tld
done
```

Sign the zone with the dnssec-signzone command.

dnssec-signzone -3 <salt> -A -N INCREMENT -o <zonename> -t <zonefilename>

Replace salt with something random. Here is an example with the output.

root@ns1:/var/cache/bind# dnssec-signzone -A -3 $(head -c 1000 /dev/random | sha1sum | cut -b 1-16) -N INCREMENT -o example.tld -t example.tld.zone
Verifying the zone using the following algorithms: ECDSAP386SHA386.
Zone signing complete:
Algorithm: ECDSAP386SHA386: KSKs: 1 active, 0 stand-by, 0 revoked
                        ZSKs: 1 active, 0 stand-by, 0 revoked
example.tld.zone.signed
Signatures generated:                       14
Signatures retained:                         0
Signatures dropped:                          0
Signatures successfully verified:            0
Signatures unsuccessfully verified:          0
Signing time in seconds:                 0.046
Signatures per second:                 298.310
Runtime in seconds:                      0.056

A 16 character string must be entered as the “salt”. The following command

head -c 1000 /dev/random | sha1sum | cut -b 1-16

outputs a random string of 16 characters which will be used as the salt.

This creates a new file named example.tld.zone.signed which contains RRSIG records for each DNS record. We have to tell BIND to load this “signed” zone.

nano /etc/bind/named.conf.local

Change the file option inside the zone { } section.

zone "example.tld" IN {
    type primary;
    file "example.tld.zone.signed";
    allow-transfer { 2.2.2.2; };
    allow-update { none; };
};

Save this file and reload bind

service bind9 reload

Check if for the DNSKEY record using dig on the same server.

dig DNSKEY example.tld. @localhost +multiline

Sample output

root@ns1:/var/cache/bind# dig DNSKEY example.tld. @localhost +multiline
;; Truncated, retrying in TCP mode.

; <<>> DiG 9.8.4-rpz2+rl005.12-P1 <<>> DNSKEY example.tld. @localhost +multiline
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 43986
;; flags: qr aa rd; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 0
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;example.tld.       IN DNSKEY

;; ANSWER SECTION:
example.tld.        86400 IN DNSKEY   256 3 7 (
                AwEAActPMYurNEyhUgHjPctbLCI1VuSj3xcjI8QFTpdM
                8k3cYrfwB/WlNKjnnjt98nPmHv6frnuvs2LKIvvGzz++
                kVwVc8uMLVyLOxVeKhygDurFQpLNNdPumuc2MMRvV9me
                fPrdKWtEEtOxq6Pce3DW2qRLjyE1n1oEq44gixn6hjgo
                sG2FzV4fTQdxdYCzlYjsaZwy0Kww4HpIaozGNjoDQVI/
                f3JtLpE1MYEb9DiUVMjkwVR5yH2UhJwZH6VVvDOZg6u6
                YPOSUDVvyofCGcICLqUOG+qITYVucyIWgZtHZUb49dpG
                aJTAdVKlOTbYV9sbmHNuMuGt+1/rc+StsjTPTHU=
                ) ; key id = 40400
example.tld.        86400 IN DNSKEY   257 3 7 (
                AwEAAa2BE0dAvMs0pe2f+D6HaCyiFSHw47BA82YGs7Sj
                qSqH3MprNra9/4S0aV6SSqHM3iYZt5NRQNTNTRzkE18e
                3j9AGV8JA+xbEow74n0eu33phoxq7rOpd/N1GpCrxUsG
                kK4PDkm+R0hhfufe1ZOSoiZUV7y8OVGFB+cmaVb7sYqB
                RxeWPi1Z6Fj1/5oKwB6Zqbs7s7pmxl/GcjTvdQkMFtOQ
                AFGqaaSxVrisjq7H3nUj4hJIJ+SStZ59qfW3rO7+Eqgo
                1aDYaz+jFHZ+nTc/os4Z51eMWsZPYRnPRJG2EjJmkBrJ
                huZ9x0qnjEjUPAcUgMVqTo3hkRv0D24I10LAVQLETuw/
                QOuWMG1VjybzLbXi5YScwcBDAgtEpsQA9o7u6VC00DGh
                +2+4RmgrQ7mQ5A9MwhglVPaNXKuI6sEGlWripgTwm425
                JFv2tGHROS55Hxx06A416MtxBpSEaPMYUs6jSIyf9cjB
                BMV24OjkCxdz29zi+OyUyHwirW51BFSaOQuzaRiOsovM
                NSEgKWLwzwsQ5cVJBEMw89c2V0sHa4yuI5rr79msRgZT
                KCD7wa1Hyp7s/r+ylHhjpqrZwViOPU7tAGZ3IkkJ2SMI
                e/h+FGiwXXhr769EHbVE/PqvdbpcsgsDqFu0K2oqY70u
                SxnsLB8uVKYlzjG+UIoQzefBluQl
                ) ; key id = 62910

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Wed Nov 27 18:18:30 2013
;; MSG SIZE  rcvd: 839

Check for the presence of RRSIG records.

dig A example.tld. @localhost +noadditional +dnssec +multiline
; <<>> DiG 9.8.4-rpz2+rl005.12-P1 <<>> A example.tld. @localhost +noadditional +dnssec +multiline
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 32902
;; flags: qr aa rd; QUERY: 1, ANSWER: 2, AUTHORITY: 3, ADDITIONAL: 5
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 4096
;; QUESTION SECTION:
;example.tld.         IN A

;; ANSWER SECTION:
example.tld.          86400 IN A 93.184.216.119
example.tld.          86400 IN RRSIG A 7 2 86400 20131227171405 (
                            20131127171405 40400 example.tld.
                            JCoL8L7As1a8CXnx1W62O94eQl6zvVQ3prtNK7BWIW9O
                            lir/4V+a6c+0tbt4z4lhgmb0sb+qdvqRnlI7CydaSZDb
                            hlrJA93fHqFqNXw084YD1gWC+M8m3ewbobiZgBUh5W66
                            1hsVjWZGvvQL+HmobuSvsF8WBMAFgJgYLg0YzBAvwHIk
                            886be6vbNeAltvPl9I+tjllXkMK5dReMH40ulgKo+Cwb
                            xNQ+RfHhCQIwKgyvL1JGuHB125rdEQEVnMy26bDcC9R+
                            qJNYj751CEUZxEEGI9cZkD44oHwDvPgF16hpNZGUdo8P
                            GtuH4JwP3hDIpNtGTsQrFWYWL5pUuuQRwA== )

;; AUTHORITY SECTION:
example.tld.          86400 IN NS ns1.example.tld.
example.tld.          86400 IN NS ns2.example.tld.
example.tld.          86400 IN RRSIG NS 7 2 86400 20131227171405 (
                            20131127171405 40400 example.tld.
                            hEGzNvKnc3sXkiQKo9/+ylU5WSFWudbUc3PAZvFMjyRA
                            j7dzcVwM5oArK5eXJ8/77CxL3rfwGvi4LJzPQjw2xvDI
                            oVKei2GJNYekU38XUwzSMrA9hnkremX/KoT4Wd0K1NPy
                            giaBgyyGR+PT3jIP95Ud6J0YS3+zg60Zmr9iQPBifH3p
                            QrvvY3OjXWYL1FKBK9+rJcwzlsSslbmj8ndL1OBKPEX3
                            psSwneMAE4PqSgbcWtGlzySdmJLKqbI1oB+d3I3bVWRJ
                            4F6CpIRRCb53pqLvxWQw/NXyVefNTX8CwOb/uanCCMH8
                            wTYkCS3APl/hu20Y4R5f6xyt8JZx3zkZEQ== )

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Thu Nov 28 00:01:06 2013
;; MSG SIZE  rcvd: 1335

The configuration of the primary server is complete.
DNSSEC Secondary Configuration

The secondary servers only require DNSSEC to be enabled and the zone file location to be changed. Edit the main configuration file of BIND.

nano /etc/named.conf

Place these lines inside the options { } section if they don’t exist.

dnssec-enable yes;
dnssec-validation yes;
dnssec-lookaside auto;

Edit the file option inside the zone { } section.

zone "example.tld" IN {
    type secondary;
    file "example.tld.zone.signed";
    masters { 1.1.1.1; };
    allow-notify { 1.1.1.1; };
};

Reload the BIND service.

service named reload

Check if there is a new .signed zone file.

[root@ns2 ~]# ls -l /var/lib/named/secondary/
total 16
-rw-r--r-- 1 named named  472 Nov 27 17:25 example.tld.zone
-rw-r--r-- 1 named named 9180 Nov 27 18:29 example.tld.zone.signed

Voila! That’s it. Just to make sure things are working as they should ,query the DNSKEY using dig as mentioned in the previous section.
Configure DS records with the registrar

When we ran the dnssec-signzone command apart from the .signed zone file, a file named dsset-example.tld was also created, this contains the DS records.

root@ns1:/var/cache/bind# cat dsset-example.tld.
example.tld.        IN DS 62910 7 1 1D6AC75083F3CEC31861993E325E0EEC7E97D1DD
example.tld.        IN DS 62910 7 2 198303E265A856DE8FE6330EDB5AA76F3537C10783151AEF3577859F FFC3F59D

These have to be entered in your domain registrar’s control panel. The screenshots below will illustrate the steps on GoDaddy.

Login to your domain registrar’s control panel, choose your domain, and select the option to manage DS records. GoDaddy’s control panel looks like this.

GoDaddy's Domain control panel

Here is a breakup of the data in the dsset-example.tld. file.
DS record 1:

Key tag: 62910
Algorithm: 7
Digest Type: 1
Digest: 1D6AC75083F3CEC31861993E325E0EEC7E97D1DD

DS record 1
DS record 2:

Key tag: 62910
Algorithm: 7
Digest Type: 2
Digest: 198303E265A856DE8FE6330EDB5AA76F3537C10783151AEF3577859FFFC3F59D

DS record 2

The second DS record in the dsset-example.tld. file had a space in the digest, but when entering it in the form you should omit it. Click Next, click Finish and Save the records.

It’ll take a few minutes for these changes to be saved. To check if the DS records have been created query the nameservers of your TLD. Instead of finding the TLD’s nameservers we can do a dig +trace which is much simpler.

root@ns1:~# dig +trace +noadditional DS example.tld. @8.8.8.8 | grep DS
; <<>> DiG 9.8.2rc1-RedHat-9.8.2-0.17.rc1.el6_4.6 <<>> +trace +noadditional DS example.tld. @8.8.8.8
example.tld.          86400   IN      DS      62910 7 2 198303E265A856DE8FE6330EDB5AA76F3537C10783151AEF3577859F FFC3F59D
example.tld.          86400   IN      DS      62910 7 1 1D6AC75083F3CEC31861993E325E0EEC7E97D1DD

Once this is confirmed, we can check if DNSSEC is working fine using any of the following online services.

    http://dnssec-debugger.verisignlabs.com

    http://dnsviz.net/

The first tool is a simple one, while the second gives you a visual representation of things. Here is a screenshot from the first tool.

Notice the lines I’ve marked. The first one mentions the Key tag value (62910) of the DS record while the second one key id (40400) of the DNSKEY record which holds the ZSK (Zone Signing Key).
Modifying Zone Records

Each time you edit the zone by adding or removing records, it has to be signed to make it work. So we will create a script for this so that we don’t have to type long commands every time.

root@ns1# nano /usr/sbin/zonesigner.sh

#!/bin/sh
PDIR=`pwd`
ZONEDIR="/var/cache/bind" #location of your zone files
ZONE=$1
ZONEFILE=$2
DNSSERVICE="bind9" #On CentOS/Fedora replace this with "named"
cd $ZONEDIR
SERIAL=`/usr/sbin/named-checkzone $ZONE $ZONEFILE | egrep -ho '[0-9]{10}'`
sed -i 's/'$SERIAL'/'$(($SERIAL+1))'/' $ZONEFILE
/usr/sbin/dnssec-signzone -A -3 $(head -c 1000 /dev/random | sha1sum | cut -b 1-16) -N increment -o $1 -t $2
service $DNSSERVICE reload
cd $PDIR

Save the file and make it executable.

root@ns1# chmod +x /usr/sbin/zonesigner.sh

Whenever you want to add or remove records, edit the example.tld.zone and NOT the .signed file. This file also takes care of incrementing the serial value, so you needn’t do it each time you edit the file. After editing it run the script by passing the domain name and zone filename as parameters.

root@ns1# zonesigner.sh example.tld example.tld.zone

You do not have to do anything on the secondary nameserver as the incremented serial will ensure the zone if transferred and updated.
Securing the DNSSEC setup from Zone Walking

Zone Walking is a technique used to find all the Resource Records of a zone by querying the NSEC (Next-Secure) record. NSEC3 was released which “hashed” this information using a salt. Recall the dnssec-signzone command in which we specified a -3 option followed by another elaborate command to generate a random string. This is the salt which can be found using the following dig query.

# dig NSEC3PARAM example.tld. @ns1.example.tld. +short
1 0 10 7CBAA916230368F2

All this makes zone walking difficult but not impossible. A determined hacker using rainbow tables can break the hash, though it’ll take a long time. To prevent this we can recompute this salt at regular intervals, which makes a hacker’s attempt futile as there is a new salt before he/she can find the hash with the old salt. Create a cron job to do this for you using the zonesigner.sh script we created previously. If you run the cronjob as root you don’t have to worry about file ownership. Or else make sure the user under whom you’re placing the cron has write permission on the zone directory and read permission on the private keys (Kexample.tld.*.private).

root@ns1:~# crontab -e

0       0       */3     *       *       /usr/sbin/zonesigner.sh example.tld example.tld.zone

This will sign the zone every 3 days and as a result a new salt will be generated. You’ll also receive an email containing the output of the dnssec-signzone command. 
