title: CA Certificates rebuild on Debian
date: 2021-11-20 11:00
status: published
tags: OpenSSL, PKI, certificate authority, Debian
category: research
lang: en
private: False

This article details how the rebuilding of Trusted Root CA occurs on a Debian
Linux using the `update-ca-certificates` tool as part of `ca-certificates`
Debian package.

Also it details what my current thoughts are regarding the auditable aspect of
Root CA, its intermediate CA, trusted CA and blacklisting CAs.

For the first round of audit, by executing the `update-ca-certificates --fresh` using `strace -f`, the output has compile a list of files read and written by `update-ca-certificates`.

```bash
strace -f update-ca-certificates -f | grep openat
```

The list of files that are opened and read-only are in the following order:

1. `/etc/ca-certificates.conf` file
2. `/usr/share/ca-certificates/*` directory
3. `/usr/share/ca-certificates/mozilla/*` directory
4. `/usr/share/ca-certificates/*/*` directory
5. `/usr/local/share/ca-certificates/*` directory
6. `/usr/local/share/ca-certificates/*/*` directory
7. `/etc/ssl/certs` directory
8. `$CWD/<all-certs-read-before>` files
9. `/usr/lib/ssl/openssl.cnf` file
10. `/etc/ca-certificates/update.d` directory
11. `/etc/ca-certificates/update.d/jks-keystore` directory
12. `/etc/default/cacerts` directory
13. `/etc/java-11-openjdk/security/nss.cfg` file
14. `/usr/share/ca-certificates-java` directory
15. `/usr/lib/jvm/java-11-openjdk-amd64/lib/jvm.cfg` file
16. `/usr/share/ca-certificates-java/ca-certificates-java.jar` file
17. `/etc/ca-certificates/update.d/mono-keystore` directory
18. `/etc/mono/4.5/machine.config` file
19. `/etc/mono/assemblies/cert-sync/cert-sync.config` file
20. `/etc/mono/assemblies/Mono.Security/Mono.Security.config` file
21. `/etc/mono/assemblies/mscorlib/mscorlib.config` file
22. `/etc/mono/assemblies/System/System.config` file
23. `/etc/mono/config` file
24. `/etc/ssl/certs/ca-certificates.crt` file
25. `$HOME/.mono/config` file
26. `/usr/lib/mono/4.5/cert-sync.exe.config` file
27. `/usr/lib/mono/4.5/cert-sync.exe.config` file
28. `/usr/lib/mono/4.5/mscorlib.dll.config` file
29. `/usr/lib/mono/gac/Mono.Security/4.0.0.0_0738eb9f132ed765/Mono.Security.dll.config` file
30. `/usr/lib/mono/gac/System/4.0.0.0__b77a5c561934e089/System.dll.config` file
31.  `/usr/share/.mono/certs/Trust/ski-*.cer` file
32.  `/usr/share/.mono/certs/new-certs/XXXXXXXX.0` file
33.  `$CWD/openssl` EXECUTABLE!!! (why look in $CWD?)
34.  `/usr/bin/openssl`
35.  `/usr/local/bin/openssl`
36.  `/usr/local/sbin/openssl`
37.  `/usr/sbin/openssl`  (VERY STRANGE ordering of /usr/[local/][s]bin/


and writes to the following text files:

1. `$CWD/ca-certificates.txt`
2. `/etc/ssl/certs/java/cacerts`


AUDITABLE OBSERVATION
=====================

OpenSSL binary, misordered lookup sequence of
---------------------------------------------

In observing the "finding" of the OpenSSL binary by `update-ca-certificates`,
I noticed a very strange lookup ordering of looking for this `openssl` binary.

Probably should have been something in the (re)order of:

1. $CWD/openssl  (probably should NOT have this entry)
2. /usr/local/bin/openssl
3. /usr/local/sbin/openssl
4. /usr/bin/openssl
5. /usr/sbin/openssl

From an auditor's perspective, one could argue that the `sbin`-variant always have precedence over `bin`-variant.

Arguably, I would like to see this ordering, instead:

1. /usr/local/sbin/openssl
2. /usr/local/bin/openssl
3. /usr/sbin/openssl
4. /usr/bin/openssl

Auditable Impact Toward CA Certificates
---------------------------------------
Then there are three groups of certificates.

Now, I would normally raise an eye-brow about the inclusion of the two groups
outside of OpenSSL.

However this is the open-source community (and not the enterprise-based
ones), and different inclusion mechanism are in play; it resulted in
the addition of two additional groups (MONO and OpenJDK).

When auditing, the output of `update-ca-certificates` probably 
should show various 'modules' being referred to during the rebuilding
of CA certificates pool:

1.  MONO
2.  OpenJDK Java 11
3.  Mozilla

then

4.  OS System

Auditable Output of CA Certificates
-----------------------------------
Also for writing the output file, it should probably show various 
CREATION of files (or PKI Subject, or both) that are found in:


1. `$CWD/ca-certificates.txt`
2. `/etc/ssl/certs/java/cacerts`

This would enable auditors to do tracibility matrix against this.  

A singular JSON output file would be a plus.


Better Summarization
--------------------

Also `update-ca-certificates` should probably indicate those 
summarization by group AT THE END of its output, broken
down by CA-CERTIFICATE MODULES.  Into something like this:

```
      OS System:
        Added:   0
        Deleted: 0
        Used:    0
      Mozilla package:
        Added:   0
        Deleted: 0
        Used:  129
      OpenJDK package:
        Added:   0
        Deleted: 0
        Used:   86
      MONO package:
        Added:   0
        Deleted: 0
        Used:   44
      Total Merge:   129

  Master File:  /usr/share/ca-certificates  (depends on distro)
  Master File:  /etc/ca-certificates
  Master File:  /etc/ssl/certs
  Master File:  /etc/pki/tls/certs
```

Will try and find appropriate package maintainer and/or author to let them know
of these findings.


