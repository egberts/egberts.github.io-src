title: Configuring automatic file creation/deletion during systemd bootup
date: 2020-08-16 10:07
status: published
tags: systemd, bootup, cleanup
category: HOWTO
summary: How to configure systemd to perform automatic creation and deletion of files during bootup.

Configuring Automatic File Creation and Deletion
================================================

There are several services that create or delete files or directories:

* `systemd-tmpfiles-clean.service`
* `systemd-tmpfiles-setup-dev.service`
* `systemd-tmpfiles-setup.service`

The system location for the configuration files is `/usr/lib/tmpfiles.d/*.conf`. 
The local configuration files are in `/etc/tmpfiles.d`. 
Files in `/etc/tmpfiles.d` override files with the same name in `/usr/lib/tmpfiles.d`. 
See tmpfiles.d(5) manual page for file format details.

Note that the syntax for the `/usr/lib/tmpfiles.d/*.conf` files can be 
confusing. 
For example, the default deletion of files in the `/tmp` directory is 
located in `/usr/lib/tmpfiles.d/tmp.conf` with the line:

`cron
q /tmp 1777 root root 10d
`

The type field, `q`, discusses creating a subvolume with quotas which is 
really only applicable to BTRFS filesystems. 
It references type `v` which in turn references type `d` (directory). 
This then creates the specified directory if is is not present and adjusts 
the permissions and ownership as specified. 
Contents of the directory will be subject to time based cleanup if 
the age argument is specified.

If the default parameters are not desired, then the file should be 
copied to `/etc/tmpfiles.d` and edited as desired. For example:

```bash
mkdir -p /etc/tmpfiles.d
cp /usr/lib/tmpfiles.d/tmp.conf /etc/tmpfiles.d
```
