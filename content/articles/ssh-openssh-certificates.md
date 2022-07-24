title: PKI Certificates in OpenSSH
date: 2022-03-24 07:38
status: published
tags: OpenSSH, PKI, ssh
category: research
summary: How to create PKI certificates for use by OpenSSH
slug: ssh-openssh-certificates
lang: en
private: False

Just a couple of things:

* OpenSSL `openssl` cannot manage your SSH certificates.
* SSH certificate file format is RFC4716.  Not PEM ('`.pem`'), and not PKCS#8 ('`.pkc`').
* Selection of SSH-related CA authority is admin-definable.

Introduction to SSH Certificates
================================

Certificates are an extension to the existing ssh public-key authentication system. They can be applied to any existing public and private key pair, and can be used in addition to any authentication method currently supported by ssh.

While it’s based on public-key authentication, it’s also designed to simplify the complexity of managing keys across any number of servers. Certificates eliminate the need for `known_hosts` and `authorized_users` files, and if implemented properly, replicate their entire functionality with less management overhead.

Since certificate authentication is an extension of public key encryption, it will work with any `ssh2` key-type and key-size already supported by OpenSSH. This means that RSA, DSA, and EC will all work if they are supported by the version of OpenSSH you are working with. For the sake of simplicity, we are using default RSA-1024 for this guide.

Certificates vs. Public-Key
===========================

There are some important differences of authentication between regular public-key-based (that is commonly found in SSH authentication) and SSH certificate-based. For the most part the differences are in favor of certificate authentication.

Differences From Other Public-Key Certificate Standards
=======================================================

SSH certificates are more simplistic than other certificate formats, such as x509, PKCS#11 or PEM used in SSL (and OpenSSL):

* There is no certificate chaining. Therefore there is only one CA.
* There is no dubious commercial signing authority
* There is no trust model aside from CA signing

Host Authentication
===================
[jtable]
Operation, Public Key Authentication, Certificate Authentication
Authenticating unknown host, User is asked if they want to accept host key on initial login, Verify host-cert is signed by CA
Authenticating known host, Key compared with user’s `known_hosts` file, Verify host-cert is signed by CA
Replacing a known host’s keys, Entry must be deleted from user’s `known_hosts` file then User is asked if they want to accept new host key on login, Verify host-cert is signed by CA
Revoking a key/cert, '@revoked' line prepended to the host entry in user’s `known_hosts file`, “@revoked” line prepended to the host entry in user’s `known_hosts` file
[/jtable]

The benefits of using certificate authentication:

* Users can authenticate a host that they have never logged into before
* There is no longer a need to distribute or manage known_hosts files (such as with puppet)
* Servers can be replaced or their keys regenerated without user intervention
* Users should never be prompted to accept server-keys in the workplace unless something is wrong.
* Non-compliant hosts can be discovered by searching for unsigned hostkeys.

User Authentication
===================
[jtable]
Operation, Public Key Authentication, Certificate Authentication
Authentication, User’s public key is pulled from host-user `authorized_keys` file on each server, Check to see if user-cert is signed by CA
Expiration key/cert, Not enforced, Expiration set by administrator at time of signing
Login Username, User’s public-key placed in `authorized_keys` file for each destination user on each server, Usernames can be added to certificate at time of signing or Can also be controlled via "AuthorizedPrinciples" file on each server.
Restrictions (Port Forwarding; Force-Command; etc), Can be in `authorized_keys` file (may be edited by user) or Can be within Match User/Group block in each server’s `sshd_config`, Can be added to certificate at time of signing; or Can be within Match User/Group block on each server’s `sshd_config`; Can be added within "AuthorizedPrinciples" file on each server
Revoking a key/cert, Can be added to RevokedKeys file on each server or (and preferred) Removed from every affected `authorized_keys` file on server, Add cert to "RevokedKeys" file on each server 
Replacing a user’s cert, All affected `authorized_keys` files on each server must be edited, Add old certificate to each server’s RevokedKeys file; Sign new certificate
[/jtable]

The benefits of using certificate authentication:

* Certificates expiration can be set by administrator at time of signing, enforcing a rotation policy
* No need to manage authorized_keys files across multiple hosts
* No fear of malicious users editing or adding to unmanaged authorized_keys files
* Easier ability to restrict certain user abilities on a per-user basis at time of signing
* No need to remove revoked keys from authorized_keys files
* Users can be limited to specific usernames at time of certificate signing


Making it work

Implementing ssh certificate authentication is much easier than working with SSL certificates. The hardest part is determining whether to use a single CA key for signing users as well as servers or two CA keys — one each for server and users.

It’s recommended to use two separate keys for signing users and servers, to allow for different roles to manage each function: For example, a system administrator can sign the server keys while a security administrator can sign the user keys.

The examples below uses separate certificate authorities for servers and users.
Server Authentication

Host authentication can be enabled in as few as 4 steps!
Create Server CA

On your preferred certificate authority server run the following commands

