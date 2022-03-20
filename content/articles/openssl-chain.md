title: Chaining of CA Certificates in OpenSSL
date: 2022-03-19 16:51
status: published
tags: OpenSSL
category: HOWTO
summary: How to work with and validate with CA Chain files.
slug: openssl-chain
lang: en
private: False

You have a PKI certificate.  You're unsure whether it is currently valid.  How do one go about doing this validation step?

Assuming you are vaguely aware about the basic relationship between Root CA, Intermediate CAs, and its end-use certificates, we will jump into CA chains.

Like a link in the chain, each link is attached to the next link representing this strong bond of staying together.  This bond of staying together at PKI level gets formed by signing details about a CA using public key and private key of the parent node, except when the parent is the Root CA.  

In the case of a first link, Root CA self-signs with itself and its public key are stored in well-known places like each web browsers.

Chain File Content
==================

The file format of a certificate file is in one form of an ASCII text format called PEM using UNIX newline convention.  There are 3 other formats but mostly, certificate administrators work with PEM and DER format.  Here we focus on PEM format.

PEM have a header in the first line and a header in the last line of the text file.  And a bunch of multi-line characters in between representing the base64 content of binary ASN.1 notations containing multiple pairs of OID and its value.

A single chain file has one or more PEM appended back-to-back.  A 'chain' file that has only ONE PEM may still be called a chain because the end-use certificate wants its parent CA PEM alongside with it:

```console
ls -1 *.pem
webserver.cert.pem
webserver.key.pem
webserver.csr.pem
webserver.chain.pem   # this one has the signer's PEM (parent CA)
webserver.fullchain.pem  # this one has all signers of all parents' PEM.
```

The ordering of PEM inside a chain file depends on the application's need.

Most applications want the chain file to start with all parent CA (and it's parent's parent, ad infinitium) along with the certificate's PEM at the end of file.

If you already have the fullchain, one can check the ordering of the CAs from the fullchain file:

```console
$ openssl crl2pkcs7 -nocrl -certfile webserver-fullchain.pem \
    | openssl pkcs7 -print_certs -noout
subject=/C=Countrycode/ST=State/O=Organization/CN=wwww.example.invalid
issuer=/C=Countrycode/ST=State/O=Organization/CN=the name of the intermediate CA

subject=/C=Countrycode/ST=State/O=Organization/CN=the name of the intermediate CA
issuer=/C=Countrycode/ST=State/O=Organization/CN=the name of the CA
```

In this output, the ordering should be:

* subject: Server certificate file subject (your FQDN usually)
* issuer: Intermediate CA certificate name
* subject: Intermediate CA certificate name (this should match with the previous issuer value)
* issuer: CA certificate subject


File Name Convention
====================

When we see the file name having a `chain` notation, this typically refers to the immediate parent CA (or one who signed this certificate).

For a full chain length (going from end-use certificate to intermediate(s) to Root CA), the file name notation of `fullchain` gets used here.

An example of filenames having chain are:

```console
ca-root.pem
ca-intermediate-chain.pem  # only has one parent PEM 
ca-webserver-fullchain.pem  # has all ancestral CA PEMs  # PKI-centric
ca-webserver-bundle.pem     # has all ancestral CA PEMs  # web-centric 
```

Verification of a Chain
=======================

Assuming that the `fullchain` has all the ancestral CA PEMs put in proper order, we can then verify the whole chain for a web server certificate:

```console
$ openssl verify -trusted ../rootCA.crt.pem -untrusted /etc/letsencrypt/live/FQDN/chain.pem webserver.crt.pem
```

References
==========

* https://medium.com/@superseb/get-your-certificate-chain-right-4b117a9c0fce
* [Resolve the fullchain over network](https://github.com/zakjan/cert-chain-resolver)
* http://giantdorks.org/alain/shell-script-to-check-ssl-certificate-info-like-expiration-date-and-subject/
* http://prefetch.net/code/ssl-cert-chec
* [ssh-cert-chain-check.sh](https://gist.github.com/hilbix/bde7c02009544faed7a1)
* [Cert\_Tree (Python)](https://github.com/jkolezyn/cert_tree)

