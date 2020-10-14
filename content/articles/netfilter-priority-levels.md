title: Netfilter Priority Levels
date: 2020-10-13 20:31
status: published
tags: netfilter, nftables
category: research
summary: Details on Netfilter hook prioritization
lang: en
private: False


Nftables has documented how the priority number should be used [here](https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes#Chains).

I summarized and expand these priorities below:
[jtable caption="Priority Level of Netfilter Hooks]
Priority Level , Mnemonic , Symbol , Description
-400 , , `NF_IP_PRI_CONNTRACK_DEFRAG` , defragmentation
-300 , , `NF_IP_PRI_RAW` , traditional priority of the raw table placed before connection tracking operation
-225 , , `NF_IP_PRI_SELINUX` , SELinux operations
-200 , , `NF_IP_PRI_CONNTRACK` , Connection tracking operations
-150 , `mangle` , `NF_IP_PRI_MANGLE` , mangle operations
-100 , `dstnat` , `NF_IP_PRI_NAT_DST` ,  destination network address translation (NAT)
0 , `filter` , `NF_IP_PRI_FILTER` , filtering operation, the filter table
50 , , `NF_IP_PRI_SECURITY` , Place of security table where secmark can be set, for example.
100 , `srcnat` , `NF_IP_PRI_NAT_SRC` , source network address translation (NAT)
225 , , `NF_IP_PRI_SELINUX_LAST` , SELinux at packet exit
300 , , `NF_IP_PRI_CONNTRACK_HELPER` , connection tracking, at exit
[/jtable]

In nftable perspective, the basic traffic flow of 6 hooks is:

```
                                             Local
                                            process
                                              ^  |      .-----------.
                   .-----------.              |  |      |  Routing  |
                   |           |-----> input /    \---> |  Decision |----> output \
--> prerouting --->|  Routing  |                        .-----------.              \
                   | Decision  |                                                     --> postrouting
                   |           |                                                    /
                   |           |---------------> forward --------------------------- 
                   .-----------.
```
`ingress` is missing from diagram and its firstly done before `prerouting` (it was added  in Linux  4.3).

The ordering of subhooks are:

Ingress

1. raw
2. prerouting 
3. conntack
4. mangle
5. nat,  destination

Forward

1. mangle
2. filter

Input

1. mangle
2. filter

Output

1. raw
2. conntrack
3. mangle
4. net, destination
5. filter

Postrouting

1. mangle
2. nat, source

