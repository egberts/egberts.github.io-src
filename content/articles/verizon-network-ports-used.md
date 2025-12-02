title: Ports used in Verizon Network
date: 2018-01-18 13:15
modified: 2025-07-13T0341
status: published
tags: Verizon, ISP, ports
category: research
summary: Ports used in Verizon Network


I've got a Verizon residential cable setup where I placed a personal Linux router directly to the Verizon white box via Ethernet 10Base-1000 and CAT-5 cable.  And I need to relocate this Actiontec media gateway router somewhere within my new home subnet and no longer in front of my personal router.

Why would I do such a convoluted setup like this?  Because, I like full control of my home network which is full of 802.1X devices, Bro IDS and various other pet projects related to network security.

In order to do this, a complete remapping out the Verizon home network topology is necessary, complete with TCP/UDP, IP and Ethernet layer.

I attached a 10-BaseT Ethernet --> HUB <-- so that Wireshark can be captured in its entirety and unchanged from default Verizon setup.
In order to cut out the marketspeak to mere labels for this article, I use the following terms:

* cable router - Actiontec broadband gateway router, provided by Verizon
* personal router - Your beefy brand-new Linux gateway box


I used IP subnets used throughout the home (listed in ingress to egress order):

```
    192.168.1.100 - Verizon Settop box, first
    192.168.1.0/24 - Cable subnet, not changeable by cable router
    192.168.1.1 - gateway for cable subnet; provided by cable router
    192.168.6.233 - egress IP of cable router; IP provided by your personal gateway router
    192.168.6.0/24 - Declared by personal router for home-wide uses.
```

When a broadband router boots up, it access the following ports to communicate with various Verizon infrastructure servers:

DHCP Client - Verizon HFC network
===
First, the cable router issues a DHCP request to Verizon FiOS DHCP server using the following IP ports:

```
    Port 67/UDP - egress
    Port 68/UDP - ingress
```

Then the DHCP-REQUEST options sent by your cable router looks like:

```wireshark
User Datagram Protocol, Src Port: 68, Dst Port: 67
Bootstrap Protocol (Request)
    Message type: Boot Request (1)
    Hardware type: Ethernet (0x01)
    Bootp flags: 0x0000 (Unicast)
        0... .... .... .... = Broadcast flag: Unicast
        .000 0000 0000 0000 = Reserved flags: 0x0000
    Client IP address: 172.32.1.132
    Your (client) IP address: 0.0.0.0
    Next server IP address: 0.0.0.0
    Relay agent IP address: 0.0.0.0
    Client MAC address: -f8:e4:XX:XX:XX:XX
    Client hardware address padding: 00000000000000000000
    Server host name not given
    Boot file name not given
    Magic cookie: DHCP
    Option: (53) DHCP Message Type (Request)
        Length: 1
        DHCP: Request (3)
    Option: (60) Vendor class identifier
        Length: 25
        Vendor class identifier: Wireless Broadband Router
    Option: (12) Host Name
        Length: 25
        Host Name: Wireless_Broadband_Router
    Option: (15) Domain Name
        Length: 4
        Domain Name: home
    Option: (55) Parameter Request List
        Length: 18
        Parameter Request List Item: (1) Subnet Mask
        Parameter Request List Item: (28) Broadcast Address
        Parameter Request List Item: (2) Time Offset
        Parameter Request List Item: (3) Router
        Parameter Request List Item: (15) Domain Name
        Parameter Request List Item: (6) Domain Name Server
        Parameter Request List Item: (4) Time Server
        Parameter Request List Item: (7) Log Server
        Parameter Request List Item: (23) Default IP Time-to-Live
        Parameter Request List Item: (26) Interface MTU
        Parameter Request List Item: (43) Vendor-Specific Informatio
        Parameter Request List Item: (50) Requested IP Address
        Parameter Request List Item: (51) IP Address Lease Time
        Parameter Request List Item: (54) DHCP Server Identifier
        Parameter Request List Item: (55) Parameter Request List
        Parameter Request List Item: (60) Vendor class identifier
        Parameter Request List Item: (61) Client identifier
        Parameter Request List Item: (72) Default WWW Server
    Option: (255) End
        Option End: 255
```

