title: Match criteria in OpenSSH
date: 2026-02-03 03:00
status: published
Tags: OpenSSH, sshd, configuration, match
category: HOWTO
Summary: Match-capable sshd\_config directives in OpenSSH 10.2, grouped by function.
lang: en
private: False

Below is a complete, matchable-only list for OpenSSH 10.2, regrouped by functionality (not resorted arbitrarily).

Complete List
====

A alphabetical list for 'Matchable' keywords (for 10.2) are:

`AcceptEnv`, `AllowAgentForwarding`, `AllowGroups`, `AllowStreamLocalForwarding`, `AllowTcpForwarding`, `AllowUsers`, `AuthenticationMethods`, `AuthorizedKeysCommand`, `AuthorizedKeysCommandUser`, `AuthorizedKeysFile`, `AuthorizedPrincipalsCommand`, `AuthorizedPrincipalsCommandUser`, `AuthorizedPrincipalsFile`, `Banner`, `CASignatureAlgorithms`, `ChannelTimeout`, `ChrootDirectory`, `ClientAliveCountMax`, `ClientAliveInterval`, `DenyGroups`, `DenyUsers`, `DisableForwarding`, `ExposeAuthInfo`, `ForceCommand`, `GatewayPorts`, `GSSAPIAuthentication`, `GssApiCleanupCredentials`, `GSSAPIStrictAcceptorCheck`, `HostbasedAcceptedAlgorithms`, `HostbasedAuthentication`, `HostbasedUsesNameFromPacketOnly`, `IgnoreRhosts`, `Include`, `IPQo`, `KbdInteractiveAuthentication`, `LogLevel`, `MaxAuthTries`, `MaxSessions`, `PAMServiceName`, `PermitEmptyPasswords`, `PermitListen`, `PermitOpen`, `PermitRootLogin`, `PermitTT`, `PermitTunnel`, `PermitUserR`, `PubkeyAcceptedAlgorithms`, `PubkeyAuthentication`, `PubkeyAuthOptions`, `RefuseConnection`, `RekeyLimit`, `RevokedKeys`, `SetEnv`, `StreamLocalBindMask`, `StreamLocalBindUnlink`, `TrustedUserCAKeys`, `UnusedConnectionTimeout`, `X11DisplayOffset`, `X11Forwarding`, `X11UseLocalhost`

By Functional Categories
====
The list below is organized by:

* Initialization / Environment
* Connnection / Transport Behavior
* Forwarding / Tunneling
* Authentication (How user prove identity)
* Authorization (Who is allowed)
* Key / Certificate Authorization
* Session / Setup & Control
* Miscellaneous / Observability

## Initialization / Environment

[jtable]
Keyword,Description
`AcceptEnv`,Accept client-provided environment variables
`Banner`,Display pre-authentication login banner
`Include`,Include additional sshd_config files
`SetEnv`,Set environment variables for sessions
[/jtable]

## Connection & Transport Behavior

[jtable]
Keyword,Description
`ChannelTimeout`,Close idle SSH channels after timeout
`ClientAliveCountMax`,Max unanswered keepalives before disconnect
`ClientAliveInterval`,Interval between keepalive messages
`GatewayPorts`,Control remote port forwarding bind address
`IPQoS`,Set IP QoS/TOS values for connections
`RekeyLimit`,Limit data or time before rekeying
`UnusedConnectionTimeout`,Close unused connections
[/jtable]

## Forwarding / Tunneling

[jtable]
Keyword,Description
`AllowAgentForwarding`,Permit SSH agent forwarding
`AllowStreamLocalForwarding`,Permit UNIX-domain socket forwarding
`AllowTcpForwarding`,Permit TCP port forwarding
`DisableForwarding`,Disable all forwarding features
`PermitListen`,Restrict listening addresses for forwards
`PermitOpen`,Restrict destination addresses for forwards
`StreamLocalBindMask`,Set permissions for stream local sockets
`StreamLocalBindUnlink`,Allow unlinking existing stream sockets
`X11Forwarding`,Enable X11 forwarding
`X11DisplayOffset`,First X11 display number
`X11UseLocalhost`,Bind X11 forwarding to localhost
[/jtable]

## Authentication (How users prove identity)

[jtable]
Keyword,Description
`AuthenticationMethods`,Require specific authentication method combinations
`GSSAPIAuthentication`,Enable GSSAPI/Kerberos authentication
`GssApiCleanupCredentials`,Remove GSSAPI credentials on logout
`GSSAPIStrictAcceptorCheck`,Enforce strict GSSAPI acceptor checks
`HostbasedAuthentication`,Enable host-based authentication
`HostbasedAcceptedAlgorithms`,Allowed host-based signature algorithms
`HostbasedUsesNameFromPacketOnly`,Use hostname from client packet
`KbdInteractiveAuthentication`,Enable keyboard-interactive authentication
`MaxAuthTries`,Maximum authentication attempts
`PubkeyAuthentication`,Enable public key authentication
`PubkeyAcceptedAlgorithms`,Allowed public key algorithms
`PubkeyAuthOptions`,Control per-key authentication behavior
[/jtable]

## Authorization (Who is allowed)

[jtable]
Keyword,Description
`AllowGroups`,Permit login only for listed groups
`AllowUsers`,Permit login only for listed users
`DenyGroups`,Deny login for listed groups
`DenyUsers`,Deny login for listed users
`PermitRootLogin`,Control root login permissions
`PermitEmptyPasswords`,Allow empty passwords
[/jtable]

## Key & Certificate Authorization

[jtable]
Keyword,Description
`AuthorizedKeysFile`,Location of authorized_keys files
`AuthorizedKeysCommand`,External command to fetch public keys
`AuthorizedKeysCommandUser`,User to run authorized keys command
`AuthorizedPrincipalsFile`,File listing certificate principals
`AuthorizedPrincipalsCommand`,Command to fetch certificate principals
`AuthorizedPrincipalsCommandUser`,User to run principals command
`CASignatureAlgorithms`,Allowed CA signature algorithms
`RevokedKeys`,File of revoked public keys
`TrustedUserCAKeys`,Trusted certificate authority keys
[/jtable]

## Session Setup & Control

[jtable]
Keyword,Description
`ChrootDirectory`,Chroot users after authentication
`ForceCommand`,Force execution of a specific command
`LogLevel`,Set logging verbosity
`MaxSessions`,Maximum multiplexed sessions
`PAMServiceName`,PAM service name to use
`PermitTTY`,Allow allocation of a TTY
`PermitTunnel`,Allow tun device forwarding
`PermitUserRC`,Allow execution of user rc files
`RefuseConnection`,Refuse matched connections immediately
[/jtable]

## Miscellaneous / Observability

[jtable]
Keyword,Description
`ExposeAuthInfo`,Expose authentication info to subprocesses
`IgnoreRhosts`,Ignore legacy .rhosts authentication
[/jtable]



Final Notes
====

* This list is exhaustive for matchable directives
* Every directive above is legal inside Match in OpenSSH 10.2.
* Anything not shown must remain global-only.
* Grouping reflects how sshd processes the connection lifecycle, not alphabetical order.
