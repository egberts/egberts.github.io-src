title: Vim Syntax File Layout
date: 2020-04-02 17:35
status: published
tags: vim, syntax, file layout
category: research, HOWTO
summary: How to organize a Vim syntax file used in highlighting.

DRAFT DRAFT DRAFT
=================

So you want to tackle a new text language and create your very own
Vim syntax highlighting.  

You may feel that you will be soaring pass 
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


A quick comparison with other Vim syntax files shows the following top 7
syntax count.

```shell
grep contained /usr/share/vim/vim81/syntax/* | wc -l
```


produces a list:
[jtable]
Vim syntax file, numbers of `contained` keywords
neomuttrc.vim, 523
redif.vim, 447
muttrc.vim, 321
nsis.vim, 276
postscr.vim, 260
css.vim, 259
php.vim, 248
[/jtable]

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
Except this syntax file is written and executed in **Vimscript** format.  

Your favorite editor can create this syntax file.  

Syntax files may be found in the following directories:

* System - /usr/share/vim/vim81/syntax
* Local - $HOME/.vim/syntax

We will use `vim` as our choice of editor in this blog demostration.  You will
find that `vim` also has its own syntax highlighting for its own Vimscript
format.  

Then we can [live-prototype](https://egbert.net/blog/articles/debugging-bind9-syntax-file-of-vim.html)  our syntax file by having your text edit session 
read it directly from out from our local syntax directory.

Outline of Vim Syntax File
--------------------------

If you are trying to learn programming of syntax in this blog, it 
might be best read this in sequential order from here on.

If you are trying to capture some syntax tricks, go directly to the end.

Some basic outline of a Vim syntax file can be ordered as:

1. Vim Standard Header
2. Vim script, starting
3. Naming Convention
4. Highlight definition, 1st-tier
5. Static pattern
(a) Static fixed pattern, contained
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

Every file should have some decent meta data in form of a text-based
file header.

Vim community supplies such a standard Vim header.

Use of this standard header should appear 
before attempting to be delivered toward the Vim community.  
It's also the first step
before getting your stuff accepted into stock Vim core.

This header template of a real working example is given below:
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


Language meta refers to the format of the text file. 

Maintainer should be the email address.

Last change is helpful in comparing versions.

Filenames refer to the informal declaration of what type of file
will this syntax template be used for.  You can specify
a comma-separate list and have multiple `Filenames:` lines, as I've done.

Note: I've tightened the regex pattern from
older `named*.conf` used by the current stock Vim named syntax 
and broke it up into several variants.  

Reason are:

* some other app is also using 'named9999.conf'.
* more sense for an enterprise/large-whitelab to split up the `named.conf`
into the following 

Split-up is done by using `include` statements within its 
main `named.conf` config file.

Such split-up of a `named.conf` is typically done in following directory tree:

```
/etc/bind/named.conf
  |
  + acl-named.conf
  + channels-named.conf
  + controls-named.conf
  + hz.cache.home
  + hz.cache.lab
  + keys/
  + local-named.conf
  + masters-named.conf
  + mz.home
  + mz.ip4.127
  + mz.ip4.7.168.192
  + mz.lab
  + mz.localhost
  + sz.example.com
  + options-named.conf
  + servers-named.conf
  + statistics-named.conf
  + trusted-keys-named.conf
  + green.view
  + red.view
  + chaos.view
```


This filespec naming convention makes it easier to do 
a 'vim <first 1-or-2 letter>' to tab myself a bash-completion 
then edit that file.  It's quicker than `named-options.conf` which
would require `vim n<tab>o<tab>` to edit. And easier to find.
Easier to add HUGE amount of comments for each statement
and not deal with a 6,000-line named conf file.  

Alternatively, some may prefer the following filespec naming 
convention:

```
/etc/bind/named.conf
  |
  + named_acl.conf
  + named_channels.conf
  + named_controls.conf
  + named.ca   # that's the db.zone.[home|root]
  + db.hint.cache.zone
  + keys/
  + named_local.conf
  + named_masters.conf
  + db.master.home.zone
  + db.master.ip4.127.rev
  + db.master.ip4.7.168.192.rev
  + db.master.lab.zone
  + db.master.localhost.zone
  + db.slave.example.com.zone
  + named_options.conf
  + named_servers.conf
  + named_statistics.conf
  + named_trusted_keys.conf
  + view.green
  + view.red
  + view.chaos
```


Oh, wait; that's off-topic.  Nonetheless, I've covered most enterprises'
naming conventions on Bind9 config filenames.  
Such enterprises are Sun/Solaris,
[Oracle](https://docs.oracle.com/cd/E19683-01/816-7511/dnsintro-23/index.html), UC Berkeley, O'Reilly, 
[Mice-and-Men](https://www.dns-school.org/Documentation/bind-arm/Bv9ARM.ch06.html), and [Zytrax](https://www.zytrax.com/books/dns/).

Then last metadata, the remark part, of the Vim header is actually followed 
by a 300-line comment section.

Vim Starting Script
===================
Remember, this syntax file contains the Vimscript language and format.

So, we got a little Vimscript going at the beginning and end of the this syntax
file.

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

Follow that up with:

```vim
" I've got the largest named.conf possible.
" it's a heavily commented named.conf file containing every 
" valid statements, options, and clauses.
" sync gets barely triggered here.
syntax sync match namedSync grouphere NONE "^(zone|controls|acl|key)"

let s:save_cpo = &cpoptions
set cpoptions-=C
```


`syntax sync` provides several anchor points in a large text file in which
for Vim to start the syntax engine at.  Despite 4,300 lines, it 
is not beneficial until you go over 5,000 lines (which I might so I put it
there, just in case.)

`save_cpo` enables saving of Vi compatible behaviors set by other syntax 
files (if any).

`set cpoptions-=C` takes away just the C option from the entire settings
that an end-user or a system syntax may have set.  ['C' option](http://vimdoc.sourceforge.net/htmldoc/options.html#'cpoptions') represents "Do not concatenate sourced lines that start with a backslash."

```
" `syn case match` means that all keyword/identifier 
" must be exact match, unless `\c` has been prefixed 
" in the `match` (or `region`) statement.
syntax case match
```


The Pseudo-BNF of Bind9 named configuration shows that
both lower-case and mixed-case keyword and identifier are used.

For Vimscript, I need to make a choice for this `syntax case` argument: `match` or `nomatch`.

`nomatch` mode choice 
---------------------

** Vim keywords are forced in mixed-case mode
** Regex patterns are selectively forced into lower-case mode

`match` mode choice
-------------------

** Vim keywords are forced lower-case
** Regex patterns are selectively mixed-case

Lucky for me, I had already pre-mapped out all the Pseudo-BNF syntaxes 
for this Bind9 named configuration.   

And based on the majority of its BNF static text pattern were 
mostly in the forced lower-case.

So, I chosed `syntax case match` which forces lower-case and lets 
my regex supports mixed-case.

Naming Convention
=================

Readablity is important.  Consistency is also important.

Selecting a Prefix Name
-----------------------
Naming convention of syntax identifier makes it easy to associate 
with the specific component of each phrase within your text body 
in question.  

NOTE: it is important to ensure that ALL the names of your 
 syntaxes does **NOT** conflict with the many other syntaxes 
 that may be found elsewhere outside of your syntax file, such as in 
 both your local (`~/.vim/syntax`) syntax or 
 system-wide (`/usr/share/vim/vim81/syntax`) 
 syntax directory.    Vim namespace of syntax identifier is a 
 global (shared) pool, so don't get greedy.

The only way to tell if there is a conflict is to use Vim 
[`:syntax`](http://vimdoc.sourceforge.net/htmldoc/syntax.html) command 
and the Python-based Vim-lint [`vint`](https://github.com/Vimjas/vint.git) lint command. I've found the vint more recent on Github rather than via `pip install vim-vint`.

Latest vim-vint version is 0.4a4

A good way is to prefix all your syntax identifiers and 
definitions with a 4 to 8 letter prefix after 
checking against the `/usr/share/vim/vim81/syntax` for any already-taken 
prefix letterings.

We will start all syntax identifiers with `named`.  I re-used `named` 
as I had intended to replace it.

Mapping Keywords to Syntax Identifier
-------------------------------------
A simple config file may contain:

```vim
server 127.0.0.1 {
    provide-ixfr no;
    notify-source 10.0.0.1 port 53;
    };
```

And the Bind Administration Reference Manual (ARM) has many Pseudo-BNF 
diagrams, such as:

```bnf
server <ip_addr> {
    [ provide-ixfr <boolean>; ]
    [ notify-source <ip_addr> [ port <port_no> ]; ]
    };
```

And we will need to map our new syntax identifer for each part of the 
config text file.  We can use those documented BNF as our labeling guide.

For the snippet of config given above, we could use the following
example as our syntax identifiers:

```vim
namedStmtServerKeyword
namedStmtServerIP4Addr
namedStmtServerSection  " that pair of curly braces
namedStmtServerSectionProvideIxfrKeyword
namedStmtServerSectionProvideIxfrBoolean
namedStmtServerSectionNotifySourceKeyword
namedStmtServerSectionNotifySourceIP4Addr
namedStmtServerSectionNotifySourcePortKeyword
namedStmtServerSectionNotifySourcePortValue
```


Underscore is optional in name of syntax identifiers, but I shall 
use it to enhance readability because my syntax file is HUGE 
and DEEP by others' standard.

Partial example config file be like:

```named
server 127.0.0.1  // ... continue with more components
```

I started out using a fully terse naming convention for 
this `server` statement:

```vim
syntax match namedStmtServerSectionIP4Addr contained skipwhite
\ /\S\+/

syntax keyword namedStmtServerKeyword server skipwhite
\ nextgroup=namedStmtServerSectionIP4Addr
```

Bind makes available many options within each statement.  
And many clauses within each options.  
Plus, Bind support RECURSION of certain syntax.  

As a result, 
these identifiers' naming got longer, longer and longer until they
look like this:

```vim
syn keyword namedStmtOptionsViewDualStackServersPortWildcard ...
```


Ok, this is wrong.  I've been looking at this super-long syntax identifier
and decided to pare it down even further.  `Stmt` is extraneous after 
its first keyword were detected so all other options following that main
keyword need not have its already discarded scope called `Stmt`.

A section is a region between a pair of curly braces.  Most top-level
statements have an accompanying section to contain all of its 
associated options:

```named
zone red_zone {
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
    zone red_zone;
    # ...
    };
```

Noticed that many of those same options are also used in different statements?

I made a name, `ViewZone` naming to reflect that this option has being 
reused in both the `view` and the `zone` based (see config snippet above).

`OptionsView` refers to the fact that a syntax
can be used in both `zone` section and `view` section.  This will 
happen ... a lot!

Note: In fact, Bind9 has over 200 options just within that `view` 
statement alone, and Bind's `options` statement has over 357 
additional options.  
Many of those options are shared not only between the 2 statements, 
but with 3 or 4 other statements as well.  

Couple that with over 16 top-level statements. Too much typing.  Way too much.

Wait for it, we have this `OptionsServerViewZone` syntaxes too.  That's four.
It's time to use that `namedOSVZ_` annotation from there on, as applicable.

Let us make a table, an annotation table to codify all these 
statements and save me some strong typing (and maybe avert carpal-tunnel
syndrome, or something.)

[jtable]
Annotated letter(s), Bind named config statement 
A, `acl`
C, `controls`
Ch, `channels`
K, `keys`
M, `masters`
Mk, `managed-keys`
O, `options`
P, `plugin`
S, `server`
Sc, `statistics-channels`
T, `trusted-keys`
V, `view`
Z, `zone`
[/jtable]

So, with less typing, we will condense that to 
just `namedOV_` to represent that the option being used in 
both `options` and `view` sections.

So far, we have transformed the old full-terse naming convention, 
and produced:

```vim
syn keyword namedOV_DualStackServersPortWildcard ...
```
Mmmmmm, a bit more readable.  Instead of `DualStackServers`, I'm 
going to condense it to just the first two word parts of its keyword:

```named
    dual-stack-servers port *;
```


can be pared down to just:

```vim
syn keyword namedOV_DualStack_PortWildcard /\*/ 
```

Oh yeah, forgot to mention the liberal use of underscore.  

I'm done with this naming convention.  
It's readable and concise enough for future updates and expansion.


Highlighter Declarations
======================

Next is the highlighter declarations.  Many of the pre-defined colors
can be found in `syncolor.vim` in `/usr/share/vim/vim81/syntax/` directory.

They are but not limited to:

[jtable]
Color, Description
cyan, `Comment`
magenta, `Constant`; `String`; `Number`
yellow, `Statement`
light cyan, `Identifier`
orange, `Special`
light blue, `PreProc, Include
light green, Type
light blue, Underlined
[/jtable]

To prevent disruption by other syntax files, I would add aliases
for standard highlight colors.
Some example of Bind-related color-based syntax identifiers are:

```vim
hi link  namedHL_Comment    Comment
hi link  namedHL_Include    Include
hi link  namedHL_Statement  Statement
hi link  namedHL_Option     Statement
hi link  namedHL_CLause     DiffAdd
hi link  namedHL_Identifier Identifier
hi link  namedHL_Error      Error
hi link  namedHL_Builtin    Special
hi link  namedHL_String     String
hi link  namedHL_Number     Number
hi link  namedHL_Operator   Operator
```

Noticed that I'm using `HL\_` after `named`?  It stands for 'H'igh'L'ight.

I used the Vim-supplied identifiers such as `Comment` and 
`Include` exactly once and used my newly-defined  
identifiers (`namedHL\_Comment` and `namedHL\_Include`) thereafter instead.

I noticed the many of the stock Vim syntax files put their 
highlight declarations at the end of their script.

I put these declarations near the beginning of my syntax file.  
Why?  Because it's measurably faster.  And discovered this by accident
as my file got bigger.


Color Philosophy
--------------------
Your color selection is based on what your terminal supports, your $MYVIMRC is
doing, and what the ftdetect and ftplugins are doing.  

MANY syntax files can loaded during the initial part of startup, depending on the filetype of your file being edited.  

You may end up loading JavaScript, HTML, CSS, Ruby, Python and PHP
simultaneously together:  

Lucky for me, it is just my `named.vim` and Vim's `syncolor.vim`.

Having your own color-based alias identifier makes it easier to 
change color scheme and apply consistently across this syntax file.  

Note: I am looking forward to a 256-color
scheme on this file.  Being stuck on 7-color is no fun but I would 
have to expend considerable effort to make it work satisfactorily 
in both `light` and `dark` mode in order to get it accepted.

Static Pattern
==============
Now it's time to start defining syntaxes.

The simplest syntax is a fixed-length unchanging (static, non-regex) pattern.

There's a reason for starting simple and going complex later onr:  Vimscript
and its `syntax` command uses the LAST matched pattern.

There are some more static keyword that are built-in into Bind 
named configuration syntax.

```vim
syn keyword named_Any any 
syn keyword named_None none 
syn keyword named_Localhost localhost 
syn keyword named_Localnets localnets 
```

They don't change, don't have regex and are common throughout the 
configuration file.

Wildcard and semicolon is one other such pattern that we 
must use regex (via `match`) because these characters are 
non-alphabetic and non-numeric so we must use `//` notation
to contain those special characters.

```vim
syn match namedSemicolon /;/
syn match namedWildcard /\*/
```

Oh, noticed the backslash before asterisk?  Many characters requires
escaping in regex.  

I've got to add a short table on which character to escape here someday.  But
it's documented [here]().

[jtable]
`\\v`,	`\\m`,  `\\M`,   `\\V`,		matches 
 ,   , 'magic', 'nomagic'
  `$`,	   `$`,	    `$`,     `\\$`,	matches end-of-line
  `.`,	   `.`,	    `\\.`,   `\\.`,	matches any character
  `\*`,	   `\*`,    `\\\*`,  `\\\*`,	any number of the previous atom
  `()`,	  `\\(\\)`, `\\(\\)`, `\\(\\)`,	grouping into an atom
  `|`,	  `\\|`,    `\\|`,    `\\|`,	separating alternatives
  `\\a`,  `\\a`,    `\\a`,    `\\a`,	alphabetic character
  `\\\\`, `\\\\`,   `\\\\`,   `\\\\`,	literal backslash
  `\\\.`, `\\\.`,   `\.`,     `\.`, 	literal dot
  `\\\{`, `\\\{`,   `\{`,     `\{`, 	literal '{'
  `a`,	   `a`,	    `a`	       `a`,	literal 'a'
[/jtable]
{only Vim supports \m, \M, \v and \V}

I would take Google's Vim Syntax Guideline and use `\\m` where I can.


Number Pattern
--------------
We have a generic number pattern with no range checking.

```vim
server 192.1.1.124/24 {
    edns-version 15;
    };
```

For `15` part of the config above, we can provide a generic 
syntax that can be reused by many other options' syntax:

```vim
syntax match named_Number /\d\+/
```

BUT, it would make for a faster screen redraw if the `+` symbol
were to be replaced with a range of integers, such as:

```vim
syntax match named_Number /\d\{1,10}/
```

So, as a rule, `+` and `\*` should be avoided, whenever it is possible.

(When we start talking about 'contained', move following over there) TODO: I gotta stop you there.  There's some interesting limitation on the
reusing of Vim syntax going on there.  As I've discovered, that
sharing of common syntax may not work beyond its selected groupings.

Number with Unit
----------------
Often times we wonder if the syntax is in millisecond, second, minutes,
hours, days, or weeks.  And this is a real problem with Bind 
configuration, they don't make it easy to remember "unit"  
without consulting the manual.
I do have a master Bind configuration file in Python that notes
the unit for each statements, options, and clauses in [here](https://github.com/egberts/bind9_parser/blob/master/examples/rough-draft/namedconfglobal.py)

But we can note then incorporate such unit of its keyword 
and incorporate the value range into its syntax name.

```vim
syn keyword namedOV_MaxClientsPerQuery ...
```

Query is that unit, but there is so few of of those self-explanatory "unit".

Here's another example:

```vim
view red_view {
    max-refresh-time 53;
    };
```

Which translates into:
```vim
syn match namedOV_MaxRefreshTimeCount /\d\+/ ...

syn keyword namedOV_MaxRefreshTime max-refresh-time
\ nextgroup=namedOV_MaxRefreshTime
\ containedin=namedStmt_ViewSection
```
Well, we know that the unit is `Time`, just don't know what kind of time.  
We had to consult the ARM documentation to determine what increment this kind of time is. Turns out to be in 'seconds'.  Rewrite the
syntax name as:

```vim
syn match namedOV_MaxRefreshTime_Seconds /\d\+/ ...
...
```

Specific syntax name probably won't help anyone except the most 
saavy Vimscript highlight debugging person who can leverage 
the syntax identifier name.
Maybe we can somehow shows the type of "unit" in the status
bar below (future task?).

Number with Annotation
----------------------
Then there is this BNF:

```bnf
max-cache-size [ <sizespec> ];
```
Number or Non-Numeric Keywords
--------------------------------

Dynamic Pattern
===============
5. Static pattern
(a) Static fixed pattern, contained
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

Vim Ending Script
===================

Insert the following at the end of your Vimscript:

```vim
let &cpoptions = s:save_cpo
unlet s:save_cpo

let b:current_syntax = 'bind-named'

if main_syntax ==# 'bind-named'
  unlet main_syntax
endif

```

Whew, isn't that something?
