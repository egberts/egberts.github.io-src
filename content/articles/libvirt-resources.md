title: Resource Requirements for `libvirt`
date: 2022-08-08 04:25
modified: 2025-12-31 02:18
status: published
tags: libvirt
category: research
summary: What resources does `libvirt` require?
slug: libvirt-resources.md
lang: en
private: False


Eclectic things that I've found about virtual machine (`libvirt`) library that is used by `virt-manager` (among many others).

# Kernel Configuration
The required settings of Linux kernel configuration (`/usr/src/linux/.config`) for `virt-manager` (on 
the host machine) are:

[jtable]
Kconfig keyword, Value, Description
`CONFIG_FUSE_FS`,  y, Enable FUSE filesystem support required by libvirt tooling |
[/jtable]

# Environment Variables
## Reading Environment Variables
[jtable]
Envvar name,Default value,Description,Source code file
`CODE_FILE`,–,Source filename for debug macros,`util.h`
`CODE_LINE`,–,Source line for debug macros,`util.h`
`CODE_FUNC`,–,Source function for debug macros,`util.h`
`DISPLAY`,unset,X11 display,`vbox_common.c`
`DNSMASQ_CLIENT_ID`,unset,DHCP client identifier,`leaseshelper.c`
`DNSMASQ_IAID`,unset,DHCP IAID,`leaseshelper.c`
`DNSMASQ_SERVER_DUID`,unset,DHCP server DUID,`leasehelper.c`
`DNSMASQ_INTERFACE`,unset,Network interface name,`leaseshelper.c`
`DNSMASQ_LEASE_EXPIRES`,unset,Lease expiration timestamp,`virlease.c`
`DNSMASQ_MAC`,unset,Client MAC address,`leaseshelper.c`
`DNSMASQ_OLD_HOSTNAME`,unset,Previous hostname,`virlease.c`
`DNSMASQ_SUPPLIED_HOSTNAME`,unset,Supplied hostname,`leaseshelper.c`
`EDITOR`,unset,Editor used for configuration editing,–
`EVENT_GLIB_ADD_HANDLE`,unset,GLib add file descriptor,`vireventglib.c`
`EVENT_GLIB_ADD_TIMEOUT`,unset,GLib add timeout,`vireventglib.c`
`EVENT_GLIB_DISPATCH_HANDLE`,unset,GLib dispatch fd,`vireventglib.c`
`EVENT_GLIB_DISPATCH_TIMEOUT`,unset,GLib dispatch timeout,`vireventglib.c`
`EVENT_GLIB_REMOVE_HANDLE`,unset,GLib remove fd,`vireventglib.c`
`EVENT_GLIB_REMOVE_TIMEOUT_IDLE`,unset,GLib remove idle timeout,`vireventglib.c`
`EVENT_GLIB_UPDATE_HANDLE`,unset,GLib update fd,`vireventglib.c`
`LC_ALL`,C,Locale override,`util.c`
`LD_PRELOAD`,unset,Preloaded shared libraries,dynamic linker
`LD_LIBRARY_PATH`,unset,Library search path,dynamic linker
`LIBVIRT_ADMIN_DEFAULT_URI`,unset,Default admin connection URI,`libvirt-admin.c`
`LIBVIRT_AUTH_FILE`,`/etc/libvirt/auth.conf`,Authentication config path,`virauth.c`
`LIBVIRT_AUTOSTART`,unset,Enable autostart,`remote_sockets.c`
`LIBVIRT_DEBUG`,unset,Debug verbosity,`virtlog.c`
`LIBVIRT_DIR_OVERRIDE`,unset,Override libvirt base directory,`virfile.c`
`LIBVIRT_DRIVER_DIR`,unset,Driver module directory,`virfile.c`
`LIBVIRT_GNUTLS_DEBUG`,unset,GnuTLS debug level,`virnettlscontext.c`
`LIBVIRT_LIBSSH_DEBUG`,unset,libssh debug level,`virnetlibsshsession.c`
`LIBVIRT_LOCK_MANAGER_PLUGIN_DIR`,unset,Lock manager plugins,`virtlog.c`
`LIBVIRT_LOG_FILTERS`,unset,Log category filters,`virtlog.c`
`LIBVIRT_LOG_OUTPUT`,unset,Log output destinations,`virtlog.c`
`LIBVIRT_MTAB`,unset,Alternate mtab file,`virfile.c`
`LIBVIRT_SOURCE`,unset,Log source identifier,`virtlog.c`
`LIBVIRT_STORAGE_BACKEND_DIR`,unset,Storage backend directory,`storage_backend.c`
`LIBVIRT_STORAGE_FILE_DIR`,unset,File-based storage backends,`storage_backend.c`
`LIBVIRTD_PATH`,unset,Daemon executable path,–
`LIBVIRTLOCKD_PATH`,unset,Lock daemon runtime path,`lock_driver_lockd.c`
`LIBVIRTLOGD_PATH`,unset,Log daemon runtime path,`log_manager.c`
`LISTEN_FDNAMES`,unset,systemd fd names,`virsystemd.c`
`LISTEN_FDS`,unset,systemd fd count,`virsystemd.c`
`LISTEN_PID`,unset,systemd listener pid,`virsystemd.c`
`LOGNAME`,unset,Login name,libc
`MESSAGE`,unset,Syslog message,libc
`NOTIFY_SOCKET`,unset,systemd notify socket,`virsystemd.c`
`PRIORITY`,unset,Syslog priority,libc
`QEMU_AUDIO_DRV`,unset,QEMU audio backend,`qemu_domain.c`
`SDL_AUDIODRIVER`,unset,SDL audio backend,`qemu_domain.c`
`TERM`,unset,Terminal type,libc
`TMPDIR`,unset,Temporary directory,libc
`USER`,unset,Username,libc
`VIR_BRIDGE_NAME`,unset,Default bridge name,`leaseshelper.c`
`XDG_CONFIG_HOME`,unset,XDG config root,`util.c`
`XDG_DATA_HOME`,unset,XDG data root,`util.c`
`XDG_CACHE_HOME`,unset,XDG cache root,`util.c`
`VIRSH_DEFAULT_CONNECT_URI`,unset,Default virsh URI,`virsh.c`
[/jtable]