```console
$ # Lets start with good organization
$ mkdir -p ssh_cert_authorita/server_ca
$ cd ysh_cert_authority/server_ca/

~/ssh_cert_authority/server_ca $ # Now lets generate our server certificate authority keypair
~/ssh_cert_authority/server_ca $ ssh-keygen -f server_ca -C "companyname_server_ca"
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
wour identification has been saved in server_ca.
Your public key has been saved in server_ca.pub.
The key fingerprint is:
21:f6:9f:5d:ec:75:2e:df:c0:6b:5e:9d:5b:97:d8:19 "companyname_server_ca"

~/ssh_cert_authority/server_ca $ # The resulting files
~/ssh_cert_authority/server_ca $ ls -l
total 8
-rw------- 1 username username 1675 Aug 16 14:12 server_ca
-rw-r--r-- 1 username username  409 Aug 16 14:12 server_ca.pub
```

Notes:

    It’s strongly suggested you not only use a passphrase, but also use a strong one. Anyone who signs with this key will be able to add trusted servers to your network.

# Sign Host Keys

Since certificate authentication is an extension to public key authentication, you can use the existing ssh host public keys found in /etc/ssh/ssh_host*key.pub. Any type of ssh host key will do, as long as it’s the public key rsa is only being used as an example.

On your preferred certificate authority server run the following commands

```
~/ssh_cert_authority/server_ca $ # Make a place to keep copies of host keys and certs
~/ssh_cert_authority/server_ca $ mkdir -p host_certs
~/ssh_cert_authority/server_ca $ cd host_certs

~/ssh_cert_authority/server_ca/host_certs $ # Download a hostkey from a host
~/ssh_cert_authority/server_ca/host_certs $ scp -rp example.host.net:/etc/ssh/ssh_host_rsa_key.pub example.host.net.pub
ssh_host_rsa_key.pub                                                                   100%  396     0.4KB/s   00:00    

~/ssh_cert_authority/server_ca/host_certs $ # Sign host key 
~/ssh_cert_authority/server_ca/host_certs $ ssh-keygen -s ../server_ca -I example.host.net -h -n example.host.net,96.126.102.173,2600:3c01::f03c:91ff:fe69:87a2 example.host.net.pub 
Signed host key example.host.net-cert.pub: id "example.host.net" serial 0 for example.host.net,123.45.67.89,2600:dead:beef:cafe:::87a2 valid forever

~/ssh_cert_authority/server_ca/host_certs $ # The resulting files
~/ssh_cert_authority/server_ca/host_certs $ ls -l
total 8
-rw-r--r-- 1 username username 1430 Aug 16 14:19 example.host.net-cert.pub
-rw-r--r-- 1 username username  396 Jul 14 20:19 example.host.net.pub

~/ssh_cert_authority/server_ca/host_certs $ # Copy the cert back to the server
~/ssh_cert_authority/server_ca/host_certs $ scp -rp example.host.net-cert.pub root@example.host.net:/etc/ssh/ssh_host_rsa_key-cert.pub
example.host.net-cert.pub                                                           100% 1430     1.4KB/s   00:00 
```

Notes:

Important: Keep all pubkeys and certs with the CA. If you need to revoke them, you must have a copy handy!

Important: You cannot negate the use of the options -I -h -n when creating server certificates.

The -n options must only refer to the relevant host name(s) and ip(s). A blank, wildcard, or ambiguous name will result in interchangeable server certificates.

The -I option can be any text used to identify this certificate and you do not need to follow the same format used above.

The -h designates the certificate will be a host certificate

# Server Configuration Change

```
HostCertificate /etc/ssh/ssh_host_rsa_key-cert.pub
```

Once `/etc/ssh/sshd_config` is saved, restart sshd.


# Client Configuration Change

Copy the text from `server_ca.pub` and enter into your `~/.ssh/known_hosts` (or `/etc/ssh/known_hosts`) file then prepend with the underline text shown below:

```
@cert-authority *.host.net,123.45.67.* ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDVifNRc+EN4b9g/ygWRCIvV1qw0aR33qzkutIA6C3MzHidaXe6tO4Q35YqrP2UUhOdcl2g8nO7BNSSHkjrFyEnyNqkpgHYcDzUdpE6XGS6rNcjrmLajf1CRvUBvFD0ceu//z6HL1dpE347AHSZbFxHT6NdhscdEd/Bd5c1aVyS+dUdiGX4U9YdgTN2lM8zQy5rJo+siFyHmtqXh1ZVBBC+VBF6ZPzMkxvkJmAp4eWCQJOZLIybcNZlyuXrs1bXV0X0ZIIL2j/gYC2gJPO1FUTKRcqzo/fQ/m6hAhxMMpTTgI92FiE/QOfOk5+MmgfTOqsF0us2TJ5mrSIE9o/3DQsj "companyname_server_ca"
```

Notes: Delete any existing `known_host` entries for “example.host.net”
    The file formatting follows standard `known_hosts` format, but note the wildcard matching for the entire domain and ip address range.

# Testing Server Authentication

```console
~ $ ssh -v username@example.host.net
...
debug1: Server host key: RSA-CERT 39:aa:3f:bb:eb:24:11:93:15:b1:63:2f:de:ad:be:ef
debug1: Host 'example.host.net' is known and matches the RSA-CERT host certificate.
...
```

# User Authentication

User authentication is not much harder than server authentication.
Create User CA

On your preferred certificate authority server run the following commands

