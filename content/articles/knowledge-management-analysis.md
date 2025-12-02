title: Comparison of Client-Side Knowledge-Base Management (KBM)
date: 2024-06-14 05:00
modified: 2025-12-02 05:00
status: published
tags: KBM, comparison
category: research
summary: Comparing Knowledge-Base Management for Desktop Usage
lang: en
private: False


This article details my effort to select the most suitable 
knowledge-based management tool that covers several 
functionalities:

* Note-taking, in Markdown
  * Note organization
    * File-based (Database-free)
      * Hierarchical structure
    * Zettlekasten note method
  * File-Tagging
    * Subtag
  * interactive tables
* Tasklists
  * Goal setting
* Output enhancement
  * Syntax highlight
* Usability
  * work offline
  * cross-OS support
  * sync between devices
  * Search textbox
  * Version history
    * Git support (optional)
* Privacy
  * No tracking
  * No hardcoded AI support
* Export
  * Markdown (should be central format)
  * static-site generation (Pelican/Jeckyl/Hugo)
  * PDF
  * HTML
* Import
  * Customizable
    * Pelican (optional)

Criteria
========
I am most curious to know where the market stands with regard to the 
integration of the functional aspects of KBM

* Note-taking
* Journal (Daily) 
* Tasking
* Backlinking
* Analysis (graphing)

In effort to select the most suitable knowledge-based management tool
for my desktop, a couple of criteria were set forth:

* Rebuildable
* Offline support
* Robustness

Rebuildable KBM
---------------
First criteria of the KBM is the ability to rebuild at a much later date
in case the maintainer/company goes out of business.

I've been burnt all too often by this criteria when adopting software.

Time wasted is time not gain.

K.I.S.S. (Keep it simple, stupid.)

Offline Support
---------------
Again, the ability to host the backend yourself is the ultimate pillar of
privacy, end-user privacy.  

Robustness
---------------
Robustness of the KBM also entails the extensibility and usability of 
such software, not only in user-interface (UI) but at command line (CLI) 
as well.