To deal with that Juniper DHCP server request, my copy of ISC DHCP client configuration for personal router is (also given at [GitHub](https://github.com/egberts/systemd-dhclient/etc/dhcp/dhclient.conf)).

If your personal gateway router is going to be directly attached to the ONT (Optical Network Terminator, a white box) like I hooked mine up, then that gateway's ingress DHCP server is required to serve additional DHCP specialized options toward the cable router's dhclient.

```nginx
# Configuration file for /sbin/dhclient.
#
# Customized for Verizon FiOS Juniper DHCP server
#
# This is a sample configuration file for dhclient. See dhclient.conf's
# man page for more information about the syntax of this file
# and a more comprehensive list of the parameters understood by
# dhclient.
#
# Normally, if the DHCP server provides reasonable information and does
# not leave anything out (like the domain name, for example), then
# few changes must be made to this file, if any.
#

send host-name = "Wireless_Broadband_Router";
send domain-name "home";
request subnet-mask, broadcast-address, time-offset, routers,
 domain-name, domain-name-servers, time-servers, log-servers,
        default-ip-ttl, dhcp-requested-address, dhcp-lease-time,
        dhcp-server-identifier,dhcp-parameter-request-list,
        vendor-class-identifier,dhcp-client-identifier,
        www-server,
 dhcp6.name-servers, dhcp6.domain-search, dhcp6.fqdn, dhcp6.sntp-servers,
 interface-mtu,
 ntp-servers;

timeout 60;
retry 60;
reboot 10;
```


Verizon uses Juniper routers and their DHCP server is ... quirky.

```wireshark
Internet Protocol Version 4, Src: 192.168.6.1, Dst: 255.255.255.255
User Datagram Protocol, Src Port: 67, Dst Port: 68
Bootstrap Protocol (NAK)
    Message type: Boot Reply (2)
    Hardware type: Ethernet (0x01)
    Bootp flags: 0x8000, Broadcast flag (Broadcast)
        1... .... .... .... = Broadcast flag: Broadcast
        .000 0000 0000 0000 = Reserved flags: 0x0000
    Client IP address: 0.0.0.0
    Your (client) IP address: 0.0.0.0
    Next server IP address: 0.0.0.0
    Relay agent IP address: 0.0.0.0
    Client MAC address: -f8:e4:XX:XX:XX:XX
    Client hardware address padding: 00000000000000000000
    Server host name not given
    Boot file name not given
    Magic cookie: DHCP
    Option: (53) DHCP Message Type (NAK)
        Length: 1
        DHCP: NAK (6)
    Option: (54) DHCP Server Identifier
        Length: 4
        DHCP Server Identifier: 192.168.6.1
    Option: (56) Message
        Length: 30
        Message: requested address is incorrect
    Option: (255) End
        Option End: 255
    Padding: 000000000000000000000000000000000000
```

DHCP Server - Home Network
--------------------------

For the home network, my DHCP server has the following options.

```nginx
# shared-network
#   subnet
#      group
#      pool

shared-network "dmz2" {

  # deny bootp;
  deny duplicates;
  # deny booting;

  subnet 192.168.6.0 netmask 255.255.255.0
  {
    # SERVER CONTROL
    # authoritative - Tells the DHCP server that it is to act as the one
    # true DHCP server for the scopes it's configured to understand, by
    # sending out DHCPNAK (DHCP-no-acknowledge) packets to
    # misconfigured DHCP clients.

    server-identifier 192.168.6.1;
    server-name dhcp-server-192-168;

    # CLIENT CONTROL

    # 'allow unknown-clients' - Tells the DHCP server to assign
    # addresses to clients without static host declarations,
    # which is almost certainly something you want to do.
    #
    # Otherwise, only clients you've manually given addresses to
    # later in the file will get DHCP assignments.
    deny unknown-clients;
    ignore client-updates;

    # do not use option domain-search in DMZ
    # do not use option domain-name in DMZ

    # NETWORK COMPONENTS

    option log-servers 192.168.6.1;
    option subnet-mask 255.255.255.0;
    option routers 192.168.6.1;
    option ntp-servers 192.168.6.1;
    option www-server 192.168.6.1;

    option domain-name "verizon.net";

    # domain-name-servers may be a standalone DHCP config file
    # that gets updated by resolvd daemon and loaded by DHCPD
    # via 'include' statement.
          #
    # Here, it's copied manually from personal gateway's /etc/resolv.conf

    option domain-name-servers XXX.XXX.XXX.XXX, XXX.XXX.XXX.XXX;

    # log-facility local7;
    option broadcast-address 192.168.6.255;

    # on release { }

    # on expiry { }
    on commit {
            set clip = binary-to-ascii(10, 8, ".", leased-address);
            set clhw = binary-to-ascii(16, 8, ":", substring(hardware, 1, 6));
            execute("/usr/local/sbin/dhcpevent", "commit", clip, clhw, host-decl-name);
        }
  }
}
```


Of course, I include the following line in the main DHCP server configuration file, usually `/etc/dhcp/dhcpd.conf`.

```cfg
    include "/etc/dhcp/dhcpd.conf.192.168.6.dmz"
```

The objective of the above DHCP configuration sub-settings is to emulate the following egress packet from your new DHCP server or your home devices are NOT going to get an IP address.


Ports Used
----------


Then the following Verizon infrastructure servers are consulted next:

```
    53/udp DNS (nsphil01.verizon.net, 71.242.0.12)
    53/udp DNS (nsrest01.verizon.net, ns5.verizon.net, 71.252.0.12)
    443/tcp HTTPS (cpe-ems2333.verizon.com, 206.46.32.32) Edgecast Server
    443/tcp HTTPS (cpe-ems2214.verizon.com, 206.46.32.28) Edgecast Server
    80/tcp HTTP (www.verizon.com, mercuryipg.FALDMDFLD00.fiostv.verizon.net, 71.246.255.44) main web site
    443/tcp HTTPS (cpe-ems2214.verizon.com, 206.46.32.28) Edgecast Server
    80/tcp HTTP (71.245.255.44)
    80/tcp HTTP (www.verizon.com, 71.242.0.12)
```

Note: Verizon uses CMTS's own time servers via DOCSIS protocol (which is not an NTP protocol) to keep their customer premise equipment's real clock in sync.
