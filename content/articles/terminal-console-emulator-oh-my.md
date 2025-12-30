title: Terminal, console, emulator, oh, my!
date: 2025-01-13 08:18
modified: 2025-12-30 05:37
status: skip
tags: terminal, text terminal, console terminal, raster terminal, vector terminal
category: research
summary: 
lang: en
private: False

"Glass TTY", a reference to a `TERM=dumb` character-oriented cathode ray video display unit (VDU),
having no cursor-positioning, coloring, nor screen erase capability.

In 1970, Cursor-positioning came next to [DEC VT05](https://en.wikipedia.org/wiki/VT05) and Hazeltime 2000.


* Character-Oriented
In the old days ... never mind those character-oriented terminals used today.

Anything over serial communication to a video display unit (VDU), notably having a cathode ray tube, is a 
character-oriented terminal: the protocol, wire, and VDU operates one character at a time.

Even our UNIX pipe socket handles the same thing using `netcat` (`nc`), and `minicom`.

Today, Linux terminal (`/dev/tty0`) console is one example of a character-oriented terminal.  

* Pseudo-TTY

Pseudo terminal is a pseudo-device pair that provides a text terminal interface without 
associated virtual console, computer terminal or serial port hardware.

