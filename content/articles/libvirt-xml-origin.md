title: Origin of Libvirt XML file
date: 2023-02-02 12:02
status: published
tags: XML, libvirt
category: research
summary: Why did Libvirt configuration files use XML?
lang: en
private: False


= The network filter driver =

This driver provides a fully configurable network filtering capability that leverages ebtables, iptables and ip6tables. This was written by the libvirt guys at IBM and although its XML schema is defined by libvirt, the conceptual model is closely aligned with the DMTF CIM schema for network filtering:


    https://www.dmtf.org/sites/default/files/cim/cim_schema_v2230/CIM_Network.pdf


