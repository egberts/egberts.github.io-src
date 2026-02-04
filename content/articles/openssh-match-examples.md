title: Examples of Match criteria in OpenSSH
date: 2026-02-03 03:00
status: published
Tags: OpenSSH, sshd, configuration, match
category: HOWTO
Summary: Examples of Match-capable sshd\_config directives in OpenSSH 10.2
lang: en
private: False

Some examples of using `Match` criterion in OpenSSH server daemon configuration files (in `/etc/ssh/sshd_config` or `*/sshd_config.d/*`)

For a complete list of 'Matchable' keyword directives that can be used under `Match` criterion statements, see [[{filename}openssh-match.md]].

This article focus on criterion keywords used after the `Match` statement along with its most popular keyword statements afterward.


Summary of Examples of using `Match` directives
====

A alphabetical list for 'Matchable' keywords (for 10.2) are:

`AcceptEnv`, `AllowAgentForwarding`, `AllowGroups`, `AllowStreamLocalForwarding`, `AllowTcpForwarding`, `AllowUsers`, `AuthenticationMethods`, `AuthorizedKeysCommand`, `AuthorizedKeysCommandUser`, `AuthorizedKeysFile`, `AuthorizedPrincipalsCommand`, `AuthorizedPrincipalsCommandUser`, `AuthorizedPrincipalsFile`, `Banner`, `CASignatureAlgorithms`, `ChannelTimeout`, `ChrootDirectory`, `ClientAliveCountMax`, `ClientAliveInterval`, `DenyGroups`, `DenyUsers`, `DisableForwarding`, `ExposeAuthInfo`, `ForceCommand`, `GatewayPorts`, `GSSAPIAuthentication`, `GssApiCleanupCredentials`, `GSSAPIStrictAcceptorCheck`, `HostbasedAcceptedAlgorithms`, `HostbasedAuthentication`, `HostbasedUsesNameFromPacketOnly`, `IgnoreRhosts`, `Include`, `IPQo`, `KbdInteractiveAuthentication`, `LogLevel`, `MaxAuthTries`, `MaxSessions`, `PAMServiceName`, `PermitEmptyPasswords`, `PermitListen`, `PermitOpen`, `PermitRootLogin`, `PermitTT`, `PermitTunnel`, `PermitUserR`, `PubkeyAcceptedAlgorithms`, `PubkeyAuthentication`, `PubkeyAuthOptions`, `RefuseConnection`, `RekeyLimit`, `RevokedKeys`, `SetEnv`, `StreamLocalBindMask`, `StreamLocalBindUnlink`, `TrustedUserCAKeys`, `UnusedConnectionTimeout`, `X11DisplayOffset`, `X11Forwarding`, `X11UseLocalhost`

Per-User Restriction
----
Per-user restrictions (the classic).

Why it’s popular: Granular control without splitting configs or running multiple daemons.

Typical uses of `Match User`:

* Disable port forwarding for specific users
* Force commands for service accounts
* Chroot or jail a single user

Example

```ssh
Match User backup
    ForceCommand /usr/local/bin/backup-wrapper
    PermitTTY no
    AllowTcpForwarding no
```

Group-based access control
----

Why it’s popular: Scales cleanly with LDAP/AD/Unix groups.

Typical uses:

* Different policies for admins vs normal users
* Lock down contractors
* Restrict legacy access paths

Example:

```ssh
Match Group admins
    AllowTcpForwarding yes
    PermitRootLogin prohibit-password

Match Group contractors
    AllowTcpForwarding no
    X11Forwarding no
```

Locking down automation / service accounts
----

Why it’s popular: Service users are high-risk and frequently abused.

Typical uses:

* No shell access
* No TTY
* No agent, X11, or port forwarding
* Forced command only

Example:

```ssh
Match User git,deploy,ci
    ForceCommand /usr/bin/git-shell
    PermitTTY no
    AllowAgentForwarding no
    X11Forwarding no
```

Network- or host-based policy differences
----

Why it’s popular: Different trust levels for internal vs external access.

Typical uses:

* Stronger controls from untrusted networks
* Allow forwarding only from VPN ranges
* Reduce attack surface on public-facing IPs

Example:

```ssh
Match Address 10.0.0.0/8,192.168.0.0/16
    AllowTcpForwarding yes

Match Address 0.0.0.0/0
    AllowTcpForwarding no
```

Authentication method enforcement
----

Why it’s popular: Step-up security without breaking legacy access everywhere.

Typical uses:

* Require MFA for privileged users
* Allow passwords only from specific networks
* Force key-only auth for admins

Example:

```ssh
Match Group sudo
    AuthenticationMethods publickey,keyboard-interactive

Match User legacyuser
    AuthenticationMethods password
```

Per-subnet SSH feature throttling
----

Why it’s used: Internal networks are trusted; everything else is “minimum viable SSH”.

Example:

