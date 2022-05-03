title: How to maintain small multiple configs for Linux kernels
date: 2022-04-27 04:10
status: published
tags: Linux, kernel
category: HOWTO
summary: Making minute changes of Linux kernel easier with various scripts
slug: linux-kernel-config-parts
lang: en
private: False

I find it much easier to maintain numerous but smaller `.config` files when
building a Linux kernel.  

The `.config` file is located at the apex of Linux source directory.

This `.config` is a text-based INI-format file
that many Windows and Linux sysadmin comes to 
love (no section needs apply there).

Its file format comprises of `#` for a commentline and a simple syntax of:
```bnf
variable_name=value
```

And there are shell scripts maintained by the Linux development 
team to deal with
their INI-formatted `.config` file that can be used as well for 
your own config files.

Go ahead and saunter over to your Linux source `./kernel/configs` directory;
and notice the few default settings for different (hardware and virtual) targets.

```console
# cd ./kernel/configs
# ls -lat
total 40
drwxrwxr-x  2 root root 4096 Apr 13 14:03 .
drwxrwxr-x 21 root root 4096 Apr 13 14:03 ..
-rw-rw-r--  1 root root 4134 Apr 13 14:03 android-base.config
-rw-rw-r--  1 root root 2857 Apr 13 14:03 android-recommended.config
-rw-rw-r--  1 root root  670 Apr 13 14:03 kvm_guest.config
-rw-rw-r--  1 root root  306 Apr 13 14:03 nopm.config
-rw-rw-r--  1 root root   18 Apr 13 14:03 tiny-base.config
-rw-rw-r--  1 root root  320 Apr 13 14:03 tiny.config
-rw-rw-r--  1 root root 1138 Apr 13 14:03 xen.config
```

Now, I need to do removal of `initramfs`, some hardening
efforts, and an inclusion of a
motherboard-specific hardware-wide settings.  This article only details the mechanism to using Linux kernel scripts.

One would take that config text file and fold them into a `.config` of the latest Linux kernel.

All in one-go.

The few basic approaches of config file handling for Linux kernels are:

* Single-option 
* Multiple config files

The available scripts found in nearly all Linux source tarballs.

# Linux kernel scripts

Linux kernel has includes several scripts (available since kernel v3.3) to deal with the `.config` files.

These scripts mostly help to support the various options of `make` evocations
(such as `make oldconfig` or `make newconfig`).

A true embedded-engineer (at least, I) would always start out with the bare minimum `.config` by doing:
```console
$ make tinyconfig
  HOSTCC  scripts/basic/fixdep
  HOSTCC  scripts/kconfig/conf.o
  HOSTCC  scripts/kconfig/confdata.o
  HOSTCC  scripts/kconfig/expr.o
  LEX     scripts/kconfig/lexer.lex.c
  YACC    scripts/kconfig/parser.tab.[ch]
  HOSTCC  scripts/kconfig/lexer.lex.o
  HOSTCC  scripts/kconfig/menu.o
  HOSTCC  scripts/kconfig/parser.tab.o
  HOSTCC  scripts/kconfig/preprocess.o
  HOSTCC  scripts/kconfig/symbol.o
  HOSTCC  scripts/kconfig/util.o
  HOSTLD  scripts/kconfig/conf
#
# configuration written to .config
#
Using .config as base
Merging ./kernel/configs/tiny.config
Value of CONFIG_CC_OPTIMIZE_FOR_PERFORMANCE is redefined by fragment ./kernel/configs/tiny.config:
Previous value: CONFIG_CC_OPTIMIZE_FOR_PERFORMANCE=y
New value: # CONFIG_CC_OPTIMIZE_FOR_PERFORMANCE is not set

<snippet boring stuff here>

#
# merged configuration written to .config (needs make)
#
#
# configuration written to .config
#
```

