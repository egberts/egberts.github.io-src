title: Which Certificate Uses What X509v3 Extensions
date: 2022-03-19 07:18
status: published
tags: OpenSSL, X509v3, environment variables
category: research
summary: So you want to make a blank-type of PKI certificate but unsure of what X509v3 extensions to use.
lang: en
private: False

There are several types of PKI certificates used today:

* Web TLS
 * TLS server
 * TLS client, used in mutual TLS (mTLS) rarely
* Certificate Authority (CA)
 * Root CA
 * Intermediate CA
 * Crossover CA
* Code Signing
* Timestamping
* Certificate Revocation List (CRL)
* Online Certificate Status Protocol (OCSP)
* 

You can add X.509 extensions to a certificate at two different stages of the creation of PKI certification:

* When creating the Certificate Signing Request (CSR)
* When signing the certificate using the Root (or Intermediate) CA certificate
 * using `openssl ca`
 * using `openssl x509`


With the X509v3 extensions and its attributes detailed in [OpenSSL config file by section]({filename}openssl-conf-by-section.md), this article will assign them to each type of certificate:

Root CA
=======
Following the progression from top to bottom, Root CA is at the top.

Root CA requires the following X509v3 extensions:

```ini
# BC must be present
# BC must be marked `critical`
# BC must have a `cA`
# `cA` field must be set TRUE
# pathLenConstraint may not be present
# pathLenConstraint must be non-zero for a non-leaf CA node
basicConstraints=critical,CA:TRUE

subjectKeyIdentifier=hash

# if Root CA key is used to sign OCSP responses
keyUsage=critical,digitalSignature,keyCertSign,cRLSign
# if Root CA key is NOT being used to sign OCSP responses
#keyUsage=critical,keyCertSign,cRLSign
# absolutely no certificatePolicies here  (CAB BR-1.7.6 s7.1.6.2)
# absolutely no extendedKeyUsage here

authorityKeyIdentifier=keyid:always,issuer
```

Intermediate CA
================

Non-Leaf Intermediate CA
------------------------
Following the progression from top to bottom, Intermediate CA that does NOT serve certificates are called non-leaf Intermediate CA and is next in line.

Its parent CA must have at least `critical,keyCertSign` value in `keyUsage` X509v3 attribute.

Non-leaf node Intermediate CA requires the following X509v3 extensions:

```ini

# BC must be present
# BC must be marked `critical`
# `ca` field must be set TRUE
# pathLenConstraint may not be present
# pathLenConstraint must be non-zero for a non-leaf CA node
basicConstraints=critical,CA:TRUE,pathLen=1

subjectKeyIdentifier=hash

# AKI is required
# AKI must NOT be marked `critical`
# AKI must set keyid
# AKI may set issuer
# AKI must not contain `authorityCertIssuer`
# AKI must not contain `authorityCertSerialNumber`
authorityKeyIdentifier=keyid:always,issuer

# KU must be present
# KU must be marked `critical`
# KU must contain `keyCertSign`
# KU must contain `cRLSign`
# KU must contain `digitalSignature` if Root CA key is used to sign OCSP responses
keyUsage=critical,digitalSignature,keyCertSign,cRLSign

# if Root CA key is NOT being used to sign OCSP responses
#keyUsage=critical,keyCertSign,cRLSign

# EKU is optional for non-leaf CA nodes
# EKU is mandatory for leaf CA nodes by Mozilla
# EKU may be marked `critical` for non-leaf CA nodes
# EKU SHALL be marked `critical` for leaf CA nodes
# EKU SHALL NOT contain `anyExtendedKeyUsage` for a leaf CA nodes.
# EKU may contain `anyExtendedKeyUsage` if within same org as parent CA.
# EKU MUST carry same settings as their issued certificates by this CA.
extendedKeyUsage=

# absolutely no certificatePolicies here  (CAB BR-1.7.6 s7.1.6.2)

# AIA should be present
# AIA should contain caIssuer or URI:
# AIA should contain OCSP or URI:
authorityInformationAccess=caIssuer,OCSP

# For Cross Certificates that share a Subject Distinguished Name and Subject Public
Key with a Root Certificate operated in accordance with these Requirements, this
extension MAY be present. 

If present for XCC, this extension SHOULD NOT be marked
critical. This extension MUST only contain usages for which the issuing CA has
verified the Cross Certificate is authorized to assert. This extension MAY contain
the anyExtendedKeyUsage [RFC5280] usage, if the Root Certificate(s) associated
1Non‐critical Name Constraints are an exception to RFC 5280 (4.2.1.10), however, they MAY be used until
the Name Constraints extension is supported by Application Software Suppliers whose software is used by
a substantial portion of Relying Parties worldwide.
pg. 69
with this Cross Certificate are operated by the same organization as the issuing
Root Certificate.


```

