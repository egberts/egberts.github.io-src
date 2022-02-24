title: Host Names Used in ASUS Routers
date: 2022-02-23 15:54
status: published
tags: ASUS, router
category: research
summary: Hostnames Used in ASUS Routers
lang: en
private: False


The things that ASUS router do when resolving your DNS queries,
specifically the ASUS RT-AC68U with firmware `3.0.0.4.386_46065`.

They will substitute the following hostnames to your defined LAN-side IP address:

* `172.28.130.10 <yourhostname>.<yourdomainnametld> <yourhostname>`
* `172.28.130.10 <yourhostname>.local`
* `172.28.130.10 router.asus.com`
* `172.28.130.10 www.asusnetwork.net`
* `172.28.130.10 www.asusrouter.com`
* `172.28.130.10 RT-AC68U-DAE8.<yourdomainnametld> RT-AC68U-DAE8`

It is in their /etc/hosts file and saved beyond modification using SquashFS.

I mean, you could modify it through the web GUI but only the `<yourhostname>` 
and the `<yourdomainnametld>` portion but you won't easily get to the
ASUS-related fully-qualified domain names in the `/etc/hosts` file.
