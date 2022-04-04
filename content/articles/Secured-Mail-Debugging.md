title: Secured Mail and DNS debugging
date: 2020-05-12 09:03
modified: 2022-04-04 10:31
status: published
tags: TLSA, DANE, DNSSEC, SMTP, mail, submissions, IMAP, OPENPGPKEY, DKIMv1
category: HOWTO
summary: How to debug secured e-mail transport and delivery

This article covers DNS-related debugging of a single-host mail server using:
* ISC Bind9 v9.15,
* Postfix v3.4.10-0+deb10u1
* Dovecot v2.3.4.1-5+deb10u1
* Debian 10.3
* Linux v4.19

When setting up DANE, DKIM, and TLSA, several things have to be inserted into DNS records in
proper domain name sequences.

* Top-level FQDN
 * Mail Exchange (MX)
 * Service Announcement (SRV)
 * DANE checking
  * TLSA (\_tcp.example.invalid)
 * DMARC
  * Sender PF (TXT)
  * DKIM
 * AutoDiscover
 * OPENPGPKEY
* Host-specific domain name (\_tcp.mx1.example.invalid)

For the duration of this article, we will be assuming that `example.invalid`
is your domain name that you use with your example
email address `john_doe+localpart@example.invalid`, 

# Top-Level FQDN #

Starting with the top-level `example.invalid` FQDN, we will need several
different types of DNS record (RCODE) types:

* MX
* SRV
* TLSA
* TXT
* OPENPGPKEY

Assuming that our Bind9 zone file settings for example.invalid are in `/etc/bind/named.conf` 
(or whatever that include file containing our `zone` statement ) containing 
our `example.invalid` zone, we look for the `file` option (within 
`zone example.invalid` statement) and use that value containing its filespec path 
to the DNS record file for `example.invalid` zone:

NOTE: If the `type` option within that zone file is NOT of a `master` or `primary` value 
(it might be `slave` or `secondary`, you're on
the wrong server; go upstream toward the master nameserver and work from there.
If you got a `slave` type, you can find the upstream master nameserver by perusing
the `masters` statement in `named.conf` or the `masters` option within its
`zone` statement for its IP address(es) and go SSH over there.

```named
zone IN "example.invalid" {
    type master;
    file "/var/lib/bind/db.example.invalid";
};
```

In this example, we have `/var/lib/bind//db.example.invalid`.  This will be our
sole file to edit for the duration of this article.

## Bumping DNS Serial Number ##

Don't forget to bump the serial no. by an appropriate amount.

Note: Depending on whether you're using a straight sequential bump from zero, a 
date-format bump, or a unix timestamp bump), I recommend using the unix timestamp 
bump method but it is far easier to use the 2020051103 format as May 11, 2020 third 
iteration.  The only hazard of using this date-format serial number is that DNSSEC 
often bumps that serial no. by 40 or 50
(depending on how many DNSSEC keys needs to be resigned within that DNS record file)
hence the safer approach of using unix timestamp as a serial number.

```console
# Total seconds since Unix Epoch (Jan 1, 1970 00:00)
# Works correctly, regardless of your timezone (TZ).
$ date +%s
1589295578
````
I find it easier to insert the following comment into your DNS record file
placed near that serial number:

```dns
$ORIGIN example.invalid.
$TTL 86400
; use `date +%s` command to get latest serial number
example.invalid.        IN SOA  ns1.example.invalid. admin.example.invalid. (
                                1589295578 ; serial, Unix Epoch
                                ;;;; 2020051103 ; serial, date-format
                                1200      ; refresh (20 minutes)
                                180        ; retry (3 minutes)
                                1209600    ; expire (2 week, RFC1912)
                                10800      ; minimum (3 hours)
                                )
