title: Resource Requirements for `libvirt`
date: 2022-08-08 04:25
status: published
tags: libvirt
category: research
summary: What resources does `libvirt` require?
slug: libvirt-resources.md
lang: en
private: False


Eclectic things that I've found about virtual machine (`libvirt`) library that is used by `virt-manager` (amongst many others).

# Kernel Configuration
The required settings of Linux kernel configuration (`/usr/src/linux/.config`) for `virt-manager` (on 
the host machine) are:

[jtable]
Kconfig keyword ,  Value ,  Description
`CONFIG_FUSE_FS`, `y`, Userland file system
[/jtable]

# Environment Variables
## Reading Environment Variables
[jtable]
Envvar name ,  Default value ,  Description, source code
`CODE_FILE` ,  ,  ,
`CODE_LINE` ,  ,  ,
`CODE_FUNC` ,  ,  ,
`DISPLAY` ,  ,  ,  `vbox_common.c`
`DNSMASQ_CLIENT_ID` ,  ,  ,  `leaseshelper.c`
`DNSMASQ_IAID` ,  ,  ,  `leaseshelper.c`
`DNSMASQ_SERVER_DUID` ,  ,  ,  `leasehelper.c`
`DNSMASQ_INTERFACE` ,  ,  ,  `leaseshelper.c` ,  `leasehelper.c`
`DNSMASQ_LEASE_EXPIRES` ,  ,  Expired leases of DNS Masquerade daemon ,  `virlease.c`
`DNSMASQ_MAC` ,  ,  MAC address of DNS Masquerade daemon ,  `leaseshelper.c`
`DNSMASQ_OLD_HOSTNAME` ,  ,  Old hostname of DNS Masquerade daemon ,  `virlease.c`
`DNSMASQ_SUPPLIED_HOSTNAME` ,  ,  supplied hostname of DNS Masquerade daemon ,  `leaseshelper.c`
`EDITOR` ,  ,  Executable path to the editor
`EVENT_GLIB_ADD_HANDLE` ,  ,  ,  `vireventglib.c`
`EVENT_GLIB_ADD_TIMEOUT` ,  ,  ,  `vireventglib.c`
`EVENT_GLIB_DISPATCH_HANDLE` ,  ,  ,  `vireventglib.c`
`EVENT_GLIB_DISPATCH_TIMEOUT` ,  ,  ,  `vireventglib.c`
`EVENT_GLIB_REMOVE_HANDLE ` ,  ,  ,  `vireventglib.c`
`EVENT_GLIB_REMOVE_HANDLE_IDLE` ,  ,  ,  `vireventglib.c`
`EVENT_GLIB_UPDATE_HANDLE` ,  ,  ,  `vireventglib.c`
`EVENT_GLIB_REMOVE_TIMEOUT` ,  ,  ,  `vireventglib.c`
`EVENT_GLIB_REMOVE_TIMEOUT_IDLE` ,  ,  ,  `vireventglib.c`
`LC_ALL` ,  `C` ,   Locale to be used by `virt-manager`, 
`LD_PRELOAD` ,  `` ,   Alternative library to used instead of default `/var/lib`, 
`LD_LIBRARY_PATH` ,  `` ,   Alternative library to used instead of default `/var/lib`, 
`LIBVIRT_ADMIN_DEFAULT_URI` ,  ,   Default URI for an administrator account ,  `libvirt-admin.c`, 
`LIBVIRT_AUTH_FILE` ,  `/etc/libvirt/auth.conf` ,   First priority lookup for the authentication configuration file ,  `virauth.c`
`LIBVIRT_AUTOSTART` ,  ,   Starts up the `libvirtd` daemon ,  `remote_sockets.c`
`LIBVIRT_DEBUG` ,  ,   debug verbosity ,  `virtlog.c`
`LIBVIRT_DIR_OVERRIDE` ,  ,   Log redirect by directory ,  `virfile.c`
`LIBVIRT_DRIVER_DIR` ,  ,  directory path specification to the libvirt drivers,  `virfile.c`
`LIBVIRT_GNUTLS_DEBUG` ,  ,   Debugging GnuTLS ,  `virnettlscontext.c`
`LIBVIRT_LIBSSH_DEBUG` ,  ,   Debugging OpenSSH ,  `virnetlibsshsession.c`
`LIBVIRT_LOCK_MANAGER_PLUGIN_DIR` ,  the directory path specification where the plugins for lock management are stored at; typically appends `/src` to the given directory path specification; plugins are in `$(libdir)/libvirt/lock-driver/@name.so`,   syslog facility/priority filter  `virtlog.c`
`LIBVIRT_LOG_FILTERS` ,  ,   syslog facility/priority filter ,  `virtlog.c`
`LIBVIRT_LOG_OUTPUT` ,  ,   Log redirect ,  `virtlog.c`
`LIBVIRT_MTAB` ,  ,  mock the `/etc/mtab` file, 
`LIBVIRT_SOURCE` ,  ,   log source, 
`LIBVIRT_STORAGE_BACKEND_DIR` ,  Directory path to files containing the storage backends; typically appends `/src` subdirectory this dirspec,   log source, `storage_backend.c`
`LIBVIRT_STORAGE_FILE_DIR` ,  Directory path to files containing the storage backends; typically appends `/src` subdirectory this dirspec,   log source, `storage_backend.c`
`LIBVIRTD_PATH` , ,  The alternate shell `$PATH` for `libvirtd` daemon to `VIRTD_PATH`,
`LIBVIRTLOCKD_PATH` , ,  The directory path specification to the lock files; typically appends `/src` subdirectory to its directory path specification;, `lock_driver_lockd.c`
`LIBVIRTLOGD_PATH` , ,  Directory path to log files written by virtlogd daemon, `log_manager.c`
`LISTEN_FDNAMES` ,  ,  File names of the listener ,  `virsystemd.c`
`LISTEN_FDS` ,  ,  File ID file of the listener ,  `virsystemd.c`
`LISTEN_PID` ,  ,  process ID file of the listener ,  `virsystemd.c`
`LOGNAME` ,  Name of label to prepend to log output, 
`MESSAGE` ,  ,  log message content, 
`NOTIFY_SOCKET` ,  ,  systemd-related sockets ,  `virsystemd.c`
`PRIORITY` ,  ,  log message priority, 
`QEMU_AUDIO_DRV` ,  ,  Audio driver ,  `qemu_domain.c`
`SDL_AUDIODRIVER` ,  ,  SDL Audio driver ,  `qemu_domain.c`
`SYSLOG_FACILITY` ,  ,  log message facility, 
`TERM` , ,  Terminal type, 
`TMPDIR`,  ,  Name of temporary duty.label to prepend to log output,
`USER`,  ,  Secure the name of the user,
`VIR_BRIDGE_NAME` ,  ,  The bridge name that is dedicated toward for `libvirtd` use-only. ,  `leaseshelper.c`
`XDG_CONFIG_HOME` ,  `/etc/libvirt/auth.conf` ,  Third priority lookup for the authentication configuration file (`XDG_CONFIG_HOME/libvirt/auth.conf`),
`XDG_DATA_HOME` ,  `/etc/libvirt/auth.conf` ,  Path to data home,
`XDG_CACHE_HOME` ,  `/etc/libvirt/auth.conf` ,  Path to cache home,
`VBOX_APP_HOME` , ,  home directory for vbox apps ,  `vbox_XPCOMCGlue.c`
`VIRSH_DEFAULT_CONNECT_URI` , ,  connect URI to the `libvirtd` daemon,
`VIRTD_PATH` , ,  The shell `$PATH` for `libvirtd` daemon,
`VISUAL` ,  ,  Executable path to the visual editor,
[/jtable]

