title: Debugging boot sequence in systemd
date: 2020-08-11 10:13
status: published
tags: systemd, debugging, boot
category: research
summary: How to debug boot sequence in systemd

Debugging the Boot Sequence
===========================

Rather than plain shell scripts used in SysVinit or BSD style init 
systems, `systemd` uses a unified format for different types of startup 
files (or units). 
The command `systemctl` is used to enable, disable, control state, and 
obtain status of unit files. 
Here are some examples of frequently used commands:

```bash
# lists loaded unit files of type service.
systemctl list-units -t <service> [--all]

# lists loaded unit files of type target.
systemctl list-units -t <target> [--all]

# shows all units that depend on the multi-user target. 
# Targets are special unit files that are anogalous to 
# runlevels under SysVinit.
systemctl show -p Wants <multi-user.target>

# shows the status of the servicename service. 
The `.service` extension can be omitted if there are no other unit 
files with the same name, such as `.socket` files (which create a 
listening socket that provides similar functionality to inetd/xinetd).
systemctl status <servicename.service>
```

