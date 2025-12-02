title: Terminal, console, emulator, oh, my!
date: 2025-01-13 08:18
status: hidden
tags: terminal, text terminal, console terminal, raster terminal, vector terminal
category: research
summary: 
lang: en
private: False

"Glass TTY", a reference to a `TERM=dumb` character-oriented cathode ray video display unit (VDU),
having no cursor-positioning, coloring, nor screen erase capability.

In 1970, Cursor-positioning came next to [DEC VT05](https://en.wikipedia.org/wiki/VT05) and Hazeltime 2000.


* Character-Oriented
In the old days ... never mind, character-oriented terminals are still being used today.

Anything over serial communication to a video display unit (VDU), notably having a cathode ray tube, is a 
character-oriented terminal: the protocol, wire, and VDU operates one character at a time.

Even our UNIX pipe socket handles exactly the same thing using `netcat` (`nc`), and `minicom`.

Today, Linux terminal (`/dev/tty0`) console is one example of a character-oriented terminal.  

* Pseudo-TTY

Pseudo terminal is a pseudo-device pair that provides a text terminal interface without 
associated virtual console, computer terminal or serial port hardware.




[jtable caption="This is caption" separator="," th=1 ai="1"]
# caption - the table caption
# separator - default is comma
# th - table header (=0 means disable)
# ai - auto-index, adds a column numbering starts at 1
columnA, columnB, columnC
row1, dataB1, dataC1
row2, dataB2, dataC2
# : if the date is not specified and DEFAULT_DATE is set to 'fs', Pelican will rely on the file’s “mtime” timestamp, and the category can be determined by the directory in which the file resides.
[/jtable]
