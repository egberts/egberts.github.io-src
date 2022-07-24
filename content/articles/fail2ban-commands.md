title: Commands for fail2ban 
date: 2020-05-05 13:02
Modified: 2020-09-16 14:16
status: published
tags: fail2ban
category: HOWTO
summary: Commands for fail2ban

# Fail2ban Configuration Files #

Relevant File2Ban Configuration files and dirs:

[jtable]
File/Directory, Description
`/etc/fail2ban/filter.d/`, Contains predefined (regex) fail2ban filters
`/etc/fail2ban/jail.conf`, Not recommended to be updated, use custom jails
`/etc/fail2ban/jail.local`, Your customized Jails (or customisation.local)
`/etc/fail2ban/fail2ban.conf`, Main Configuration File
[/jtable]

# Fail2ban Definitions #

Before we continue, it’s probably good idea to define what’s what:

[jtable]
Keyword, description
`filter`, a filter defines a regular expression which must match a pattern corresponding to a log-in failure or any other expression
`action`, an action defines several commands which are executed at different moments
`jail`, a jail is a combination of one filter and one or several actions. Fail2ban can handle several jails at the same time
`client`, refers to the script fail2ban-client
`server`, refers to the script fail2ban-server
[/jtable]

Fail2ban Server is multi-threaded, listens on a Unix socket for commands. Knows nothing about configuration files.

Command line options for fail2ban server are:
[jtable]
Command line option, description
`-b`, start in background
`-f`, start in foreground
`-s <FILE>`, socket path
`-x`, force execution of the server
`-h`, `--help`, display this help message
`-V`, `--version`, print the version
[/jtable]

Fail2ban Client is basically the frontend, operate the servers. Reads the configuration files, or accept individual commands via interactive mode.

Command line options for `fail2ban-client` command are:
[jtable]
Command line option, description
`-c <DIR>`, configuration directory
`-s <FILE>`, socket path
`-d`, dump configuration. For debugging
`-i`, interactive mode
`-v`, increase verbosity
`-q`, decrease verbosity
`-x`, force execution of the server
`-h`, `--help`, display this help message
`-V`, `--version`, print the version
[/jtable]

Examples:

```bash
fail2ban-client set loglevel 1
fail2ban-client set logtarget STDERR

fail2ban-client status
```
output is:
```console
|- Number of jails: 1
`- Jail list: sshd

$ fail2ban-client status sshd
Status for the jail: sshd
|- Filter
|  |- Currently failed: 2
|  |- Total failed: 42635
|  |- File list: /var/log/auth.log
`- Actions
   |- Currently banned: 0
   |- Total banned: 863
   |- Banned IP list:
```

The main configuration keywords of fail2ban goes 
into `/etc/fail2ban/fail2ban.conf` AND
your customization goes into `/etc/fail2ban/fail2ban.local`:

[jtable]
Main key name, description, valid value(s)
`loglevel`, The level of detail that Fail2ban’s logs provide, 1 (error); 2 (warn); 3 (info); 4 (debug)
`logtarget`, Logs actions into a specific file. The default value of `/var/log/fail2ban.log` which puts all loggings into this defined file., Alternatively you can change the value to, STDOUT: output any data; STDERR: output any errors; SYSLOG: message-based logging; FILE: output to a file
`socket`, The location of the socket file., 
`pidfile`, The location of the PID file., 
[/jtable]

The keywords used for jail configuration goes into
`/etc/fail2ban/jail.conf` AND 
your customization goes into `/etc/fail2ban/jail.local`:

[jtable]
Jail key word, description
`filter`, name of the filter to be used by the jail to detect matches. Each single match by a filter increments the counter within the jail
`logpath`, Path to the log file which is provided to the filter
`maxretry`, Number of matches (i.e. value of the counter) which triggers ban action on the IP.
`bantime`, Duration (in seconds) for IP to be banned for. Negative number for “permanent” ban.
`enabled`, True or false. Defines if filter is turned on or not
`port`, The port used by the service
`ignoreip`, IP(s) that should be ignored by fail2ban
`findtime`, Time range fail2ban will pay attention to when looking at the logs.
`backend`, Defines how fail2ban monitor logs. It will try pinotify then gaming and finaly OS polling.
`destemail`, Address to send email notifications to
`sendername`, From field for notification emails
`sender`, Email address from which Fail2ban will send emails.
`mta`, MTA used to send notification mails
`protocol`, 
`banaction`, Action to be used when ban is triggered. Check /etc/fail2ban/action.d/
[/jtable]

Here's one working example in `/etc/fail2ban/jail.local`:

```ini
[sshd]

enabled = true
port = ssh
filter = sshd
action = iptables[name=SSH, port=ssh, protocol=tcp]
logpath = /var/log/secure
findtime = 120
maxretry = 5
bantime = 3600
```

Log path can vary, you can adjust it on your system (OS). 

Based on rules above, fail2ban monitors SSH log (`/var/log/secure`), and will be banning anyone (for 1 hour, or 3600 seconds) who fails to log 5 times 
within 2 minutes (120 seconds). 

Rules are pretty straight forward. Specify the "`sshd`" filter, so if you 
go to `/etc/fail2ban/filter.d/sshd.conf`, you’ll see a number of failregex 
rules, used to match login attempts from log file.

