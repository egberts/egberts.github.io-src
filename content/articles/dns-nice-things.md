title: Chain DNSthingy
date: 2020-10-13 11:00
status: draft
tags: DNS
category: research
lang: en
private: True

The result:

Chain DNSthingy (1 references)
num pkts bytes target prot opt in out source destination
2 645 44407 DNAT udp -- * * 0.0.0.0/0 !192.168.11.1 udp dpt:53 to:192.168.11.1:53
3 2 80 DNAT tcp -- * * 0.0.0.0/0 !192.168.11.1 tcp dpt:53 to:192.168.11.1:53

These types of rules are also referred to as DNS hijacking rules. Hijacking in a good sense, of course, because if you have a reason to distrust a device, you want to at the very least hijack its DNS usage to apply the policy of the router.
Benefits of forcing DNS

    DNS poisoning is mitigated, especially when the attacker has a publicly-available DNS server that is being used by silently changing internal client device DNS settings (like DNSchanger does).
    Convenience for devices with static DNS configured. Sometimes devices have statically assigned themselves a DNS server, now it doesn’t matter what public DNS resolver is statically set on a client device because the hijacking rule forces the router’s DNS to be used.
    Endpoints require no DNS management. Since the forced DNS settings are applied, no customization is required on a per-endpoint basis.

Important note on DNS benchmark tests

Steve Gibson has an awesome freeware Domain Name Speed Benchmark utility we often recommend.

When DNS usage is forced, it makes it impossible to benchmark public DNS resolvers from “behind” one of these gateways. During benchmark tests, you want to disable the hijacking rules temporarily.

To disable these rules on AsusWRT or Linux, which will delete line number 2 and 3 based on the query above:

iptables -D DNSthingy 2
iptables -D DNSthingy 3

After ASUS reboot and/or Linux networking restart, the firewall rules will once again be auto-applied.

To disable these rules on pfSense, simply click on the checkmark to disable it, and apply the changes. After the benchmark tests are run, the rules can be enabled once again.
WARNING: Forcing DNS on port 53 alone won’t force all DNS

As a result of port 53 DNS enforcement on many edge devices, endpoint security software has begun to work around it. For example, Webroot uses port 7777. AVG and several others use port 443. Of course it’s easy to simply block destination port 7777 but when it comes to port 443 that’s not so easy as you would be blocking HTTPS (with TCP) and you’d be blocking QUIC (with UDP). This is where the zero trust model comes in.
