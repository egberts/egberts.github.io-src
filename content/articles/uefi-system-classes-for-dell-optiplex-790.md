title: UEFI System Classes for Dell Optiplex 790 
date: 2022-09-29 08:47
status: published
tags: UEFI, Optiplex
category: research
summary: A detailed insight on about UEFI for Linux and Dell Optiplex 790 (2012)
slug: uefi-class-dell-optiplex-790
lang: en
private: False


# Classes of UEFI systems

UEFI Class 0
 - Legacy BIOS
 - No UEFI or UEFI PI interfaces

UEFI Class 1  (Dell Optiplex 790)
 - Uses UEFI/PI interfaces
 - Runtime exposes only legacy BIOS runtime interfaces
 - Cannot use GPT on primary hard drive
 - No Secure Boot
 - MBR legacy only
 - No ACPI 2.0 support (Dell Optiplex 790)
 - No UEFI 2.3.1 support (Dell Optiplex 790)

UEFI Class 2
 - Uses UEFI/PI interfaces
 - Runtime exposes only UEFI and legacy BIOS interfaces
 - No legacy support of CSM

UEFI Class 3
 - Uses UEFI/PI interfaces
 - Runtime exposes only UEFI interfaces


# UEFI Details

The 790 has class 1 Bios.

Class 2.3.1 UEFI bios is required for GPT UEFI Secure boot.

New systems are class 3 bios with no legacy booting of anything.

Intel will be only supporting UEFI Class 3, which means no legacy support of CSM.  It also means windows 10 only and 64 bit only from now on.

The 790 allows legacy as well as 32 bit windows xp and therefore will never have secure boot due to lacking ACPI 2.0 and UEFI 2.3.1

Firmware that meets the UEFI 2.3.1 specifications

Secure boot certificates cannot be added as a bios update by end users.

Only OEM's can do that.

is required for Windows 10 security features like Secure Boot, Windows Defender Credential Guard, and Windows Defender Exploit Guard.

Platform firmware must ensure that operating system physical memory is consistent across S4 sleep state transitions, in both size and location. Operating system physical memory is defined according to the ACPI 3.0 specification.

Class 2.3.1 UEFI BIOS must have windows key built in and must be digitally signed with a Windows, WHQL, ELAM, or Store certificate (WHQL 64 bit).

.

http://www.uefi.org/sites/default/files/resources/2.3.1_D.pdf
