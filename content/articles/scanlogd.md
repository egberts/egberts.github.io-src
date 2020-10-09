title: Scanlogd and Fail2ban
date: 2020-10-03 23:11
modified: 2020-10-04 08:11
status: published
tags: fail2ban, scanlogd
category: HOWTO
summary: How to set up fail2ban to monitor scanlogd log file

Seems like quite a bit of portscanning is going on against VPS ecosphere.

It's time to ban those pesking log-clogging offenders.  I thought
of a port-scanning ban tool, but none can be found.

So, let's split those functions into two and look for a 
detector and a ban hammer for port scanning.

I already use [fail2ban](https://github.com/fail2ban/fail2ban) as a 
ban hammer and am quite happy with it.  
Barely ekes a Unix load of 0.3 for `fail2ban`.

A quick scan of the Debian package repository shows that there is a
portscan detection tool called [`scanlogd`](https://www.openwall.com/scanlogd/)

Quickly installed `scanlogd`.
```bash
apt install scanlogd
```

WARNING: This portscanner is not suitable for protection of dense internal
network.  It is fine for home use and maybe small businesses.
You could run a risk of blocking yourself due to packet's fake source IP 
address being set to your external gateway IP.

Be sure to have the following configuration setting in your
`/etc/fail2ban/jail.local` configuration file:
```ini
[DEFAULT]

ignoreip = 127.0.0.1/8 <MY-EXTERNAL-IP-ADDRESS> <MY-INTERNAL-IP-ADDRESS>
```
and replace the `<MY-EXTERNAL-IP-ADDRESS>` and `<MY-INTERNAL-IP-ADDRESS>`
with the IP addresses that you are defending against. 


Setting up Scanlogd
-------------------
Current version v2.2.5 is still stuck in the SysV init days so there
is no systemd service unit file; but that gets automatically generated
by systemd-sysv-generator.  The service name is `scanlogd.service`.

```bash
systemctl enable scanlogd.service
systemctl start scanlogd.service
```

No configuration settings needed.  This is a 360-degree, all-round, all-ports
port scanning daemon.

Fail2ban
========
Now we need two more configuration files for fail2ban.

* filter - To extract the IP address from each line in scanlogd file.
* jail - to take action against these IP

Fail2ban - Filter
=================
Create the new filter file in `/etc/fail2ban/filter.d/scanlogd.conf` to 
contain the following:
```ini
[Definition]
failregex = \s{1,1}\S{2,256} scanlogd: <HOST>:\d{1,5} to [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} .*$
ignoreregex =
```

Fail2ban - Jail
===============
Create the new jail file in `/etc/fail2ban/jail.d/scanlogd.local` 
to contain:
```ini
[scanlogd]
enabled = true
#filter = scanlogd
logpath = /var/log/scanlogd.alert
maxretry = 1
; bantime should be longer than 1 week
bantime = 1w
```
What the configuration will do is enable the filter, read the  scanlogd.alert 
file, and all offenders are not allowed to try more than ONCE
and are banned from using this host for 1 week.

Wrap it up
==========
Then execute:
```bash
systemctl start scanlogd.service
fail2ban-client reload
```
and check the status of both daemons:
```bash
systemctl status scanlogd.service | fold
fail2ban-client status
fail2ban-client status scanlogd
```

Now go back to real life.
