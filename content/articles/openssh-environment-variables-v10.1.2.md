title: OpenSSH Environment Variables (v10.1.2)
date: 2026-01-03 13:19
status: published
tags: OpenSSH, ssh, environment variables
category: research
summary: List of OpenSSH Environment Variables (v10.1.2)
slug: openssh-environment-variables-10.1.2
lang: en
private: False

I have compiled a list of shell environment variable names used by OpenSSH v10.1.2, reflecting the changes and updates from version 8.8.

## Environment variables used in OpenSSH (10.1.2)
as referenced by static `getenv(3)` function and supplemented by code reviews.

### SSH client (shell session)
For the OpenSSH client, the list of environment variables are:

[jtable]
Env. varname, description, type, source
`AUTHSTATE`, IBM AIX only; used in place of `/etc/environment`, filespec, `session.c`
`DISPLAY`, The default host/display number and screen of the current desktop session. Set by ssh to point to a value of the form “hostname:n” for X11 forwarding., `<host>:<display-id>.<screen-id>`, `channels.c` `mux.c` `readpass.c` `ssh.c`
`KRB5CCNAME`, The absolute path of the Kerberos5 user credential cache., filepath, `session.c`, `sshd.c`
`HOME`, The path of the user home directory as specified by the password database., filepath, `sshconnect.c`
`LANG`, The locale of the OS system., locale category, `misc.c`
`PATH`, A set of directories where executable programs are located., list of filepaths, `session.c`
`SHELL`, The file path to the user's shell executable image as specified by the password database., filepath, `readconf.c` `sftp.c` `ssh-agent.c` `sshconnect.c`
`SSH_ASKPASS`, If ssh needs a passphrase, it will execute the program specified by `SSH_ASKPASS` to open an X11 window for passphrase input., filepath, `readpass.c`
`SSH_ASKPASS_ENV`, Alternative to `SSH_ASKPASS`, filepath, `readpass.c`
`SSH_ASKPASS_REQUIRE`, Controls use of the askpass program. Can be set to `never`, `prefer`, or `force`., 'never' or 'prefer', `readpass.c`
`SSH_ASKPASS_REQUIRE_ENV`, Alternative to `SSH_ASKPASS_REQUIRE`, filepath, `readpass.c`
`SSH_PKCS11_HELPER`, Used with HMS vault., filepath, `ssh-pkcs11-client.c`
`SSH_SK_HELPER`, Security Key helper binary file for FIDO2 or U2F security keys., filepath, `ssh-sk-client.c`
`SSH_SOCKS_SERVER`, SOCKS firewall connection info, set by the SSH user before ssh(1) is called., string, 
`TERM`, The terminal handling environment variable., `tty_name`, `mux.c` `ssh.c`
`TMPDIR`, Specifies a temporary directory for scratch space., dirpath, `misc.c`
`TZ`, Specifies the timezone., 3-char timezone string, `auth-pam.c` `session.c`
`WAYLAND_DISPLAY`, The default host/display number and screen of the current desktop session. Set by ssh to point to a value of the form “hostname:n” for X11 forwarding., `<host>:<display-id>.<screen-id>`, `channels.c` `mux.c` `readpass.c` `ssh.c`
[/jtable]

### SSH server (daemon)
For the OpenSSH server, the list of environment variables are:

[jtable]
Env. varname, description, type, source
`KRB5CCNAME`, The absolute path of the Kerberos5 user credential cache., filepath, `session.c`, `sshd.c`
`SSH_CONNECTION`, Identifies the client and server ends of the connection. Contains client IP, client port, server IP, and server port., SSH client and server socket info, `sftp-server.c`
`SHELL`, The file path to the user's shell executable image as specified by the password database., filepath, `readconf.c` `sftp.c` `ssh-agent.c` `sshconnect.c`
[/jtable]

### SSH agent (daemon)
For the OpenSSH agent, the list of environment variables are:

[jtable]
Env. varname, description, type, source
`LISTEN_FDS`, File descriptior, integer, `ssh-agent.c`
`LISTEN_PID`, UNIX process ID, process ID integer, `ssh-agent.c`
`SHELL`, The file path to the user's shell executable image as specified by the password database., filepath, `readconf.c` `sftp.c` `ssh-agent.c` `sshconnect.c`
`SSH_AGENTPID_ENV_NAME`, Name of the environment variable containing the process ID of the authentication agent., process ID, `ssh-agent.c`
`SSH_AUTHSOCKET_ENV_NAME`, Name of the environment variable containing the pathname of the authentication socket., filepath, `authfd.c`
`SSH_AUTH_SOCK`, Identifies the path of a UNIX-domain socket used to communicate with the agent. Passed to SSH user., UNIX socket path, 
[/jtable]

### SSH keygen (CLI)
For the `keygen` utility, the list of environment variables are:

[jtable]
Env. varname, description, type, source
`SSH_SK_PROVIDER`, Security Key helper binary file for FIDO2 or U2F security keys., filepath, `ssh-add.c` `ssh-keygen.c`
`SSH_SK_HELPER`, Security Key helper binary file for use with FIDO2 or U2F security keys., filepath, `ssh-add.c` `ssh-keygen.c`
[/jtable]

### Add SSH ssh-add(1) (CLI)
For the `ssh-add` utility, the list of environment variables are:

[jtable]
Env. varname, description, type, source
`SSH_SK_HELPER`, Security Key helper binary file for use with FIDO2 or U2F security keys., filepath, `ssh-add.c` `ssh-keygen.c`
[/jtable]

### SSH session forwarder
For the OpenSSH session forwarder (used by `sftp`, `sctp`, and `ssh`), the list of environment variables are:

[jtable]
Env. varname, description, type, source
`DISPLAY`, The default host/display number and screen of the current desktop session., string, `channels.c` `mux.c` `readpass.c` `ssh.c`
`HOME`, The path of the user home directory as specified by the password database., filepath, `sshconnect.c`
`LOGIN`, UNIX user name (used only on IBM AIX)., string, `session.c`
`LOGNAME`, Synonym for `USER`, set for compatibility with systems that use this variable., string, `session.c`
`KRB5CCNAME`, MIT Kerberos 5 session name (only used in KRB5 environment)., string, `session.c`
`MAIL`, Set to the filepath of a user local inbox for UNIX Maildir system., filepath or directory path, `session.c`
`PATH`, A set of directories where executable programs are located., list of filepaths, `session.c`
`SSH_CLIENT`, **Deprecated**: SSH client connection socket info., string, `session.c`
`SSH_CONNECTION`, Identifies the client and server ends of the connection. Contains four space-separated values: client IP, client port, server IP, server port., SSH client and server socket connection info, `session.c`
`SSH_ORIGINAL_COMMAND`, Contains the original command line if a forced command is executed., string, `session.c`
`SSH_TTY`, The name of the tty (path to the device) associated with the current shell or command., string, `session.c`
`SSH_TUNNEL`, Optionally set by `sshd` to contain the interface names assigned if tunnel forwarding was requested by the client., string, `session.c`
`SSH_USER_AUTH`, Optionally set by `sshd`; may contain a pathname to a file listing the authentication methods successfully used during session establishment., string, `session.c`
`SUPATH`, A set of directories where executable programs are located from a superuser shell., list of filepaths, `session.c`
`TERM`, UNIX terminal device name., string, `session.c`
`TZ`, UNIX timezone., string, `session.c`
`UMASK`, UNIX file permission mask., 4-digit octal, `session.c`
`USER`, Set to the name of the user logging in., string, `session.c`
[/jtable]