```console
$ # Lets start with good organization
$ mkdir -p ssh_cert_authority/user_ca
$ cd ssh_cert_authority/user_ca

~/ssh_cert_authority/user_ca $ # Now lets generate our server certificate authority keypair
~/ssh_cert_authority/user_ca $ ssh-keygen -f user_ca -C "companyname_user_ca"
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in user_ca.
Your public key has been saved in user_ca.pub.
The key fingerprint is:
90:67:8a:ed:b6:53:0a:bd:06:f0:71:ce:fb:89:b9:3e "companyname_user_ca"

~/ssh_cert_authority/user_ca $ # The resulting files
~/ssh_cert_authority/user_ca $ ls -l
total 8
-rw------- 1 username username 1679 Aug 16 18:14 user_ca
-rw-r--r-- 1 username username  407 Aug 16 18:14 user_ca.pub

~/ssh_cert_authority/user_ca $ # Copy user_ca.pub to the server
~/ssh_cert_authority/user_ca $ scp -rp user_ca.pub root@example.host.net:/etc/ssh
user_ca.pub                                                                            100%  407     0.4KB/s   00:00
```
Notes: It’s strongly suggested you not only use a passphrase, but also use a strong one. Anyone who signs with this key will be able to allow access to any user on all of your servers on your network.

# Sign User Key

Have a user create an ssh public-key set, and obtain a copy of their public key.

Retrieve a copy of the user’s public SSH key and execute the following command:

```console
~/ssh_cert_authority/user_ca $ # We need a place to keep signed certs
~/ssh_cert_authority/user_ca $ mkdir -p user_certs
~/ssh_cert_authority/user_ca $ cd user_certs/

~/ssh_cert_authority/user_ca/user_certs $ # Using my public key as an example
~/ssh_cert_authority/user_ca/user_certs $ cp ~/.ssh/id_rsa.pub username.pub

~/ssh_cert_authority/user_ca/user_certs $ # Sign the key
~/ssh_cert_authority/user_ca/user_certs $ ssh-keygen -s ../user_ca -I user_full_name -n root,loginname username.pub 
Signed user key username-cert.pub: id "user_full_name" serial 0 for root,loginname valid forever

~/ssh_cert_authority/user_ca/user_certs $ # The resulting files
~/ssh_cert_authority/user_ca/user_certs $ ls -l
total 8
-rw-r--r-- 1 username username 1525 Aug 16 22:01 username-cert.pub
-rw------- 1 username username  411 Aug 16 22:00 username.pub

~/ssh_cert_authority/user_ca/user_certs $ # Copy the certificate back to the user's ~/.ssh/ folder
~/ssh_cert_authority/user_ca/user_certs $ cp username-cert.pub ~/.ssh/id_rsa-cert.pub
```

Important: Keep all pubkeys and certs with the CA. If you need to revoke them, you must have a copy handy!

Important: You cannot negate the use of the options -I or -n when creating server certificates.

The -n option must only refer to the relevant login usernames, a blank or wildcard name will allow login to any valid user account unless otherwise restricted on the server-side. In this example the usernames “root” and “loginname” were used.

The -I option can be any text used to identify this certificate and you do not need to follow the same format used above.

# Server Configuration Change

Add the following to `/etc/ssh/sshd_config` on every server you want to enable user certificate authentication on:

```
TrustedUserCAKeys /etc/ssh/user_ca.pub
```

Once `sshd_config` is saved, restart sshd.

# Testing User Authentication

Delete the user’s public key from all authorized_keys file on the server.

Run the following command:

```console
~ $ ssh -v username@example.host.net
...
debug1: identity file /home/username/.ssh/id_rsa-cert type 4
debug1: Offering RSA-CERT public key: /home/username/.ssh/id_rsa
debug1: Server accepts key: pkalg ssh-rsa-cert-v01@openssh.com blen 1101
...
```

Additionally, on the server you will see the following logs, if you enable debug logging:

```console
Jul 18 23:22:03 localhost sshd[9603]: debug1: list_hostkey_types: ssh-rsa,ssh-rsa-cert-v01@openssh.com [preauth]
Jul 18 23:22:03 localhost sshd[9603]: Accepted certificate ID "user_username" signed by RSA CA d2:c0:6c:08:2b:e4:b4:f2:cd:56:22:66:de:ad:be:ef via /etc/ssh/user_ca.pub
```

# Taking It Further

The above steps are the basics for certificate authentication. Now we’ll cover features that allow you control certificate authentication with more granularity.

## Revoking Keys and Certificates

Granting access to your servers is great, but without the ability to revoke access you will not be able to lock out compromised host-keys or users no longer welcome on your systems.

The following methods also work with public-key authentication. Currently they are the only way to revoke ssh certificates.
Revoking User Keys

To enable user revocation, add the following line to your server’s `/etc/ssh/sshd_config`:

```
RevokedKeys /etc/ssh/ssh_revoked_keys
```

Then enter the following commands:

```console
~ $ # If the file doesn't exist and is not readable by sshd, **all** users will be denied access.
~ $ sudo touch /etc/ssh/ssh_revoked_keys
~ $ sudo chmod 644 /etc/ssh/ssh_revoked_keys.
```

Once complete, restart sshd.

