title: Removing `initramfs` from Linux kernel bootup
date: 2022-08-01 10:15
modified: 2025-07-13 02:02
status: published
tags: Linux, initramfs, initramd, libmusl
category: HOWTO
summary: How to bootup Linux OS without using initramfs.
slug: linux-kernel-booting-without-initramfs
lang: en
private: False


This article details how to do a straight bootup of Linux OS without the
use of a separate (and often compressed) RAM-based filesystem used by 
its kernel for loading various kernel modules.

Preparation
====

The latest source to the Linux kernel should be downloaded and saved
within its own subdirectory name under the `/usr/src` directory:

```bash
$ cd /usr/src
$ wget -O - <url-to-kernel-source.tarball>
$ tar xvfz <downloaded-kernel-source.tarball>
$ mv <new_directory_name>  <your_preferred_dirname>
```

We will assume `linux-5.15.52` in this article.


Kernel Re-Configuration
----

```bash
cd /usr/src/linux-5.15.52
make oldconfig
make menuconfig
```


Building
====

```bash
cd /usr/src/linux-5.15.52
make && make modules install
```

Boot Update
====


Verifying
----

```
cd /usr/src/linux
make listnewconfig   # a safe passive (non-changing) status command
```
The output of `listnewconfig` should be empty (no new config undefined).





Rebuild Modules & Libraries
----

```
emerge @module-rebuild     # rebuild modules
emerge @preserved-rebuild  # rebuild system libraries
```


System Install
====


Install Bootloader using GRUB2
----

```bash
grub-install /dev/sda
```


Configuring GRUB2
----

Because the root (`/`) partition got mounted in read-only, we must force this to be mounted as "read-write":

```console
vi /etc/default/grub
```
and append to the `GRUB_CMDLINE_LINUX` environment setting by inserting an `rw` at the end of the boot command line:
```ini
GRUB_CMDLINE_LINUX=`root=/dev/vda3 nomodule rw`
```

Then update the Grub2 menu:
```bash
   # reads from /etc/default/grub
   # reads from /etc/grub.d/*

   grub-mkconfig -o /boot/grub/grub.cfg
```

Rebooting
====

Exit and then reboot

```console
(chroot) / # exit
/root # reboot
```


Enjoy
