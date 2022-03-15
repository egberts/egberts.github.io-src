title: How to read a OpenSSL configuration file
date: 2021-11-18 11:00
status: published
tags: OpenSSL
category: research
summary: 15 years of barely ignoring this file, I've finally detailed the `openssl.cnf` file.
lang: en
private: False

I've stared at the `openssl.cnf` far more times than I cared for.  It wasn't
until some 15 years later, I have set out to fully understand the entire OpenSSL
configuration file and its intricities.

How exactly does one grok an OpenSSL configuration file?  Grok?  Yeah, grok as
in perusing, parsing, absorbing, dissemination and dissection:

- You follow the assignments.  

- Each assignment either leads you to:

   - a value or 
   - a label leading to a different group of values.

All assignment parsings start from the first uncommented line.

`openssl.cnf` was designed by like-minded folks who also designed OIDs, SNMP MIBs, and ASN1 as well as X.509.

In this article, I will outline what or which actual keywords that the OpenSSL will be looking for when constructing a list of configurable values before creating your certificate-request, and other certificates.

BACK UP A BIT
=============

But before we go further into `openssl.cnf`, we have to consider who the external influencers are toward the `openssl` binary: shell environment variables.

I've identified the following shell environment names used by `openssl` 
(by scanning for `getenv()` functions and few other code review tricks):

  - `CN`
  - `CTLOG_FILE_EVP`
  - `LEGACY_GOST_PKCS12`
  - `HOME`
  - `http_proxy`
  - `https_proxy`
  - `no_proxy`
  - `NO_PROXY`
  - `OPENSSL`
  - `OPENSSL_armcap`
  - `OPENSSL_CONF`, util/wrap.pl
  - `OPENSSL_CONFIG`, app/CA.pl
  - `OPENSSL_CONF_INCLUDE`, util/wrap.pl
  - `OPENSSL_DEBUG_DECC_INIT`
  - `OPENSSL_ENGINES`, util/wrap.pl
  - `OPENSSL_ia32cap`
  - `OPENSSL_MALLOC_FAILURES`
  - `OPENSSL_MALLOC_FD`
  - `OPENSSL_MODULES`, util/wrap.pl
  - `OPENSSL_HTTP_PROXY`
  - `OPENSSL_NO_PROXY`
  - `OPENSSL_ppccap`
  - `OPENSSL_s390xcap`
  - `OPENSSL_sparcv9cap`
  - `OPENSSL_TEST_LIBCTX`
  - `OPENSSL_TRACE`
  - `RANDFILE`
  - `SSL_CIPHER`
  - `TEMP`
  - `TMP`
  - `TSGET`

NOTE: Above list are derived from `openssl` version 1.1.1k (11/18/2021).

Yeah, a lot of environment names there, accidential or not, to watch out for while using `openssl`.  

WARNING:  If you defined any envvar that OpenSSL extracts, the executable binary will NOT tell you that these envars got used.

As long as your shell doesn't define any of the above, you should be good to go
and not be surprised by any 'mysterious' behaviors of your configuration settings.

With that out of the way, now we can delve into OpenSSL configuration file and
all its simplicity.

Why So Complicated?
-------------------
I do do believe that the OpenSSL configuration file was originally designed to
perform testing and fuzzing of its many settings; later, it became the post de
facto configuration for its various certificate creations.