When user access needs to be revoked from a server, simply add their public key or certificate and add it to `/etc/ssh/ssh_revoked_keys`. The file format is similar to authorized_keys, one key or cert per line.

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDL8HShSFKdY3Tox9U+gUotTFlRedPxI5zSrU6KiZEXA8i+37BtB0yp502q3Dx1MmXBF8Pqa+xEQ9DOgtragDwX0V7ieOjvRSB83w2Orj9cdMj8U6WluU2T+QlD2JtVmOp0Skg4k3AENIN9J0rmnxvmuCZa2G5f+6DGp/pW5kk9FfNv1xaAOgy3yfExD2w5cEHZfztajbTuCE6z9aNxU96ZHvXdV6Z8M3xkkea6IUU3XCyg+lB/qSq+KoBoByzwZSJ6BfA7x63okq57K6XsPp4GuVukq0OmDk9ZLpqmeC8esWhniA+2DwmjdaFa1k9K/bpCy4mVLhqTgwkU9u8rxaCd username@hostname
ssh-rsa-cert-v01@openssh.com AAAAHHNzaC1yc2EtY2VydC12MDFAb3BlbnNzaC5jb20AAAAgcrHTa3GDn51GnAnGuuFz//tS+NsIk0pP16nEglh4/08AAAADAQABAAABAQCxl7RSkZwRW0igzKUGUqkthFvH8Su3m0G1kWC4YBQht9TkXsSsWVW5FGbIGrYWy2JOJngAKTk6T82ySiuJnMA2esEW4thZ5kp8MgdCcMuqUGfFXxkHHF0cnzY0AWSD3z8WvuGVEWDTtIUpBqiW/ZvVZgVpHViqGF8AAbiFL2iRdG4D5g35ydFs0Gujn38zfyJLRVK/AQtqS9yzh6wRfgOu0/QXI/pYVV4imuXgQCsouW/gSItvg5Qdp8tyaA0hYJA7XHD6DCxr3RplT1XrsIMuROY1nSqTq0wpXl7XPM6aLOts63uPypumMIuq5kqX+5NBd+C6gDnEU7Xedce+Ch/LAAAAAAAAAAAAAAABAAAADnVzZXJfZnVsbF9uYW1lAAAADAAAAAh1c2VybmFtZQAAAAAAAAAA//////////8AAAAAAAAAggAAABVwZXJtaXQtWDExLWZvcndhcmRpbmcAAAAAAAAAF3Blcm1pdC1hZ2VudC1mb3J3YXJkaW5nAAAAAAAAABZwZXJtaXQtcG9ydC1mb3J3YXJkaW5nAAAAAAAAAApwZXJtaXQtcHR5AAAAAAAAAA5wZXJtaXQtdXNlci1yYwAAAAAAAAAAAAABFwAAAAdzc2gtcnNhAAAAAwEAAQAAAQEAy/B0oUhSnWN06MfVPoFKLUxZUXnT8SOc0q1OiomRFwPIvt+wbQdMqedNqtw8dTJlwRfD6mvsREPQzoLa2oA8F9Fe4njo70UgfN8Njq4/XHTI/FOlpblNk/kJQ9ibVZjqdEpIOJNwBDSDfSdK5p8b5rgmWthuX/ugxqf6VuZJPRXzb9cWgDoMt8nxMQ9sOXBB2X87Wo207ghOs/WjcVPemR713VemfDN8ZJHmuiFFN1wsoPpQf6kqviqAaAcs8GUiegXwO8et6JKueyul7D6eBrlbpKtDpg5PWS6apngvHrFoZ4gPtg8Jo3WhWtZPSv26QsuJlS4ak4MJFPbvK8WgnQAAAQ8AAAAHc3NoLXJzYQAAAQBza5ekUSM6/HKNNxfsPsynW6XNVblHdWuWGdFdHU+xo5y+MqPhkOcHEK3g3MZ5xQ75CSBeNPmd+ivIAUr7czwnWE7gJF/0q2ft3tahp+t9vOV7bvTQDf6afnSOwFRWVhoUC0OItHVQ5DphL+QuUsRtq/1a99DuhhNoqO7RJeNvgWwhnPI9LuTZ/wdJGxBsY0d1bS/3ktFtPPdbQNBWcQG8ShwdJj3XM5eKkzUNrjm1CfSi4fyVWX53gx6+dKxwlg7rI1GuZ14is3ZEb6oSk++P4MrSsqeIhKiE0QLNp6kXi8qwdYX93VrI+pD9mv7qLU3h22JvQUKnuWNvdJJuQATZ username@hostname
```

Notes: This blocks the public key or certificate from being used system-wide

* Public-keys are more ideal as they are smaller and block both public-key in addition to certificate authenitcation
* Certificates work fine here too, but do not block the public-key should it be in an authorized_keys file

```
Jul 19 00:27:26 localhost sshd[11546]: error: WARNING: authentication attempt with a revoked RSA-CERT key 6d:59:82:70:2b:93:dc:57:a6:c6:1f:64:de:ad:be:ef
```

## Revoking Server Keys

Server keys must be revoked in a user’s known_hosts file, or in /etc/ssh/known_hosts as follows:

```
@revoked * ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDc9wlKYUzWZcfvPOa0L+h6Wbb/k9yJgXbnqa3VF+ucdwmBSiT3zBMAjqjFMnN3MuI4oig3SqkIXKPWn0QgFoV4d3G4opzs/OdZ6WLyxLwYQBggUQDg4QhKuHDltIR/BMxYlhB20ngmkaiBiK+Q4ThFRpW7FElOsuZ3rgJq559PgkFeFMY06oyzUMaSshFM84U/1zrVL4BgdnZBcJn018psem5kSkd0Gxm+ao1TuEnMGeArVMFiG9Hq1o2E+QGp1euE4YYQtR533fyZ8BSTE9ThLkmTXgU31dn1irFatBrBENm7TnIVmNT410NqV5J9zDME4NAnuEVwNWtq65rZkgut root@localhost
```

Notes: The wildcard prevents the host-key from being used by any host

As above, both public-keys and certificates work, but public key is smaller and more effective

When working with individual known_hosts entries, simply deleting an entry does not prevent the key from being used again

```console
~ $ ssh example.host.net
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@       WARNING: REVOKED HOST KEY DETECTED!               @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
The RSA host key for example.host.net is marked as revoked.
This could mean that a stolen key is being used to impersonate this host.
RSA host key for example.host.net was revoked and you have requested strict checking.
Host key verification failed.
```

# Applying Controls to Certificates

When signing a certificate, an administrator can apply controls directly into the certificate that cannot be altered without re-signing.
Certificate Expiration

Most organizations apply password expiration policies, and many compliance requirements require regular password and certificate expiration. Unfortunately there have only been ad-hoc methods enforce ssh key rotation.

With certificates, an expiration date can be built into the certificate at the time of signing. This can be done with the -V option using the ssh time format

```
~/ssh_cert_authority/user_ca/user_certs $ # Expiration in 52 weeks
~/ssh_cert_authority/user_ca/user_certs $ ssh-keygen -s ../user_ca -I user_full_name -n root,loginname -V +52w username.pub