Cross-Cert Intermediate CA
--------------------------
Following the progression from top to bottom, Cross-Cert Intermediate CA is next in line.

Its parent CA must have at least `critical,keyCertSign` value in `keyUsage` X509v3 attribute.

Cross-Cert Intermediate CA requires the following X509v3 extensions:

```ini

# BC must be present
# BC must be marked `critical`
# `ca` field must be set TRUE
# pathLenConstraint may be present
# pathLen=X where X is the number of nodes away from end-leaf Intermediate CA
basicConstraints=critical,CA:TRUE,pathLen=1
subjectKeyIdentifier=hash

# AKI is required
# AKI must NOT be marked `critical`
# AKI must set keyid
# AKI may set issuer
# AKI must not contain `authorityCertIssuer`
# AKI must not contain `authorityCertSerialNumber`
authorityKeyIdentifier=keyid:always,issuer

# KU must be present
# KU must be marked `critical`
# KU must contain `keyCertSign`
# KU must contain `cRLSign`
# KU must contain `digitalSignature` if Root CA key is used to sign OCSP responses
keyUsage=critical,digitalSignature,keyCertSign,cRLSign

# if Root CA key is NOT being used to sign OCSP responses
#keyUsage=critical,keyCertSign,cRLSign

# absolutely no certificatePolicies here  (CAB BR-1.7.6 s7.1.6.2)

# AIA should be present
# AIA should contain caIssuer or URI:
# AIA should contain OCSP or URI:
authorityInformationAccess=caIssuer,OCSP

# EKU is optional for non-leaf CA nodes
# EKU is mandatory for leaf CA nodes by Mozilla
# EKU may be marked `critical` for non-leaf CA nodes
# EKU SHALL be marked `critical` for leaf CA nodes
# EKU SHALL NOT contain `anyExtendedKeyUsage` for a leaf CA nodes.
# EKU MUST carry same settings as their issued certificates by this CA.
# EKU may contain `anyExtendedKeyUsage` if within same org as parent CA.
extendedKeyUsage=anyExtendedKeyUsage
```

TLS Signing CA
----------
Following the progression from top to bottom, End-Node Intermediate CA for TLS Signing CA is a leaf-node CA and is at the end of the line before signing any end-use TLS-based certificates.

Its parent CA must have at least `critical,keyCertSign` value in `keyUsage` X509v3 attribute.

Its signed certificate must all have the exact same `keyUsage` attribute as this CA have or less.

TLS Signing CA is used for the following types of end-use certificates:

* Email Protection (via Email CA)
* TLS Server (via TLS CA)
* TLS Client (via TLS CA)
* Code Signing (via Software CA)

End-Node Intermediate CA for TLS Signing requires the following additional X509v3 extensions:

```ini
[ signing_ca_ext ]

# BC must be present
# BC must be marked `critical`
# BC shall have 'cA' option
# `cA` field must be set TRUE
# BC shall have pathLenConstraint (`pathLen`)
# pathLen shall be set to 0 for this is a leaf-node CA.
basicConstraints=critical,cA:TRUE,pathLen=0

subjectKeyIdentifier=hash

# AKI is not required
# AKI is often 'keyid:always'

# KU must be present
# KU must be marked `critical`
# KU must contain `keyCertSign`
# KU must contain `cRLSign`
# KU must contain `digitalSignature` if Root CA key is used to sign OCSP responses
keyUsage=critical,digitalSignature,keyCertSign,cRLSign

# EKU shall be present
# EKU shall have the same option as all of its issued certificates
# EKU must NOT have `anyExtendedKeyUsage`.
extendedKeyUsage=serverAuth
extendedKeyUsage=serverAuth,clientAuth
extendedKeyUsage=clientAuth
extendedKeyUsage=X?????????

# AIA should be present
# AIA should contain caIssuer or URI:
# AIA may add OCSP or URI:
authorityInformationAccess=caIssuer

crlDistributionPoints   = @crl_info

```

