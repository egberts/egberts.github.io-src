title: Resource Requirements for `libvirt`
date: 2022-08-08 04:25
modified: 2025-12-31 02:18
status: published
tags: libvirt, virt-manager, VM, QEMU
category: research
summary: What resources does `libvirt` require?
slug: libvirt-resources.md
lang: en
private: False


Eclectic things that I've found about virtual machine (`libvirt`) library that is used by `virt-manager` (among many others).

# Kernel Configuration
The required settings of Linux kernel configuration (`/usr/src/linux/.config`) for `virt-manager` (on the host machine) are:

[jtable]
Kconfig keyword, Value, Description
`CONFIG_FUSE_FS`, y, Enable FUSE filesystem support required by libvirt tooling, which is used by libvirt for mounting virtualized storage in a guest VM.
`CONFIG_BRIDGE_EBT_MARK`, y, Enable support for Ethernet bridge marking in netfilter, used to mark traffic passing through bridges.
`CONFIG_NETFILTER_ADVANCED`, y, Enable advanced netfilter options, required for firewall and packet filtering operations.
`CONFIG_NETFILTER_XT_CONNMARK`, y, Enable connection tracking for netfilter, allowing connection marking for tracking connection states.
`CONFIG_NETFILTER_XT_TARGET_CHECKSUM`, y, Enable checksum handling for netfilter, necessary for checksum calculation in the network packet filtering system.
`CONFIG_IP6_NF_NAT`, y, Enable IPv6 NAT support in netfilter, required for virtualized environments running IPv6 traffic.
`CONFIG_BLK_CGROUP`, y, Enable block device cgroup support, enabling resource management, particularly in virtual machines that need to control disk I/O.
`CONFIG_MEMORY`, y, Enable memory management options, which are required for managing the memory used by virtual machines in a virtualized environment.
`CONFIG_TUN`, y, Enable virtual network device (TUN/TAP) support for networking, allowing support for TUN/TAP virtual networking devices crucial for virtual machine network interfaces.

[/jtable]
Take the default settings on the rest of their kernel suboptions.

