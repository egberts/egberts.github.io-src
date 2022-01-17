title: How to access Proxmox QEMU image, MS-DOS formatted
date: 2022-01-16 09:56
status: published
tags: ArchLinux, Proxmox, QEMU, MS-DOS, grub
category: HOWTO
lang: en
private: False

You fired up the QEMU image of ArchLinux distro within a Proxmox server.

And the BIOS/GRUB boot dies.  

Worse, you've shortened the BOOT\_TIMEOUT to an insane `0` second.  

And Proxmox JavaScript-based console isn't letting you get into the GRUB menu mode.

It's nigh time to access that dead VM's disk image and its EXT4 filesystem directly.  And try to undo the botched initramfs-less kernel.

```bash
kpartx -av /dev/pve/vm-134-disk-0 
mount -t ext4 /dev/vg-archlinux/root /mnt/134
mount -t ext4 /dev/mapper/pve-vm--134--disk--0p1 /mnt/134/boot
mount -t ext4 /dev/vg-archlinux/var /mnt/134/var
mount -t ext4 /dev/vg-archlinux/usr /mnt/134/usr
mount -t ext4 /dev/vg-archlinux/tmp /mnt/134/tmp
mount -t devtmpfs none /mnt/134/dev  # you get your /dev/[null,zero,true] here
chroot /mnt/134
```
At this point, the full QEMU filesystem for ArchLinux is now `chroot` at `/` directory.

Head over to the linux build subdirectory.

First glance is that my Linux kernel `.config` had `CONFIG_COMPAT_BINFMT_ELF`
turned off which explains the boot-up stoppage:
```console
   Booting `Arch Linux'

Loading Linux linux515 ...
Loading initial ramdisk ...
```
And not seeing further activities, much less any EXT4-related ones.

Upon closer examination of my botched `.config` file also showed that I had turned off `CONFIG_BINFMT_SCRIPT` (along with `CONFIG_BINFMT_MISC`).

Side effect of not having `CONFIG_BINFMT_SCRIPT` is not being able to run the RC
startup script.

Thankfully, the entire `chroot` was recreated so I could do 
an out-of-QEMU kernel build there and reinstall the drive
