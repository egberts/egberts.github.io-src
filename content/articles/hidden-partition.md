title: Wiping Device Drives Securely
date: 2022-06-24 08:09
status: published
tags: HDD, SDD
category: research
lang: en
private: False

# Hidden Partition

Things to do when re-using a hard drive of unknown source (Craig's List, in my example).

* Self-Encrypting Drive (SED)
* ATA Security
* * Unlock the hard drive
* * Check for hidden partition
* * * Host Protected Area
* * * DCO - Device Configuration Overlay
* Wipe the hard drive

# Self-Encrypting Drive (SED)

Self-encrypting drive have firmware support that will take a key and do the encryption/decryption at
the hard drive controller.

OPAL and `sedutil` provide settings to the SED.

Must allow ATA to be access by TPM:
```console
$ echo "1" > /sys/module/libata/parameters/allow_tpm
```
or most probably by adding `libata.allow_tpm=1`
to the kernel flags at boot time due to restrictive `/sys` write.


# ATA Security

ATA-4 secification allows for locking the hard drive.  Nothing to do with encryption whatsoever.  

This ATA-4 security lock is easily circumventable by relocating the drive to a different platform or 
a different ATA controller having its own BIOS (ie., Dell R710 PERC6i RAID).



# # Unlock the Hard Drive

Fortunately, locking mechanism of the hard drive is enforced only by the BIOS that it is controlled by.

A simple relocation of hard drive to another BIOS system will get the needed unlock.

You can even do a hot-plug after BIOS bootup (on its original system) of this hard drive to get it unlocked.

Unfortunately, some USB-SATA enclosure will not support SATA hot-plugging, caveat emptor.


# Wipe the Hard Drive

Two ways to securely wipe the hard drive (in Linux):

Using `shred` (as part of `coreutils` packae):
```console
$ sudo shred -vfz -n 10 /dev/sda
```
or alternatively,
```console
# replace 'sdX' with actual hard drive
# takes care of bad sectors
# takes care of residual magnetism
i=0
while [[ $i -le 10 ]]; do
  dd if=/dev/urandom of=/dev/sdX bs=1M 
  ((i=i+1))
done
$ dd if=/dev/zero of=/dev/sdX bs=1M
```

# HPA - Host protected area

The Host Protected Area (HPA) is an area of a hard drive or solid-state drive that is not normally visible to an operating system. It was first introduced in the ATA-4 standard CXV (T13) in 2001.

How it works:

The IDE controller has registers that contain data that can be queried using ATA commands. The data returned gives information about the drive attached to the controller. There are three ATA commands involved in creating and using a host protected area. The commands are:

    IDENTIFY DEVICE
    SET MAX ADDRESS
    READ NATIVE MAX ADDRESS

Operating systems use the IDENTIFY DEVICE command to find out the addressable space of a hard drive. The IDENTIFY DEVICE command queries a particular register on the IDE controller to establish the size of a drive.

This register however can be changed using the SET MAX ADDRESS ATA command. If the value in the register is set to less than the actual hard drive size then effectively a host protected area is created. It is protected because the OS will work with only the value in the register that is returned by the IDENTIFY DEVICE command and thus will normally be unable to address the parts of the drive that lie within the HPA.

The HPA is useful only if other software or firmware (e.g. BIOS) is able to use it. Software and firmware that are able to use the HPA are referred to as 'HPA aware'. The ATA command that these entities use is called READ NATIVE MAX ADDRESS. This command accesses a register that contains the true size of the hard drive. To use the area, the controlling HPA-aware program changes the value of the register read by IDENTIFY DEVICE to that found in the register read by READ NATIVE MAX ADDRESS. When its operations are complete, the register read by IDENTIFY DEVICE is returned to its original fake value.
Figure 1: Creation of an HPA

The diagram shows how a host protected area (HPA) is created:

    IDENTIFY DEVICE returns the true size of the hard drive. READ NATIVE MAX ADDRESS returns the true size of the hard drive
    SET MAX ADDRESS reduces the reported size of the hard drive. READ NATIVE MAX ADDRESS returns the true size of the hard drive. An HPA has been created
    IDENTIFY DEVICE returns the now fake size of the hard drive. READ NATIVE MAX ADDRESS returns the true size of the hard drive, the HPA is in existence

Usage:

    At the time HPA was first implemented on hard-disk firmware, some BIOS had difficulty booting with large hard disks. An initial HPA could then be set (by some jumpers on the hard disk) to limit the number of cylinder to 4095 or 4096 so that older BIOS would start. It was then the job of the boot loader to reset the HPA so that the operating system would see the full hard-disk storage space
    HPA can be used by various booting and diagnostic utilities, normally in conjunction with the BIOS. An example of this implementation is the Phoenix First BIOS, which uses Boot Engineering Extension Record (BEER) and Protected Area Run Time Interface Extension Services (PARTIES). Another example is the Gujin installer which can install the bootloader in BEER, naming that pseudo-partition /dev/hda0 or /dev/sdb0; then only cold boots (from power-down) will succeed because warm boots (from Ctrl-Alt-Delete) will not be able to read the HPA
    Computer manufacturers may use the area to contain a preloaded OS for install and recovery purposes (instead of providing DVD or CD media)
    Dell notebooks hide Dell MediaDirect utility in HPA. IBM ThinkPad and LG notebooks hide system restore software in HPA
    HPA is also used by various theft recovery and monitoring service vendors. For example, the laptop security firm Computrace use the HPA to load software that reports to their servers whenever the machine is booted on a network. HPA is useful to them because even when a stolen laptop has its hard drive formatted the HPA remains untouched
    HPA can also be used to store data that is deemed illegal and is thus of interest to government and police
    Some vendor-specific external drive enclosures (Maxtor) are known to use HPA to limit the capacity of unknown replacement hard drives installed into the enclosure. When this occurs, the drive may appear to be limited in size (e.g. 128 GB), which can look like a BIOS or dynamic drive overlay (DDO) problem. In this case, one must use software utilities (see below) that use READ NATIVE MAX ADDRESS and SET MAX ADDRESS to change the drive's reported size back to its native size, and avoid using the external enclosure again with the affected drive
    Some rootkits hide in the HPA to avoid being detected by anti-rootkit and antivirus software
    Some NSA exploits use the HPA for application persistence

## DCO - Device Configuration Overlay

Device Configuration Overlay (DCO) is a hidden area on many of today’s hard disk drives (HDDs). Usually when information is stored in either the DCO or host protected area (HPA), it is not accessible by the BIOS, OS, or the user. However, certain tools can be used to modify the HPA or DCO. The system uses the IDENTIFY_DEVICE command to determine the supported features of a given hard drive, but the DCO can report to this command that supported features are nonexistent or that the drive is smaller than it actually is. To determine the actual size and features of a disk, the DEVICE_CONFIGURATION_IDENTIFY command is used, and the output of this command can be compared to the output of IDENTIFY_DEVICE to see if a DCO is present on a given hard drive. Most major tools will remove the DCO in order to fully image a hard drive, using the DEVICE_CONFIGURATION_RESET command. This permanently alters the disk, unlike with the (HPA), which can be temporarily removed for a power cycle.

Usage:

The Device Configuration Overlay (DCO), which was first introduced in the ATA-6 standard, "allows system vendors to purchase HDDs from different manufacturers with potentially different sizes, and then configure all HDDs to have the same number of sectors. An example of this would be using DCO to make an 80-gigabyte HDD appear as a 60-gigabyte HDD to both the (OS) and the BIOS.... Given the potential to place data in these hidden areas, this is an area of concern for computer forensics investigators. An additional issue for forensic investigators is imaging the HDD that has the HPA and/or DCO on it. While certain vendors claim that their tools are able to both properly detect and image the HPA, they are either silent on the handling of the DCO or indicate that this is beyond the capabilities of their tool.

# References

* [OPAL](https://en.wikipedia.org/wiki/Opal_Storage_Specification)
* [Self-encrypting drive](https://wiki.archlinux.org/title/Self-encrypting_drives)
* [sedutil](https://github.com/Drive-Trust-Alliance/sedutil)
