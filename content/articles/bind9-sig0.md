Title: Bind9 SIG(0)
Date: 2022-04-16 03:30
Tags: Bind9, DNS
Status: published
Category: research
summary: How to use SIG(0) instead of TSIG.

SIG(0) 


Network port numbers used by [List of DNS record types](List_of_DNS_record_types "wikilink").

Network port number used by Bind9
---------------------------------
[jtable separator = ","]
Port number,Protocol,Description
53 , tcp/udp , General DNS data communication
80 , tcp/udp , HTTP statistics
953 , udp , Remote control channel for Bind9 `named` process. Port used by <code>rndc</code> and <code>nsupdate</code> utility.
`not specified` , udp , TSIG-based zone transfer channel between the hidden-master and the public-authoritative name server.
[/jtable]

# References

* [List of DNS record types - KEY](https://en.wikipedia.org/wiki/List_of_DNS_record_types#cite_ref-5)
* [List of DNS record types - TKEY](https://en.wikipedia.org/wiki/List_of_DNS_record_types#cite_ref-12)
