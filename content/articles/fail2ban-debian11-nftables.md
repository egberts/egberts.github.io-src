title: fail2ban setup
date: 2020-05-04 17:00
status: published
modified: 2022-07-24 09:45
tags: fail2ban, regex, Debian
category: HOWTO
summary: How to setup fail2ban for NFTABLES, Debian 11

[fail2ban](https://www.fail2ban.org/wiki/index.php/Main_Page) is a
autonomous firewall-blocker that gets alerted by many log messages
and performs banning by its detected IP, IP-protocol, and IP-port indications.

NOTICE: This does not apply toward IPv6 system (yet).

The other day, I cloned [fail2ban from GitHub](https://github.com/fail2ban/fail2ban.git)
 (version 0.10.2-2.1) onto my fresh Debian 11 by doing:

```shell
git clone https://github.com/fail2ban/fail2ban.git
cd fail2ban
git checkout debian
python3 ./setup.py install --install-layout=deb
```
It didn't work.  Something about 2to3.

# WORKING INSTALLATION #

Yeah, one of those "package distro manager" issue.  Argh.  A short search on
Debian bugzilla didn't reveal any prior experiences.  
I dug hard into the fail2ban's GitHub Issues and barely found the solution.

This fail2ban repository is based on Python2 source code, but by running the `2to3` utility,
 you'll get this Python3-variant easily and in-place.

So, let's forge ahead...

```shell
# Supply missing but required packages
apt install 2to3
apt install sqlite3
apt install dh-python
apt install python3-configparser
apt install python3-systemd    # Debian distro probably already got this
apt install python3-pyinotify  # recommends, but we need this
apt install whois              # recommends
apt install mailx              # suggested
apt install monit              # suggested
apt install system-log-daemon  # suggested

apt remove iptables

# Convert python source into python3
./fail2ban-2to3

# Finally install it
python3 ./setup.py install --install-layout=deb

# Test it
fail2ban-client -h
fail2ban-client version
```
YEAH!  

## Debian-Specific Configuration ##

Debian has many specific customizations that are required:

* `/etc/systemd/system/multi-user*/fail2ban.service`
* `/etc/jail.conf`
* `/etc/fail2ban/jail.d/defaults-debian.conf`
* `/etc/fail2ban.local`

### Systemd Unit File ###
First one is the default init subsystem called `systemd`.  Add a new systemd
unit file into `/etc/systemd/system/multi-users*/fail2ban.service` with the
following content:

```systemd
[Unit]
Description=Fail2Ban Service
Documentation=man:fail2ban(1)
After=network.target iptables.service firewalld.service ip6tables.service ipset.service nftables.service
#### PartOf=iptables.service firewalld.service ip6tables.service ipset.service nftables.service
# Apply Debian-specific `PartOf`
PartOf=firewalld.service

[Service]
Type=simple
ExecStartPre=/bin/mkdir -p /run/fail2ban
ExecStart=/usr/bin/fail2ban-server --async -xf start
# if should be logged in systemd journal, use following line or set logtarget to sysout in fail2ban.local
# ExecStart=/usr/bin/fail2ban-server -xf --logtarget=sysout start
ExecStop=/usr/bin/fail2ban-client stop
ExecReload=/usr/bin/fail2ban-client reload
PIDFile=/run/fail2ban/fail2ban.pid
Restart=on-failure
RestartPreventExitStatus=0 255

[Install]
WantedBy=multi-user.target
```

or you can simply execute:

```shell
cp build/fail2ban.service  \
    /etc/systemd/system/multi-user.target.wants/
chmod 644 /etc/systemd/system/multi-user.target.wants/fail2ban.service
chown root:root /etc/systemd/system/multi-user.target.wants/fail2ban.service
```
and edit the file to replace the `PartOf=` line with:

```ini
PartOf=firewalld.service
```

Then auto-start this systemd unit service.

```shell
systemctl daemon-reload
systemctl unmask fail2ban.service
systemctl enable fail2ban.service
# Defer starting up this daemon later below this article
```

### Jail Configuration ###
For changing the jail configuration, this is the only exception to the 
rule, we're going to modify a `.conf` file
(and not the `.local`).

Edit the `/etc/fail2ban/jail.conf` and replace the following lines:

```ini
[INCLUDES]

before = paths-distro.conf
```
and change that `before` setting into:
```ini
[INCLUDES]

before = paths-debian.conf
```

Exit the editor and then search for any inadvert enabling of jails in the
jail.conf.  


```console
$ egrep "^\s*enable" /etc/fail2ban/jail.conf
enabled = false
```

Set to a `false` value.

### Turning on A Specific Jail ###

Let us turn on our first ban, for failed attempts to login via SSH protocol.

Add a file to `/etc/fail2ban/jail.d/` subdirectory.  Could be set to any filename, but this
time, it's Debian-specific.  Create the `defaults-debian.conf` file
for our first filename and fill it with:

```ini
[sshd]
enabled = true
port     = 2222 ; <= Set your custom SSH server port number here
```

For those who have installed the Debian `fail2ban` package, that file already
exists.

Or you could copy it directly from there:
```shell
cp debian/debian-files/jail.d_defaults-debian.conf \
    /etc/fail2ban/jail.d/defaults-debian.conf
chmod 066 /etc/fail2ban/jail.d/defaults-debian.conf
chown root:root /etc/fail2ban/jail.d/defaults-debian.conf
```
That `defaults-debian.conf` is the only Debian-specific configuration, hence we
do not use `.local` filetype for that purpose.

For subsequential jail(s), the filename can be anything you want, just as as long as it ends
with a filetype of `.local`.  

### Daemon Settings ###
Adjustment is required in the `fail2ban.conf` file, so create an additional
file (a side configuration) to modify this vendor-supplied file
called `fail2ban.local`, and filled this file with the following text:

The `.local` filetype is to ensure that the next package upgrade will 
not undo any custom settings.

```ini
[DEFAULT]
### For debugging fail2ban-server, set the logtarget to sysout
### logtarget = sysout
usedns = "true"

[Definition]
# Following `pidfile`-related entries 
#     ExecStartPre=/bin/mkdir -p /run/fail2ban
#     PIDFile=/run/fail2ban/fail2ban.pid
# must be identical, directory-path-wise, in file:
#    /etc/systemd/system/multi-user.target.wants/fail2ban.service

pidfile = /run/fail2ban/fail2ban.pid
socket = /run/fail2ban/fail2ban.sock
```

# NFTABLES #

Next, use the new `nftables` to perform this "ban" action.  
Skip the `iptables` and `netfilter` because it is obsolete.  

Here, I've used
`shorewall` firewall software with fail2ban with no problem either (but that's
another article).

Install the nftables package:

```console
$ apt install nftables

$ nft -v
nftables v0.9.0 (Fearless Fosdick)

$ nft list ruleset
```

## NFTABLES configuration ##

Couple of files/subdirectories to create are:

1. `/etc/nftables` subdirectory
2. `/etc/nftables/fail2ban.conf`

First, we edit the new `/etc/nftables.conf` so that it looks like:

```nft
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
	chain input {
		type filter hook input priority 0;
	}
	chain forward {
		type filter hook forward priority 0;
	}
	chain output {
		type filter hook output priority 0;
	}
}

# If you had prior nftables.conf settings, 
# just add the following line instead 
# toward your own nftable.conf.
include "/etc/nftables/fail2ban.conf" 
```

Create the new `/etc/nftables/fail2ban.conf` file to contain the following text:

```nft
#!/usr/sbin/nft -f
# File: /etc/nftables/fail2ban.conf
# Description: Set up NFT ruleset for fail2ban

table ip fail2ban {
    chain input {
        # Assign a high priority to reject as fast as possible and 
        # avoid more complex rule evaluation

        type filter hook input priority 100;
    }
}
```
Load up the NFT filters and view the ruleset
```shell
nft /etc/nftables/fail2ban.conf
nft list ruleset
```

# Configuration Files #

Configuration files for fail2ban are grouped into 3 distinctive categories:

* Jail (ban-severity, ban-frequency, sentencing guidelines)
* Filter (Law, patterns, aberrant behavior identification)
* Fail2ban (Judge, interaction, daemon, interaction, OS-related)

## Configuration Inter-Files ##

Overall, 'jail' is the 'master' configuration file that ties both
'action' and 'filter' together.

Dependencies are:

```
        jail
         |
   +-----+---------+
   |               |
 action          filter
```

## Main and Local Configuration Files ##
Be easier just to point out in advance that we:

* Only needs to work with `*.local` configuration files
* Not need to ever be touching any existing `*.conf` files

Those `*.conf` are merely just there for your evening readings.  Don't rewrite
them: those `*.conf` files will just be getting overwritten by the next fail2ban upgrade.

## Configuration File Layout ##
fail2ban configuration file follows the [INI] format.  Many of you developers from Windows
platform are already familiar with INI format.

The pre-defined sections are:

* INCLUDES
* DEFAULT
* KNOWN
* Init
* Definition

### Action File Layout ###
Available keywords are:

* actname
* name   # Name of jail
* actionstart
* actionstart_on_demand
* actionstop
* actionflush
* actionreload
* actioncheck
* actionrepair
* actionban
* actionunban
* norestored
* bantime
* timeout

### 

## FAIL2BAN Daemon Configuration ##

Daemon and OS related settings goes into the main `fail2ban.conf`.  Thankfully,
it also supports `fail2ban.local` which won't be touched by any major package upgrade.


First configuration file to add is `fail2ban.local` in the `/etc/fail2ban`
directory.  Create that file with:

```ini
[DEFAULT]
usedns = "true"
```

## JAIL Configuration ##

Jail is the sentencing mechnaism, its guidelines and how justice is mete out.
It may be in form of:

* blanket and outright IP subnet ban, 
* port-specific ban on an IP, or just
* a simple ban on a all-port IP address.

Second configuration file to add is `jail.local` in the `/etc/fail2ban`
directory.  Create that file with:

```ini
#
[DEFAULT]

ignoreip = 127.0.0.1/8 
bantime = 3600
findtime = 600
maxretry = 5

# configure nftables
chain     = input
banaction = nftables-multiport
banaction_allports = nftables-allports

# Destination email for action that send you an email
destemail = admin+fail2ban@localhost

# Sender email. Warning: not all actions take this into account. Make sure to test if you rely on this
sender    = admin+fail2ban@localhost

# Simply ban
action    = %(action_)s
```

## Filter Configuration ##

Now for the last category of configuration files: Filter.

Filter category is the law.

Filter helps to define aberrant behavior in order to determine if jail is needed 
or not.  Filter do not determine the severity of the punishment, just that a law
has been broken.

You can easily create filters to catch such network-based (and host-based) scofflaws.

Now to test the actual ban in action

```console
$ fail2ban-client ban 127.0.0.1 sshd
```

