title: Systemd-Resolved NOPE!
date: 2020-06-06 18:06
modified: 2025-07-13 03:18
status: published
tags: systemd, resolver, resolv.conf
category: security
summary: systemd-resolved and DNSSEC, Ouch!

You should never let `systemd` do your DNSSEC, notably
if you are 're a hobbyist maintainer of gateway router, operating a homenet or
whitelab with private TLDs.


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

; no DNS server available to systemd
DNS=

;
DNSDefaultRoute=
```

