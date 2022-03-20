title: OpenSSL Configuration File by Section
date: 2022-03-19 09:15
status: published
tags: OpenSSL
category: research
summary: OpenSSL config file organized by sections.
slug: openssl-config-by-section
lang: en
private: False

The basic layout of the openssl.cnf file are as given below but with respect to section, sectionalization, and reference by section.

Generic section:
----------------

* `[ default ]`
* `[ ca ]`
* `[ req ]`

`[ default ]` Attributes
========================
Default attributes may start at the beginning of the `openssl.cnf` configuration file before any section (as denoted by a pair of square-brackets `[ xxxx ]`) begins or be clustered together under a `[default]` section, or across both.

`[ default ]` Directories
-------------------------
[jtable]
Attribute, Description, Section
`HOME`, file specification of a current working directory for all the files referenced later therewithin, [default]
[/jtable]

`[ default ]` Files
-------------------------
[jtable]
Attribute, Description, Section
`RANDFILE`, file specification of a file holding the random seed (good for recreating unit tests); typically set to `$ENV::HOME/.rnd` or `$dir/private.rand`, [default,ca,req]
`oid_file`, file specification to a file containing the OID attribute settings; uses `$ENV::HOME/.oid` file as a default?, [default,ca]
[/jtable]

`[ default ]` Section Assignment
-------------------------
[jtable]
Attribute, Description, Section
`openssl_conf`, the top-most section name to take in new settings at a new OpenSSL-wide scoping level; including all OpenSSL modules such as TLS/SSL, [default]
`ssl_conf`, section name to take in new settings for TLS/SSL module; Used only by `openssl s_client` or `openssl s_server`, [default]
`engines`, section name to the `engine` module, [default]
`stbl_section`, section name to the ASN.1 module, [default]
`oid_section`, section name to a new section containing the oid-related attribute settings, [default]
`alg_section`, section name to the EVP module, [default]
`asn1`, section name to a new section containing the selected ASN1 attributes; used only by `openssl asn1pars` command., [default,asn1pars]
[/jtable]

`[ ssl_conf ]` Attributes 
-------------------------
[jtable]
Attribute, Description, Section
`system_default`, section name to a new section containing the TLS/SSL-relatd attribute settings such as `MinProtocol=TLSv1.3`, `CipherSuites`, or `Options=-SessionTicket,MiddleboxCompat`, [ssl]
[/jtable]

See man page `SSL_CONF_cmd_value_type.3ssl` for more TLS/SSL options under `[ ssl_conf ]` section.

`[ engine ]` Attributes 
-------------------------
[jtable]
Attribute, Description, Section
`engine_id`, name of the FIPS engine, [engine]
`soft_load`, alternate name of the FIPS engine, [engine]
`dynamic_path`, alternate name of the FIPS engine, [engine]
`default_algorithms`, a CSV string of the name of desired (but supported) algorithms to use with the FIPS, [engine]
[/jtable]

Other `engine` keyvalues encountered are `SO_PATH`, `LIST_ADD`, `LOAD`, `EMPTY`, `init`. 

`[ default ]` Attributes - EVP
-------------------------
[jtable]
Attribute, Description, Section
`fips_mode`, `yes`/`no`, [engine]
[/jtable]

Found in '[ca]':
=======================

Section names within [ca]
---------------------------
[jtable]
Attribute, Description, Section
`default_ca`, section name to a new section containing [CA]-related attributes to be used by 'openssl ca' and can be overridden by `-name` CLI option, [ca]
`x509_extensions`, section name to a new section containing the X509v3 extension attributes to add to the cert; `-extensions` CLI option overrides this setting., [ca]
`policy`, section name to a new section that contains attributes that enforces which distinguished names to keep or force supplied or copy.; `-policy` CLI option overrides this setting, [ca]
`crl_extensions`, section name to a new section that holds CRL-related X509v3-only attributes settings; `-crlexts` overrides this setting;, [ca]
[/jtable]

