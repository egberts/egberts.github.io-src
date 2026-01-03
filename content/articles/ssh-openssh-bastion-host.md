title: How to Set Up a Bastion SSH Server
date: 2022-03-15 0619
modified: 2026-01-03 04:38
status: published
tags: ssh, OpenSSH
category: HOWTO
summary: A bastion SSH server allows a work-from-home user to login onto the company's internal host thus bypassing company intrusion detection system and company firewall.
lang: en
private: False

The following are the best practices while configuring a bastion host

1. Never place your SSH private keys within a bastion hosts/ server. As suggested, use SSH Agent Forwarding for this task to connect first to the bastion host then to other instances on the private subnets. This lets you keep the private keys only with your servers.
2. Make sure the security group on the bastion host to allow SSH (port 22) to connect only from your trusted hosts and never from 0.0.0.0/0 mask
3. Always have more than one bastion. For example, having a bastion host for each Availability Zone (AZ).
4. Make sure to configure security groups on private subnets to accept SSH traffic only from the bastion hosts.

SSH Bastion Server is the most secured of any SSH server configuration: SSH Jump Server or SSH Proxy Server are most useful when used within the enterprise network or non-Internet part of your network (e.g. homeLAN, small-medium-business network).

Well, maybe except for the proprietary Cloudflare SSH server which also boast secured logging of any and all SSH commands that goes through such an SSH bastion server.

Typical interaction with an SSH bastion server:


Step 1: Adding the private key (PEM file) to the keychain. This allows the user to access the private instances without copying to the bastion host. This adds additional layer of security.
```console
$ ssh-add -k <PEM_file_name>
```
Step 2: Check whether the private key is properly added to the keychain
```console
$ ssh-add -L
```
The above will list all the keys added to the chain. Check whether the key you added is listed there.

Step 3: Access the Bastion Host (Public instance)
```console
$ ssh -A [email protected]<bastion-host-elastic-ip>
```
[Here ec2-user is the user for the Linux instance]

Step 4: Access the private instance
```console
$ ssh [email protected]<private-instance-ip>
```

How to Set Up a Bastion SSH Host
================================
A bastion server host allows user to login onto the
host and then can do one of the following:

* perform some local work within that bastion host OR
* perform an outbound SSH session using ssh(1) to elsewhere.

A bastion SSH server has both capabilities but predominately only has exactly one of those capability enable.  

Example Usages of Bastion SSH
==============
Some example uses of bastion SSH server are:

* Inbound-from-Internet pubkey'd SSH connection for carefully-constrained local work:
* * Automated send messaging
* * * Instant Messaging (Stack, XMPP, Matrix, Telegram)
* * * Internet Relay Chat
* * Automated retrieval
* * * Network Management System (NMS)
* * * SNMP
* * On-demand system-administration-related activity
* Outbound-to-Internet pubkey'd SSH connection for audit purpose of corporate external activities
* * System-admin remote site maintenance


How Is It Different from SSH Jump Server?
-----------------------------------------
A Jump Server is intended to breach the gap between two security zones.
The intended purpose here is to have a gateway to access something inside the security zone, from the DMZ.

SSH Jump Server is
where a user can log in onto the host and then
forward on to another (but internal) SSH server.


The key difference here is whether such an SSH user will get drop to a shell or not:

- bastion host gets user a shell, and makes use of two separate SSH processes (as a security feature).  This is the only (yet extremely powerful) way to get to be able to use an `ssh` client.
- jump host gets no shell, by leveraging a single SSH process to receive then forward an SSH connection without making a use of any local TTY device.  Downside is that there is often poor auditing of internal SSH connections being multiplexed through its main SSH TCP connection.


Audit, Logging, Compliance
==========================
In all cases, the bastion SSH server have a separate disk partition for all activity logging including:

* Successful/Attempted/Failed authentications
* Forwarding connections attempted/failed/successes.

Tracking SSH Forwarding
=======================
Primary purpose of bastion SSH server is to have its
main SSH daemon do that extra process-forking of a new 
SSH user session with each inbound SSH connection.

This process-forking comes with assured auditing of its SSH-multiplexed activities; doing this with SSH Forwarding, not so much.


SSH Daemon Configuration
========================
Bastion SSH host only allows
SSH connection with following `sshd_config` settings:

- `PermitOpen <allowed_public_IP>:2222`
- `PermitTunnel no`
- `AllowTcpForwarding yes`
- `X11Forwarding no`
- `AllowAgentForwarding no`
- `PermitTTY no`
- `ForceCommand echo 'Nope'`
- `GatewayPorts none`

And bastion server must not open nor serve any other network ports than the SSH port itself.

For SMB (small and medium businesses), SSH clients should be forced to use their read-only keys OUTSIDE their `\$HOME` directory.  The example `sshd_config` snippet is:

- `AuthorizedKeysFile /etc/ssh/keys/%u`

When a user named 'Bob' attempts the shell command `ssh somewhere.tld`, `sshd` daemon will consult the `/etc/ssh/keys/Bob` for its public key for its Pubkey SSH authentication approach.

This `AuthorizedKeysFile` method eases the SMB system administrator's duty to the quickest lockout by a simple removal of the targeted user's key file.

After the above setup is deployed, this allows for an easy log-through from outside world to one of your internal host with the following command:

    ssh -J finaluser@finalhost bastionuser@bastion.domain.tld

OS Configuration for Bastion SSH 
================================
Also it is prudent that this dedicated bastion host's OS should also 
have the following attributes:

- Shell(s) re-compiled without any built-ins
- No `sudo` binary
- Root account disabled
- Read-only Root filesystem
- No user home directory
- No coreutils 
- Separate disk partition for /var/log (Common Criteria)
- OSSEC/Tripwire/audit/SELinux
- Email outlet for alerts
- Templates are destroyed and rebuilt every 8 hours

Enjoy.


References
==========

* 