```

## Mail Exchange (MX) ##
Most familiar of the DNS RCODEs is `MX`, the mail exchange.

```dns
example.invalid.  IN MX 10 mx1.example.invalid
```

## DMARC ##

DMARC, which stands for Domain-based Message Authentication, Reporting, and Conformance 
is an email protocol; that when published for a domain; controls what happens if a 
message fails authentication tests (i.e. the recipient server can't verify that 
the message's sender is who they say they are). 

A DMARC policy allows a sender to indicate that their messages are protected by SPF and/or DKIM, and tells a receiver what to do if neither of those authentication methods passes – such as junk or reject the message. DMARC removes guesswork from the receiver’s handling of these failed messages, limiting or eliminating the user’s exposure to potentially fraudulent & harmful messages. DMARC also provides a way for the email receiver to report back to the sender about messages that pass and/or fail DMARC evaluation. 

### How does DMARC works ###
DMARC is used in conjunction with SPF and DKIM (the authentication tests we 
mentioned earlier) and these three components work wonders together to 
autenticaticate a message and determine what to do with it. Essentially, 
a sender’s DMARC record instructs a recipient of next steps (e.g., do 
nothing, quarantine the message, or reject it) if suspicious email 
claiming to come from a specific sender is received. Here is how it works:

1. The owner of the domain publishes a DMARC DNS Record at their DNS 
hosting company.
2. When an email is sent by the domain (or someone spoofing the domain), the 
recipient mail server checks to see if the domain has a DMARC record.
3. The mail server then performs DKIM and SPF authentication and alignment 
tests to verify if the sender is really the domain it says it is.

    Does the message have a proper DKIM-Signature that validates?
    Does the sender's IP address match authorized senders in the SPF record?
    Do the message headers pass domain alignment tests?
4. With the DKIM & SPF results, the mail server is then ready to apply the 
sending domain's DMARC policy. This policy basically says:

    Should I quarantine, reject, or do nothing to the message if the message has failed DKIM/SPF tests?
5. Lastly, after determining what to do with the message, the receiving mail 
server (think Gmail) will send a report on the outcome of this message and 
all other messages they see from the same domain. Thesse reports are called 
DMARC Aggregate Reports and are sent to the email address or addresses 
specified in the domain's DMARC record.

### DMARC Tags ###
There are a total of 11 tags that can be applied to a DMARC policy. Of those 11, the "v" and "p" tags are required and we strongly recommend the "rua" tag as well in order to receive the reports. Below is a full list of tags that can be added to a DMARC record.

[jtable]
Tag, Description 	 
Version (v), The v tag is required and represents the protocol version. An example is v=DMARC1
Policy (p), The required p tag demonstrates the policy for domain (or requested handling policy). It directs the receiver to report, quarantine, or reject emails that fail authentication checks. Policy options are: 1) None 2) Quarantine or 3) Reject. 
Percentage (pct), This DMARC tag specifies the percentage of email messages subjected to filtering. For example, pct=25 means a quarter of your company’s emails will be filtered by the recipient.
RUA Report Email Address(s) (rua), This optional tag is designed for reporting URI(s) for aggregate data. An rua example is rua=mailto:CUSTOMER@for.example.com.
RUF Report Email Address(s) (ruf), the ruf (like the rua tag) designation is an optional tag. It directs addresses to which message-specific forensic information is to be reported (i.e., comma-separated plain-text list of URIs). An ruf example is ruf=mailto:CUSTOMER@for.example.com. 
Forensic Reporting Options (fo), The FO tag pertains to how forensic reports are created and presented to DMARC users. 
ASPF Tag (aspf), The aspf tag represents alignment mode for SPF. An optional tag aspf=r is a common example of its configuration. 
ADKIM Tag (adkim), the optional adkim (similiar to aspf) tag is the alignment mode for the DKIM protocol. A sample tag is adkim=r. 
Report Format (rf), Forensic reporting format(s) is declared by the DMARC rf tag. 
Report Interval (ri), The ri tag corresponds to the aggregate reporting interval and provides DMARC feedback for the outlined criteria. 
Subdomain Policy (sp), This tag represents the requested handling policy for subdomains.
[/jtable]

```dns
$ORIGIN example.invalid.
_dmarc   TXT "v=DMARC1; p=reject; pct=100; sp=reject; adkim=s; aspf=s; fo=1; ri=86400; rua=mailto:admin+dmarc@example.invalid; ruf=mailto:netsoc+dmarc@example.invalid"
```


## Sender Policy Filter (SPF) TXT ##

Next familiar of the DNS RCODEs is `TXT`, the TEXT record.  We store
text-oriented information into the DNS records using TXT RCODE.

Sender Policy Filter is one such information that we need to store in TXT RCODE.

```dns
example.invalid.  IN TXT  v=spf1 a -all
```

Testing this SPF intensively can be done online [in MxToolbox.com](https://mxtoolbox.com/spf.aspx) which will validate your SPF against the Internet and produce results in easy to read format comprising of green indicators (pass) or yellow/red indicators (warn/fail).

## DKIMC ##

After installing opendkim package and getting the domain up and running, another
TXT record is needed to provide the DKIM key to
`mail._domainkey.example.invalid`.

To create a DKIMv1 DNS record, execute:

```bash
opendkim-genkey -s mail -d example.invalid
```
And copy the following resulting but newly-created `mail.txt` file into your DNS record file.

```dns
;
; Made with 'opendkim-genkey -s mail -d example.invalid' command
;
$ORIGIN example.invalid.
mail._domainkey         IN      TXT     ( "v=DKIM1; h=sha256; k=rsa; "
          "p=f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0"
          "f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0F0f0" )  ; ----- DKIM key mail for example.invalid
