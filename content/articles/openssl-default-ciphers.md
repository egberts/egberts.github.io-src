title: Change Default TLS Setting in OpenSSL, System-Wide
date: 2022-03-20 06:16
status: published
tags: OpenSSL, TLS
category: HOWTO
summary: How to change the default TLS settings system-wide for openssl.
slug: openssl-default-ciphers
lang: en
private: False

Many utilities and tools often make uses of OpenSSL libraries.

Bet you did not know that those APIs in `openssl.so.1.1` library all often consult the `/usr/lib/ssl/openssl.cnf` as a default?  Even if you executed a simple `openssl version`.

A long long time ago and far away, I had once thought that a shared library should not reference a fixed file location or compiled-in a hardcoded file specification.  Time has changed.

Even recently, I thought it was hardcoded ONLY (and ONLY) to `/etc/ssl/openssl.cnf`, but nooooooooo.

You can easily prove it without looking at the OpenSSL code:
```console
strace -f /usr/bin/openssl verrsion 2>&1 | grep open
execve("/usr/bin/openssl", ["/usr/bin/openssl", "version"], 0x7ffe9e472dd0 /* 44 vars */) = 0
<snipped many gibberish output>
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
<snipped many gibberish output>
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpthread.so.0", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libdl.so.2", O_RDONLY|O_CLOEXEC) = 3



openat(AT_FDCWD, "/usr/lib/ssl/openssl.cnf", O_RDONLY) = 3



newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=11118, ...}, AT_EMPTY_PATH) = 0
read(3, "#\n# OpenSSL example configuratio"..., 4096) = 4096
read(3, "F8Strings).\n# MASK:XXXX a litera"..., 4096) = 4096
brk(0x55ab0655c000)                     = 0x55ab0655c000
read(3, "icConstraints=CA:FALSE\n\n# Here a"..., 4096) = 2926
read(3, "", 4096)                       = 0
close(3)                                = 0
exit_group(0)                           = ?
+++ exited with 0 +++
```
I spaced the line apart out for easier viewing.  Notice that it even read the entire `/usr/lib/ssl/openssl.cnf`, and loaded it.

First thought now then was "I thought I had disabled TLS 1.2" in `/etc/ssl/openssl.cnf` earlier; this is not the way to do default changing for TLS by OpenSSL.

What is the deal?  

I was faced with two separate problems:

* Wrong default location for an `openssl.cnf` file
* Wrong configuration settings between TLS versions

OK, I got that first part right ... now.

But the part about "Between TLS versions?" (sigh)


OpenSSL 1.1 New TLS API
=======================
OpenSSL 1.1 uses an independent, new interface to set ciphersuites for TLSv1.3, the old ciphersuites interface is only effective up to TLSv1.2.

So any changes of default settings for TLSv1.2 will have no effect toward TLSv1.3. 

Now a few applications has adopted the new interface, there is a DIFFERENT way to change ciphersuites for TLSv1.3.

I'll document those so that every program in the system will use your preferred default settings (let me guess, just TLSv1.3 only, right?)

You can change the global `openssl.cnf`.  Just that it is not where (most of) you expected.  Again, it is not in `/etc/ssl/openssl.cnf` (nor RedHat-family `/etc/pki/openssl.cnf`).  (hint: it is mentioned earlier).

To modify the default TLSv1.3 ciphersuites for OpenSSL itself, so every program in the system will use the ciphersuites you specified:

```console
sudo nano /usr/lib/ssl/openssl.cnf
```
and add the following at the end of the config file:
```ini
openssl_conf = default_conf

[default_conf]
ssl_conf = ssl_sect

[ssl_sect]
system_default = system_default_sect

[system_default_sect]
# Note: TLSv1.2 ciphersuites are configured in the "CipherString" setting,
#       whereas TLSv1.3 ciphersuites in the "Ciphersuites" setting.
#       Don't mix and match between the two!!
# Ciphersuites = TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
Ciphersuites = TLS_CHACHA20_POLY1305_SHA256:TLS_AES_256_GCM_SHA384:TLS_AES_128_GCM_SHA256


CipherString = DEFAULT@SECLEVEL=2

Options = PrioritizeChaCha,-MiddleboxCompat,-SessionTicket,-Compression,-DHSingle,-ECDHSingle,ServerPreference,-AllowNoDHEKEX

MinProtocol = TLSv1.3
```

Detailed break down of the above snippet:

```ini
openssl_conf = default_conf

[default_conf]
ssl_conf = ssl_sect
```

`openssl_conf` is one of the many OpenSSL built-in attributes.

A custom-named `default_conf` section name is assigned to `openssl_conf`.  It is now telling OpenSSL to follow to the next section named `default_conf` for any attribute settings.

`[default_conf]` denotes a new section (in INI-parlance) containing new settings.

`ssl_conf` is also one of many built-in attributes.  It holds the TLS/SSL settings.

`ssl_sec` is the section name to follow for TLS/SSL settings.  This section name is user-definable.

`[ssl_sect]` is a new section to contain TLS/SSL settings.

`system_default` is a built-in attributes to hold system default settings.

`system_default_sect` is the section name to find and take in more settings; the name is user-definable.

`[system_default_sect]` is the user-definable section which contains settings related to TLS/SSL ciphersuites.

`Ciphersuites` is the new built-in OpenSSL (v1.1+) attributes.  It contains a list of algorithms to support.

`TLS_CHACHA20_POLY1305_SHA256:TLS_AES_256_GCM_SHA384:TLS_AES_128_GCM_SHA256` is the author's choice of algorithms to use.  It is not the best, could be better, but it a demonstration that puts ChaCha20-Poly1305 in the forefront during the TLS negotiation stage of server/client algorithms.

`CipherString` is an existing built-in OpenSSL attributes.  It contains a special notation to control availability of selected TLSv1.2 algorithms.

`DEFAULT@SECLEVEL=2` states to use only security level 2.


RECAP
=====
New sections, new attributes.

New section-related attributes are:

* `openssl_conf`  # that covers also `libssl.so`
* `system_conf`
* `ssl_conf`

New `ssl_conf`-related attributes are:

* `system_default`
* `Ciphersuites`
* `MinProtocol`
* `PrioritizeChaCha`

Some notable ones (but not mentioned in this article).

* `RSA.Certificate`
* `ECDSA.Certificate`
* `Ciphers = ALL:!RC4`

SUMMARY
=======

Only need to remember one thing, `-cipher` is no longer a viable option with `openssl`.

It is now called `-ciphersuites`.


References
===========

* `man 3ssl SSL_CONF_cmd_value_type`  (part of `libssl1.1-doc` package)
* `TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256`
