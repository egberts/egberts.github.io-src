title: PKI for BIMI
date: 2022-04-14 11:13
status: draft
tags: BIMI, SMTP, mail
category: research
summary: I was curious as to how a new CA infrastructure is forming for this BIMI PKI part.
slug: smtp-bimi-pki
lang: en
private: False

## X509v3 Used in BIMI PKI

A simple dump from https://bimi.entrust.net/entrust.com/certchain.pem then analyzed the X509 data:

```console
wget https://bimi.entrust.net/entrust.com/certchain.pem
# split certchain.pem file into two; entrust1.pem, entrust2.pem
openssl x509 -text -noout -in entrust2.pem
```
has the following X509v3 settings:

* Basic Contraint: TRUE
* Key Usage: Digital Signature, Certificate Sign, CRL Sign
* Extended Key Usage: 1.3.6.1.5.5.7.3.31 (BrandIndicatorforMessageIdentification)

Note: `asn1dump` utility shows nothing for `.31` field here.

BrandIndicatorforMessageIdentification is a valueless OID whose presence indicates that this certificate is being used only for BIMI.

CA authorities that provide BIMI certs are called "Verified Mark Certificate (VMC) CA authority".  Entrust, DigiSign, Comodo are most of the VMC providers.


And one new X509v3 extension for embeddeding the same logo inside the PEM certificate:

* 1.3.6.1.5.5.7.1.12 (Logotype; id-pe-logotype; not parsable by OpenSSL; no value field)

