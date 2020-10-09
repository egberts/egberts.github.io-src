title: Vim Syntax File Layout NEW
date: 2020-04-02 17:35
status: published
tags: vim, syntax, file layout
category: research, syntax
summary: How to organize a Vim syntax file used in highlighting.

DRAFT DRAFT DRAFT
=================

So you want to tackle a new text language and create your very own
Vim syntax highlighting.  

You feel that you will be soaring pass 
the 50-syntax rules.  Fifty-rules and things get complicated.  

400-rules-and-beyond, then strict organization is a must, not only
for maintenance and future expansion, but your sanity (or others') will go
after a few years of absent upgrading.

I have a very large Vim syntax file and have organized it successfully.

Having created my 3rd syntax file (2 for internal corporate; [1 open source](https://github.com/egberts/vim-syntax-bind-named/)), 
some idea should be documented about how to organize such a large 
Vim syntax file.

Such organized Syntax file would make it easier to continue 
in expanding to engulf additional complex logic in the future, such as 
a [ISC Bind](https://www.isc.org/bind/) named configuration file.

At this writing, there are over 848 syntaxes for ISC Bind9 named configuration
file.  You can determine this by executing:

```shell
grep contained ~/.vim/syntax/bind-named.vim | wc -l
```

A quick comparison with stock Vim syntax files shows the following top 7.

```shell
grep contained /usr/share/vim/vim81/syntax/* | wc -l
```
produces a list:
```
./php.vim 248
./css.vim 259
./postscr.vim 260
./nsis.vim 276
./muttrc.vim 321
./redif.vim 447
./neomuttrc.vim 523
```

So,  you can see that I've gone a bit past Vim's limitation there.  
And I'm not done adding!!!


Vim Syntax File Layout
======================

What is a Vim Syntax File?
--------------------------
A Vim syntax file can enable Vim editor to perform the parsing of 
text and the application of highlighting and edit operations 
against its body of text.

Format of the Vim syntax file is UTF-8, Unix (no CR-LF, just CR) text file.

Your favorite editor can create this text file.  

Syntax files may be found in the following directories:

* System - /usr/share/vim/vim81/syntax
* Local - $HOME/.vim/syntax

We will use `vim` as our choice of editor in this blog demostration.

And prototype our syntax file in our local syntax directory.

Outline of Vim Syntax File
--------------------------

I'll lay the groupings out and you can pick-and-choose what you need.

I might point out the irony that this Vim syntax file is a bottom-to-top 
dependency approach (and the only viable and maintable way).  

If you are trying to learn syntax in this blog
might be best read in sequential order from this point on.  

If you are trying to capture some syntax tricks, go start at the bottom.

Some basic outline of a Vim syntax file can be ordered as:

1. Vim Standard Header
2. Vim script, starting
3. Naming Convention
4. Highlight definition, 1st-tier
5. Static pattern
  a. Static fixed pattern, contained
    1) Number
    2) Annotated Number
    3) Number with Unit
    4) Number with some optional non-numeric keywords
    5) String
    6) Single/Double quoted string
  b. Dynamic fixed pattern, contained
    1) multiple word choice
6. Dynamic pattern
  1. Simple regex
    c. Zone name and View name
    d. ACL name
    e. Domain name
    f. Full-path File specification
  2. Combo Regex
    a. IP4 Address
    b. IP6 Address
    c. multiple number patterns
7. All syntaxes, ted to only other syntax(es) (contained)
  a. Group-specific syntax
  b. Multi-Group syntax
8. All standalone syntaxes, not using 'contained'
  a. top-level things
  b. built-in words 
9. Vim script, ending



Vim Standard Header
===================

Vim community supplies a standard Vim header in which should appear 
before attempting to be delivered to the Vim community.  It's the first step
before getting your stuff into stock Vim core.

A real example is given below:
```vim
" Vim syntax file
" Language:     ISC BIND named configuration file
" Maintainer:   egberts <egberts@github.com>
" Last change:  2020-03-12
" Filenames:    named.conf, rndc.conf
" Filenames:    named[-_]*.conf, rndc[-_]*.conf
" Filenames:    *[-_]named.conf
" Location:     http://github.com/egberts/bind-named-vim-syntax
" License:      MIT license
" Remarks:
```

The remark section is actually followed by a 300-line comment section.

Vim Starting Script
===================
An example starting script (based on many examples and stock 
Vim plugins) would be:

```vim
" quit when a syntax file was already loaded
if !exists('main_syntax')
  if exists('b:current_syntax')
    finish
  endif
  " My syntax name is 'bind-named'
  let main_syntax='bind-named'
endif
```
The above is useful when multiple Vim plugins comes into play.

Ideally, you want your own script to be loaded just once.

```
" `syn case match` means that all keyword/identifier 
" must be exact match, unless `\c` has been prefixed 
" in the `match` (or `region`) statement.

syn case match
```

My basic problem with Bind9 named configuration style is that both lower-case
and mixed-case are used and supported, so I had a choice between:

