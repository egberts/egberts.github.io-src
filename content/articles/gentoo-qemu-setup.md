title: Gentoo OS for Home Gateway Router
date: 2022-07-22 01:38
status: published
tags: Gentoo, gateway, musl, libmusl, Linux
category: HOWTO
summary: How to setup Linux OS for Home Gateway Router
slug: gentoo-qemu-setup
lang: en
private: False


How to setup the Gentoo OS from scratch ... within the QEMU VM startup.

This would be extremely useful for a home gateway (whose requirement is
not entailing MySQL database nor JavaScript-based web browsing or easily hijacked using a `LD_PRELOAD` environment variable.)


## Download ISO

Visit [Gentoo](https://www.gentoo.org) and click on "Get Gentoo" button at top-row navigation panel.

Under `amd64`, 'stage archives', select the desired ISO image.  

Of the several variants of Stage 3, I chose "OpenRC" because `systemd` PID 1 has too much network access privilege which IMHO is ripe for a file-less backdoor malware.  OpenRC PID 1 has no such network privilege (same as original ATT SysV `initrc`/`init.d`), which sets my security mind at ease.


## Configure VM

At the host OS (virt-manager), point CD to minimal-gentoo.iso.

  - Reorder VirtIO and DVD so that VirtIO disk is first in boot ordering
  - Do not select "Enable direct kernel boot" option


# Create the VM


# Identify the hard drive 

Within the newly booted minimal Gentoo, identify the har drive used to hold our filesystems.

```
lsblk -a | grep -v ^loop | grep -v ^ram | grep disk
NAME   MAJOR:MIN RM   SIZE RO TYPE MOUNTPOINTS
vda      253:0    0    80G  0 disk
```

The hard drive provided by QEMU virtualization is `/dev/vda`.


# Format the hard drive

Use `fdisk /dev/vda` to continue to stay with the 'dos' (MS-DOS/MBR) disktype.

Do not use GNU `parted` for this QEMU.

  Partition 1 - 250MB - /boot  (should be 1G if heavy kernel tweaking)
  Partition 2 - 2GB - swap  (should be twice your total 'physical' memory)
  Partition 3 - remainder of QCOW2 media - ROOT label - / directory

Change the type of partition 2 to '82' (for 'Linux Swap').

Write out the entire partition table and quit.


# Format the partitions

Using a mixture of EXT4, BTRFS filesystems and swap space, execute:

```bash
mkfs.ext4  -L BOOT /dev/vda1
mkswap     -L SWAP /dev/vda2
mkfs.btrfs -L ROOT /dev/vda3
```

# Rescue Reboot

In the case that you rebooted while not finishing the rest of this document,
then this is your new starting point.

## Enable Swapper

```
swapon
```

# Mount the root partition

Now set up the root filesystem to hold the minimal Gentoo CD installation.

Create the parent root file path for our new Gentoo OS:
We defer mounting the boot partition for later.

```
mkdir --parents /mnt/gentoo
mount -t btrfs /dev/vda3 /mnt/gentoo
```

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
cd /mnt/gentoo  # that is /dev/vda3 partition
links https://www.gentoo.org/downloads/mirrors
```

Go down to 'Downloads' link and hit enter.

Go down to 'Advance choices and other architectures' section (past the 'amd64 aka x86-64, x64, Intel 64' section).

Select `amd64` link.

Go past just the 'Musl stage archives' section.

Select and download `Stage 3 musl | openrc 2022-XX-XX XXXMB`.

Make a note of the filename that you just saved.  My resultant filename is 'stage3-amd64-musl-20220720T2237212.tar.xz'.

Go down a bit further but just before the 'amd64' section, to 'All stages' link and press enter.

Select the 20220720T2237212Z subdirectory.

Go down to that filename you just saved.

Go down two more lines to the stage3-amd64-musl-20220720T2237212.tar.DIGESTS.gz file.  Download and save that file.


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
mount /dev/vda1 /boot
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
emerge --sync
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
# 35 is default/linux/amd64/17.0/musl (exp)
eselect profile set --force 35
```


# Configuring USE

Add the following to /etc/portage/make.conf
```
USE="acl -alsa cdr curl dvd ipv6 -kde -gnome -gtk pam -qt5 readline vim-syntax -X"
```


## Updating Entire World

Within the given Gentoo stage 3 that we chose and installed, update the entire
thing with the latest and greatest repositories:

```
emerge --ask --verbose --update --deep --newuse @world
```

Required packages for basic QEMU of Linux kernel, OpenRC, portage, modules

```bash
emerge sys-boot/grub
#    sys-libs/libpng
#    sys-apps/hwdata
#    virtual/libudev
#    media-libs/freetype
#    sys-apps/pciutils
#    sys-libs/efivar
#    sys-boot/efibootmgr
emerge app-portage/cpuid2cpuflags
emerge sys-kernel/gentoo-sources
emerge app-editors/vim
```


# Selecting Kernel

```
eselect kernel list
eselect kernel set 1  # there shall only be one
```


# Installing Kernel Tools

```
emerge sys-apps/pciutils
```

This has to be done AFTER kernel source has been selected.


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


## VirtIO Driver Support

Add the VirtIO drivers whose virtual 'hardware' are provided [by RedHat](https://cateee.net/lkddb/web-lkddb/VIRTIO.html) for use within QEMU by creating a small Kconfig file for merging into the `.config`.

There are [kernel tools](https://stackoverflow.com/questions/27090431/linux-kconfig-command-line-interface/70728869#70728869) that allows for multiple `.config` (in form of `config.XXXXX` filename).

```bash
vi config-qemu-guest-virtio.conf
```
and add the following Kconfig settings:
```ini
CONFIG_VIRTIO=y
CONFIG_ARCH_HAS_RESTRICTED_VIRTIO_MEMORY_ACCESS=y
CONFIG_VIRTIO_PCI_LIB=y
CONFIG_VIRTIO_PCI_LIB_LEGACY=y
CONFIG_VIRTIO_MENU=y
CONFIG_HW_RANDOM_VIRTIO=y
CONFIG_VIRTIO_PCI=y
CONFIG_VIRTIO_PCI_LEGACY=y
CONFIG_VIRTIO_BALLOON=y
CONFIG_VIRTIO_MEMORY=y
CONFIG_VIRTIO_INPUT=y
CONFIG_VIRTIO_CONSOLE=y
CONFIG_VIRTIO_MMIO=y
CONFIG_VIRTIO_MMIO_CMDLINE_DEVICES=y
CONFIG_VIRTIO_IOMMU=y
CONFIG_VIRTIO_DMA_SHARED_BUFFER=y
CONFIG_VIRTIO_BLK=y
CONFIG_BLK_MQ_VIRTIO=y
CONFIG_SCSI_VIRTIO=y
CONFIG_VIRTIO_NET=y
CONFIG_RPMSG_VIRTIO=n
CONFIG_CRYPTO_DEV_VIRTIO=y
```

To merge the above settings into the `.config` file, execute:

```bash
cd /usr/src/linux
scripts/kconfig/merge_config.sh config.my-qemu-guest-virtio
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
make && make modules install
```


Optionally, tweak BOOT_CMDLINE in /etc/default/grub.  This becomes
a required step if not using UUID for device identifier within GRUB2.

```ini
GRUB_DISABLE_LINUX_UUID=true
GRUB_CMDLINX_LINUX="root=/dev/vda3"
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

# Fill in Filesystem

Edit and ensure that the following is in `/etc/fstab`:
```
/dev/vda1    /boot      ext4   noauto,noatime  1 2
/dev/vda2    none       swap   sw              0 0
/dev/vda3    /          btrfs  noatime         0 1
/dev/cdrom   /mnt/cdrom auto   noauto,ro       0 0
```

Ensure that `/boot` is mounted for genkernel to fill in:
```bash
df | grep boot
```
If resultant output is empty, go mount the `/boot`:
```bash
mount /dev/vda1 /boot
```


# Build kernel for QEMU

Complete kernel build including all modules as denoted by 'make defconfig'
or after your kernel customization.

```
genkernel --static --bootloader=grub2 --loglevel=5 --virtio \
          --color --menuconfig all     # (with modules)
```
or for a static kernel build without any module support.
```
    genkernel --menuconfig bzImage # (module-less)
```

# Configure GRUB2 Bootloader



# Rebuild Bootloader using GRUB2

```bash
   # reads from /etc/default/grub
   # reads from /etc/grub.d/*

   grub-mkconfig -o /boot/grub/grub.cfg
```
