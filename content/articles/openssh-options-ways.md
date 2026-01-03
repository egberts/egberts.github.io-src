title: Adding An Option to an SSH client OR SSH session using OpenSSH?
date: 2022-05-03 05:10
modified: 2026-01-03T0328
status: published
tags: SSH, OpenSSH
category: HOWTO
summary: What are the different ways to use or see an option toward an SSH client using OpenSSH, whether it is at a command line before startup or during an existing SSH session?
slug: ssh-openssh-options-ways
lang: en
private: False

# Methods
There are several methods for an end-user to pass a specific option 
setting for a new or existing SSH session.

1. Command Line Interface (CLI)
2. Configuration File
3. SSH Control Sequence Code

The variable name of all option setting commands in OpenSSH are case-insensitive (upper or lower case): For example, `VerifyHostKeyDNS` and `verifyhostkeydns` are exactly alike.  Only the CLI options remain sensitive to case (`-g` is not same as `-G`).

# Command Line Interface (CLI)

At the command line, option `-o` is one way to try out an SSH setting in question before deciding into making it a permanent setting:

```console
$ ssh -oServerAliveInterval=60 host.domain.tld
# type nothing for 1 minute and watch it disconnect

$
```
The above example demonstrate a temporary passing of `serveraliveinterval=60`,
which is 60 seconds, if no data has been received 
from the server, ssh(1) will send a message 
through the encrypted channel to request a 
response from the server.  The default is 0, 
indicating that these messages will not be sent 
to the server.

If an SSH setting is desired to be made more permanent, 
there are various more ways to do this.

# Configuration File

Configuration file for SSH client/server is the only way to make a setting
permanent and makes for a shorter CLI usage (no lengthy `-o` setting).

The nesting methods of adding to config are separated by client or server:

SSH Client

* by scope 
  * by directory/files  
    * by pattern `Match`ing  

SSH Server

* by directory/files  (both client/server)
  * by pattern `Match`ing  (both client/server)

Despite similarity between server/client in nesting methods above, it is
strictly a generalization ... by design, for none of specific SSH setting work 
for both the client and the server;  a setting is keyed and named
for either the server-side or client-side.

For ease of reading this article, we start with most common side 
of SSH protocol, the client-side.

Both sides share many similar uses of incorporating a setting.

## By Scope - SSH Client Configuration 

For the client-side only, the first way is to decide whether 
such a permanent setting is for the:

* default user 
* system-wide
  * specific user

### Default User - By Scope - Client

For the default user, this is the username of this login session.  
Username can be identified by echoing the shell `$USER` environment name.

File `$HOME/.ssh/config` is where all settings for its user are being
held.  

This config will only impact `$USER` user and not affect any other users.

An example setting of `$HOME/.ssh/config`:
```ssh
# Settings for all connections

HashKnownHosts yes
FingerprintHash sha256

# End of settings for all connections

Host github.com
    Hostname github.com
    PubkeyAcceptedKeyTypes ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,ssh-ed25519,ssh-ed25519-cert-v01@openssh.com
    IdentityFile ~/.ssh/id_ecdsa

Host gitlab.com
    Hostname gitlab.com
    IdentityFile ~/.ssh/id_ed25519_gitlab_com.privkey

# Project-specific stuffs
Include ~/.ssh/config.project-wfh
Include ~/.ssh/config.project-spooler
Include ~/.ssh/config.project-whirlpool

# Settings to counteract any includes above
AddressFamily inet

# 'Match All' is always the last one
Match All 
    UseRoaming no
```

### System-Wide - By Scope - Client 

System-wide applies toward all users on this host. System-wide settings
go into `/etc/ssh/ssh_config`.

This is useful for:

* security mandates
* multiple-users
* mobile device
* laptop
* have multiple ISPs

Some examples of `/etc/ssh/ssh_config` (for OpenSSH v8.8p1+):

```ssh
# Private Security mandate
HashKnownHosts yes
FingerprintHash sha256
PubkeyAcceptedAlgorithms ssh-ed25519,ssh-ed25519-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,sk-ssh-ed25519-cert-v01@openssh.com
HostKeyAlgorithms ssh-ed25519,sk-ssh-ed25519@openssh.com,sk-ssh-ed25519-cert-v0
1@openssh.com,ssh-ed25519-cert-v01@openssh.com
KexALgorithms sntrup4591761x25519-sha512@tinyssh.org,curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group18-sha512,diffie-hellman-group16-sha512,diffie-hellman-group14-sha256
 
Match Host *.onion
    ProxyCommand socat - SOCKS4A:localhost:%h:%p,socksport=9050
    UpdateHostKeys ask
```

### Specific-User - By Scope - Client

For the specific user, add a `Match User <username_goes_here>` before the
setting in the system-wide config.  More on this `Match` later.

System admin can give specific users some specific settings by
inserting `Match User` into the system-wide config file.


File: `/etc/ssh/ssh_config`
```ssh
Match User admin
    VisualHostKey yes
```

## By Directory/Files - SSH Client

The settings can be grouped into a:

* single configuration file
* multi-file configuration

The `include` statement by OpenSSH makes possible this
 multi-file config approach. 

