title: ASUS Router Ports
date: 2022-02-23 14:31
status: published
tags: ports, ASUS, router
category: research
summary: Ports Used in ASUS Router
lang: en
private: False

Below are the list of ports opened for ASUS routers, specifically the ASUS RT-AC68U
with firmware `3.0.0.4.386_46065` (built inhouse on Jan 17, 2022 20:38:

TCP Ports used in ASUS routers
=========

[jtable]
port , protocol , daemon , web configurable , description
12 , tcp , `iptv` , yes , IpTV
22 , tcp , `dropbear` , yes , SSH server, ID is Dropbear SSH 2018.76+; OpenSSH 7.4+ compatible (some functionality from 6.9)
80 , tcp , `lighttpd` , yes , Web server (unencrypted)
515 , tcp , `lpd` , no , LPC printer queue server; lpd daemon built w/ uCLib and GCC 3.5
1194 , tcp , `openvpn` , yes , OpenVPN
1812 , tcp , `radius` , no , RADIUS
1990 , tcp , `wps_monitor` , no , Universal Plug-N-Play (uPnP); This one got binded to its WAN port.
2021 , tcp , `?` , FTP control port number
3394 , tcp , `u2ec` , no , ASUS USB Printer support daemon
3838 , tcp , `lpd` , no , LPC printer queue server; 
5473 , tcp , `u2ec` , no , ASUS USB Printer support daemon
7788 , tcp , `cfg_server` , no , 
8082 , tcp , `webdav?` , yes , WebDAV access to N.A.S./CIFS file share
8088 , tcp , `httpds` , yes , Administrator Login Panel  (web-based)
8200 , tcp , `dms?` , yes , dms?
8443 , tcp , `httpds` , yes , Misc. Web Server
9100 , tcp , `lpd` , no , LaserJet-specific LPC printer queue server
18017 , tcp , `wanduck` , no , recursive DNS resolver
57530 , tcp , `?` , no , passive FTP port number
[/jtable]

UDP Ports used in ASUS routers
=========

[jtable separator="," th=1]
port,protocol,daemon,web configurable,description
1194,udp,`openvpn`,yes,OpenVPN
1900,udp, `wps_monitor`, Universal Plug-N-Play (uPnP) , ? ,
5353, 36630, udp, `avahi-daemon`, no , The Avahi mDNS/DNS-SD daemon implements Apple's Zeroconf architecture (also known as "Rendezvous" or "Bonjour"). The daemon registers local IP addresses and static services using mDNS/DNS-SD and provides two IPC APIs for local programs to make use of the mDNS record cache the avahi-daemon maintains. 
5474, udp, `u2ec`, ? ,ASUS USB Printer support daemon
7788, udp, `cfg_server`, ? ,
9999, udp, `infosvr`, no , used for device discovery using the "ASUS Wireless Router Device Discovery Utility; if you do a `ps Tw`, you can see that `infosvr` has limited themselves to just the LAN (`br0`) interface.
18018, udp, `wanduck`, no , recursive DNS resolver
37064, udp, `wps_monitor`, ? , 
38032, udp , `nas` , yes , Network Access Storage, Samba4/CIFS-compatible; Port is binded to `localhost`
39925, udp , `syslog` , ? , 
40500, udp, `wps_monitor`, ? , Port is binded to `localhost`
42032, udp, `acsd`, no , [Veritas NetBackup](https://www.veritas.com/support/en_US/doc/23395442-133128031-0/v95639226-133128031); Port is binded to `localhost`
47032, udp , `roamast` , ? , Port is binded to `localhost`
59032, udp , `wlceventd` , no , detects wireless client connecting/disconnecting; Port is binded to `localhost`
61689, udp , `mastiff` , ? , AiCloud (closed-source)
[/jtable]