## Writing Environment Variables
[jtable]
Envvar name,Description,Source code file
`HOME`,User home directory,`virt-login-shell-helper.c`
`IFS`,Shell field separator,`virt-aa-helper.c`
`LISTEN_FDS`,systemd file descriptors,`virsystemd.c`
`LISTEN_PID`,systemd listener pid,`virsystemd.c`
`LOGNAME`,Login name,`virt-login-shell-helper.c`
`PATH`,Executable search path,`virt-login-shell-helper.c`
`SHELL`,User shell,`virt-login-shell-helper.c`
`TERM`,Terminal type,`virt-login-shell-helper.c`
`USER`,Username,`virt-login-shell-helper.c`
`VBOX_APP_HOME`,VirtualBox application root,`vbox_XPCOMCGlue.c`
[/jtable]

## Files (input)
[jtable caption="This is caption" separator=", " th=0 ai="1"]
Filename,Descriptor,Directory,Source code file
`.cache`,Cache directory,$HOME,`vircommand.c`
`.config`,User configuration,$HOME,`vircommand.c`
`.local/share`,User data,$HOME,`vircommand.c`
`auth.conf`,Authentication config,/etc/libvirt,`virauth.c`
`block`,Block devices,/dev,`virdevmapper.c`
`block`,Block subsystem,/sys,`virfile.c`
`cgroups`,Control groups,/proc/self,`vircgroup.c`
`control`,Device-mapper control,/dev/mapper,`virdevmapper.c`
`cpuinfo`,CPU information,/proc,`virhostcpu.c`
`devices`,Device list,/proc,`virconf.c`
`devices`,Mediated devices,/sys/bus/mdev,`virlog.c`
`hugepages`,Hugepage info,/sys/kernel/mm,`virnuma.c`
`hook`,Hook scripts,/etc/libvirt,`virhook.c`
`initctl`,Init control,"`/run,/dev,/etc`",`virinitctl.c`
`ipv6_route`,IPv6 routing table,/proc/net,`virnetdevip.c`
`journal`,Shared memory logs,/dev/shm,`virtlog.c`
`ksm`,Kernel samepage merging,/sys/kernel/mm,`virhostmem.c`
`kvm`,KVM device,/dev,`virhostcpu.c`
`libvirt`,Main config directory,/etc,`virconf.c`
`locale`,Locale database,/usr/share,`virgdbus.c`
`lldpad.pid`,LLDP daemon pid,/var/run,`virnetdevip.c`
`lldpad.pid`,IPv6 LLDPAD process ID,/var/run,`src/util/virnetdevip.c`
`loop%i`,Loop control,/dev,`virfile.c`
`loopcontrol`,Loop control,/dev,`virfile.c`
`meminfo`,Memory information,/proc,`virfile.c`
`modprobe`,add or remove module from Linux kernel,/usr/sbin,`src/util/virjson.c`
`mount`,Active mount point listing,/proc,`src/util/vircgroup.c`
`numad`,Determine available NUMA node,/usr/bin,`src/util/virnuma.c`
`rmmod`,remove module from Linux kernel,/usr/sbin,`src/util/virjson.c`
`stat`,System statistics,/proc,`src/util/virhostcpu.c`
`system`,System devices information,/sys/devices,`src/util/virhostcpu.c`
`tap%d`,Tap netdev device,/dev,`src/util/virnetdevip.c`
`uptime`,uptime since bootup,/proc,`src/util/virhostmem.c`
`vfio`,subdirectory to virtual file input/output,/dev,`src/util/virlog.c`
`virip.pid`,IPv6 virtualprocess ID,/var/run,`src/util/virnetdevip.c`
[/jtable]

