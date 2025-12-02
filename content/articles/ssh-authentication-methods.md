title: Valid OpenSSH `AuthenticationMethods`
date: 2021-11-18 11:00
modified: 2022-03-15 07:58
status: published
tags: OpenSSH, ssh
category: HOWTO
summary: 
lang: en
private: False

Need to know how to use the `AuthenticationMethods` in OpenSSH v7.4+.

There isn't a way ... over the network ... to list ALL the active methods of authentications of OpenSSH ... in advance … ever: You are challenged to only the first one then the next …

This is by design.  You want to know? You must look at the `/etc/ssh/sshd_config` directly on that server, if you could. Oh, you can’t? That’s security by design. 

So, I'll expand the `AuthenticationMethods` list even further as I've been code-reviewing OpenSSH for some time.

The available authentication methods are:

* `gssapi-with-mic`,
* `hostbased`,
* `keyboard-interactive`,
* `none` (used for access to password-less accounts when `PermitEmptyPassword` is enabled),
* `password` and
* `publickey`.


`AuthenticationMethods` specifies the authentication methods that must be successfully completed for a user to be granted access.  This option must be followed by one or more lists of comma-separated authentication method names, or by the single string any to indicate the default behavior of accepting any single authentication method.  If the default is overridden, then successful authentication requires completion of every method in at least one of these lists.

## Pubkey Authentication

For example:

    AuthenticationMethods publickey,password publickey,keyboard-interactive

would require the user to complete public key authentication, followed by either password or keyboard interactive authentication.  Only methods that are next in one or more lists are offered at each stage, so for this example it would not be possible to attempt password or keyboard-interactive authentication before public key.

# Keyboard Interactive Authentication

For keyboard interactive authentication it is also
possible to restrict authentication to a specific
device by appending a colon followed by the device
identifier bsdauth or PAM depending on the server
configuration.  For example:

    AuthenticationMethods keyboard-interactive:bsdauth

would restrict keyboard interactive authentication to the bsdauth device.

# Multiple Pubkey Authentication

If the publickey method is listed more than once, sshd(8) verifies that keys that have been used successfully are not reused for subsequent authentications.

For example: 

    AuthenticationMethods publickey,publickey

requires successful authentication using two different public keys.

## Note

A comma (`,`) separator symbol that separates a pair of auth options are tried together (AND-logic) firstly before any of its space separator(s). 

A whitespace (` `) separator symbol that separates one or more auth options (whose options may be joined by comma(s)) are tried separately (OR-logic).

NOTE: Colon (`:`) separator are used to restrict its accompanied authentication method to a specific authentication device pathway mechanism such as `pam`, `bsdauth`, and `skey`. For keyboard interactive authentication it is also possible to restrict authentication to a specific device by appending a colon followed by the device identifier `bsdauth`, `pam`, or `skey`, depending on the server configuration. For example, `keyboard-interactive:bsdauth` would restrict keyboard
interactive authentication to the `bsdauth` device.


Note that each authentication option listed in `AuthenticationMethods` should also have its corresponding config setting be explicitly enabled in the configuration.  For example, if `pubkey` option got used in `AuthenticationMethods` setting then it’s accompanied config line `PubkeyAuthentication on` must also be in its config file. 

## Details for code reviewers of OpenSSH

* Channel type: preauth (pre-channel)
* CLI option: -oAuthenticationMethods=XXXX"
* Process context: main
* SSH service: ssh-userauth (SSH2_MSG_USERAUTH_REQUEST)
* options.auth_methods[]/auth2_setup_methods_lists()/input_userauth_request()
* AuthenticationMethods defaults to 'any'.