# Environment Variables
## Reading Environment Variables
[jtable]
Envvar name, Default value, Description, Source code file
`CODE_FILE`, –, `Source filename for debug macros. The macro is used to capture the filename where a particular function or code is located, helping with debugging and tracing back the exact file and line in case of errors or issues.`, `util.h`
`CODE_LINE`, –, `Source line for debug macros. This macro stores the line number in the source code where a particular piece of code resides, allowing detailed debugging information and making it easier to pinpoint the location of any error or issue during runtime.`, `util.h`
`CODE_FUNC`, –, `Source function for debug macros. This stores the name of the function that is being executed, which is important for debugging, as it helps identify which function caused an issue in the program flow.`, `util.h`
`DISPLAY`, unset, `X11 display. It defines the environment variable for the X11 display server that is being used for graphical output, especially useful in virtualized or remote desktop environments. If not set, it means the display is not yet defined or unset.`, `vbox_common.c`
`DNSMASQ_CLIENT_ID`, unset, `DHCP client identifier. This is used by the DHCP client to uniquely identify itself when requesting an IP address from a DHCP server. It’s unset by default until a value is assigned during network setup.`, `leaseshelper.c`
`DNSMASQ_IAID`, unset, `DHCP IAID (Identity Association Identifier). This is used to uniquely identify a DHCP lease client. IAID is used in combination with the DUID (DHCP Unique Identifier) to identify a client in the DHCPv6 protocol.`, `leaseshelper.c`
`DNSMASQ_SERVER_DUID`, unset, `DHCP server DUID (DHCP Unique Identifier). This variable holds the identifier that uniquely defines a DHCP server. It is critical for the proper functioning of DHCP in networking environments.`, `leasehelper.c`
`DNSMASQ_INTERFACE`, unset, `Network interface name. This variable stores the name of the network interface to which the DHCP service is bound. It is crucial for routing and ensuring the correct interface is used in a virtual machine or network configuration.`, `leaseshelper.c`
`DNSMASQ_LEASE_EXPIRES`, unset, `Lease expiration timestamp. This defines the expiration time for a DHCP lease in a timestamp format, allowing the system to determine when the assigned IP address should be renewed or released.`, `virlease.c`
`DNSMASQ_MAC`, unset, `Client MAC address. This stores the Media Access Control address of the DHCP client, used to uniquely identify devices on the network, particularly in DHCP assignments.`, `leaseshelper.c`
`DNSMASQ_OLD_HOSTNAME`, unset, `Previous hostname. This variable keeps track of the previous hostname of a client, which is helpful in managing changes to the network configuration and ensuring the proper system behavior after a hostname change.`, `virlease.c`
`DNSMASQ_SUPPLIED_HOSTNAME`, unset, `Supplied hostname. This refers to the hostname provided by the client during the DHCP request, which may differ from the one assigned by the system. It is stored for consistency and networking purposes.`, `leaseshelper.c`
`EDITOR`, unset, `Editor used for configuration editing. This environment variable specifies which text editor will be used for configuration tasks, often set to editors like `vim`, `nano`, or `emacs`. If unset, the default editor is used.`, –
`EVENT_GLIB_ADD_HANDLE`, unset, `GLib add file descriptor. This variable is used to manage the addition of file descriptors to GLib’s event loop for non-blocking I/O operations. It helps handle events such as network or disk activity asynchronously.`, `vireventglib.c`
`EVENT_GLIB_ADD_TIMEOUT`, unset, `GLib add timeout. This setting is used for adding timeouts to the GLib event loop, allowing operations to be scheduled at regular intervals or after a set duration. Useful for event-driven applications.`, `vireventglib.c`
`EVENT_GLIB_DISPATCH_HANDLE`, unset, `GLib dispatch fd (file descriptor). This variable refers to the handling of file descriptors in the GLib event loop, allowing the program to respond to network or disk events as they occur.`, `vireventglib.c`
`EVENT_GLIB_DISPATCH_TIMEOUT`, unset, `GLib dispatch timeout. Similar to the dispatch handle, this defines how GLib processes timeout events, ensuring that operations are dispatched after the timeout period has elapsed.`, `vireventglib.c`
`EVENT_GLIB_REMOVE_HANDLE`, unset, `GLib remove file descriptor. This environment variable helps manage the removal of file descriptors from GLib's event loop when they are no longer needed for I/O operations.`, `vireventglib.c`
`EVENT_GLIB_REMOVE_TIMEOUT_IDLE`, unset, `GLib remove idle timeout. This variable is used to remove timeout events that are set to trigger on idle conditions in the GLib event loop, allowing better resource management when no events are active.`, `vireventglib.c`
`EVENT_GLIB_UPDATE_HANDLE`, unset, `GLib update file descriptor. This setting is used to update or modify file descriptors that are being monitored by GLib's event loop, allowing for dynamic handling of I/O events.`, `vireventglib.c`
`LC_ALL`, C, `Locale override. This environment variable is used to set the system's locale configuration, overriding any other settings for consistent language, character encoding, and regional settings. The value 'C' sets it to the default C locale.`, `util.c`
`LD_PRELOAD`, unset, `Preloaded shared libraries. This environment variable specifies a list of shared libraries that should be loaded before any other libraries when an application starts. It is useful for debugging or modifying library behavior at runtime.`, dynamic linker
`LD_LIBRARY_PATH`, unset, `Library search path. This specifies the directories where shared libraries are searched for when an application is run. If unset, the default system paths are used.`, dynamic linker
`LIBVIRT_ADMIN_DEFAULT_URI`, unset, `Default admin connection URI. This environment variable sets the default connection URI for the libvirt administration interface. It helps the program locate and connect to virtual machines and manage them.`, `libvirt-admin.c`
`LIBVIRT_AUTH_FILE`, `/etc/libvirt/auth.conf`, `Authentication config path. This specifies the path to the configuration file used by libvirt for authentication. By default, this file is located at `/etc/libvirt/auth.conf`, where credentials and access control settings are stored.`, `virauth.c`
`LIBVIRT_AUTOSTART`, unset, `Enable autostart. This variable determines whether virtual machines should automatically start when the system boots. If unset, the default behavior is no autostart unless specified in the VM configuration.`, `remote_sockets.c`
`LIBVIRT_DEBUG`, unset, `Debug verbosity. This environment variable controls the level of debugging information that libvirt generates during execution. It can help troubleshoot issues by providing more detailed logs when set.`, `virtlog.c`
`LIBVIRT_DIR_OVERRIDE`, unset, `Override libvirt base directory. This allows the user to override the default installation directory of libvirt, which can be useful for testing or development purposes.`, `virfile.c`
`LIBVIRT_DRIVER_DIR`, unset, `Driver module directory. This variable specifies the location of the directory containing libvirt driver modules, used for managing different hypervisors and other backend components.`, `virfile.c`
`LIBVIRT_GNUTLS_DEBUG`, unset, `GnuTLS debug level. This environment variable controls the verbosity of the debug output from GnuTLS, a library used by libvirt for secure communications. It helps diagnose security-related issues with SSL/TLS.`, `virnettlscontext.c`
`LIBVIRT_LIBSSH_DEBUG`, unset, `libssh debug level. This setting is used to control the verbosity of debugging information generated by the libssh library, which is used for secure communication over SSH.`, `virnetlibsshsession.c`
`LIBVIRT_LOCK_MANAGER_PLUGIN_DIR`, unset, `Lock manager plugins. This variable specifies the directory where libvirt can find lock manager plugins. These plugins are used to manage the locking of resources such as virtual machine images.`, `virtlog.c`
`LIBVIRT_LOG_FILTERS`, unset, `Log category filters. This variable controls the filtering of log messages by category, allowing users to limit or customize the logging output for specific libvirt subsystems.`, `virtlog.c`
Envvar name, Default value, Description, Source code file
`LIBVIRT_LOG_OUTPUT`, unset, `Log output destinations. This environment variable determines where the logs generated by libvirt are sent, such as to specific log files or to the system’s logging facilities. This allows for centralized logging and easier management of log data.`, `virtlog.c`
`LIBVIRT_MTAB`, unset, `Alternate mtab file. This specifies the location of an alternate mtab file that lists mounted filesystems, typically used in virtual environments or when the system does not follow traditional mounting conventions.`, `virfile.c`
`LIBVIRT_SOURCE`, unset, `Log source identifier. This variable is used to tag the source of log messages generated by libvirt, helping to distinguish logs from different sources or subsystems for easier troubleshooting and monitoring.`, `virtlog.c`
`LIBVIRT_STORAGE_BACKEND_DIR`, unset, `Storage backend directory. This specifies the directory where storage backend drivers or modules are stored, which libvirt uses for managing storage pools, volumes, and other storage resources.`, `storage_backend.c`
`LIBVIRT_STORAGE_FILE_DIR`, unset, `File-based storage backends. This variable points to the directory where file-based storage backends are configured, which libvirt uses to manage virtual disk images and other file-based storage resources.`, `storage_backend.c`
`LIBVIRTD_PATH`, unset, `Daemon executable path. This specifies the path to the libvirtd daemon executable, which is the central service that manages virtual machine instances and their resources in libvirt.`, –
`LIBVIRTLOCKD_PATH`, unset, `Lock daemon runtime path. This environment variable points to the path where the libvirt lock daemon is running, helping with the management of resource locking, especially in virtualized environments to avoid conflicts.`, `lock_driver_lockd.c`
`LIBVIRTLOGD_PATH`, unset, `Log daemon runtime path. This variable defines the path for the runtime executable of the log daemon, which handles the logging of libvirt operations and provides a structured log management system.`, `log_manager.c`
`LISTEN_FDNAMES`, unset, `systemd fd names. This variable specifies the names of the file descriptors being passed to the program by systemd, allowing for integration with systemd’s socket activation and other file descriptor management features.`, `virsystemd.c`
`LISTEN_FDS`, unset, `systemd fd count. This environment variable holds the number of file descriptors passed to the program by systemd during startup, which is critical for handling socket-based communication and event-driven programming in systemd-based environments.`, `virsystemd.c`
`LISTEN_PID`, unset, `systemd listener pid. This variable stores the process ID (PID) of the program that systemd has used for socket activation. It helps to track the PID associated with the file descriptors passed during startup.`, `virsystemd.c`
`LOGNAME`, unset, `Login name. This variable stores the login name of the user executing the program, typically derived from the system’s user database and used for identifying the user in logs and configuration files.`, libc
`MESSAGE`, unset, `Syslog message. This variable is used to define the content of messages that are sent to the system’s syslog service, typically used for logging events and error messages generated by the system or applications.`, libc
`NOTIFY_SOCKET`, unset, `systemd notify socket. This is used in systemd-based environments to specify the socket through which services communicate their readiness or status to systemd, typically used to indicate the service's state during startup or shutdown.`, `virsystemd.c`
`PRIORITY`, unset, `Syslog priority. This environment variable specifies the priority level of messages sent to the system’s syslog service, allowing logs to be filtered or categorized based on their severity (e.g., info, warning, error).`, libc
`QEMU_AUDIO_DRV`, unset, `QEMU audio backend. This variable specifies the audio backend driver to be used by QEMU virtual machines, determining the system’s audio configuration for virtualized environments.`, `qemu_domain.c`
`SDL_AUDIODRIVER`, unset, `SDL audio backend. This environment variable specifies the audio backend used by SDL (Simple DirectMedia Layer), which can control how audio is managed in a QEMU or virtualized environment.`, `qemu_domain.c`
`TERM`, unset, `Terminal type. This variable specifies the type of terminal being used, ensuring proper handling of control characters, display formatting, and terminal input/output. It is typically set by the terminal emulator.`, libc
`TMPDIR`, unset, `Temporary directory. This environment variable points to the directory where temporary files should be stored. It is often set to a default location, but can be overridden by users or applications.`, libc
`USER`, unset, `Username. This environment variable specifies the username of the user executing the application, typically derived from the system’s user database and used for file permissions, process management, and logging.`, libc
`VIR_BRIDGE_NAME`, unset, `Default bridge name. This variable specifies the default name of the network bridge used by libvirt for creating virtual network interfaces between virtual machines and the host system.`, `leaseshelper.c`
`XDG_CONFIG_HOME`, unset, `XDG config root. This specifies the directory used for storing user-specific application configuration files, based on the XDG base directory specification.`, `util.c`
`XDG_DATA_HOME`, unset, `XDG data root. This points to the directory where user-specific data files are stored, in accordance with the XDG base directory specification.`, `util.c`
`XDG_CACHE_HOME`, unset, `XDG cache root. This environment variable specifies the directory for storing user-specific cache files, which can be used to optimize application performance by caching frequently accessed data.`, `util.c`
`VIRSH_DEFAULT_CONNECT_URI`, unset, `Default virsh URI. This variable specifies the default URI for connecting to libvirt through the `virsh` command-line tool, allowing users to interact with virtual machines and hypervisors.`, `virsh.c`
[/jtable]

