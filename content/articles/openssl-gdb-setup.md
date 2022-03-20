title: GDB Setup for OpenSSL
date: 2022-03-16 11:12
status: published
tags: gdb, OpenSSL
category: HOWTO
summary: How to properly setup OpenSSL for a gdb debug session 
lang: en
private: False

Rebuilding OpenSSL
==================
if using OpenSSL v3+, use `Configure`.
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

What does all these options mean?

`


Preparing GDB Init File
=======================
GDB init (`.gdbinit`) file can be placed in the same directory or in your \$HOME directory.  A typical GDB init file has the following:

```ini
set auto-load safe-path /
break main
run
```

Starting GDB
============

After rebuilding the `openssl`, start up the GDB:

```console
cd \<your-work-area\>

gdb -q ~/work/github/openssl/apps/openssl
```

Enjoy!
