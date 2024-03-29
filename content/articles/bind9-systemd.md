title: Bind9 Systemd
date: 2021-10-15 08:13
status: published
tags: Bind9, DNS, split-horizon
category: research
summary: Pick up the latest systemd unit files for ISC Bind9
slug: systemd-isc-bind9
lang: en
private: False


Systemd for Bind9 has been redesigned here for allowing multiple instances 
of named daemon.

This unit name is `bind9@.service`.

```ini
#
# File: bind9@.service
# Path: /etc/systemd/system
# Title: ISC Bind9 named daemon systemd unit
# Systemd version: v247.3-7
# Sysmted-analyze security: 7.0 MEDIUM
# Creator: 512-dns-bind9-systemd.sh
# Created on: Fri Apr 22 11:55:05 AM EDT 2022
# Description:
#
#   An instantiation of bind9.service to support
#   bastion DNS hosting (multiple DNS servers on
#   multi-home gateway)
#
#   Cannot use '-f' nor '-g' option in this Bind9 
#   named setup without additional but intensive 
#   changes.
#
#   NAMED_CONF string contains a file spec to the named configuration file
#     NAMED_CONF defaults to /etc/bind/named.conf as specified in
#     the bind9@.service file.
#     NAMED_CONF must be defined so that named-checkconf syntax-checker
#     can pre-validate the configuration file before startup.
#
#   NAMED_OPTIONS string must be defined in /etc/default/bind9
#     Useful examples:
#        NAMED_OPTIONS="-p 53 -s"  # open port 53/udp and write stats
#        NAMED_OPTIONS="-d 63"     # turn on various debug bit flags
#        NAMED_OPTIONS="-4"        # restrict to IPv4 net family
#
#   RNDC_OPTIONS string contains option settings for `rndc` to
#     perform stop or reload command.
#     Default example: RNDC_OPTIONS="-p 953 -s 127.0.0.1"
#
#   As a legacy, /etc/default/bind9-%I environment settings
#   are read in to overwrite any defaults that are set before.
#
# References:
#   * https://bind9-users.isc.narkive.com/qECPVuuu/enable-systemd-hardening-options-for-named
#
#
[Unit]
Description=ISC BIND9 nameserver for '%I' instance
Documentation=https://github.com/egberts/systemd-bind9
Documentation=https://bind9.readthedocs.io/
Documentation=man:named(8)
After=network.target
Wants=nss-lookup.target
Before=nss-lookup.target
# AssertFileIsExecutable=/usr/sbin/named
# AssertFileIsExecutable=/usr/sbin/rndc
# AssertPathIsDirectory=/%I
# AssertFileIsExecutable=
# AssertFileIsExecutable=/usr/sbin/rndc
# AssertPathExists=/var/lib/bind/%I
# AssertPathIsDirectory=/var/lib/bind/%I
# AssertPathIsReadWrite=/var/lib/bind/%I

# ArchLinux
# AssertPathExists=/var/named/%I
# AssertPathIsDirectory=/var/named/%I
# AssertPathIsReadWrite=/var/named/%I

# We rely on /etc/tmpfiles.d/ for our /run/named needs
# systemd v247 has not perfected /run/named/XXXX yet
# maintainer puts one in /usr/lib/tmpfiles.d/named.conf
# we override one from /etc/tmpefiles.d/named.conf
ConditionPathExists=/run/named
ConditionPathIsDirectory=/run/named
ConditionPathExists=/run/named/%I
ConditionPathIsDirectory=/run/named/%I
ConditionPathIsReadWrite=/run/named/%I

# ConditionPathExists=/var/cache/named
# ConditionPathIsDirectory=/var/cache/named

# ConditionPathExists=/var/cache/named/%I
# ConditionPathIsDirectory=/var/cache/named/%I
# ConditionPathIsReadWrite=/var/cache/named/%I

#ConditionPathExists=/var/lib/named
#ConditionPathIsDirectory=/var/lib/named

#ConditionPathExists=/var/lib/named/%I
#ConditionPathIsDirectory=/var/lib/named/%I
#ConditionPathIsReadWrite=/var/lib/named/%I
#ReadWritePaths=/var/lib/named/%I

#ConditionPathExists=/var/log/named/%I
#ConditionPathIsDirectory=/var/log/named/%I
#ConditionPathIsReadWrite=/var/log/named/%I
#ReadWritePaths=/var/log/named/%I

# ReadOnlyPaths=+/etc/bind/
# ReadOnlyPaths=+/etc/bind/*
# ReadOnlyPaths=+/etc/bind/*/*
# ReadWritePaths=+/
# ReadWritePaths=+/var/lib/named/%I
# ReadWritePaths=+/var/named/%I

#ReadWritePaths=-/run/named
#ReadWritePaths=-/run/named/%I

[Service]
Environment=
Environment=SYSTEMD_LOG_LEVEL=debug

Type=simple

# resources
DeviceAllow=/dev/random r
DeviceAllow=/dev/urandom r
InaccessiblePaths=/home
InaccessiblePaths=/opt
InaccessiblePaths=/root

# Define defaults settings that can be overwritten by
# SysV /etc/default/bind9-%I environment setting files.
Environment=NAMED_CONF="/etc/bind/%I/named.conf"
Environment=NAMED_OPTIONS="-c /etc/bind/%I/named.conf"
Environment=RNDC_OPTIONS="-s %I"

EnvironmentFile=-/etc/default/bind9
# instantiation-specific Bind environment file is absolutely required
EnvironmentFile=/etc/default/bind9-%I

# Far much easier to peel away additional capabilities after
# getting a bare-minimum cap-set working
# h.reindl at thelounge.net:
CapabilityBoundingSet=CAP_CHOWN CAP_SETGID CAP_SETUID CAP_SYS_ADMIN CAP_DAC_OVERRIDE CAP_KILL CAP_NET_ADMIN CAP_NET_BIND_SERVICE CAP_NET_BROADCAST CAP_NET_RAW CAP_IPC_LOCK CAP_SYS_CHROOT
AmbientCapabilities=CAP_NET_BIND_SERVICE

# User/Group
# If you set 'DynamicUser=true', MANY subdirectories will be created
# under /var/cache, /var/log, /var/run; save yourself some pain, don't do that.
# TO undo this accident, rm /var/[(log|run|cache)/(named|bind)
# and restore via 'mv /var/log/private/named /var/log/'
# and restore via 'mv /var/run/private/named /var/run/'
# and restore via 'mv /var/cache/private/named /var/cache/'
DynamicUser=false
User=bind
Group=bind

# File Security settings
NoNewPrivileges=true
ProtectHome=true
ProtectKernelModules=true
ProtectKernelTunables=true
ProtectControlGroups=true

###RootDirectory=/
UMask=0007
LogsDirectory=named/%I
LogsDirectoryMode=0750

ConfigurationDirectory=bind/%I
ConfigurationDirectoryMode=0755

# **
# Tmpfiles
PrivateTmp=false


# RuntimeDirectory=named/%I
# RuntimeDirectoryMode=0755

# Home directory (instantiation-excluded)
WorkingDirectory=/var/cache/named

# systemd v251
CacheDirectory=named/%I
CacheDirectoryMode=0750

# State directory (Bind9 database files, static/dynamic)
StateDirectory=named/%I
StateDirectoryMode=0750

# named takes care of the PID and stores it in /run/named/%I
#PIDFile=/run/named/%I/named.pid

# Errors in ExecStart can be seen in syslog-ng/rsyslog with facility.severity of daemon.* 
# Does not seem to be an easy way to 'grep' the journalctl streams, hence syslog remains
# maybe  'journalctl -p0..6 -xb | grep named-checkconf'
# or a quicker 'ag named-checkconf /var/log/daemon.log'
ExecStartPre=/usr/sbin/named-checkconf -jz $NAMED_CONF
ExecStart=/usr/sbin/named -f -u bind $NAMED_OPTIONS -c $NAMED_CONF

# rndc will dovetail any and all instantiations of
# Bind9 'named' daemons into a single rndc.conf file
# and use its '-s <server>' as a reference from
# this rndc.conf config file.
ExecReload=/usr/sbin/rndc $RNDC_OPTIONS reload
ExecStop=/usr/sbin/rndc $RNDC_OPTIONS stop
#ExecStop=/bin/sh -c /usr/sbin/rndc stop > /dev/null 2>&1 || /bin/kill -TERM 

# No need for 'KillMode=process' unless cgroups get disabled
RestartSec=5s
Restart=on-failure

[Install]
WantedBy=multi-user.target


# Additional settings mentioned but not tested from
#   various Linux distros and ISC bind9-users
# CapabilityBoundingSet=CAP_SYS_RESOURCE
# IgnoreSIGPIPE=false
# LockPersonality=yes
# PermissionsStartOnly=True
# PrivateDevices=true
# PrivateMounts=yes
# ProtectKernelLogs=yes
# ProtectSystem=strict
# ReadWritePaths=/run/named /var/run/bind
# ReadWritePaths=/var/cache/bind
# RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6 AF_NETLINK
# RestrictRealtime=yes
# RestartPreventExitStatus=255
# SystemCallArchitectures=native
# Type=notify

```

The creator tool for the above file is located in [here (Github)](https://github.com/egberts/easy-admin/blob/main/500-dns/512-dns-bind9-systemd.sh).

And you can pick the latest version for bind9 on (system v247) in [here (Github)](https://github.com/egberts/systemd-bind9):



This [systemd template unit - freedesktop.org](https://www.freedesktop.org/software/systemd/man/systemd.service.html) is only for running multiple instances, commonly
found in "Multi-Daemon Split-Horizon" DNS setup.