~/ssh_cert_authority/user_ca/user_certs $ # Expiration in 180 days
~/ssh_cert_authority/user_ca/user_certs $ ssh-keygen -s ../user_ca -I user_full_name -n root,loginname -V +180d username.pub
```

Notes: Expirations work equally on user and server certificates.

# Login Names

As mentioned earlier, both login-names and server-names can be enforced in the certificate using the -n option.

For users, this restricts the user to specific login names on the remote server. Typically this should be a single username, but in some environments they may be a need for multiple names.

The following is an example of allowing multiple login names on a single certificate:

```
~/ssh_cert_authority/user_ca/user_certs $ ssh-keygen -s ../user_ca -I user_full_name -n loginname,anothername,thirdname username.pub
```

# Options (user certs only)

For user certs, there can be several options built directly into the certificate at the time of signing. Typically these options were applied in `/etc/sshd_config` or in `authorized_keys` file. The options are:

```
    clear to assume no default options
    force-command=(command) To enforce remote command execution
    permit-agent-forwarding/no-agent-forwarding Permitted by default
    permit-port-forwarding/no-port-forwarding Permitted by default
    permit-pty/no-pty Permitted by default
    permit-user-rc/no-user-rc Permitted by default
    permit-x11-forwarding/no-x11-forwarding Permitted by default
    source-address=(address_list) Limit source-address from which this certificate is valid
```

```console
~/ssh_cert_authority/user_ca/user_certs $ ssh-keygen -s ../user_ca -I user_full_name -n login \
  -O clear \ # Clear all default options, including forwarding of all kinds
  -O force-command=/some/specific/command \ # force execution of a specific command
  -O source-address=10.22.72.0/24 \ # limit logins from specific source addresses
  username.pub
```


The above example restrictions an automated batch-job to only be run from specific servers, not allowing pty, forwarding, and forcing a specific command.

# Known Issues

## Certificate Version Issues

With the release of OpenSSH 6.x, an update was made to the certificates resulting in a compatibility issue with OpenSSH 5.x.

OpenSSH 6.x generated certificates will not work with OpenSSH 5.x unless the option “-t v00” option is used. For example:

```
$ ssh-keygen -t v00 -s ca_key -I key_id host_key.pub
```

OpenSSH 6.x appears to be backward compatible with OpenSSH 5.x generated certificates.


## SSH Client Compatibility

Outside of OpenSSH there are few, if any, clients that support certificate based authentication.

While OpenSSH runs on most common and uncommon operating systems, there will always be other clients out there. Such example is the ever popular Putty for Windows, which does not support certificate authentication, yet. Also, many commercial applications with ssh support do not support certificate authentication – An example is Nexpose by Rapid7.

As a result, some environments may be hard, if not impossible, to enforce only certificate based authentication. 

# CA Key Management

## CA Key Security

Centralizing the management of keys simplifies management of authentication. Unfortunately it also simplifies the attack-surface. An attacker only needs to gain access to the CA keys to gain full access to the network.

As a result, it’s critical that the CA keys be managed under high-security. If possible have them stored where they cannot have network access, and always, always, ensure they are encrypted.


Root CA for SSH
===============
Create the Root CA for SSH:

```bash
ssh-keygen -f my-enterprise-root-ca  -C "CA key for example.com"
```

* `-C "CA key for example.com"` - The `-C` option sets a comment in your key file. The default is `user@host`, but since you'll be dealing with a lot of keys at a time now it might be better to give the keys moe descriptive names.

Oh, and please note that most other guides will tell you to do these steps as root. There's no real need to generate keys as root - any ordinary user will do fine. So it's probably best if you do use an ordinary user account. 

Also, it doesn't matter where you generate the key pair - do it on your workstation if you can, not your server. 

Just remember to keep the SSH CA signing keys safe - this one is probably one of those that you should use a password with, because this key is really powerful and you don't need to use it very often.

and the output is:
```console
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in my-enterprise-root-ca
Your public key has been saved in my-enterprise-root-ca.pub
The key fingerprint is:
SHA256:xjLvnQYx/5h6uW/wllKgnu/eCDT1/vXSMs6LiiF958A wolfe@circa
The key's randomart image is:
+---[RSA 3072]----+
|                 |
|                 |
|          .      |
|       .o...     |
|      o S= ..    |
|       Booo..    |
|      ..=oEOo. ..|
|       oo*BB*++.o|
|        +BXB=.==.|
+----[SHA256]-----+
```

Two files got generated in the same working directory:

* `my-enterprise-root-ca`
* `my-enterprise-root-ca.pub`

INFO: Their naming convention is markedly different than TLS CA, so take a note of this table:

[jtable]
kind of cert, TLS, SSH
Private key, `<filename>.key.pem`, `<filename>`
Public key, `<filename>.cert.pem`, `<filename>.pub`
[/jtable]

SECURITY CAVEAT: Yeah, they are that different so pay attention and keep those file permission to a bare minimum for the SSH private key file WITHOUT a filetype.


Create Certificates for SSH
===========================

Host Certificates
-----------------

To create a user certificate:
```bash
ssh-keygen -h -n hostname \
    -s my-enterprise-root-ca.privatekey.pem \
    -I key_identifier \
    -V +52w \
    host_rsa_key
