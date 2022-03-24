title: Debugging Exim4 Daemon
date: 2022-03-21 01:50
status: published
tags: Exim4
category: HOWTO
summary: How to debug Exim4 daemon.
slug: exim4-daemon-debugging
lang: en
private: False


To debug the `exim4` daemon, stop the `exim4` daemon and run this:

Put yet another bash script into your `$HOME/bin` directory, I call this `exim4-daemon-debug.sh`:

```bash
#!/bin/bash
# File: exim4-daemon-debug.sh
# Title: Run exim4 in debug for troubleshooting
echo "Running exim4 daemon in debug mode ..."
echo

if [ "$USER" != 'root' ]; then
  echo "Must be in 'root' to debug exim4 daemon. Aborting ..."
  exit 255
fi

/usr/sbin/exim4 -bd -q30m -oX 587:465:25 -oP /run/exim4/exim.pid -d
echo $?

echo
echo "Done debugging exim4 daemon: exit code $retsts"
```
Then make it an executable:
```bash
chmod a+rx ~/bin/exim4-daemon-debug.sh
```

If you want to capture the output into a temporary file (e.g, `output.script`), do this step:
```bash
exim4-daemon-debug.sh 2>&1 > /tmp/exim4-output.script
``

To test SMTP protocol, use the awesome [`swaks`](http://www.jetmore.org/john/code/swaks/) tool to exercise this.  `swaks` is found in most distros' package library.  For more details on me using `swaks`, see [here]({file}swaks-quick-guide.md).

```console
swaks --to test@egbert.net --from somename@yahoo.com --server egbert.net --quit-after RCPT --hide-all
```

NOTE: Oh drat, after writing this article, I found my problem: I have inadvertly included the unwanted `--quit-after RCPT`.  So, I have fixed it for me.  Might get you further.


Then scan the intensive output for the output marker:

```console
<pid> ----------- end verify ------------
```

Look for the all of the lines with the starting word `check `:

First level check:
```console
grep -E "^[0-9]{1,6} check" /tmp/output.script
<pid> check !acl = acl_local_deny_exceptions
<pid> check recipients = ${if exists{/etc/exim4/local_rcpt_callout}{/etc/exim4/local_rcpt_callout}{}}
<pid> check !acl = acl_local_deny_exceptions
<pid> check senders = ${if exists{/etc/exim4/local_sender_blacklist}{/etc/exim4/local_sender_blacklist}{}}
<pid> check !acl = acl_local_deny_exceptions
<pid> check hosts = ${if exists{/etc/exim4/local_host_blacklist}{/etc/exim4/local_host_blacklist}{}}
```

All-level checks:
```console
grep -E "^[0-9]{1,6}\s+check" /tmp/output.script
15445 check !acl = acl_local_deny_exceptions
15445  check hosts = ${if exists{/etc/exim4/host_local_deny_exceptions}{/etc/exim4/hos
t_local_deny_exceptions}{}}
15445  check senders = ${if exists{/etc/exim4/sender_local_deny_exceptions}{/etc/exim4
/sender_local_deny_exceptions}{}}
15445  check hosts = ${if exists{/etc/exim4/local_host_whitelist}{/etc/exim4/local_hos
t_whitelist}{}}
15445  check senders = ${if exists{/etc/exim4/local_sender_whitelist}{/etc/exim4/local
_sender_whitelist}{}}
15445 check recipients = ${if exists{/etc/exim4/local_rcpt_callout}{/etc/exim4/local_r
cpt_callout}{}}
15445 check !acl = acl_local_deny_exceptions
15445  check hosts = ${if exists{/etc/exim4/host_local_deny_exceptions}{/etc/exim4/hos
t_local_deny_exceptions}{}}
15445  check senders = ${if exists{/etc/exim4/sender_local_deny_exceptions}{/etc/exim4
/sender_local_deny_exceptions}{}}
15445  check hosts = ${if exists{/etc/exim4/local_host_whitelist}{/etc/exim4/local_hos
t_whitelist}{}}
15445  check senders = ${if exists{/etc/exim4/local_sender_whitelist}{/etc/exim4/local
_sender_whitelist}{}}
15445 check senders = ${if exists{/etc/exim4/local_sender_blacklist}{/etc/exim4/local_
sender_blacklist}{}}
15445 check !acl = acl_local_deny_exceptions
15445  check hosts = ${if exists{/etc/exim4/host_local_deny_exceptions}{/etc/exim4/hos
t_local_deny_exceptions}{}}
15445  check senders = ${if exists{/etc/exim4/sender_local_deny_exceptions}{/etc/exim4
/sender_local_deny_exceptions}{}}
15445  check hosts = ${if exists{/etc/exim4/local_host_whitelist}{/etc/exim4/local_hos
t_whitelist}{}}
15445  check senders = ${if exists{/etc/exim4/local_sender_whitelist}{/etc/exim4/local
_sender_whitelist}{}}
15445 check hosts = ${if exists{/etc/exim4/local_host_blacklist}{/etc/exim4/local_host
_blacklist}{}}
```

References
==========
* [My Debugging Effort with RCPT TO: and Exim4]({filename}exim4-inbound-filtering.md)