Email Protection CA
-------------------
Following the progression from top to bottom, Email Protection CA is last CA of a chain before Email Protection certificate.

Email Protection CA requires the following X509v3 extensions:

```ini
# BC must be present
# BC must be marked `critical`
# BC shall have 'cA' option
# `cA` field must be set TRUE
# BC shall have pathLenConstraint (`pathLen`)
# pathLen shall be set to 0 for this is a leaf-node CA.
basicConstraints=critical,CA:TRUE,pathLen=0

subjectKeyIdentifier=hash

# AKI is required
# AKI must NOT be marked `critical`
# AKI must set keyid, may have ':always' suboption
# AKI may set issuer
# AKI must not contain `authorityCertIssuer`
# AKI must not contain `authorityCertSerialNumber`
authorityKeyIdentifier=keyid:always

# KU must be present
# KU must be marked `critical`
# KU must contain `keyCertSign`
# KU must contain `digitalSignature` if `cRLSign` is specified
# KU should contain `cRLSign` if its CA key signs OCSP responses
keyUsage=critical,digitalSignature,keyCertSign,cRLSign

# EKU must be present
# EKU should not be marked `critical`
# EKU shall include `emailProtection`
# EKU shall include `clientAuth`
# EKU may include `anyExtendedKeyUsage`
extendedkeyUsage=emailProtection,clientAuth,anyExtendedKeyUsage

# AIA should be present
# AIA should contain caIssuer or URI:
# AIA should contain OCSP or URI:
authorityInformationAccess=caIssuer,OCSP
```

Code Signing CA (Software)
----------------------------
Following the progression from top to bottom, End-Node Intermediate CA for Code Signing is the last CA on the tree before Code Signing certificate comes into play.

End-Node Intermediate CA for Code Signing requires the following X509v3 extensions:

```ini
# BC must be present
# BC must NOT be marked `critical`
# `ca` field must be set FALSE
# BC must have pathLen 
# pathLen must be set to 0 for this is a leaf-node CA.
basicConstraints=CA:true,pathLen=0

subjectKeyIdentifier=hash

# AKI is required
# AKI must NOT be marked `critical`
# AKI must set keyid:always
# AKI may not set issuer
authorityKeyIdentifier=keyid:always

# KU is required
# KU should be set 'critical'
# KU must have `digitalSignature`
# KU may have `nonRepudiation`
keyUsage=critical,keyCertSign,cRLSign

# EKU shall be present
# EKU should be set 'critical'
# EKU must have 'codeSigning'
# EKU shall have the same option as all of its issued certificates
# EKU must NOT have `anyExtendedKeyUsage`.
extendedKeyUsage=critical,codeSigning

# AIA should be present
# AIA should contain caIssuer or URI:
authorityInformationAccess=caIssuer

# CDP must be mandatory
# CDP must not be `critical`
# CDP must contain URI: to a web page containing CA's CRL service
crlDistributionPoints=URI:http://ocsp.example.invalid/crl
```

TimeStamping Intermediate CA
----------------------------
Following the progression from top to bottom, End-Node Intermediate CA for TimeStamping is next in line.

End-Node Intermediate CA for TimeStamping requires the following X509v3 extensions:

```ini

# BC must be present
# BC must be marked `critical`
# `ca` field must be set TRUE
# BC may have pathLenConstraint
# pathLen must be set to 0
basicConstraints=critical,CA:TRUE,pathLen=0
subjectKeyIdentifier=hash

# AKI is required
# AKI must NOT be marked `critical`
# AKI must set keyid
# AKI may set issuer
# AKI must not contain `authorityCertIssuer`
# AKI must not contain `authorityCertSerialNumber`
authorityKeyIdentifier=keyid:always,issuer

# KU must be present
# KU must be marked `critical`
# KU must contain `keyCertSign`
# KU must contain `cRLSign`
# KU must contain `digitalSignature` if Root CA key is used to sign OCSP responses
keyUsage=critical,digitalSignature,keyCertSign,cRLSign

# if Root CA key is NOT being used to sign OCSP responses
#keyUsage=critical,keyCertSign,cRLSign

# AIA should be present
# AIA should contain caIssuer or URI:
# AIA should contain OCSP or URI:
authorityInformationAccess=caIssuer,OCSP

# EKU is optional
# EKU should not be marked `critical`
# EKU shall use ONLY timeStamping and no other bit setting.
# EKU must not have `anyExtendedKeyUsage`
extendedKeyUsage=timeStamping
```


