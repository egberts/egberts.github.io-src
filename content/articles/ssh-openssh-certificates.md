title: PKI Certificates in OpenSSH
date: 2022-03-24 07:38
status: draft
tags: OpenSSH, PKI, ssh
category: research
summary: How to create PKI certificates for use by OpenSSH
slug: ssh-openssh-certificates
lang: en
private: False

Just a couple of words:

* You will not be able to use OpenSSL `openssl` to manage your SSH certificates.

The SSH certificate file format is RFC4716.  Not PEM ('`.pem`'), and not PKCS#8 ('`.pkc`').


Root CA for SSH
===============
Create the Root CA for SSH:

```bash
ssh-keygen -f my-enterprise-root-ca
```
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

We will start by configuring certificates that will authenticate our servers to our clients. This will allow our clients to connect to our servers without needing to question the authenticity of the server.

We begin on the machine that we will be using as the certificate authority. In this example, we’ll refer to this as “auth.example.com”.
Generating Signing Keys

First, we need to generate some RSA keys that will function as the signing keys. Use any user you’d like, but the root user is probably a good idea. We will be creating keys called “server_ca” and “server_ca.pub” since these will be used to authenticate our servers.

Let’s create these keys in our home directory:

cd ~
ssh-keygen -f server_ca

You will be asked if you’d like to create a passphrase. This will add an additional layer of protection to your key in the event that it falls into the wrong hands. Once this is finished, you’ll have a private and public key in your home directory:

ls

server_ca   server_ca.pub

Signing Host Keys
=================

Now that we have our keys, we can begin signing our host keys.

We should start by signing the host key of the certificate authority itself. We can do this using the following syntax:

<pre> ssh-keygen -s <span class=“highlight”>signing_key</span> -I <span class=“highlight”>key_identifier</span> -h -n <span class=“highlight”>host_name</span> -V +52w <span class=“highlight”>host_rsa_key</span> </pre>

Let’s go over what all of this means.

    -s: This is the private key that we just created that we will use to sign all of the other keys.
    -I: This is a name that is used to identify the certificate. It is used for logging purposes when the certificate is used for authentication.
    -h: This marks the resulting certificate as a host key, as opposed to a client key.
    -n: This is used to identify the name (user or host) that is associated with this certificate.
    -V: This specifies how long the certificate is valid for. In this instance, we specify that the certificate will expire in one year (52 weeks).

Afterwards we specify the key that we want to sign.

In our case, to sign our own host RSA key, we will use a line that looks like this. We are going to identify this server as “host_auth_server”. We will be prompted for the passphrase we used when creating the signing key:

ssh-keygen -s server_ca -I host_auth_server -h -n auth.example.com -V +52w /etc/ssh/ssh_host_rsa_key.pub

Signed host key /etc/ssh/ssh_host_rsa_key-cert.pub: id "host_auth_server" serial 0 for auth.example.com valid from 2014-03-20T12:25:00 to 2015-03-19T12:26:05

As you can see from the output, our certificate is valid for one year. It has been created in the same directory as our server host key (/etc/ssh/) and is called “ssh_host_rsa_key-cert.pub”.

Now that we have signed our host key on the certificate authority itself, we can sign the host key for the separate SSH server we’re trying to authenticate to clients.

Copy the host key from our SSH server. We’ll refer to this machine as “sshserver.example.com”. You can do this using scp:

cd ~
scp root@sshserver.example.com:/etc/ssh/ssh_host_rsa_key.pub .

Now, we can create a certificate from this file using the same method we used above. We’ll need to change some values to refer to the new host we’re signing:

ssh-keygen -s server_ca -I host_sshserver -h -n sshserver.example.com -V +52w ssh_host_rsa_key.pub

Signed host key ssh_host_rsa_key-cert.pub: id "host_sshserver" serial 0 for sshserver.example.com valid from 2014-03-20T12:40:00 to 2015-03-19T12:41:48

Now, we need to copy the generated certificate file back onto the host. Again, we can use scp for this:

scp ssh_host_rsa_key-cert.pub root@sshserver.example.com:/etc/ssh/

Afterwards, we can delete both the SSH server’s public key and certificate from our authentication server:

rm ssh_host_rsa_key.pub ssh_host_rsa_key-cert.pub

We now have the signed certificates in place, we just need to configure our components to use them.
Configuring Components to Use Host Certs

First, we need to continue with both of our servers (auth.example.com and sshserver.example.com) to make them aware of the certificate files we created.

On both of these machines, we’ll have to edit the main SSH daemon configuration file. Make sure you are editing the sshd_config file, not the ssh_config file:

sudo nano /etc/ssh/sshd_config

If you can find a HostCertificate line, modify it. Otherwise, add this to the bottom of the file. We need to establish to path to our host certificate file:

HostCertificate /etc/ssh/ssh_host_rsa_key-cert.pub

Save and close the file when you are finished.

Now, restart the SSH daemon to make these changes happen:

sudo service ssh restart

Do this on all of the servers you are configuring host certificates for.

Now, our servers are configured to use the certificate, but our client does not know how to check the certificate that the server will present.

On our client machine, which we’ll be referring to as “client.example.com”, open or create the “~/.ssh/known_hosts” file:

nano ~/.ssh/known_hosts

We need to remove any entries that have to do with the servers we’re configuring for certificate entry. It may be best to delete everything.

