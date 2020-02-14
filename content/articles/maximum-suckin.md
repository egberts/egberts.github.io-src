Title: Maximum Suck-In
Date: 2019-12-17T10:35
Tags: development, engineering, stack, full-stack, web, server
Category: development
I was designing a new web server that has the following capabilities:

* web page are one-time, never served again
 * Age timer starts at first authenticated visit
 * Then gets deleted and returns HTTP 404

It wasn't meant to be a one-time delivery mechanism, but only for
a mutually-assured data exchange (much like Signal auto-delete).

Intended audience would be for sales prospectors who wish to send files, content, video, audio to their customers.

Might have password-only prompt to prevent email sniffers from successfully visiting the password-protected link.

Some obstecles are:

* What is the URI format?
* Is it .NET/CGI argument or is it flat URI?
* How to map a directory file layout to these disposable web pages.
* How to serve HTML in a secured manner (HTTPS?)


Initial Design
==============

HTML to File Mapping
--------------------


Secured Web Content Delivery
----------------------------


Slippery Slope
==============

The suck-in list was so much longer and included:

* Datadog for infrastructure monitoring.
* DigitalOcean for virtual machine hosting.
* Django REST Framework for APIs.
* Drip for marketing email campaigns.
* Jekyll for the marketing site.
* JSON API as a communication protocol.
* Let's Encrypt for TLS certificates.
* Mailgun for transactional emails.
* Mixpanel for behavior analysis.
* Rollbar for error tracking.
* Segment for data aggregation.
* Stripe for recurring payments.
* wal-e for database backups.
* webpack for JavaScript asset bundling.