Directories within [ca]
---------------------------
[jtable]
Attribute, Description, Section
`database`, directory specification to the main working directory that holds `openssl`-generated database files, [ca]
`certs`, directory specification to the holding area for newly-issued certificate PEM file; not clear if `CApath` CLI option overrides this setting (TBD); `-no-CApath` does overrides this setting, [ca]
`crl_dir`, directory specification to the holding area for CRL-related files, [ca]
`new_certs_dir`, directory specification to the holding area for newly-issued certificate PEM files, [ca]
[/jtable]

Files within [ca]
-----------------
[jtable]
Attribute, Description, Section
`certificate`, file specification to a file containing the CA certificate in PEM format; not sure if `-cert` CLI option overrides this setting? (TBD), [ca]
`private_key`, file specification to a file containing the CA private key in PEM format; `-keyfile` CLI overrides this setting, [ca]
`serial`, file specification to a file containing the current serial number text file; `-create-serial` can reset this; `-rand_serial` ignores this file., [ca]
`crl`, file specification to a file containing the current CRL PEM file, [ca]
`crlnumber`, file specification to a file containing the base 10 number for serial number to the CRL certificateion, [ca]
`oid_file`, file specficiation to a file containing the OIDs; uses `$ENV::HOME/.oid` file as a default?, [default,ca]
[/jtable]

Attributes options within [ca]
------------------------------
[jtable]
Attribute, Description, Section
`default_days`, how long to certify for; `-days` overrides this setting., [ca]
`default_startdate`, options are `today` or a date format of `YYMMDDHHMMSSZ`; `-startdate` CLI option overrides this setting., [ca]
`default_enddate`, a date format of `YYMMDDHHMMSSZ`; `-enddate` CLI option overrides this setting., [ca]
`default_md`, default for non-EC public key message digest; can be `default` or any option listed in `openssl dgst -list`; using one of the listed CLI options shown by `openssl dgst -list` overrides this setting.; if EC algorithm is used, this attribute gets ignored, [ca,req]
`preserve`, keep the ordering of distinguished names or not as the DN get copied from CSR to CA certificate., [ca]
`name_opt`, options only for the Subject Name (SN) are `multiline` `-esc_msb` `utf8` or `ca_default`; more intensive options are `esc_2253` `esc_2254` `esc_ctrl` `esc_msb` `use_quote` `utf8` `ignore_type` `show_type` `dump_all` `dump_nostr` `dump_der` `compat` `sep_comma_plus` `sep_comma_plus_space` `sep_semi_plus_space` `sep_multiline` `dn_rev` `nofname` ` sname` `lname` `align` `oid` `space_eq` `dump_unknown` `RFC2253` `oneline` `multiline` `ca_default`, [ca]
`cert_opt`, options only for the distinguished names (DN); options are: `compatible` `ca_default` `no_header` `no_version` `no_serial` `no_signame` `no_validity` `no_subject` `no_issuer` `no_pubkey` `no_extensions` `no_sigdump` `no_aux` `no_attributes` `ext_default` `ext_error` `ext_parse` `ext_dump`, [ca]
`utf8`, `yes`/`no` value for UTF8 support, [ca]
`copy_extensions`, options are `none` `copy` or `copyall`, [ca]
`email_in_dn`, options are `no` or a valid email address, [ca]
`default_email_in_dn`, options are `no` or a valid email address, [ca]
`default_crl_days`, how long before next CRL; `-crldays` or `-crlhours` and `-crlsec` overrides this setting., [ca]
`default_crl_hours`, how long before next CRL; `-crldays` or `-crlhours` and `-crlsec` overrides this setting., [ca]
`default_crl_seconds`, how long before next CRL; `-crldays` or `-crlhours` and `-crlsec` overrides this setting., [ca]
`unique_subject`, `yes`/`no` value; recommended to say `no` for an easier rollover; default is `yes`, [ca]
[/jtable]



