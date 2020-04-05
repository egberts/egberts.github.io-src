title: Vim Syntax File Layout
date: 2020-04-02 17:35
status: draft
tags: vim, syntax, file layout
category: research, vim, syntax
summary: How to organize a Vim syntax file used in highlighting.

I have a very large Vim syntax file and have organized it successfully.

Having created my 3rd syntax file (2 for private; 1 open source), some idea
should be documented about how to layout a future Vim syntax file.
Such organization would make it easier to continue expanding to engulf 
a complex logic such as ISC Bind named configuration.


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
3. Highlight definition, 1st-tier
4. Static pattern
  a. Static fixed pattern, contained
    1) Number
    2) Annotated Number
    3) Number with Unit
    4) Number with some optional non-numeric keywords
    5) String
    6) Single/Double quoted string
  b. Dynamic fixed pattern, contained
    1) multiple word choice
5. Dynamic pattern
  1. Simple regex
    c. Zone name and View name
    d. ACL name
    e. Domain name
    f. Full-path File specification
  2. Combo Regex
    a. IP4 Address
    b. IP6 Address
    c. multiple number patterns
6. All syntaxes, ted to only other syntax(es) (contained)
  a. Group-specific syntax
  b. Multi-Group syntax
7. All standalone syntaxes, not using 'contained'
  a. top-level things
  b. built-in words 
9. Vim script, ending

Vim Starting Script
===================
An example starting script (based on many examples and stock 
Vim plugins) would be:

```vim
" quit when a syntax file was already loaded
if !exists("main_syntax")
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


Highlighter Definition
======================

MANY syntax files are loaded at the same time, depending on the filetype
of your file being edited.  
You may end up loading JavaScript, HTML, CSS, Ruby, Python and PHP
simultaneously together.

It is important to ensure that ALL the names of your syntaxes does 
not conflict with the many other syntaxes that may be found in 
both your local (`~/.vim/syntax`) syntax or 
system-wide (`/usr/share/vim/vim81/syntax`) 
syntax directory.  The only way to tell is to use Vim `:syntax` command and
the `vlint` lint command.

A good way is to prefix all your syntax identifiers and definitions with a 4 to 8 letter prefix.
I re-used `named` because I had intended to replace it.

Some example of syntax identifiers are:

```vim
hi link  namedHL_Comment    Comment
hi link  namedHL_Include    Include
```

I used the Vim-supplied identifiers such as `Comment` and 
`Include` exactly once and used the corresponding 
my-prefixed identifiers (`namedHL_Comment` and
`namedHL_Include`).  

Underscore is optional in your identifiers but I use it to 
enhance readability because my syntax file is HUGE by others' standard.

