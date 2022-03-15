title: How to Set Up a Bastion SSH Server
date: 2022-04-15 06190
status: published
tags: ssh, OpenSSH
category: HOWTO
summary: A bastion SSH server allows a work-from-home user to login onto the company's internal host thus bypassing company intrusion detection system and company firewall.
lang: en
private: False


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


How Is It Different than SSH Jump Server?
-----------------------------------------
This is a marked difference from a SSH Jump Server
where a user can login onto the host and then
forward on to another (but internal) SSH server:

- a bastion host makes use of two separate SSH processes (as a security feature)
- whereas a SSH Jump host leverages a single SSH process to receive then forward a SSH connection without making a use of any local TTY device.  

The key difference here is whether such user will get drop down to a shell or not:

- Bastion, drops down to a shell (to allow use of outbound `ssh` client
- Jump, no shell, TCP connection only, one way, often one-way-only.

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

This process-forking comes with assured auditing of its activities; with SSH Forwarding, not so much.


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

For SMB (small and medium businesses), SSH clients should be forced to use their read-only keys OUTSIDE of their `\$HOME` directory.  The example `sshd_config` snippet is:

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