Identity CA
----------------------------
Following the progression from top to bottom, End-Node Intermediate CA for Identity is next in line.

End-Node Intermediate CA for Identity requires the following X509v3 extensions:

```ini

# BC must be present
# BC must be marked `critical`
# `ca` field must be set TRUE
# BC may have pathLenConstraint
# pathLen must be set to 0
basicConstraints=critical,CA:TRUE,pathLen=0
subjectKeyIdentifier=hash

# AKI is required
# AKI must NOT be marked `critical`
# AKI must set keyid
# AKI may set issuer
# AKI must not contain `authorityCertIssuer`
# AKI must not contain `authorityCertSerialNumber`
authorityKeyIdentifier=keyid:always,issuer

# KU must be present
# KU must be marked `critical`
# KU must contain `keyCertSign`
# KU must contain `cRLSign`
# KU must contain `digitalSignature` if Root CA key is used to sign OCSP responses
keyUsage=critical,digitalSignature,keyCertSign,cRLSign

# if Root CA key is NOT being used to sign OCSP responses
#keyUsage=critical,keyCertSign,cRLSign

# AIA should be present
# AIA should contain caIssuer or URI:
# AIA should contain OCSP or URI:
authorityInformationAccess=caIssuer,OCSP

# EKU is optional
# EKU should not be marked `critical`
# EKU shall use ONLY timeStamping and no other bit setting.
# EKU must not have `anyExtendedKeyUsage`
extendedKeyUsage=timeStamping
```



Certificate (non-CA)
====================
All non-CA certificate are at the bottom of the PKI tree.

TLS Server Certificate 
----------------------

TLS Server Certificate may only sign with CA having `extendedKeyUsage=serverAuth` or `=anyExtendedKeyUsage` option.

TLS Server certificate requires the following additional X509v3 extensions:

```ini
# Used only with `openssl ca`
[ server_ext ]
# BU is not required

subjectKeyIdentifier=hash

# AKI is not required

# KU is mandatory
# KU must have `critical`.
# KU must have `digitalSignature`.
# KU must have `keyEncipherment`.
# KU must NOT have `cRLsign`
# KU must NOT have `keyCertSign`
keyUsage=critical,digitalSignature,keyEncipherment

# EKU is mandatory
# EKU must have either `serverAuth`, or `serverAuth,clientAuth`
# EKU must NOT have `anyExtendedKeyUsage`
extendedKeyUsage=serverAuth

# AIA should be present
# AIA should contain caIssuer or URI:
# AIA should contain OCSP or URI:
authorityInformationAccess=caIssuer,OCSP

# CDP must be mandatory
# CDP must not be `critical`
# CDP must contain URI: to a web page containing CA's CRL service
crlDistributionPoints=URI:http://ocsp.example.invalid/crl

subjectAltName          = $ENV::SAN
```

Environment variable `SAN` makes it easier to pass the FQDN of the host to the command:
```console
$ SAN=DNS:example.test,DNS:www.example.test \
openssl req -new \
    -config etc/server.conf \
    -out certs/green.no.csr \
    -keyout certs/green.no.key
```

TLS Client Certificate
----------------------
Following the progression from top to bottom, TLS Client certificate type is at the bottom (along with a bunch of other end-node CA types).

Can only sign with Root or Intermediate CAs having X509v3 attribute of `extendedKeyUsage=clientAuth` or `extendedKeyUsage=anyExtendedKeyUsage`.

TLS Client certificate requires the following additional X509v3 extensions:

```ini
# BC is optional

subjectKeyIdentifier=hash

# AKI is optional

# KU must be defined
# KU must have `critical`
# KU must have `digitalSignature`
# KU must not have `cRLsign`
# KU must not have `keyCertSign`
keyUsage=critical,digitalSignature

# EKU must be defined
# EKU must not have `critical`
# EKU must have `clientAuth`
# EKU must NOT have `anyExtendedKeyUsage`
extendedKeyUsage=clientAuth

# CDP must be mandatory
# CDP must not be `critical`
# CDP must contain URI: to a web page containing CA's CRL service
crlDistributionPoints=URI:http://ocsp.example.invalid/crl

# SAN must be defined
# SAN must contain 'email:move'
subjectAltName          = email:move

```