```ssh
Match Address 172.16.0.0/12
    X11Forwarding yes
    AllowAgentForwarding yes

Match Address 0.0.0.0/0
    X11Forwarding no
    AllowAgentForwarding no
```

Read-only / observation access
----

Why it’s used: Auditors, SOC, and compliance users need access but must not change anything.

Example:

```ssh
Match Group auditors
    ForceCommand /usr/bin/readonly-shell
    PermitTTY yes
    AllowTcpForwarding no
```

Rate-limiting “expensive” SSH usage
----

Why it’s used: SSH tunnels and multiplexed sessions can chew resources.

Example:

```ssh
Match Group heavyusers
    MaxSessions 2
    ClientAliveInterval 60
    ClientAliveCountMax 2
```


Conditional environment exposure
----

Why it’s used: Some tools depend on environment variables; others shouldn’t see them.

Example:

```ssh_config
Match User buildbot
    AcceptEnv CI_* BUILD_*
    SetEnv BUILD_MODE=noninteractive
```

Safety rails for bastion / jump hosts
----

Why it’s used: Jump hosts are prime targets and should be tightly constrained.

Example:

```ssh
Match All
    PermitRootLogin no
    AllowTcpForwarding local
    GatewayPorts no
    LogLevel VERBOSE
```


Honorable mentions (very common too)
----

Chroot SFTP users

```ssh
Match Group sftp
    ChrootDirectory /sftp/%u
    ForceCommand internal-sftp
```


Emergency lockout / kill switch

```ssh
Match All
    RefuseConnection yes
```

Compliance Setups
====

PCI DSS v4.0
----
Compliance with PCI 8.1.2 and PCI DSS v4.0:

```sshd_config
# PCI 8.1.2: Restrict remote root access
Match User root
    PermitRootLogin no

Match User git
    ForceCommand /usr/bin/git-shell
    PermitTTY no

# PCI 8.4: Idle session timeout
Match Group heavyusers
    MaxSessions2
    ClientAliveInterval 60
    ClientAliveCountMax 0

# PCI 8.5.2: Separate administrative users, key-only auth
Match Group admins
    AuthenticationMethods publickey

```


CIS Benchmark v8
----
Compliance with CIS Benchmark v8:
```sshd_config
# CIS 1.1.1: Disable root login
Match User root
    PermitRootLogin no

# CIS 5.2: Key-only authentication for privileged users
Match Group sudo
    AuthenticationMethods publickey

# CIS 4.1: Restrict SSH access by IP
Match Address 10.0.0.0/8
    AllowTcpForwarding yes
    X11Forwarding yes

Match Address 0.0.0.0/0
    AllowTcpForwarding no
    X11Forwarding no

# CIS 6.1
Match User git
    ForceCommand /usr/bin/git-shell
    PermitTTY no

# CIS 6.1/6.2: Chroot SFTP users
Match Group sftp
    ChrootDirectory /sftp/%u
    ForceCommand internal-sftp

# CIS 5.5: Auditors read-only access
Match Group auditors
    ForceCommand /usr/bin/readonly-shell

```

NIST
----
Compliance with NIST SP 800-53:

```sshd_config
# AC-7: Limit unsuccessful logon attempts
Match Group sudo
    MaxAuthTries 3
    AuthenticatonMethods publickey

# AC-17: Remote access by network
Match Address 10.0.0.0/8
    AllowTcpForwarding yes

# AC-17: Default access by network
Match Address 0.0.0.0/0
    AllowTcpForwarding no

# AU-2: Enable audit info for specific users
Match Group auditors
    ExposeAuthInfo yes
    ForceCommand /usr/bin/readonly-shell

# AC-6: Least privilege for service accounts
Match User git
    ForceCommand /usr/bin/git-shell
    PermitTTY no
    AllowAgentForwarding no
```

ISO
----
Compliance with ISO 27001:

```sshd_config
# A.9.2: Restrict access by group
Match Group developers
    AllowTcpForwarding yes
    X11Forwarding yes

# A.9.4.1: Force key authentication for privileged users
Match Group sudo
    AuthenticationMethods publickey

# A.9.4.3: Limit root privileges
Match User root
    PermitRootLogin no
    PermitTTY no

# A.9.4: Auto-terminate idle sessions
Match Group heavyusers
    # A.9.4.4 User session management
    MaxSessions 2

    # ISO 27001 A.9.4
    ClientAliveInterval 300

    # ISO 27001 A.9.4.1 - Secure Log-in Procedure
    ClientAliveCountMax 2
```

Conclusion
====
Most Match usage falls into one of these buckets:

* Who (User / Group)
* From where (Address / Host)
* How (AuthenticationMethods)
* What they can do (Forwarding / Commands / TTY)

These examples still fall into the same four mental buckets, just applied more creatively:

* Trust boundary (network, bastion, subnet)
* User intent (human vs automation vs audit)
* Resource protection (sessions, keepalives)
* Data exposure control (env vars, forwarding)

