Title: Bind9 RCodes
Date: 2020-07-01 11:48
status: published
tags: DNS, Bind9
category: research
summary: RCodes for Bind9 network message

RCodes
=================
The “status” portion of the message is derived from the RCODE.  
Some common RCODEs are: 
[jtable]
NOERROR,0,no error condition,Does not imply that there is an answer to the query.
FORMERR,1,format error,The name server did not understand the query. 
SRVFAIL,2,server failure,The server couldn’t process the query due to a variety of reasons, which will be discussed in a later slide. 
NXDOMAIN,3,“name error” according to RFC 1035,The domain in which the query was made does not exist.  Not to be confused with an empty NOERROR response!
NOTIMPL,4,not implemented,The name server basically understands the query, but doesn’t implement the query type or some other aspect of the query. 
REFUSED,5,refused,The server refuses to answer the query, for a variety of reasons.
[/jtable]

Flags
================
What are these flags?  Initial RFC 1035 definitions: 
[jtable]
qr, Query Response (response to query)
aa, Authoritative Answer
tc, TrunCated (answer is truncated and you need to fall over to TCP)
rd, Recursion Desired: In a query, this specifies that the querier wants the server to perform recursion.  Its value is copied into the response from the server. 
ra,Recursion Available: The server is willing to do recursion for this client.  Of course, not all servers perform recursion, and those that do, often do not do so for every client.  It is generally a best practice to restrict recursion to known clients.
[/jtable]

The presence of the RD and the absence of the RA flag prompts dig to issue a more visible warning: “recursion requested but not available.
