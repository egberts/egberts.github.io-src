title: Resuming Gentoo OS after reboot
date: 2022-07-24 01:38
status: published
tags: Gentoo, gateway, musl, libmusl, Linux
category: HOWTO
summary: How to resume installing Gentoo Linux OS
slug: gentoo-qemu-setup-resume
lang: en
private: False


How to resume the setup the Gentoo OS ... within the QEMU VM startup.

This would be extremely useful if you are doing a major developmental
iteration of tweaking Linux kernel ... within Gentoo rescue disk.

This article details in the fewest amount of step to revert to the
resume checkpoint for additional kernel tweaking.

This article assumes that you have gotten as far as `tar pxvf` command
of installing the Stage 3 tarball file, which is after disk partition
and filesystem layout (`/etc/fstab`).

# Mount Root

```bash
swapon /dev/vda2
mount -t btrfs /dev/vda3 /mnt/gentoo
date
wget -O - https://qa-reports.gentoo.org/output/service-keys.gpg | gpg --import
cat /etc/resolv.conf
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

# Mount Boot Partition
mount /dev/vda1 /boot

# Show active network links
ip addr

emerge --sync

# Choose The Right Profile
# 35 is default/linux/amd64/17.0/musl (exp)
# ensure that a blue asterisk is next to #35
eselect profile list

# if any change in USE= within /etc/portage/make.conf, uncomment next line
#emerge --ask --verbose --update --deep --newuse @world

# Selecting Kernel
# 1 is linux-5.xx.xx-gentoo
# ensure that a blue asterisk is next to #1
eselect kernel list

# List expected QEMU modules
lspci -k | grep driv | sort -u
# must list: ahci, i801_smbus, lpc_ich, pcieport, virtio-pci, xhci_hcd

cd /usr/src/linux

#make oldconfig
# CONFIG_VIRTIO=y
# CONFIG_ARCH_HAS_RESTRICTED_VIRTIO_MEMORY_ACCESS=y
# CONFIG_VIRTIO_PCI_LIB=y
# CONFIG_VIRTIO_PCI_LIB_LEGACY=y
# CONFIG_VIRTIO_MENU=y
# CONFIG_HW_RANDOM_VIRTIO=y
# CONFIG_VIRTIO_PCI=y
# CONFIG_VIRTIO_PCI_LEGACY=y
# CONFIG_VIRTIO_BALLOON=y
# CONFIG_VIRTIO_MEMORY=y
# CONFIG_VIRTIO_INPUT=y
# CONFIG_VIRTIO_CONSOLE=y
# CONFIG_VIRTIO_MMIO=y
# CONFIG_VIRTIO_MMIO_CMDLINE_DEVICES=y
# CONFIG_VIRTIO_IOMMU=y
# CONFIG_VIRTIO_DMA_SHARED_BUFFER=y
# CONFIG_VIRTIO_BLK=y
# CONFIG_BLK_MQ_VIRTIO=y
# CONFIG_SCSI_VIRTIO=y
# CONFIG_VIRTIO_NET=y
# CONFIG_RPMSG_VIRTIO=n
# CONFIG_CRYPTO_DEV_VIRTIO=y


# Ways to Build a Kernel

There are two ways to build a Linux kernel:

* directly using `make`
* `genkernel` tool

##  Directly Build a Kernel

```bash
# make && make modules install  # if not using genkernel
```

##  Using `genkernel` build tool

alternatively, you could use the Gentoo `genkernel` build tool.

```console
# emerge --ask sys-kernel/genkernel
# emerge --ask sys-kernel/dracut      # used with initramfs

# list 2 mounted partitions
df | grep vda

# Complete kernel build including all modules as denoted by 'make defconfig'
# or after your kernel customization.
genkernel --color \
          --loglevel=5 \
          --virtio \
          --no-lvm \
          --bootloader=grub2 \
          --menuconfig \
          --static \
          all     # (with modules)

#  or for a static kernel build without any module support.
#genkernel --menuconfig bzImage # (module-less)

cat /etc/conf.d/hostname   # ensure desired hostname
cat /etc/conf.d/hwclock   # ensure desired timezone

cat /etc/dhcp/dhclient.conf  # ensure customized DHCP client settings


grub-install --verbose /dev/vda

# Configuring GRUB2
# reads from /etc/default/grub
# reads from /etc/grub.d/*
grub-mkconfig -o /boot/grub/grub.cfg


# Rebooting
exit
reboot
```


# Conclusion

Enjoy
