title: Creating an emulated QEMU using virt-manager
date: 2022-08-06 16:17
modified: 2025-12-30 05:35
status: draft
tags: QEMU, virt-manager
category: howto
summary: How to create an emulated QEMU startup using virt-manager
slug: virt-manager-qemu-create
lang: en
private: False

This article outlines the creation of an emulated QEMU startup using virt-manager.

Emulated QEMU does not allow direct machine code execution as this is considered the safest but also the slowest method.  Alternatively, you may be interested the fastest and fairly safe QEMU/KVM method in [[{filename}virt-manager-qemu-kvm.md]].

Version 4.0 of virt-manager is used here, on Debian 11.


# Troubleshooting

## Incomplete Boots

### Firmware hang

If the following lines were the last breath of a failed Gentoo boot:

```console
[  0.95951] Loading firmware: regulatory.db
[  0.95980] platform regulatory.0: Direct firmware load for regulatory.db
```
then the next line (that is missing) is your video driver bootup failed.

Workaround:  Go back to the `virt-manager` `View->Detail` submenu and change the `Video Virtio` into `Video QXL`.


Enjoy
