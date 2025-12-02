title: OpenSSH Environment Variables (v8.8)
date: 2022-03-14 13:19
status: published
tags: OpenSSH, ssh, environment variables
category: research
summary: List of OpenSSH Environment Variables (v8.8p1)
lang: en
private: False

I have compiled a list of shell environment variable names
used by OpenSSH v8.8.

Environment variables used in OpenSSH (8.8p1)
as references by static getenv(3) function and supplemented by
my code reviews.

SSH client (shell session)
====
For the OpenSSH client, the list of environment variables are:
[jtable]
Env. varname, description, type, source
`AUTHSTATE`, IBM AIX only; used in place of `/etc/environment`, filespec, session.c
`DISPLAY`, the default host/ display number/ and screen of the current desktop session; The DISPLAY variable indicates the location of the X11 server.  It is automatically set by ssh to point to a value of the form “hostname:n” where “hostname” indicates the host where the shell runs and ‘n’ is an integer ≥ 1.  ssh uses this special value to forward X11 connections over the secure channel.  The user should normally not set DISPLAY explicitly as that will render the X11 connection insecure (and will require the user to manually copy any required authorization cookies)., <host>:<display-id>.<screen-id>, channels.c mux.c readpass.c readpass.c ssh.c
`KRB5CCNAME`, the absolute path of the Kerberos5 user credential cache., filepath, session.c, sshd.c
`HOME`, the path of the user home directory as specified by the password database, filepath, sshconnect.c
`LANG`, the locale of the OS system, locale category, misc.c
`PATH`, a set of directories where executable programs are located, list of filepaths, session.c
`SHELL`, The file path to the user's shell executable image as specified by the password database., filepath, readconf.c sftp.c ssh-agent.c sshconnect.c
`SSH_ASKPASS`, If ssh needs a passphrase then it will read the passphrase from the current terminal if it was run from a terminal.  If ssh does not have a terminal associated with it but `DISPLAY` and `SSH_ASKPASS` are set then it will execute the program specified by `SSH_ASKPASS` and open an X11 window to read the passphrase.  This is particularly useful when calling ssh from a .xsession or related script.  (Note that on some machines it may be necessary to redirect the input from /dev/null to make this work.) set by user; a filepath to the Ask Password executable program/script, filepath, readpass.c
`SSH_ASKPASS_ENV`, alternative to `SSH_ASKPASS`, filepath, readpass.c
`SSH_ASKPASS_REQUIRE`, Allows further control over the use of an askpass program.  If this variable is set to “never” then ssh will never attempt to use one.  If it is set to "prefer" then ssh will prefer to use the askpass program instead of the TTY when requesting passwords.  Finally if the variable is set to "force" then the askpass program will be used for all passphrase input regardless of whether `DISPLAY` is set., 'never' or 'prefer', readpass.c
`SSH_ASKPASS_REQUIRE_ENV`, alternative to `SSH_ASKPASS_REQUIRE`, filepath, readpass.c
`SSH_PKCS11_HELPER`, Used with HMS vault, filepath, ssh-pkcs11-client.c
`SSH_SK_HELPER`, Security Key helper binary file for use with FIDO2 or U2F security keys.  Typically found in `~/openssh/libexec/ssh-sk-helper`, filepath, ssh-sk-client.c
`SSH_SOCKS_SERVER`, SOCKS firewall connection info; set by the SSH user before ssh(1) is called, string,
`TERM`, The TERM environment variable is used for terminal handling. It lets DB-Access (and other character-based applications) recognize and communicate with the terminal that you are using., `tty_name`, mux.c ssh.c
`TMPDIR`, `TMPDIR` is the canonical environment variable in Unix and POSIX that should be used to specify a temporary directory for scratch space. Most Unix programs will honor this setting and use its value to denote the scratch area for temporary files instead of the common default of `/tmp` or `/var/tmp`., dirpath, misc.c
`TZ`, Tells what timezone you're in., 3-char timezone string, auth-pam.c session.c
[/jtable]