```
SIDEBAR:  I had to rename `my-enterprise-root-ca` by adding a `privatekey.pem` filetype to denote that it is a private key and that it is a PEM-styled file.

alternatively, you can do this:
```bash
ssh-keygen -s /etc/ssh/ca \
     -I "$(hostname --fqdn) host key" \
     -n "$(hostname),$(hostname --fqdn),$(hostname -I|tr ' ' ',')" \
     -V -5m:+3650d \
     -h \
     /etc/ssh/ssh_host_rsa_key.pub \
     /etc/ssh/ssh_host_dsa_key.pub \
     /etc/ssh/ssh_host_ecdsa_key.pub
```
 
Options are detailed below:
* `-s` - This is the private key that we just created that we will use to sign all of the other keys.
* `-I` - This is a name that is used to identify the certificate. It is used for logging purposes when the certificate is used for authentication.  the certificate's identity, an alphanumeric string that will be visible in SSH logs when the user certificate is presented. I recommend using the email address or internal username of the user that the certificate is for - something which will allow you to uniquely identify a user. This value can also be used to revoke a certificate in future if needed.
* `-h` - This marks the resulting certificate as a host key, as opposed to a client key.  Without this option, you would be making a user certificate.
* `-n` - Contains a comma-separated list of the names (user or host) that is associated with this certificate.  For UNIX, the name is the account name used in `/etc/passwd`.  For Kerberos KRB5 and Windows AD, the name is the AD/KRB5 principal name.
* `-V` - This specifies how long the certificate is valid for. In this instance, we specify that the certificate will expire in one year (52 weeks).

Also the final argument is the file to read for the PRIVATE key in PEM format.  Typically, those keys are found in `/etc/ssh` directory starting with `ssh_host_ecdsa_key.pub`

How To Configure Host Certificates
==================================

Let us start by configuring certificates that will authenticate our servers to our clients. This will allow our clients to connect to our servers without needing to question the authenticity of the server.

Begin on the machine that that will be using as the certificate authority. In this example, we’ll refer to this as “auth.example.com”.
Generating Signing Keys

First, we need to generate some RSA keys that will function as the signing keys. Use any user you’d like, but the root user is probably a good idea. Create these keys called “server_ca” and “server_ca.pub” since these will be used to authenticate our servers.

Let’s create these keys in our home directory:

cd ~
ssh-keygen -f server_ca

You will be asked if you’d like to create a passphrase. This will add an additional layer of protection to your key in the event that it falls into the wrong hands. Once this is finished, you’ll have a private and public key in your home directory:

ls

server_ca   server_ca.pub

Signing Host Keys
=================

Now that we have our keys, we can begin signing our host keys.

Start by signing the host key of the certificate authority itself. Use the following syntax:

<pre> ssh-keygen -s <span class=“highlight”>signing_key</span> -I <span class=“highlight”>key_identifier</span> -h -n <span class=“highlight”>host_name</span> -V +52w <span class=“highlight”>host_rsa_key</span> </pre>

Let’s go over what all of this means.

    -s: This is the private key that we just created that we will use to sign all of the other keys.
    -I: This is a name that is used to identify the certificate. It is used for logging purposes when the certificate is used for authentication.
    -h: This marks the resulting certificate as a host key, as opposed to a client key.
    -n: This is used to identify the name (user or host) that is associated with this certificate.
    -V: This specifies how long the certificate is valid for. In this instance, we specify that the certificate will expire in one year (52 weeks).

Afterwards we specify the key that we want to sign.

In our case, to sign our own host RSA key, we will use a line that looks like this. identify this server as "`host_auth_server`".  Then a prompt appears for the passphrase we used when creating the signing key:

```console
$ ssh-keygen -s server_ca -I host_auth_server \
    -h -n auth.example.com \
    -V +52w \
    /etc/ssh/ssh_host_rsa_key.pub