## Writing Environment Variables
[jtable]
Envvar name, Description, Source code file
`HOME`, The user's home directory. This environment variable points to the default directory where user-specific files and configurations are stored. It's typically used by applications and scripts to reference the user's personal directory for storing files, preferences, and settings. It is crucial for identifying the user's environment and managing personal data and configurations. , `virt-login-shell-helper.c`
`IFS`, Shell field separator. The Internal Field Separator (IFS) defines how the shell splits input into fields. It's commonly used in shell scripting to separate variables or data into arrays or individual components. For example, it might separate spaces, tabs, or newlines between fields. Adjusting the IFS can modify how data is parsed within scripts and commands. , `virt-aa-helper.c`
`LISTEN_FDS`, Systemd file descriptors. This variable holds the number of file descriptors that systemd passes to the program during startup, typically related to socket-based communication or inter-process communication. The program can use these file descriptors to accept incoming connections or communicate with other services in a systemd-managed environment. , `virsystemd.c`
`LISTEN_PID`, Systemd listener PID. This environment variable contains the process ID (PID) of the program used by systemd for socket activation. It helps the program identify the PID of the service that is listening for events or connections, allowing for proper handling of socket-based communication within the systemd framework. , `virsystemd.c`
`LOGNAME`, Login name. This environment variable stores the login name of the user executing the program. It is typically derived from the system’s user database and is used in logs, configuration files, and by the system to identify the current user. It helps associate actions with a specific user and is especially useful for tracking and auditing purposes. , `virt-login-shell-helper.c`
`PATH`, Executable search path. This variable contains a colon-separated list of directories where executable files are located. The system uses the `PATH` to search for programs when they are invoked from the command line or within scripts. Modifying the `PATH` allows users to specify custom locations for executables and software binaries. , `virt-login-shell-helper.c`
`SHELL`, User shell. This environment variable specifies the shell program that is used by the user when interacting with the system’s command line interface. It defines the command processor, which interprets commands, provides a command prompt, and executes scripts. Common values include `/bin/bash` or `/bin/zsh`. , `virt-login-shell-helper.c`
`TERM`, Terminal type. This variable defines the type of terminal being used, ensuring proper handling of control characters, display formatting, and terminal input/output. It tells applications which terminal capabilities to expect, enabling them to adjust their output formatting (e.g., color schemes, text wrapping, etc.) based on the terminal being used. , `virt-login-shell-helper.c`
`USER`, Username. This variable holds the username of the user executing the application. It is typically derived from the system's user database, such as `/etc/passwd`, and is used for permissions, logging, and user-specific configurations. It helps the system understand which user is interacting with a particular process. , `virt-login-shell-helper.c`
`VBOX_APP_HOME`, VirtualBox application root. This environment variable specifies the root directory for VirtualBox-related files and configurations. It tells VirtualBox where to find application data, configuration files, and other related resources, ensuring that the application functions properly in different environments or installations. , `vbox_XPCOMCGlue.c`
[/jtable]


