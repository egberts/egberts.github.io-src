title: Current State with Private Subnets and DNSSEC
date: 2022-05-08 06:42
status: published
tags: DNSSEC, Bind9, DNS
category: HOWTO
summary: What's the current situation of DNSSEC and private subnets?
slug: dns-dnssec-private
lang: en
private: False

It would seem like a good thing for administrators of private LAN (e.g., an enterprise or a homelab) to set up DNSSEC for their private subnets or 
even private top-level domain names.

But the story of DNSSEC for private LAN uses is that this concept is far from deployable and
does not bode well for its struggling but continuing adoption rate of DNSSEC.

In 2017 and 2018, the DNSSEC adoption rate measured by APNIC.NET actually [declined](https://blog.apnic.net/2019/03/14/the-state-of-dnssec-validation/).  Although, its adoption rate is still slowly climbing, but still way [too slow](https://blog.apnic.net/2020/03/02/dnssec-validation-revisited/).

Even Tony Finch and Evan Hunts discussed this ['private local DNSSEC'](https://fanf.dreamwidth.org/125531.html) for
enterprise (and implicitly last-mile use such as HomeLab) usage.

Here is a good recap of what Tony (and most of us) wanted:

```
I want:

    Support for DNS zone transfers over TLS

    Validation of zone contents after transfer, and 
    automatic retransfer to recover from corrupted 
    zones

    A localized DLV to act as an enterprise trust 
    anchor distribution mechanism
```

It is this last point that nearly all (except for probably ISP) DNS admins wanted.  
Noticed that we got the first one in form of DNS-over-HTTPS (DoH) and 
DNS-over-TLS (DoT).  IMHO:  DoT has better overall security but
DoH has easier adoption rate.

Second item is an ongoing state of integration.

So what's the current state of affair ... after 5 years ... for the third wishlist item covering this local private DNSSEC?

This article covers the bowel of the DNS validators found in both DNS nameservers (authoritative and resolvers) and most hosts' resolver mechanims in details.

# Current State

So far, DLV for Root has been [removed from](https://kb.isc.org/docs/aa-01310) Bind v9.16.  But no 
suitable replacement is on the horizon as far as we can see.
Not even the latest Bind 9.20 has anything closely resembling this DNSSEC lookaside validation.

In the latest Bind 9.16+, there is this new `trust-anchors` clause.

`trust-anchors` clause is only a general overall setting.  
I might even add that this option is nearly useless outside of the 13 
Root DNS (unless you're 
into erecting a thin veil of querying privacy by doing this 'in-house').

Take, for example, the [`.test`](https://www.rfc-editor.org/rfc/rfc2606.html) (or even the newly created [`home.arpa`](https://datatracker.ietf.org/doc/html/rfc8375) domain that is available for 
anyone to use: DNSSEC would not YET work in those 'private' zone trees.

How did DNSSEC ever stop working on those 'private' zone trees? It didn't
ever stop working; just that it was never workable for a private LAN (enterprise/homelab) in the first place.  

DNSSEC is designed such that the chaining of valid public-keys over each name 
part of the FQDN is going from the top of the zone (`.`) downward to the 
bottom (your hostname) zone; unbroken links of a verifiable chain.

To support this public-key chaining, each maintainer of its 
downward zone name (`myhomelab` in `myhomelan.mydomain.example.com`) must 
submit a DS RR containing the public key of your `myhomelab` zone 
to the higher owner of `mydomain.example.com.`.  

Of course, if you own both the `mydomain` as well as `myhomelan`, 
then it is not a problem to make `myhomelab`
DNSSEC valid, EXCEPT that you must continue to support the validating of the chain 
linkages toward higher zone names, as this what current DNS validators (resolvers and nameservers) do.
As a domain owner, you must repeat the same `DS` RR delivery for each
zone name until you no longer own that zone name, which is 
invariably always its TLD or someone else's zone (domain) name.

The next chain link is the DS RR of `mydomain` zone must be sent 
to the TLD admin of `example` zone.  Ad naseum, but not quite ad infinitium.

# MyDomain, MyChoice

Execuse the ripped-off slogan: my domain, my choice;
it should be possible to deploy DNSSEC throughout the enteprise, small-medium
businesses and home labs.  But this is not happening ... for private LAN/TLD ... yet.

The idea of continual extension of DNSSEC below your owned `mydomain.tld`
is already technically practical, and it is in fact commonly deployed.

However, consider this common story; some top-secret corporate lab does 
not want their DNSSEC to be leaked out onto the net; what can 
a DNS administrator do?

There are a couple of basic choices today:

1. filter out private subdomain
2. split-horizon name servers
3. set up a private top-level domain (TLD)
4. mimic DNSSEC chains

It is painfully evident that the first two choices are not protective enough
alone for the requisite DNSSEC and privacy combined.

The first one requires a separate Bind9 view.  No, this `validate-except { mydomain.tld; };`
statement setting doesn't quite cut the mustard, instead it just 
leaves DNSSEC broken (via un-validated answer).

The second one helps to stem the privacy leakage caused, but one can make interference past this weak privacy veil
if given enough depth the zone names of its hostname.  Sure that `deny-answer-aliases` statement setting may help, but this solves only half of the privacy in the query-answer exchange.  It still breaks the DNSSEC chain.

The third choice isn't even possible with today's DNSSEC validators. 
The closest nameserver vendor to support the DNSSEC of private TLD 
is `hdns` of handshake.org but it still doesn't solve the 
problem of wide-spread acceptance (within
today's constraints of un-obsoleted IETF RFC specifications).

# DNS Validator

So why is today's DNSSEC validators not capable of doing this zone cut
of DNSSEC?  I mean, the validator has this DNS zone cut mechanism. Why
not a DNSSEC zone cut?

## Zone Cut

What is this "zone cut"?  Zone cut is the boundary between
authoritative zones.  It also represents the seeking of
the next authoritative zone.  `SOA` RR is the authoritative DNS record 
for its parent (next) zone name.

Note: Keep in mind, multiple zone names may be served by the 
same authoritative nameserver; `mypersonallab.myhomelab.mydomain.tld`
may have its `myworkstation.mypersonallab.myhomelab.mydomain` all served by
the same but single authoritative nameserver, so a `myworkstation`
could still be zone cut as `mydomain` singularily.

During a zone cut where a nameserver finds its next authoritative zone
up the chain, it takes the `myhomelab.mydomain.tld`
and "zone-cut" the `myhomelab` name off, leaving us with 
just the `mydomain.tld` remaining.  Then the next step
is to find the `SOA` for this new `mydomain.tld`.  In turn, you receive 
an answer containing its nameserver (`NS` RR) for that zone 
name `mydomain`. This is the basic mechanism of a zone cut within
the validator logic of a resolving nameserver.

## DNS Zone Cut

Surely we could have the DNSSEC zone cut in much exactly the same way 
as DNS zone cut, no?

Except that validation is being done with retrieving the
`DS` RR of its parent zone name in addition to query retrieval of
its `SOA` RR answer;  that's now going outside the zone.

The lookup sequence of DNSSEC validator is almost identical to DNS validator
except that it has to go out-of-zone to retrieve the `DS` RR 
from its parent zone's authoritative nameserver before answering anything
about the original zone and its cryptographically-proven validity
(as well as its mere presence of existing or not existing).  

Whereas, DNS validator can claim an early finish before heading onward
to the parent zone and its authoritative nameserving; whereas for each zone,
DNSSEC is stymied by this inherent and immovable design trait of 
consulting a parent authoritative nameserver before even being able to be responding to 
its DNS query.

Because the basic tenet of DNSSEC is to find the DS RR from
its parent zone, this is easy to do for 
`myworkstation.mypersonallab.myhomelab.mydomain` because you 
own all those (sub)zone names and probably can
do all the required DS insertions within your own authoritative
nameserver ... all in one ... zone ... cut.

The problem begins once the zone cut crosses ownership of 
authoritative nameservers, it requires out-of-band cooperation 
(that is outside of DNS protocol to the uninitiated) with the 
nameserver owner of its parent zone to take in your DS public key
of your `mydomain` and then to register 
that DS into its own parent zone database file.

Tedious but common, uh?

## DNSSEC Zone Cut

What if we can have our own DNSSEC-capable TLD or even sub-TLD on top
of the existing DNSSEC trees?  

What if we can pre-validate the parent DS?

We could get the following zones to call our own and have 
it DNSSEC'd based on our own public key.

* `test.`
* `home.`
* `168.192.in-addr.arpa.`
* `16.172.in-addr.arpa.` to `31.172.in-addr.arpa.`
* `10.in-addr.arpa.`
* `whatevermydesiredtldisgoingtobe.`

By having these non-root trust-anchors, we could 
have a controlled set of RFC-compliant DNS resolvers herding 
all the queries from its internal net, and still DNSSEC-validate all
the answers related to the inside.

What needs to change is how the validator logic of an RFC-compliant DNS
 resolver would operate and do this extra step of DNSSEC pre-validation.

Such validator logic needs not to be a (major) design change nor 
a (major) code change; 
it could be a configuration enhancement in the form of a single-logic 
being inserted.

This single logic is the terminator of a chain link and where to
do this break of this loop of the chain links.

Unfortunately, such logic would dictact that the entire chain link
would now have to be done within one resolver context (and not by any
failover resolvers either).  Why?  Because the faking of the remaining
chain link(s) now needs to be done internally and completely finished
by and within this same resolver (so any secondary resolver has to stay
out during that particular query/answer set).

Why is this break of the chain link not really a full-stop break? 

Like in Proof of Work (PoW), which is a cryptocurrency concept, you still
have to validate the entire DNSSEC chain before declaring the crypto-money 
valid.

Arguably, a full-stop break on a sub-TLD domain trusted key by the 
DNSSEC validator chain loop processing would be an OK option for a privately-rolled 
DNS tree, but NEVER as a publicly-available option.  

Until we solve the technical issues of publically-available option, 
we shouldn't even be deploying the private TLD/LAN DNSSEC yet, despite my trekking
the desert for 8 years and the need to quench my parched throat because of
this.

What if I could make this concept available now, using Bind v9.19?
I am going to say just this one thing: 

    DO NOT DO THIS ON THE INTERNET.

Yet I am already doing this internally, behind a firewall that blocks DNS payload via UDP/TCP, behind a transparent Squid proxy whose HTTPS/ICAP is blocking DNS-over-HTTP (but not yet DNS-over-TLS),
behind a NAT, behind a split-tri-horizon DNS, behind an RPZ firewall, 
for a total of some multi-layered DNS craziness and I have 
my own private Root DNSSEC.

It is really an ongoing effort to make a reductive of the current 9 
instances of `named` processes that help me to create a 
fake `168.192.in-addr.arpa` and `home.` zones that works well 
with the real-world of DNSSEC-secured `168.192.in-addr.arpa` and `home.`; 
in other words, I can web browse comfortably, get my 
DNSSEC-validated records for anything on the Internet 
(that is DNSSEC-secured) as well as having all my private DNS and 
its reverse IP also to be all DNSSEC-validated.

Our end-goal should be simple: to have a workstation with DNSSEC validation 
enabled as "absolutely always" that works for home, enterprise and
Internet Cafe.  (Keep in mind, no ISP providers would ever want this).

At the moment, most hosts' resolver is currently set to be as 
"if DNSSEC-secured, then DNSSEC-validated any DNS record; 
if not DNSSEC-secured, then return any DNS answer as-is."

# Where's the Beef?

The key thing here is to modify the resolver's behavior so that
it can do the pre-validating of `DS` record of the parent zone, then
keep pre-validating after each zone cut, and keep pre-validating all the way up to your 
very-own private Root TLD/DNS.  That is about as concise as I can make it.

Pre-validation of the `DS` needs not to be a dynamic on-the-fly thing; you create
the public/private key, insert the public key into the parent zone, 
and repeat this at each zone name until you reach the root zone ... of your own.

Can ISC Bind9 do all this?  Yeah, it currently can.  But I have spread the 
functionality of this concept of a private TLD over many separate processes
of `named` daemon so that I could maintain this duality of private DNSSEC and with the Internet's Root Servers.


# A New Resolve(r)

What if our nameserver(s) were to have its own validator mechanism re-instructed
to take any query request for `mydomain` DS and circumvent (or 
redirect) its tld `SOA` elsewhere ... just for our `mydomain` zone name
and supply a working DS public key 
... instead of going out to the Internet and get it from `tld` zone database?

Such feasibility would massively restart DNSSEC adoption rate at a faster
rate: not only in deployment rate but also in training of general admins
to use complex DNSSEC alongside with the DNSSEC deployment artists.

What are the downsides to doing this DNSSEC-extra-zone-cut?

In chime, the cybersecurity and protocol experts would repeatedly say:

* Man-in-the-Middle (MitM) 
* Faked DNSSEC
* DDoS via DNSSEC

## DNS MitM

Would it surprise you to learn that nearly ALL workstations 
do not make use of DNSSEC?  Even Linux? Probably most IoT too?

Let me stop you there. Do not just be starting the enforcing of DNSSEC in your workstation
by inserting the following settings into your 
`/etc/resolv.conf` file ... yet:

```
edns0 yes
options trust-ad
```

I did warn ya.  The problem there is that there is only about 20% adoption
rate of DNSSEC (by traffic volume) on the Internet.  Your web browsing experience will surely
suffer if you do not heed my warning.

So, why is this a potential MitM for DNSSEC at workstation-level?  It isn't.
It is not even an issue whether the workstation has the option of `only-DNSSEC`,
`also-DNS-validated` or `no-DNSSEC` option.

Think about that:  

* If DNSSEC is (mostly) turned off at nearly every
workstation's resolver, what do you care if DNSSEC is not validated or not? 
It is ignoring DNSSEC completely and still getting to working
websites ... as usual.  It may not the legitimate website you wanted, but hey, you disabled DNS security.

* If your workstation resolver's DNSSEC is `always-enforcing`, 
then you simply would not be able to visit those DNSSEC-protected 
that got hijacked or even any other non-DNSSEC websites;
that's a security feature and a HUGE plus for DNSSEC.  For an practical end-user
experience, not so much.

* If `also-DNS-validated`; you also can still visit other websites who 
are still not using DNSSEC.  End-user experience would still be
the same kind of awesome and perhaps ever more safer so now 
that hijacked DNSSEC websites will get blocked by DNS clients.  There are a few kinks that needs to be worked out that are circumventing this current method, but hey, you getting better form of protection and may still lose your bank account (as opposed to surely lose your bank account if not using DNSSEC at all).

For DNSSEC MitM to succeed, this can only happen if the private key
gets lifted, stolen, pilfered, copied, cloned, recovered, captured, recomputed, or leaked.  

You would still need to tamper with the DNS resolver code on the client-side 
(anyway) but you would still not be able to break the 
server-side DNSSEC (via RFC-compliant DNS protocol).

This means that MitM doesn't get any worse with the rolling out 
this new DNSSEC zone cut of a private subdomain.  I am 
arguing that the security theatre would get better and 
the rollout will go out faster if 
the DNS validator logic got updated to allow this 
new DNSSEC zone cut.

The DNS-related MitM is usually the domain of 
a broken-in/unpatched nameservers or app/libresolv/libresolver 
of workstation; but not the DNSSEC-protocol-layer when it comes to
attempting MitM (at its protocol layer).

In short, DNSSEC is a subset of DNS: to do DNS MitM at protocol-layer 
is hard, but not impossible; to do DNSSEC MitM at protocol-layer is next 
to impossible. Of course this is assuming a deployment of
properly-hardened, currently-patched nameservers.


# Pre-Validated DNSSEC

For the new pre-validation of DNSSEC scenario, you are still required to carefully choose your (remote or not)
resolver, preferably the resolvers that you and yourself maintain and control.
Pre-validated DNSSEC via network protocol is still solely in the
realm of where the zone cut is made; if it is under the fewest
number of authoritative controllers, the better the 
security of its resolver.

In these days and ages, security-conscious people are grabbing 
whatever [public DNS resolvers](https://egbert.net/blog/articles/public-nameservers-with-dnssec-support.html) are out there and using them:  yes, this remains a serious problem.  

Pre-validation is only as secured as how you treat your private key
of your domain name and useable only within the subnet that your authoritative nameserver provides over.

Ideally, you would like that private-key stored inside a 
Hardware Security Module (HSM).

The Internet's Root DNS Servers has an elaborate but heavily audited
procedure for its public/private key generation 
and stores its generated key in a vault and distributed toward 
a PCI-based HSM card at each of the 13 Root nameservers.

The `.com` (and a few others') private key is stored in 
a HSM at VeriSign Lab.  
Most domain registars can happily handle your 
insertion request of your domain's `DS` key into 
VeriSign Lab `.com`  and that is heavily guarded
by their set of strong public/private key combo.

Your private key to `mydomain` is probably and experimentally 
stored as a file in your nameserver's filesystem; most
Fortune-500 businesses probably (or already are)using an HSM PCI card or an HSM USB stick 
for their own domain names.

In DNSSEC protocol level, this is pretty well hardened by the
virtue of its public-key/private-key scheme and its 
security of where each zone-cut private-key is stored at.  

Short of hosting your own nameserver in the cloud/VPS, most of us
start with privacy-invading ISP DNS resolvers.


# Home.Arpa

Let us find out who the owner of `home.arpa.` is: IANA/IAB.
[Wikipedia](https://en.wikipedia.org/wiki/.arpa) says 
'no domain registration is possible'.  A proverbial dead-cat bounce,
right there.  

Why even bother with a RFC4750?  Section 7 says:

    The reason that this delegation must not be 
    signed is that not signing the delegation 
    breaks the DNSSEC chain of trust, which 
    prevents a validating stub resolver from 
    rejecting names published under 'home.arpa.' 
    on a homenet name server.

In short, `home.arpa.` mandates not requiring DNSSEC, 
whereas TLD `.home` requires DNSSEC.  Can we all do an
"eye-roll" together?

Many "talking-cans"/VoIP/cable/ISP providers need to deal with 
many different gateway routers/modem manufacturers
and yet have this consistent domain name.  That is
what their marketing folks are saying, but in reality these 
providers are basically trying to avoid DNSSEC deployment. 
Doesn't bode well for a unified goal of DNSSEC deployment
but, I am going off the rail here a little.



# Upward Chain Validator

What is preventing the DNS vendors from tweaking the upward 
DNSSEC chain validator?

Take for example, the reverse IP of a private IP subnet 192.168.0.0/24:
```nginx
trust-anchors {
    168.192.in-addr.arpa. 99999 8 2 "XXXXXXXXXXXXXXXXXXX ... XXXXX";
    };
```

This `trust-anchors` won't buy you any useful functionality other than 
just to save a query from going out of the network (but it 
remains a good privacy setting to have).

Historical: Bind v9.15.1 introduced a new `trust-anchors` clause
that  had its obsoleted `trusted-keys` and `managed-keys` clauses merged 
together and replaced with.  Also, `dnssec-keys` clause was the 
shortest-lived keyword which got introduced in v9.15.2 and 
quickly obsoleted by 9.15.6.

[jtable]
new, old, description
`trust-anchors` w/ `static-key`, `trusted-keys`,  no key rollover support
`trust-anchors` w/ `initial-key`, `managed-keys`,  automatic key rollover support
`trust-anchors` w/ `initial-ds`, ???, That would make for an excellent DNSSEC-zone-cut candidate, but no.
[/jtable]

`trust-anchors` is not only a top-level clause but can also be found 
within the block of a `view` or a `server` clause.




Still waiting for that other shoe to drop: private local DNSSEC
