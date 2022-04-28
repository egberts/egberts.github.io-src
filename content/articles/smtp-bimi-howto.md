title: HOWTO BIMI-fy Your Domain
date: 2022-04-14 11:13
status: published
tags: BIMI, SMTP, mail, SPF, DMARC, DKIM
category: HOWTO
summary: I needed to create a TinySVG v1.2 image file for use with BIMI.  BIMI stands for Brand Indicator for Message Notification. BIMI allows adding your own logo to email messages that your mail server sends.  Recipients who use BIMI-friendly email clients will see your logo next to messages sent by your mail server.
slug: smtp-bimi-howto
lang: en
private: False

So your mail server is up and running?  People who received your emails compliment you?  Pat yourself on the back.  This is just the beginning.

One recipient may comment to you that a logo is missing next to your sent-email on their phone-based mail clients.  You've spent 35 years of digesting some 400-off IETF Request For Comments (RFCs) and its drafts, countless of SMTP specifications, and many onerous hidden protocol tweaks by various mail client vendors, you say "WHAT? What dastardly new feature is it this time?  This logo next to my emails?".

BIMI, stands for Brand Indicator for Message Notification. It has been percolating around since 2017 and officially appeared in ([2018 IETF Draft](https://datatracker.ietf.org/doc/html/draft-chuang-bimi-certificate-00)).

BIMI is now being used entirely by certain Mail User Agents (MUA, that is, mail clients apps and webmails).  Google Mail (Android/iPhone/Web-based) client app/webmail and Apple Mail client app both make use of their own BIMI logo; so does Fastmail and Yahoo! webmail providers.

Of course, BIMI has nothing to do with your mail server (MTA); it's all about the billions of mail client apps (MUA) and webmails out there viewing your chosen logo placed next to your sent emails.

The thing about having a BIMI for your own domain is, you have to jump precariously through many hoops to get this logo BIMI images of yours working ... perfectly (and spend quite a bit of $$$).  

And this article will show you how to do this BIMI.  And without making use of expensive Adobe Acrobat tools or stumbling over various HOWTOs and to generate the PKI certificates, to have a working BIMI without shoveling a shitload of money toward CA registry ... each year.

You can replace the `example.test.` with your domain name in question.

Also replace the `ns1.example.test.` with the hostname of your primary (master) name server that holds the original zone file of your domain.


# Security Ramification

There is a security ramification to NOT using this BIMI feature.  Other senders would (not 'may', would) be able to impersonate you.  Ideally, you too will want to be able to disable this BIMI (whether your domain has a mail server or not).

Nevermind the fact that SPF and DKIM can too be impersonated if not properly secured.

If the complexity of using BIMI exceeds your desire, you must at a minimum provide for one BIMI DNS TXT record that tells everyone that your BIMI is "disabled" ... just to prevent others from impersonating you.

The TXT record for a properly disabled BIMI must look like this:
```dns
default._bimi.example.test.  TXT  "v=BIMI1; l=; a=;"
```

Much in the same way as SPF and DKIM being forced as disabled, you would not want other senders to mimic your logo (domain name) in other recipients' mail client apps.

## Validation of BIMI Image
I've seen a BIMI Logo appear next to a sender's email address that CLEARLY do not belong to each other (this is spam).  

Google protects their BIMI logo from being used by spammers by mandating a signed PKI certificate which is embedded inside the BIMI SVG-formatted image file. 

<!-- and have their own Google Mail app check each domain's BIMI for a signed Validate Mark Certificate (PKI) that is found inserting its URL into their BIMI (logo) image.  -->

# Jumping Through Hoops

So, you still want your logo plastered and viewed next to each email that your domain sent?  To do BIMI? For billions of mail clients out there?

Some of the hoops that we have to jump through depend on whether a  mail client support BIMI and how intensely they validate BIMI.

* Select an image file to be your 'logo' (that is to be displayed next to your recipient's viewing of your emails).
* Convert the image file into TinySVG+PKI
* Deploy the BIMI image to your website
* Test the TinySVG image
* Create a TXT record type for BIMI configuration settings.
* Modify a TXT record type for DMARC, if needed
* Test DNS lookup on BIMI and DMARC
* Test logo on various online BIMI testers.
* Test BIMI on Mail client apps

At this writing, the good news is that only Google Mail client app demands the one extra step (that is required) to display any domains' BIMI logo image file.

* Insert your BIMI image and insert inside a signed "VMA-approved" PKI certificate

Before you'd say "TAKE MY MONEY!", Entrust and DigiCert offer to sign just one BIMI image once a year for $999.00 and $1,499.00, respectively.  <!-- Another good thing is that it is only required by the Google mail client app.  -->


## First Step - Select an Image

Obviously, the first step is to select a logo.  A logo that represents your domain name.  There are restrictions on this image file having your logo:

* must be in SVG, WebP, JPG/JPEG, or PNG format.
* must be equally 2-D dimensioned (exactly-squared, even-length sides).
* should not exceed 128KB before conversion to TinySVG. (pixel/color artifact)
* must be less than 28KB after conversion to TinySVG. (some mail clients' requirement)
* should also be suitably viewable after its 4-corner cropped to make a circle-type avatar.


## Convert Image into TinySVG

Send the image through [https://image2svg.com/](https://image2svg.com/).

The name of the saved image file name can be `logo.svg`, `bimi1_logo_corporate_trademark_standard_240x240.svg` or even `a.svg`; whatever makes your boat floats.

Rename the image file as `bimi1_image.svg` as this article's HOWTO.

Save the image file.


## Domain Webserver.

Using your favorite file transfer tool, transfer the TinySVG image file to your domain's webserver.

BIMI image can be stored under any URL path under its domain.

Do not forget file permission setting for this BIMI image file.

Also, the `Content-Security-Policy` of your webserver must allow retrieval of this BIMI image, so be sure to test this retrieval using a web browser.  If in doubt, master the CSP (or check out the overly-restrictive CSP settings that I use, in my articles: [Current HTTP CSP]({filename}http-csp-current.md) and [HTTP Headers]({filename}http-headers.md)).

For this article, the URL of this BIMI logo image file is:

    https://example.test/images/bimi1_image.svg

Use a web browser, go fetch it.  Enjoy your latest handiwork then keep moving.


# BIMI TXT DNS Resource Record

Add a TXT record to your domain's DNS zone file to hold the new BIMI configuration settings.

This is probably the easiest step of all.

It is very much like DMARC and SPF config settings.  

TIME-SAVER: If your domain DNS zone file does not have the required TXT record that is containing your DMARC settings, FULL STOP:  You should stop reading and deploy DMARC first; then resume back here.  DMARC is required to be properly deployed before tinkering with this BIMI.  

If you operate the name server of your domain, locate the text-based DNS zone file having the origin of your domain name, edit the file.  For Bind9 admins, this primary zone file is specified in your domain's `zone` clause `file` statement of `/etc/named.conf` or roughly under `/var/lib/bind/master/` subdirectory.

At any rate, insert the following DNS record into your domain's DNS zone file
```dns
default._bimi	TXT	"v=BIMI1; l=https://example.test/images/bimi1_image.svg; a=;"
```

Save the BIMI record.


## What is this `default._bimi.example.test`

`_bimi` is the designated DNS namespace for all things related to BIMI1 under the domain in question.  Just like `_tcp.`, `_udp.`, `_tls`, and `_openpgpkey`, this `_bimi.` is a DNS namespace under your domain that may serve up additional DNS records under each.

For `_bimi.`, the `default` template name represents the 'BIMI Assertion Record'; it may have the current word 'default' or a 5-digit number namespace; a DNS namespace to contain BIMI1 settings in the form of a TXT RTYPE record.  

NOTE: A 5-digit number helps to support BIMI for 65,535 websites under one domain name (so far, no one appears to be doing this).  Stick with the `default.` for now.



## TXT RTYPE Record for BIMI1 Settings

TXT records has three settings (so far):

* `v=` - BIMI version; so far, it is fixed at '1'.
* `l=` - Location of Image File; a valid URI, HTTPS-only, minimum two locations; CSV
* `a=` - Empty or `self`.  `self` means to actually verify the embedded PKI certificate in the image file before using it.

## TXT Record for DMARC Settings

Now to re-check your `_dmarc.example.test` DNS record.

It is time to change the DMARC mode to `quaratine`.

You probably had a working DMARC setup, and you might have had your DMARC set to "monitoring mode".  BIMI requires that DMARC not be set to `none`.  


```dns
_dmarc.example.test.	86400	TXT	"v=DMARC1; p=quaratine; rua=mailto:dmarc@example.test; fo=1"
```

A short summary, TXT record for DMARC DNS resource type have several settings.

DMARC policy options:
[jtable]
attribute, value, description
`v=`,DMARC1,The `v=DMARC1` property indicates that this DNS record contains a DMARC policy. This must be the first item in the DMARC record.
`p=`,`none`,For emails with `example.test` in the sender address, the receiving server is advised to take no additional action against emails the fail DMARC alignment. This is also known as monitoring only mode.
`sp=`,\<not set\>,"For emails with any subdomain of `example.test` in the sender address, the receiving server is advised to take no additional action against email that fails alignment. This is also known as monitoring only mode."
`adkim=`,`r`,Apply relaxed DKIM alignment. The domain name in the DKIM signature may be any subdomain of `example.test` for DKIM to be aligned.
`aspf=`,`r`,Apply relaxed SPF alignment. The domain name in the email From header may be any subdomain of `example.test` for the SPF to be aligned.
`pct=`,`100`,The DMARC policy defined in p and/or sp should be applied to 100% of emails that fail DMARC alignment.
[/jtable]

Aggregate reporting options:
[jtable]
attribute, value, description
`rua=`,mailto:dmarc@example.test`, Request the receiver to send aggregate reports to dmarc@example.test`.
`ri=`,`86400`,The interval requested between aggregate reports (send to the rua address, if set) in seconds. 86400 seconds equals 1 day.
[/jtable]

Failure (forensic) reporting options:
[jtable]
attribute, value, description
`ruf=`,\<not set\>,Failure reporting is not enabled.
`fo=`,`1`,Request failure reporting (send to the ruf address, if set) if an email fails either SPF or DKIM alignment.
`rf=`,`afrf`,Request failure reporting (send to the ruf address, if set) to be sent in the [AFRF (RFC6591)](https://www.rfc-editor.org/rfc/rfc6591.html) format.
[/jtable]

Further DMARC settings and its attributes are detailed in [DMARCanalyzer.com/how-to-create-a-dmarc-record](https://www.dmarcanalyzer.com/how-to-create-a-dmarc-record/)


## Test the DNS Records

Just before exiting that `$EDITOR` session of your `example.test` zone file, do not forget to bump up the serial number found in that domain's `SOA` record (near the beginning of the file).

Then reload (or restart) your name server daemon.

Recap:  `default._bimi.example.test` is the FQDN of this BIMI TXT record.  One of the TXT records will be the set of BIMI1 settings and also point to a web server containing your BIMI image.

Recap:  `_dmarc.example.test` is the FQDN of this DMARC TXT record.  TXT record will describe how SPF and DKIM are to be enforced.

Check out the newly created BIMI TXT record.

### Unsecured DNS Query

In examples below, replace the `ns1.example.test` with your domain's authoritative (DNS) name server.

```console
$ nslookup -query=TXT default._bimi.example.test.  ns1.example.test.
$ dig @ns1.example.test default._bimi.example.test. TXT
```

Condensed output should have following relevant details:
```dns
default._bimi.example.test. TXT	"v=BIMI1; l=https://example.test/images/bimi1_image.svg; a=;"
```

### Secured DNS Query - BIMI

I too shall assume that you have a working DNSSEC properly set up for your domain.

ISC has a good `nslookup`/`dig` replacement tool for checking out your DNSSEC called `delv`.  `delv` can be found in the `dnsutils` Debian package.

To check whether your domain has adequate DNSSEC cover, examine the very first line out of `devl`.  The first line can be either:
```console
; fully validated

or

; unsigned answer
```

`; fully validated` means that your domain demonstrated par excellence.
`; unsigned answer` is a muted way of saying, nothing you have read so far will be safe from any imposters of this domain.

Check out BIMI1 TXT using `delv`.

```console
$ delv  @ns1.example.test.  default._bimi.example.test.  TXT
; fully validated
default._bimi.example.test. 85798	IN	TXT	"v=BIMI1; l=https://example.test/images/bimi1_image.svg; a=;"
default._bimi.example.test. 85798	IN	RRSIG	TXT 8 4 86400 20220428212555 20220414170603 58791 example.test. <snipped zone base64 text>==
```

Ignore the DNSSEC overhead `RRSIG` record, that is a part of DNSSEC.  

We got our TXT record and it looks good.

### Secured DNS Query - DMARC

Last check is your updated DMARC TXT.  (You did change it from `none` to `quaratine`?)

```console
$ delv @ns1.example.test.  _dmarc.example.test.  TXT
; fully validated
_dmarc.example.test.	TXT	"v=DMARC1; p=quaratine; rua=mailto:dmarc@example.test; fo=1"
<snipped RRSIG line>
```

Note: The storage of mail-related TXT record is different for SPF, DKIM, DMARC, STS, and BIMI:

[jtable]
Type, FQDN
SPF, `example.test`
DKIM, `_domainkey.example.test`
DMARC, `_dmarc.example.test`
STS, `_mta-sts.example.test`
BIMI, `default._bimi.example.test`
[/jtable]


## Real World Test of BIMI 

A BIMI online tester can check out the BIMI setup for your domain.  There are several BIMI online testers:

* [EasyDMARC](https://easydmarc.com/tools/bimi-lookup) (best)
* [MailHardener](https://www.mailhardener.com/tools/bimi-validator)
* [BIMI Group](https://bimigroup.org/bimi-generator/) (very good)
* [Mailkit](https://www.mailkit.com/resources/bimi-inspector/)
* mxtoolbox.com

# In Closing

After passing your DNS record lookup and BIMI online testers, your domain should be very very safe from any imposter.


# References

* [BIMI - IETF RFC Rough Draft](https://tools.ietf.org/id/draft-blank-ietf-bimi-00.html)
* [Convert PNG/JPG/JPEG/WEBP to TinySVG](https://image2svg.com/)
* [SVG Tiny v1.2](https://www.w3.org/TR/SVGTiny12/)
* [Entrust Verified Mark Certificate](https://go.entrust.com/vmc-order-form)
* [DigiCert Verified Mark Certificate](https://order.digicert.com/step1/vmc_basic)
* [BrandIndicatorForMessageIdentification OID](http://oid-info.com/get/1.3.6.1.5.5.7.3.31)
* [id-pe-logotype OID](https://datatracker.ietf.org/doc/html/rfc3709#section-4.1)
* [Issuance of VMC v1.1](https://bimigroup.org/resources/2021-09-01-VMC_Guidelines_latest.pdf)
* [VMC Guidelines v.1.1](https://bimigroup.org/resources/2021-10-08-VMC_Guidelines_latest.pdf)
* [BIMI TinySVG Schema](https://bimigroup.org/resources/SVG_PS-latest.rnc.txt)
* [IETF Draft BIMI - Chuang](https://datatracker.ietf.org/doc/html/draft-chuang-bimi-certificate-00)