Database is a non-starter. Imagine how many times I've had to move
the database as I went from one Wiki to another Wiki, before settling
on file-based [DocuWiki](https://www.dokuwiki.org/dokuwiki) and Haskell-based [gitit](https://hackage.haskell.org/package/gitit); they got lost, a few times.

Preliminary Candidates
======================

* [Joplin](https://joplinapp.org)
* [Notion](https://www.notion.so/)
* [Obsidian](https://obsidian.md)
* [Zettlr](https://www.zettlr.com/)
* [Logseq](https://logseq.com/)
* [AppFlowy]()

Joplin
------
Joplin was the 2nd note-taking app (after Bear).

After a year, the user-interface was deemed non-flowing and unusable for
the purpose of knowledge-based management.

Apple iNote resume their role as a basic note-taking app on my mobiles,
because you cannot beat simplicity and ease-of-use.

Used Joplin mostly as a file-conversion tool on mobile devices, not much else.

Notion
------
A freemium KBM.  A business that is constantly buying out 
other companies to bolster their main flagship: Notion:  Most 
notably the [buyout of Skiff](https://techcrunch.com/2024/02/09/notion-acquires-privacy-focused-productivity-platform-skiff/), 
a good move but their focus on the core product remains 
shallow thus setting the direction of a shaky future.

UI?  Second best, next to Obsidian.

Search analysis, poorest of all KBM.

Also for some reason, Notion cannot be used in an off-line manner.  
That plane trip and your Notion app becomes a no-op. So much for being
tied into your Internet infrastructure (which is exactly what I am
trying to avoid).  I suspect this to be a new phenomena due to
its recent integration of AI Chat bot into its freemium product.

Notion is no file-centric product, as it uses a database: Gagh!


Obsidian
--------
This looks like the finest product as well of 
any KBM that I have encountered.

Shiniest aspect of Obsidian is that entire product is based on
hierarchical file-centric Markdown for its core.

Obsidian has the best documentation, bar none.  

Obsidian Syncing is awesome!  Use your own `ownCloud` 
(or `NextCloud` or WebDAV or Obsidian's own $4/month sync repository).

All data-at-rest are secured behind AES-256 end-to-end encryption where
the key stays only on your client OS: on some mobile device, it leverages
iOS hardware-based KeyStore vault.

Still rough around the far edge but its extensibility is noted 
through its deep community-supported NodeJS-based TypeScript plug-ins 
libraries; a quick perusal shows that it covered nearly everything I needed.

Note: I wasn't about to enhance my TypeScript language skillset 
anytime soon if I needed anything not covered by their rich library (maybe
 leveraging an approach of co-opt closest plugin, refit to desire, 
and release).

Obsidian was remove from consideration once once I could not review the
source code due to its closed-source of its client software; a nit-pick here.

Crying shame. But it is their viable business model and definitely
beats out the Notion app by a mile.

I may revert to this option on a paying-basis, once their pricing model
improves (currently $50/year per user for commercial use).

Zettlr
------
Zettlr is the best citation tracker of any KBM or note-taking 
apps; Citations are handled by Zotero, JabRef, and many others.

It is an Electron app; if that doesn't bother you, skip to next paragraph.
First thing I noticed when cloning Zetllr repository is that all the codes
are written in TypeScript using Electron SDK and stored in Electron ASAR
archive (`file resources/*`, kinda of like JAVA `.jar` format).  Requires
the use of Electron virtual machine (kinda like the Python script interpreter).

Yet, I soldier on into the Electron arena for the purpose of this article.

Undo is buggy as hell (first reported in 2020, four-years, unfixed).

Vim editing mode also has its shaky moment.

No spell-check; isn't this a note-taking app?

Noticed that Zettlr has second best polished appearance of UI of 
any KBM reviewed but it remains a note-taking app with a glorious
self-grandiose appearance of claiming to be a KBM.  
But that is about the only thing that shine in this app; online reviews 
have all been counter-SEO'd and inflated by a lone user.

Note: Electron is yet another disdainful bloatware with goals to 
make same graphic user interface (GUI) work across various 
platforms, in this case, specifically on macOS, iOS/iPadOS, Windows, and Linux.
Unfortunately, Signal app makes good use of Electron (which in itself
is the single one most major security vulnerability that is awaiting to be
revealed).

Quickly ruled out for SW bloatness and lack of support for Apple iOS, 
even though Electron supports iOS.  I suspect this to be yet another case
of developer not wanting to go thru the notion of securing his DUNS ID
and thus his Apple Developer ID.

Also ruled out due to spammy but artificial support for its software.
Yep, author of Zettlr is trying too hard to elevate his stuff to something other than what it is supposed to be ... note-taking. (Also looking at you, [Alternatives.to](https://alternatives.to), for poor anti-spam support).

FWIW, [Ulysses](https://ulysses.app/) makes for a better choice than Zettlr, but
Zettlr is no KBM.

Logseq
------
Logseq is a promising KBM-in-the-making, but remains firmly within 
the functional group of note-taking/tasking/to-do.

Logseq is unique apart from all other apps such that 
everything is web-based, including data entry and management there of:
a [Logseq demo](https://demo.logseq.com/#/) can be explored.

The shiny star is its search engine and graphing relationship between pages.

Its GUI has high resemblance to the layout of Obsidian, so familiarity is good.

Unfortunately, Logseq attempts to leverage Chromium-centric of native filesystem
(which is a bad thing, end-user-security-wise); only Edge, Vivaldi and Chrome-based browser supports native file system (still a bad thing).

Useful for some students, but not for academics nor faculty due to its 
poor citation support.

Conclusion
==========

We are not there yet.

For free, Obsidian remains the best, but not the cream-of-the-crop yet.  You
run the risk of being shutout by company closure (but your own markdown file remains yours, those relationships may be gone).



References
==========
* [Joplin](https://joplinapp.org)
* [Logseq](https://logseq.com/)
* [Notion](https://www.notion.so/)
* [Obsidian](https://obsidian.md)
* [Obsidian API](https://github.com/obsidianmd/obsidian-api)
* [Ulysses](https://ulysses.app/)
* [Zettlr](https://www.zettlr.com/)

Alternative Analysis
--------------------
* [Zettlr](https://alternativeto.net/software/zettlr/)