```

## Service Announcement ##
To announce services as being available on your `example.invalid` server, we
will need the following SRV RCODEs:

* \_imaps.example.invalid
* \_submission.example.invalid
* \_submissions.example.invalid

```dns
$ORIGIN mx1.example.invalid.
_imap._tcp           SRV   0 0 0     . 
_imaps._tcp          SRV   0 1 993   mx1.example.invalid
_pop3._tcp           SRV   0 0 0     . 
_pop3s._tcp          SRV   0 0 0     .
_submission._tcp     SRV   0 1 587   mx1.example.invalid
_submissions._tcp    SRV   0 1 465   mx1.example.invalid
```


## TLSA DNS Records ##

Several DNS records with TLSA RCODE are required in your TLD (e.g. `example.invalid`):

* \_25.\_tcp.example.invalid.
* \_465.\_tcp.example.invalid.
* \_587.\_tcp.example.invalid.

```dns
$ORIGIN example.invalid.
; smtp          25/tcp          mail
_25._tcp.mx1 IN TLSA 3 1 1 f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0

; submissions   465/tcp         ssmtp smtps urd # Submission over TLS [RFC8314]
_465._tcp.mx1 IN TLSA 3 1 1 f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0

; submission    587/tcp                         # Submission [RFC4409]
_587._tcp.mx1 IN TLSA 3 1 1 f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0
```


## AutoDiscover ##

Auto-discover assists mail clients (Outlook, Mozilla Thunderbird, mutt) with
configuration of your account by using just the `example.invalid` domain name
and your username.

To support this, add the following hostnames:

* autodiscover.example.invalid (HTTP used by mail client autodiscovery)
* imap.example.invalid  (used by dovecot)
* smtp.example.invalid  (used by smtp, submission, submissions)

```dns
$ORIGIN example.invalid.
smtp           CNAME ns1.example.invalid
imap           CNAME ns1.example.invalid

; Serve autodiscover.php in autodiscover.example.invalid/
autodiscover   CNAME ns1.example.invalid

_autodiscover._tcp   SRV   0 1 443   ns1.example.invalid

example.invalid.		83640	IN	TXT	"mailconf=https://example.invalid/.well-known/autoconfig/mail/config-v1.1.xml"


