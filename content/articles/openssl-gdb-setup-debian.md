title: GDB Setup for OpenSSL for Debian
date: 2022-03-19 19:02
status: published
tags: gdb, OpenSSL
category: HOWTO
summary: How to properly setup OpenSSL for a gdb debug session in Debian.
lang: en
private: False

Preparing GDB
=============
Install GDB:
```bash
# apt install gdb
```

Add Automatic Debug Package to APT
==================================
Add debug symbols repository support by adding a config file 
to `/etc/apt/sources.list.d` subdirectory that contains:

```bash
deb http://deb.debian.org/debian-debug/ $RELEASE-debug main
# for security updates
deb http://deb.debian.org/debian-debug/ $RELEASE-proposed-updates-debug main
```

Replace the `$RELEASE` with your current Debian release name (mine is `bullseye`).

```console
$ cat << SRC_LIST_EOF | tee /etc/apt/sources.list.d/debian-debug.list 

deb http://deb.debian.org/debian-debug/ bullseye-debug main

# for security updates
deb http://deb.debian.org/debian-debug/ bullseye-proposed-updates-debug main
SRC_LIST_EOF

$ apt update
$ find-dbgsym-packages /usr/bin/openssl
# nothing there

$ apt search libssl1.1-dbgsym
# nothing there

$ apt-file search /usr/bin/openssl
openssl: /usr/bin/openssl
# YEAH! openssl is the package name

# Now go find all shared library needing debug symbols
$ ldd /usr/bin/openssl
	linux-vdso.so.1 (0x00007ffe133ca000)
	libssl.so.1.1 => /lib/x86_64-linux-gnu/libssl.so.1.1 (0x00007efe043c1000)
	libcrypto.so.1.1 => /lib/x86_64-linux-gnu/libcrypto.so.1.1 (0x00007efe04044000)
	libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007efe04023000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007efe03e4a000)
	libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007efe03e44000)
	/lib64/ld-linux-x86-64.so.2 (0x00007efe04564000)
```

In my API troubleshooting effort, I need debug symbols AND source lines for both `libssl.so.1.1` and `libcrypto.so.1.1`.

Find the packages associated with those two shared library files:
```console
$ apt-file search libssl.so.1.1
libssl1.1

$ apt-file search libcrypto.so.1.1
libssl1.1
```
So both shared libraries of interest are provided by the same Debian `libssl1.1` package.

In OpenSSL's case, there is no debug symbol support for OpenSSL nor its shared library `libssl1.1`.  We must do meatball surgery.

Preparing Rebuild
=================

Create a working subdirectory to hold all this:

```bash
mkdir build
cd build
```

Note that you can skip the rebuilding part and go straight to running gdb, but it is unlikely that you will get a useful backtrace. (If the build-dep line fails, check you have deb-src lines in apt sources) 

Prepare the workstation for source rebuilding and gdb environment:
```console
# apt install build-essential fakeroot gdb
# apt build-dep openssl
# apt build-dep libssl1.1
```

Several `*.deb` packages get created in that working directory.

```console
# DEB_BUILD_OPTIONS="nostrip noopt" apt -b openssl
# DEB_BUILD_OPTIONS="nostrip noopt" apt -b libssl1.1
```

Find the `*.deb` packages in the `build` directory
```console
# ls *ssl*.deb
openssl_1.1.1k-1+deb11u1_amd64.deb
libssl1.1_1.1.1k-1+deb11u1_amd64.deb 
```

Install the two newly unstripped-debug packages.
```console
# apt install ./openssl_1.1.1k-1+deb11u1_amd64.deb
# apt install ./libssl1.1_1.1.1k-1+deb11u1_amd64.deb
```

You can ensure the binaries installed from your .deb have debugging symbols with the `file` command, or with `gdb` itself (see below). 

```console
$ file /usr/bin/openssl  # output should contain "not stripped"
```

Rebuilding OpenSSL Debug Symbol
===============================

Sometimes I would patch the OpenSSL and this would be an opportunity to introduce debug symbols via `CFLAGS` and `configure`.

If using OpenSSL v3+, use `Configure`.
If using OpenSSL v1+, use `config`.

```bash
./config --prefix=/usr/local/ssl \
         --openssldir=/usr/local/ssl \
         --debug -O0 -g -ggdb \
         -ggdb3 -g3 \
         -fno-omit-frame-pointer -fno-inline \
         zlib \
         no-ssl2 no-ssl3
make clean
make -j6
```

Despite what bloggers and mailing lists say, do not bother with the `shared` option in my example: you will just not be able to debug deep down into the OpenSSL library (as opposed to having OpenSSL library getting folded into your binary executable with my example).


Preparing GDB Init File
=======================

My example `.gdbinit` RC script that gets loaded each time `gdb` gets run can look like this.  This RC script is customized for an `openssl` using shared library but will work just fine with static-built `openssl` executable binary.:

```gdb
# File: .gdbinit
set auto-load safe-path /
add-auto-load-safe-path ~/work/github/tls-ca-manage/examples/.gdbinit

# Automatically loads shared object (.so) library
# Turn off if using disparate target (from host) during a remote GDB session
set auto-solib-add on
set pagination 0

#
sharedlibrary libssl1.1

directory ./libssl1.1/
directory ./openssl-1.1.1k/
directory ./openssl-1.1.1k/crypto/
directory ./openssl-1.1.1k/crypto/x509v3/

symbol-file ./openssl-1.1.1k/apps/openssl/
symbol-file /lib/x86_64-linux-gnu/libssl.so.1.1/

set args req -config /etc/ssl/etc/AcmeComponent-ca__ocsp__AcmeOCSP__req.cnf -reqexts ocsp_AcmeComponent_reqext -new -key /etc/ssl/private/AcmeOCSP.key -sha256 -out /etc/ssl/certs/AcmeOCSP.csr

break main
break do_cmd
break req_main
break auto_info
break X509V3_EXT_REQ_add_nconf

run
```

GDB init (`.gdbinit`) file can be placed in the same directory or in your `$HOME` directory.  


Starting GDB
============

After rebuilding the `openssl`, start up the GDB:

```console
cd build

# start the debug-unstripped executable
$ gdb -q openssl-1.1.k/build_shared/apps/openssl

# or
# start the static (no shared library) but debug-unstripped version executable
$ gdb -q openssl-1.1.k/build_static/apps/openssl
```

Enjoy!

Capturing Reproducible Crash Report
====================================

For including a backtrace in a bug report, you can run this command and then try to reproduce your crash:

```console
$ gdb -batch -n \
    -ex 'set pagination off' \
    -ex run \
    -ex bt \
    -ex 'bt full' \
    -ex 'thread apply all bt full' \
    --args openssl-1.1.1k/build_static/apps/openssl verify -help
```

References:
===========
* https://wiki.debian.org/HowToGetABacktrace?highlight=%28CategoryDebugging%29