SSH server (daemon)
====
For the OpenSSH server, the list of environment variables are:
[jtable]
Env. varname, description, type, source
`KRB5CCNAME`, the absolute path of the Kerberos5 user credential cache., filepath, session.c, sshd.c
`SSH_CONNECTION`, Identifies the client and server ends of the connection.  The variable contains four space-separated values: client IP address and client port number and server IP address and server port number. SSH client and server socket connection info; set by the sshd(8) daemon, string, sftp-server.c
`SHELL`, The file path to the user's shell executable image as specified by the password database., filepath, readconf.c sftp.c ssh-agent.c sshconnect.c
[/jtable]

SSH agent (daemon)
===
For the OpenSSH agent, the list of environment variables are:
[jtable]
Env. varname, description, type, source
`SHELL`, The file path to the user's shell executable image as specified by the password database., filepath, readconf.c sftp.c ssh-agent.c sshconnect.c
`SSH_AGENTPID_ENV_NAME`, Name of the environment variable containing the process ID of the authentication agent., process ID, ssh-agent.c
`SSH_AUTHSOCKET_ENV_NAME`, Name of the environment variable containing the pathname of the authentication socket., filepath, authfd.c
`SSH_AUTH_SOCK`, Identifies the path of a UNIX-domain socket used to communicate with the agent. Passed to SSH user, UNIX socket path,
[/jtable]

SSH keygen (CLI)
===
For the `keygen` utility, the list of environment variable are:
[jtable]
Env. varname, description, type, source
`SSH_SK_PROVIDER`, Security Key helper binary file for use with FIDO2 or U2F security keys.  Typically found in `~/openssh/libexec/libsk-libfido2`, filepath, ssh-add.c ssh-keygen.c
`SSH_SK_HELPER`, Security Key helper binary file for use with FIDO2 or U2F security keys.  Typically found in `~/openssh/libexec/ssh-sk-helper`, filepath, ssh-add.c ssh-keygen.c
[/jtable]

Add SSH ssh-add(1) (CLI)
====
For the `ssh-add` utility, the list of environment variable are:

[jtable]
Env. varname, description, type, source
`SSH_SK_HELPER`, Security Key helper binary file for use with FIDO2 or U2F security keys.  Typically found in `~/openssh/libexec/libsk-libfido2`, filepath, ssh-add.c ssh-keygen.c
[/jtable]

SSH session forwarder
====
For the OpenSSH session forwarder, the list of environment variable are:
[jtable]
Env. varname, description, type, source
`DISPLAY`, the default host/ display number/ and screen of the current desktop session, string, channels.c mux.c readpass.c readpass.c ssh.c
`HOME`, the path of the user home directory as specified by the password database, filepath, sshconnect.c
`LOGIN`, UNIX user name; used only on IBM AIX, string, session.c
`LOGNAME`, Synonym for USER; set for compatibility with systems that use this variable., string, session.c
`KRB5CCNAME`, MIT Kerberos 5 session name; only used in KRB5 environment, string, session.c
`MAIL`, Set to the filepath of a user local inbox for UNIX Maildir system, filepath or directory path, session.c
`PATH`, a set of directories where executable programs are located, list of filepaths, session.c
`SSH_CLIENT`, (deprecated) SSH client connection socket info; set by the sshd(8) daemon, string, session.c
`SSH_CONNECTION`, Identifies the client and server ends of the connection.  The variable contains four space-separated values: client IP address and client port number and server IP address and server port number. SSH client and server socket connection info; set by the sshd(8) daemon, string, session.c
`SSH_ORIGINAL_COMMAND`, This variable contains the original command line if a forced command is executed.  It can be used to extract the original arguments.; set by the sshd(8) daemon, string, session.c
`SSH_TTY`, This is set to the name of the tty (path to the device) associated with the current shell or command.  If the current session has no tty, this variable is not set.  Set by the sshd(8)., string, session.c
`SSH_TUNNEL`,  Optionally set by sshd(8) to contain the interface names assigned if tunnel forwarding was requested by the client., string, session.c
`SSH_USER_AUTH`, Optionally set by sshd(8) this variable may contain a pathname to a file that lists the authentication methods successfully used when the session was established including any public keys that were used., string, session.c
`SUPATH`, a set of directories where executable programs are located from a superuser shell, list of filepaths, session.c
`TERM`, UNIX terminal device name, string, session.c
`TZ`, UNIX timezone, string, session.c
`UMASK`, UNIX file permission mask, 4-digit octal, session.c
`USER`, Set to the name of the user logging in., string, session.c
[/jtable]
