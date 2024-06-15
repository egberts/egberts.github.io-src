title: Comparison of Large SVG File Viewers
date: 2024-06-11 06:00
status: published
tags: comparison, viewer, SVG, bison, python-graphviz, graphviz, DOT, PDF, Python
category: HOWTO
slug: comparison-svg-viewers-large-file
summary: A comparison of large-SVG viewers are reviewed here.
lang: en
private: False

Comparison of grpahical viewers for large SVG file are covered here.


Background 
=============
Was working on a NeoVim/Vim syntax highlighter for the `nft` command of nftables package on Linux.

Would make sense if I had a concrete visual view of this `nft` command syntax other than the cryptic lexer code deep in the `nftables` code.

NeoVim/Vim I need to see the parser as a whole for an application.  The parser
leverages the Bison lexer.

This `parse_bison.y` is a Bison lexer file for the `nft` command of nftables.org.  `nft` is the network filter for Linux OS.  These are the Bison lexer stats:

* 370 keywords/expression-tokens
* 828 transitions (rules)
* 1,385 grammars
* 2,377 states
* 6,438 Bison lexer lines
* 17,381 C lexer lines

As you can see, one needs to see the big picture before going into the nitty-gritty.

First step is to map the Bison file into DotGraph (.dot, formerly Ghostview, or .gv).  Execute:

```bash
bison --graph parser_bison.y
mv parser_bison.gv parser_bison.dot
```

A bit more about the DotGraph file:

* 22,820 DOT lines
* 1,200,000 bytes, DOT file

Converted the DotGraph file into SVG:

```bash
#!/usr/bin/env python3

import subprocess
import pygraphviz

# input_file='/tmp/parser.gv'  # current filetype, not used here
input_file='./parser_bison.dot'  # alternative older filetype

image_file='./parser_bison.svg'

print('Reading %s as DOT graph.' % input_file)
graph = pygraphviz.AGraph(
                   name='myGraph', 
                   filename=input_file, 
                   directed=True, 
                   strict=False
                  )
graph.layout(prog='dot')  # read DOT-format
graph.draw(image_file)
print('File %s created.' % image_file)
```

The resulting SVG file looks like:

* 156,711 SVG lines
* 33,300,000 bytes, SVG file

Convert it to PDF, just in case:

```bash
cairosvg parser_bison.svg parser_bison.pdf
```
* 9,200,000 bytes, PDF file

I have a 33MB SVG file that was translated from DotGraph (.dot).  And cannot view this DOT, SVG, nor PDF.

Summary
=======
None of today's viewer that I have tried in the past works on this large-sized
DOT file anymore.

Of the some 2-dozen window-based SVG viewers, the following were listed simply because they can load this crazy-huge 50MB-sized SVG file:

* Inkscape
* Okular
* Gwenview


Onward to see what works:

Inkscape
===========

And THERE SHE BLOWS!

```console
Gdk-Message: 11:35:43.122: Lost connection to Wayland compositor.
```

[jtable caption="SVG Viewers" separator="," th=0 ai="1"]
[Inkscape](https://inkscape.org), 1m45s, 
[Okcular](https://apps.kde.org/en/okular), 
[Gwenview](https://www.kde.org/),
[/jtable]


Alernatives
==============
Alternatively, you can splice out a portion of the view at DotGraph-level
before doing any SVG/PDF rendering:

More on this [here](https://egbert.net/blog/articles/viewing-extremely-large-dot-or-gv-graph.html)
