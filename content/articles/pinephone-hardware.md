title: Pinephone hardware
date: 2021-01-18 09:00
status: published
tags: pinephone
category: research
summary: Details of Pinephone hardware
lang: en
private: False


PinePhone with a case
=====================
[jtable]
Manufacturer, PINE64
Name, PinePhone
Codename, pine64-pinephone
Released, 2019
Category, main
Original software, postmarketOS
[/jtable]

PinePhone Hardware
==================
[jtable]
Battery, Samsung J7 3000mAh
Chipset, Allwinner A64 @ 1.152GHz
CPU, Quad-Core (4x) ARM Cortex-A53
GPU, Mali-400 MP2
Display, 720x1440 IPS LCD, 5.9"
Storage, 16 GB / 32 GB
Memory, 2 GB / 3 GB
Architecture, aarch64
Non-Android based device, Yes
Unixbench Whet/Dhry score, 1314.3
[/jtable]

Pinephone Features
==================
[jtable]
Type, Chipset, Driver, Status
Acceleration 3D (Sixaxis), InvenSense MPU-6050, INV_MPU6050_I2C, Works
Ambient light / Proximity, SensorTek STK3335, STK3310,
Battery fuel guage, X-Powers AXP803, BATTERY_AXP20X, Works
Bluetooth, Realtek RTL8723CS, BT\_HCIUART\_RTL, Works
Camera (Rear), OmniVision OV5640 2Mpixel, VIDEO\_OV5640, Partial
Camera (Front), GalaxyCore GC2145 5Mpixel [GC2145](https://wiki.postmarketos.org/wiki/PINE64_PinePhone_(pine64-pinephone)), no
Camera (Flash), SGMICRO SGM3140, LEDS\_SGM3140, Unavailable
Display (LCD), Xingbangda XBD599, CONFIG\_DRM\_PANEL\_XINGBANGDA\_XBD599, Works
GNSS/GPS, Quectel EC25-G, CONFIG_USB_SERIAL_OPTION, Works
GPU, Mali 400 MP2, , Works
LED (Notification), LED0603RGB, LEDS_GPIO, Works
Magentometer, ST LIS3MDL, IIO_ST_MAGN_3AXIS, Works
Memory (RAM), 2GB,, Works
Memory (Storage), 16GB,, Works
Modem, Quectel EC25-G, USB\_NET\_QMI\_WWAN, Works
Power button, X-Powers AXP803, INPUT_AXP20X_PEK, Works
Serial console, USB, /dev/ttyUSB2, Works
Touchscreen, Goodix GT917S, TOUCHSCREEN_GOODIX, Works
Vibration motor, (unknown), INPUT_GPIO_VIBRA, Works
WiFi, Realtek RTL8723CS, RTL8723CS, Works
Volume buttons, Buttons connected to the KEYADC, KEYBOARD_SUN4I_LRADC, Works
[/jtable]

USB Networking, Works
Xwayland, Works
FDE, Works
Mainline, Works
Battery, Works
Accelerometer, Works
Audio, Works
Mobile data, Works
SMS, Works
USB OTG, Broken


Hardware DIP switches
=====================
There's a 6 contact dipswitch on the back of the phone underneath the back cover. The 6 switches are for enabling/disabling hardware components. The switch has tiny numbers 1-6 beneath the contacts, moving the contact up sets that contact on.
[jtable]
\#, Off, On
1, Modem disabled, Modem enabled
2, Wifi/BT disabled, Wifi/BT enabled
3, Microphone disabled, Microphone enabled
4, Rear camera disabled, Rear camera enabled
5, Front camera disabled, Front camera enabled
6, Headphone UART mode, Headphone audio mode 
[/jtable]

Pinephone CPU
=============
Pinephone CPU is an Allwinner A64 1.2Ghz 4x Cortex-A53, 64-bit, superscalar, 32KB instruction & 32KB data L1 cache per core, 512KB L2 shared cache, ARM Mali-400 MP2 (Utgard) GPU, HDMI 1.4 (up to 4K@30), USB 2.0 with OTG, MIPI CSI, 4 channels in/out, 24-bit, 8-48 KHz audio, video encode: H.264 1080p@60, video decode: H.265 4K@30, H.265 1080p@120, H.264, MPEG1/2/4 / VP8 / AVS / AVS+ 1080p@60, FBGA-396 15x15 mm
Note: Clocked at 1.152Ghz on the PinePhone.

Pinephone Display
=================
The Pinephone display is a LCM/CTP which stands for liquid crystal display monitor/capacitive touch panel". An LCM generally includes an LCD screen + LED backlight + PCB with the LCD controller + frame.

LCD Panel is a [Xingbangda XBD599](https://lkml.org/lkml/2020/6/16/1654), 5.99″ IPS LCD, 720x1440 pixels, 16.7M colors, hardened glass.

LCD Driver is a [Sitronix ST7703](http://files.pine64.org/doc/datasheet/pinephone/ST7703_DS_v01_20160128.pdf) MIPI LCD driver.

Touchpanel is a [Goodix GT917S](http://files.pine64.org/doc/datasheet/pinephone/GT917S-Datasheet.pdf) touch controller.

Pinephone Data Communication
============================
Pinephone Modem - 4G
--------------------
Cellular modem is a [Quectel EG25-G](https://www.quectel.com/UploadFile/Product/Quectel_EG25-G_LTE_Specification_V1.1.pdf) GSM/UMTS/LTE cellular modem and GNSS (GPS/Galileo/GLONASS/BeiDou/QZSS, with A-GPS), LGA-144 9.0x32.0x2.4 mm.

Pinehone Wireless/Bluetooth
---------------------------
WiFi/Bluetooth is a [Realtek RTL8723CS](http://files.pine64.org/doc/datasheet/pine64/RTL8723BS.pdf) 802.11 b/g/n, single-band (2.4 GHz), Bluetooth 4.0, with SDIO for WiFi and UART for Bluetooth, LGA-40 12x12x1.6 mm.


References
==========
* [Pinephone component list](https://wiki.pine64.org/wiki/PinePhone_component_list)