### Single Config - SSH Client

Since OpenSSH was first release, the `/etc/ssh/ssh_config` is that single-file
configuration approach.

### Multi-File - SSH Client

Multi-file organize settings using subdirectory(s) and multiple files.

This multi-file approach makes it possible for OTHER projects or 
packages to drop into their needed settings without being disruptive
toward the user's or system's settings.

Most popular approaches are currently used by many Linux distros:

[jtable]
directory, Protocol Side
`/etc/ssh/ssh_config.d`, SSH Client
`/etc/ssh/sshd_config.d`, SSH Server
[/jtable]

Note: I have seen other approaches, generally more convoluted and deeper-nested ones, especially for multiple projects and departments.

I provide one extreme (but clearly concise) working example of distributed settings by multi-file config in
[Easy Admin](https://github.com/egberts/easy-admin/tree/main/490-net-ssh/ssh_config.d).

## By `Match` - SSH Client

The keyword `Match` is a match criteria used to group the set of settings to.

Keyword `Match` can be found in either SSH client or server config files.

A typical layout of using `Match` given below:
```ssh
<settings for all SSH connections>

Match ...
   <settings specific to that match>

Match ...

Match all
   <a fallback, catch-all settings>
   # Useful for UN-doing any earlier settings as a security measure
```

### Match Criteria

Available criteria of `Match` are:

[jtable]
match criteria keyword, description
`host`, Fully-qualified domain name of the host. `Match host <hostname>` is the same as `Host <hostname>`
`user`, username that was passed to at the command line (CLI) interface.
`localuser`, actual username of the current shell session
`exec`, an executable that is run at `$USER` session to determine whether it returns a 0 or not before applying settings under `Match exec`.  Useful as an access control method.  One can pass on the user's public key and see if the user is authorized or not.
`originalhost`, exact name that was entered at the command line before any effort of canonicalization got applied (using the `search` domainname from `/etc/resolv.conf` and appending to the end of that CLI hostname.
`canonical`
`final`
`all`, last resort; must be the last `Match` in its config.
[/jtable]

### Negation - Match Criteria

You can add an exclamation (`!`) symbol before the Match value.

```ssh
# Company-wide settings
Match host !gateway.public.mydomain.example
    KexALgorithms curve25519-sha256@libssh.org
```    

### Match `exec`

`exec` criteria is useful for LDAP, public key checking, and other finer aspect of access control mechanism.

```ssh
Match exec "/usr/local/sbin/ssh_check_remote_priv_access.py %u"
    VisualHostKey yes
```

However, there is a better way to do authorization by known public key(s) and it is by using the `AuthorizedKeysCommand` setting.  Detail is given [here](https://jpmens.net/2019/03/02/sshd-and-authorizedkeyscommand/)


### Multiple Matches

```ssh
Match user %U
    <user-specific settings>
Match host public.gateway.domain.example
    <public-gateway settings>


include <default match-by-home-settings settings>
include <default match-by-travel-settings settings>
include <default match-by-project settings>
include <default match-by-project settings>
include <default match-by-project settings>

Match canonical
    # If `CanonicalizeHostname true`, this is the same as `Match final`
Match final
    # settings that pertains to hostnames that got changed
    #   during the parsing of client config.

Match all
    include <default corporate settings>
    include <default security settings>
    # settings that is always done
```


## By Directory/Files - SSH Server

Except for name of settings and default user, everything else is pretty
much the same for SSH server as it is in SSH client.

The system-wide and specific-user for SSH server are:

[jtable]
file specification, description
`/etc/ssh/sshd_config`, single-file config for SSH server
`/etc/ssh/sshd_config.d`, multi-file config for SSH server
[/jtable]

## By `Match` - SSH Server

Pretty much the same for SSH client, except the `Match` criteria are:

[jtable]
`Match` criteria, description
`User`, the username received by SSH server and found by `getpwd()` (typically in `/etc/passwd`).
`Group`, the groupname received by SSH server and also found by `getpwd()` (typically in `/etc/group`).
`Host`, the fully canonical hostname (complete with domain name and all).
`LocalAddress`,
`LocalPort`, the TCP port number used within this established SSH session/TCP-connection.
`RDomain`, 
`Address`, 
`All`, 
[/jtable]

### Match Criteria
### Multiple Matches


# SSH Control Sequence Code

Once an SSH session is up and running, there is a hidden menu that is accessible by your control sequence.

So, how do you start this control sequence? First, make sure "Enter" was the last key you pressed, as the SSH client won't notice the control sequence otherwise. Next, press the tilde character (shift + backtick) followed by another character.
```console
Supported escape sequences:

    ~. - terminate connection (and any multiplexed sessions)
    ~B - send a BREAK to the remote system
    ~C - open a command line
    ~R - request rekey
    ~V/v - decrease/increase verbosity (LogLevel)
    ~^Z - suspend ssh
    ~# - list forwarded connections
    ~& - background ssh (when waiting for connections to terminate)
    ~? - this message
    ~~ - send the escape character by typing it twice
    (Note that escapes are only recognized immediately after newline.)
```

There is one live active command available: "Request Rekey".  

