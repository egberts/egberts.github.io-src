title: Comparison of Railroad Diagrams
date: 2024-07-01 08:43
status: draft
tags: railroad diagram, EBNF, ABNF, BNF, SRFB
category: research
summary: A comparison of different railroad diagram tools
lang: en
private: False


A quick overview of all file format needed to construct railroad diagram and its comparison.

The starter list of railroad format is:

* ABNF
* EBNF
* SRBF
* Tabatkins' construct using either Python or JavaScript (1,600 Stars; 151 Forks, MIT)

ABNF last updated in 2008, [first roughed](https://datatracker.ietf.org/doc/rfc2234/) in May 1996 by Dave Crocker (dhc@dcrocker.net) of Internet Mail Consortium and Paulo Overell (paulo@turnpike.com) of Demon Internet Ltd.

EBNF 
====

Online tools are:

* https://rr.red-dove.com/ui


Tab Atkin's Construct 
=====================

Online tools are:

* https://railroad.omegatower.net/generator.html
* https://tabatkins.github.io/railroad-diagrams/generator.html

PyRailroad
====
Makes excellent use of Tab Atkin's Railroad-Diagram (Railroad package).A

* https://epithumia.github.io/pyrailroad/#


See https://egbert.net/blog/articles/pelican-metadata.html for details

[jtable caption="This is caption" separator="|" th=0 ai="1"]
# caption - the table caption
# separator - default is comma
# th - table header (=0 means disable)
# ai - auto-index, adds a column numbering starts at 1

# : if the date is not specified and DEFAULT_DATE is set to 'fs', Pelican will rely on the file’s “mtime” timestamp, and the category can be determined by the directory in which the file resides.


References
==========
* [ABNF - IETF RFC 5234 - Augumented BNF for Syntax Specification](https://datatracker.ietf.org/doc/html/rfc5234)
* [EBNF - International standard (ISO 14977)](https://en.wikipedia.org/wiki/International_standard)
* [SRFB](https://github.com/gbrault/railroad-diagrams/blob/gh-pages/live/doc/readme.md/)
* [IETF RFC 5234 history](https://datatracker.ietf.org/doc/rfc2234/)
* [Translate EBNF to SRFB](https://github.com/gbrault/railroad-diagrams)
