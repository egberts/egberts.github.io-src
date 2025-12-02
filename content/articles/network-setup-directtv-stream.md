title: Setting up your own gateway for DirectTV-stream
date: 2022-07-15 07:26
modified: 2025-07-13 02:08
status: published
tags: DirectTV, gateway
category: howto
slug: network-setup-directtv-stream
lang: en
private: False
summary: How to setup gateway for DirectTV access


DirecTV, a network-based entertainment television service, is available in the residence halls and in many other locations on campus. Before placing an order for service, departments on campus should review the following network requirements with the local Network Administrator:

* Existing infrastructure and equipment will determine if you can have High Definition service.
* Both Standard and High Definition services require a full-duplex communication and will not work with hubs.
* Determine if this will be on a dedicated or non-dedicated data port.

# Standard Definition vs. High Definition Service

## Standard Definition Service

* Standard definition (SD) service runs at less than 10Mb/s (variable bit rate between 2Mb/s and 8Mb/s).
* SD service can be supported just about any place there is a wired CIT network service.

## High Definition Service

* High definition (HD) service runs at higher speeds (up to 30+Mb/s).
* A wired network with a speed of 100Mb/s or better is required.

# Dedicated Data Port

VLANs/subnets set up to specifically support DirecTV Set-Top Boxes can be used.


## Non-dedicated Data Port

DHCP is required. 

Set-top boxes have no mechanism for manually setting IP addresses. 

ISC DHCP is recommended for your interior DHCP server because there are specific DHCP option requirements. 

If you choose to use your own DHCP service, vendor-encapsulated-options (option 43) must be set to return hex string “3c:04:6d:66:68:33” (without quotes).

Sample configuration using Internet Systems Consortium’s (ISC) DHCP server:

```nginx
class "DirecTV_MFH3" {
    match if option vendor-class-identifier = "mfh3";
    option vendor-encapsulated-options = 3c:04:6d:66:68:33;
    }
```

ACLs and Firewalls need to allow IP access (both TCP and UDP, unicast and multicast) between the set-top box and the DirecTV servers on the same internal subnets, including any running an internal video server.

Using `ipfilter`, the simplest and recommended examples are:

```console
allow IP traffic to and from subnet 10.10.14.7/26
allow IP traffic to and from subnet 10.16.196.0/24
```

Example ACL settings using `ipfilter` are:

```
permit ip 10.10.14.7 0.0.0.7 any
permit ip 10.16.196.0/24 239.255.0.0. 0.0.255.255
```

Note: Above examples are outbound from the router/firewall to the subnet (inbound to the subnet).

# Port Openings

Port filters are not recommended because DirecTV may change ports without warning. 

For default-deny firewall scenarios, the following ports are in use:

```
UDP src port 1024 (video streams)
UDP src port 1758 (multicast TFTP)
UDP src port 4999 (multicast TFTP)
UDP src port 9875 (SAP/SDP)
TCP dst port 554 (RTSP)
```

## Sample IOS ACL:
The text below shows FIVE commands, each beginning with the word "permit."

```command
permit udp 10.10.14.7 0.0.0.63 239.255.0.0 0.0.255.255 eq 1024
permit udp 10.10.14.7 0.0.0.63 239.255.0.0 0.0.255.255 eq 1758
permit udp 10.10.14.7 0.0.0.63 239.255.0.0 0.0.255.255 eq 9875
permit udp 10.10.14.7 0.0.0.63 239.255.0.0 0.0.255.255 eq 4999
permit tcp 10.10.14.7 0.0.0.63 eq 554 any

Note: Above examples are outbound from the router/firewall to the subnet (inbound to the subnet).
             
# Routers

Routers, including routing firewalls, need to understand and run multicast routing protocols, specifically Protocol Independent Multicast (PIM) running in pim-sparse mode.

This usually entails enabling `mrouted`.
