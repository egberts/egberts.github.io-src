Title: ISC DHCP and Weird Hostnames
Tags: DHCP, security, dhcpd
Date: 2019-01-05 08:30
Modified: 2022-02-24 13:55
Category: research
Summary: ISC DHCP handling of weird hostnames found in Nintendo 3DS and iPods.
Status: published

Believe it or not, I dusted off my Ninetendo 3DS and very old Apple iPods and tried to join my home network, and it failed.

When it came time to configure it and attach it to my ISC DHCP server, the
server rejected the devices' DHCP-REQUEST message.

A closer look showed that the hostname was funky for various reasons:

1. Nintendo 3DS had a space in the middle of its requested hostname in its DHCP-REQUEST: as in "Nintendo 3DS".

2. Apple iPod couldn't request due to no hostname.

3. Google Samsung Android phone couldn't request because of no hostname.

DHCP for Nintendo 3DS
---------------------

Temporary fixed only for Nintendo 3DS is to include the following into
`dhcpd.conf.options` (or `dhcpd.conf` for those flat-file folks):

```dhcp
if (option host-name ~= "Nintendo 3DS") {
   ddns-hostname = concat ("Nintendo3DS", binary-to-ascii (16, 8, "x", substring (hardware, 1, 6)));
   log(concat("Changing hostname1: ", option host-name, " into ", ddns-hostname));
}

if (option host-name ~= "(Nintendo 3DS)") {
   ddns-hostname = concat ("Nintendo3DS", binary-to-ascii (16, 8, "x", substring (hardware, 1, 6)));
   log(concat("Changing hostname2: ", option host-name, " into ", ddns-hostname));
}
```

DHCP for Apple iPod
-------------------
For Apple iPod, a specific MAC address subclass is needed here.  Added the
following to `dhcpd.conf.options`:

```nginx
class "iPod" {
        # match hardware;
        match pick-first-value (option dhcp-client-identifier, hardware);
}
```

And added the following to `dhcpd.conf.reserved` (or `dhcpd.conf`):

```nginx
subclass "iPod" 1:00:23:df:ee:62:53;  # Apple iPod

group blue {
    # Apple iPod
    host ipod1.home. {
        hardware ethernet 00:23:df:ee:62:53;
        fixed-address 192.168.1.153;
    }
...
}
```

DHCP for Google Samsung Android Phone
-------------------------------------
That was annoying.  No way to change hostname on this phone.  Must be a very
old model.

The workaround to this kind of phone is to following the "DHCP for Apple iPod"
section above.
