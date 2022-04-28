title: What CUPS LP/LPR consult for Configuration File(s)
date: 2020-10-13 11:00
status: published
tags: CUPS, lpr
category: HOWTO
summary: What CUPS LP/LPR consult for Configuration File(s)
lang: en
private: False

Executing:
```bash
strace -f lp /etc/hosts
```
gives us this gem on what the CUPS printer tool is looking for in user-defined
and system-defined configuration settings:

```
access("printers.conf", R_OK)           = 0
openat(AT_FDCWD, "/root/.cups/lpoptions", O_RDONLY) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/cups/lpoptions", O_RDONLY) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/cups/client.conf", O_RDONLY) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/root/.cups/client.conf", O_RDONLY) = -1 ENOENT (No such file or directory)
access("/run/cups/cups.sock", R_OK)     = 0
```

