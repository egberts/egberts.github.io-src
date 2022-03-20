title: Environment Variables for OpenSSL
date: 2022-03-16 11:20
status: published
tags: OpenSSL
category: research
summary: Here are the list of environment variables used by OpenSSL
lang: en
private: False
slug: openssl-envvars

I've identified the following shell environment names used by `openssl` 
(by scanning for `getenv()` functions and few other code review tricks):

[jtable]
env var name, description, source
`CN`, commonName ,
`CTLOG_FILE_EVP`, Crypto CT, `crypto/ct/ct_log.c`
`HARNESS_OSSL_PREFIX`, , `apps.c`
`HOME`, User home directory specification, `crypto/rand/randfile.c`
`http_proxy`, ,
`https_proxy`, ,
`LEGACY_GOST_PKCS12`, GOST-related, `crypto/pkcs12/p12_mutl.c`
`no_proxy`, ,
`NO_PROXY`, ,
`OPENSSL`, ,
`OPENSSL_armcap`, Crypto Access for ARM architecture, `crypto/armcap.c`
`OPENSSL_CONF`, OpenSSL configuration file, `openssl.c`; `crypto/conf/conf_mod.c`; `util/wrap.pl`
`OPENSSL_CONFIG`, , `app/CA.pl`
`OPENSSL_CONF_INCLUDE`, util/wrap.pl
`OPENSSL_DEBUG_MEMORY`, Debug memory, `openssl.c`
`OPENSSL_DEBUG_DECC_INIT`, DEC VAX VMS, `vms_decc_init.c`
`OPENSSL_ENGINES`, , `crypto/engine/eng_list.c`; `util/wrap.pl`
`OPENSSL_FIPS`, FIPS, `openssl.c`
`OPENSSL_ia32cap`, Crypto Intel Itanium Architecture, `crypto/cryptlib.c`
`OPENSSL_MALLOC_FAILURES`, `malloc` test intrumentation point, `crypto/mem.c`
`OPENSSL_MALLOC_FD`, `malloc` file descriptor, `crypto/mem.c`
`OPENSSL_MODULES`, , `util/wrap.pl`
`OPENSSL_HTTP_PROXY`, ,
`OPENSSL_NO_PROXY`, ,
`OPENSSL_ppccap`, PowerPC-related crypto, `crypto/ppccap.c`
`OPENSSL_s390xcap`, ,
`OPENSSL_sparcv9cap`, ,
`OPENSSL_TEST_LIBCTX`, ,
`OPENSSL_TRACE`, ,
`RANDFILE`, a file specification to a random device, `crypto/rand/randfile.c`
`SSL_CIPHER`, , `apps/s_time.c`
`TEMP`, A pathname of a directory made available for programs that need a place to create temporary files.,
`TMP`, A pathname of a directory made available for programs that need a place to create temporary files.,
`TSGET`, ,
[/jtable]

NOTE: Above list are derived from `openssl` version 1.1.1k (11/18/2021).

Yeah, a lot of environment names there, accidential or not, to watch out for while using `openssl`.  

Expert
======

Bet you did not know that the `openssl` practically opens the default `/usr/lib/ssl/openssl.cnf` everytime you use the command.

Sometime, you have your own configuration file.  And you might think that specifying `-config my_damn_ssl_config_file.cnf` is all you get.  

What you actually get is the COMBINED part of the default config and your config together with your config file overwriting any older settings made in the default config.

What to do?  Usually, this is not a problem for most people.

What if you do not want this folding of default settings?

Let me show the way through using this `OPENSSL_CONF` environment variable; leave the assignment empty.  (You could put `/dev/null` instead).

```console
OPENSSL_CONF= openssl verify ...
```

How Did I Find Out
------------------

How did I find out about all this? After 8 months pouring over OpenSSL documentation and numerous blogs/websites/search-engines, it took an `strace -f` to catch this:

```console
$ strace -f /usr/bin/openssl req ... 2>&1 | grep -E '(open|stat)'
execve("/usr/bin/openssl", ["/usr/bin/openssl"], 0x7fff97693b48 /* 44 vars */) = 0
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
...  (ignore all the libraries)
openat(AT_FDCWD, "/usr/lib/ssl/openssl.cnf", O_RDONLY) = 3
newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=11118, ...}, AT_EMPTY_PATH) = 0
newfstatat(1, "", {st_mode=S_IFIFO|0600, st_size=0, ...}, AT_EMPTY_PATH) = 0
newfstatat(0, "", {st_mode=S_IFCHR|0600, st_rdev=makedev(0x88, 0x2), ...}, AT_EMPTY_PATH) = 0
```

Look at the `/usr/lib/ssl/openssl.cnf`.  I did not specify `-config my_config.cnf`.

Even when I put my own `-config`, it still reads and loads in all the settings from the `/usr/lib/ssl/openssl.cnf` file.

Found a `getenv()` to be using `OPENSSL_CONF` so I experimented with `/dev/null` as an assignment value.   Later, I can make it quicker by using an empty assignment (ie. `OPENSSL_CONF=`).

There are no command line option to prevent this pre-loading of the "default" settings from `/usr/lib/ssl/openssl.cnf` file.

Unfortunately, this environment variable is shell-specific.  So it would not work if you forked from a bash shell;  much less tried to do a command substitution or a process-substitution (both bash-specific methods).

For a real slick bash programming concept, use:

```bash
OPENSSL_BIN="env OPENSSL_CONF=  openssl"

execute() {
  if [[ "$VERBOSITY" -ge 1 || -n "$DRY_RUN" ]]; then
    echo "COMMAND: $@"
  fi
  if [ -z "$DRY_RUN" ]; then
    $@
    return $?
  fi
}


execute $OPENSSL_BIN verify ...
```

This makes it easier to add `--dry-run` and `--verbose` options, separately.
