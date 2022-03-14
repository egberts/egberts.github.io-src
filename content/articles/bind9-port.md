Title: Bind9 Network Ports
Date: 2011-07-11 06:31
Modified: 2020-02-20 19:03
Tags: network, port, bind9
Category: research
summary: Network port numbers used by ISC Bind9. -  Network port numbers used by [Bind9](Bind9 "wikilink").

Network port number used by Bind9
---------------------------------
[jtable separator = ","]
Port number,Protocol,Description
53 , tcp/udp , General DNS data communication
80 , tcp/udp , HTTP statistics
953 , udp , Remote control channel for Bind9 `named` process. Port used by <code>rndc</code> and <code>nsupdate</code> utility.
`not specified` , udp , TSIG-based zone transfer channel between the hidden-master and the public-authoritative name server.
[/jtable]

