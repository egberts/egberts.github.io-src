title: Gentoo OS for a Dell Optiplex 790
date: 2022-07-22 01:38
modified: 2022-09-21 09:32
status: published
tags: Gentoo, gateway, Dell, Optiplex 790, Linux
category: HOWTO
summary: How to setup Linux OS for use on Dell Optiplex 790
slug: gentoo-os-setup-dell-optiplex-790
lang: en
private: False


How to setup the Gentoo 2022 OS from scratch ... on a Dell Optiplex 790

Dell Optiplex 790 is a cheap low-power (<100W) PC that has a crappy UEFI Class 1 making UEFI unusable from Linux point-of-view; this one remains firmly as a legacy master-boot record (MBR) boot sequence.

Optiplex 790 BIOS does not support ACPI 2.0 nor UEFI 2.3.1; save yourself further headache, use only the MBR approach.

This would be extremely useful for a home gateway (whose requirement is
not entailing MySQL database nor JavaScript-based web browsing or easily hijacked using a `LD_PRELOAD` environment variable.)

# Hardware Gotcha

There are a couple of hardware gotcha that has made installation of Linux OS into a struggle with the Dell Optiplex 790:

1. USB mouse gets randomly jumpy during BIOS setup; use a PS/2 mouse or try the USB mouse on each and every USB port until it this stops.  I used the upper right corner USB port on front-panel before mouse got steady enough to be usable.

2. Any extra PCI-based video adapter will turns off the Intel HD VGA components on its motherboard.  This may result in tiny (and hard-to-read) fonts during bootup sequence.

3. UEFI is not supported by Linux here.  Dell 790 BIOS do not support UEFI 2.3.1 (they are stuck on UEFI Class 1 mode).  Do not bother.  Stick with the good old legacy master boot record (MBR) approach here.




## Download ISO

