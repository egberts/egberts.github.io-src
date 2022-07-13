title: Many Ways to Pass a Password to OpenSSL
date: 2022-03-19 07:32
status: published
tags: OpenSSL, environment variables
category: HOWTO
summary: See here the many ways to pass a password to the openssl command line.
slug: openssl-password
lang: en
private: False


There are two directions and two methods that a password can go with the `openssl` command:

By directions:

* Reading a password or password file in [req] and [ca] sections, only in openssl `req`, `x509`, `pkey`, `s_client`, or `s_server` commands.
* Writing to a password file, only in openssl `req` or `genpkey` commands.

and by methods:

* directly into the command line (`pass:`)
* by a file using a filename as a reference (`file:`)
* by an environment variable name (`env:`)
* by a UNIX file descriptor (`fd:`)

Also password file can be:

* unsecured
* secured by your choice of a digest algorithm

Pass A Password by Command Line
-------------------------------

pass the password directly on the command line to `openssl` 
```bash
openssl req ... -passin 'pass:mysecretpassword' ...
```

Of course, be mindful that your shell history will be recording this unless your shell setting has something like `HISTSIZE=0` to disable history recording.  Also, do not forget the memory of your terminal emulator (eg. scrollback line count, memory buffer, copy buffer).  

Just might be easier to avoid this method, so read on.


Pass A Password by File
-----------------------

To create a UNSECURED password file
```bash
echo "mysecretpassword" > password.txt
chmod 0600 password.txt
```

Then pass the filename of the password to the command line of `openssl`:

```bash
openssl req ... -passin 'file:password.txt' ...
```

The specification is simple:
```bash
openssl req ... -passin 'file:<filespec>' ...
```
where `<filespec>` is the filename, relative filename, or absolute file specification.


Password by Environment Variable
--------------------------------

To create an secured password file by environment variable:
```bash
export MY_PASSWORD="mysecretpassword"
```

Then pass the environment variable of the password to the command line of `openssl`:

```bash
openssl req ... -passin 'env:MY_PASSWORD' ...
```

Password by UNIX Pipe
---------------------

To pass a password file by UNIX pipe (file descriptor):

```bash
echo "mysecretpassword" | openssl req ... -passin 'fd:1' ...
```

Also there is a `stdin` option (which is equivalent to `fd:1`).

```bash
echo "mysecretpassword" | openssl req ... -passin stdin ...
```

Securing A Password File
========================

The password file also can be secured using any one of the digest command options available.

To find the available digests, the `openssl req -help` command will output many options related to the `[req]` section and creation of CSR certificate;, please noticed the `-*` option (at the beginning of the output).  That `-*` is the help notation for many-digest options.

To list the available digest command options, execute:
```console
$ openssl dgst -list
Supported digests:
-blake2b512                -blake2s256                -md4                      
-md5                       -md5-sha1                  -ripemd                   
-ripemd160                 -rmd160                    -sha1                     
-sha224                    -sha256                    -sha3-224                 
-sha3-256                  -sha3-384                  -sha3-512                 
-sha384                    -sha512                    -sha512-224               
-sha512-256                -shake128                  -shake256                 
-sm3                       -ssl3-md5                  -ssl3-sha1                
-whirlpool  
```


`-sha512` is preferred over `-sha3-512`, `-sha3-384`, `-sha3-256`, `-sha512-256` or `-sha512-224` for those two-numbered SHAs are actually the lowest number supported but stored in 512-bit data space.  Stick with `-sha512`.   

You could also experiment with `-blake2b512` safely than the rest of the unmentioned ones.


Safely Storing Password File
============================

If you are storing many different passwords for creating a large CA PKI tree for research or white lab uses, it may make sense to hardcode the same password for all certificates.

If many people are submitting different passwords to the creator of certificates(CA administrator), then the password MUST BE salted  and then to to pass the salted password into the `openssl` PKI system.

`openssl` has a `passwd`-like command.  `openssl passwd` takes one raw password (from many input methods listed above) and creates a salted password (much like UNIX `passwd` would do) for safer storage in a filesystem.  Unfortunately, this feature has a default salt and iteration settings baked-in, which isn't so bad but definitely better than stored in raw form.

It is better to use a different front-end password utility, like `mcrypt` or `ccrypt`.  Different passowrd utility most likely would provide more refined salt, iteration, and random seeding control for such a safer password storage system.

Of course, you would roll your own front-end password utility that would choose a fixed salt value and maybe leave the iteration setting to the end-user.  One salt value per group of end-users, if possible to manage.

An example workflow of handling password securely might be like this:

```console
$ openssl passwd -6 > password.txt
Password: <type something>
Verifying - Password: <type the same thing>
$
$ cat password.txt
$6$771Qtv7Rxww2Xa9h$s8n72W6Hud84tldggJAwgMCwP4D1LGJpSRtgHUrTr9Ay0WoVgJvfwOWc/TyM/ucZTlAp1Ouae8eMdQo9NFf8C.
```

Once this is done, there is little worry for a trusted CA administrator to be knowing what their end-users password are: the password got salted.

With a salted password, CA admin can now perform their usual mass production of certificates for such a large but closed PKI ecosystems.

