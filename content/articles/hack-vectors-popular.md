title: Popular Hack Vectors on Windows
Date: 2016-04-03 01:14
tags: hack, vectors, methods
category: research
status: published
slug: hack-popular-vectors-windows
summary: Popular hack vectors in Windows

Most Popular Attacks
====================

In 2001, checksums were useful enough to confuse the reverse engineers of
network protocols.

Nowadays, PBKs with fancy debuggers are the greatest adversaries. Such fancy
debuggers are but not limited to:

* IDA Pro
* IDA Pro with HexRay
* OllyDbg
* WinDbg
* Cheat Engines
* Hopper
* Radare2

Some of the popular attack vector on Windows are:
* Protocols (`openssl.dll`, Win32 API TLS calls)
* Data: Windows `WM_GETTEXT`
* Code: IDA
    * For both encrypted and really-encrypted code: dumping+IDA or
      custom_loader+IDA
    * FLIRT, encrypted machine code
* Debugging+patching: disabling protection (mausy31)[https://www.youtube.com/watch?v=mOUPOkJoseE]
* Backtracing stack - this is where system calls cannot hide and who is calling these system calls
* Debugging: data-analysis: RTTI, VMT pointer (Sabanal Yason)[https://www.blackhat.com/presentations/bh-dc-07/Sabanal_Yason/Paper/bh-dc-07-Sabanal_Yason-WP.pdf]
* Protocol-level: Self-MitM
* Hooks (Aiko)[https://www.blackhat.com/presentations/bh-jp-08/bh-jp-08-Aiko/bh-jp-08-Aiko-EN.pdf]