But you would not normally be using `make tinyconfig` unless you like building
Linux kernel from ground-zero or from scratch (like from during the good ol' days of Linux From Scratch distro).

Most serious hardened-kernel users would just execute:
```console
$ make oldconfig
```
and whittle down the unneeded config parts until it stops working.

Most embedded Linux guys would still use the `tinyconfig` and start from there.

# Single Option approach

There is a way to do this setting-tweaks to the Linux kernel, 
one option at time, which would be especially useful for 
non-interactive (batch) mode such as shell-scripting.

To do a series of simple flipping of a single config setting 
while updating any and all config dependencies, let's start 
with the very basic script, `config`; located in `./scripts`
subdirectory.  

`scripts/config` has been around since [2.6.29
days](https://github.com/torvalds/linux/commit/2302e8730e5caa774e7c6702fc878404d71f13f9), so it is not
exactly a state secret amongst eminent kernel builders and embedded engineers.

```bash
./scripts/config --set-val CONFIG_OPTION y
./scripts/config --enable CONFIG_BRIDGE
./scripts/config --enable CONFIG_MODULES
./scripts/config --disable CONFIG_X25
./scripts/config --module CONFIG_NFT

# Remove any unneeded configs and re-add any required configs
make oldconfig
```
The above `make oldconfig` will update any new dependencies not found in the current `.config`; it may prompt the developer with new dependencies, but the old dependency will silently goes away.  

One thing to note about `make oldconfig` is that it will always put a required option back into the `.config`.  When this happens, one often has to scan for all the `Kconfig` files throughout the entire Linux source directories for matching config option, then re-examine the requirement conditional logics to figure out how to make that option truly stay the way you want it to be (that is, disabled or enabled).

While this single option approach is useful, doing this for many options may
prove to be tangle-some and unwieldly.

It is common to group those option settings together into a small `config` file
and file-name it to something like `config-ethernet-vendors-gone` or
`config-proc-dir-offlimit`.

## Weird Debian case of initramd/initramfs

I had a weird case of trying to completely disable modules in Debian 11.

There were intractable clawbacks of other options that will pull modules back into the kernel, despite setting `CONFIG_MODULES=n`.  If you do not clear those other options, then re-activated modules (`CONFIG_MODULES=y`) will appear after the next `make oldconfig` command.

In advanced, I've identified those "pesky things" interfering with our goal as a
module-less Linux kernel as:

```ini
SYSTEM_TRUSTED_KEYRING=n
MODULE_SIG_KEY=n
SYSTEM_DATA_VERIFICATION=n
KEXEC_BZIMAGE_VERIFY_SIG=n
KEXEC_VERIFY_SIG=n
SIGNED_PE_FILE_VERIFICATION=n
REQUIRED_SIGNED_REGDB=n
```

For Debian-only, with the above settings, there may be a 
side-effect of knocking out the signed-certified country 
authorized RF bands database for one particular
WiFi drivers (but that is easily replaced with a different WiFi driver). 
Just an opinion, Debian isn't friendly toward high-reliability servers, 
and you should not be using Debian for all your production servers 
unless you like job-security and system-downtimes.

# Multiple-File Merge approach

Once you start to have multiple tiny `config-*` files lying all round you, 
there will come a
time when you want to whip out a new `kernelbuild` subdirectory and work on a
new Linux kernel.  

It is then (after you do `make menuconfig/xconfig/gconfig/nconfig`) 
that you will be pummeled with the daunting task of 
answering yes, 'n'o, 'n'o, 'y'es, 'y'es, enter, 'm'odule, 'n'o ... 
for about 1,000 times (or papercuts).

Instead of a single-prompt/multiple-times approach, we can have a 
text file containing just those names of selected Kconfig variables 
and merge them into the master `.config` file.

The merge tool of `Kconfig` settings is `merge_config.sh`.  This
`merge_config.sh` has been around since 
[kernel v3.33](https://github.com/torvalds/linux/blob/master/scripts/kconfig/merge_config.sh)

Usage syntax of `merge_config.sh` is pretty simple:

```bnf
merge_config.sh  output-config-file  [ input-config-file1 [ ... ]]
```

If you have several small snippets of `.config-*` files that you want to selectively merge into the main `.config` file, execute:

```bash
# Merge IP fragment CONFIG_ settings into the main .config file
./scripts/kconfig/merge_config.sh .config config-initramfs-initramd-disable

# Merge  Notebook HW-specific CONFIG_ settings into main .config file
./scripts/kconfig/merge_config.sh .config .config-notebook-toshiba

# Auto-add/auto-remove/restore any CONFIG_ dependencies
make oldconfig
```

Hopefully, you will then have a clean `make -j4` and a kernel closer to your
liken.

# References

* [https://www.kernel.org/doc/html/latest/kbuild/kconfig.html#nconfig-mode](https://www.kernel.org/doc/html/latest/kbuild/kconfig.html#nconfig-mode)
* [https://stackoverflow.com/questions/27090431/linux-kconfig-command-line-interface/70728869#70728869](https://stackoverflow.com/a/70728869/4379130)
