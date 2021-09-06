title: Bash Scripts Startup Ordering
date: 2020-06-03 10:56
modified: 2020-12-03 15:16
status: published
tags: bash, shell, script
category: HOWTO
summary: What are the execution order of the many Bash shell scripts?

This article will explain the execution sequence of the many bash shell script files.

The current (and well-established) ordering of such bash shell scripts are:

    /etc/profile
    /etc/profile.d/*.sh  # New in Debian 9
    ~/.bash_profile
    ~/.bashrc
    /etc/bashrc  # sourced by ~/.bashrc
    ~/.bash_login
    ~/.profile
    ~/.profile.d/*.sh  # New in Debian 9
    ~/.bash_logout

[jtable]
Script name, login, UNIX pipe, bash, sh, Debian9, note
`/etc/profile`, Y, Y, Y, Y, Y
`/etc/bash.bashrc`, Y, Y, Y, Y, Y, called by `/etc/profile`
`/etc/profile.d/*.sh`, N, N, N, N, Y, called by `/etc/profile`
`~/.bash_profile`, Y, ?, ?, ?, ?, ?
`~/.bashrc`
`/etc/bashrc`
`~/.bash\_login`, Y, n, Y, n, Y
`~/.profile`, Y, n, Y, Y, Y
`~/.profile.d/*.sh`, Y, Y, Y, Y, Y
`~/.bash_logout`

[/jtable]

Shell Classes
=============

There are two classes of shell sessions:

1.  Interactive shell session
2.  Non-interactive shell session

Best way to differentiate the two different classes of shell sessions is 
by whether the user gets to directly interact with the process of its 
bash shell session.

There are four types of shell environments (over 2 classes of shell sessions) that will selectively execute the aforementioned bash shell scripts:

A)  Interactive Shell Session
 1.  Login 
 2.  Terminal (aka Non-login)
B)  Non-interactive Shell Session
 3.  Unix Pipe
 4.  Daemon

Interactive Shell Sessions
==========================

To interact with a shell session, a terminal device 
(such as `/dev/tty1` or `/dev/pty0`) is used to relay interactive 
information of a keyboard and a display with this process.

Such interactive shell may have a login session, a terminal session, 
a GUI-based terminal session.  These kinds of shell may be remotely
interactive over network or local to your PC's OS.  But the key point
is that a user is involved ... directly.

Some daemons that evoke `-login` are:

A) local daemons
 * `getty`
 * `vgetty`
B) remote daemons
 * `sshd`
 * `telnetd`


Execution sequence for interactive login shell
==============================================

Following pseudo code explains the sequence of execution of these files
for the interactive login shell session.  Such interactive login shell 
sessions may be provided by `getty`, `vgetty`, `sshd`, or `telnetd`.

Written in bash ONLY for logic readability here.  System binaries 
and a few scripts will do the execution of shell script files for you.
```bash
source /etc/profile
if [ -e ~/.bash_profile ];  then
  if [ -r ~/.bash_profile \; then
    source ~/.bash_profile
  else
    echo "Error reading ~/.bash_profile"
  fi
else
  if [ -e ~/.bash_login ]; then
    if [ -r ~/.bash_login \; then
      source ~/.bash_login
    else
      echo "Error reading ~/.bash_login"
    fi
  else
    if [ -e ~/.profile ]; then
      if [ -r ~/.profile ]; then
        source ~/.profile
      else
        echo "Error reading ~/.profile"
      fi
    fi
  fi
fi
```
Above are also duplicated in KDE SDDM `/etc/sddm/wayland.session` and X11 session
`/etc/sddm/X11.session`.

When you logout of the interactive shell, following is the 
execution sequence:

```bash
if [ -f ~/.bash_logout ]; then
  if [ -r ~/.bash_logout ]; then
    source ~/.bash_logout
  else
    echo "Error reading ~/.bash_logout"
  fi
fi
```

Note that system-provided `/etc/bashrc` is optional but ONLY 
executed by user's `~/.bashrc` as shown below:

```bash
# cat ~/.bashrc
if [ -f /etc/bashrc ]; then
  if [ -r /etc/bashrc ]; then
    . /etc/bashrc
  else
    echo "Error reading /etc/bashrc"
  fi
fi
```

Interactive Non-login Shell
---------------------------

Non-login interactive shell get created by being:

1. forked off by the user's login shell via another (i.e., `bash`) shell
2. created by user's GUI Desktop Manager (i.e., `xterm`, `gnome-terminal`)
3. spawned by application via `execv()`-class of system functions.
4. rarely by daemon or cron jobs (i.e. serial port access or dedicated second
   video display in terminal session mode.)

While launching a non-login interactive shell, following is the sequence of execution:

Written in bash ONLY for readability.  System binaries and a few scripts
will do the execution of shell script files for you.
```bash
if [ -e ~/.bashrc ]; then
  if [ -r ~/.bashrc ]; then
    source ~/.bashrc
  else
    echo "Error reading ~/.bashrc"
  fi
fi
```

Non-interactive Shell Session
=============================

It is important to recognize that there are some things that a bash 
shell SHOULD NOT execute from within an non-interactive shell.

Also that there are some things for an non-interactive shell session
that a bash shell WOULD NOT be doing (because it only impacts 
interactive shells.)

Non-interactive shell has no such direct interaction with a user: no 
keyword, no display.

There are "indirect" interactions between the user and such 
non-interactive shell sessions.  
Such activity types of indirect interaction may be accomplished by a 
user from within its existing interactive shell session having to be
communicating control information toward a non-interactive shell, 
using one or more of the following methods:

1. Sending UNIX signal 
2. Using UNIX socket or IPC to communicate control data
3. Using shared memory to communicate control data
4. Creating or updating a file for a non-interactive shell process to pick up
5. Operating system-assisted enclave (i.e., TPM, spinlock).

That's all for now.

References
==========
* [Bash Startup Files](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html)