* Choice A

** Vim keywords are forced in mixed-case mode
** Regex patterns are selectively forced into lower-case mode

* Choice B

** Vim keywords are forced lower-case
** Regex patterns are selectively mixed-case

Lucky for me, I pre-mapped out all the BNF syntaxes for this Bind9 named
configuration.   And majority of its BNF static text pattern were 
in the forced lower-case.
So, I chosed Choice B: Vim `keyword`/`iskeyword` are in forced 
lower-case and my regex supports mixed-case.

Naming Convention
=================

Readablity is important.  Consistency is also important.

Naming convention of syntax identifier makes it easy to associate 
with the specific phrase within your text body in question.

Furthermore, it is important to ensure that ALL the names of your 
syntaxes does **NOT** conflict with the many other syntaxes 
that may be found elsewhere outside of your syntax file, such as in 
both your local (`~/.vim/syntax`) syntax or 
system-wide (`/usr/share/vim/vim81/syntax`) 
syntax directory.  

The only way to tell if there is a conflict is to use Vim 
[`:syntax`](http://vimdoc.sourceforge.net/htmldoc/syntax.html) command 
and the Python-based Vim-lint [`vint`](https://github.com/Vimjas/vint.git) lint command. I've found the vint more recent on Github rather than via `pip install vim-vint`.

Latest vim-vint version is 0.4a4


A good way is to prefix all your syntax identifiers and definitions with a 4 to 8 letter prefix.
I re-used `named` because I had intended to replace it.

Some example of syntax identifiers are:

```vim
hi link  namedHL_Comment    Comment
hi link  namedHL_Include    Include
hi link  namedHL_Statement  Statement
hi link  namedHL_Option     Statement
hi link  namedHL_CLause     Statement
hi link  namedHL_Identifier Identifier
hi link  namedHL_Error      Error
hi link  namedHL_Builtin    Special
hi link  namedHL_String     String
hi link  namedHL_Number     Number
hi link  namedHL_Operator   Operator
```

I used the Vim-supplied identifiers such as `Comment` and 
`Include` exactly once and used my newly-defined  
identifiers (`namedHL_Comment` and `namedHL_Include`) instead.

Having your own identifier makes it easier to change color scheme and apply
consistently across this syntax file.  I am looking forward to a 256-color
scheme on this file.  Being stuck on 7 color is no fun.

Underscore is optional in your identifiers but I use it to 
enhance readability because my syntax file is HUGE by others' standard.

I started out with fully terse naming convention such as:

```vim
syn region namedStmtOptionsSection start=+{+ end=+}+
```

There are many options within that Options statement.  As a result, 
the naming got longer, longer and longer:

```vim
syn keyword namedStmtOptionsViewDualStackServersPortWildcard ...
```

Ok, this is wrong.  I've been looking at this super-long syntax identifier
and decided to pare it down even further.  `Stmt` is extraneous after 
its first keyword were detected so all other options following that main
keyword need not have `Stmt`.

A section is a region between a pair of curly braces.  Most top-level
statements have an accompanying section.

```named
options {
    # ...
    allow-update {1.1.1.1;};
    allow-v6-synthesis AAAA; // obsoleted
    also-notify { 123.123.123.123; 2.2.2.2; };
    alt-transfer-source *;
    # ...
    };
view red_public {
    # ...
    allow-update {1.1.1.1;};
    allow-v6-synthesis AAAA; // obsoleted
    also-notify { 123.123.123.123; 2.2.2.2; };
    alt-transfer-source 1.1.1.1;
    # ...
    };
```

`OptionsView` is repeatedly used to refer to the fact that this syntax
can be applied in both `Options` section and `View` section.  In fact, 
Bind9 has over 55 keywords just within `Options` alone.  

Couple that with over 16 top-level keywords. Too much typing.  

Let us make a table, a secton table:

[jtable]
Annocated letter(s), top-level Bind statement section
A, `acl`
C, `controls`
Ch, `channels`
K, `keys`
M, `masters`
Mk, `managed-keys`
O, `options`
S, `server`
T, `trusted-keys`
V, `view`
Z, `zone`
[/jtable]

Majority of Bind9 options are found in multiple sections, listed above.

So, less typing, we will condense that to just `namedOV_`. 

So far, we have:

```vim
syn keyword namedOV_DualStackServersPortWildcard ...
```
Mmmmmm, a bit more readable.  I'm going to condense it to just the 
first two words of its keyword:  `dual-stack-servers`` can be pared down
to just:

```vim
syn keyword namedOV_DualStack_PortWildcard contained /\*/ skipwhite
\ nextgroup=namedSemicolon
```

Oh yeah, forgot to mention the liberal use of underscore.  

I'm done with naming convention.

Highlighter Definition
======================

Color ght Philosophy
--------------------
MANY syntax files are loaded at the same time, depending on the filetype
of your file being edited.  
You may end up loading JavaScript, HTML, CSS, Ruby, Python and PHP
simultaneously together.

Vim Ending Script
===================
