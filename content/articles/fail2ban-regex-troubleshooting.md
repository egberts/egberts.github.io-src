title: Troubleshooting Regex in fail2ban during Bind9 DDOS
date: 2020-09-19 11:24
status: published
tags: fail2ban, regex, bind9, DDOS
category: HOWTO
summary: How to troubleshoot regex in fail2ban 

NO HITS, NO MATCH, NO NOTHING!
==============================
So, you're eager to write a new fail2ban filter and it failed ... miserably.

fail2ban couldn't match anything ... regardless of whether it is
standard fail2ban config or your highly, purportedly, hapzardly-concoted 
filter config file: this page is for you.

[fail2ban](https://www.fail2ban.org/wiki/index.php/Main_Page) is a
autonomous firewall-blocker that gets alerted by many log messages
and performs banning by its detected IP, IP-protocol, and IP-port indications.

At this point, there is little or no documentation on filtering for `fail2ban` v10+.

That is where this blog page comes into, specifically troubleshooting Regex
and Fail2ban.

WHAT STAGES OF REGEX?
=====================
Fail2ban has several components of regex in which to apply toward
the log text, these components/subcomponents are:

* `datepattern`
* `prefregex`
    + `failregex`
    + `ignoreregex`

Most of the time, the date is at the beginning of the log text that is
being searched against. For this article, we assume the date is firstly
before anything. 

ACTUAL EXAMPLES!
================
The actual examples pertain to the DDOS going on against my Bind9 
master nameserver. Bind9 uses named for an executable and process name.
Bind9 also uses their own log file (which is our focus here) and
not the usual syslog files.

Actual log file is (after privacy redactions):
```log
19-Sep-2020 11:47:00.116 query-errors: info: client @0x7f0410000e40 123.123.123.123#80 (sl): view red: query failed (REFUSED) for sl/IN/ANY at query.c:5445
19-Sep-2020 11:47:01.120 query-errors: info: client @0x7f0410000e40 123.123.123.123#80 (sl): view red: query failed (REFUSED) for sl/IN/ANY at query.c:5445
19-Sep-2020 11:47:02.020 query-errors: info: client @0x7f0410000e40 123.123.123.123#80 (sl): view red: query failed (REFUSED) for sl/IN/ANY at query.c:5445
19-Sep-2020 11:47:03.356 query-errors: info: client @0x7f0410000e40 123.123.123.123#80 (sl): view red: query failed (REFUSED) for sl/IN/ANY at query.c:5445
19-Sep-2020 11:47:04.988 query-errors: info: client @0x7f0410000e40 123.123.123.123#80 (sl): view red: query failed (REFUSED) for sl/IN/ANY at query.c:5445
19-Sep-2020 11:47:05.576 query-errors: info: client @0x7f0410000e40 123.123.123.123#80 (sl): view red: query failed (REFUSED) for sl/IN/ANY at query.c:5445
```

Note: A little history, the `sl` TLD went off-line and my nameserver
was used as DNS-QUERY-REFUSED DDOS against a target 
(IP 123.123.123.123 which, of course, is a fake IP.)

But I needed a fail2ban to shut this up. Some poor unwitted IoT devices
crafted a bogus source UDP and sent it to my Bind9 nameserver which
successfully goad it into a DNS amplication attack via DNS-QUERY-REFUSED
error message. 

Sadly, latest Bind9 daemon has no configuable field to deal 
false DNS-QUERY-REFUSED acknowledgement message (they claim
it is not kosher to do this, but I still have a problem and intend fail2ban
to deal with it).

I GOT A DATE HIT
================
So you got a 'date' hit. Something like from your `fail2ban-regex -v` 
(please note the important `-v` command line option):
```bash
fail2ban-regex -v /tmp/captured.log /etc/fail2ban/filter.d/named-refused.conf
```
which outputted the following:
```console
...
Date template hits:
|- [# of hits] date format
|  [6] {^LN-BEG}Day(?P<_sep>[-/])MON(?P=_sep)ExYear[ :]?24hour:Minute:Second(?:\.Microseconds)?(?: Zone offset)?
...
```
whose output shows that `[6]` lines have matched the date timestamp at the 
beginning of each line. That's an excellent good start for troubleshooting.

In the sad case of `[0]` match for a date pattern hit, use the `--VD` option
along with `-l HEAVYDEBUG` option in your `fail2ban-regex`. 
Having a `[0]` means you
are dealing with a log text whose `datepattern` that fail2ban has never 
dealt with before. You'll need to craft your own `datepattern`.

This unknown `datepattern` is a subject for another blog. 

PRE-FILTER MATCHED
------------------
In every filter file, `prefregex` is defaulted to `^(?P<content>.+)$`.
If you haven't touch or set the `prefregex`, move on to the next section.

Otherwise, `prefregex` becomes your focus in troubleshooting.

You can tell that the (default or customized) `prefregex` works if 
you added `-l HEAVYDEBUG` to your `fail2ban-regex` command line:
```bash
fail2ban-regex \
    -v \
    -l HEAVYDEBUG \
    /tmp/captured.log \
    /etc/fail2ban/filter.d/named-refused.conf
```
Remember the above command, we are going to use it each time we modified
the filter configuration file: and quite very often.  Use
your bash history buffer and recall that command, over and over again. 
Remember.

and the output shows a line starting with `T:   Pre-filter matched`:
```console
H:   Looking for prefregex '^(?P<content>.+)$'
T:   Pre-filter matched {'content': ' query-errors: info: client @0x7f01e00004e0 123.123.123.123#80 (sl): view red: query failed (REFUSED) for sl/IN/ANY at query.c:5445'}
```
and note the value of `content:`. 
This `content` is then fed into the `failregex` patterns.

Please note in `'content':` value that there is an extra space at 
the beginning of that value so be careful with the '`^`' and make sure 
it starts with '`^ `' (note a space after caret symbol.)

But, with regard to that extra space char, do what I do; incorporate that 
space into your `prefregex`. Your 
custom `prefregex` will take away that beginning space character
from all your future (and current) filter patterns. This makes
for an easier-to-read `failpregex` pattern(s).
```ini
prefregex = ^ <F-CONTENT>.+</F-CONTENT>$
```
The above custom `prefregex` will ensure that that beginning space 
character is removed before going on to `failregex` and return
just the interesting `<F-CONTENT>.+</F-CONTENT>$` which is basically
everything after that lone (but unwanted) space char.

Running that `fail2ban-regex` with the `-l HEAVYDEBUG`, the new output 
shows:
```console
T:   Pre-filter matched {'content': 'query-errors: info: client @0x7f0410000e40 123.123.123.123#80 (sl): view red: query failed (REFUSED) for sl/IN/ANY at query.c:5445'}
```
Notice that a space no longer exist before `query-errors`.

Everything from the beginning of the first non-space to the end of the
line must be dealt with by our newly customized `failregex`.

FAILREGEX MATCHED
-----------------
Focus on the `failregex` portion of the filter config file.

The catch of using `failregex` is that there MUST be at least one 
group match such as `<HOST>`, `USERID`, or ????.

So, do what I do... Make a generic `failregex` in your filter conf file
like:
```ini
failregex = query.+<HOST>
```
Notice that there is no `$` to catch end-of-line match condition? 
Do those `$` lastly because our goal is to just match ... ANYTHING!

Re-run `fail2ban-regex` with `-l HEAVYDEBUG` and notice the 
`T:   Matched FailRegex` part:
```console
T:   Matched FailRegex('query.+(?:(?:::f{4,6}:)?(?P<ip4>(?:\\d{1,3}\\.){3}\\d{1,3})|\\[?(?P<ip6>(?:[0-9a-fA-F]{1,4}::?|::){1,7}(?:[0-9a-fA-F]{1,4}|(?<=:):))\\]?|(?P<dns>[\\w\\-.^_]*\\w))')
```
Now I am matching SOMETHING! Notice the convoluted patterns after `query.+`?
These long patterns represent `<HOST>` part. Ignore that for 
now.

Most importantly, I am MATCHING something that starts with `^query`! Yippee!

GYRATING TOWARD FULL MATCH
==========================
With a working matching pattern (albiet a failed but overly-broad pattern), 
we can then work toward a full-blown concise (yet flexible) pattern.

Let's start by adding more static pattern. I am pretty sure 
from my intensive examination of that line 5445 in Bind9 `query.c`
source file that `query-error: info:` is something that will 
not change for my target condition. This log output may have other 
variance like `query-error: warn` or `query-error: debug` but I 
am ignoring 
those.

First iteration of `failregex` expansion:
```ini
failregex = ^query-errors: info: .+<HOST>
```
Execute the command:
```bash
fail2ban-regex \
    -l HEAVYDEBUG \
    --print-no-missed \
    /tmp/query-errors.log named-refused.local
```
and notice the output:
```console
Results
=======

Failregex: 6 total
|-  #) [# of hits] regular expression
|   1) [6] ^query-errors: info: .+<HOST>
`-
```
See the `[6]`? I have six matches out of 6 lines give in log text file.
I am getting close to a full-blown pattern! Don't forget, we have to
close that pattern out with a `$` but not yet, save that for the end of this
tutorial.

CAUTION: Everytime you make a change to `failregex`, PAY VERY CLOSE ATTENTION 
to the `Failregex: X total` tabulation. Once you get that `Failregex: 0 total` 
, you know you have done something HORRIBLE, busted and broke your 
pattern, so roll that pattern back to its simpler pattern and start again.

INCREMENTS, INCREMENTS, INCREMENTS
==================================

So, the increments of me adding more and more patterns and ensuring
that I am still getting `Failregex: 6 matches` are listed below:

1. `failregex: query-errors: info: client.+<HOST>`
2. `failregex: query-errors: info: client @0x[0-9a-fA-F]{8,12}.+<HOST>`

Whoa, it's getting too long... so I made a variable to contain this entire
pattern and called it `_client`.

```ini
_client = query-error: info: client @0x[0-9a-f]{8,12}
```
Now I can shorten the `failregex` a bit:
```ini
failregex = ^%(_client)s <HOST>
```
It's the same thing, but readable.... onward to matching the rest of 
the line.

NOTE: You are running `fail2ban-regex` between each modification, aren't you?

NOW FOR THE ENDING PART
=======================
FINALLY it reached the `<HOST>` part of the log text. 

Now it is closing time!  Let's race to the `$` (end).

Add that port number after the host:
```
failregex = ^%(_client)s <HOST>#\d{1,5}
```

NOTE: You are running `fail2ban-regex` between each modification, aren't you?

REPETITION
==========
Notice that the domain name `example.tld` is used twice in the same log line?

Let us make a pattern called `_domain` and reduce our typing errors a bit.

```ini
_domain = [0-9a-zA-Z\._\-]{2,256}
```
Our new `failregex` becomes:
```ini
failregex = ^%(_client)s <HOST>#\d{1,5} \(%(_domain)s\):
```

NOTE: You are running `fail2ban-regex` between each modification, 
still getting that exact same match `[6]` (or whatever count you're aiming
for.)

SIMPLIFICATION
==============
Now for the `view` part of Bind9 where we handle the view name.  
View name is optional.  A `view` name may not be used on some nameserver
installation.  

```ini
_view_name = [0-9a-zA-Z\._\-]{1,64}
_view = ( \%(_domain)s\))?: view %(_view_name)s
```
Our latest `failregex` becomes:
```ini
failregex = ^%(_client)s <HOST>#\d{1,5}%(_view)s
```

Still have a long way to go before we add that `$` ending pattern.

NOTE: You are running `fail2ban-regex` between each modification, aren't you?

FINAL STRETCH
=============
With the remaining of log text ` query failed (REFUSED) for example.tld/IN/ANY at query.c:5445` left to go, rush it up with:

```ini
_query_refused = query failed \(REFUSED\) for %(_dns_tuple)s at %(_codeloc)s$
```
and supply missing defines:
```ini
_domain = [0-9a-zA-Z\._\-]{1,254}
_dns_tuple = %(_domain)s\/IN\/ANY

_filespec = [0-9a-zA-Z\._\-]{1,254}
_codeloc = %(_filespec)s:\d{1,6}
```

NOTE: Guess? You are running `fail2ban-regex` between each modification?
 You still getting that non-zero `Failregex: 6 total` match under `Results`?
```console
Failregex: 6 total
|-  #) [# of hits] regular expression
|   1) [6] ^query-errors: info: client @0x[0-9a-f]{8,12} <HOST>#\d{1,5}( \([0-9a-zA-Z\._\-]{1,254}\))?: view [0-9a-zA-Z\._\-]{1,64}: query failed \(REFUSED\) for [0-9a-zA-Z\._\-]{1,254}\/IN\/ANY at [0-9a-zA-Z\._\-]{1,254}:\d{1,6}$
`-
```

Ok, you could have paid attention to the last line of the output:
```console
Lines: 6 lines, 0 ignored, 6 matched, 0 missed
```
But I've find this to be easily overlooked hence the focal point 
within the `Failregex` as being more informative.

CONCLUSION
==========
Now we can add the `$` to the end of `failregex`.

Execute `fail2ban-client reload` and watch the blocking begin.

External References
====================

* [Monitoring the fail2ban log](https://www.the-art-of-web.com/system/fail2ban-log/)
