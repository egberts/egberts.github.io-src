Title: Authentication for API
Date: 2018-12-28 06:30
Updated: 2020-02-25 01:34
Status: published
Tags: API, CORS, JWT, Authentication, Auth0, Fusion, Gluu
Category: research
Summary: Authentication methods for API usages.

Authentication for API
======================

When deploying a new web API, authentication approaches came to mind foremostly.  Needed to determine which type of authentication to use.  Large binning, salting of hash, and revocatable are my criteria.

Some toolkits that went out the window firstly are: 

* auth0, 
* Fusion auth, and 
* Gluu.

So, some of the basic criteria are:

* User and password login instead of plain HTTP session cookies.
* HTTP-only over TLS v1.2+ (secured HTTP, HTTPS)
    * ECDSA 1K or better
* SameSite [1]
* __Host prefix [1]
* preload HTTP Strict-Transport-Security header line [2]
* Bearer token supplied by API clients
* Don't listen on port 80... like ever.  Or revoke token if over non-port 443.
* DO NOT use JWT [3]
* DO NOT use CORS [4]


External References
-------------------

* [1]: [Set Cookie - Mozilla Developer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)
* [2]: [Strict Transport Security - Mozilla Developer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)
* [3]: [JSON Web Token - Wikipedia](https://en.wikipedia.org/wiki/JSON_Web_Token)
* [4]: [CORS - Mozilla Developer](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