Signed host key `/etc/ssh/ssh_host_rsa_key-cert.pub`: id "host_auth_server" serial 0 for auth.example.com valid from 2014-03-20T12:25:00 to 2015-03-19T12:26:05
```

As you can see from the output, our certificate is valid for one year. It has been created in the same directory as our server host key (in `/etc/ssh/` directory) and is called "`ssh_host_rsa_key-cert.pub`".

Now that we have signed our host key on the certificate authority itself, we can sign the host key for the separate SSH server we’re trying to authenticate to clients.

Copy the host key from our SSH server. Refer to this machine as the "`sshserver.example.com`". You can do this using scp:

```console
$ cd ~
$ scp root@sshserver.example.com:/etc/ssh/ssh_host_rsa_key.pub .
```

Now, create the certificate from this file using the same method we used above. Change some values to refer to the new host that is being signed:

```
ssh-keygen -s server_ca -I host_sshserver -h -n sshserver.example.com -V +52w ssh_host_rsa_key.pub

Signed host key ssh_host_rsa_key-cert.pub: id "host_sshserver" serial 0 for sshserver.example.com valid from 2014-03-20T12:40:00 to 2015-03-19T12:41:48
```

Now, copy the generated certificate file back onto the host. Again, using `scp` for this:

```console
$ scp ssh_host_rsa_key-cert.pub root@sshserver.example.com:/etc/ssh/
```

Afterwards, we can delete both the SSH server’s public key and certificate from our authentication server:

```bash
rm ssh_host_rsa_key.pub ssh_host_rsa_key-cert.pub
```

We now have the signed certificates in place, we just need to configure our components to use them.


# Configuring Components to Use Host Certs

First, we need to continue with both of our servers (`auth.example.com` and `sshserver.example.com`) to make them aware of the certificate files we created.

On both of these machines, we’ll have to edit the main SSH daemon configuration file. Make sure you are editing the `sshd_config` file, not the `ssh_config` file:

```bash
sudo nano /etc/ssh/sshd_config
```

If you can find a HostCertificate line, modify it. Otherwise, add this to the bottom of the file. We need to establish to path to our host certificate file:

```
HostCertificate /etc/ssh/ssh_host_rsa_key-cert.pub
```

Save and close the file when you are finished.

Now, restart the SSH daemon to make these changes happen:

```
sudo service ssh restart
```

Do this on all of the servers you are configuring host certificates for.

Now, our servers are configured to use the certificate, but our client does not know how to check the certificate that the server will present.

On our client machine, which we’ll be referring to as "`client.example.com`", open or create the "`~/.ssh/known_hosts`" file:

```bash
nano ~/.ssh/known_hosts
```

Need to remove any entries that have to do with the servers we’re configuring for certificate entry. It may be best to delete everything.

Afterwards, we need to add a special entry that specifies the public key that we should use to check the certificate that our hosts will give us during login. Start it off with @cert-authority. Afterwards, it can include a domain restriction where the key will be applied, followed by the public certificate authority key that we’ve been signing everything with.

On your certificate authority machine, you can get the public certificate signing key by typing:

```console
$ cat ~/server_ca.pub

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxC+gikReZlWEnZhKkGzhcNeRD3dKh0L1opw4/LQJcUPfRj07E3ambJfKhX/+G4gfrKZ/ju0nanbq+XViNA4cpTIJq6xVk1uVvnQVOi09p4SIyqffahO9S+GxGj8apv7GkailNyYvoMYordMbIx8UVxtcTR5AeWZMAXJM6GdIyRkKxH0/Zm1r9tsVPraaMOsKc++8isjJilwiQAhxdWVqvojPmXWE6V1R4E0wNgiHOZ+Wc72nfHh0oivZC4/i3JuZVH7kIDb+ugbsL8zFfauDevuxWeJVWn8r8SduMUVTMCzlqZKlhWb4SNCfv4j7DolKZ+KcQLbAfwybVr3Jy5dSl root@auth
```

Using this information, the line in your `~/.ssh/known_hosts` file should look like:

```
@cert-authority *.example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxC+gikReZlWEnZhKkGzhcNeRD3dKh0L1opw4/LQJcUPfRj07E3ambJfKhX/+G4gfrKZ/ju0nanbq+XViNA4cpTIJq6xVk1uVvnQVOi09p4SIyqffahO9S+GxGj8apv7GkailNyYvoMYordMbIx8UVxtcTR5AeWZMAXJM6GdIyRkKxH0/Zm1r9tsVPraaMOsKc++8isjJilwiQAhxdWVqvojPmXWE6V1R4E0wNgiHOZ+Wc72nfHh0oivZC4/i3JuZVH7kIDb+ugbsL8zFfauDevuxWeJVWn8r8SduMUVTMCzlqZKlhWb4SNCfv4j7DolKZ+KcQLbAfwybVr3Jy5dSl root@auth
```

Save and close the file when you’re done.

When you visit the SSH server for the first time from your client (using the full hostname), you should not be asked whether you trust the remote host. This is because the host has presented its host certificate to you, signed by the certificate authority. You’ve checked your `known_hosts` file and verified that the certificate is legitimate.


How To Configure User Keys
==========================

Now that we’ve learned how to authenticate servers to our users, one can then configure our certificate authority to authenticate our users to our servers.

As before, this process will start on our certificate authority server. We will need to generate a new set of keys, this time, to sign user certificates:

```bash
ssh-keygen -f users_ca
```

Again, select a passphrase so that your key will be protected if someone gains access.


## Configuring Servers to Accept Logins with the User Certification

When you are done, you will need to copy the public key onto each of your SSH servers that need to validate user authenticity. We will do this using scp as usual:

```
scp users_ca.pub root@sshserver.example.com:/etc/ssh/
```

We need to modify our SSH daemon configuration on our SSH server to look for this key.

On our "`sshserver.example.com`" host, open the configuration file:

```
sudo nano /etc/ssh/sshd_config
```

At the bottom, below our HostCertificate line, we need to add another line that references the file we just copied over:

```
TrustedUserCAKeys /etc/ssh/users_ca.pub
```

Again, we’ll need to restart the SSH daemon for these changes to take place:

```
sudo service ssh restart
```

## Signing User Login Keys

SSH Server is now configured to trust keys signed by the `users_ca` key, we need to actually sign the users’ authentication keys so that this scheme will work.

First, to get our client key onto the certificate authority server with scp, type:

```console
$ vi user_ca
<pre> cd ~ scp <span class=“highlight”>username</span>@client.example.com:/home/<span class=“highlight”>username</span>/.ssh/id_rsa.pub . </pre>
```

With the key on the cert machine, sign it using our `users_ca` key. This will be very similar to last time the keys got signed using the `server_ca` keys, only now, don’t include the `-h` parameter, because these are for user keys.

The command we want is something like this. Change the "`user_username`" value to reflect the name of the user you’re signing for easier management:

```bash
$ ssh-keygen -s users_ca \
    -I user_username \
    -n username \
    -V +52w id_rsa.pub