Note: I used `asn1dump` to decipher this `.12` field into a PKIX private extension:
```console
$ as1dump -v cert.pem

...

1036    8:           OBJECT IDENTIFIER logoType (1 3 6 1 5 5 7 1 12)
         :             (PKIX private extension)
    <04 82 04 DE>
1046 1246:           OCTET STRING, encapsulates {
    <30 82 04 DA>
1050 1242:             SEQUENCE {
    <A2 82 04 D6>
1054 1238:               [2] {
    <A0 82 04 D2>
1058 1234:                 [0] {
    <30 82 04 CE>
1062 1230:                   SEQUENCE {
    <30 82 04 CA>
1066 1226:                     SEQUENCE {
    <30 82 04 C6>
1070 1222:                       SEQUENCE {
    <16 0D>
1074   13:                         IA5String 'image/svg+xml'
    <30 33>
1089   51:                         SEQUENCE {
    <30 31>
1091   49:                           SEQUENCE {
    <30 0D>
1093   13:                             SEQUENCE {
    <06 09>
1095    9:                               OBJECT IDENTIFIER
         :                                 sha-256 (2 16 840 1 101 3 4 2 1)
         :                                 (NIST Algorithm)
    <05 00>
1106    0:                               NULL
         :                               }
    <04 20>
1108   32:                             OCTET STRING    
         :                               45 4E 79 48 20 A9 65 7A    ENyH .ez
         :                               D0 C2 DC 52 85 49 FD A6    ...R.I..
         :                               5B 50 97 BA F2 3A DC F8    [P...:..
         :                               8C 39 D6 A7 91 98 2E 17                            
         :                             }
         :                           }
    <30 82 04 7E>
1142 1150:                         SEQUENCE {
    <16 82 04 7A>
1146 1146:                           IA5String
         :                   'data:image/svg+xml;base64,H4sIAAAAAAAAAJVUW2vbMB'
         :                   'R+3mD/4Ux7GliKJMuyXeKOtewGHQwGfe8cLzbz7OC4Sbtfv+'
         :                   '/IqUnKRjeBrU/SuXznIi3f3P1saVcN26bvCmGUFlR1Zb9qun'
         :                   'UhbsfvMhNvzl88X76Ukj5UXTXcjP1wRm9X/beKPrXt7XYMW2'
         :                   'QTZVUc0dfrD/TubtMPI31pb9fyU0cqbF5PTs7IK63p4rZpV6'
         :                   'RfE0nJ9re79TENK+jbzbb6MvTfm7YqxNh093KzFQS63fbsrm'
         :                   '26H4Wox3Fztljs93u1j1U/rBcmz/NFOBW0a6r9RX9XCE2abJ'
         :                   'zwdzDwJ1WrtV6AhgAdouXYjG11/q4bB4RIl/2AkG5G0Fsupi'
         :                   'OQHqpypPtCSM2EwbQtxKvU24vsraB9sxrrQsCpcoLqqlnX47'
         :                   'xcsPoav2fLTd/er/vuQf19GII2fdONIOq88pGxXlmyj6FOVU'
         :                   'IQMCfQGOUpPgFOOXJGJacwgwpGkGDMwFpl6OCTIU1cn6SZ2J'
         :                   'nQBAPNJGVCR9CgR8hn7D7spg49cwyDBZ+r/AAxppU1IJ5ks5'
         :                   'd/JZbms8oEQ1aybM7UBAOF3M7EJhgEjDbH6L+8myxV7qBzwJ'
         :                   'OlPFHZKZ7qqvWckAMOMlZnszzGYfmIys1YP+axKsRnY/SD7s'
         :                   '7VuUpKLpCOrMrRuHmYbaklbh3WmbTS8v9j0Ls60j7Gv+gzl2'
         :                   'TOB8GogdFYpZGGeceCypcwGk1fFoW+wOxAAZJw6FhOOmgiBa'
         :                   '2OdOtAyKu8lnhOWpx4iV6sJWq0CwC6O4luTa9O3R8vfz2ZEZ'
         :                   'eELFuVlpx7DZextOGPAOAA1Gq4ujZWgyoQHKdMTIYUADDbUv'
         :                   'KF02EPSXMTwCEIwYh9MGLySxNzD3NmgLgN2Hl0ROTqL/jpYD'
         :                   'Id7lXectniEhFgQsYSyZXF5eFNg9C0MszQ8HPFwHPWS15FLh'
         :                   'QOT1PEly1RyTY8ASDBs0U8W+6NiIP0kMI1ZkdpsOnhEAmDS8'
         :                   'et00q+O7GyZcxysJBixZ2v2I1Dyrn9QCCR4SHSsINElmh3lJ'
         :                   '0/K/3EFBXh3pLcJnzsQxg+zAbV466NmXuw5Dku5S5N6rnlDJ'
         :                   '+ZNAu+sX5I1NWMDsldLtbhj9f//DcoMJnvEgcAAA=='
         :                           }
         :                         }
         :                       }
         :                     }
         :                   }
         :                 }
         :               }
         :             }
```


RFC 3702 detailed the breakdown of `id-pe-logotype` OID records.


# References

* [BIMI - IETF RFC Rough Draft](https://tools.ietf.org/id/draft-blank-ietf-bimi-00.html)
* [Convert PNG/JPG/JPEG/WEBP to TinySVG](https://image2svg.com/)
* [SVG Tiny v1.2](https://www.w3.org/TR/SVGTiny12/)
* [Entrust Verified Mark Certificate](https://go.entrust.com/vmc-order-form)
* [DigiCert Verified Mark Certificate](https://order.digicert.com/step1/vmc_basic)
* [BrandIndicatorForMessageIdentification OID](http://oid-info.com/get/1.3.6.1.5.5.7.3.31)
* [id-pe-logotype OID](https://datatracker.ietf.org/doc/html/rfc3709#section-4.1)
* [Issuance of VMC v1.1](https://bimigroup.org/resources/2021-09-01-VMC_Guidelines_latest.pdf)
* [VMC Guidelines v.1.1](https://bimigroup.org/resources/2021-10-08-VMC_Guidelines_latest.pdf)
* [BIMI TinySVG Schema](https://bimigroup.org/resources/SVG_PS-latest.rnc.txt)
* [IETF Draft BIMI - Chuang](https://datatracker.ietf.org/doc/html/draft-chuang-bimi-certificate-00)