## Writing Environment Variables
[jtable]
Envvar name ,  Description ,  source code
`HOME` ,  ,  `virt-login-shell-helper.c`
`IFS` ,  ,  `virt-aa-helper.c`
`LISTEN_FDS` ,  ,  `virsystemd.c`
`LISTEN_PID` ,  ,  `virsystemd.c`
`LOGNAME` ,  ,  `virt-login-shell-helper.c`
`PATH` ,  ,  `virt-login-shell-helper.c`
`SHELL` ,  ,  `virt-login-shell-helper.c`
`TERM` ,  ,  `virt-login-shell-helper.c`
`USER` ,  ,  `virt-login-shell-helper.c`
`VBOX_APP_HOME` ,  ,  home directory for vbox apps ,  `vbox_XPCOMCGlue.c`
[/jtable]

# Files, Input
[jtable caption="This is caption" separator=", " th=0 ai="1"]
Filename ,  descriptor ,  directory ,  source code
`.cache` ,  Cache ,  `/etc/libvirt` ,  `src/util/vircommand.c`
`.config` ,  Configuration ,  `/etc/libvirt` ,  `src/util/vircommand.c`
`.local/share` ,  User-specific share directory ,  `$HOME/.local/share` ,  `src/util/vircommand.c`
`auth.conf` ,  Authentication ,  `/etc/libvirt` ,  `src/util/virauth.c`
`block` ,  Block control ,  `/dev/block` ,  `virdevmapper.c`
`block` ,  System Block control ,  `/sys` ,  `virfile.c`
`cgroup` ,  CGroups ,  `/proc/self/cgroups` `/proc/99999/cgroups` `/proc/cgroups` ,  `src/util/vircgroup.c`
`control` ,  Mapper control ,  `/dev/mapper` ,  `virdevmapper.c`
`cpuinfo` ,  Host CPU details ,  `/proc` ,  `virhostcpu.c`
`devices` ,  Devices list ,  `/proc` ,  `virconf.c`
`devices` ,  subdirectory of System Devices list ,  `/sys/bus/mdev/` ,  `virlog.c`
`hugepages` ,  subdirectory to system huge pages ,  `/sys/kernel/mm/` ,  `virnuma.c`
`hook` ,  Script hook routines subdirectory ,  `/etc/libvirt` ,  `virhook.c`
`initctl` ,  boot up controller ,  `/run` ,  `virinitctl.c`
`initctl` ,  boot up controller ,  `/dev` ,  `virinitctl.c`
`initctl` ,  boot up controller ,  `/etc` ,  `virinitctl.c`
`ipv6_route` ,  IPv6 route table ,  `/proc/net` ,  `virnetdevip.c`
`journal` ,  Shared Memory journaling ,  `/dev/shm` ,  `src/util/virlog.c`
`ksm` ,  Kernel system memory statistics ,  `/sys/kernel/mm` ,  `src/util/virhostmem.c`
`kvm` ,  Kernel virtual memory statistics ,  `/dev` ,  `src/util/virhostcpu.c`
`libvirt` ,  Default directory ,  `/etc/libvirt` ,  `virconf.c`
`locale` ,  Locale subdirectory ,  `/usr/share` ,  `virgdbus.c`
`lldpad.pid` ,  IPv6 LLDPAD process ID ,  `/var/run` ,  `src/util/virnetdevip.c`
`loop%i` ,  Loop control ,  `/dev` ,  `virfile.c`
`loopcontrol` ,  Loop control ,  `/dev` ,  `virfile.c`
`meminfo` ,  Memory information ,  `/proc` ,  `virfile.c`
`modprobe` ,  add or remove module from Linux kernel ,  `/usr/sbin` ,  `src/util/virjson.c`
`mount` ,  Active mount point listing ,  `/proc` ,  `src/util/vircgroup.c`
`numad` ,  Determine available NUMA node ,  `/usr/bin` ,  `src/util/virnuma.c`
`rmmod` ,  remove module from Linux kernel ,  `/usr/sbin` ,  `src/util/virjson.c`
`stat` ,  System statistics ,  `/proc` ,  `src/util/virhostcpu.c`
`system` ,  System devices information ,  `/sys/devices` ,  `src/util/virhostcpu.c`
`tap%d` ,  Tap netdev device ,  `/dev` ,  `src/util/virnetdevip.c`
`uptime` ,  uptime since bootup ,  `/proc` ,  `src/util/virhostmem.c`
`vfio` ,  subdirectory to virtual file input/output ,  `/dev` ,  `src/util/virlog.c`
`virip.pid` ,  IPv6 virtualprocess ID ,  `/var/run` ,  `src/util/virnetdevip.c`
[/jtable]

