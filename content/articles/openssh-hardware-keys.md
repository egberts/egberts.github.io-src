title: OpenSSH Hardware Keys and `SSH_SK_PROVIDER` envvar (FIDO2 and U2F)
date: 2022-03-14T12:20
status: published
tags: ssh, OpenSSH
category: research
lang: en
private: False


The OpenSSH tools use the `$SSH_SK_PROVIDER` environment variable to
point to the middleware, though all tools that support security keys
accept dedicated command-line or configuration options (e.g. `ssh_config`
SecurityKeyProvider). This provider needs to be available for key
generation and signing (e.g. pubkey authentication) operations.

```bash
$ SSH_SK_PROVIDER=/path/to/libsk-libfido2.so
$ export SSH_SK_PROVIDER
$ ssh-keygen -t ecdsa-sk
```

You will typically need to tap your token to confirm the keygen
operation, but once complete this will yield a keypair at
`~/.ssh/id_ecdsa_sk`. It can be used much like any other key -
`id_ecdsa_sk.pub` can be copied to a server's `authorized_keys` file and
can be used for authentication, Note that the server only verifies
signatures, so it doesn't need to communicate with tokens.

Reference
====
* https://lists.mindrot.org/pipermail/openssh-unix-dev/2019-November/037999.html)