OCSP Responder Certificate
--------------------------
Following the progression from top to bottom, OCSP Responder is at the bottom.

OCSP Responder certificate requires the following X509v3 extensions:

```ini
# BC is optional
# 'ca' must always be 'FALSE'
basicConstraints=critical,CA:FALSE

#
subjectKeyIdentifier=hash

# Only issuerAltName and authorityKeyIdentifier make any sense in a CRL
authorityKeyIdentifier=keyid:always,issuer

# KU is required
# KU should be set 'critical'
# KU must have `digitalSignature`
# KU must have `keyEncipherment`
# KU may have `nonRepudiation`
keyUsage=critical,nonRepudiation,digitalSignature,keyEncipherment

# EKU is required
# EKU must have 'OCSPSigning'
# EKU must NOT have `anyExtendedKeyUsage`
extendedKeyUsage=OCSPSigning
```
CRL Cert
--------------------------
Following the progression from top to bottom, CRL is at the bottom.

CRL certificate requires the following X509v3 extensions:

```ini
basicConstraints=critical,CA:TRUE
subjectKeyIdentifier=hash

# Only issuerAltName and authorityKeyIdentifier make any sense in a CRL
authorityKeyIdentifier=keyid:always,issuer

# if Root CA key is used to sign OCSP responses
keyUsage=critical,digitalSignature,keyCertSign,cRLSign
# if Root CA key is NOT being used to sign OCSP responses
#keyUsage=critical,keyCertSign,cRLSign
# EKU must NOT have `anyExtendedKeyUsage`
```

Code Signing Certificate
------------------------
Following the progression from top to bottom, Code Signing certificate type is at the bottom.

Can only sign with CA having the `extendedKeyUsage=codeSigning` X509v3 attribute.

Code Signing certificate requires the following X509v3 extensions:

```ini
[ codesign_reqext ]
# BC should not be used

subjectKeyIdentifier=hash

# AKI may not be defined

# KU must be defined
# KU should be set 'critical'
# KU must have `digitalSignature`
# KU may have `nonRepudiation`
keyUsage=critical,digitalSignature

# EKU must be defined
# EKU should be set 'critical'
# EKU must have 'codeSigning'
# EKU must NOT have `anyExtendedKeyUsage`
extendedKeyUsage=critical,codeSigning

# AIA should not be defined

# CDP may be defined
# CDP must not be `critical`
# CDP must contain URI: to a web page containing CA's CRL service
# crlDistributionPoints=URI:http://ocsp.example.invalid/crl
```

Email Protection Certificate
----------------------------
Following the progression from top to bottom, Email Protection certificate type is at the bottom and only after a CA having `extendedKeyUsage=emailProtection,clientAuth` X509v3 attribute.

Email Protection certificate requires the following X509v3 extensions:

```ini
# BC should not be defined
basicConstraints        = CA:false

subjectKeyIdentifier    = hash

# AKI should not be defined

# KU must be defined
# KU must be set 'critical'
# KU must have `digitalSignature`
# KU must have `keyEncipherment`
# KU may have `nonRepudiation`
keyUsage = critical,digitalSignature,keyEncipherment

# EKU must be defined
# EKU should be set 'critical'
# EKU must have 'emailProtection'
# EKU must have 'clientAuth'
# EKU must NOT have `anyExtendedKeyUsage`
extendedKeyUsage = emailProtection,clientAuth

# AIA should not be defined

# CDP may be defined
# CDP must not be `critical`
# CDP must contain URI: to a web page containing CA's CRL service
# crlDistributionPoints=URI:http://ocsp.example.invalid/crl

# SAN must be defined
# SAN must contain 'email:move'
subjectAltName          = email:move

```

TimeStamping Certificate
----------------------------
Following the progression from top to bottom, TimeStamping certificate type is at the bottom and only after a CA having `extendedKeyUsage=timeStamping` X509v3 attribute.

TimeStamping certificate requires the following additional X509v3 extensions:

