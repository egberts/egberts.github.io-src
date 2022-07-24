Title: Uses
Date: 2018-07-05
Modified: 2022-03-19 11:39
Status: published
blastedbugger: Special Date


Dated fairly regularly. As of March 19, 2022, this is what I'm doing:

# Current Focused Activities

## Cybersecurity

- Latest focus is designing the framework in detecting malwares written within WASM/JavaScript environment.

- JavaScript vs. CPU hardware interaction.
  - Custom high-performance timers
  - Modulo address jumping
  - `clflush` instruction
  - See my [JavaScript MindSet chart](https://egbert.net/blog/articles/javascript-malware-mindset.html).

- Finished the private cloud; has the following:

 - Private Root PKI CA
 - Private DNS Root Servers w/ DNSSEC support
 - VPN 

- Secondary focus is DNSSEC and writing a Python libary module to perform
  intensive security check against DNSSEC for any weakness or failure points.
 - mastered DANE/SMTPS.

- I've completed my [Bind9 parser](https://github.com/egberts/bind9_parser) as my large exercise in using [PEG (parser expression grammer)](https://en.wikipedia.org/wiki/Parsing_expression_grammar).  This guide on [Parsing: Algorithms and Terminology](https://tomassetti.me/guide-parsing-algorithms-terminology/) is a great start for anyone.

- I've finished a tiny bash shell front-end to [OpenSSL](https://github.com/openssl/openssl) to provide appropriate TLS/SSL certificates in many setup modes.  It's called [Multi-level Certificate Authority Management tool, front-end tool to
OpenSSL, written in bash shell.](https://github.com/egberts/tls-ca-manage) and
helps us to reduce OpenSSL option conflict errors between options by providing actual workable pairups of CLI options toward OpenSSL.  Useful if running your own Internet DNS infrastructure.

- Also expanding stock Vim highlight for ISC Bind named configuration file from
  version 9.4 to 9.20.  My current work-in-progress is called
[vim-syntax-bind-named](https://github.com/egberts/vim-syntax-bind-named).

## Web

- I run my main web server on a [InterServer](https://www.interserver.net/) VPS.
- I normally access my remote files through a custom-made bastion SSH server as well as a SSH jump server.
- My website uses [Pelican](http://blog.getpelican.com/). No JavaScript is ever used on my website.  This is my primary security stance.
- I use [Let's Encrypt](https://letsencrypt.org/) for all my public PKI needs for TLS/SSL.
- I post the latest HTTP CSP [here](https://egbert.net/blog/articles/current-http-content-security-policy-csp.html).

## Miscellaneous

- I use [Debian](http://debian.org/) to install OS for all my gateway, desktop, and laptop needs.
- [QubeOS](https://www.qubes-os.org/) is now the primary desktop.
- [Proxmox](https://www.proxmox.com/en/) is the cloud server in my white lab having many VMs running.
- I use [Homebrew](http://brew.sh/) to install Unix-y programs on Macbooks.
- I'm partial to both [Hack](https://sourcefoundry.org/hack/) and [Consolas](https://en.wikipedia.org/wiki/Consolas) for my monospaced fonts.  Otherwise I use [IBM Plex](https://www.ibm.com/plex/) fonts.
- Gentoo Linux for all my embedded host needs, of which my gateway is using `libmusl` (not libc6) because `LD_PRELOAD` is hardcoded into libc and it is way too easy for non-root user to hijack any process this way.  Also use OpenRC (instead of `systemd` because systemd opens network sockets at PID1 thus it is way too easy for a trojan to be slipped into; OpenRC PID 1 uses no network socket).


# Desktop apps

## Graphic design

- Poked with SASS-CSS and Pug-HTML on [openpen.io](https://openpen.io/) a bit as part of my unidentified vulnerability assessment effort.  You can see my SASS-CSS/Pug-HTML work on [this website's page](https://egbert.net/blog/index.html).

- Mastering of CSS is shown in my [motto](https://egbert.net/blog) page;  And that accomplishment is JavaScript-free too.


## Productivity

- My secret for avoiding the siren call of the internet is my personal home gateway.  I have two blocklists: (1) *antisocial*, which blocks Facebook and Twitter, and (2) *nuclear*, which blocks everything. I have the antisocial blocklist enabled on my laptop and phone from 8:00 AM–6:00 PM and 8:30 PM–11:30 PM. Since I accidentally discovered that it's relatively easy to circumvent the blocking on the Mac, I also use [Focus](https://heyfocus.com/) with the same schedule.
- I also have another Internet in which I exclusively work within without
  distraction.
- I was an early convert to [Todo.txt](http://todotxt.com/) and used it for years until my tasks and projects got too unwieldy. I switched to [Taskpaper](https://www.taskpaper.com/) for a while before recently settling on [2Do](http://www.2doapp.com/) (due to [incredibly](https://www.macstories.net/stories/why-2do-is-my-new-favorite-ios-task-manager/) [positive](https://brooksreview.net/2016/01/2do/) reviews), and I'm in love.
- [Fantastical 2](https://flexibits.com/fantastical)'s natural language input is a glorious thing.
- I keep a log of what I work on (and occasionally do more traditional diary-like entries) with [Day One 2](http://dayoneapp.com/) on both iOS and macOS.
- I use [TextExpander](https://smilesoftware.com/textexpander) to replace and expand a ton of snippets, and I use [Keyboard Maestro](https://www.keyboardmaestro.com/main/) to run dozens of little scripts that help control my computer with the keyboard.
- I use [Übersicht](http://tracesof.net/uebersicht/) to show weather, iTunes track information, and my todo lists on my desktop.
- I no longer use [Dropbox](https://www.dropbox.com) nor [NextCloud](https://nextcloud.net). [OwnCloud](https://owncloud.org) is a end-to-end encryption file server and provides all my Internet file serving needs without any privacy loss.

# Development

## Cybersecurity

- I run a transparent proxy server between my ISP and my gateway router.  That
  is the jewel of my past cybersecurity research minuate.  It runs [Zeek](https://www.zeek.org) (used to be called Bro-IDS), [Suricata](https://suricata-ids.org), and [Snort](https://snort.org) on an undisclosed but hand-built platform.  Packet analysis remains my forte.
- Also this transparent proxy server runs [Squid Proxy](http://www.squid-cache.org) along with many custom-made ICAP modules of mine.
- - has HTTPS/ICAP server (to block DNS-over-HTTP)
- - has TLS/ICAP server (to block DNS-over-TLS)
- I use [ISC Bind9](https://isc.org/bind) to support this website's DNSSEC and to maintain a hidden master with quad secondary nameservers as well as a hidden bastion nameserver.  I run my own private Root Servers with DNSSEC within my WhiteLab.

## Development research

- Things that I publically post are on [GitHub](https://github.com/egberts).
- Found microcode vulnerabilty bug in QEMU TLB cache reload failure during my [Unicorn](https://github.com/unicorn-engine/unicorn/issues/437) that emulates just about any file-less malware.
- Things that I do not publically post stay inside my White Lab.
- I use [R](https://www.r-project.org/) and [RStudio](https://www.rstudio.com/) for most of my statistical computing, and I'm a dedicated devotee of the [tidyverse](http://tidyverse.org/) (especially [ggplot2](http://ggplot2.org/) and [dplyr](https://cran.rstudio.com/web/packages/dplyr/vignettes/introduction.html)). I sometimes use [knitr](http://yihui.name/knitr/) and [RMarkdown](http://rmarkdown.rstudio.com/), but I generally just export figures and tables from R and reference them in my writing rather than making full-blown literate documents.
- I also use [Python](https://www.python.org/) ([3!](http://www.onthelambda.com/2014/05/13/damn-the-torpedoes-full-speed-ahead-making-the-switch-to-python-3/)) pretty regularly, especially for natural language processing (with [nltk](http://www.nltk.org/)) and web scraping (with [Requests](http://docs.python-requests.org/en/master/) + [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)). Every few months I play with pandas and numpy and Jupyter, but I'm far more comfortable with R for scientific computing.
- I use RStudio for editing R files, but I use [Sublime Text 3](https://sublimetext.com/3) for everything else.

# Source Code Revision Controls
- Maven
- Git (Github, Gitlab, sr.ht)
- CVS
- Mercurial (Mozilla Firefox)
- Atlassian Confluence
- Wikipedia 
- Jira
- Bugzilla
- CT/CI

# Languages
- C/C++
- Assembly, x86, MIPS, ARM, MPB860, i960, 
- Python
- R
- JavaScript
- Haskell
- Nim

# Administration

I keep all my autoconfiguration of many network daemons in [here](https://github.com/egberts/easy-admin).

# Security

- CISecurity Level 1 and 2
- many [government standards](https://dodiac.dtic.mil/wp-content/uploads/2022/07/2022-06-24-csiac-dod-cybersecurity-policy-chart.pdf)


# Network Layer

- maintain a default deny-firewall using newer `nftables`.  Also maintain Vim syntax highlighter for 430 keywords used eithin `nft` command line [here](https://github.com/egberts/vim-nftables).
- Wrote a protocol to connect LAN bridges together from 1,000s of miles apart and called it [Bridge Relay Element](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?search=4096); that one worked really well with remote sites like savannah Africa via X.25, Frame Relay, and shortwave radio.
- Wrote, rewrote, rewrote, ported, and re-ported PPP-over-Ethernet for many employers.


# Systems

- Xeon, 24-core, with a mixture of 24TB RAID5 HD storage and 6TB RAID1 SDD storage.
- Dell Optiplex and Precison hardware for all my gateway, servers and security
  needs.
- 2016 13″ MacBook Pro, iPad Mini 2, and iPhone 6s.  Some smattering of
  iPods and odd Internet thingies.
- Raspberry Pi for my Kerberos/LDAP ticketing and multiple-session/single-login SAML needs across all GUI devices above (except for iPhone).
- PinePhone (the original) is also a hobby of mine, with focus on profiling the cellular firmware API.
- often make my own toolchains from scratch (full toolchains for cross-platforms).


# Hardwares

- wrote a bootloader for a radition-hardened CPU.  Improved TCP protocol (called TCP-Westwood) with Sally Floyd of ISC for bit rot compensation.
- Xilinx ARM, Real-Time Linux, ruggedized portable test unit; full integration of U-Boot, BusyBox, USB file downloader; Yocto build.
- performed full FPGA troubleshooting and resolution for RocketIO issues within noisy EMP environment.  Successful demonstration at customer site. Project approved.
- Efficient Network ENI3600 ATM PCI adapter card.  Helped John Williams of US Navy to extend Linux ATM driver for this product.  Also wrote PPPoE protocol for maximum theoretical throughput.
- MIPS evaluation board, a complete bootup of VxWorks Real-Time OS, enahnced Ethernet driver for maximum throughput.
- Motorola MPC850, a complete writeup of bootup sequence; wrote PPPoE from scratch, again.
- Intel i960, a complete writeup of bootup sequence and Ethernet driver for VxWorks RT-OS
- many Software-Defined Radio using many [tools](https://www.rtl-sdr.com/big-list-rtl-sdr-supported-software/)
- Motorola 68000, vendor OS, pure assembly programming, including floppy drive controller
- used to memorize the entire instruction set of Motorola 68000 and Intel x86-32 in hexidecimal; and programmed assembly using hexicode values, as well as mnenmonic opcode/operands.
- breadboard, I have lots, lots and lots of breadboards

# Writing

- I permanently ditched Microsoft Word as a writing environment in 2004.  I do all my writing in [joplin](http://joplinapp.org/) [Markdown](https://daringfireball.net/projects/markdown/) (including e-mails and paper-and-pencil writing)—it's incredibly intuitive, imminently readable, flexible, future proof, end-to-end encrypted, and lets me ignore formatting and focus on content.  I like it that I can use on Linux and Apple interchangably via [OwnCloud](https://owncloud.org).
- The key to my writing workflow is the magical [joplin](http://joplinapp.org/), which converts Markdown files into basically anything else.
- I store all my bibliographic references, books, and articles in a [BibTeX](http://www.bibtex.org/) file that I edit with [BibDesk](http://bibdesk.sourceforge.net/).
- I read and annotate all my PDFs with [Skim](http://skim-app.sourceforge.net/) (and [iAnnotate](http://www.iannotate.com/) on iOS), since both export annotations as clean plain text.

## Patent Efforts

- I've written, filed, and have been awarded several patents.  Those awarded
  patents are available upon request.  
- Filed patents are pending and hopefully will be awarded. 
- Unfiled patents will be kept as unfiled and unreported.
