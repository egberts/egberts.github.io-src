title: Enable long running process in systemd
date: 2020-08-11 14:52
modified: 2025-12-30T05:40
status: published
tags: systemd, process
category: HOWTO
summary: How to enable long-running process in systemd

Enabling Long-Running Process in Systemd
===========================

Beginning with systemd-230, all user processes gets killed when a user
session gets ended, even if `NOHUP` signal (via `nohup` command) gets used,
or the process uses the daemon() or setsid() functions.
This is a deliberate change from a historically permissive environment
to a more restrictive one.
The new behavior may cause issues if you depend on long running
programs (e.g., `screen` or `tmux`) to remain active after ending your
user session.
There are three ways to enable lingering processes to remain after
a user session ends.

Process Lingering for Selected Users
------------------------------------
Enable process lingering for selected users:
* Normal users have permission to enable process lingering with the
command loginctl enable-linger for their own user.
* System administrators can use the same command with a user argument
to enable for a user.  That user can then use the systemd-run command to
start long running processes. For example: `systemd-run --scope --user /usr/bin/screen`.
If you enable lingering for your user, the `user@.service` will remain even
after all login sessions gets closed, and will automatically start at
system boot. This has the advantage of explicitly allowing and
disallowing processes to run after the user session has ended,
but breaks backwards compatibility with tools like nohup and
utilities that use deamon().

System-wide Process Lingering
------------------------------

Enable system-wide process lingering:
You can set `KillUserProcesses=no` in `/etc/systemd/logind.conf` to enable
process lingering globally for all users.
This has the benefit of leaving the old method available to all users at
the expense of explicit control.

Disable at Build-Time
---------------------
Disable at build-time: You can enable lingering by default while
building systemd by adding the switch `-Ddefault-kill-user-processes=false`
to the meson command for systemd.
This disables the ability of systemd to kill user
processes at session end.

