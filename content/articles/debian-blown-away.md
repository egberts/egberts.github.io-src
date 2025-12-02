title: Debian Blown Away!
date: 2020-04-22 12:23
modified: 2022-04-04 11:10
status: published
tags: debian, recovery
category: HOWTO
summary: So you downgraded something and lost your Linux kernel.

For the life of me, I somehow entered in "Yes, I want to delete!" 
during Debian upgrade and lost not only the libc library but 
the Linux kernel too.  This happened in one of my VPS ("cloud").

This article details the cloud recovery using a Debian minimal CD ISO
image remotely mounted by the cloud provider's VPS management portal.

For some reason, Interserver.Net VPS management portal would not
let me supply a valid HTTPS to the portal.  It simply says "Invalid URL".

Yeah, three different valid URL (of which my web browser managed 
to download) but not at this Interserver.Net portal.  Opened a 
ticket, response in less than 10 minutes saying essentially 
"We mounted it for ya!".   I retried the image URL
again, it still says failed.

Lost my last remaining shell session too (the ones without the 
libc and kernel).  Mmmm.  This could have been handled better.  
Couldn't figure out the reason for this VPS reboot.  I didn't want this.
I wanted a live CD mount into existing system.  Perhaps, I could
see how this might have been a security risk from the POV of 
hosting providers' support folks just to have.

So I opened up a VNC session to the failing VPS: 

```bash
xtightvncviewer -noshared 999.999.999.999::99999
```

It's a password-less VNC session.  This cannot be good for secured 
reconstruction.  A race in time before this port gets discovered but 
'noshared' option should block concurrent connections (IF and 
only IF the VPS provider properly configured it; no way to 
verify that, either).  I tracerouted it and it is to some OTHER 
VPS hosting these VNC portals. Clearly an exposure there. Tsk tsk.  
Now, I hurry.

Desktop VNC window appears.  Yep, it got rebooted without my consent.
It is currently in Debian GNU Boot Prompt, ncurse-style of menu options.

Since I've lost the kernel narrative (read as, MY custom but secured 
variants of Debian linux kernel), whole system is contaminated all
because of a reboot, an unwanted reboot.