# URI, query parameters
[jtable]
Envvar name ,  Default value ,  Description
`authfile` ,  `/etc/libvirt/auth.conf` ,  Second priority lookup for the authentication configuration file.  The file path specified by the `authfile` URI query parameter
`/proc/self/fd` ,  TBS ,  
`filename` ,  `/etc/libvirt/conf` ,   Defines the directory path to the `virt-manager` configuration file.
`hostsfile` ,  TBS ,  
`addnhosts` ,  TBS ,  
`username` ,  TBS ,  
[/jtable]

# Settings for `auth.conf`
The content of the `auth.conf` file is in [.INI v1.4](https://cloanto.com/specs/ini/#escapesequences) text format.
[jtable]
Keyword ,  Description ,  Default
`VIR_CRED_AUTHNAME`, Authenticator account name, n/a
`VIR_CRED_PASSPHRASE`, Password to pass on to `virt-manager`, TBS
`VIR_CRED_NOECHOPROMPT`, Suppress output of obfuscated keypresses during password prompt, TBS
[/jtable]


# Command Line Options

[jtable]
Option name,  Description
`--bind-dynamic`, `dnsmasq`-specific
`--concurrent`, firewall
`--ra-param`, `dnsmasq`-specific
[/jtable]

# Firewall 
The following firewall chain name have been reserved by the `libvirt`/`libvirtd` library/daemon.
[jtable]
Firewall Chain Name,  Description
`nat`,		  NAT
`LIBVIRT_INP` ,   Firewall input, 
`LIBVIRT_FWI` ,   Firewall input, `viriptable.c`
`LIBVIRT_FWO` ,   Firewall output, `viriptable.c`
`LIBVIRT_FWX` ,   Firewall forward, `viriptable.c`
`LIBVIRT_OUT` ,   Firewall output, 
`LIBVIRT_PRT` ,   Firewall postrouting, 
[/jtable]