Afterwards, we need to add a special entry that specifies the public key that we should use to check the certificate that our hosts will give us during login. Start it off with @cert-authority. Afterwards, it can include a domain restriction where the key will be applied, followed by the public certificate authority key that we’ve been signing everything with.

On your certificate authority machine, you can get the public certificate signing key by typing:

cat ~/server_ca.pub

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxC+gikReZlWEnZhKkGzhcNeRD3dKh0L1opw4/LQJcUPfRj07E3ambJfKhX/+G4gfrKZ/ju0nanbq+XViNA4cpTIJq6xVk1uVvnQVOi09p4SIyqffahO9S+GxGj8apv7GkailNyYvoMYordMbIx8UVxtcTR5AeWZMAXJM6GdIyRkKxH0/Zm1r9tsVPraaMOsKc++8isjJilwiQAhxdWVqvojPmXWE6V1R4E0wNgiHOZ+Wc72nfHh0oivZC4/i3JuZVH7kIDb+ugbsL8zFfauDevuxWeJVWn8r8SduMUVTMCzlqZKlhWb4SNCfv4j7DolKZ+KcQLbAfwybVr3Jy5dSl root@auth

Using this information, the line in your ~/.ssh/known_hosts file should look like:

@cert-authority *.example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxC+gikReZlWEnZhKkGzhcNeRD3dKh0L1opw4/LQJcUPfRj07E3ambJfKhX/+G4gfrKZ/ju0nanbq+XViNA4cpTIJq6xVk1uVvnQVOi09p4SIyqffahO9S+GxGj8apv7GkailNyYvoMYordMbIx8UVxtcTR5AeWZMAXJM6GdIyRkKxH0/Zm1r9tsVPraaMOsKc++8isjJilwiQAhxdWVqvojPmXWE6V1R4E0wNgiHOZ+Wc72nfHh0oivZC4/i3JuZVH7kIDb+ugbsL8zFfauDevuxWeJVWn8r8SduMUVTMCzlqZKlhWb4SNCfv4j7DolKZ+KcQLbAfwybVr3Jy5dSl root@auth

Save and close the file when you’re done.

Now, when you visit the SSH server for the first time from your client (using the full hostname), you should not be asked whether you trust the remote host. This is because the host has presented its host certificate to you, signed by the certificate authority. You’ve checked your known_hosts file and verified that the certificate is legitimate.


How To Configure User Keys
==========================

Now that we’ve learned how to authenticate servers to our users, we can also configure our certificate authority to authenticate our users to our servers.

As before, this process will start on our certificate authority server. We will need to generate a new set of keys, this time, to sign user certificates:

ssh-keygen -f users_ca

Again, select a passphrase so that your key will be protected if someone gains access.
Configuring Servers to Accept Logins with the User Certification

When you are done, you will need to copy the public key onto each of your SSH servers that need to validate user authenticity. We will do this using scp as usual:

scp users_ca.pub root@sshserver.example.com:/etc/ssh/

We need to modify our SSH daemon configuration on our SSH server to look for this key.

On our “sshserver.example.com” host, open the configuration file:

sudo nano /etc/ssh/sshd_config

At the bottom, below our HostCertificate line, we need to add another line that references the file we just copied over:

TrustedUserCAKeys /etc/ssh/users_ca.pub

Again, we’ll need to restart the SSH daemon for these changes to take place:

sudo service ssh restart

Signing User Login Keys

Now that the servers are configured to trust keys signed by the users_ca key, we need to actually sign the users’ authentication keys so that this scheme will work.

First, we need to get our client key onto the certificate authority server with scp. From the cert server, type:

<pre> cd ~ scp <span class=“highlight”>username</span>@client.example.com:/home/<span class=“highlight”>username</span>/.ssh/id_rsa.pub . </pre>

Now that we have the key on the cert machine, we can sign it using our users_ca key. This will be very similar to last time we signed keys using the server_ca keys, only now, we don’t include the -h parameter, because these are user keys.

The command we want is something like this. Change the “username” value to reflect the name of the user you’re signing for easier management:

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

You will be prompted for the users_ca passphrase that set during the key’s creation. Now, we have an id_rsa-cert.pub file in our directory that we need to transfer back onto our client machine:

<pre> scp id_rsa-cert.pub <span class=“highlight”>username</span>@client.example.com:/home/<span class=“highlight”>username</span>/.ssh/ </pre>

Now, when you log into sshserver.example.com from your client computer, you should not be asked for your authentication details, even if you’ve never before logged into this server as this user.
Conclusion

By signing your host and user keys, you can create a more flexible system for user and server validation. This allows you to set up one centralized authority for your entire infrastructure, in order to validate your servers to your user, and your users to your servers.

While perhaps not the most powerful way of creating centralized authentication, it is easy to set up and leverages existing tools without requiring a lot of time and configuration. It also has the advantage of not requiring the CA server to be online to check the certificates.

Reference
=========
* https://www.lorier.net/docs/ssh-ca.html
* IETF RFC 4716
* [Distributing and Trusting SSH CA Public Keys - Fedora 26 System Administrator Guide](https://docs.fedoraproject.org/en-US/Fedora/26/html/System_Administrators_Guide/sec-Distributing_and_Trusting_SSH_CA_Public_Keys.html)
* [UNIX StackExchange (ssh+certificate)](https://unix.stackexchange.com/search?q=%5Bssh%5D+certificate)
