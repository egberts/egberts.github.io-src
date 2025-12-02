title: Invalid SSHFP DNS resource record
date: 2022-04-03 07:38
modified: 2025-12-02 12:25
status: published
tags: DNS, SSHFP
category: HOWTO
summary: How to use fix invalid SSHFP RR in DNS with OpenSSH
slug: dns-rr-sshfp-invalid
lang: en
private: False

You ever get the following pesky prompts during an initial SSH login?

```console
ssh host.domain.example
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ED25519 key sent by the remote host is
SHA256:XxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx.
Please contact your system administrator.
Update the SSHFP RR in DNS with the new host key to get rid of this message.
Warning: Permanently added '[host.domain.example.]:22,[192.168.1.1]:22' (ED25519) to the list of known hosts.
</etc/motd content goes here>
user@host.domain.example.'s password: 
```

The key thing to note in the above output is the following line:

```
Update the SSHFP RR in DNS with the new host key to get rid of this message.
```

It means exactly what it means.

The `VerifyHostKeyDNS yes` in your local SSH client config is what 
controls that output; the config being either in `$USER/.ssh/config` or in `/etc/ssh/ssh_config`.

The above decision is based on a simple comparison between:

* authoritative nameserver holding the `SSHFP` zone data of this host.domain.example
* The SSH server of host.domain.example providing the public key

This message covers 99.999% of the scenario.

* `sshd` is not using the same pubkey, possibly due to:
    * shell aliased your `ssh` command
    * different set of config file (via `sshd -c <config_file>`)
    * `AuthorizedKeyFile` had been change
    * fingerprint hash (`FingerprintHash`) setting had been changed
    * `PubkeyAcceptedKeyTypes` had been changed
    * `CASignatureAlgorithms` had been changed
    * `TrustedCAUserKeys` had been changed

The other 0.001% of the time is broken down in one of the many not so common scenarios:

* points to a different SSH server
    * a new port number has been opened (legitimately or not)
    * Dockerized container reusing same IP address
    * MAC address has been changed to point to a cloned server
    * IP route has been changed (by route table or by various IP route protocol like BGP, OSPF, RIP)
    * a ghost daemon replaced the ones that your server's `systemd start sshd.service` and is using its own SSH server public key.


At any rate, once you've eliminated the 0.001%, it is a simple matter of:

* Generate new `SSHFP` DNS record (`ssh-keyscan -r host.domain.example`); save the output to an editor buffer
* Identifying the authoritative nameserver of `domain.example` (`dig domain.example. soa` and note the `MNAME` portion of SOA record data).
* Log in as root on that `MNAME` authoritative nameserver of `host.domain.example`
* go to the correct config file of nameserver (ISC Bind9 is `/etc/named.conf`; newer Bind v9.11+ shows default config via `named -V`)
* Note the database file name of the `domain.example` zone. (ISC Bind9 is `file /var/lib/bind/db.domain.example`)
* change the directory to where that zone database file is located at
* Edit the `db.domain.example` file.
* paste the new `SSHFP` DNS records from the editor buffer that you saved in the first step.

Enjoy!
