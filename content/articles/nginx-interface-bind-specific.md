title: How NGINX binds to a specific netdev interface
date: 2021-11-15 10:00
status: published
tags: NGINX
category: HOWTO
summary: NGINX binds to a specific netdev interface.
lang: en
private: False


Is there a way to make Nginx 1.11 bind to a specific interface regardless of the IP address?  Let us find out.

I've got a home gateway to an ISP provider; it uses DHCP client to obtain its dynamic IP address. I do not know what that IP address is at NGINX configuration time.

Surely, there must be a way to make such a fine HTTP server bind to a specific network interface? I know that Apache can.

The other interfaces are related to enterprise network (which has its own web server), test network (which has none), and a virtual network for the virtual host farm (which runs Apache). Hence, the need to bind this Nginx specifically to the external interface

The Answer
==========
Edit your startup sequence to run a command or script that captures the interface's IP address and writes it to a file in the format `listen <ip>:80` or whatever port you want:

    echo "listen $(ip -o -4 a s eth0 | awk '{ print $4 }' | cut -d/ -f1):80;" > /path/to/some/file

Then just have your Nginx config include that file:

    include /path/to/some/file;

Obviously, you'll need to make sure the IP capture occurs before the Nginx startup does.