Found in '[req]':
==================
Section names within [req]
---------------------------
[jtable]
Attribute, Description, Section
`req_extensions`, section name to a new section for attribute settings used by 'openssl req' command and overridden by `-reqexts` CLI option, [ca]
`distinguished_name`, section name to a new section to contain distinguished names., [req]
`x509_extensions`, section name to a new section containing X509v3 extension attributes to add to the self-signed cert (ie. RootCA); `-extensions` CLI overrides this setting.; only used for self-signed within [req], [ca]
`attributes`, section name to a new section containing attributes commonly holding `challengePassword*` attributes, [req]
`default_csr`, section name to a new section containing CSR-related attribute for use with 'openssl req' command and overridden by `-name` CLI, [req]
[/jtable]

Directories within [req]
---------------------------
There are no attributes related to directory path within the request `[ req ]` section.

Files within [req]
---------------------------
[jtable]
Attribute, Description, Section
`default_keyfile`, file specification of a file that holds the private key used in request (CSR) certificate., [req]
[/jtable]

Attributes options within [req]
------------------------------
[jtable]
Attribute, Description, Section
`default_bits`, number of bits for non-EC algorithms; if EC algorithm is selected, then this attribute gets ignored., [req]
`default_md`, default for non-EC public key message digest; can be `default` or any option listed in `openssl dgst -list`; using one of the listed CLI options shown by `openssl dgst -list` overrides this setting.; if EC algorithm is used, this attribute gets ignored, [ca,req]
`encrypt_key`, `yes`/`no` value as to whether to wrap a digest around the key using the `default_md` digest algorithm, [req]
`string_mask`, # This sets a mask for permitted string types. There are several options.  default is `PrintableString` `T61String` and `BMPString`; pkix compliance use `PrintableString` and `BMPString` (PKIX recommendation before 2004); For utf8only: only `UTF8Strings` (PKIX recommendation after 2004); For nombstr: `PrintableString` and `T61String` (no BMPStrings or UTF8Strings).; `MASK:XXXX` is a literal mask value.; WARNING: ancient versions of Netscape crash on `BMPStrings` or `UTF8Strings`., [req]
`input_password`, string containing a password for the private key if not present then it will be prompted for; `-passin` overrides this setting., [req]
`output_password`, string pattern containing a password for the private key if not present then it will be prompted for
`encrypt_rsa_key`, OBSOLETED; use `encrypt_key` instead, [req]
[/jtable]


Found in section name by [req]attributes=
-----------------------------------------

```ini
challengePassword               = A challenge password                 
challengePassword_min           = 4
challengePassword_max           = 20
```

See [OpenSSL Password]({filename}openssl-password.md) for more details.

Distinguished Names
-------------------
Distinguished Names (DN) are declared in a section whose section name are assigned to the `distinguished_name=` assignment commonly found under [req]-related sections.

DN attributes are defined in two different ways, depending on the `prompt=` attribute settings :

