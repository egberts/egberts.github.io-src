Title: OpenSSH Overview
Date: 2016-09-24T12:08
Modified: 2022-03-15 08:00
Status: published
Tags: ssh, OpenSSH, environment variables
Category: research
Summary: An overview of OpenSSH server and client.
This page details the hardening of SSH.

* [SSH client](SSH_client "wikilink")
* [SSH server](SSH_server "wikilink")

Algorithms Used
===============

To display available algorithms for a specific SSH client

```bash
ssh -Q cipher
ssh -Q cipher-auth
ssh -Q mac
ssh -Q kex
ssh -Q key
```

Audit
=====

Auto-Assess
-----------

To audit in a passive manner the SSH servers and clients, execute
`ssh-audit`.

`ssh-audit` (written in Python) can be found over at
[GitHub jtesta/ssh-audit](https://github.com/jtesta/ssh-audit).

Manual Remediation
------------------

To manually check and ensure that the SSH is clamped down securely,
execute the following:

* [CIS Debian Linux 8 Benchmark v1.0.0](https://benchmarks.cisecurity.org/tools2/linux/CIS_Debian_Linux_8_Benchmark_v1.0.0.pdf)
* [CIS Debian Linux 7 Benchmark v1.0.0](https://benchmarks.cisecurity.org/tools2/linux/CIS_Debian_Linux_7_Benchmark_v1.0.0.pdf)

Make effective all changes, by executing:

```bash
    systemctl reload sshd.service
```

Escape Codes
============

Did you know that when you’re using OpenSSH from the command line you
have a variety of escape sequences available to you? SSH somewhere, then
type “~” and “?” (tilde, then question mark) to see all the options. You
should get something like: SSH Escape Codes

Supported escape sequences:

[jtable]
command sequence, description
~., connection (and any multiplexed sessions)
~B, a BREAK to the remote system
~C, a command line
~R, rekey (SSH protocol 2 only)
~^Z, ssh
~#, forwarded connections
~&, ssh (when waiting for connections to terminate)
~?, message
~~, the escape character by typing it twice

Most commonly, I use tilde-period (~.) to close an unresponsive session,
like when a firewall has closed my connection. BREAK is useful for
various things, usually getting back to a terminal server console or
getting the attention of network equipment. The command line doesn’t do
much, but you can alter forwards from it. I’ve never used it but it’s
probably handy for troubleshooting if your tunnels aren’t working right:

```ssh
ssh> ?
Commands:`
     -L[bind_address:]port:host:hostport
     -R[bind_address:]port:host:hostport
     -D[bind_address:]port
     -KR[bind_address:]port
```

Request local forward Request remote forward Request dynamic forward
Cancel remote forward

I’ve also never had to rekey a session for any reason, as SSH protocol
version 2 does it automatically after a certain amount of data has been
transferred. You can mess with it via the RekeyLimit configuration
directives, or read more about it in RFC 4344. Suspending SSH via
tilde-Ctrl-Z is handy from time to time, especially when you’re on the
console of a machine that doesn’t have screen or some other multiplexer
on it (or you forgot to start one). Of course, you have to remember that
when you need it, but now that you’ve read it maybe you will.

List forwarded connections is handy for managing the forwards you might
have created with the command line. Backgrounding SSH attempts to close
all the connections, and will wait patiently for them to die. I have
never needed this, because I’m the impatient bastard that just
tilde-periods them if they don’t close right away.

You can use the EscapeChar configuration directive to change the tilde,
if that conflicts with something. Or you can just type it twice to send
it.

Current Secured Configurations
==============================

Current Secured Client Configuration
------------------------------------
```cfg
#
# ssh_config
#
# Description: ssh client system-wide configuration file
#
# Status:  Hardened
#
# This is the ssh client system-wide configuration file.  See
# ssh_config(5) for more information.  This file provides defaults for
# users, and the values can be changed in per-user configuration files
# or on the command line.

# Configuration data is parsed as follows:
#  1. command line options
#  2. user-specific file
#  3. system-wide file
# Any configuration value is only changed the first time it is set.
# Thus, host-specific definitions should be at the beginning of the
# configuration file, and defaults at the end.

# Site-wide defaults for some commonly used options.  For a comprehensive
# list of available options, their meanings and defaults, please see the
# ssh_config(5) man page.

# Keyword ordering in this ssh_config are laided
# out as the ssh client binary actually acts
# on them.
# This naturally results in grouping such as
#    key exchange,
#    user authentication, and
#    session.

# IgnoreUnknown specifies a pattern-list of unknown
#    options to be ignored if they are encountered
#    in configuration parsing.
#    This may be used to suppress errors if
#    ssh_config contains options that are unrecognised
#    by ssh(1).
#    It is recommended that IgnoreUnknown be listed
#    early in the configuration file as it will not
#    be applied to unknown options that appear
#    before it.
IgnoreUnknown yes

# Include includes the specified configuration
#    file(s).  Multiple pathnames may be specified
#    and each pathname may contain glob(7)
#    wildcards and, for user configurations,
#    shell-like ‘~’ references to user home
#    directories.  Files without absolute paths are
#    assumed to be in ~/.ssh if included in a user
#    configuration file or /etc/ssh if included from
#    the system configuration file.  Include
#    directive may appear inside a Match or Host
#    block to perform conditional inclusion.
#Include /etc/ssh/ssh_config_local

# HostName specifies the real host name to log into.
#    This can be used to specify nicknames or
#    abbreviations for hosts.  Arguments to HostName
#    accept the tokens described in the TOKENS
#    section.  Numeric IP addresses are also
#    permitted (both on the command line and in
#    HostName specifications).  The default is the
#    name given on the command line.
#    Source: main()/ssh.c
# HostName <system-hostname>  # default

# CanonicalizeHostname controls whether explicit
#    hostname canonicalization is performed.
#    The default, no, is not to perform any name
#    rewriting and let the system resolver handle all
#    hostname lookups.  If set to yes then, for
#    connections that do not use a ProxyCommand or
#    ProxyJump, ssh(1) will attempt to canonicalize
#    the hostname specified on the command line using
#    the CanonicalDomains suffixes and
#    CanonicalizePermittedCNAMEs rules.
#    If CanonicalizeHostname is set to always, then
#    canonicalization is applied to proxied
#    connections too.
#    Source: options.canonicalize_hostname/resolve_canonicalize()/main()
#    Source: options.canonicalize_hostname/check_follow_cname()/resolve_canonicalize()/main()
CanonicalizeHostname no


# CanonicalizeMaxDots specifies the maximum number of
#    dot characters in a hostname before
#    canonicalization is disabled.  The default, 1,
#    allows a single dot (i.e. hostname.subdomain).
#    Source: resolve_canonicalize()/ssh.c
# CanonicalizeMaxDots 1  # default
CanonicalizeMaxDots 1

# CanonicalDomains When CanonicalizeHostname is
#    enabled, this option specifies the list of
#    domain suffixes in which to search for the
#    specified destination host.
#    Source options.num_canonical_domains/resolve_canonicalize()/main()
#    Source options.canonical_domains[]/resolve_canonicalize()/main()


# CanonicalizeFallbackLocal specifies whether to fail
#    with an error when hostname canonicalization
#    fails.  The default, yes, will attempt to look
#    up the unqualified hostname using the system
#    resolver's search rules.  A value of no will
#    cause ssh(1) to fail instantly if
#    CanonicalizeHostname is enabled and the target
#    hostname cannot be found in any of the domains
#    specified by CanonicalDomains.
#    Source: resolve_canonicalize()/ssh.c
CanonicalizeFallbackLocal yes

# CanonicalizePermittedCNAMEs specifies rules to
#    determine whether CNAMEs should be followed when
#    canonicalizing hostnames.  The rules consist of
#    one or more arguments of
#    source_domain_list:target_domain_list, where
#    source_domain_list is a pattern-list of domains
#    that may follow CNAMEs in canonicalization, and
#    target_domain_list is a pattern-list of domains
#    that they may resolve to.
#
#    For example,
#    "*.a.example.com:*.b.example.com,*.c.example.com"
#    will allow hostnames matching "*.a.example.com" to
#    be canonicalized to names in the "*.b.example.com"
#    or "*.c.example.com" domains.
#    Source: resolve_canonicalize()/ssh.c
# CanonicalizePermittedCNAMEs <cname-hostname>

# AddressFamily specifies which address family to use
#    when connecting.  Valid arguments are any (the
#    default), inet (use IPv4 only), or inet6 (use
#    IPv6 only).
#    Source: is_addr()/resolve_canonicalize()/ssh.c
# AddressFamily any  # default
# AddressFamily inet
# AddressFamily inet6
AddressFamily inet

# Port specifies the port number to connect on the
#    remote host.  The default is 22.
#    Source: main()/ssh.c
Port 22

# ProxyCommand specifies the command to use to
#    connect to the server.  The command string
#    extends to the end of the line, and is executed
#    using the user's shell ‘exec’ directive to avoid
#    a lingering shell process.
#
#    Arguments to ProxyCommand accept the tokens
#    described in the TOKENS section.  The command
#    can be basically anything, and should read from
#    its standard input and write to its standard
#    output.  It should eventually connect an sshd(8)
#    server running on some machine, or execute
#    sshd -i somewhere.  Host key management will be
#    done using the HostName of the host being
#    connected (defaulting to the name typed by the
#    user).  Setting the command to none disables
#    this option entirely.  Note that CheckHostIP is
#    not available for connects with a proxy command.
#    NOTE: Ignore ProxyCommand if ProxyJump already
#          specified.
#
#    This directive is useful in conjunction with
#    nc(1) and its proxy support.  For example, the
#    following directive would connect via an HTTP
#    proxy at 192.0.2.0:
#
#        ProxyCommand /usr/bin/nc -X connect -x 192.0.2.0:8080 %h %p
#        ProxyCommand ssh -q -W %h:%p gateway.example.com
#    Source: main()/ssh.c

# ClearAllForwardings specifies that all local,
#    remote, and dynamic port forwardings specified
#    in the configuration files or on the command
#    line be cleared.  This option is primarily
#    useful when used from the ssh(1) command line to
#    clear port forwardings set in configuration
#    files, and is automatically set by scp(1) and
#    sftp(1).
#    The argument must be yes or no (the default).
#    Source: options.clear_forwardings/fill_default_options()/main()
# ClearAllForwardings no  # default
ClearAllForwardings no

# ProxyJump specifies one or more jump proxies as
#    either [user@]host[:port] or an ssh URI.
#    Multiple proxies may be separated by comma
#    characters and will be visited sequentially.
#    Setting this option will cause ssh(1) to connect
#    to the target host by first making a ssh(1)
#    connection to the specified ProxyJump host and
#    then establishing a TCP forwarding to the
#    ultimate target from there.
#
#    Note that this option will compete with the
#    ProxyCommand option - whichever is specified
#    first will prevent later instances of the other
#    from taking effect.
#    NOTE: ProxyCommand is ignored if ProxyJump
#          already specified.
#    Source: options.jump_host/process_config_line_depth()/main()/ssh.c
#    Source: options.jump_user/process_config_line_depth()/main()/ssh.c
#    Source: options.jump_port/process_config_line_depth()/main()/ssh.c
#    Source: options.jump_extra/process_config_line_depth()/main()/ssh.c
# ProxyJump  <ssh-URI>

# ProxyUseFdpass specifies that ProxyCommand will
#    pass a connected file descriptor back to
#    ssh(1) instead of continuing to execute and
#    pass data.  The default is no.
#    Source: main()/ssh.c
# ProxyUseFdpass no  # default

# Protocol is obsoleted since 7.1; always v2
Protocol 2

# ControlPersist, when used in conjunction with
#    ControlMaster, specifies that the master
#    connection should remain open in the background
#    (waiting for future client connections) after
#    the initial client connection has been closed.
#    If set to no, then the master connection will
#    not be placed into the background, and will
#    close as soon as the initial client connection
#    is closed.  If set to yes or 0, then the master
#    connection will remain in the background
#    indefinitely (until killed or closed via a
#    mechanism such as the "ssh -O exit").  If set to
#    a time in seconds, or a time in any of the
#    formats documented in sshd_config(5), then the
#    backgrounded master connection will
#    automatically terminate after it has remained
#    idle (with no client connections) for the
#    specified time.  (ssh_session2()/ssh.c)
#    Source: main()/ssh.c
# ControlPersist   # not specified by default

# UpdateHostKeys specifies whether ssh(1) should accept
#    notifications of additional hostkeys from the
#    server sent after authentication has completed and
#    add them to UserKnownHostsFile.  The argument must
#    be yes, no (the default) or ask.  Enabling this
#    option allows learning alternate hostkeys for a
#    server and supports graceful key rotation by
#    allowing a server to send replacement public keys
#    before old ones are removed.  Additional hostkeys
#    are only accepted if the key used to authenticate
#    the host was already trusted or explicitly accepted
#    by the user.  If UpdateHostKeys is set to ask, then
#    the user is asked to confirm the modifications to
#    the known_hosts file.  Confirmation is currently
#    incompatible with ControlPersist, and will be
#    disabled if it is enabled.
#
# Presently, only sshd(8) from OpenSSH 6.8 and greater
#    support the "hostkeys@openssh.com" protocol
#    extension used to inform the client of all the
#    server's hostkeys.
#    Source: main()/ssh.c
# UpdateHostKeys no  # default
UpdateHostKeys no
# UpdateHostKeys ask
# UpdateHostKeys yes

# ConnectionAttempts specifies the number of tries
#    (one per second) to make before exiting.  The
#    argument must be an integer.  This may be
#    useful in scripts if the connection sometimes
#    fails.  The default is 1.
#    Source: main()/ssh.c
# ConnectionAttempts 1  # default
ConnectionAttempts 1

# RemoteCommand specifies a command to execute on the
#    remote machine after successfully connecting to
#    the server.  The command string extends to the
#    end of the line, and is executed with the user's
#    shell.  Arguments to RemoteCommand accept the
#    tokens described in the TOKENS section.
#    Source: main()/ssh.c
# RemoteCommand # not defined by default

# LogLevel gives the verbosity level that is used
#    when logging messages from ssh(1).  The
#    possible values are: QUIET, FATAL, ERROR, INFO,
#    VERBOSE, DEBUG, DEBUG1, DEBUG2, and DEBUG3.
#    The default is INFO.
#    DEBUG and DEBUG1 are equivalent.
#    DEBUG2 and DEBUG3 each specify higher levels of
#    verbose output.
#    Source: options.log_level/main()/ssh.c
# LogLevel INFO  # default
LogLevel INFO

# SyslogFacility gives the facility code that is used
#    when logging messages from ssh(1).  The possible
#    values are: DAEMON, USER, AUTH, LOCAL0, LOCAL1,
#    LOCAL2, LOCAL3, LOCAL4, LOCAL5, LOCAL6, LOCAL7.
#    The default is USER.
#    Source: options.log_facility/main()/ssh.c
# SyslogFacility USER  # default
SyslogFacility AUTH

# RequestTTY specifies whether to request a pseudo-tty
#    for the session.  The argument may be one of:
#        no (never request a TTY),
#        yes (always request a TTY when standard input is a TTY),
#        force (always request a TTY) or
#        auto (request a TTY when opening a login session).
#            This option mirrors the -t and -T flags for ssh(1).
#    Source: options.request_tty/main()/ssh.c
# RequestTTY no
# RequestTTY yes
# RequestTTY force
# RequestTTY auto

# User specifies the user to log in as.
#    This can be useful when a different user name is
#    used on different machines.  This saves the
#    trouble of having to remember to give the user
#    name on the command line.
#    Used with 'IdentityAgent' option.
#    Source: options.user/main()/ssh.c
#  User <derived-from-pw->pw_name>

# ControlPath specify the path to the control socket
#    used for connection sharing as described in the
#    ControlMaster section above or the string none
#    to disable connection sharing.  Arguments to
#    ControlPath may use the tilde syntax to refer to
#    a user's home directory or the tokens described
#    in the TOKENS section.  It is recommended that
#    any ControlPath used for opportunistic
#    connection sharing include at least %h, %p, and
#    %r (or alternatively %C) and be placed in a
#    directory that is not writable by other users.
#    This ensures that shared connections are
#    uniquely identified.
#    Source: options.control_path/main()/ssh.c

# ConnectTimeout specifies the timeout (in seconds)
#    used when connecting to the SSH server, instead
#    of using the default system TCP timeout.  This
#    value is used only when the target is down or
#    really unreachable, not when it refuses the
#    connection.
#    Source: options.connect_timeout/main()/ssh.c
# ConnectTimeout 0  # default
ConnectTimeout 0

# TCPKeepAlive specifies whether the system should
#    send TCP keepalive messages to the other side.
#    If they are sent, death of the connection or
#    crash of one of the machines will be properly
#    noticed.  This option only uses TCP keepalives
#    (as opposed to using ssh level keepalives), so
#    takes a long time to notice when the connection
#    dies.  As such, you probably want the
#    ServerAliveInterval option as well.  However,
#    this means that connections will die if the
#    route is down temporarily, and some people find
#    it annoying.
#
#    The default is yes (to send TCP keepalive
#    messages), and the client will notice if the
#    network goes down or the remote host dies.  This
#    is important in scripts, and many users want
#    it too.
#
#    To disable TCP keepalive messages, the value
#    should be set to no.  See also ServerAliveInterval
#    for protocol-level keepalives.
# TCPKeepAlive yes  # default
TCPKeepAlive yes

# BindAddress use the specified address on the local
#    machine as the source address of the connection.
#    Only useful on systems with more than one address.
#    Source: options.bind_address/ssh_create_socket()/ssh_connect_direct()/ssh_connect()/main()


# BindInterface use the address of the specified
#    interface on the local machine as the source
#    address of the connection.
#    Source: options.bind_interface/ssh_create_socket()/ssh_connect_direct()/ssh_connect()/main()


# ServerAliveInterval sets a timeout interval in
#    seconds after which if no data has been received
#    from the server, ssh(1) will send a message
#    through the encrypted channel to request a
#    response from the server.  The default is 0,
#    indicating that these messages will not be sent
#    to the server, or 300 if the BatchMode option is
#    set (Debian-specific).  ProtocolKeepAlives and
#    SetupTimeOut are Debian-specific compatibility
#    aliases for this option.
# ServerAliveInterval 0  # default 0
ServerAliveInterval 0

# ServerAliveCountMax sets the number of server alive
#    messages (see below) which may be sent without
#    ssh(1) receiving any messages back from the
#    server.  If this threshold is reached while
#    server alive messages are being sent, ssh will
#    disconnect from the server, terminating the
#    session.  It is important to note that the use
#    of server alive messages is very different from
#    TCPKeepAlive (below).  The server alive messages
#    are sent through the encrypted channel and
#    therefore will not be spoofable.  The TCP
#    keepalive option enabled by TCPKeepAlive is
#    spoofable.  The server alive mechanism is
#    valuable when the client or server depend on
#    knowing when a connection has become inactive.
#
#    The default value is 3.  If, for example,
#    ServerAliveInterval (see below) is set to 15
#    and ServerAliveCountMax is left at the default,
#    if the server becomes unresponsive, ssh will
#    disconnect after approximately 45 seconds.
# ServerAliveCountMax 3  # default
ServerAliveCountMax 3

# PKCS11Provider specifies which PKCS#11 provider to
#    use.  The argument to this keyword is the
#    PKCS#11 shared library ssh(1) should use to
#    communicate with a PKCS#11 token providing the
#    user's private RSA key.
#    Source: load_public_identity_file()/ssh.c
# PKCS11Provider

# BatchMode, if set to yes, passphrase/password
#    querying will be disabled.  In addition, the
#    ServerAliveInterval option will be set to 300
#    seconds by default (Debian-specific).  This
#    option is useful in scripts and other batch jobs
#    where no user is present to supply the password,
#    and where it is desirable to detect a broken
#    network swiftly.  The argument must be yes or
#    no (the default).
#    Source: options.batch_mode/ssh.c
# BatchMode no  # default
BatchMode no

# IdentityFile specifies a file from which the user's
#    DSA, ECDSA, Ed25519 or RSA authentication
#    identity is read.
#    The default are all:
#        IdentityFile ~/.ssh/id_dsa
#        IdentityFile ~/.ssh/id_ecdsa
#        IdentityFile ~/.ssh/id_ed25519
#        IdentityFile ~/.ssh/id_rsa
#    Additionally, any identities represented by the
#    authentication agent will be used for
#    authentication unless IdentitiesOnly is set.
#    If no certificates have been explicitly
#    specified by CertificateFile, ssh(1) will try to
#    load certificate information from the filename
#    obtained by appending -cert.pub to the path of a
#    specified IdentityFile.
#
#    Arguments to IdentityFile may use the tilde
#    syntax to refer to a user's home directory or
#    the tokens described in the TOKENS section.
#
#    It is possible to have multiple identity files
#    specified in configuration files; all these
#    identities will be tried in sequence.  Multiple
#    IdentityFile directives will add to the list of
#    identities tried (this behaviour differs from
#    that of other configuration directives).
#    Source: options.num_identity_files/pubkey_prepare()/ssh_userauth2()/ssh.c
#    Source: options.identity_files[]/pubkey_prepare()/ssh_userauth2()/ssh.c
#    Source: options.identity_keys[]/pubkey_prepare()/ssh_userauth2()/ssh.c
#    Source: options.identity_file_userprovided[]/pubkey_prepare()/ssh_userauth2()/ssh.c


# IdentityAgent specifies the UNIX-domain socket used
#    to communicate with the authentication agent.
#
#    This option overrides the SSH_AUTH_SOCK
#    environment variable and can be used to select a
#    specific agent.  Setting the socket name to none
#    disables the use of an authentication agent.  If
#    the string "SSH_AUTH_SOCK" is specified, the
#    location of the socket will be read from the
#    SSH_AUTH_SOCK environment variable.  Otherwise
#    if the specified value begins with a ‘$’
#    character, then it will be treated as an
#    environment variable containing the location of
#    the socket.
#
#    Arguments to IdentityAgent may use the tilde
#    syntax to refer to a user's home directory or
#    the tokens described in the TOKENS section.
#    Source: main()/ssh.c

# StreamLocalBindMask sets the octal file creation
#    mode mask (umask) used when creating a
#    UNIX-domain socket file for local or remote port
#    forwarding.  This option is only used for port
#    forwarding to a UNIX-domain socket file.
#
#    The default value is 0177, which creates a
#    UNIX-domain socket file that is readable and
#    writable only by the owner.  Note that not all
#    operating systems honor the file mode on
#    UNIX-domain socket files.
StreamLocalBindMask 0177

#
# StreamLocalBindUnlink specifies whether to remove
#    an existing UNIX-domain socket file for local or
#    remote port forwarding before creating a new
#    one.
#    If the socket file already exists and
#    StreamLocalBindUnlink is not enabled, ssh will
#    be unable to forward the port to the
#    UNIX-domain socket file.
#    This option is only used for port forwarding to
#    a UNIX-domain socket file.
#
#    The argument must be yes or no (the default).
StreamLocalBindUnlink no


# GlobalKnownHostsFile specifies one or more files
#    to use for the global host key database,
#    separated by whitespace.  The default
#    is /etc/ssh/ssh_known_hosts, and
#    /etc/ssh/ssh_known_hosts2.
#    Source: options.system_hostfiles[]/main()/ssh.c
#    NOTE: disable /etc/ssh/ssh_known_hosts2
GlobalKnownHostsFile /etc/ssh/ssh_known_hosts

# UserKnownHostsFile specifies one or more files to
#    use for the user host key database, separated
#    by whitespace.  The default is
#    ~/.ssh/known_hosts, ~/.ssh/known_hosts2.
#    Source: options.user_hostfiles[]/main()/ssh.c
UserKnownHostsFile ~/.ssh/known_hosts


##################################################################
#################  KEY EXCHANGE  #################################
##################################################################

# Ciphers specifies the ciphers allowed and their
#    order of preference.  Multiple ciphers must be
#    comma-separated.  If the specified value begins
#    with a ‘+’ character, then the specified ciphers
#    will be appended to the default set instead of
#    replacing them.  If the specified value begins
#    with a ‘-’ character, then the specified ciphers
#    (including wildcards) will be removed from the
#    default set instead of replacing them.
#
#              The supported ciphers are:
#
#                  3des-cbc
#                  aes128-cbc
#                  aes192-cbc
#                  aes256-cbc
#                  aes128-ctr
#                  aes192-ctr
#                  aes256-ctr
#                  aes128-gcm@openssh.com
#                  aes256-gcm@openssh.com
#                  chacha20-poly1305@openssh.com
#
#            The default is:
#
#                  chacha20-poly1305@openssh.com,
#                  aes128-ctr,aes192-ctr,aes256-ctr,
#                  aes128-gcm@openssh.com,aes256-gcm@openssh.com
#
#            The list of available ciphers may also be obtained using "ssh -Q
#            cipher".
#    Source: options.ciphers/ssh_kex2()/ssh_login()/sslconnect2.c
# Ciphers chacha20-poly1305@openssh.com, aes128-ctr,aes192-ctr,aes256-ctr, aes128-gcm@openssh.com,aes256-gcm@openssh.com  # default
# Ciphers chacha20-poly1305@openssh.com,aes256-ctr,aes256-gcm@openssh.com
Ciphers chacha20-poly1305@openssh.com,aes256-ctr

# KexAlgorithms specifies the available KEX (Key
#    Exchange) algorithms.  Multiple algorithms must
#    be comma-separated.  Alternately if the
#    specified value begins with a ‘+’ character,
#    then the specified methods will be appended to
#    the default set instead of replacing them.
#    If the specified value begins with a ‘-’
#    character, then the specified methods
#    (including wildcards) will be removed from the
#    default set instead of replacing them.
#    The default is:
#
#        curve25519-sha256,curve25519-sha256@libssh.org,
#        ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,
#        diffie-hellman-group-exchange-sha256,
#        diffie-hellman-group16-sha512,
#        diffie-hellman-group18-sha512,
#        diffie-hellman-group-exchange-sha1,
#        diffie-hellman-group14-sha256,
#        diffie-hellman-group14-sha1
#
#    The list of available key exchange
#    algorithms may also be obtained using "ssh -Q kex".
#    Source: options.kex_algorithms/ssh_kex2()/ssh_login()/sslconnect2.c
# KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org, ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521, diffie-hellman-group-exchange-sha256, diffie-hellman-group16-sha512, diffie-hellman-group18-sha512, diffie-hellman-group-exchange-sha1, diffie-hellman-group14-sha256, diffie-hellman-group14-sha1  # default
KexAlgorithms curve25519-sha256@libssh.org,curve25519-sha256,diffie-hellman-group18-sha512,diffie-hellman-group16-sha512

# Compression specifies whether to use compression.
#    The argument must be yes or no (the default).
#
# NOTE: Compression leaves tell-tale fingerprinting for keystroke analysis
# Source: options.compression/ssh_kex2()/ssh_login()/sslconnect2.c
# Compression no  # default
Compression no

# MACs specifies the MAC (message authentication
#    code) algorithms in order of preference.
#    The MAC algorithm is used for data integrity
#    protection.  Multiple algorithms must be
#    comma-separated.  If the specified value begins
#    with a ‘+’ character, then the specified
#    algorithms will be appended to the default set
#    instead of replacing them.  If the specified
#    value begins with a ‘-’ character, then the
#    specified algorithms (including wildcards) will
#    be removed from the default set instead of
#    replacing them.
#
#    The algorithms that contain "-etm" calculate the
#    MAC after encryption (encrypt-then-mac).  These
#    are considered safer and their use recommended.
#
#    The default is:
#
#        umac-64-etm@openssh.com,umac-128-etm@openssh.com,
#        hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,
#        hmac-sha1-etm@openssh.com,
#        umac-64@openssh.com,umac-128@openssh.com,
#        hmac-sha2-256,hmac-sha2-512,hmac-sha1
#
#    The list of available MAC algorithms may also be
#    obtained using:
#        "ssh -Q mac".
# Source: options.macs/ssh_kex2()/ssh_login()/sslconnect2.c
# MACs umac-64-etm@openssh.com,umac-128-etm@openssh.com, hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com, hmac-sha1-etm@openssh.com, umac-64@openssh.com,umac-128@openssh.com, hmac-sha2-256,hmac-sha2-512,hmac-sha1  # default
# MACs hmac-sha2-512,hmac-sha2-256,hmac-sha1,hmac-ripemd160  # SLE
# Place "-etm" algos in front
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256


# HostKeyAlgorithms specifies the host key algorithms
#    that the client wants to use in order of
#    preference.  Alternately if the specified value
#    begins with a ‘+’ character, then the specified
#    key types will be appended to the default set
#    instead of replacing them.  If the specified
#    value begins with a ‘-’ character, then the
#    specified key types (including wildcards) will
#    be removed from the default set instead of
#    replacing them.  The default for this option is:
#
#        ecdsa-sha2-nistp256-cert-v01@openssh.com,
#        ecdsa-sha2-nistp384-cert-v01@openssh.com,
#        ecdsa-sha2-nistp521-cert-v01@openssh.com,
#        ssh-ed25519-cert-v01@openssh.com,
#        rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,
#        ssh-rsa-cert-v01@openssh.com,
#        ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,
#        ssh-ed25519,rsa-sha2-512,rsa-sha2-256,ssh-rsa
#
#    If hostkeys are known for the destination host
#        then this default is modified to prefer their algorithms.
#
#    The list of available key types may also be obtained using:
#         "ssh -Q key" command.
# Source: options.hostkeyalgs/ssh_kex2()/ssh_login()/sslconnect2.c
# HostKeyAlgorithms ecdsa-sha2-nistp256-cert-v01@openssh.com, ecdsa-sha2-nistp384-cert-v01@openssh.com, ecdsa-sha2-nistp521-cert-v01@openssh.com, ssh-ed25519-cert-v01@openssh.com, rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com, ssh-rsa-cert-v01@openssh.com, ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521, ssh-ed25519,rsa-sha2-512,rsa-sha2-256,ssh-rsa  # default
# HostKeyAlgorithms ssh-ed25519-cert-v01@openssh.com,ssh-rsa-cert-v01@openssh.com,ssh-ed25519,ssh-rsa
HostKeyAlgorithms ssh-ed25519-cert-v01@openssh.com,ssh-ed25519,ssh-rsa-cert-v01@openssh.com,rsa-sha2-512


# RekeyLimit specifies the maximum amount of data that
#    may be transmitted before the session key is
#    renegotiated, optionally followed a maximum
#    amount of time that may pass before the session
#    key is renegotiated.  The first argument is
#    specified in bytes and may have a suffix of ‘K’,
#    ‘M’, or ‘G’ to indicate Kilobytes, Megabytes, or
#    Gigabytes, respectively.  The default is between
#    ‘1G’ and ‘4G’, depending on the cipher.
#    The optional second value is specified in
#    seconds and may use any of the units documented
#    in the TIME FORMATS section of sshd_config(5).
#    The default value for RekeyLimit is default
#    none, which means that rekeying is performed
#    after the cipher's default amount of data has
#    been sent or received and no time based
#    rekeying is done.
# Source: options.rekey_limit/ssh_kex2()/ssh_login()/sslconnect2.c
# Source: options.rekey_interval/ssh_kex2()/ssh_login()/sslconnect2.c
# RekeyLimit 1G 1h  # default

# FingerprintHash specifies the hash algorithm used
#    when displaying key finger‐ prints.
#    Valid options are: md5 and sha256 (the default).
# FingerprintHash sha256  # default
FingerprintHash sha256

# RevokedHostKeys specifies revoked host public keys.
#    Keys listed in this file will be refused for
#    host authentication.
#    Note that if this file does not exist or is not
#    readable, then host authentication will be
#    refused for all hosts.
#    Keys may be specified as a text file, listing
#    one public key per line, or as an OpenSSH Key
#    Revocation List (KRL) as generated by
#    ssh-keygen(1).
#    For more information on KRLs, see the KEY
#    REVOCATION LISTS section in ssh-keygen(1).

# VerifyHostKeyDNS specifies whether to verify the
#    remote key using DNS and SSHFP resource
#    records.
#    If this option is set to yes, the client will
#    implicitly trust keys that match a secure
#    fingerprint from DNS.  Insecure fingerprints
#    will be handled as if this option was set to
#    ask.
#    If this option is set to ask, information on
#    fingerprint match will be displayed, but the
#    user will still need to confirm new host keys
#    according to the StrictHostKeyChecking option.
#    The default is no.
#    See also VERIFYING HOST KEYS in ssh(1).
# VerifyHostKeyDNS no  # default
# VerifyHostKeyDNS ask
# VerifyHostKeyDNS yes
VerifyHostKeyDNS yes

# HostKeyAlias specifies an alias that should be used instead
#    of the real host name when looking up or saving the host
#    key in the host key database files and when validating
#    host certificates.  This option is useful for tunneling
#    SSH connections or for multiple servers running on a
#    single host.
#    Source: options.host_key_alias/check_host_key()/verify_host_key()/verify_host_key_callback/kex_verify_host_key()/input_kex_gen_reply()/ssh_dispatch_run()/ssh_dispatch_run_fatal()/ssh_userauth2()/ssh_login()/sshconnect2.c
#    Source: options.host_key_alias/userauth_passwd()/userauth()/ssh_dispatch_run()/ssh_dispatch_run_fatal()/ssh_userauth2()/ssh_login()/sshconnect2.c
# HostKeyAlias ssh  # no default

# NoHostAuthenticationForLocalhost disable host
#    authentication for localhost (loopback addresses).
#    The argument to this keyword must be yes or
#    no (the default).
#    Source: options.no_host_authentication_for_localhost/check_host_key()/verify_host_key()/verify_host_key_callback/kex_verify_host_key()/input_kex_gen_reply()/ssh_dispatch_run()/ssh_dispatch_run_fatal()/ssh_userauth2()/ssh_login()/sshconnect2.c
NoHostAuthenticationForLocalhost no

# VisualHostKey, if this flag is set to yes, an ASCII
#    art representation of the remote host key
#    fingerprint is printed in addition to the
#    fingerprint string at login and for unknown host
#    keys.  If this flag is set to no (the default),
#    no fingerprint strings are printed at login and
#    only the fingerprint string will be printed for
#    unknown host keys.
VisualHostKey yes

# StrictHostKeyChecking, if this flag is set to yes,
#    ssh(1) will never automatically add host keys to
#    the ~/.ssh/known_hosts file, and refuses to
#    connect to hosts whose host key has changed.
#    This provides maximum protection against
#    man-in-the-middle (MITM) attacks, though it can
#    be annoying when the /etc/ssh/ssh_known_hosts
#    file is poorly maintained or when connections
#    to new hosts are frequently made.  This option
#    forces the user to manually add all new hosts.
#
#    If this flag is set to “accept-new” then ssh
#    will automatically add new host keys to the user
#    known hosts files, but will not permit
#    connections to hosts with changed host keys.
#    If this flag is set to “no” or “off”, ssh will
#    automatically add new host keys to the user
#    known hosts files and allow connections to hosts
#    with changed hostkeys to proceed, subject to
#    some restrictions.
#    If this flag is set to ask (the default), new
#    host keys will be added to the user known host
#    files only after the user has confirmed that is
#    what they really want to do, and ssh will refuse
#    to connect to hosts whose host key has changed.
#    The host keys of known hosts will be verified
#    automatically in all cases.
# StrictHostKeyChecking yes
# StrictHostKeyChecking ask  # default
# StrictHostKeyChecking accept-new
# StrictHostKeyChecking no
StrictHostKeyChecking accept-new


##################################################################
#################  USER AUTHENTICATION  ##########################
##################################################################

# HostbasedAuthentication specifies whether to try
#    rhosts based authentication with public key
#    authentication.  The argument must be yes or
#    no (the default).
#    Source: options.hostbased_authentication/check_host_key()
# HostbasedAuthentication no  # default
HostbasedAuthentication no

# ChallengeResponseAuthentication specifies whether
#    to use challenge-response authentication.  The
#    argument to this keyword must be yes (the
#    default) or no.
#    NOTE: A yes enables KbdInteractiveAuthentication
#    NOTE: If host name or IP changed from what
#        the known_hosts file contains, then
#        KbdInteractiveAuthentication and
#        ChallengeResponseAuthentication get disabled.
#    Source: options.challenge_response_authentication(r/w)/ssh_userauth2()
#    Source: options.challenge_response_authentication(r)/check_host_key()
# ChallengeResponseAuthentication yes  # default
ChallengeResponseAuthentication no

# PasswordAuthentication specifies whether to use
#    password authentication.
#    The argument to this keyword must be yes
#    (the default) or no.
# PasswordAuthentication yes  # default
PasswordAuthentication yes

# KbdInteractiveAuthentication specifies whether to
#    use keyboard-interactive authentication.  The
#    argument to this keyword must be yes (the
#    default) or no.
#    Source: options.kbd_interactive_authentication/userauth_kbdint()/userauth()/input_userauth_failure()/ssh_dispatch_run()/ssh_dispatch_run_fatal()/ssh_userauth2()/ssh_login()/sshconnect2.c
# KbdInteractiveAuthentication yes  # default
KbdInteractiveAuthentication yes

# PubkeyAuthentication specifies whether to try
#    public key authentication.
#    The argument to this keyword must be yes (the
#    default) or no.
# PubkeyAuthentication yes  # default
PubkeyAuthentication yes

# GSSAPIAuthentication specifies whether user
#    authentication based on GSSAPI is allowed.
#    The default is no.
#    Source: options.gss_authentication
# GSSAPIAuthentication no  # maintainer-default
# GSSAPIAuthentication yes  # Debian-default
GSSAPIAuthentication yes

# PreferredAuthentications specifies the order in
#     which the client should try authentication
#     methods.  This allows a client to prefer one
#     method (e.g.  keyboard-interactive) over
#     another method (e.g. password).  The default
#     is:
#
#     gssapi-with-mic,hostbased,publickey,
#     keyboard-interactive,password
#
#     Source: options.preferred_authentication/ssh_userauth2()/ssh_login()/sshconnect2.c
PreferredAuthentications gssapi-with-mic,hostbased,publickey,keyboard-interactive,password

# CertificateFile specifies a file from which the user
#    's certificate is read.  A corresponding private
#    key must be provided separately in order to use
#    this certificate either from an IdentityFile
#    directive or -i flag to ssh(1), via
#    ssh-agent(1), or via a PKCS11Provider.
#
#    Arguments to CertificateFile may use the tilde
#    syntax to refer to a user's home directory or
#    the tokens described in the TOKENS section.
#
#    It is possible to have multiple certificate
#    files specified in configuration files; these
#    certificates will be tried in sequence.
#    Multiple CertificateFile directives will add to
#    the list of certificates used for authentication.
#    Source: options.num_certificate_files/pubkey_prepare()/ssh_userauth2()
#    Source: options.certificate_files[]/pubkey_prepare()/ssh_userauth2()
#    Source: options.certificate_file_userprovided[]/pubkey_prepare()/ssh_userauth2()

# IdentitiesOnly specifies that ssh(1) should only
#     use the authentication identity and certificate
#     files explicitly configured in the ssh_config
#     files or passed on the ssh(1) command-line,
#     even if ssh-agent(1) or a PKCS11Provider offers
#     more identities.  The argument to this keyword
#     must be yes or no (the default).  This option
#     is intended for situations where ssh-agent
#     offers many different identities.
#     Source: options.identities_only/pubkey_prepare()/ssh_userauth2()/ssh_login()/sshconnect2.c
IdentitiesOnly no

# options.fingerprint_hash/format_identity()/pubkey_prepare()/ssh_userauth2()

# NumberOfPasswordPrompts specifies the number of
#    password prompts before giving up.
#    The argument to this keyword must be an integer.
#    The default is 3.
#    Used only with:
#        KbdInteractiveAuthentication,
#        PubkeyAuthentication,
#        PasswordAuthentication
#    Source: options.number_of_password_prompts/userauth_kbdint()/userauth()/ssh_dispatch_run()/ssh_dispatch_run_fatal()/ssh_userauth2()/ssh_login()/sshconnect2.c
#    Source: options.number_of_password_prompts/load_identity_file()/userauth_pubkey()/userauth()/ssh_dispatch_run()/ssh_dispatch_run_fatal()/ssh_userauth2()/ssh_login()/sshconnect2.c
#    Source: options.number_of_password_prompts/userauth_passwd()/userauth()/ssh_dispatch_run()/ssh_dispatch_run_fatal()/ssh_userauth2()/ssh_login()/sshconnect2.c
# NumberOfPasswordPrompts 3  # default
NumberOfPasswordPrompts 3

# CASignatureAlgorithms specifies which algorithms
#    are allowed for signing of certificates by
#    certificate authorities (CAs).
#    The default is:
#        ecdsa-sha2-nistp256.ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,
#        ssh-ed25519,rsa-sha2-512,rsa-sha2-256,ssh-rsa
#
#    ssh(1) will not accept host certificates signed
#    using algorithms other than those specified.
#
#    Note: Used with HostbasedAuthentication and ??? (TBS)
#
#    Source: options.ca_sign_algorithms/check_host_cert()/check_host_key()/verify_host_key()/verify_host_key_callback()/kex_verify_host_key()/input_kex_gen_reply()/ssh_dispatch_run()/ssh_dispatch_run_fatal()/ssh_kex2()/ssh_login()/main()
# CASignatureAlgorithms ecdsa-sha2-nistp256.ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,ssh-ed25519,rsa-sha2-512,rsa-sha2-256,ssh-rsa  # default
CASignatureAlgorithms ssh-ed25519,rsa-sha2-512


######################################
#  User Authentication - Host-based  #
######################################

# HostbasedKeyTypes specifies the key types that will
#    be used for hostbased authentication as a
#    comma-separated list of patterns.  Alternately
#    if the specified value begins with a ‘+’
#    character, then the specified key types will be
#    appended to the default set instead of replacing
#    them.  If the specified value begins with a ‘-’
#    character, then the specified key types
#    (including wildcards) will be removed from the
#    default set instead of replacing them.
#    The default for this option is:
#
#        ecdsa-sha2-nistp256-cert-v01@openssh.com,
#        ecdsa-sha2-nistp384-cert-v01@openssh.com,
#        ecdsa-sha2-nistp521-cert-v01@openssh.com,
#        ssh-ed25519-cert-v01@openssh.com,
#        rsa-sha2-512-cert-v01@openssh.com,
#        rsa-sha2-256-cert-v01@openssh.com,
#        ssh-rsa-cert-v01@openssh.com,
#        ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,
#        ecdsa-sha2-nistp521,
#        ssh-ed25519,rsa-sha2-512,rsa-sha2-256,ssh-rsa
#
#    The -Q option of ssh(1) may be used to list
#    supported key types.
# HostbasedKeyTypes ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,ssh-rsa-cert-v01@openssh.com,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,ssh-ed25519,rsa-sha2-512,rsa-sha2-256,ssh-rsa  # default
HostbasedKeyTypes ssh-ed25519-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,ssh-ed25519,rsa-sha2-512

# EnableSSHKeysign setting this option to yes in the
#    global client configuration file
#    /etc/ssh/ssh_config enables the use of the
#    helper program ssh-keysign(8) during
#    HostbasedAuthentication.
#    The argument must be yes or no (the default).
#    This option should be placed in the
#    non-hostspecific section.
#    See ssh-keysign(8) for more information.
EnableSSHKeysign no



##################################
# User Authentication - Password #
##################################


##############################################
# User Authentication - Keyboard Interactive #
##############################################

# KbdInteractiveDevices specifies the list of methods
#    to use in keyboard-interactive authentication.
#    Multiple method names must be comma-separated.
#    The default is to use the server specified list.
#    The methods available vary depending on what the
#    server supports.  For an OpenSSH server, it may
#    be zero or more of: bsdauth and pam.
#    Source: options.kdb_interactive_devices/
# KbdInteractiveDevices bsdauth  # maintainer-default
# KbdInteractiveDevices pam  # Debian-default
KbdInteractiveDevices pam

######################################
#  User Authentication - Public Key  #
######################################

# PubkeyAcceptedKeyTypes specifies the key types that
#    will be used for public key authentication as a
#    comma-separated list of patterns.  Alternately
#    if the specified value begins with a ‘+’
#    character, then the key types after it will be
#    appended to the default instead of replacing it.
#    If the specified value begins with a ‘-’
#    character, then the specified key types
#    (including wildcards) will be removed from the
#    default set instead of replacing them.
#    The default for this option is:
#
#        ssh-ed25519
#        ssh-ed25519-cert-v01@openssh.com
#        ssh-rsa
#        ecdsa-sha2-nistp256
#        ecdsa-sha2-nistp384
#        ecdsa-sha2-nistp521
#        ssh-rsa-cert-v01@openssh.com
#        ecdsa-sha2-nistp256-cert-v01@openssh.com
#        ecdsa-sha2-nistp384-cert-v01@openssh.com
#        ecdsa-sha2-nistp521-cert-v01@openssh.com
#        ssh-dss (not a default)
#        ssh-dss-cert-v01@openssh.com (not a default)
#        rsa-sha2-512-cert-v01@openssh.com (unlisted)
#        rsa-sha2-256-cert-v01@openssh.com (unlisted)
#        rsa-sha2-512 (unlisted)
#        rsa-sha2-256 (unlisted)
#
#    The list of available key types may also be obtained using "ssh
#    -Q key".
#
#     Source: options.pubkey_key_types/pubkey_prepare()/ssh_userauth2()/ssh_login()/sshconnect2.c
PubkeyAcceptedKeyTypes ssh-ed25519,ssh-ed25519-cert-v01@openssh.com

# AddKeysToAgent specifies whether keys should be
#    automatically added to a running ssh-agent(1).
#    If this option is set to yes and a key is loaded
#    from a file, the key and its passphrase are
#    added to the agent with the default lifetime, as
#    if by ssh-add(1).  If this option is set to ask,
#    ssh(1) will require confirmation using the
#    SSH_ASKPASS program before adding a key (see
#    ssh-add(1) for details).  If this option is set
#    to confirm, each use of the key must be
#    confirmed, as if the -c option was specified to
#    ssh-add(1).  If this option is set to no, no
#    keys are added to the agent.
#    The argument must be yes, confirm, ask, or
#    no (the default).
#    Source: options.add_key_to_agent/maybe_add_key_to_agent()/load_identity_file()/identity_sign()/sign_and_send_pubkey()/userauth_pubkey()/userauth()/input_userauth_failure()/ssh_dispatch_run()/ssh_dispatch_run_fatal()/ssh_userauth2()/ssh_login()/main()
# AddKeysToAgent no  # default
AddKeysToAgent no


##################################
#  User Authentication - GSSAPI  #
##################################

# GSSAPIDelegateCredentials forward (delegate)
#    credentials to the server.
#    The default is no.
#    Source: options.gss_deleg_creds
# GSSAPIDelegateCredentials no  # default
GSSAPIDelegateCredentials no


##################################################################
#################  SESSION  ######################################
##################################################################

# ControlMaster enables the sharing of multiple
#     sessions over a single network connection.
#     When set to yes, ssh(1) will listen for
#     connections on a control socket specified using
#     the ControlPath argument. Additional sessions
#     can connect to this socket using the same
#     ControlPath with ControlMaster set to no (the
#     default). These sessions will try to reuse the
#     master instance's network connection rather
#     than initiating new ones, but will fall back
#     to connecting normally if the control socket
#     does not exist, or is not listening.
#
#     Setting this to ask will cause ssh(1) to listen
#     for control connections, but require
#     confirmation using ssh-askpass(1). If the
#     ControlPath cannot be opened, ssh(1) will
#     continue without connecting to a master
#     instance.
#
#     X11 and ssh-agent(1) forwarding is supported
#     over these multiplexed connections, however the
#     display and agent forwarded will be the one
#     belonging to the master connection i.e. it is
#     not possible to forward multiple displays or
#     agents.
#
#     Two additional options allow for opportunistic
#     multiplexing: try to use a master connection
#     but fall back to creating a new one if one does
#     not already exist. These options are: auto and
#     autoask. The latter requires confirmation like
#     the ask option.
#
#     NOTE:  'MaxSession 1' disables ControlMaster

ControlMaster ask

# TunnelDevice specifies the tun(4) devices to open
#    on the client (local_tun) and the server
#    (remote_tun).
#
#    The argument must be local_tun[:remote_tun].
#    The devices may be specified by numerical ID or
#    the keyword any, which uses the next available
#    tunnel device.  If remote_tun is not specified,
#    it defaults to any.  The default is any:any.
#    Source: options.tun_local/ssh_init_stdio_forwarding()/ssh_session2()/ssh.c
#    Source: options.tun_remote/ssh_init_stdio_forwarding()/ssh_session2()/ssh.c
# TunnelDevice any:any  # default

# LocalForward specifies that a TCP port on the local
#    machine be forwarded over the secure channel to
#    the specified host and port from the remote
#    machine.  The first argument must be
#    [bind_address:]port and the second argument must
#    be host:hostport.  IPv6 addresses can be
#    specified by enclosing addresses in square
#    brackets.  Multiple forwardings may be
#    specified, and additional forwardings can be
#    given on the command line.  Only the superuser
#    can forward privileged ports.  By default, the
#    local port is bound in accordance with the
#    GatewayPorts setting.  However, an explicit
#    bind_address may be used to bind the connection
#    to a specific address.  The bind_address of
#    localhost indicates that the listening port be
#    bound for local use only, while an empty address
#    or ‘*’ indicates that the port should be
#    available from all interfaces.
#    Source: options.num_local_forwards/ssh_init_forwarding/ssh_session2/main
#    Source: options.local_forwards[]/ssh_init_forwarding/ssh_session2/main

# GatewayPorts specifies whether remote hosts are
#    allowed to connect to local forwarded ports.
#    By default, ssh(1) binds local port forwardings
#    to the loopback address.  This prevents other
#    remote hosts from connecting to forwarded ports.
#    GatewayPorts can be used to specify that ssh
#    should bind local port forwardings to the
#    wildcard address, thus allowing remote hosts to
#    connect to forwarded ports.
#    The argument must be yes or no (the default).
#    Source: options.fwd_opts.gateway_ports/ssh_init_forwarding()/ssh_session2()/main()
# GatewayPorts no  # default
GatewayPorts no

# RemoteForward specifies that a TCP port on the
#    remote machine be forwarded over the secure
#    channel.  The remote port may either be
#    forwarded to a specified host and port from the
#    local machine, or may act as a SOCKS 4/5 proxy
#    that allows a remote client to connect to
#    arbitrary destinations from the local machine.
#    The first argument must be [bind_address:]port
#    If forwarding to a specific destination then the
#    second argument must be host:hostport, otherwise
#    if no destination argument is specified then the
#    remote forwarding will be established as a SOCKS
#    proxy.
#
#    IPv6 addresses can be specified by enclosing
#    addresses in square brackets.  Multiple
#    forwardings may be specified, and additional
#    forwardings can be given on the command line.
#    Privileged ports can be forwarded only when
#    logging in as root on the remote machine.
#
#    If the port argument is 0, the listen port will
#    be dynamically allocated on the server and
#    reported to the client at run time.
#    Source: options.num_remote_forwards/ssh_init_forwarding/ssh_session2/main
#    Source: options.remote_forwards[]/ssh_init_forwarding/ssh_session2/main


# DynamicForward specifies that a TCP port on the
#    local machine be forwarded over the secure
#    channel, and the application protocol is then
#    used to determine where to connect to from the
#    remote machine.
#
#    The argument must be [bind_address:]port.  IPv6
#    addresses can be specified by enclosing
#    addresses in square brackets.  By default, the
#    local port is bound in accordance with the
#    GatewayPorts setting.  However, an explicit
#    bind_address may be used to bind the connection
#    to a specific address.  The bind_address of
#    localhost indicates that the listening port be
#    bound for local use only, while an empty address
#    or ‘*’ indicates that the port should be
#    available from all interfaces.
#
#    Currently the SOCKS4 and SOCKS5 protocols are
#    supported, and ssh(1) will act as a SOCKS
#    server.  Multiple forwardings may be specified,
#    and additional forwardings can be given on the
#    command line.  Only the superuser can forward
#    privileged ports.
#    Source: options.num_local_forwards/ssh_init_forwarding/ssh_session2/main
#    Source: options.local_forwards[]/ssh_init_forwarding/ssh_session2/main
#    Source: options.num_remote_forwards/ssh_init_forwarding/ssh_session2/main
#    Source: options.remote_forwards[]/ssh_init_forwarding/ssh_session2/main

# ExitOnForwardFailure specifies whether ssh(1)
#    should terminate the connection if it cannot set
#    up all requested dynamic, tunnel, local, and
#    remote port forwardings, (e.g. if either end is
#    unable to bind and listen on a specified port).
#    Note that ExitOnForwardFailure does not apply to
#    connections made over port forwardings and will
#    not, for example, cause ssh(1) to exit if TCP
#    connections to the ultimate forwarding
#    destination fail.  The argument must be yes or
#    no (the default).
#    Source: options.exit_on_fwd_failure/ssh_init_forwarding()/ssh_session2()/main()/ssh.c)
ExitOnForwardFailure no

# Tunnel request tun(4) device forwarding between the
#    client and the server.  The argument must be
#    yes, point-to-point (layer 3), ethernet (layer 2),
#    or no (the default).  Specifying yes requests
#    the default tunnel mode, which is point-to-point.
#    Source: options.tun_open/ssh_init_forwarding/ssh_session2()
Tunnel no

# PermitLocalCommand allows local command execution
#    via the LocalCommand option or using the
#    !command escape sequence in ssh(1).
#    The argument must be yes or no (the default).
#    Source: options.permit_local_cmd/ssh_local_cmd()/ssh_session2()/main
# PermitLocalCommand no  # default
PermitLocalCommand no

# LocalCommand specifies a command to execute on the
#    local machine after successfully connecting to
#    the server.  The command string extends to the
#    end of the line, and is executed with the user's
#    shell.  Arguments to LocalCommand accept the
#    tokens described in the TOKENS section.
#
#    The command is run synchronously and does not
#    have access to the session of the ssh(1) that
#    spawned it.  It should not be used for
#    interactive commands.
#
#    This directive is ignored unless
#    PermitLocalCommand has been enabled.
#    Source: options.local_command/ssh_local_cmd()/

# ForwardX11 specifies whether X11 connections will
#    be automatically redirected over the secure
#    channel and DISPLAY set.
#    The argument must be yes or no (the default).
#
#    X11 forwarding should be enabled with caution.
#    Users with the ability to bypass file
#    permissions on the remote host (for the user's
#    X11 authorization database) can access the
#    local X11 display through the forwarded
#    connection.
#    An attacker may then be able to perform
#    activities such as keystroke monitoring if the
#    ForwardX11Trusted option is also enabled.
#    Source: options.forward_x11/ssh_session2_setup()/channel_register_open_confirm()/ssh_session2_open()/ssh_session2()/main()/sshconnect.c
# ForwardX11 no  # default
ForwardX11 no

# XAuthLocation specifies the full pathname of the
#    xauth(1) program.  The default is /usr/bin/xauth.
#    Source: options.xauth_location/ssh_session2_setup()/channel_register_open_confirm()/ssh_session2_open()/ssh_session2()/main()/sshconnect.c
XAuthLocation /usr/bin/xauth

# ForwardX11Trusted, if this option is set to yes,
#    (the Debian-specific default), remote X11
#    clients will have full access to the original
#    X11 display.
#
#    If this option is set to no (the upstream default),
#    remote X11 clients will be considered untrusted
#    and prevented from stealing or tampering with
#    data belonging to trusted X11 clients.
#    Furthermore, the xauth(1) token used for the
#    session will be set to expire after 20 minutes.
#    Remote clients will be refused access after
#    this time.
#
#    See the X11 SECURITY extension specification for
#    full details on the restrictions imposed on
#    untrusted clients.
#    Source: options.forward_x11_trusted/ssh_session2_setup()/channel_register_open_confirm()/ssh_session2_open()/ssh_session2()/main()/sshconnect.c
# ForwardX11Trusted yes  # Debian-default
# ForwardX11Trusted no  # maintainer-default
ForwardX11Trusted yes

# ForwardX11Timeout specify a timeout for untrusted
#    X11 forwarding using the format described in the
#    TIME FORMATS section of sshd_config(5).
#    X11 connections received by ssh(1) after this
#    time will be refused.  Setting ForwardX11Timeout
#    to zero will disable the timeout and permit X11
#    forwarding for the life of the connection.
#    The default is to disable untrusted X11
#    forwarding after twenty minutes has elapsed.
#    Source: options.forward_x11_timeout/ssh_session2_setup()/channel_register_open_confirm()/ssh_session2_open()/ssh_session2()/main()/sshconnect.c
ForwardX11Timeout 1200

# ForwardAgent specifies whether the connection to
#    the authentication agent (if any) will be
#    forwarded to the remote machine.
#    The argument must be yes or no (the default).
#
#    Agent forwarding should be enabled with caution.
#    Users with the ability to bypass file
#    permissions on the remote host (for the agent's
#    UNIX-domain socket) can access the local agent
#    through the forwarded connection.  An attacker
#    cannot obtain key material from the agent,
#    however they can perform operations on the keys
#    that enable them to authenticate using the
#    identities loaded into the agent.
#    Source: options.forward_agent/ssh_session2_setup()/channel_register_open_confirm()/ssh_session2_open()/ssh_session2()/main()/sshconnect.c
# ForwardAgent no  # default
ForwardAgent no

# IPQoS specifies the IPv4 type-of-service or DSCP
#    class for connections.
#    Accepted values are
#    af11, af12, af13, af21, af22, af23, af31, af32,
#    af33, af41, af42, af43, cs0, cs1, cs2, cs3, cs4,
#    cs5, cs6, cs7, ef, lowdelay, throughput,
#    reliability, a numeric value, or none to use
#    the operating system default.
#    This option may take one or two arguments,
#    separated by whitespace.
#    If one argument is specified, it is used as the
#    packet class unconditionally.
#    If two values are specified, the first is
#    automatically selected for interactive sessions
#    and the second for non-interactive sessions.
#    The default is lowdelay for interactive sessions
#    and throughput for non-interactive sessions.
#    Source: options.ip_qos_iteractive
#    Source: options.ip_qos_bulk
# IPQoS lowdelay throughput  # default
IPQoS lowdelay throughput

# SendEnv specifies what variables from the local
#    environ(7) should be sent to the server.  The
#    server must also support it, and the server must
#    be configured to accept these environment
#    variables.
#    Note that the TERM environment variable is
#    always sent whenever a pseudo-terminal is
#    requested as it is required by the protocol.
#    Refer to AcceptEnv in sshd_config(5) for how to
#    configure the server.  Variables are specified
#    by name, which may contain wildcard characters.
#    Multiple environment variables may be separated
#    by whitespace or spread across multiple
#    SendEnv directives.
#
#    It is possible to clear previously set SendEnv
#    variable names by prefixing patterns with -.
#    The default is not to send any environment
#    variables.
#    Source: options.num_send_env/
#    Source: options.send_env[]/
SendEnv LANG LC_*

# SetEnv directly specify one or more environment
#    variables and their contents to be sent to the
#    server.  Similarly to SendEnv, the server must
#    be prepared to accept the environment variable.
#    Source: options.num_setenv/
#    Source: options.setenv[]/

# EscapeChar sets the escape character (default: ‘~’).
#    The escape character can also be set on the
#    command line.  The argument should be a single
#    character, ‘^’ followed by a letter, or none to
#    disable the escape character entirely (making the
#    connection transparent for binary data).
#    Source: options.escape_char/ssh_session2()/main()/sshconnect.c
# EscapeChar ~  # default
EscapeChar ~


# CheckHostIP, if set to yes (the default), ssh(1)
#    will additionally check the host IP address in
#    the known_hosts file.  This allows it to detect
#    if a host key changed due to DNS spoofing and
#    will add addresses of destination hosts to
#    ~/.ssh/known_hosts in the process, regardless of
#    the setting of StrictHostKeyChecking.
#    If the option is set to no, the check will not
#    be executed.
#    NOTE: CheckHostIP is disabled if connected to
#          localhost only VIA PROXY.
#    Source: options.check_host_ip/client_input_hostkeys()/client_input_global_request()/ssh_dispatch_set()/client_init_dispatch()/client_loop()/ssh_session2/ssh.c
# CheckHostIP yes  # default
CheckHostIP yes

# HashKnownHosts indicates that ssh(1) should hash
#    host names and addresses when they are added to
#    ~/.ssh/known_hosts.  These hashed names may be
#    used normally by ssh(1) and sshd(8), but they do
#    not reveal identifying information should the
#    file's contents be disclosed.
#    The default is no.
#    Note that existing names and addresses in known
#    hosts files will not be converted automatically,
#    but may be manually hashed using ssh-keygen(1).
#    Use of this option may break facilities such as
#    tab-completion that rely on being able to read
#    unhashed host names from ~/.ssh/known_hosts.
#
#    Source: options.hash_known_hosts/update_known_host/client_input_hostkeys()/client_input_global_request()/ssh_dispatch_set()/client_init_dispatch()/client_loop()/ssh_session2/ssh.c
# HashKnownHosts yes  # default
HashKnownHosts no


##################################################################
#################  UH?  AUTHENTICATION  ##########################
##################################################################

# NumberOfPasswordPrompts specifies the number of
#    password prompts before giving up.
#    The argument to this keyword must be an integer.
#    The default is 3.
#    Source: options.number_of_password_prompts/sshconnect2.c
NumberOfPasswordPrompts 3

#    Source: options.kbd_interactive_devices
#    Source: options.hostbased_key_types
#    Source: options.pubkey_key_types

# Host restricts the following declarations (up to
#    the next Host or Match keyword) to be only for
#    those hosts that match one of the patterns given
#    after the keyword.  If more than one pattern is
#    provided, they should be separated by
#    whitespace.  A single ‘*’ as a pattern can be
#    used to provide global defaults for all hosts.
#    The host is usually the hostname argument given
#    on the command line (see the
#    CanonicalizeHostname keyword for exceptions).
#
#    A pattern entry may be negated by prefixing it
#    with an exclamation mark (‘!’).  If a negated
#    entry is matched, then the Host entry is
#    ignored, regardless of whether any other
#    patterns on the line match.  Negated matches are
#    therefore useful to provide exceptions for
#    wildcard matches.
Host *.local
    ForwardX11 yes
    ForwardX11Trusted yes
    UpdateHostKeys no

Host *.onion
    ProxyCommand socat - SOCKS4A:localhost:%h:%p,socksport=9050
    UpdateHostKeys ask

Host *
    UpdateHostKeys yes

# Match restricts the following declarations (up to
#    the next Host or Match keyword) to be used only
#    when the conditions following the Match keyword
#    are satisfied.  Match conditions are specified
#    using one or more criteria or the single token
#    all which always matches.  The available
#    criteria keywords are: canonical, exec, host,
#    originalhost, user, and localuser.  The all
#    criteria must appear alone or immediately after
#    canonical.  Other criteria may be combined
#    arbitrarily.
#    All criteria but all and canonical require an
#    argument.  Criteria may be negated by prepending
#    an exclamation mark (‘!’).
#
#    The canonical keyword matches only when the
#    configuration file is being re-parsed after
#    hostname canonicalization (see the
#    CanonicalizeHostname option.)  This may be
#    useful to specify conditions that work with
#    canonical host names only.  The exec keyword
#    executes the specified command under the user's
#    shell.  If the command returns a zero exit
#    status then the condition is considered true.
#    Commands containing whitespace characters must
#    be quoted.  Arguments to exec accept the tokens
#    described in the TOKENS section.
#
#    The other keywords' criteria must be single
#    entries or comma-separated lists and may use the
#    wildcard and negation operators described in the
#    PATTERNS section.  The criteria for the host
#    keyword are matched against the target hostname,
#    after any substitution by the Hostname or
#    CanonicalizeHostname options.  The originalhost
#    keyword matches against the hostname as it was
#    specified on the command-line.  The user keyword
#    matches against the target username on the
#    remote host.  The localuser keyword matches
#    against the name of the local user running
#    ssh(1) (this keyword may be useful in
#    system-wide ssh_config files).
# Match *

# Obsoleted options:
# RhostsRSAAuthentication no
# RSAAuthentication yes
# GSSAPIKeyExchange no
# GSSAPITrustDNS no
```

Current Secured Server Configuration
------------------------------------

```sshd_config
# Package generated configuration file
# See the sshd_config(5) manpage for details

# What ports, IPs and protocols we listen for
# Port 22
# Open port 2223 on all interfaces
#Port 22
Port 2223
# open port 22 only on gateway IP
ListenAddress 172.28.130.1:22
# ListenAddress 0.0.0.0 closes off all interfaces, except for ones above
ListenAddress 0.0.0.0


# Use these options to restrict which interfaces/protocols sshd will bind to
#ListenAddress ::
Protocol 2
# HostKeys for protocol version 2
HostKey /etc/ssh/ssh_host_ed25519_key
# HostKey /etc/ssh/ssh_host_rsa_key
# HostKey /etc/ssh/ssh_host_ecdsa_key
# HostKey /etc/ssh/ssh_host_dsa_key
#Privilege Separation is turned on for security
# UsePrivilegeSeparation yes  # Obsoleted by OpenSSH 7.9

# Logging
SyslogFacility AUTH
LogLevel INFO
# LogLevel VERBOSE

# Authentication:
LoginGraceTime 35
PermitRootLogin no
StrictModes yes

PubkeyAuthentication yes
#AuthorizedKeysFile %h/.ssh/authorized_keys

# Don't read the user's ~/.rhosts and ~/.shosts files
IgnoreRhosts yes
# similar for protocol version 2
HostbasedAuthentication no
# Uncomment if you don't trust ~/.ssh/known_hosts for RhostsRSAAuthentication
#IgnoreUserKnownHosts yes

# To enable empty passwords, change to yes (NOT RECOMMENDED)
PermitEmptyPasswords no

# Change to yes to enable challenge-response passwords (beware issues with
# some PAM modules and threads)
# ChallengeResponseAuthentication no

# Change to no to disable tunnelled clear text passwords
#PasswordAuthentication yes

# Kerberos options
#KerberosAuthentication no
#KerberosGetAFSToken no
#KerberosOrLocalPasswd yes
#KerberosTicketCleanup yes

# GSSAPI options
#GSSAPIAuthentication no
#GSSAPICleanupCredentials yes

# X11Forwarding no
X11Forwarding yes
X11DisplayOffset 10
PrintMotd yes
PrintLastLog yes
TCPKeepAlive yes
#UseLogin no

#MaxStartups 10:30:60
Banner /etc/issue.net

# Allow client to pass locale environment variables
AcceptEnv LANG LC_*

Subsystem sftp /usr/lib/openssh/sftp-server

# Set this to 'yes' to enable PAM authentication, account processing,
# and session processing. If this is enabled, PAM authentication will
# be allowed through the ChallengeResponseAuthentication and
# PasswordAuthentication.  Depending on your PAM configuration,
# PAM authentication via ChallengeResponseAuthentication may bypass
# the setting of "PermitRootLogin without-password".
# If you just want the PAM account and session checks to run without
# PAM authentication, then enable this but set PasswordAuthentication
# and ChallengeResponseAuthentication to 'no'.
UsePAM yes
IgnoreUserKnownHosts no
PasswordAuthentication yes
GatewayPorts yes
AllowTcpForwarding yes
KeepAlive yes
AllowGroups ssh


# Need to execute the following commands for safer KexAlgorithms
#     ssh-keygen -G moduli-2048.candidates -b 2048
#     ssh-keygen -T moduli-2048 -f moduli-2048.candidates
#
# KexAlgorithms curve25519-sha256@libssh.org,ecdh-sha2-nistp521,ecdh-sha2-nistp384,ecdh-sha2-nistp256,diffie-hellman-group-exchange-sha256
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
# diffie-hellman-group1-sha1
# diffie-hellman-group14-sha1
# diffie-hellman-group-exchange-sha1
# diffie-hellman-group-exchange-sha256
# ecdh-sha2-nistp256
# ecdh-sha2-nistp384
# ecdh-sha2-nistp521
# diffie-hellman-group1-sha1
# curve25519-sha256@libssh.org

Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr

# Following MACs does not work on Mac OSX 10.10 or older
# MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha1
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha1



ChallengeResponseAuthentication yes

# LEO customizations
DenyUsers root
DenyGroups root
ClientAliveInterval 300
ClientAliveCountMax 5

Compression delayed
MaxAuthTries 4
MaxSessions 1
AllowAgentForwarding no

PermitUserEnvironment no
# KeyRegenerationInterval 3600  # obsoleted at OpenSSL 4.7p1

PubkeyAcceptedKeyTypes ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,ssh-rsa-cert-v01@openssh.com,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521

```

# External References #

* [Secure Secure Shell](https://stribika.github.io/2015/01/04/secure-secure-shell.html)
* [grsec](https://grsecurity.net/)
* [tor-hs](https://www.torproject.org/docs/hidden-services.html.en)
* [SSH server comparisons](https://ssh-comparison.quendi.de/comparison/cipher.html)