Visit [Gentoo](https://www.gentoo.org) and click on "Get Gentoo" button at top-row navigation panel.

Under `amd64`, 'stage archives', select the desired ISO image.  

Of the several variants of Stage 3, I chose "OpenRC" because `systemd` PID 1 has too much network access privilege which IMHO is ripe for a file-less backdoor malware.  OpenRC PID 1 has no such network privilege (same as original ATT SysV `initrc`/`init.d`), which sets my security mind at ease.


## Identify the hard drive 

Within the newly booted minimal Gentoo, identify the hard drive used to hold our filesystems.  

Note: It should be `/dev/sda` (as opposed to `/dev/sda`).


```
lsblk -a | grep -v ^loop | grep -v ^ram | grep disk
NAME   MAJOR:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda      253:0    0    80G  0 disk
```

The hard drive provided by QEMU virtualization is `/dev/sda`.


# Drive Format

Optiplex 790 still mandates the use of legacy MBR.  No need to touch UEFI here (not supported, despite BIOS settings).

The above partition scheme encompasses:

* four(4) physical partitions
* two(2) LVM volume groups (`vg_os` and `vg_log`)
* seven(7) LVM volume partitions 


## Purging any physical partitions

Use `fdisk` to continue to stay with the 'dos' (MS-DOS/MBR) disktype.

```bash
fdisk /dev/sda
```

Delete all partitions.  Write and exit `fdisk`.  

WARNING: If any error message appears saying that OS is still using it, then reboot the machine and go back into `fdisk` command again before continuing here.

Do not use GNU `parted`; GPT is not supported in 790 BIOS.


## Create physical partitions

*  Partition 1 - 250MB - /boot  (should be 1G if doing some heavy kernel tweaking)
*  Partition 2 - 2GB - swap  (should be twice your total 'physical' memory)
*  Partition 3 - 50GB of hard media - ROOT label - / directory
*  Partition 4 - remainder of hard media - LVM partition (MBR type 0x8E)


## Changing physical partition type

Change partitions to:

* Partition 1 - Type 0x83  Linux
* Partition 2 - Type 0x82  Linux swap
* Partition 3 - Type 0x83  Linux
* Partition 4 - Type 0x8E  LVM partition

Write out the entire partition table and quit.

## Make /boot bootable

Do not forget to toggle the partition 1 as "bootable".  In the fstab, enter in option `a` and select partition 1.



## Creating LVM partitions

Create the logical partitions by doiong `pvcreate`, `vgcreate`, and `lvcreate` commands:


```bash
#!/bin/bash

PHYSICAL_PARTITION_LOG="/dev/sda5"
PHYSICAL_PARTITION_OS="/dev/sda6"
VG_NAME_OS="vg_os"
VG_NAME_LOG="vg_log"
LV_NAME_USR="lv_usr"
LV_NAME_TMP="lv_tmp"
LV_NAME_VAR="lv_var"
LV_NAME_HOME="lv_home"
LV_NAME_VAR_TMP="lv_var_tmp"
LV_NAME_VAR_LOG="lv_var_log"
LV_NAME_VAR_LOG_AUDIT="lv_var_log_audit"

pvcreate ${PHYSICAL_PARTITION_LOG}
pvcreate ${PHYSICAL_PARTITION_OS}

vgcreate ${VG_NAME_OS}  ${PHYSICAL_PARTITION_OS}
vgcreate ${VG_NAME_LOPG} ${PHYSICAL_PARTITION_LOG}

lvcreate -L24G -n${LV_NAME_TMP} ${VG_NAME_OS}
lvcreate -L80G -n${LV_NAME_VAR} ${VG_NAME_OS}
lvcreate -L256G -n${LV_NAME_USR} ${VG_NAME_OS}
lvcreate -L50G -n${LV_NAME_VAR_TMP} ${VG_NAME_OS}
vgdisplay  # note remaining "Free PE" space and plug into next command
lvcreate -n${LV_NAME_HOME} ${VG_NAME_OS}

lvcreate -L10G -n${LV_NAME_VAR_LOG_AUDIT} ${VG_NAME_LOG}
lvcreate       -n${LV_NAME_VAR_LOG} ${VG_NAME_LOG}
```

If `lv_home` failed due to insufficient space, execute:
```bash
lvremove lv_home vg_os
# follow series of prompts and delete 'lv_home' partition
```
then repeat `lvcreate -L<your-next-largest-size> -nlv_home vg_os` command until success.


## Format physical partitions

Format the physical partitions:

```bash
#!/bin/bash

FS_TYPE_BOOT="ext4"
FS_TYPE_ALL="ext4"
echo "Formatting all partitions ..."
echo "Press ENTER to continue (or Ctrl-C to quit)"
read JUNK

mkfs -t ${FS_TYPE_BOOT} -LBOOT /dev/sda1
mkswap /dev/sda2
mkfs -t ${FS_TYPE_ALL} -LROOT /dev/sda3
mkfs -t ${FS_TYPE_ALL} /dev/mapper/vg_os-lv_usr
mkfs -t ${FS_TYPE_ALL} /dev/mapper/vg_os-lv_tmp
mkfs -t ${FS_TYPE_ALL} /dev/mapper/vg_os-lv_var
mkfs -t ${FS_TYPE_ALL} /dev/mapper/vg_os-lv_home
mkfs -t ${FS_TYPE_ALL} /dev/mapper/vg_os-lv_var_tmp
mkfs -t ${FS_TYPE_ALL} /dev/mapper/vg_os-lv_var_log
mkfs -t ${FS_TYPE_ALL} /dev/mapper/vg_os-lv_var_log_audit

echo "Done."
```
Now onward to set up the root filesystem to hold our initial Gentoo CD installation.


## Create mountpoint directories then mountings

Create the parent root file path for our new Gentoo OS:

```
mkdir --parents /mnt/gentoo
```

# Rescue Reboot (Resumption Point)

NOTE: If your kernel boot up fails (after finishing all this page), this is your starting point
to resume setup.

## Enable Swapper

```
swapon /dev/sda2
```

# Partition mountings

I typically create a bash script to store in `/mnt/gentoo` so that it would
cut down on my typing time during my kernel config tweaking/reduction effort.

Store following bash script as `/mnt/gentoo/myinstall0.sh`, set its file permission to 0750.
```bash
mount /dev/sda3 /mnt/gentoo
mkdir -p /mnt/gentoo/boot
mkdir -p /mnt/gentoo/home
mkdir -p /mnt/gentoo/usr
mkdir -p /mnt/gentoo/tmp
mkdir -p /mnt/gentoo/var
mount /dev/sda1 /mnt/gentoo/boot
mount /dev/mapper/vg_os-lv_usr /mnt/gentoo/usr
mount /dev/mapper/vg_os-lv_tmp /mnt/gentoo/tmp
mount /dev/mapper/vg_os-lv_home /mnt/gentoo/home
mount /dev/mapper/vg_os-lv_var /mnt/gentoo/var
mkdir -p /mnt/gentoo/var/tmp
mkdir -p /mnt/gentoo/var/log
mount /dev/mapper/vg_log-lv_var_log /mnt/gentoo/var/log
mkdir -p /mnt/gentoo/var/log/audit
mount /dev/mapper/vg_log-lv_var_log_audit /mnt/gentoo/var/log/audit
```


## Mount the root (/) partition

```
mount /dev/sda3 /mnt/gentoo
```

This above command is the only thing you need to memorize when coming back here after a failed kernel boot.  This is assuming that you have made the `myinstall0.sh` scripts to do recreate the following steps.


## Mount /usr (and additional) partitions (optional)

I often break out `/usr` into a separate partition as I do the recommended CISecurity partitioning scheme:


# Filesystems

The goal is to have the following filesystem partitions:

[jtable]
device, path
`/dev/sda3`, `/`
`/dev/sda1`, `/boot`
`/dev/mapper/vg_os-lv_usr`, `/usr`
`/dev/mapper/vg_os-lv_tmp`, `/tmp`
`/dev/mapper/vg_os-lv_var`, `/var`
`/dev/mapper/vg_os-lv_home`, `/home`
`/dev/mapper/vg_os-lv_var_tmp`, `/var/tmp`
`/dev/mapper/vg_log-lv_var_log`, `/var/log`
`/dev/mapper/vg_log-lv_var_log_audit`, `/var/log/audit`
[/jtable]

Go mount them all using above script or use snippet of following:
```bash
mkdir -p /mnt/gentoo/boot
mkdir -p /mnt/gentoo/home
mkdir -p /mnt/gentoo/usr
mkdir -p /mnt/gentoo/tmp
mkdir -p /mnt/gentoo/var
mount /dev/sda1 /mnt/gentoo/boot
mount /dev/mapper/vg_os-lv_usr /mnt/gentoo/usr
mount /dev/mapper/vg_os-lv_tmp /mnt/gentoo/tmp
mount /dev/mapper/vg_os-lv_home /mnt/gentoo/home
mount /dev/mapper/vg_os-lv_var /mnt/gentoo/var
mkdir -p /mnt/gentoo/var/tmp
mkdir -p /mnt/gentoo/var/log
mount /dev/mapper/vg_log-lv_var_log /mnt/gentoo/var/log
mkdir -p /mnt/gentoo/var/log/audit
mount /dev/mapper/vg_log-lv_var_log_audit /mnt/gentoo/var/log/audit
```


# Creating `/etc/fstab`
Edit the  `/mnt/gentoo/etc/fstab` to contain:

[jtable]
device, path, options, boot sequence
`/dev/sda1`, `/boot`, `vfat`, `noauto,rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=iso8859-1,shortname=mixed,errors=remounte-ro`, `1`, `1`
`/dev/sda2`, `swap`, `swap`, `defaults,sw`, `0`, `0`
`/dev/sda3`, `/root`, `ext4`, `defaults,noatime,errors=remount-ro,rw`, `0`, `1`
`/dev/sda4`, `(LVM volume group)`

`/dev/mapper/vg_os-lv_tmp`, `/tmp`, `ext4`, `defaults,nosuid,nodev,rw,relatime`, `0`, `2`
`/dev/mapper/vg_os-lv_usr`, `/usr`, `ext4`, `defaults,nodev,rw,relatime`, `0`, `2`
`/dev/mapper/vg_os-lv_var`, `/var`, `ext4`, `defaults,nosuid,nodev,rw,relatime`, `0`, `2`
`/dev/mapper/vg_os-lv_var_tmp`, `/var/tmp`, `ext4`, `defaults,noexec,nosuid,nodev,rw,relatime`, `0`, `2`
`/dev/mapper/vg_os-lv_var_log`, `/var/log`, `ext4`, `defaults,noexec,nosuid,nodev,rw,relatime`, `0`, `3`
`/dev/mapper/vg_os-lv_var_log_audit`, `/var/log/audit`, `ext4`, `defaults,noexec,nosuid,nodev,fmask=0022,dmask=0022,rw,relatime`, `0`, `4`
`/dev/mapper/vg_os-lv_home`, `/home`, `ext4`, `defaults,rw,relatime`, `0`, `2`
[/jtable]

NOTE: Since we use `initramfs` here, must add a `noauto` mount option
for any non-root (`/`) partitions, such as `/usr`.

In our case here, we have 8 non-root partitions (1 physical and 7 logicals).

If we had only the `/` partition and nothing else, then no `noauto` mount
option is needed for the lone `/` partition.  

NOTE: Do not forget to remove any non-root partitions from `/etc/initramfs.mounts` in this lone-root partition scenario.

In multi-partition, all partitions must have `noauto` mount options 
and its corresponding directory path is each inserted/appended to
the `/etc/initramfs.mounts` file.  Failure to have `noauto` will
result in a harmless but extraneous `e2fsck` execution for each
non-root partition(s).




# Check the DateTimestamp

To ensure accurate recording of files being created on, check the date:

```bash
date                # to view the date
date 202207211500   # to change to July 21, 2022, 1500UTC
```


# Network connectivity

I use the Gentoo `net-setup` to get the Internet up and running ... fast.

Use the 'manual configuration' option in `net-setup`, if you got some esoteric but exotic network setup.


# Selection of Gentoo Installers

Since we are booting within a QEMU environment, we only need the following
installer features:

* OpenRC (no systemd due to uncontrolable network-access within PID 1)
* libmusl (no glibc, no `LD_PRELOAD` support; [comparison chart](http://www.etalabs.net/compare_libcs.html))
* no-multilib (x86-64 only, no x86-32 support)
* no-desktop
* hardened (oops, make that no-hardened; [announcement](https://www.gentoo.org/support/news-items/2017-08-19-hardened-sources-removal.html), [discontinued](https://www.gentoo.org/news/2017/08/19/hardened-sources-removal.html)

From the terminal prompt, enter in:

```
cd /mnt/gentoo  # that is /dev/sda3 partition
links https://www.gentoo.org/downloads/mirrors
```

Go down to 'Downloads' link and hit enter.

Go down to 'Advance choices and other architectures' section (past the 'amd64 aka x86-64, x64, Intel 64' section).

Select `amd64` link.

Go slightly past just the 'Musl stage archives' section.

Select and download `Stage 3 musl | openrc 2022-XX-XX XXXMB`.

Make a note of the filename that you just saved.  My resultant filename is 'stage3-amd64-musl-20220720T2237212.tar.xz'.

A tiny bit further down the screen to just before the BIG 'amd64' section, move to on the 'All stages' link and press enter.

Select the 20220720T2237212Z subdirectory.

Go down to that filename you just saved.

Go down two more lines to the stage3-amd64-musl-20220720T2237212.tar.DIGESTS.gz file.  Download and save that file.

## Integrity of Download
### Obtain PGP Keys of Gentoo Organization

If not done already, save the PGP keys of the entire Gentoo organization:

```bash
wget -O - https://qa-reports.gentoo.org/output/service-keys.gpg | gpg --import
```


### Verify Gentoo Organization PGP keys

```bash
gpg --verify stage3-amd64-musl-20220720T2237212.tar.xz.DIGESTS.xz
```


### Validate Stage3 File

```console
# sha512sum -c --ignore-missing \
    stage3-amd64-musl-20220720T2237212.tar.xz.DIGESTS.xz
stage3-amd64-musl-20220720T2237212.tar.xz: OK
WARNING: 14 lines are improperly formatted
```

NOTE: WARNING is because I've opted to read a DIGEST file that has GnuPG headers and footers wrapped around the checksum values; we are only interested in the `OK` part of the `sha512sum` output.


# Content of root filesystem

Unpack the stage 3 tarball file that contains the initial root filesystem:

```
tar xpvf stage3-*.tar.xz --xattrs-include='*.*' --numeric-owner
```

## Clone network setup

Save the resolver into the future 
```bash
cp --dereference /etc/resolv.conf /mnt/gentoo/etc/
```

## Clone system filesystems

```bash
mount --types proc /proc /mnt/gentoo/proc
mount --rbind /sys /mnt/gentoo/sys
mount --make-rslave /mnt/gentoo/sys
mount --rbind /dev /mnt/gentoo/dev
mount --make-rslave /mnt/gentoo/dev
mount --bind /run /mnt/gentoo/run
mount --make-slave /mnt/gentoo/run 
chroot /mnt/gentoo /bin/bash
source /etc/profile
export PS1="(chroot) ${PS1}"
```



# Build setup

If you know how many CPU processors you have, then you can increase
the make build tool with all those processors by leveraging `--job=` options of the make utility.  For two CPUs, execute:

```
echo 'MAKEOPTS="-j2"' >> /mnt/gentoo/etc/portage/make.conf
```


## Selecting Remote Sources

```bash
mirrorselect -i -o >> /mnt/gentoo/etc/portage/make.conf
```


## Required packages

Create a local repository for Gentoo portage packages:
```
mkdir --parents /mnt/gentoo/etc/portage/repos.conf
cp /mnt/gentoo/usr/share/portage/config/repos.conf /mnt/gentoo/etc/portage/repos.conf/gentoo.conf
```

# CHROOT

```bash
chroot /mnt/gentoo /bin/bash
```


# Network Interfaces

Identify available network interface to use:

```bash
ip -o link | awk '{ print $2 }' | grep -v ^lo
```

In our case, we have `enp1s0` for the name of our network interface.

Now we create a startup script for `enp1s0` called `net.enp1s0`:

```bash
cd /etc/init.d
ln -s net.lo net.enp1s0
```

Edit `/etc/conf.d/net` :
```
# Rely on host's VM manager to provide us IP address via DHCP.
config_enp1s0="dhcp"
```


# Portage


## Syncing

```bash
emerge-websync
```

## Perusing Latest News

```bash
eselect news list 
eselect news read | more
```

## Choose The Right Profile

Get a list of System Models.

```bash
eselect profile list
```

## Choosing from a List of System Models

```bash
# 36 is default/linux/amd64/17.0/musl (exp)
eselect profile set --force 36
```

Those index numbers can change weekly, so check for the correct index number to this 'amd64 musl'.


# Configuring USE

Add the following to /etc/portage/make.conf
```
USE="acl -alsa cdr curl dvd -emacs ipv6 -kde -gnome -gtk mount openrc pam -qt5 readline -systemd usbredir vim vim-syntax x86-64 -X"
```


## Updating Entire World

Within the given Gentoo stage 3 that we chose and installed, update the entire
thing with the latest and greatest repositories:

```
emerge --ask --verbose --update --deep --newuse @world
```

Required packages for basic QEMU of Linux kernel, OpenRC, portage, modules

```bash
emerge sys-kernel/gentoo-sources
emerge app-editors/vim    # optional
emerge net-misc/openssh    # optional
```


# Selecting Kernel

```
eselect kernel list
eselect kernel set 1  # there shall only be one
```


# Installing Kernel Tools

```
emerge dev-vcs/git
emerge app-portage/cpuid2cpuflags
emerge virtual/libudev
emerge sys-apps/pciutils
emerge app-portage/gentoolkit
emerge sys-kernel/genkernel   # pulls in linux-firmware
emerge sys-power/acpid  # for proper shutdown by VM host manager
emerge sys-boot/grub

# following are optional
# emerge sys-apps/hwdata  # pulled in by sys-apps/pciutils
# emerge sys-apps/usbutils
# emerge media-libs/freetype
# emerge sys-libs/efivar     # only if UEFI used instead of BIOS
# emerge sys-boot/efibootmgr # only if UEFI used instead of BIOS
```

This has to be done AFTER kernel source has been e-selected.

SECURITY: I do not install SSH server.  If this VM needs network access, the VM itself can do the SSH or RSYNC protocol as a client.


# Defaulting Kernel Configuration

If no kernel (`.config`) configuration file exist, create one
with all of its default settings:

```bash
cd /usr/src/linux
make oldconfig
```

Note: If `.config` exist, then it shall have any and all newer Kconfig settings added at default setting (using `oldconfig` make option).

Note: If `.config` does not exist, then default settings are used.


# QEMU-related Driver Support

## Gateway-Related QEMU Settings

Of course, a gateway OS that is NOT directly on a physical host but instead inside a virtual machine typically does not have the following, for security reason:

* a soundcard (not even a tinny-souding PC speaker)
* USB memory stick access
* CD/DVD access (it's a potential malicious vector, turn BIOS off to that too)
* HugePageTLB (prevents heap-spraying)
* libmusl (prevents `LD_PRELOAD` attacks at user-level)
* No JIT-based application needing write/execute memory segments (Numba/Pyjion/Cinder/Piston-lite/Jpython/IronPython/PyPy/Chrome/Firefox/Acrobat Multimedia)


# Kernel configuration

## Dell-specific driver support

### Boot-specific

```ini
CONFIG_AMD_PLATFORM_DEVICE=n
CONFIG_CPU_SUP_AMD=n
CONFIG_EFI=n
CONFIG_PERF_EVENTS_AMD_POWER=n
CONFIG_PERF_EVENTS_AMD_UNCORE=n
CONFIG_MICROCODE=intel
CONFIG_MICROCODE_INTEL=y
CONFIG_MICROCODE_AMD=n
CONFIG_AMD_MEM_ENCRYPT=n
CONFIG_ARCH_SUPPORTS_ACPI=y
CONFIG_ACPI=y
CONFIG_ACPI_LEGACY_TABLES_LOOKUP=y
CONFIG_ARCH_MIGHT_HAVE_ACPI_PDC=y
CONFIG_ACPI_SYSTEM_POWER_STATES_SUPPORT=y
CONFIG_ACPI_AC=y
CONFIG_ACPI_BATTERY=n
CONFIG_ACPI_BUTTON=y
CONFIG_ACPI_FAN=y
CONFIG_ACPI_THERMAL=y
CONFIG_SENSORS_*=n

```

### CPU-specific

For my Intel Core i7-2600 CPU processor, the kernel config settings are also set:

```ini
CONFIG_NUMA=n
CONFIG_AMD=n
CONFIG_AMD_PMC=n
CONFIG_AMD_IOMMU=n
CONFIG_AMD_MEM_ENCRYPT=n
CONFIG_AMD_NB=n
```

There are [kernel tools](https://stackoverflow.com/questions/27090431/linux-kconfig-command-line-interface/70728869#70728869) that allows for multiple `.config` (in form of `config.XXXXX` filename).


```bash
cd /usr/src/linux
make listnewconfig   # a safe passive (non-changing) status command
```
The output of `listnewconfig` should be empty (no new config undefined).


# Configuring Kernel for QEMU

```bash
cd /usr/src/linux
make menuconfig

# introduce gcc CFLAGS here
export CFLAGS="-Ofast -march=native -flto"

make && make modules install
```


Optionally, tweak "boot cmdline" in `/etc/default/grub`.  This becomes
a required step if not using UUID for device identifier within GRUB2.

```ini
GRUB_DISABLE_LINUX_UUID=true
GRUB_CMDLINX_LINUX="root=/dev/sda3 nofb vga=current"
GRUB_DISABLE_OS_PROBER=true
GRUB_TIMEOUT=5
GRUB_DISABLE_UUID=true
```

Note: `nofb` is mandatory if a graphic card has been inserted into the PCI slot thus overriding Intel HD graphic card.
d
Note: `vga=current` compensates for any flakey or mis-configured graphic hardware settings.

Details of above GRUB2 settings can be found in [here](https://www.gnu.org/software/grub/manual/grub/grub.html#Simple-configuration).


# Genkernel

## Firmware Required for Genkernel

We must accept a bit more latitude and flexibility for firmware used
on Linux OS.  This is required for building using the `genkernel` tool.

Append the following text into `/etc/portage/package.license`:
```
# Accepting both licenses for linux-firmware
sys-kernel/linux-firmware linux-fw-redistributable no-source-code

# Accepting any license that permits redistribution
sys-kernel/linux-firmware @BINARY-REDISTRIBUTABLE
```

# Automated Kernel Build

Install the `genkernel` tool:

```bash
emerge --ask sys-kernel/linux-firmware
emerge --ask sys-kernel/genkernel
emerge --ask sys-kernel/dracut      # used with initramfs
```

Ensure that `/boot` is mounted for genkernel to fill in:
```bash
df | grep boot
```
If resultant output is empty, go mount the `/boot`:
```bash
mount /dev/sda1 /boot
```

Instructing InitRamFS to mount multiple disk partitions/volumes at boot.

```bash
vi /etc/initramfs.mounts
```
and put in something like what I use for CISecurity partitionings:
```
/usr
/tmp
/var
/var/tmp
/var/log
/var/log/audit
/home
#
# If you had some need of these:
#/usr/local
#/opt
```


# Build kernel for QEMU

Complete kernel build including all modules as denoted by 'make defconfig'
or after your kernel customization.

```
DATE="$(date +%F-%H-%M)"
genkernel \
          --loglevel=5 \
          --color \
          --kernel-append-localversion=-gateway-${DATE} \
          --microcode=intel \
          --menuconfig  \
          --bootloader=grub2 \
          --lvm \
          all     # (with modules)
```

## Rebuild Modules & Libraries

If tweaking kernel config on the second (or nth) pass, modules need to be rebuilt
```
emerge @module-rebuild     # rebuild modules
emerge @preserved-rebuild  # rebuild system libraries
```


# System Install


## Host and Domain Information

```bash
echo 'hostname="tux"' > /etc/conf.d/hostname
```

## Password Quality

To bastardize the password quality to that those of 1980-style:

Edit the line to reflect in the `/etc/security/passwdqc.conf` file:

```ini
min-default=24,8,8,7
match=0
```

Now you can use any 8-char simple password or longer.

```bash
passwd    # enter in your root password
```

## System Clock Timezone

Edit the timezone to your desire setting (I use UTC) in `/etc/conf.d/hwclock` file:
```ini
clock="UTC"
```


# Tools

## Syslog

Install the smallest syslog daemon possible, `sysklogd` and activate them at bootup:

```bash
emerge app-admin/sysklogd
emerge app-admin/syslog-ng
rc-update add sysklogd default
rc-update add syslog-ng default
```

## Remote Access (SSH)

Activate SSH server daemon:

```bash
rc-update add sshd default
```

Maybe allow root to log in (for the short-term during setup) by adding:

```ini
PermitRootLogin=yes
```
into the `/etc/ssh/sshd_config` SSH daemon config file.

## Serial Console

On OpenRC, ensure that the serial console section in /etc/inittab are
commented out (prepend with `#`) in `/etc/inittab` file:

```
# SERIAL CONSOLES
#s0:12345:respawn:/sbin/agetty 9600 ttyS0 vt100
#s1:12345:respawn:/sbin/agetty 9600 ttyS1 vt100
```

## Time Synchronization

Install `chronyd` and activate it:

```bash
emerge net-misc/chrony
rc-update add chronyd default
```


## Filesystem Tools

Install filesystem tools:

```bash
emerge sys-fs/btrfs-progs   # for BtrFS
emerge sys-fs/e2fsprogs     ax1800# for Ext2/Ext3/Ext4
```


## Network Tools

### DHCP Client

We are using ISC DHCP client on one side of the network, and  our ISP DHCP server is on the other side; add some editor syntax coloring:

```bash
emerge dhcp dhcpd-syntax
```


# Bootloader 

## Selecting Bootloader Package

To select a Grub2 bootloader:

```bash
emerge --ask --update --newuse --verbose sys-boot/grub
```

## Install GRUB2 Bootloader

```bash
grub-install /dev/sda
```


## Configuring GRUB2

```bash
   # reads from /etc/default/grub
   # reads from /etc/grub.d/*

   grub-mkconfig -o /boot/grub/grub.cfg
```

# Rebooting

Exit and then reboot

```console
(chroot) / # exit
/root # reboot
```