If the `prompt=yes` then the following section is the default (as found in `/usr/lib/ssl/openssl.cnf`:
```ini
[ req_distinguished_name ]
countryName                     = Country Name (2 letter code)
countryName_default             = AU
countryName_min                 = 2
countryName_max                 = 2

stateOrProvinceName             = State or Province Name (full name)
stateOrProvinceName_default     = New South Wales

organizationName		= Organization Name (eg, company)
organizationName_default	= CAcert Inc.

organizationalUnitName		= Organizational Unit Name (eg, section)
organizationalUnitName_default	= http://www.CAcert.org

commonName			= Common Name (eg, YOUR name)
commonName_default		= CAcert Inc. Signing Authority
commonName_max			= 64
```

See [To Prompt or Not to Prompt in OpenSSL]({filename}openssl-prompt.md) for more details on `prompt=` settings.


Certificate Policies
--------------------

```ini
[ my_cert_policy ]
CPS                             = "http://www.CAcert.org/index.php?id=10"
policyIdentifier                = my_policy_oid
```


X509v3 extensions
=================

There are many X509v3 extensions.  Most are commonly used and are listed here with their commonly-used acronym:

* `authorityInfoAccess` (AIA)
* `authorityKeyIdentifier` (AKI)
* `basicConstraints` (BC)
* `certificatePolicies` (CP)
* `subjectAltName` (SAN)
* `keyUsage` (KU)
* `extendedKeyUsage` (EKU)
* `issuerAltName` (IAN)
* `subjectKeyIdentifier` (SKI)
* `issuingDistributionPoint` (IDP)
* `crlDistributionPoint` (CDP)
* `proxyCertInfo` (PCI)

What X509v3 extension settings to use for each type of certificates are detailedin [{filename}openssl-x509v3.md]

authorityInfoAccess (AIA) 
-------------------------

Some X509v3 extension settings that authorityInfoAccess (AIA) can take:

```ini

authorityInfoAccess = caIssuers
authorityInfoAccess = OCSP
authorityInfoAccess = DNS:example.com
authorityInfoAccess = IP:127.0.0.1
authorityInfoAccess = URI:http://127.0.0.1:8080
authorityInfoAccess = email:johndoe@example.com
authorityInfoAccess = caIssuers;OCSP;URI:http://127.0.0.1:8080
```
AIA are used only with `openssl ca`? (TBD)

authorityKeyIdentifier (AKI)
----------------------------
Some X509v3 extension settings that authorityKeyIdentifier (AKI) can take:
```ini
authorityKeyIdentifier=keyid:always,issuer
```

AKI are used only with `openssl ca`? (TBD)

subjectKeyIdentifier (SKI)
-----------------------------------------------------
Valid values for SKI are `hash` or a hexidecimal number.

SKI are used only with `openssl ca`? (TBD)


Issuer X509v3 Extension Attributes
==================================
The following X509v3 extension attributes only applies:

* when using the `openssl ca` and
* referenced by the selected section name under `[ ca ]` section

```ini
issuingDistributionPoint=[critical,]@my_issuer_dp_section
```

An example of an Issuer X509v3 section is:

```ini
issuingDistributionPoint=[critical,]@my_issuer_dp_section

[my_issuer_dp_section]
indirectCRL=TRUE
CRLissuer=dirName:my_issuer_distinguished_name_section
fullname=URI:http://ca.myhost.com/myca.crl
onlysomereasons=keyCompromise, CACompromise
onlyAA=FALSE
onlyCA=TRUE
onlyuser=FALSE

[my_issuer_distinguished_name_section]
C=UK
O=Organization
CN=Some Name
```



CRL X509v3 Extension Attributes
===============================

The following X509v3 extension attributes only applies:

*  by the selected section name under `[ ca ]` section and 
*  using the `-gencrl` CLI option during `openssl ca` command

```ini
crlDistributionPoint=[critical,]@my_crl_dp_section
```

It is a PKIX recommendation to include the `issuingDistributionPoint` along with the CRL certificate.

An example of CRL X509v3 section is:
```ini
crlDistributionPoint=critical,@my_crl_dp_section

[my_crl_dp_section]
CRLissuer=dirName:my_crl_distinguished_name_section
fullname=URI:http://ca.myhost.com/myca.crl
onlysomereasons=keyCompromise, CACompromise
onlyAA=FALSE
onlyCA=TRUE
onlyuser=FALSE

[my_crl_distinguished_name_section_name]
C=UK
O=Organization
CN=Some Name
```

Other X509v3 attributes
---------------------------------
Have not the time to document the rest.

```ini
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
certificatePolicies             = @cert_policy_section_ca
subjectAltName=email:copy
issuerAltName=issuer:copy
proxyCertInfo=critical,language:id-ppl-anyLanguage,pathlen:3,policy:foo
crlDistributionPoints=URI:http://crl.abc.com/my.crl,URI:http://crl.com/abc.crl
crlDistributionPoint=[critical,]@my_crl_dp_section
issuingDistributionPoint=[critical,]@my_issuer_dp_section

#nsCertType = objsign, sslCA, emailCA
#nsComment                       = "OpenSSL Generated Certificate"
#nsCaRevocationUrl              = http://www.domain.dom/ca-crl.pem
#nsBaseUrl
#nsRevocationUrl
#nsRenewalUrl
#nsCaPolicyUrl
#nsSslServerName
```

Other OpenSSL details may be found in [tag:OpenSSL]({tag}OpenSSL).
