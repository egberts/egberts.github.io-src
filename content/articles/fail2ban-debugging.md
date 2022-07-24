title: Debugging fail2ban 
date: 2020-05-05 12:02
status: published
tags: fail2ban, debugging, Debian
category: HOWTO
summary: How to debug fail2ban for NFTABLES, Debian 11

[fail2ban](https://www.fail2ban.org/wiki/index.php/Main_Page) is a
autonomous firewall-blocker that gets alerted by many log messages
and performs banning by its detected IP, IP-protocol, and IP-port indications.

NOTICE: This does not apply toward IPv6 system (yet).

# Debugging `fail2ban`

In debugging `fail2ban`,  an error occurred.  And it's obviously a
failed pattern (IMHO, the worse kind to debug).


## Debugging `fail2ban-client`

To debug the `fail2ban-client`, the outputs are governed by syslog severity
level.  It defaults to `SYSLOG_ERROR`.  Its cmdline options to use are:

[jtable]
`fail2ban-client -v`, `SYSLOG_WARNING`
`fail2ban-client -v -v`, `SYSLOG_INFO`
`fail2ban-client -v -v -v`, `SYSLOG_DEBUG`
`fail2ban-client -v -v -v -v`, Heavy debug outputs
[/jtable]


## Debugging `fail2ban-server`

To debug the `fail2ban-server`, the outputs are statically fixed via `XXXXX`
settings in `/etc/fail2ban/fail2ban.(local|conf)` file.

To change the debug level and output, execute:
```shell
fail2ban-client set loglevel 1
fail2ban-client set logtarget STDERR
```

# External References

* [Monitoring the fail2ban log](https://www.the-art-of-web.com/system/fail2ban-log/)

