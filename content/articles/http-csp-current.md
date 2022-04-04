title: Current HTTP Content Security Policy (CSP)
date: 2008-06-3 08:16
modified: 2022-03-31 11:34
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
block-all-mixed-content; 
child-src https://egbert.net/frames/; 
connect-src 'self' https://egbert.net/; 
frame-ancestors 'self'; 
frame-src https://egbert.net/frames/; 
font-src https://egbert.net/fonts/; 
form-action 'none'; 
img-src 'self' https://egbert.net/favicon.ico https://egbert.net/images/ https://egbert.net/blog/ data:; 
manifest-src 'self'; 
media-src https://egbert.net/media/ data:; 
object-src 'none'; 
prefetch-src 'self'; 
require-trusted-types-for 'script'; 
sandbox allow-same-origin; 
script-src 'strict-dynamic'; 
script-src-elem 'strict-dynamic'; 
script-src-attr 'strict-dynamic'; 
style-src 'self' https://egbert.net/ https://egbert.net/images/ https://egbert.net/css/ https://egbert.net/fonts/ ; 
style-src-elem 'self' https://egbert.net/fonts/; 
style-src-attr 'self' https://egbert.net/fonts/; 
upgrade-insecure-requests; 
worker-src 'self';
```

Side note: Permission Policy:
```css
permissions-policy:
   accelerometer=(), 
   ambient-light-sensor=(), 
   autoplay=(), 
   battery=(), 
   camera=(), 
   clipboard-read=(), 
   clipboard-write=(), 
   conversion-measurement=(), 
   cross-origin-isolated=(), 
   display-capture=(), 
   document-domain=(), 
   encrypted-media=(), 
   execution-while-not-rendered=(), 
   execution-while-out-of-viewport=(), 
   focus-without-user-activation=(), 
   fullscreen=(), 
   gamepad=(), 
   geolocation=(), 
   gyroscope=(), 
   hid=(), 
   idle-detection=(), 
   interest-cohort=(), 
   keyboard-map=(), 
   magnetometer=(), 
   microphone=(), 
   midi=(), 
   navigation-override=(), 
   payment=(), 
   picture-in-picture=(), 
   publickey-credentials-get=(), 
   screen-wake-lock=(), 
   serial=(), 
   speaker-selection=(), 
   sync-script=(), 
   sync-xhr=(), 
   trust-token-redemption=(), 
   usb=(), 
   vertical-scroll=()
   web-share=(), 
   window-placement=(), 
   xr-spatial-tracking=(), 
```

You can check them out at [Google CSP online checker](https://csp-evaluator.withgoogle.com/?csp=https://egbert.net)

References
==========
* [https://blog.rapidsec.com/10-tips-to-build-a-content-security-policy-csp-without-breaking-your-site/](https://blog.rapidsec.com/10-tips-to-build-a-content-security-policy-csp-without-breaking-your-site/)
* [https://content-security-policy.com/strict-dynamic/](https://content-security-policy.com/strict-dynamic/)
* [Content-Security-Policy (Mozilla)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy)
* [Multiple CSP (Mozilla)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy?utm_source=mozilla&utm_medium=devtools-netmonitor&utm_campaign=default#Multiple_content_security_policies)
* [Web Security (Mozilla](https://infosec.mozilla.org/guidelines/web_security#Examples_5)
* [W3 CSP Specification](https://www.w3.org/TR/CSP2/#directive-frame-src)