```ini
# BC should not be defined
basicConstraints        = CA:false

subjectKeyIdentifier    = hash

# AKI is required
# AKI must NOT be marked `critical`
# AKI must set keyid
# AKI may set issuer
# AKI must not contain `authorityCertIssuer`
# AKI must not contain `authorityCertSerialNumber`
authorityKeyIdentifier=keyid:always

# KU must be defined
# KU must be set 'critical'
# KU must have `digitalSignature`
# KU may have `nonRepudiation`
keyUsage = critical,digitalSignature

# EKU must be defined
# EKU should be set 'critical'
# EKU must have 'timeStamping'
# EKU must NOT have `anyExtendedKeyUsage`
extendedKeyUsage = critical,timeStamping

# AIA should be present
# AIA should contain caIssuer or URI:
# AIA should contain OCSP or URI:
authorityInformationAccess=caIssuer,OCSP

# CDP may be defined
# CDP must not be `critical`
# CDP must contain URI: to a web page containing CA's CRL service
# crlDistributionPoints=URI:http://ocsp.example.invalid/crl

# CP may be defined
# CP must not be empty
[ openssl_init ]
oid_section             = additional_oids
[ additional_oids ]
blueMediumDevice        = Blue Medium Device Assurance, 1.3.6.1.4.1.0.1.7.9
```

Encryption Certificate
----------------------------
Following the progression from top to bottom, Encryption certificate type is at the bottom and only after a CA having `extendedKeyUsage=emailProtection,msEFS` X509v3 attribute.

Encryption certificate requires the following additional X509v3 extensions:

```ini
# BC should not be defined
basicConstraints        = CA:false

subjectKeyIdentifier    = hash

# AKI is required
# AKI must NOT be marked `critical`
# AKI must set keyid
# AKI may set issuer
# AKI must not contain `authorityCertIssuer`
# AKI must not contain `authorityCertSerialNumber`
authorityKeyIdentifier=keyid:always

# KU must be defined
# KU must be set 'critical'
# KU must have `keyEncipherment`
# KU may have `nonRepudiation`
keyUsage = critical,keyEncipherment

# EKU must be defined
# EKU should be set 'critical'
# EKU must have 'emailProtection'
# EKU must have 'msEFS'
# EKU must NOT have `anyExtendedKeyUsage`
extendedKeyUsage = critical,emailProtection,msEFS

# AIA should be present
# AIA should contain caIssuer or URI:
# AIA should contain OCSP or URI:
authorityInformationAccess=caIssuer,OCSP

# CDP may be defined
# CDP must not be `critical`
# CDP must contain URI: to a web page containing CA's CRL service
# crlDistributionPoints=URI:http://ocsp.example.invalid/crl

# CP may be defined
# CP must not be empty
# oid_section             = additional_oids
[ additional_oids ]
blueMediumDevice        = Blue Medium Device Assurance, 1.3.6.1.4.1.0.1.7.9
```

OCSP Responder Certificate
----------------------------
Following the progression from top to bottom, OCSP Responder certificate type is at the bottom and only after a CA having `extendedKeyUsage=OCSPSigning` X509v3 attribute.

OCSP Responder certificate requires the following additional X509v3 extensions:

```ini
# BC should not be defined
basicConstraints        = CA:false

subjectKeyIdentifier    = hash

# AKI is required
# AKI must NOT be marked `critical`
# AKI must set keyid
# AKI may set issuer
# AKI must not contain `authorityCertIssuer`
# AKI must not contain `authorityCertSerialNumber`
authorityKeyIdentifier=keyid:always

# KU must be defined
# KU must be set 'critical'
# KU must have `digitalSignature`
# KU may have `nonRepudiation`
keyUsage = critical,digitalSignature

# EKU must be defined
# EKU should be set 'critical'
# EKU must have 'OCSPSigning'
# EKU must NOT have `anyExtendedKeyUsage`
extendedKeyUsage = critical,OCSPSigning

# AIA should be present
# AIA should contain caIssuer or URI:
# AIA should contain OCSP or URI:
authorityInformationAccess=caIssuer,OCSP

# CDP may be defined
# CDP must not be `critical`
# CDP must contain URI: to a web page containing CA's CRL service
# crlDistributionPoints=URI:http://ocsp.example.invalid/crl

# CP may be defined
# CP must not be empty
[ openssl_init ]
oid_section             = additional_oids
[ additional_oids ]
blueMediumDevice        = Blue Medium Device Assurance, 1.3.6.1.4.1.0.1.7.9
```


References
==========
* https://www.golinuxcloud.com/add-x509-extensions-to-certificate-openssl/#Intermediate_Certificate_Extensions


