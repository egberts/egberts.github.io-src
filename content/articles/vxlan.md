title: VXLAN Setup
date: 2025-11-29 14:41
status: published
tags: VXLAN, network
category: HOWTO
summary: How to setup a VXLAN
lang: en
private: False

This article is on about configuring a host-based VXLAN for use with multiple virtual machines ... on Linux.

VXLAN describes Virtual eXtensible Local Area Network, which is used to
address the need for overlay networks within virtualized data centers
accommodating multiple tenants.  Defined in [IETF RFC7348](https://datatracker.ietf.org/doc/html/rfc7348)

To skip overview, go straight to Setup section.

Overview
====

VXLAN takes VM's packets in Ethernet II/802.3 format and sends it over UDP/IP over Internet to remote host with corresponding VXLAN support.

 Virtual Machine
     |
     v
   vnetX
     |
     v
   br-vx
     |
     v
   vlan100
     |
    br0
     |
   wlan0

This VXLAN has considerable overhead as opposed to its smaller cousin, VLAN.  VLAN simply uses 0x8100 for its Ethernet type.  Whereas the VXLAN uses 0x0800 (for IPv4) or 0x86dd (IPv6) then have its own VXLAN header before encapsulating the inner-network's Ethernet payload in its entirety as-is (after stripping off the Ethernet FCS checksum).

Smaller Cousin: VLAN
----
For comparison purpose, the VLAN Header is:

    +----------------------+----------------------+
    | Destination MAC (6B) |   Source MAC (6B)    |
    +----------------------+----------------------+

    +-----------------------------------------------+
    |  802.1Q VLAN Tag:                             |
    +-----------------------------------------------+
    |  TPID (2B) = 0x8100 (indicates VLAN tag)      |
    +-----------------------------------------------+
    |  TCI (2B): Tag Control Information            |
    |   • PCP: Priority Code Point (3 bits)         |
    |   • DEI: Drop Eligible Indicator (1 bit)      |
    |   • VID: VLAN Identifier (12 bits)            |
    +-----------------------------------------------+

    +-------------------------------+
    | Inner-network payload         |
    +-------------------------------+
    |   Ethertype (2B) (L3 Type)    |
    +-------------------------------+
    |   Payload (46–1500 bytes)     |
    +-------------------------------+

    +-------------------------------+
    |     Frame Check Sequence (4B) |
    +-------------------------------+

Notice only 12-bits for the VLAN identifier (VID) or maximum 4095 (technically 4093, 2 are reserved)?

Hiccups during Expansion of Virtual LAN
----
There is attempts to extend VLAN IDs, several in fact, but none of them solved the real scaling and multi-tenant problems that modern datacenters face now

So, the evolution of VLAN are:

     Bridge Relay Element (ascom Timeplex)
        │
        ▼
     VLAN (802.1Q) ──┐
                     │
                     ▼
                 VXLAN ──────────┐
                     │           │
                     ▼           ▼
                   EVPN        Geneve
                     │           │
                     ▼           ▼
                   NSX           NSX-T
                     │
                     ▼
                   OVN

     GRE ────────────┐
                     │
                    NVGRE
                     │
                     ▼
                   Geneve

    STT ────────────┘ (parallel high-performance overlay)

    GUE ────────────┘ (independent Linux/cloud-native overlay)


VXLAN and other “overlay” virtual LAN technologies ([NVGRE](https://www.rfc-editor.org/rfc/rfc7637.html), [STT](), [Geneve](https://www.rfc-editor.org/rfc/rfc8926.html)) emerged because simply expanding the VLAN ID field was fundamentally insufficient but all failed to deal with multi-tenants found in today's datacenter.

Below is the clear, technical explanation:

VLANs were designed for Layer-2, not multi-tenant cloud networks
----

VLANs (802.1Q) were meant to segment a single enterprise LAN.
Cloud datacenters needed to isolate tens of thousands to millions of tenants, with:

- overlapping IP spaces

- dynamic provisioning

- virtual machine mobility

- multi-tenant routing and security

Even if the VLAN ID were expanded from 12 bits:

- VLANs fundamentally lack tenant isolation at Layer-3
- VXLAN overlays provide network virtualization, not just segmentation.

Expanding the VLAN ID would require changing every switch ASIC
----

To expand VLAN IDs:

- All Ethernet silicon (merchant silicon and custom ASICs)

- Link protocols

- Frame parsers

- Spanning-tree logic

- 802.1ad, QinQ, Q-in-Q-in-Q stack handling

... would need to be redesigned and replaced globally.

VXLAN avoids this completely.

-  VXLAN uses existing IP & UDP hardware, so existing switches/NICs continued functioning.

VLANs cannot span L3 networks — VXLAN can
---

Classic VLANs are strictly Layer-2 broadcast domains.

Datacenters needed L2 adjacency across L3 boundaries (for VM mobility, vMotion, etc.).

Options:

- Extend L2 everywhere → unstable, loops, huge broadcast domains

- Use overlay tunnels → preserve L2 while using scalable L3 fabric

VXLAN gave:

- L2 service

- over a scalable L3 leaf/spine network

- with ECMP hashing for load balancing

Expanding VLAN IDs would not fix this.

VLAN scaling problems: broadcast, STP, MAC table size
----

L2 networks do not scale:

- STP convergence issues

- Broadcast storms

- MAC learning explosion

- Limited ECMP

- Convergence amplification across 100k+ servers

VXLAN solves this with:

- L3 underlay

- ECMP

- No STP

- EVPN control-plane (no flooding)

Expanding VLAN ID bits does not solve the broadcast/control-plane problems inherent to L2.

Datacenters needed 16M+ segments (VNIs), not 4096 or 65k
----

Even if VLAN IDs were expanded:

-  Scheme 	Max segments
-  Classic VLAN (12 bits) 	4096
-  Hypothetical 16-bit VLAN 	65,536
-  VXLAN (24-bit VNI) 	16,777,216

Large multi-tenant clouds (AWS, Azure, Google) can easily require millions of isolated overlays**.

Even 65k is too small.

VXLAN’s 24-bit VNI gave enough room for cloud-scale.

UDP/IP encapsulation works with existing routing fabrics
----

VXLAN chose UDP/IP encapsulation because:

-  Works over any IP network

-  Uses ECMP load-balancing (UDP src-port hashing)

-  Allows hardware offloads (NICs, switches) easily

-  No need for Ethernet to carry giant tables

-  Expanding VLAN IDs would not bring:

  - ECMP across spine switches
  - IP routing scalability
  - Multi-path transport
  - Hardware offload compatibility

VXLAN gained all of this for free by riding on IP and UDP.

The industry already standardized on 802.1Q; changing it is hard
---

Protocols that completely replace an 802.1 standard rarely succeed.
But adding a new protocol over IP is easy:

VXLAN could be adopted:

- incrementally

- as software (hypervisors, VNFs)

- without needing to replace switches

This accelerated real-world deployment.

Final Summary: Why VLAN expansion didn't happen
====

Because expanding VLAN IDs does NOT solve the real scalability and architecture problems of modern datacenters. VXLAN solved all the problems that VLAN expansion can’t:

VXLAN advantages:

-  Works over L3 (ECMP, scalable fabrics)

- 16 million segments

- Tenant isolation at true virtualization scale

- Hardware-friendly and software-friendly

- Requires no changes to Ethernet framing or ASICs

- Removes reliance on spanning tree

Hence datacenters moved to L3 underlay + L2 overlay, and VXLAN became the standard.


So instead of extending VLAN header, the new packet layout of virtual LAN entails the wrapping of
each Ethernet payload with a UDP/IP in which to connect with other gateways/hosts' internal VLAN network.

VXLAN ID is 24-bits, providing up to 16,77,215 (minus 2 that are reserved).

But save the Geneva protocol for future topics as this is also an emerging technology that is posed to overtake VXLAN, simply because one can add any information to each packet such as which firewall policy got used, which BGP route was taken, which committed service level used, which country it came from;  VXLAN is not extensible for any of those, but VXLAN remains an incredible useful expansion protocol for each multi-tenant to enjoy their own Internet space without restriction.

Setup
====

There are three stages to setting up a VXLAN, using 3 different network configuration tools:

1. Create a network bridge with VXLAN attached
2. Create a virtual network attached to the existing bridge
3. Configure the VM to use the VXLAN network via the virtual network attached to the network bridge


NetworkManager
====

Creating a network bridge
----
1. Using `nmcli`, we execute:

    sudo nmcli connection add type bridge con-name br0 \
            ifname br0 \
            ipv4.method disabled \
            ipv6.method disabled

Prevents assigning an IPv4/IPv6 address to the `br0` interface.

2. Create a VXLAN network interface attached to the existing bridge

    $ sudo nmcli connection add type vxlan slave-type bridge con-name vxlan1-br0 \
            ifname vxlan1 id 1 local 192.10.3.1 \
            remote 10.5.0.2 master br0
    Connection 'vxlan1-br0' (bdbe27f1-5cfe-41df-a811-462e89eba6e9) successfully added.
    $


1: Specifies the interface name for the VXLAN connection. This is the name that will be assigned to the VXLAN interface.

2: Specifies a unique numeric VXLAN identifier to differentiate between different VXLAN networks.

3: Specifies the local IP address to be used for the VXLAN interface. This is the IP address that NetworkManager will use for the local VXLAN endpoint. This address must be reachable by the VMs that will be using the VXLAN network.

4: Specifies the remote IP address of the VXLAN endpoint with which the local VXLAN interface will communicate. This address must be reachable by the VM Host Server that hosts the VMs that will be using the VXLAN network.

5: Specifies the name of the bridge device to which the VXLAN interface will be attached. This is typically the bridge device that acts as the VXLAN endpoint. 



3. Activate the bridge `br0` connection profile:

    sudo nmcli connection up br0

4. If firewalld is active, open port 8472 to allow `nmcli` incoming UDP connections.

    firewall-cmd --permanent --add-port=8472/udp && firewall-cmd --reload

Verification
-----

Display the forwarding table:

    sudo bridge fdb show dev vxlan10
    2a:53:bd:d5:b3:0a master br0 permanent
    00:00:00:00:00:00 dst 203.0.113.1 self permanent


Creating a virtual network
----
Requirements

You installed libvirt virtualization tools and the libvirtd service is enabled and started.

You configured the network bridge br0 with the VXLAN attached on SLES. 

Create a temporary XML file (/tmp/vxlan1-br0.xml) that defines a new virtual network. The file should be similar to the following one:

    <network>
    <name>vxlan1-br0</name>
    <forward mode="bridge" />
    <bridge name="br0" />
    </network>

Use the XML file to create a new libvirt-based virtual network.

    sudo virsh net-define /tmp/vxlan1-br0.xml

(Optional) Remove the XML definition file from disk. It is no longer needed.

    rm /tmp/vxlan1-br0.xml

Alternatively, you can go to `virt-manager`, Edit -> Connection Details -> Virtual Networks tab, then '+' icon to add a network, then click on `XML` tab, then paste the content of `/tmp/vxlan1-br0.xml` file.  Once saved, it automatically becomes active.

Start the new vxlan1-br0 virtual network and configure it to start automatically when the libvirtd service starts.

    sudo virsh net-start vxlan1-br0

    sudo virsh net-autostart vxlan1-br0

Verify the status of the newly created network. If the newly created virtual network is listed as active, the configuration was successful.

    sudo virsh net-list
    Name              State    Autostart   Persistent
    ----------------------------------------------------
    vxlan1-br0        active   yes         yes

Configurint virtual machines
----
You need to configure virtual machines to use the virtual network vxlan1-br0 to communicate via a network bridge with an attached VXLAN network.
TipTip: Configuring new VMs to use VXLAN

To attach a new VM to a VXLAN network, configure it to use the vxlan1-br0 network when creating the VM. If you use the virt-install tool to create VMs, for example, pass the --network network:vxlan1-br0 option to it.

The following procedure describes how to adjust an existing VM. Our example virtual machine VM1 is running on host SLES-HOST-A.

Requirements:


1. You created a VM using libvirt.

2. You configured the virtual network vxlan1-br0 using libvirt. 

3. Connect the network interface of the VM to the virtual network vxlan1-br0.

    sudo virt-xml VM1 --edit --network network=vxlan1-br0

Restart the VM, for example:

    sudo virsh shutdown VM1
    sudo virsh start VM1

Verify the virtual network interfaces on the host.

    sudo virsh domiflist VM1
    Interface   Type     Source           Model    MAC
    -------------------------------------------------------------------
    vnet1
    
        bridge   vxlan1-br0
    
        virtio   52:54:12:a7:89:1f

1: A virtual network automatically created by libvirt. It is used by the virtual machine VM1.

2: A network bridge with the attached VXLAN network. The vnet1 network is connected to that bridge.

Verify the interface attached to the vxlan1-br0 network bridge on the host.

    sudo ip link show master vxlan1-br0
    14: vxlan1:
     <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br0 state UNKNOWN mode DEFAULT group default qlen 1000
        link/ether 2a:53:bd:d5:b3:0a brd ff:ff:ff:ff:ff:ff
    15: vnet1:
     <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br0 state UNKNOWN mode DEFAULT group default qlen 1000
        link/ether 52:54:12:a7:89:1f brd ff:ff:ff:ff:ff:ff

1: The configured VXLAN network attached to the vxlan1-br0 bridge.

2: A virtual network automatically created by libvirt. It is used by the virtual machine VM1. 

