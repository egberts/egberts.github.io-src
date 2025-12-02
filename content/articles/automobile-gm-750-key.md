title: GM 750 ignition key
date: 2020-07-31 18:39
modified: 2025-12-02 07:52
status: published
tags: auto, cryptkey
category: research
summary: What's up with the GM 750 ignition key?

This article is about the General Motor chip in the ignition key.

Had to create another set of car key for a General Motor as the car 
that I had bought only came with one key.

After much perusal on the Internet for how to get this new set of key
plus a remote fob to go with it, I can now summarize what I've learned.

There are two components to the user-end of the said GM ignition system:

* Transponder key
* Remote keyless fob

Transponder Key
===============

General Motor part number for the uncut key blade is SKU: GM KEY 750.

General Motor part number for the uncut key blade is also B111-PT.

The GM KEY 750 is used in the following type of cars:

[jtable]
Year(s), Compatible Vehicles
2005—2005,Buick Allure
2008—2017,Buick Enclave
2008—2008,Buick LaCrosse
2006—2014,Buick Lucerne
2008—2014,Cadillac CTS
2006—2011,Cadillac DTS
2006—2014,Cadillac Escalade
2007—2013,Cadillac Escalade EXT
2007—2009,Cadillac SRX
2007—2014,Chevrolet Avalanche
2014—2014,Chevrolet Captiva
2005—2010,Chevrolet Cobalt
2007—2009,Chevrolet Equinox
2008—2014,Chevrolet Express
2006—2014,Chevrolet HHR
2006—2013,Chevrolet Impala
2014—2016,Chevrolet Impala Limited
2004—2014,Chevrolet Malibu
2013—2016,Chevrolet Malibu Classic
2004—2007,Chevrolet Malibu MAXX
2006—2007,Chevrolet Monte Carlo
2007—2015,Chevrolet Silverado
2006—2014,Chevrolet Suburban
2006—2014,Chevrolet Tahoe
2009—2017,Chevrolet Traverse
2008—2008,Chevrolet Uplander
2007—2017,GMC Acadia
2014—2014,GMC Canyon
2014—2014,GMC Explorer
2008—2014,GMC Savana
2007—2014,GMC Sierra
2017—2017,GMC Terrain
2006—2014,GMC Yukon
2007—2010,GMC Yukon Denali
2008—2009,Hummer H2
2007—2010,Pontiac G5
2005—2011,Pontiac G6
2007—2007,Pontiac Grand Prix
2006—2011,Pontiac Pursuit
2006—2011,Pontiac Solstice
2007—2009,Pontiac Torrent
2007—2009,Saturn Aura
2003—2007,Saturn ION
2007—2011,Saturn Outlook
2007—2010,Saturn Sky
2007—2011,Suzuki XL-7
[/jtable] 

TAG Transponder Chip
--------------------
The key has a chip embedded inside the plastic head part of the key.

The embedded chip component is a Philips 46 TAG Transponder.

Philips 46 ("wedge") plastic enclosure contains a 
[Philips Security Transponder plus Remote Keyless, HITAG2](https://www.datasheetq.com/PCF7946-doc-Philips) chip.

Datasheet specs are:

The HITAG2 is a high performance monolithic Security Transponder and 
Remote Keyless Entry Chip ideally suited for car immobiliser 
applications that incorporate keyless entry functions.

The HITAG2 PLUS transponder circuitry is compatible with the 
Security Transponder PCF7936AS to support mixed systems using 
a HITAG2 PLUS and a standard Security Transponder, 
PCF7936AS at the same time.

* Compatible with Security Transponder, PCF7936AS
* Rolling Code Generator for keyless entry
* 14-pin SO package

Manufacturer part number of this chip is PCF7946.

It has patented KEELOQ code hopping technology with bi-directional 
Transponder challenge-and-response Security into a single chip 
solution for logical and physical access control.

When used as a code hopping encoder, the PCR7946 is ideally suited 
to Keyless entry systems; vehicle and garage door access in 
particular. 

The same PCR7946 can also be used as a secure bi-directional 
Transponder for contactless token verification. 
These capabilities make the PCR7946 ideal for combined secure access 
control and identification applications, dramatically reducing the 
cost of hybrid transmitter/Transponder solutions.


Remote Keyless FOB
==================


Summary of Specifications
=========================

• 512 Byte EEPROM for extended data storage

RF Spec
-------
* 13.56MHz carrier frequency
* PWM/ASK modulation

Data Transmission
-----------------

* Max. of 6 bits customer programmable data
* Output data baud rate: 10kbps (Typ.) at VDD=3V
* 6 bits checksum for error rejection

Security Protocol Spec
----------------------
* KEELOQ® Classic 
    * (it is not KEELOQ® AES, because a learning process is required)
* Code-hopping Encoder
* 48 bit Secret Key
* Fast mutual authentication, 39ms
*  Programmable 64-bit encoder crypt key
*  Two 64-bit IFF keys
*  Keys are read protected
*  32-bit bi-directional challenge and response using one of two possible keys
* 69-bit transmission length
    * 32-bit hopping code, 
    * 37-bit nonencrypted portion
* Programmable 28/32-bit serial number
* 60-bit, read protected seed for secure learning
* Two IFF encryption algorithms
* Delayed counter increment mechanism
* Asynchronous transponder communication
* Transmissions include button Queuing information

Functional Spec
---------------
* OTP data memory
* 32 bit quasi unique device identification (serial number)
   and product type identification.
* RISC programmable device features
* Up to seven Keyless Entry command buttons

References
==========
* [title](https://a.b/)