## Files (input)
[jtable caption="This is caption" separator=", " th=0 ai="1"]
Filename, Descriptor, Directory, Source code file
`.cache`, Cache directory. This directory holds temporary and cached data generated by applications. It's used to store data that can be recreated but is expensive to regenerate. These caches help applications run faster by avoiding repeated computations or downloads. , $HOME, `vircommand.c`
`.config`, User configuration. This directory contains user-specific configuration files for applications and services. It is typically used to store settings, preferences, and configuration options that modify how applications behave for the user. , $HOME, `vircommand.c`
`.local/share`, User data. This directory is typically used for user-specific application data that doesn't fall under configuration or cache. It may contain logs, resources, or state data needed by applications. , $HOME, `vircommand.c`
`auth.conf`, Authentication config. This file contains the configuration information necessary for authentication within libvirt-managed systems. It is used to define the parameters for secure connections and permissions management. , /etc/libvirt, `virauth.c`
`block`, Block devices. This file or directory is used to manage block devices, which are storage devices that provide raw data access (like hard drives or SSDs). It contains details about devices and their partitioning. , /dev, `virdevmapper.c`
`block`, Block subsystem. This represents the system-level management of block devices, typically found in the `/sys` directory. It exposes information and parameters related to the block devices managed by the Linux kernel. , /sys, `virfile.c`
`cgroups`, Control groups. This directory represents the system’s control groups, a Linux kernel feature that allows for the management of resources (such as CPU, memory, and IO) for a group of processes. , /proc/self, `vircgroup.c`
`control`, Device-mapper control. This file is used to manage device-mapper-based devices in Linux, such as logical volumes. It provides an interface for controlling block-level devices and storage management. , /dev/mapper, `virdevmapper.c`
`cpuinfo`, CPU information. This file contains detailed information about the system’s CPU, including its architecture, model, speed, and number of cores. It’s a valuable resource for system performance tuning and analysis. , /proc, `virhostcpu.c`
`devices`, Device list. This file contains information about all the devices on the system. It is used for querying the current state of the system's hardware devices. , /proc, `virconf.c`
`devices`, Mediated devices. This directory is used for devices that support mediation, where a virtualized device is shared between processes. It helps manage the configuration and access to mediated devices in a system. , /sys/bus/mdev, `virlog.c`
`hugepages`, Hugepage info. This directory contains information related to the system's use of hugepages, which are large memory pages that help optimize memory performance in large-scale applications and virtualized environments. , /sys/kernel/mm, `virnuma.c`
`hook`, Hook scripts. This directory contains scripts executed by libvirt at certain points during its operation, such as before or after certain events like virtual machine lifecycle changes. These are typically used for system-wide configurations or custom actions. , /etc/libvirt, `virhook.c`
`initctl`, Init control. This file allows for the management of services and their states in a system. It interacts with the system's init process to control system-level services. , `/run,/dev,/etc`, `virinitctl.c`
`ipv6_route`, IPv6 routing table. This file provides information about the routing table for IPv6 addresses, which is used to manage how data is routed across networks with IPv6. , /proc/net, `virnetdevip.c`
`journal`, Shared memory logs. This file is used for logging in-memory information shared between processes, typically for system-level logs. It helps store real-time logs for analysis and debugging. , /dev/shm, `virtlog.c`
`ksm`, Kernel samepage merging. This directory contains information about kernel samepage merging, a feature that reduces memory usage by merging identical memory pages in the system. It's useful in virtualized environments to save memory. , /sys/kernel/mm, `virhostmem.c`
`kvm`, KVM device. This directory contains the KVM (Kernel-based Virtual Machine) device nodes used by the Linux kernel to enable full virtualization of the system. , /dev, `virhostcpu.c`
`libvirt`, Main config directory. This directory contains configuration files and other resources used by libvirt for managing virtual machines, storage, and networks. It is the central location for setting up and modifying virtualization environments. , /etc, `virconf.c`
`locale`, Locale database. This directory contains system locale files that define language, region, and character set preferences. It’s essential for ensuring that applications behave correctly in different geographical regions. , /usr/share, `virgdbus.c`
`lldpad.pid`, LLDP daemon pid. This file stores the process ID of the LLDP (Link Layer Discovery Protocol) daemon, which is used for discovering devices on a local network. , /var/run, `virnetdevip.c`
`lldpad.pid`, IPv6 LLDPAD process ID. This file holds the process ID of the IPv6 LLDP daemon, which helps in discovering devices and their IPv6 addresses in a network environment. , /var/run, `src/util/virnetdevip.c`
`loop%i`, Loop control. This device file is used to manage loopback devices in Linux, which are used for creating virtual block devices that map to files on the filesystem. , /dev, `virfile.c`
`loopcontrol`, Loop control. This directory contains information or control mechanisms for managing loop devices in Linux, often used for mounting files as if they were block devices. , /dev, `virfile.c`
`meminfo`, Memory information. This file contains detailed statistics about the system's memory usage, including total memory, free memory, and memory usage by different processes. It is critical for understanding memory performance and managing system resources. , /proc, `virfile.c`
`modprobe`, Add or remove module from Linux kernel. This command or path is used for loading or unloading kernel modules in Linux, allowing users to manage kernel extensions for hardware or software support. , /usr/sbin, `src/util/virjson.c`
`mount`, Active mount point listing. This file contains a list of the currently mounted file systems and their mount points. It helps the system track which devices or filesystems are mounted and accessible. , /proc, `src/util/vircgroup.c`
`numad`, Determine available NUMA node. This utility determines which NUMA (Non-Uniform Memory Access) nodes are available in the system, which is crucial for optimizing memory and CPU placement in multi-processor systems. , /usr/bin, `src/util/virnuma.c`
`rmmod`, Remove module from Linux kernel. This command or path is used to unload kernel modules from the system, often for troubleshooting or when hardware or features are no longer required. , /usr/sbin, `src/util/virjson.c`
`stat`, System statistics. This file provides various system statistics, such as CPU usage, memory usage, disk activity, and other performance indicators. It’s used for monitoring and managing system health. , /proc, `src/util/virhostcpu.c`
`system`, System devices information. This directory contains information about the devices that make up the system's hardware configuration, such as storage devices, CPU cores, and peripherals. , /sys/devices, `src/util/virhostcpu.c`
`tap%d`, Tap netdev device. This represents a network interface used for networking between virtual machines or between virtual and physical machines. It’s typically used in virtualized environments. , /dev, `src/util/virnetdevip.c`
`uptime`, Uptime since bootup. This file contains the system’s uptime, or how long the system has been running since the last reboot. It is commonly used to monitor system stability and operation time. , /proc, `src/util/virhostmem.c`
`vfio`, Subdirectory to virtual file input/output. This directory contains files related to the VFIO (Virtual Function I/O) subsystem in Linux, which allows direct access to devices for virtualized applications. , /dev, `src/util/virlog.c`
`virip.pid`, IPv6 virtual process ID. This file holds the process ID of a virtual process associated with an IPv6 address, typically used in networking or virtualization contexts. , /var/run, `src/util/virnetdevip.c`
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