```

Create the XML file for auto-discovery using this 
[web template tool](https://help.directadmin.com/item.php?id=661).

## OPENPGPKEY ##

To take advantage of the OPENPGPKEY record, your domain MUST BE fully secured
by DNSSEC.  To determine whether or not your FQDN is DNSSEC-verified or not,
execute:
```bash
delv example.invalid openpgpkey
```
In the first line output from `delv` utility, fully DNSSEC-verified if says one
of the following lines:
```shell
; fully validated
; negative response, fully validated
```

Once your FQDN is DNSSEC-secured, to make available your PGP signing key on DNS, 
install `openpgpkey` on the host machine where your GNU-PG keyring is located at:

```bash
gpg --list-keys
```
If the `echo $?` returns a zero error code status confirming that your key
ring has been created.  Check that your email address is in the keyring before
proceeding; otherwise create a new PGP key.

NOTE: If you do not want to install `openpgpkey` package, then use this [web
online OPENPGPKEY generator](https://www.huque.com/bin/openpgpkey) and skip the
rest of this subsection.

At the keyring workstation/host, install the `openpgpkey` package:
```bash
git clone https://github.com/letoams/hash-slinger.git
cd hash-slinger
```

From the list of keys, note your email address that you wish to DNS publish.
```bash
./openpgpkey john_doe+localpart@example.invalid
```
then take the content of its output file and insert it into your DNS record file.

```console
$ ./openpgpkey --create john_doe+localpart@example.invalid
; keyid: FBF2B4F78FD23A68
Fd4b41c9db9172e5f151e4a5fe3c57ca3f98b8e6ba807450b10d1897._openpgpkey.example.invalid. IN OPENPGPKEY FQENBFnVAMgBCADWXo3I9Vig02zCR8WzGVN4FUrexZh9OdVSjOeSSmXPH6V5+sWRfgSvtUp77IWQtZU810EI4GgcEzg30SEdLBSYZAt/lRWSpcQWnql4LvPgoMqU+/+WUxFdnbIDGCMEwWzF2NtQwl4r/ot/q5SHoaA4AGtDarjA1pbTBxza/xh6VRQLl5vhWRXKslh/Tm4NEBD16Z9gZ1CQ7YlAU5Mg5Io4ghOnxWZCGJHV5BVQTrzzozyILny3e48dIwXJKgcFt/DhE+L9JTrO4cYtkG49k7a5biMiYhKhLK3nvi5diyPyHYQfUaD5jO5Rfcgwk7L4LFinVmNllqL1mgoxadpgPE8xABEBAAG0MUpvaGFubmVzIFdlYmVyIChPTkxZLVRFU1QpIDxqb2hhbm5lc0B3ZWJlcmRucy5kZT6JATgEEwECACIFAlnVAMgCGwMGCwkIBwMCBhUIAgkKCwQWAgMBAh4BAheAAAoJEOvytPeP0jpogccH/1IQNza/JPiQRFLWwzz1mxOSgRgubkOw+XgXAtvIGHQOF6/ZadQ8rNrMb3D+dS4bTkwpFemY59Bm3n12Ve2Wv2AdN8nK1KLClA9cP8380CT53+zygV+mGfoRBLRO0i4QmW3mI6yg7T2E+U20j/i9IT1KATg4oIIgLn2bSpxRtuSp6aJ2q91Y/lne7Af7KbKq/MirEDeSPrjMYxK9D74EABLs4Ab4Rebg3sUga037yTOCYDpRv2xkyARoXMWYlRqME/in7aBtfo/fduJGqu2RlND4inQmV75V+s4/x9u+7UlyFIMbWX2rtdWHsO/t4sCP1hhTZxz7kvK71ZqLj9hVjdW5AQ0EWdUAyAEIAKxTR0AcpiDm4r4Zt/qGD9P9jasNR0qkoHjr9tmkaW34Lx7wNTDbSYQwn+WFzoT1rxbpge+IpjMn5KabHc0vh13vO1zdxvc0LSydhjMI1Gfey+rsQxhT4p5TbvKpsWiNykSNryl1LRgRvcWMnxvYfxdyqIF23+3pgMipXlfJHX4SoAuPn4Bra84y0ziljrptWf4U78+QonX9dwwZ/SCrSPfQrGwpQcHSbbxZvxmgxeweHuAEhUGVuwkFsNBSk4NSi+7Y1p0/oD7tEM17WjnONuoGCFh1anTS7+LE0f3Mp0A74GeJvnkgdnPHJwcZpBf5Jf1/6Nw/tJpYiP9vFu1nF9EAEQEAAYkBHwQYAQIACQUCWdUAyAIbDAAKCRDr8rT3j9I6aDZrB/9j2sgCohhDBr/Yzxlg3OmRwnvJlHjs//57XV99ssWAg142HxMQt87s/AXpIuKHtupEAClN/knrmKubO3JUkoi3zCDkFkSgrH2Mos75KQbspUtmzwVeGiYSNqyGpEzh5UWYuigYx1/a5pf3EhXCVVybIJwxDEo6sKZwYe6CRe5fQpY6eqZNKjkl4xDogTMpsrty3snjZHOsQYlTlFWFsm1KA43Mnaj7Pfn35+8bBeNSgiS8R+ELf66Ymcl9YHWHHTXjs+DvsrimYbs1GXOyuu3tHfKlZH19ZevXbycpp4UFWsOkSxsb3CZRnPxuz+NjZrOk3UNI6RxlaeuAQOBEow50
```

# Testing DNS Records #

Now to test all the DNS records, we reload the nameservers.  

Note: Of course, do not forget to bump the serial number ... firstly.

## Testing DNS MX Record ##
A simple lookup can test that this DNS record exist:

```console
$ dig example.invalid. IN MX

; <<>> DiG 9.17.1-dev <<>> example.invalid. in mx
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 55190
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;example.invalid.			IN	MX

;; ANSWER SECTION:
example.invalid.		86400	IN	MX	10 mx1.example.invalid.

