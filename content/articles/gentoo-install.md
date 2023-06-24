title: Gentoo OS install
date: 2022-09-24 12:25
status: published
tags: Gentoo, gateway, musl, libmusl, Linux
category: HOWTO
summary: How to install Gentoo 2022
slug: gentoo-install
lang: en
private: False


How to install the Gentoo OS from scratch ... for use as a home gateway.

This would be extremely useful for a home gateway (whose requirement is
not entailing MySQL database nor JavaScript-based web browsing or easily hijacked using a `LD_PRELOAD` environment variable.)


## Download ISO

Visit [Gentoo](https://www.gentoo.org) and click on "Get Gentoo" button at top-row navigation panel.

Under `amd64`, 'stage archives', select the desired ISO image.  

Of the several variants of Stage 3, I chose "OpenRC" because `systemd` PID 1 has too much network access privilege which IMHO is ripe for a file-less backdoor malware.  OpenRC PID 1 has no such network privilege (same as original ATT SysV `initrc`/`init.d`), which sets my security mind at ease.

Burn and insert CD then reboot into CD.

# Drive space

Assuming that `/dev/sda` is the first hardware drive, the bare minimum we divide that drive space.

[jtable]
partition number, physical partition, size amount, description
1, `/dev/sda1`, 1g, boot for BIOS or UEFI
2, `/dev/sda2`, (twice the size of your physical RAM)`, swap space
3, `/dev/sda3`, /`, 128g, "the" root partition
4. `/dev/sda4`, n/a, the rest of the remaining drive space, used as MBR extension for logical parition 5-9 or entirely by LVM at OS-level.

## Dividing up the drive space

Use `fdisk /dev/sda` and execute 'g' option for GFI/EUFI partition scheme (instead of MS-DOS/MBR/BIOS) disk boot sequence.

Do not use GNU `parted` for this approach.

  Partition 1 - 250MB - /boot  (should be 1G if heavy kernel tweaking)
  Partition 2 - 2GB - swap  (should be twice your total 'physical' memory)
  Partition 3 - 128GB - / (root) directory
  Partition 4 - remainder of drive space - 

Change the type of partition 1 to '81' (for 'Linux filesystem').
Change the type of partition 2 to '82' (for 'Linux Swap').
Change the type of partition 3 to '81' (for 'Linux filesystem').

## Filesystem in each partition

Create the filesystems:
```bash
mkfs.ext4 /dev/sda1
mkswap    /dev/sda2
mkfs.ext4 /dev/sda3
```

# Rescue Reboot

In the case that you rebooted while not finishing the rest of this document,
then this is your new starting point using Gentoo 2022 ISO CD.

## Enable Swapper

```
swapon /dev/sda2
```

# Mount the root partition

Now set up the root filesystem to hold the minimal Gentoo CD installation.

Create the parent root file path for our new Gentoo OS:
We defer mounting the boot partition for later.

```
mkdir --parents /mnt/gentoo
```

# Mount additional partitions (optional)

I often break out `/usr` into a separate partition plus I do the recommended CISecurity partitioning scheme:

[jtable]
device, path, options, boot sequence
`/dev/sda3`, `/`, noatime, 0 0
`/dev/sda1`, `/boot`, nodev,nouser,nosuid,noatime, 0 1
(see next section), `/usr`, nodev,nosuid,noatime, 0 2
(see next section), `/tmp`, noexec,nodev,nosuid,noatime, 0 2
(see next section), `/var`, nodev,nosuid,noatime, 0 2
(see next section), `/home`, nodev,nosuid,noatime, 0 2
(see next section), `/var/tmp`, nodev,nosuid,noatime, 0 3
(see next section), `/var/log`, nodev,nosuid,noatime, 0 3
(see next section), `/var/log/audit`, nodev,nosuid,noatime, 0 4
[/jtable]

We already did the first 4 partitions.

There are two ways to partition further by adding additional partitions:

1. physical partition (via `fdisk /dev/sda`)
2. logical parition (via `lvm` toolsuite)


## Physical partition approach

For the all-physical partition approach, create the following physical partitions based on not nominally consuming more than 10% of any parititon that are consumed by the Gentoo 2022 installation:

[jtable]
partition number, physical partition, size amount, description
1, `/dev/sda1`, 1g, boot for BIOS or UEFI
2, `/dev/sda2`, (twice the size of your physical RAM)`, swap space
3, `/dev/sda3`, /`, 128g, "the" root partition
4. `/dev/sda4`, n/a, the rest of the remaining drive space, extension for logical parition 5-9
5. `/dev/sda5`, `/usr`, 96g, UNIX-usr partition
6. `/dev/sda6`, `/var`, 96g, UNIX-var partition
7. `/dev/sda7`, `/tmp`, 24g, temporary space, cleaned out at each reboot
8. `/dev/sda8`, `/var/log`, 96g, log directory
9. `/dev/sda9`, `/var/log/audit`, 6g, audit directory
10. `/dev/sda10`, `/home`, (rest of remaining logical partition), `$HOME` directory for multi-users
[/jtable]
Write and quit from the `fdisk` tool.

Create the filesystems:
```bash
mkfs.ext4 /dev/sda1
mkswap    /dev/sda2
mkfs.ext4 /dev/sda3
mkfs.ext4 /dev/sda5
mkfs.ext4 /dev/sda6
mkfs.ext4 /dev/sda7
mkfs.ext4 /dev/sda8
mkfs.ext4 /dev/sda9
mkfs.ext4 /dev/sda10
```

Mount them in nested-order:

```bash
mount /dev/sda3 /mnt/gentoo
cd /mnt/gentoo
mkdir /mnt/gentoo/{boot,home,usr,var,tmp}
mount /dev/sda1 ./boot
mount /dev/sda5 ./usr
mount /dev/sda6 ./var
mkdir ./var/log
mount /dev/sda8 ./var/log
mkdir ./var/log/audit
mount /dev/sda9 ./var/log/audit
mount /dev/sda7 ./tmp
mount /dev/sda10 ./home
```


That is it for the physical partition approach (skip the LVM section).

## LVM approach



# Check the DateTimestamp

To ensure accurate recording of files being created on, check the date:

```bash
date                # to view the date
date 202207211500   # to change to July 21, 2022, 1500UTC
```


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

# Network Setup

I use the Gentoo `net-setup` to get the Internet up and running ... fast.

Use the 'manual configuration' option in `net-setup`, if you got some esoteric but exotic network setup.

# Obtain PGP Keys of Gentoo Organization

If not done already, save the PGP keys of the entire Gentoo organization:

```bash
wget -O - https://qa-reports.gentoo.org/output/service-keys.gpg | gpg --import
```


# Verify Gentoo Organization PGP keys

```bash
gpg --verify stage3-amd64-musl-20220720T2237212.tar.xz.DIGESTS.xz
```


# Validate Stage3 File

```console
# sha512sum -c --ignore-missing \
    stage3-amd64-musl-20220720T2237212.tar.xz.DIGESTS.xz
stage3-amd64-musl-20220720T2237212.tar.xz: OK
WARNING: 14 lines are improperly formatted
```

NOTE: WARNING is because I've opted to read a DIGEST file that has GnuPG headers and footers wrapped around the checksum values; we are only interested in the `OK` part of the `sha512sum` output.


# Unpack New Root Directory

Unpack the stage 3 tarball file that contains the initial root filesystem:

```
tar xpvf stage3-*.tar.xz --xattrs-include='*.*' --numeric-owner
```

If you know how many CPU processors you have, then you can increase
the make build tool with all those processors by leveraging `--job=` options of the make utility.  For two CPUs, execute:

```
echo 'MAKEOPTS="-j2"' >> /mnt/gentoo/etc/portage/make.conf
```

# Selecting Remote Sources

```bash
mirrorselect -i -o >> /mnt/gentoo/etc/portage/make.conf
```

# Required packages


Create a local repository for Gentoo portage packages:
```
mkdir --parents /mnt/gentoo/etc/portage/repos.conf
cp /mnt/gentoo/usr/share/portage/config/repos.conf /mnt/gentoo/etc/portage/repos.conf/gentoo.conf
```

# Get Networked

```bash
cp --dereference /etc/resolv.conf /mnt/gentoo/etc/
```

# Get partitions ready for new `chroot`

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

# Mount Boot Partition

```bash
mount /dev/sda1 /boot
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

SECURITY: I do not install SSH server on gateway (yeah, sneaker-net-protected).  


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


## Kernel configuration

### UEFI support for Linux

File `config-uefi.conf` contains:

```ini
CONFIG_RELOCATABLE=y
CONFIG_EFI=y
CONFIG_EFI_STUB=y
CONFIG_X86_SYSFB=y   # old
CONFIG_SYSFB=y
CONFIG_FB_SIMPLE=y  # old
CONFIG_SYSFB_SIMPLEFB=y
CONFIG_FRAMEBUFFER_CONSOLE=y
```

```ini
CONFIG_DRM_RADEON=y
CONFIG_FB_RADEON=y
CONFIG_FB_RADEON_I2C=y
CONFIG_FB_RADEON_BACKLIGHT=n
```

To merge the above settings into the `.config` file, execute:

```bash
cd /usr/src/linux
scripts/kconfig/merge_config.sh .config config.my-qemu-guest-virtio.conf
```

To ensure that we did not miss any new Kconfig settings for VirtIO (and other
but related kernel settings, bring `.config` up to date with newest (but defaulted) settings:

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


Optionally, tweak `BOOT_CMDLINE` in `/etc/default/grub`.  This becomes
a required step if not using UUID for device identifier within GRUB2.

```ini
GRUB_DISABLE_LINUX_UUID=true
GRUB_CMDLINX_LINUX="root=/dev/sda3"
GRUB_DISABLE_OS_PROBER=true
GRUB_TIMEOUT=5
GRUB_DISABLE_UUID=true
```
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
emerge --ask sys-kernel/genkernel
emerge --ask sys-kernel/dracut      # used with initramfs
```

## Filesystem Table (`/etc/fstab`)

Fill the `/etc/fstab` with the following content:

```
# Adjust any formatting difference and additional partitions created 
# from the Preparing the disks step
/dev/sda1   /boot        ext4    noauto,noatime       1 2
/dev/sda2   none         swap    sw                   0 0
/dev/sda3   /            ext4    noatime              0 1
  
/dev/cdrom  /mnt/cdrom   auto    noauto,user          0 0
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
genkernel \
          --loglevel=5 \
          --color \
          --kernel-append-localversion=-my-new-revision  \
          --virtio \
          --microcode=no \
          --menuconfig  \
          --bootloader=grub2 \
          --static \
          all     # (with modules)
```
or for a static kernel build without any module support.
```
    genkernel --menuconfig bzImage # (module-less)
```

## Rebuild Modules & Libraries

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
rc-update add sysklogd default
```

## Remote Access (SSH)

Activate SSH server daemon:

```bash
rc-update add sshd default
```

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
emerge sys-fs/e2fsprogs   # for Ext2/Ext3/Ext4
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

# Reference

* CIS Security Debian 10 Benchmark, 1.0, 2020-02-13

