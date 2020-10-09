title: Systemd-Resolved NOPE!
date: 2020-06-06 18:06
status: published
tags: systemd, resolver, resolv.conf
category: security
summary: systemd-resolved and DNSSEC, Ouch!

You should never let `systemd` do your DNSSEC, especially
if you're a hobbyist gateway router maintainer, running a homenet or 
whitelab with private TLDs.

I will explain why.



Forcing 'consumer' mode in `systemd-resolv`
==========================================

systemd-network setting
-----------------------

Set the `[Network]` section in the systemd network file to contain:

```ini
; LLMNR False disables Link-Local Multicast Name Resolution on the link:
;   resolution, host registration, and announcement.
LLMNR=False

; Systemd should not access any external network, period.
DNSSEC=False

; there shall be no DNS server available to systemd
DNS=

; 
DNSDefaultRoute=
```


