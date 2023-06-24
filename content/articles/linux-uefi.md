title:  Linux on UEFI
date: 2022-09-26 08:58
status: published
tags: UEFI, Linux
category: research
summary: Everything about UEFI and Linux
lang: en
private: False

This article is about UEFI and everything about Linux on top of UEFI.

UPDATE:  Aborted due to Dell Optiplex 790 not being a UEFI Class 2 or better (it is Class 1, no GPT nor Secure-Boot support).

# Partition required


UEFI requires a FAT formatted partition. 

FAT partition may be anywhere on any BIOS-accessible storage media (hard drive, SSD, USB drive, CD, DVD) drive.

It is common to use the first partition of the first storage media found on PCI bus during BIOS initialization.


## Create partition

A partition gets created using `fdisk` utility but only after using `g` option to move away from master boot record (MBR) into GFI format.

```
fdisk /dev/sda1
```


## Format partition

This partition is then formatted as FAT (VFAT 8/16/32) using `mkfs.fat`:

```
mkfs.fat -c -F 32 -v /dev/sda1
```


## Making partition non-DOS-MBR-like

Then we need to remove the MBR dirty bit because we are using GFI-formatted storage drive:

```
fsck /dev/sda1

```

## Mounting UEFI partition

Lastly, mount the `/boot` partition:

```bash
mount /dev/sda1 /boot -o noauto,nouser,rw,noatime,fmask=0022,dmask=0022,codepage=437,iocharsedt= iso8859-1,shortname=mixed,errors=remount-ro

# Build kernel

Build the Linux kernel and install it into the /boot partition

```
genkernel --loglevel=5 \
     --save-config \
    --kernel-append-localversion="-gateway1"
    --menuconfig \
    --oldconfig \
    --microcode=intel \
    --no-static \
    --all-ramdisk-modules \
    --lvm \
    $1 \
    all   # all == install+build+modules+initramfs
```

# Updating UEFI

Write the location of the `/boot/vmimage-*` into the flash region of UEFI/BIOS.

```bash
# for old PC built before 2014
grub-install --verbose --target=x86_64-efi --efi-directory=/boot --removable

# for newer PC built after 2014
grub-install --verbose --target=x86_64-efi --efi-directory=/boot
```

# Updating GRUB menu loader

```bash
grub-mkconfig -o /boot/grub/grub.cfg
```

# Reference
