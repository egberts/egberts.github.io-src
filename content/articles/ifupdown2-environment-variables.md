title: Environment variables for ipupdown hook routines
date: 2021-11-23 11:00
status: published
tags: ifupdown, environment variables
category: research
lang: en
private: False

This article details the environment variables being available to the hook
routines of ipupdown tool suite which covers `ifup` and `ifdown`.



[jtable caption="Environment variables of ipupdown" separator="|" th=1]
# caption - the table caption
# separator - default is comma
# th - table header (=0 means disable)
# ai - auto-index, adds a column numbering starts at 1
interfaces command, shell environment variable name
(any), `ADDRFAM`, protocol family (`inet` or `inet6`)
(any), `IFACE`, name of netdev 
(any), `LOGICAL`, formal name of interface
(any), `MAIL`, for e-mail alerting
(any), `METHOD`, `static` or `manual`
(any), `MODE`, `start`
(any), `OLDPWD`, `/etc/network`
(any), `PWD`, `/etc/network/if-up.d`
(any), `PHASE`, `up` or `down`
(any), `SHELL`, `/bin/bash`
`ethernet-wol`, `IF_ETHERNMET_WOL`
`ip-forward`, `IP_FORWARD`
[/jtable]