To whitelist (ignore) an IP, add them to the `ignoreip` setting:

```ini
ignoreip = 127.0.0.1/8
```

Note: Depending on the amount of traffic specific service has (website, wordpress, etc.) fail2ban can generate CPU concerns/load.

# Custom Fail2ban PhpMyAdmin filter (Jail & Regex)

The best way to learn is to try and write your own filters. I’ll show you an example for Custom Fail2ban PhpMyAdmin filter. First, we need the jail in our jail.local file:

```ini
[phpmyadmin]

enabled = true
port = http,https
filter = phpmyadmin
action = iptables-multiport[name=PHPMYADMIN, port="http,https", protocol=tcp]
logpath = /var/log/nginx/access.log
bantime = 3600
findtime = 60
maxretry = 3
```

Next we need that filter. Check your web server (Apache/nginx) logs:

```log
/var/log/nginx/access.log.1:121.169.192.227 - - [19/Sep/2018:01:41:23 +0000] "GET /phpmyadmin/index.php?pma_username=root&pma_password=root&server=1 HTTP/1.1" 200 10050 "-" "Mozilla/5.0"
/var/log/nginx/access.log.1:121.169.192.227 - - [19/Sep/2018:01:41:23 +0000] "GET /phpmyadmin/index.php?pma_username=root&pma_password=toor&server=1 HTTP/1.1" 200 10050 "-" "Mozilla/5.0"
/var/log/nginx/access.log.1:121.169.192.227 - - [19/Sep/2018:01:41:23 +0000] "GET /phpmyadmin/index.php?pma_username=root&pma_password=r00t&server=1 HTTP/1.1" 200 10050 "-" "Mozilla/5.0"
```

The IP 121.169.192.227 is trying to bruteforce its way in (well known malicious IP). 
Let us try to make their life a bit more difficult: Make a file in 
your `/etc/fail2ban/filter.d/phpmyadmin.local`, and insert:

```ini
[Definition]
failregex = ^<HOST> -.*"(GET|POST).*/phpmyadmin/index\.php\?pma_username=root&pma_password=.*$
ignoreregex =
```

The above regex is matching the lines we’ve seen in the logs. 
This will ban anyone for 1 hour if they fail to login more than 
3x in 60 seonds. When done, restart fail2ban can be done in several ways:

```bash
service fail2ban restart
# or
systemctl reload fail2ban
systemctl restart fail2ban
```
or reload:
```bash
fail2ban-client reload phpmyadmin
```

Fail2ban testing regex
----------------------

When you finish creating some filter it’s good idea to test it 
before activating it. For that, we have `fail2ban-regex`:

```bash
fail2ban-regex /var/log/nginx/access.log /etc/fail2ban/filter.d/phpmyadmin.conf
```
Output is:
```console
Running tests
=============

Use   failregex filter file : phpmyadmin, basedir: /etc/fail2ban
Use         log file : /var/log/nginx/access.log
Use         encoding : UTF-8


Results
=======

Failregex: 56 total
|-  #) [# of hits] regular expression
|   1) [56] ^<HOST> -.*"(GET|POST).*/phpmyadmin/index\.php\?pma_username=root&pma_password=.*$
`-

Ignoreregex: 0 total

Date template hits:
|- [# of hits] date format
|  [4078] Day(?P<_sep>[-/])MON(?P=_sep)Year[ :]?24hour:Minute:Second(?:\.Microseconds)?(?: Zone offset)?
`-

Lines: 4078 lines, 0 ignored, 56 matched, 4022 missed [processed in 0.33 sec]
Missed line(s): too many to print.  Use --print-all-missed to print all 4022 lines

There is a match. In case the filter/regex is wrong, this will probably end up with no matches:

Lines: 3315 lines, 0 ignored, 0 matched, 3315 missed [processed in 0.23 sec]
Missed line(s): too many to print. Use --print-all-missed to print all 3315 lines
```

Fail2ban Email Alerts
---------------------

I didn’t experiment with this much, but its probably worth mentioning 
that you have Email Alert option. Adjust email settings:

[jtable]
Key word, description
`destemail`, Destination Email address, where you would like to receive the emails.
`sendername`, Name under which the email will shows up.
`sender`, Email address from which Fail2ban will send emails.
[/jtable]

Use fail2ban predefined actions.d/sendmail-whois:

```ini
[sendmail]
enabled = true
filter = sendmail
action = iptables-multiport[name=sendmail, port="pop3,imap,smtp,pop3s,imaps,smtps", protocol=tcp]
sendmail-whois[name=sendmail, dest=user@domain.com]
logpath = /var/log/maillog
```

Example: SSH
------------
Another example:

```ini
[ssh]
enabled  = true
port     = ssh
filter   = sshd
action   = iptables-multiport[name=ssh,port=["ssh"|”22,4422”],protocol=tcp]
         mail[name=SSH,dest=dstEmail@domain.com,sender="info@domain.com"]
logpath  = /var/log/auth.log
maxretry = 3
bantime = 600
```

External References
=======================

* [Monitoring the fail2ban log](https://www.the-art-of-web.com/system/fail2ban-log/)

