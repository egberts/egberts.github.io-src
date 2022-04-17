title: Exim4 is Dead-On-Arrival
date: 2022-04-16 12:41
status: published
tags: Exim4, SMTP
category: research
lang: en
private: False

# Wait, Uh? Exim4 can do What?

A nice blurb on the [Encrypted SMTP connections using TLS/SSL](https://www.exim.org/exim-html-current/doc/html/spec_html/ch-encrypted_smtp_connections_using_tlsssl.html) on Exim4 website:

For TLS version 1.3 the control available is less fine-grained and Exim does not provide access to it at present. The value of the tls_require_ciphers option is ignored when TLS version 1.3 is negotiated.

Wow....

As of writing the library default cipher suite list for TLSv1.3 is
```
TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256
```

# Security Ramification

Looks like Exim4 is falling behind the curve (possibly due to complexity of setting algorithms between OpenSSL and GnuTLS.)

(Dumping all efforts toward Exim4; reverting back to Postfix)