So when you execute `openssl s_client` or `openssl s_server`, a whole new keyword set of OpenSSL configuration gets used (other than the default ones that we all are familiar with that is in `/etc/ssl` (or `/etc/pki/tls` for RedHat).

Meta keywords
=============
The meta keywords used in OpenSSL configuration file is:

  - `.pragma` - includes other OpenSSL configuration file
  - `.include` - includes other OpenSSL configuration file

A working example of an include statement is:

    .include=conf-includes
    .include conf-includes
    .include [.conf-includes]

ENV keywords
============
`ENV` is a prefix qualifier that is used to take a shell environment value and
use it within its configuration file.

You will see something like:

    ca_dir = $ENV::HOME/ca

Which is to assign a value of `$HOME/ca` to `ca_dir`.

Some commonly used ENV variables are:

  - `CN` - alias for `commonName`, often used as `CN = $ENV::CN`
  - `HOME`, commonly in many `*_dir` and `*dir` keywords
  - `RANDFILE`, commonly within `[ca]` section

Most promiment of the reserve keywords that OpenSSL MUST expect
is the assignment of the `distinguished_name` to another section of your own
choosing (commonly `req_distinguished_name`).

Recognized Suffixes
===================

Sometimes, the `openssl` program will leverage suffixes to give a variable name
some additional qualifiers and restrictions.

Suffixes that are `openssl`-recognized are:

  - `*_value` - useful for NOT prompting the user for its value
  - `*_default` - Appears during prompts as a default value during `prompt=no`
  - `*_max` - Restrict length of field to this number of characters.
  - `*_min` - Ensures that a minimum number of characters are typed in

Pre-defined Values
==================

There are few pre-defined values available but often are limited to its scope of
the group of keywords.

Such group of keywords like `distinguished_name` would have the following
pre-defined values:

  - `match` - do not go any further if names do not match parent CA name's value
  - `optional` - prompt for this value without a default value
  - `supplied` - prompt for SOME value but never an empty field.

Default Settings
================
OpenSSL makes uses of default settings by assigning a section name to one of the
following keywords:

  - `attributes`
  - `default_policy` - if requester did not use a `-policy` CLI option
  - `policy` - always use the policy's section name that is assigned to it
  - ` `

Section Selectors
=================

A way to add selectable policy is to pass a `-policy <name>` and
the section `[ policy_<name> ]` will be included.

Built-In Section Names
======================

For certificate creations, the built-in section names are:

  - `[ ca ]`  (BASE\_SECTION), required
  - `[ req ]`, required
  - `[ providers ]`, optional

Only for TLS network connections, the built-in section names in `openssl.cnf` configuration file that are being used are:

  - `[ connection ]`, optional
  - `[ tls ]`, optional
  - `[ credentials ]`, optional
  - `[ verification ]`, optional
  - `[ commands ]`, optional
  - `[ enrollment ]`, optional

Request section
=====================
The `openssl req` command evokes the `[req]` section along with any pre-section
value settings in `openssl.cnf`

Keywords that are used under `[req]` and `[*_req]` sections are:

  - `attributes`
  - `countryName` or `C`
  - `countryName_default`
  - `countryName_min`
  - `countryName_max`
  - `default_bits`
  - `default_keyfile`
  - `default_md`
  - `distinguished_name`
  - `encrypt_rsa_key`
  - `prompt = no`
  - `string_mask`
  - `x509_extensions`

During `openssl req` request certificate creation, one of the commonly used
keywords are:

  - `req_extensions`
  - `x509_extensions`  # aka V3 extension

Keywords under `*_extensions` are:

  - `countryName` (or `C`)
  - `organizationName` (or `O`)
  - `commonName` (or `CN`)

Base CA section
=====================
The `openssl ca` command evokes the `[ca]` section.

`ENV_DEFAULT_CA` is `default_ca`.

Keywords under `ca` and `*_ca` are:

  - `cert_opt` - Holds the name, often to `ca_default` (ENV_CERTOPT)
  - `certificate`  (ENV_CERTIFICATE)
  - `copy_extensions` (ENV_EXTCOPY)
  - `crl_extensions` (ENV_CRLEXT)
  - `crlnumber` - positive integer for CRL serial number (ENV_CRLNUMBER)
  - `database` - filespec of a text file holding its current serial number (ENV_DATABASE)
  - `default_crl_hours` - positive integer of how long to certify revocations (ENV_DEFAULT_CRL_HOURS)
  - `default_crl_days` - positive integer of how long to certify revocations (ENV_DEFAULT_CRL_DAYS)
  - `default_days` - positive integer of how long to certify for (ENV_DEFAULT_DAYS)
  - `default_enddate` - positive integer of when NOT to certify for (ENV_DEFAULT_ENDDATE)
  - `default_md` - `default` is compiler-option (ENV_DEFAULT_MD)
  - `default_email_in_dn` - `default` is compiler-option (ENV_DEFAULT_EMAIL_DN)
  - `default_startdate` - positive integer of when to certify for (ENV_DEFAULT_STARTDATE)
  - `msie_hack` (ENV_MSIE_HACK)
  - `name_opt` (ENV_NAMEOPT)
  - `new_certs_dir` - dirspec of new certificates; used by `openssl new`
  - `oid_file` - filespec to OIDs
  - `policy` - The CA policy section to support - CLI '-policy' option (ENV_POLICY)
  - `preserve` - Keep passed DN ordering (ENV_PRESERVE)
  - `private_key` - filespec of new key; used by `openssl new` (ENV_PRIVATE_KEY)
  - `rand_serial`  (ENV_RAND_SERIAL)
  - `serial`  (ENV_SERIAL)
  - `unique_subject`  (ENV_UNIQUE_SUBJECT)
  - `x509_extensions` - points to the next section for extensions (ENV_EXTENSIONS)

  - `certs` - dirspec of where certificates go into
  - `crl_dir` - dirspec of where CRL go into
  - `dir` - parent directory of this CA
  - `name_opt` - Holds the name, often to `ca_default`

Certification section
=====================
The certification section may be:

  - `usr_cert`
  - `ocsp_cert`
  - `dh_cert`
Keywords under `*_cert` are:

  - `basicConstraints`
  - `keyUsage`
  - `subjectKeyIdentifier`
  - `authorityKeyIdentifier`

Keywords under `*_ca` are:

  - `basicConstraints`
  - `keyUsage`
  - `subjectKeyIdentifier`
  - `authorityKeyIdentifier`

Sect section
=====================
The `openssl s_client` command evokes the `[sect]` section.

Section name under `sect` and `*_sect` are:

  - `provider_sect`
  - `ssl_sect`
  - `server_sect` is used by `openssl s_server`
  - `test_sect`

Miscellaneous 
=====================

OpenSSL startup
---------------

`openssl_conf` varname is used by OpenSSL, often defined to `openssl_init`

Keywords used within `openssl_conf`

  - `providers`
  - `default`
  - `activate`

OpenSSL test suite
------------------

- `ssl_conf` varname is used by OpenSSL test suite.
- `testapp` varname is used by OpenSSL test suite.
- `config_diagnostics` varname is used by OpenSSL test suite.


BITS               "default_bits"
KEYFILE            "default_keyfile"
PROMPT             "prompt"
DISTINGUISHED_NAME "distinguished_name"
ATTRIBUTES         "attributes"
STRING_MASK        "string_mask"

OTHER SHELL ENVIRONMENT VARIABLES USED
======================================
The test suite also uses the following shell environment names as well:

  - `ADD_DEPENDS_DEBUG`, util/add-depends.pl
  - `CT_DIR`
  - `CERTS_DIR`
  - `DEBUG`, util/fix-deprecation.pl
  - `EXE_SHELL`
  - `FIPSKEY`
  - `NO_FIPS`
  - `NO_LEGACY`
  - `OPENSSL_CMP_CONF`
  - `PATH` used during compiling/linking/building
  - `SSL_CERT_DIR` used during compiling/linking/building
  - `VERBOSE`
  - `V`

USAGE
========
The above enabled me to create parseable CA blocks for my test network having many CA certificates.  And I wrote all the comolicated parts in bash SHELL scripts.  You can find them here [github.com/egberts/tls-ca-manage](https://github.com/egberts/tls-ca-manage)
