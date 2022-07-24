title: Configuration file layout for fail2ban 
date: 2020-05-05 13:02
Modified: 2020-09-19 14:16
status: published
tags: fail2ban
category: HOWTO
summary: Configuration file layout for fail2ban

# Fail2ban Configuration Files #

Relevant File2Ban Configuration files and dirs:

[jtable]
File/Directory, Description
`/etc/fail2ban/filter.d/`,  Contains predefined (regex) fail2ban filters
`/etc/fail2ban/jail.conf`,  Not recommended to be updated, use custom jails
`/etc/fail2ban/jail.local`,  Your customized Jails (or customisation.local)
`/etc/fail2ban/fail2ban.conf`,  Main Configuration File, blown away by each
`/etc/fail2ban/fail2ban.local`,  YOUR personalized Main Configuration File, NOT blown away by each distro upgrades of fail2ban package.
[/jtable]

# Fail2ban Definitions #

## Fail2ban Config File ##

Fail2ban Options

There is only one section within `fail2ban.(conf|local)` file, called `[Definition]`.

For the `[Definition]` section:
[jtable]
keyword, description
socket,
pidfile,
loglevel,
logtarget,
syslogsocket,
[/jtable]

## Filter Config File ##

Filter Options are put under a custom labeled section name.

For the `[XXXX]` section:
[jtable]
keyword, description
prefregex,
ignoreregex,
failregex,
maxlines,
datepattern,
journalmatch,
addfailregex,
addignoreregex,
addjournalmatch,
regex,
logtype,
[/jtable]

## Jail Config File ##

Jail Options

[jtable]
Key name, Description
enabled, Determines if this jail is activated or not.  Default is 'false'.  Use True or false.
filter, Name of the filter to be used by the jail to detect matches. Each single match by a filter increments the counter within the jail
action,
backend, Specify how fail2ban-server will read its log file.  Default is 'auto' which will try pynotify then gamin and lastly pooling.
banaction, Action to be used when ban is triggered. Check /etc/fail2ban/action.d/
bantime, Duration (in seconds) for IP to be banned for. Negative number for “permanent” ban. Also can specify duration suffix of Y, M, W, D, H, M, S.  Example is 3w1d15m for 3 weeks, 1 day, and 15 minutes.
datepattern,
destemail: Email address in which to send the notification to via SMTP.
failregex,
findtime, A range of time that will be permitted to look at the log file(s).
ignorecache,
ignorecommand,
ignoreip, A special exclusion list of IP address(es) that should be exempted from the ban.
ignoreregex,
ignoreself,
logpath, Absolute filepath to the log file in which for the filter to read from.
logtimezone,
logencoding,
maxretry, Number of times before the `banaction` is evoked for a specific IP addres, IP/port, or IP/protocol/port.
mta, MTA used to send notification mails
port, TCP/UDP/SCTP port number used by the service; integer only.
protocol, Type of IP protocol used. Specify protocol ID or [IANA-approved](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xml#protocol-numbers-1) keyword.
sendername, From field for notification emails
sender, Email address that the email will be sending from.
usedns, Perform DNS lookup using OS-provided domain name resolver.
[/jtable]

Following example explains further:

In the customized copy of a jail configuration (`/etc/fail2ban/jail.local`):

```ini
[sshd]

enabled = true
port = ssh
filter = sshd
action = iptables[name=SSH, port=ssh, protocol=tcp]
logpath = /var/log/secure
findtime = 2m
maxretry = 5
bantime = 3600
```

Log path can vary, adjust it on your system (OS). Based on rules above, we’re monitoring SSH log (`/var/log/secure`), and we’re banning anyone (for 1 hour, 3600 seconds) who fails to log 5 times within 2 minutes (120 seconds). Rules are pretty straight forward.  With "`sshd`" filter specified, go to `/etc/fail2ban/filter.d/sshd.conf`, there will be a number of `failregex` rules that are  used to match login attempts from log file.

To whitelist (ignore) an IP, add them to the ignoreip line:

```ini
ignoreip = 127.0.0.1/8
```

Note: Depending on the amount of traffic specific service has (website, wordpress, etc.) fail2ban can generate CPU concerns/load.
Custom Fail2ban PhpMyAdmin filter (Jail & Regex)

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

Look for that filter in the web server (Apache/nginx) logs:

```
/var/log/nginx/access.log.1:121.169.192.227 - - [19/Sep/2018:01:41:23 +0000] "GET /phpmyadmin/index.php?pma_username=root&pma_password=root&server=1 HTTP/1.1" 200 10050 "-" "Mozilla/5.0"
/var/log/nginx/access.log.1:121.169.192.227 - - [19/Sep/2018:01:41:23 +0000] "GET /phpmyadmin/index.php?pma_username=root&pma_password=toor&server=1 HTTP/1.1" 200 10050 "-" "Mozilla/5.0"
/var/log/nginx/access.log.1:121.169.192.227 - - [19/Sep/2018:01:41:23 +0000] "GET /phpmyadmin/index.php?pma_username=root&pma_password=r00t&server=1 HTTP/1.1" 200 10050 "-" "Mozilla/5.0"
```

The IP 121.169.192.227 is trying to bruteforce its way in (well known malicious IP). Let us make their life a bit more difficult. Make a file in your `/etc/fail2ban/filter.d/phpmyadmin.conf`, and insert:

```
[Definition]
failregex = ^<HOST> -.*"(GET|POST).*/phpmyadmin/index\.php\?pma_username=root&pma_password=.*$
ignoreregex =
```

The above regex is matching the lines we’ve seen in the logs. This will ban anyone for 1 hour if they fail to login more than 3x in 60 seonds. When done, restart fail2ban:

```console
$ service fail2ban restart
```

or reload:

```console
$ fail2ban-client reload phpmyadmin
```

Fail2ban testing regex

After creating a filter, it’s good idea to test it before activating it. For that we have this `fail2ban-regex` tool:

```console
$ fail2ban-regex /var/log/nginx/access.log /etc/fail2ban/filter.d/phpmyadmin.conf
```

Running tests
=============

Use   failregex filter file : phpmyadmin, basedir: /etc/fail2ban
Use         log file : /var/log/nginx/access.log
Use         encoding : UTF-8


Results
=======

```console
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
```

There is a match. In case filter/regex is wrong, this will probably end up with no matches:

```
Lines: 3315 lines, 0 ignored, 0 matched, 3315 missed [processed in 0.23 sec]
Missed line(s): too many to print. Use --print-all-missed to print all 3315 lines
```

Fail2ban Email Alerts

I didn’t experiment with this much, but its probably worth mentioning that you have Email Alert option. Adjust email setings:

    destemail: Destination Email address, where you would like to receive the emails.
    sendername: Name under which the email will shows up.
    sender: Email address from which Fail2ban will send emails.

Use fail2ban predefined actions.d/sendmail-whois:

```ini
[sendmail]
enabled = true
filter = sendmail
action = iptables-multiport[name=sendmail, port="pop3,imap,smtp,pop3s,imaps,smtps", protocol=tcp]
sendmail-whois[name=sendmail, dest=user@domain.com]
logpath = /var/log/maillog
```

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
bantime = 10m
```

# External References #

* [Monitoring the fail2ban log](https://www.the-art-of-web.com/system/fail2ban-log/)

