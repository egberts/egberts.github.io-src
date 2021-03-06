title: Current HTTP Content Security Policy (CSP)
date: 2008-06-3 08:16
modified: 2020-03-23 11:37
status: published
tags: CSP, http, security, web
category: research
summary: Current Content Security Policy


Please note the directory separation are being enforced:
```
+ website
    + images
    + css
    + js
    + media
    + frames
    + fonts
```

The currently best secured policy for HTTP CSP is currently:
```nginx
default-src 'none';
base-uri 'none';
script-src 'strict-dynamic';
object-src 'none';
style-src 'self';
img-src https://egbert.net/favicon.ico https://egbert.net/images/ https://egbert.net/blog/articles/*/images/*.png data:;
media-src https://egbert.net/media/ data:;
frame-src https://egbert.net/frames/;
frame-ancestors 'self';
worker-src 'self';
child-src https://egbert.net/frames/;
font-src https://egbert.net/fonts/;
connect-src 'self' https://egbert.net/;
form-action 'none';
require-trusted-types-for;
trusted-types template;
sandbox;
report-uri https://ssoseo1.report-uri.com/r/d/csp/enforce;
report-to endpoint-1;
upgrade-insecure-requests;
block-all-mixed-content;
```

You can check them out at [Google CSP online checker](https://csp-evaluator.withgoogle.com/?csp=https://egbert.net)

References
==========

* [Content-Security-Policy (Mozilla)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy)
* [Multiple CSP (Mozilla)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy?utm_source=mozilla&utm_medium=devtools-netmonitor&utm_campaign=default#Multiple_content_security_policies)
* [Web Security (Mozilla](https://infosec.mozilla.org/guidelines/web_security#Examples_5)
* [W3 CSP Specification](https://www.w3.org/TR/CSP2/#directive-frame-src)
