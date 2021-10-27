title: Fine-tuning SSH authorized\_keys
date: 2020-10-26 08:00
status: published
tags: SSH
category: HOWTO
summary: How to restrict SSH session using options in `~/.ssh/authorized_keys`.
lang: en
private: False

How to fine-tune the `~/.ssh/authorized_keys` on SSH servers to restrict certain
behavior of its shell session.

Often times, you want to govern how the SSH shell session should behave
for a specific SSH client user.

This can be done if the SSH client user supplied its own public key for
inclusion into the remote SSH server (in `/home/user/.ssh/authorized_keys`.

There are several options in which to tack on to a specific line of the
`authorized_keys` file.

The common options are:

* `no-port-forwarding`
* `no-X11-forwarding`
* `no-agent-forwarding`
* `no-pty`
* `tunnel="1"`
* commands="sh /etc/netstart tun1"

First four is useful for `git-shell` and its remote Git repository provided by
git-daemon package.

The complete list of options are given in ssh-keygen (`man ssh-keygen`) manpage under 'Certificate' section.
