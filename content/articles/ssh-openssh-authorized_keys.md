title: `authorized_keys` file for OpenSSH
date: 2022-03-24 07:36
status: published
tags: OpenSSH
category: research
summary: What goes into an `authorized_keys` file for OpenSSH?
slug: openssh-file-authorized_keys
lang: en
private: False

OpenSSH can hold the private keys in which to enable end-user to move about via publickey-authentication.


`authorized_keys` file is a text-based file that contains public keys and its accompanied notations.

The file is optional and is located in two places:

1. `/etc/ssh/authorized_keys` for system-wide/box-wide usage.
2. `$HOME/.ssh/authorized_keys` for specific user only.

Both files are used in the order listed above.

`authorized_keys` file contains public keys, one on each line/row, along with its options.

    options,  keytype,  base64-encoded-key,  comment

UNIX newline is used for EOL markers.  Use `dos2unix` utility to convert as needed.

Whitespace is used to separate the values between each columns.


Options column in `authorized_keys`
===================================
The available options are:

[jtable]
option, description, OpenSSH, Testia, IBM
`command="cmd"`, Forces a command to be executed when this key is used for authentication. This is also called command restriction or forced command. The effect is to limit the privileges given to the key; and specifying this options is often important for implementing the principle of least privilege. Without this option; the key grants unlimited access as that user including obtaining shell access.  It is a common error when configuring SFTP file transfers to accidentally omit this option and permit shell access., y, y, y
`environment="NAME=value"`, Specifies an environment variable and its value to be added to the environment before executing shell or command., y, y, y
`from="pattern-list"`, Specifies a source restriction or from-stanza; restricting the set of IP addresses; or host names from which the reverse-mapped DNS names from which the key can be used.<p>The patterns may use * as wildcard; and may specify IP addresses using * or in CIDR address/masklen notation. Only hosts whose IP address or DNS name matches one of the patterns are allowed to use the key.<p>  More than one pattern may be specified by separating them by commas. An exclamation mark ! can be used in front of a pattern to negate it., y, y, y
`no-agent-forwarding`, Prevents forwarding the SSH authentication agent., y, y, y
`no-port-forwarding`, Prevents port forwarding for connections using this key. This can be important for; such as keys intended to be used only with SFTP file transfers.  Forgetting to disable port forwarding can allow SSH tunneling to be performed using keys only intended for file transfers., y, y, y
`no-pty`, Prevents allocation of a pseudo-tty for connections using the key., y, y, y
`no-user-rc`, Disables execution of .ssh/rc when using the key., y, y, y
`no-x11-forwarding`, Prevents X11 forwarding., y, y, y
`permitopen="host:port"`, Limits port forwarding only to the specified port on the specified host. * as port allows all ports. More than one host and port can be specified using commas., y, NO, y
`principals="principals"`, On a cert-authority line this specifies which users (principal name in proprietary OpenSSH certificates) can log in using their certificate. Use of this option (or cert-authority) is not recommended as it makes impossible to audit (by inspecting the server) how many different keys grant access as that user; and OpenSSH certificate authorities are not generally very secure., y, y, y
`tunnel="n"`, Specifies a tunnel device number to be used if the client requests IP packet tunneling after logging in using a key with this option. IP tunneling is a rarely used option; but can enable full [VPN access to the internal network over SSH., y, NO, y

`cert-authority`, Indicates that the key should be trusted as a certificate authority to validate proprietary OpenSSH certificates for authenticating as that user. We strongly recommend against using this option; using OpenSSH certificates for user authentication makes it impossible to audit who has access to the server by inspecting server configuration files; and no trustworthy OpenSSH certificate authority exists., y, y, NO
`zos-key-ring-label= "KeyRingOwner/KeyRingName label"`, Specifies the key ring owner; key ring name; and the certificate label within the key ring on the OpenSSH server that contains the user's public key. One or more blanks separate the key ring (real or virtual) name from the certificate label. Certificate labels can contain embedded blanks. The option value must be enclosed in double quotes. Key fields following the options (on the same line) are ignored., NO, NO, y
[/jtable]

Pattern String Modifier for Options
-----------------------
The following string modifier notation can be used only within the `options` column:

* `%D` is the user's home directory
* `%U` is the user's login name; expands to domain.user with Windows domain users.
* `%IU` is the user's user ID (uid); not supported on Windows
* `%IG` is the user's group ID (gid); not supported on Windows

Key Types column
================

Available key types are:

* `sk-ecdsa-sha2-nistp256@openssh.com`
* `ecdsa-sha2-nistp256`
* `ecdsa-sha2-nistp384`
* `ecdsa-sha2-nistp521`
* `sk-ssh-ed25519@openssh.com`
* `ssh-ed25519`
* `ssh-dss`  (not recommended)
* `ssh-rsa`  (not recommended)

Base64 Public Key column
========================
The third column provides the public key encoded in [base64](https://datatracker.ietf.org/doc/html/rfc4648#section-4).

Comment column
==============
The fourth and last column holds the comments that the CA administrator, system administrator or end-user may provide.

Tab and space may be used for this (last) comment column.

Example
=======
And example of the `authorized_keys` file:

```bash
# Comments allowed at start of line
ssh-rsa AAAAB3Nza...LiPk== user@example.net 
from="*.sales.example.net,!pc.sales.example.net" ssh-rsa AAAAB2...19Q== john@example.net
command="dump /home",no-pty,no-port-forwarding ssh-dss AAAAC3...51R== example.net
permitopen="192.0.2.1:80",permitopen="192.0.2.2:25" ssh-dss AAAAB5...21S==
ssh-rsa AAAA...==jane@example.net
zos-key-ring-label="KeyRingOwner/SSHAuthKeysRing uniq-ssh-rsa"
from="*.example.com",zos-key-ring-label="KeyRingOwner/SSHAuthKeysRing uniq-ssh-dsa"
```


Reference
=========
* [RFC 4648](https://datatracker.ietf.org/doc/html/rfc4648#section-4)
* [IBM zOS SSH](https://www.ibm.com/docs/en/zos/2.2.0?topic=daemon-format-authorized-keys-file)
