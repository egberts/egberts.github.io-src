title: Hardened Text-Base Config Files
date: 2020-10-13 11:00
status: published
tags: hardened
category: research
summary: How to hardened the text-based config files in Linux OS.
slug: os-linux-hardened-configs.md
lang: en
private: False


# Sudo

```bash
# Set by `SU_LOGFILE` in `/etc/login.defs`
touch /var/log/sulogin
```

# Login Defaults

`/etc/login.defs` has the following new/updated settings:

```
# Clamp down on file permissions
UMASK 0027

# Maximum time it takes to perform a login
LOGIN_TIMEOUT 15

# Upgrade password encryption from DES to YESCRYPT
# corresponding change must be made to /etc/pam.d/common-password
ENCRYPT_METHOD  YESCRYPT

# Prevents an empty password from being accepted (or removed)
PREVENT_NO_AUTH no
```
