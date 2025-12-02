title: Using Variables in a OpenSSL Config File
date: 2022-03-20 11:04
modified: 2025-07-13 03:15
status: published
tags: OpenSSL, environment variables
category: HOWTO
summary: How to specify variable names and reference them in OpenSSL configuration file.
slug: openssh-variables
lang: en
private: False


There are many ways to use a variable in a OpenSSL configuration file:

Direct Variable
===============
Those are the easiest kind (in many languages, too!)

```ini
dir = /home/johndoe/ssl

cert_file = $dir/cert.crt.pem
```

Then there are curly braces for variable names.

The set of curly braces is most useful when constructing 
a text string having variable suffix/middle/prefix, like filetype
or a sub-segment of a filename.
```ini

CRT_TYPE=.crt
cert_file = ${dir}/cert${CRT_TYPE}.pem
```

Scoping of Variable
-------------------
Scoping of variable names are strictly observed in OpenSSL configuration file.

If you declare it inside a section, that variable name is not available outside that section.  The variable names are only accessible from within that section or sections within/under.

```ini
[ distinguished_name ]
commonName = $issuer_url

[crl]
issuer_url = https://ocsp.mysite.test:80
crlDistributionPoint=URI:$issuer_url
```
The above is an error: the `issuer_url` variable is scoped to only be used under the `[ crl ]` section and not made available to the outside scope of `[ distinguished_name ]` section.

It is common to put variables in the default section.  Default sections are the outermost scope before the first section of a config file.  

There is also an optional `[ default ]` section.  Optional `[ default ]` is useful in add-on config files when one wishes to overwrite a default setting.  Such add-on config file  can be then be appended to the default `openssl.cnf` file via `-reqexts` or `-extensions` CLI option.

```ini
issuer_url = https://ocsp.mysite.test:80
.
.
.
[crl]
crlDistributionPoint=URI:$issuer_url
```


Environment Variable
====================
Use the `ENV::` notation before the name of environment variable.

```ini
# ENV::HOME is bash $HOME
dir = ENV::HOME/ssl
```

If dealing with in-the-middle-string operation, surround it with '`{}`'.
```ini
dir = /file-server/${ENV::HOME}/ssl

certificate = $dir/ca.crt.pem
key_file    = $dir/ca.key.pem
```


Multiple DNS into SAN
---------------------
To hold multiple DNS entries in SAN:
```
[ req ]
req_extensions = my_req_extensions_section

[ my_req_extensions_section ]

Cloning commonName into SAN
---------------------------
To copy the fully-qualified domain name into the `altSubjectName` from its `distinguished_name` section:
```ini
altSubjectName = ${req_dn::commonName}
```

Copying commonName into SAN with many DNS
-----------------------------------------
```ini
[ req ]
req_extensions          = server_MyCaRoot_reqext     # Desired extensions

[ server_MyCaRoot_reqext ]
.
.
.
subjectAltName          = @alt_names

[alt_names]
DNS.1 = webserver.com
DNS.2 = www.com
```

Making it Easier To Move
------------------------
If you have to move "the" server from one DNS name to another, you
could use some non-standard name for the server name (like the ones
assigned to you by your ISP), this would help with the DNS move a bit
easier to just the recreation of KEY/CSR/CERT.

```ini
[ req ]
distinguished_name = server_myWebServer_dn
req_extensions          = server_MyWebServer_reqext     # Desired extensions

[ server_MyWebServer_reqext ]
.
.
.
subjectAltName          = @alt_names

[alt_names]
DNS.1 = ${req_dn:commonName}
DNS.2 = www.example.test
DNS.2 = example.test

[ server_myWebServer_dn ]
commonName = $ENV::SERVER_NAME
```

This takes it down one step less.

1. Your script could lift the server's actual DNS name
2. Create the `SERVER_NAME=c512-does-not-exist.sea.wa.fios.verison.net` environment variable (of course, replace it with your server's actual DNS name)
3. re-run all your ready-made `openssl` scripts
4. if using an SSL provider, submit CSR to recreate the server certificate
5. deploy the new server certificate into web server's config directory

And enjoy your refreshing beverage.
