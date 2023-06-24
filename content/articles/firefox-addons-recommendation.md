title: Recommended Add-Ons for Firefox 101
date: 2022-08-02 13:13
status: published
tags: Firefox
category: research
summary: What add-ons to consider for Firefox release 101?
slug: firefox-addons-recommendation
lang: en
private: False

My core addons, things that I consider more or less essential for my experience of Firefox, are:

* [Foxy Gestures](https://addons.mozilla.org/en-US/firefox/addon/foxy-gestures/) ([Github](https://github.com/marklieberman/foxygestures)) is probably still the best gestures extension for me for modern versions of Firefox (but I can't say for sure, because I no longer investigate alternatives).  (I use some custom gestures in my Foxy Gestures configuration that go with some custom hacks to my Firefox to add support for things like 'view page in no style' as part of the WebExtensions API.)

* [uBlock Origin](https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/) ([Github](https://github.com/gorhill/uBlock)) is my standard 'block ads and other bad stuff' extension, and also what I use for selectively removing annoying elements of pages ([like floating headers and footers](https://utcc.utoronto.ca/~cks/space/blog/web/UBlockOriginZapperPraise)).

* [uMatrix](https://addons.mozilla.org/en-US/firefox/addon/umatrix/) ([Github](https://github.com/gorhill/uMatrix)) is my primary tool for blocking Javascript and cookies. [uBlock Origin could handle the Javascript](https://utcc.utoronto.ca/~cks/space/blog/web/UBlockJavascriptBlocking), but not really the cookies as far as I know, and in any case uMatrix gives me finer control over Javascript which I think is a better fit with [how the web does Javascript today](https://utcc.utoronto.ca/~cks/space/blog/web/UMatrixImprovesWeb).

* [Cookie AutoDelete](https://addons.mozilla.org/en-US/firefox/addon/cookie-autodelete/) ([Github](https://github.com/Cookie-AutoDelete/Cookie-AutoDelete)) deals with the small issue that uMatrix doesn't actually block cookies, it just doesn't hand them back to websites. This is probably what you want in uMatrix's model of the world ([see Chris's blog entry on this for more details](https://utcc.utoronto.ca/~cks/space/blog/web/FirefoxQuantumCookieModels)), but I don't want a clutter of cookies lingering around, so I use Cookie AutoDelete to get rid of them under controlled circumstances.  (However unaesthetic it is, I think that the combination of uMatrix and Cookie AutoDelete is necessary to deal with cookies on the modern web. You need something to patrol around and delete any cookies that people have somehow managed to sneak in.)

* [Stylus](https://addons.mozilla.org/en-US/firefox/addon/styl-us/) ([Github](https://github.com/openstyles/stylus)) has become necessary for me after Google changed [their non-Javascript search results page](https://utcc.utoronto.ca/~cks/space/blog/web/GoogleSearchSettings) to basically be their Javascript search results without Javascript, instead of the much nicer and more useful old version. I use Stylus to stop search results escaping off the right side of my browser window.

Additional fairly important addons that would change my experience if they weren't there:

* [Cookie Quick Manager](https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/) ([Github](https://github.com/ysard/cookie-quick-manager)) allows me to inspect, manipulate, save, and reload cookies and sets of cookies. This is kind of handy every so often, especially saving and reloading cookies.

The remaining addons I use I consider useful or nice, but not all that important on the large scale of things. I could lose them without entirely noticing the difference in my Firefox:


* [Certainly Something](https://addons.mozilla.org/en-US/firefox/addon/certainly-something/) ([Github](https://github.com/april/certainly-something)) is my TLS certificate viewer of choice. I occasionally want to know the information it shows me, especially for our own sites. The current Firefox certificate information display is almost as good as Certainly Something, but it's much less convenient to get to.

* [HTTP/2 Indicator](https://addons.mozilla.org/en-US/firefox/addon/http2-indicator/) ([Github](https://github.com/bsiegel/http2-indicator)) does what it says; it provides a little indicator as to whether HTTP/2 was active for the top-level page.

* [ClearURLs](https://addons.mozilla.org/en-CA/firefox/addon/clearurls/) ([GitLab](https://gitlab.com/KevinRoebert/ClearUrls)) is my current replacement for [Link Cleaner](https://addons.mozilla.org/en-US/firefox/addon/link-cleaner/) after the latter stopped being updated. It cleans various tracking elements from URLs, like those `utm_*` query parameters that you see in various places. 

Enjoy.
