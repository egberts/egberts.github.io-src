title: Netfilter Priority Levels
date: 2020-10-13 20:31
modified: 2022-09-09-09:26
status: published
tags: netfilter, nftables
category: research
summary: Details on Prioritization of Netfilter Hooks
slog: netfilter-priority-levels
lang: en
private: False


Nftables has documented how the priority number should be used [here](https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes#Chains).

I summarized and expand these priorities below:
[jtable caption="Priority Level of Netfilter Hooks]
Priority Level , Mnemonic , Symbol , Description
-810 , `stp`, , Bridge Spanning Tree Protocol (libvirt)
-800 , `mac`, , MAC-level filtering (libvirt); MAC is designated for the MAC address of the network interface. A filtering rule that references this variable will automatically be replaced with the MAC address of the interface. This works without the user having to explicitly provide the MAC parameter. Even though it is possible to specify the MAC parameter similar to the IP parameter above; it is discouraged since libvirt knows what MAC address an interface will be using. 
-750 , `vlan`, , Virtual LAN (VLAN) filtering (libvirt)
-700 , `ipv4`, , IPv4 filtering (libvirt); The parameter IP represents the IP address that the operating system inside the virtual machine is expected to use on the given interface. The IP parameter is special in so far as the libvirt daemon will try to determine the IP address (and thus the IP parameter's value) that is being used on an interface if the parameter is not explicitly provided but referenced. For current limitations on IP address detection; consult the section on limitations [Section 17.14.12](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-Virtual_Networking-Applying_network_filtering#sect-Applying_network_filtering-Limitations); “Limitations” on how to use this feature and what to expect when using it. 
-600 , `ipv6`, , IPv6 filtering (libvirt)
-500 , `arp`, , ARP filtering (libvirt)
-400 , `rarp`, , Reverse ARP (RARP) filtering (libvirt)
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

Priority levels as denoted by `libvirt` are also used intensively by RedHat.

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


# References

* [libvirt: Network Filters](https://libvirt.org/formatnwfilter.html)
* [Applying Network Filtering Red Hat Enterprise Linux 7](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-virtual_networking-applying_network_filtering)