# URI, query parameters
[jtable]
Name,Default value,Description
`authfile` ,  `/etc/libvirt/auth.conf` ,  Authentication file; Second priority lookup for the authentication configuration file.  The file path specified by the `authfile` URI query parameter
`/proc/self/fd`,–,File descriptor passthrough
`filename`,`/etc/libvirt`,Configuration file path
`hostsfile`,–,Hosts file override
`addnhosts`,–,Additional hosts file
`username`,–,Authentication username
[/jtable]

# Settings for `auth.conf`
The content of the `auth.conf` file is in [.INI v1.4](https://cloanto.com/specs/ini/#escapesequences) text format.
[jtable]
Keyword,Description,Default
`VIR_CRED_AUTHNAME`,Authentication name,none
`VIR_CRED_PASSPHRASE`,Passphrase credential,none
`VIR_CRED_NOECHOPROMPT`,Disable echo on prompt,none
[/jtable]


# Command Line Options

[jtable]
Option name,  Description
`--bind-dynamic`, `dnsmasq`-specific
`--concurrent`, firewall
`--ra-param`, `dnsmasq`-specific
[/jtable]

# Firewall

The following firewall chain names have been reserved by the `libvirt`/`libvirtd` library/daemon.

The following firewall chain names have been reserved by the `libvirt`/`libvirtd` library/daemon.

[jtable]
Chain Name,Direction,Description,Source file
`nat`, (dual), NAT (Network Address Translation),`virnetfirewall.c`
`LIBVIRT_INP`,Input, used for processing incoming network packets.,`viriptable.c`
`LIBVIRT_FWI`,Forward to Input, used by `libvirt` for controlling access to virtual machines' network interfaces,`viriptable.c`
`LIBVIRT_FWO`,Forward to Output, used by `libvirt` to control outgoing network packets from virtual machines,`viriptable.c`
`LIBVIRT_FWX`,Forward to Forward, used to control the forwarding of packets between virtual machines or networks,`viriptable.c`
`LIBVIRT_OUT`,Output, used for controlling outgoing network packets from the host system,`viriptable.c`
`LIBVIRT_PRT`,Post-Routing, used to handle network packet modifications after routing decisions have been made,`viriptable.c`
[/jtable]
