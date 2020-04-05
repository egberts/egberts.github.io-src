Title: Uses
Date: 2018-07-05
blastedbugger: Special Date


Dated fairly regularly. As of March 8, 2020, this is what I'm doing:

# Current Focused Activities

## Cybersecurity

- Latest focus is JavaScript vs. CPU hardware interaction.
  - Custom high-performance timers
  - Modulo address jumping
  - `clflush` instruction
  - See my [JavaScript MindSet chart](https://egbert.net/blog/articles/javascript-malware-mindset.html).

- I am also currently evaluating [WireGuard](https://wireguard.com)  as a mean to allow my personal devices go through public WiFi.  Still in security evaluation stage here.

- Secondary focus is DNSSEC and writing a Python libary module to perform
  intensive security check against DNSSEC for any weakness or failure points.
  - DANE/SMTPS is the current focus.

- I've completed my [Bind9 parser](https://github.com/egberts/bind9_parser) as my large exercise in using [PEG (parser expression grammer)](https://en.wikipedia.org/wiki/Parsing_expression_grammar).  This guide on [Parsing: Algorithms and Terminology](https://tomassetti.me/guide-parsing-algorithms-terminology/) is a great start for anyone.

- I've finished a tiny bash shell front-end to [OpenSSL](https://github.com/openssl/openssl) to provide appropriate TLS/SSL certificates in many setup modes.  It's called [Multi-level Certificate Authority Management tool, front-end tool to
OpenSSL, written in bash shell.](https://github.com/egberts/tls-ca-manage) and
helps us to reduce OpenSSL option conflict errors between options by providing actual workable pairups of CLI options toward OpenSSL.  Useful if running your own Internet DNS infrastructure.

- Also expanding stock Vim highlight for ISC Bind named configuration file from
  version 9.4 to 9.15+.  My current work-in-progress is called
[vim-syntax-bind-named](https://github.com/egberts/vim-syntax-bind-named).

## Web

- I run my main web server on a [InterServer](https://www.interserver.net/) VPS.
- I normally access my remote files through SSH in a terminal.
- My website uses [Pelican](http://blog.getpelican.com/). No JavaScript is ever used on my website.  This is my primary security stance.
- I use [Let's Encrypt](https://letsencrypt.org/) for SSL.
- I post the latest HTTP CSP [here](https://egbert.net/blog/articles/current-http-content-security-policy-csp.html).

## Miscellaneous

- I use [Debian](http://debian.org/) to install OS for all my gateway, desktop, and laptop needs.
- I use [Homebrew](http://brew.sh/) to install Unix-y programs on Macbooks.
- I'm partial to both [Hack](https://sourcefoundry.org/hack/) and [Consolas](https://en.wikipedia.org/wiki/Consolas) for my monospaced fonts.


# Desktop apps

## Graphic design

- I poked with SASS-CSS and Pug-HTML on [openpen.io](https://openpen.io/) a bit as part of my unidentified vulnerability assessment effort.  You can see my SASS-CSS/Pug-HTML work on [this website's page](https://egbert.net/blog/index.html).


## Productivity

- My secret for avoiding the siren call of the internet is my personal home gateway.  I have two blocklists: (1) *antisocial*, which blocks Facebook and Twitter, and (2) *nuclear*, which blocks everything. I have the antisocial blocklist enabled on my laptop and phone from 8:00 AM–6:00 PM and 8:30 PM–11:30 PM. Since I accidentally discovered that it's relatively easy to circumvent the blocking on the Mac, I also use [Focus](https://heyfocus.com/) with the same schedule.
- I also have another Internet in which I exclusively work within without
  distraction.
- I was an early convert to [Todo.txt](http://todotxt.com/) and used it for years until my tasks and projects got too unwieldy. I switched to [Taskpaper](https://www.taskpaper.com/) for a while before recently settling on [2Do](http://www.2doapp.com/) (due to [incredibly](https://www.macstories.net/stories/why-2do-is-my-new-favorite-ios-task-manager/) [positive](https://brooksreview.net/2016/01/2do/) reviews), and I'm in love.
- [Fantastical 2](https://flexibits.com/fantastical)'s natural language input is a glorious thing.
- I keep a log of what I work on (and occasionally do more traditional diary-like entries) with [Day One 2](http://dayoneapp.com/) on both iOS and macOS.
- I use [TextExpander](https://smilesoftware.com/textexpander) to replace and expand a ton of snippets, and I use [Keyboard Maestro](https://www.keyboardmaestro.com/main/) to run dozens of little scripts that help control my computer with the keyboard.
- I use [Übersicht](http://tracesof.net/uebersicht/) to show weather, iTunes track information, and my todo lists on my desktop.
- I no longer use [Dropbox](https://www.dropbox.com).  [NextCloud](https://nextcloud.net) is a end-to-end encryption file server and provides all my Internet file serving needs without any privacy loss.

# Development

## Cybersecurity

- I run a transparent proxy server between my ISP and my gateway router.  That
  is the jewel of my cybersecurity research minuate.  It runs [Zeek](https://www.zeek.org) (used to be called Bro-IDS), [Suricata](https://suricata-ids.org), and [Snort](https://snort.org) on an undisclosed but hand-built platform.
- Also this transparent proxy server runs [Squid Proxy](http://www.squid-cache.org) along with many custom-made ICAP modules.
- I use [ISC Bind9](https://isc.org/bind) to support this website's DNSSEC and to maintain a hidden master with dual secondary nameservers as well as a hidden bastion nameserver.

## Development research

- Things that I publically post are on [GitHub](https://github.com/egberts).
- I use [R](https://www.r-project.org/) and [RStudio](https://www.rstudio.com/) for most of my statistical computing, and I'm a dedicated devotee of the [tidyverse](http://tidyverse.org/) (especially [ggplot2](http://ggplot2.org/) and [dplyr](https://cran.rstudio.com/web/packages/dplyr/vignettes/introduction.html)). I sometimes use [knitr](http://yihui.name/knitr/) and [RMarkdown](http://rmarkdown.rstudio.com/), but I generally just export figures and tables from R and reference them in my writing rather than making full-blown literate documents.
- I also use [Python](https://www.python.org/) ([3!](http://www.onthelambda.com/2014/05/13/damn-the-torpedoes-full-speed-ahead-making-the-switch-to-python-3/)) pretty regularly, especially for natural language processing (with [nltk](http://www.nltk.org/)) and web scraping (with [Requests](http://docs.python-requests.org/en/master/) + [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)). Every few months I play with pandas and numpy and Jupyter, but I'm far more comfortable with R for scientific computing.
- I use RStudio for editing R files, but I use [Sublime Text 3](https://sublimetext.com/3) for everything else.

# Hardware

- I use Dell Optiplex and Precison for all my gateway, servers and security
  needs.
- I use 2016 13″ MacBook Pro, iPad Mini 2, and iPhone 6s.  Some smattering of
  iPods and odd Internet thingies.
- I use Raspberry Pi for my Kerberos/LDAP ticketing and multiple window-session-login SAML needs across all GUI devices above (except for iPhone).

# Writing

- I permanently ditched Microsoft Word as a writing environment in 2004.  I do all my writing in [joplin](http://joplinapp.org/) [Markdown](https://daringfireball.net/projects/markdown/) (including e-mails and paper-and-pencil writing)—it's incredibly intuitive, imminently readable, flexible, future proof, end-to-end encrypted, and lets me ignore formatting and focus on content.  I like it that I can use on Linux and Apple interchangably via [NetCloud](https://nextcloud.com).
- I live in [Ulysses](http://ulyssesapp.com/). At first I chafed at the fact that it stores everything in its own internal folder structure, since I store most of my writing in git repositories, but exporting a compiled Markdown file from a bunch of Ulysses sheets is trivial (and still easily trackable in version control).
- Ulysses has decent HTML previewing powers, but when I need more editorial tools, I use [Marked](http://marked2app.com/).
- I use [iA Writer](https://ia.net/writer/) to edit standalone Markdown files, since Ulysses uses its own syntax when using fancy things like footnotes.
- The key to my writing workflow is the magical [joplin](http://joplinapp.org/), which converts Markdown files into basically anything else.
- I store all my bibliographic references, books, and articles in a [BibTeX](http://www.bibtex.org/) file that I edit with [BibDesk](http://bibdesk.sourceforge.net/).
- I read and annotate all my PDFs with [Skim](http://skim-app.sourceforge.net/) (and [iAnnotate](http://www.iannotate.com/) on iOS), since both export annotations as clean plain text.

## Patent Efforts

- I've written, filed, and have been awarded several patents.  Those awarded
  patents are available upon request.  Unfiled patents will be kept as unfiled.