;; Query time: 759 msec
;; SERVER: 64.20.34.50#53(64.20.34.50)
;; WHEN: Tue May 12 10:31:04 EDT 2020
;; MSG SIZE  rcvd: 59
```
The `ANSWER SECTION` correctly shows the exact mailserver
(`mx1.example.invalid`) used for the `example.invalid` domain part of your email
address.

## Testing DNS TXT Record for DMARC ##

```console
$ delv @ns1.example.invalid example.invalid txt
; fully validated
_dmarc.example.invalid  83640   IN  TXT "v=DMARC1; p=reject; pct=100; sp=reject; adkim=s; aspf=s; fo=1; ri=86400; rua=mailto:admin+dmarc@example.invalid; ruf=mailto:netsoc+dmarc@example.invalid"
```

## Testing DNS TXT Record for SPF ##

```console
$ delv @ns1.example.invalid example.invalid txt
; fully validated
example.invalid.		83640	IN	TXT	"v=spf1 a -all"
```

## Testing DNS TXT Record for DKIMv1 ##

```console
$ delv @ns1.example.invalid mail._domainkey.example.invalid. TXT
; fully validated
mail._domainkey.example.invalid. 86033 IN	TXT	"v=DKIM1; h=sha256; k=rsa; " "p=F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0" "F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0"
```

## Testing DNS SRV Records ##
Make sure that all SRV records point toward your MX record (as shown in 
the first MX test above):

For secured IMAP4 service:
```console
$ delv @ns1.example.invalid _imaps._tcp.mx1.example.invalid. SRV
; fully validated
_imaps._tcp.mx1.example.invalid. 5832 IN	SRV	1 1 993 mx1.example.invalid.
```

For unsecured IMAP4 service:
```console
$ delv @ns1.example.invalid _imap._tcp.mx1.example.invalid. SRV
; fully validated
_imap._tcp.mx1.example.invalid. 77205 IN	SRV	0 0 0 .
```

For unsecured POP3 service:
```console
$ delv @ns1.example.invalid _pop3._tcp.mx1.example.invalid. SRV
; fully validated
_pop3._tcp.mx1.example.invalid. 44259 IN	SRV	0 0 0 .
```

For secured POP3 service:
```console
$ delv @ns1.example.invalid _pop3s._tcp.mx1.example.invalid. SRV
; fully validated
_pop3s._tcp.mx1.example.invalid. 44333 IN	SRV	0 0 0 .
```

For unsecured SMTP submission service:
```console
# delv @ns1.example.invalid _submission._tcp.mx1.example.invalid. SRV
; fully validated
_submission._tcp.mx1.example.invalid. 77970 IN SRV	1 1 587 mx1.example.invalid.
```

For secured SMTP submission service:
```console
# delv @ns1.example.invalid _submissions._tcp.mx1.example.invalid. SRV
; fully validated
_submissions._tcp.mx1.example.invalid. 44157	IN SRV	1 1 465 mx1.example.invalid.
```

## Testing DNS OPENPGPKEY Record ##
```console
$ delv @ns1.example.invalid 4dcde9487da4c49a8d2d8af51a70f5ce59af1f202c5b8297be203cb8._openpgpkey.example.invalid. openpgpkey
; fully validated
4dcde9487da4c49a8d2d8af51a70f5ce59af1f202c5b8297be203cb8._openpgpkey.example.invalid. 85493 IN OPENPGPKEY Z3BnOiBXQVJOSU5HOiBub3RoaW5nIGV4cG9ydGVkCg==
```

## Testing Auto-Discover ##

```console
# delv @ns1.example.invalid _submissions._tcp.mx1.example.invalid. SRV
; fully validated
_submissions._tcp.mx1.example.invalid. 44157	IN SRV	1 1 465 mx1.example.invalid.
```

## Testing DNS OPENPGPKEY Record ##

```console
# delv @ns1.example.invalid f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0._openpgpkey.example.invalid. in openpgpkey
; fully validated
f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0._openpgpkey.example.invalid. 85615 IN OPENPGPKEY Z3BnOiBXQVJOSU5HOiBub3RoaW5nIGV4cG9ydGVkCg==
```

# External References #

* [DMARC FAQ](https://dmarc.org/wiki/FAQ)
* [DMARC Detailed Overview](https://dmarc.org/overview/)
* [RFC7489 Domain-based Message Authentication, Reporting, and Conformance (DMARC)](https://tools.ietf.org/html/rfc7489)
* [Verify a DANE TLSA record](https://check.sidnlabs.nl/dane/)
* [How does DMARC works](https://mxtoolbox.com/dmarc/details/what-is-dmarc)
* [Generate DNS OPENPGPKEY Record](https://www.huque.com/bin/openpgpkey)

