title: Current HTTP Headers
date: 2020-03-23 11:49
status: published
tags: CSP, http, security, web
category: research
summary: Current HTTP Header settings

Security is a moving target; this means HTTP Headers are also moving targets.

Downside to using Open-Source NGINX is that I cannot disable the emission of
`Server:` HTTP header line.

Below is the current HTTP Headers used on my web servers:
```http
server: nginx
cache-control: max-age=604800
strict-transport-security: max-age=31536000; includeSubDomains; preload
public-key-pins-report-only: pin-sha256="r7AIbBAnB0ps+w5KY7hhXmHRLX2iDUOPLXq3CpAm5HI="; pin-sha256="tiNlIfCOopsiDaisyC3uiaNBgRKStFM7KkovUBg4Huw="; max-age=5184000; includeSubdomains; report-uri="https://ssoseo1.report-uri.com/r/d/hpkp/reportOnly"
expect-ct: enforce;max-age=30;report-uri="https://ssoseo1.report-uri.com/r/d/ct/enforce; enforce"
x-frame-options: deny
x-xss-protection: 1; mode=block
x-content-type-options: nosniff
referrer-policy: no-referrer
report-to: { "url": "https://ssoseo1.report-uri.com/r/d/csp/enforce", "group": "endpoint-1", "max-age": 10886400 }, { "url": "https://ssoseo1.report-uri.com/r/d/csp/reportOnly", "group": "endpoint-1", "max-age": 10886400 }
content-security-policy: default-src 'none'; base-uri 'none'; script-src 'strict-dynamic'; object-src 'none'; style-src 'self'; img-src https://egbert.net/favicon.ico https://egbert.net/images/ https://egbert.net/blog/articles/*/images/*.png data:; media-src https://egbert.net/media/ data:; frame-src https://egbert.net/frames/; frame-ancestors 'self'; worker-src 'self'; child-src https://egbert.net/frames/; font-src https://egbert.net/fonts/; connect-src 'self' https://egbert.net/; form-action 'none'; require-trusted-types-for; trusted-types template; sandbox; report-uri https://ssoseo1.report-uri.com/r/d/csp/enforce; report-to endpoint-1; upgrade-insecure-requests; block-all-mixed-content;
report-to: { "group": "csp-endpoint", "max-age": 10886400, "endpoints": [ { "url": "https://ssoseol.report-uri.com/r/d/csp/enforce" } ] }, { "group": "hpkp-endpoint", "max-age": 10886400, "endpoints": [ { "url": "https://ssoseol.report-uri.com/r/d/csp/enforce" } ] }
x-robots-tag: none
cache-control: max-age=86400; no-transform; public;
expires: 0
feature-policy: accelerometer 'none'; camera 'none'; fullscreen 'self'; geolocation 'none'; gyroscope 'none'; magnetometer 'none'; microphone 'none'; midi 'none'; notifications 'none'; payment 'none'; push 'none'; sync-xhr 'none'; speaker 'none'; usb 'none'; vibrate 'none';
accept-ranges: bytes
X-Firefox-Spdy: h2
```

Other online HTTP checkers are:

* [HSTS Preload checker](https://hstspreload.org/?domain?egbert.net)
* [Security Headers](https://securityheaders.com/?followRedirects=off&hide=on&q=egbert.net)
* [Crypt Check](https://tls.imirhil.fr/https/egbert.net)
* [ImmuniWeb](https://www.immuniweb.com/ssl/)
* [CSP Evaluator](https://csp-evaluator.withgoogle.com/?csp=https://egbert.net)

References
==========

* [Content-Security-Policy (Mozilla)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy)
* [Multiple CSP (Mozilla)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy?utm_source=mozilla&utm_medium=devtools-netmonitor&utm_campaign=default#Multiple_content_security_policies)
* [Web Security (Mozilla](https://infosec.mozilla.org/guidelines/web_security#Examples_5)
* [W3 CSP Specification](https://www.w3.org/TR/CSP2/#directive-frame-src)