Signed user key id_rsa-cert.pub: id “user_username” serial 0 for username valid from 2014-03-20T14:45:00 to 2015-03-19T14:46:52 
```
alternatively

```bash
ssh-keygen -s /etc/ssh/ca \
    -I "$(whoami)@$(hostname --fqdn) user key" \
    -n "$(whoami)" \
    -V -5m:+3650d \
    ~/.ssh/id_rsa.pub \
    ~/.ssh/id_dsa.pub \
    ~/.ssh/id_ecdsa.pub

ssh-add ~/.ssh/*-cert.pub
```

A prompt appears for the `users_ca` passphrase that set during the key’s creation. Enter in the passphrase.

An `id_rsa-cert.pub` file appears in `$HOME/.ssh` directory that we need to transfer back onto our client machine:

Content looks like:
```
<pre> scp id_rsa-cert.pub <span class=“highlight”>username</span>@client.example.com:/home/<span class=“highlight”>username</span>/.ssh/ </pre>
```

Log into `sshserver.example.com` from your client computer, this time no prompting should appear asking for your authentication details, even if you’ve never before logged into this server as this user.

# Conclusion

By signing your host and user keys, you can create a more flexible system for user and server validation. This allows you to set up one centralized authority for your entire infrastructure, in order to validate your servers to your user, and your users to your servers.

While perhaps not the most powerful way of creating centralized authentication, it is easy to set up and leverages existing tools without requiring a lot of time and configuration. It also has the advantage of not requiring the CA server to be online to check the certificates.


Verifying SSH Certificate Key
=============================

To verify the certificate, use `ssh-keyscan -c <hostname>`. To limit to a specific certificate type, you can include `-t type`, using `ssh-rsa` not `ssh-rsa-cert-v01@openssh.com`, if necessary.

Note: (without the `-c` option, you will only get the host key(s), not host certificate)

```bash
ssh-keyscan -c ssh-ca.my-server.test 
ssh-keyscan -c ssh-ca.my-server.test -t ssh-rsa
ssh-keyscan -c ssh-ca.my-server.test -t ssh-rsa-cert-v01@openssh.com
```

Then, you can extract the certificate details, including the Signing CA's public key, with `ssh-keygen -L -f <certfile>`. 

Note: If you use (lowercase) -l instead, then ssh-keygen only outputs the information about the underlying (public) host key embedded in the certificate, rather than all of the certificate elements.

```bash
ssh-keygen -L ssh-ca.my-server.test
```

SSH Certificate Tricks
======================

ACL by Grouping Users 
---------------------
If I add normal users to an endusers group, then I can set the `/etc/ssh/sshd_config` like this:
```ini
TrustedUserCAKeys /etc/ssh/admin_ca.pub
Match Group endusers
    TrustedUserCAKeys /etc/ssh/user_ca.pub
```


Reference
=========
* https://www.lorier.net/docs/ssh-ca.html
* IETF RFC 4716
* [Distributing and Trusting SSH CA Public Keys - Fedora 26 System Administrator Guide](https://docs.fedoraproject.org/en-US/Fedora/26/html/System_Administrators_Guide/sec-Distributing_and_Trusting_SSH_CA_Public_Keys.html)
* [UNIX StackExchange (ssh+certificate)](https://unix.stackexchange.com/search?q=%5Bssh%5D+certificate)
* https://www.digitalocean.com/community/tutorials/how-to-create-an-ssh-ca-to-validate-hosts-and-clients-with-ubuntu
* https://unix.stackexchange.com/questions/550599/ssh-user-ca-sign-a-user-certificate-with-selected-hosts-instead-of-all-hosts
* https://betterprogramming.pub/how-to-use-ssh-certificates-for-scalable-secure-and-more-transparent-server-access-720a87af6617
