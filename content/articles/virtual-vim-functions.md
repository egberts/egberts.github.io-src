title: Virtual Vim Function
date: 2020-06-01 11:11
modified: 2025-12-30 05:36
status: published
tags: vimscript, design
category: research
summary: How to create building blocks for large-scale syntaxes of Vimscript highlighting

Finished the [Bind9 named](https://github.com/egberts/vim-syntax-bind-named) syntax highlighter for Vim editor.  Was a
large undertaking, some 3700 lines.

Then I went on to get started for the NFTABLES syntax highlighter for Vim editor
as well.  But, the task of doing another 3,000 lines seems crazy at this point.
Never mind the fact that I am crazy to do it in the first place.

Next step, let's makes some Vimscript functions to shorten the amount of typing.  How
to begin?

Pre-Design Angst
================
Vimscript `syntax highlight` and `syntax keyword/match` are the two basic
building blocks for creating some nice highlightings.

I even saw the [StackOverflow question](https://vi.stackexchange.com/questions/25632/design-guideline-for-doing-both-autocompletion-and-highlighting)
on this topic, but alas... no answer.

When I reread my completed Bind9 Vimscript file and my false starts
of [VIM-NFTABLES](https://github.com/egberts/vim-nftables) (before becoming
disenchanted and started this blog), improvements to look for
are higher abstraction of building blocks for
connecting two objects together in Vimscript, that
is ... system re-engineering or smarter engineering (here, we hope).

Highlighting is easy; A -> B.  A is the color and B is the object.  So we will
skip the `hi link` out of this blog for now.

Syntax keyword/match will remain to  be our focus from thereon.

Other mechanisms like `syntax cluster` (virtual group labeling)
or `syntax region` (OR group clustering) will be cover at the end.


System Design
=============

To simplify system engineering, `syntax keyword` has 3 major components:

* "parent" groupname
* child groupname(s)
* parser pattern (`syn match` or `syn keyword`)

Basic Condition Operation
-------------------------

The condition operator consists of a relationship with a parent to a child
which produces a characteristic of an AND operator:  A child
cannot happens unless its parent happens.

(A sidebar: for OR operation, we use regex or even `syntax region`).

With `syntax keyword`, AND operation occurs when a parent condition AND
any one of the child condition occurs.

(Another sidebar:  Highlighting occurs AFTER meeting its condition,
or 'condition met before highlighting are to occur'.


Initial BNF
-----------
Let's introduce the first parser grouping of NFTABLES; that is `list`
command.  I extracted a Bison group from the
[parser_bison.y](http://git.netfilter.org/nftables/tree/src/parser_bison.y) file in Github.

```
base_cmd : /* empty */ add_cmd
   ...
    | LIST list_cmd
   ...
```

For the first Bison group (`base_cmd`), this is simple as declaring
a Vimscript of:
```vim
syn keyword nftables_LIST list skipwhite nextgroup=nftables_LIST_list_cmd
```

Detailed explanation of above Vim command:  Vim
instruct editor to label this operation as `nftables_LIST` and to
look for a `list` keyword after skipping any and all whitespaces,
if the keyword matches then go to the set of group called
`nextgroup=`.  In the above example, there is one nextgroup:
the `nftables_LIST_list_cmd`.

(Note: noticed that there is no Vim syntax `contained` option, hence we
are going to limit the total 'uncontained' (top-level rules) to
a firstly words like `list`, `flush`, `table`, and `add`.
All other group rules must have a `contained` option for its
`syn match` or `syn keyword`.

In devising such a group name like `nftables_LIST_list_cmd`, I chose
the following Vimscript naming convention separated by
underscore as:

* basename of `nftables` which is the name of the Vim package as well.
* LIST, the all capitalized label for actual keyword matched
* `list_cmd` is the same name of its actual Bison parser grouping.

With a label like that, it should be little or no problem cross-referring
with the `parser_bison.y` (or any parser file) and its grouping name for
years to come.

Second Parser
-------------
Let us go in a bit further with the second parser grouping.

Following the `list_cmd` (as shown above) by searching for `list_cmd` in
the parser (`parser_bison.y`) file, we find:

```bison
list_cmd :
   ...
    | RULESET ruleset_spec
   ...
```

Now we have another keyword, `ruleset`.  And a new (Bison) parser rule
named `ruleset_spec`.

Another vim command would be:

```vim
syntax keyword nftables_RULESET_ruleset_spec contained ruleset skipwhite
\ nextgroup=nftablesCluster_ruleset_spec
```

More on this later as I develop the polymorphic Vim functions.

Abstractions Needed
===================

Simple Object
-------------
In order to have building blocks, some form of object abstraction needed.

Our first object has 1 match and 1 or more outward flows per `syntax
match` command:

1. pattern
2. goto A
2. goto B
2. goto C
2. goto n

and a label for the object itself.

The trick is determine how to handle multiple outward flow with
the simplistic Vim function call.

Using the function arguments, one could use a list variable containing
a bunch of gotos then pass that list into function argument(s).

Or we could use multiple arguments (after the label and pattern arguments)
in form of virtual argument (`vargs`).

Labeling Crisis
---------------
The other factor to consider is the name of the object.

I want to see that label, the name of the object, and have it be
able to tell me WHERE among the syntax tree that they
specifically address or reside at.

The problem is that if such syntax tree becomes an cyclic graph, then
the act of tacking on a small name to its label string would lost its
meaning rather as the acyclic graph becomes ... cyclic.

`nftables` (nor ISC Bind9) are not cyclic, they may have
repeatable or recursive syntaxes, but it is not a circular syntax cyclic
graph.
Given that, we're co-opting a label string of an object that tells us where
deep into the syntax graph it represents.

```
      A
    /   \
   B     C
  / \   / \
  D  E F   G
```
Object names like `A_C`, `A_B_D` and `A_C_F` tells us where in the syntax tree
it refers to.

Reusing objects like D (replacing C in our example below) is also the
goal because we have some terminated objects while
same object (reused again) are not terminated.  Such as
`A_B_D` or `A_D_F` below:

```
      A
    /   \
   B     D
  / \   / \
  D  E F   G
```

It is already increasing our new virtual function with complex arguments.
Recap of arguments of our ideal virtual function is:

1. current syntax pathway
4. a constructed label name of its object
2. highlight color
3. pattern
3. goto(s)
and this function returns:

In adding a "PATH" way into our syntax tree somewhere,
adding already to its overburdened argument list of our
not-so-fancy, but dreamy, virtual function.
K.I.S.S. principle is going gone, eh? Or is it?
Time to try and scale back.

Explosive Object Label Naming
===========================
Syntax pathway typically comprises a node, a node-to-node
characteristic, and a child-node.
Here, we can eliminate node-to-node characteristics as being singular.
Node and child-node shall remain.

Somewhere in the middle of a syntax tree, a child-node is going to want
a way to return back to anywhere else in the syntax tree (middle, top,
next to the end), and often so, it is going to unrelate to the
original point of its syntax pathway.  So preservation and passing of this
labeling, addressable
labeling, of each syntax object is a must.

Can we fold that much needed information of this syntax pathway into
its object label name?  Let us explore this.

What if we use an object name whose notation spells out the pathway of
such syntax tree?
Something like:

   `LIST__ruleset_spec__table_name`

whose label would be representational to the last node in the diagram below:

```
        `list`
          |
       ruleset_spec
          |
        table_name
```

A cursory examination of the `nftables` `parser_bison.y` shows that
syntax tree is not going to be more than 8 level deep, with an average of 5.
Our ideal label would have 10 words in its label, on average.

I'll risk pushing the Vim's limitation on the length of such label, to
see if this works.

Working with a static fix-length appendable string name to represent
a point in the syntax tree does call for lots of string manipulation
to work with.  Such manipulation like appending the label of a child node,
or prefixing the package name (`nftables_`) before its declaration.

It was either that approach, or go even more programmatically using
a set list type of variable that would hold the object of each layer
in its syntax tree such as:

```vim
pathway = [ 'LIST', 'ruleset_spec', 'family_spec_explicit' ]
```

Downside of using set list is that we would have to reconstruct the string
to our full pathway label from such a set list and for each time we are
looking for an external function name.

But this set-list approach would probably end up requiring yet another
function argument toward our beleaguered virtual function name (which still
on the drawing board); one where it instructs a certain node to return
to another arbitrary node in the syntax tree.

Bad news, deep review of the Vimscript does not support passing a set list
in the function argument.  Actually, it supports ONE set list but
as the last argument of a function.   Bah.

Go with a string for its pathway, for now.

First Syntax Tree
=================
For the first definition cut of our argument list for our first virtual
function, we will focus on the simple `nft list ruleset` command. And
pull in all Bison groups for this command syntax.

From the nftable `parser_bison.y` source file, we list out the Bison
groups used to support this command.

    base_cmd -> `list` list_cmd
    list_cmd -> `ruleset` ruleset_spec
    ruleset_spec -> `family_spec_explicit` | *empty*

or diagrammatically as:
```digraph
    base_cmd
      |
    list_cmd  -> 'list'
      |
    ruleset_spec -> 'ruleset'
    /    \
 *empty* family_spec_explicit   -> 'ip'
```
Note: It's nice to know that '*empty*' branch makes other branches
(of the same layer) ... optional.

In short, we got our EBNF syntax of

    list ruleset [ netdev | bridge | arp | ip | ip6 | inet ] [;]

Let's focus on the simplest approach of reverse engineering: its end-node,
that last child node.

Reiterating the nftable Bison `family_spec_explicit` group here:

```bison
family_spec_explicit	:	IP		{ $$ = NFPROTO_IPV4; }
			|	IP6		{ $$ = NFPROTO_IPV6; }
			|	INET		{ $$ = NFPROTO_INET; }
			|	ARP		{ $$ = NFPROTO_ARP; }
			|	BRIDGE		{ $$ = NFPROTO_BRIDGE; }
			|	NETDEV		{ $$ = NFPROTO_NETDEV; }
			;
```
This Bison group makes the following EBNF:

```bnf
    netdev | bridge | arp | ip | ip6 | inet
```

The corresponding Vim script for above EBNF would be:
```vim
syntax keyword nftables_family_spec_explicit contained
\     netdev bridge arp ip ip6 inet
\ skipwhite
\ nextgroup=?????
```
No need for the nextgroup, remove that.  Oh, wait.

Syntax Error Checking
=============
I forgot, we're going to be checking syntax for error as well as highlighting,
syntax checking is not the goal of Vim editor but its a doable goal
and a laudable one, at that.  So, to do both highlighting AND syntax checking,
we are going to declare a generic Error highlighter for our script file:

```vim
hi link nftables_Error Error
syntax match nftables_Error /[ \ta-zA-Z0-9_./]\{1,64}/ skipwhite
```
OK.  This `nftables_Error` is going to be the bane of your development cycle.
But its real purpose is to be a lifesaver and a timesaver during
virtual prototyping.  If and when you goofed in your development,
you'll know it fast and glaringly so in BOLD RED highlighting and
precisely so as in exact positioning.  Note 'exact positioning' to mean
cursor position.

I cannot tell you how much this cursor positioning error will tell you
and help narrow down which offending `syntax` command goofed.
So, try and keep that `syntax match nftables_Error` enabled as much as
possible during virtual prototyping.  I know, I resisted from
commenting that out during virtual (which bites me much later on).
This "Early Detection" is your friend.

Moving on to the most commonly used Syntax group, end of syntax.

End of syntax group rule is necessary because it helps the Vim
syntax engine to reset and look from the top-level parsers.
It also helps with the Vim `syntax sync`'ing of highlighting, most notably
when it is a numerous-line syntax highlighting.  Not
having this end of syntax rule will break highlighting in the middle
of a big statement.  Also breaks your own syntax checking as well.

First draft of end of syntax group is:
```vim
syn match nftables_EndOfSyntax contained /[ \t]\{0,16}[^\n;# ]/
```
or shorten it to
```vim
syn match nftables_EOS contained /[ \t]\{0,16}[^\n;# ]/
```
No need to see beyond 16 character for an error.  First character
is more than sufficient, using the value 16 shows you where
the error is by its big long red box.

Starting Point
--------------
Back to our newest and latest `list ruleset` syntax string, the end-node
Bison group would translate to this Vim command:
```vim
syntax keyword nftables_family_spec_explicit contained
\    netdev
\    bridge
\    arp
\    ip
\    ip6
\    inet
\ skipwhite nextgroup=nftables_EOS
```
I formatted it this way so that the 'match' keywords indent
in another 4-char purely for readability sake.  Not overly concerned
with excessive line counts ... yet.

Still haven't made a function prototype yet because this is as terse
as it is going to be.... no need for a function there.

Basic Building Blocks
---------------------

Need some items out of the way with the simplest of building
blocks.  This requires:

1.  Common prefix labeling
2.  Highlighter

Common prefix of variable name are require within Vim environment as
to ensure that it doesn't interferes with other Vim plugins.
Let us use `nftables_` as our common prefix.  It doesn't make sense
to be doing:

```vim
    let newpathway = 'nftables_'.l:thisnode
```

nor should we be doing:
```vim
let global_prefix = 'nftables'

function a(b)
  let new_pathway = s:global_prefix.'_'.a:b
endfunction
```

Probably want a function call to obtain the prefix like this:
```vim
function NPrefix(qualifier)
  if (a:qualifier != '')
    return 'nftables'.a:qualifier
  else
    return 'nftables'
  endif
```

This way, we can get `nftablesHL_Underline` color this way:

    let xxx = NPrefix('HL').'_'.a:color

or, `nftables_LIST` for our `list` keyword:

    let xxx = NPrefix('').'_LIST'

Might be a small penalty in terms of function call overhead.  But it makes
it easier to move packages around.

Onward to highlighter function.

```vim
function Nftables_Hilite(thisnode, color)
  exec 'hi link '.NPrefix('').'_'.a:thisnode.' '.NPrefix('HL').'_'.a:color
endfunction
```
If we call NFtables_Hilite like this:
```vim
call Nftables_Hilite('family_spec_explicit', 'Statement')
```
it executes the following command:
```vim
hi link nftables_family_spec_explicit nftablesHL_Statement
```

Going back to reading code, let's expand it further:
```vim
call Nftables_Hilite('family_spec_explicit', 'Statement')
call Nftables_Hilite('ruleset_spec', 'Statement')
call Nftables_Hilite('family_spec', 'Statement')
call Nftables_Hilite('TABLE', 'Statement')
```
reads a lot quicker using short terse strings, but places itself better
within the syntax tree when expanded into long-form.

```vim
hi link nftables_family_spec_explicit nftablesHL_Statement
hi link nftables_rulespec nftablesHL_Statement
hi link nftables_family_spec nftablesHL_Statement
hi link nftables_TABLE nftablesHL_Statement
```
Blah reading...  Our shorten form of coding is more readable.

This will prove useful as we move on to node-based functions.

Lateral Analysis of a Node
--------------------------
Before we go to the next higher level of nftables syntax tree, we
need to know if this `family_spec_explicit` end-node
gets used elsewhere
throughout the nftables syntax tree, and hopefully also as an end-node.

Crap, `family_spec_explicit` is also used as a middle-node, as
part of the `ct helper l3protocol <here> ;` (Bison `ct_helper_config` group).
Notice that
the semicolon (Bison `stmt_separator` group) is mandatory (as opposed
to the semicolon usage of our earlier

    list ruleset [ <family_spec_explicit> ] [;]

being optional.) This impacts us because now we have two different logics
on the handling of this semicolon symbol lexical: one is optional,
other is mandatory.

Do we design a function that can have a flag telling us whether it is
an end-node or not?  Or make two separate functions? Mmmm.

Here, we're going to take the two-functions approach.  Let me tell you
why: reading code should have functions whose name tells us what it does.   
Thus one cannot always figure out what the argument does or not
at first glance.  Two-function approach, it is.

Even bigger reason for choosing the two-function approach is that we want to
cut down the permutation of arguments, notably the 'next\_group'
argument;  that one is a variable here.  The small price to pay is
a bit more complex coding repeats elsewhere but with little variances.

```vim
let nftables_log = 0
let nftables_debug = 0

function Nftables_FamilySpecExplicit( pathway, thisname, color, nxt_groups )
  let label = 'family_spec_explicit'
  if (a:pathway != '')
    let new_pathway = a:pathway.'__'.a:thisname
  else
    let new_pathway = a:thisname
  endif
  let this_grpnam = Nprefix('').'_'.l:new_pathway
  call Nftables_Hilite(a:color, l:this_grpnam)
  if (a:nxt_groups != '')
    let cmd_sk_add = ' nextgroup='.a:nxt_groups
  else
    let cmd_sk_add = ''
  endif
  let cmd_sk = 'syntax keyword '.l:this_grpnam.' contained netdev bridge arp ip ip6 inet skipwhite '.l:cmd_sk_add
  exec cmd_sk
  if (a:logme != 0)
    exec 'syn list '.l:this_grpnam
  endif
  return l:this_grpnam
endfunction

# and
function Nftables_FamilySpecExplicit_EOS( pathway, thisname, color, nxt_groups )
  let label = 'family_spec_explicit'
  if (a:pathway != '')
    let new_pathway = a:pathway.'__'.a:thisname
  else
    let new_pathway = a:thisname
  endif
  let this_grpnam = Nprefix('').'_'.l:new_pathway
  call Nftables_Hilite(a:color, l:this_grpnam)
  if (a:nxt_groups != '')
    let cmd_sk_add = ' nextgroup='.a:nxt_groups.','.'nftables_EOS'
  else
    let cmd_sk_add = ''
  endif
  let cmd_sk = 'syntax keyword '.l:this_grpnam.' contained netdev bridge arp ip ip6 inet skipwhite '.l:cmd_sk_add
  exec cmd_sk
  if (a:logme != 0)
    exec 'syn list '.l:this_grpnam
  endif
  return l:this_grpnam
endfunction
```

That variance between two functions is merely the inclusion/exclusion
of `nftables_EOS` for `nextgroup=`.  Sad, uh?  But it's worth it.

Note: Do not confuse the EOS with nextgroup. (OK, I got confused there).
EOS refers to the fact that the run of syntax tokens can end with a
carriage return or semicolon; whereas nextgroup is the run-on
further down of even more syntax rules:

You can have a state where there is an EOS, but no mandatory nextgroup
```nft
    list ruleset
                ^
    list ruleset ip6
                    ^
```
Or no EOS, yet have a mandatory nextgroup at this point
```nft
    list ruleset ip6
        ^
```

Or both EOS, and a mandatory nextgroup at this point
```nft
    list ruleset ip6
                ^
```

but the last combination is "no EOS, no nextgroup" and is not
an viable option here. This No-EOS-no-nextgroup, if you let it happen,
will become your PROTOTYPING error condition for our nftables syntax tree,
that would end up being hard to detect by yourself.
Ensure that there is an EOS or a nextgroup or both; and never missing
either one.

And here we want to be doing syntax error checking from thereon.

An error condition appears at this point of which it will be highlight as
bright red box:
```nft
    list ruleset ip6 no-such-thing
                     ^^^^^^^^^^^^^
```

Next Level Vim Group
--------------------
After `family_spec_explicit`, next layer up is `ruleset_spec`.

The Bison `ruleset_spec` group is:
```bison
ruleset_spec		:	/* empty */
			{
				memset(&$$, 0, sizeof($$));
				$$.family	= NFPROTO_UNSPEC;
			}
			|	family_spec_explicit
			{
				memset(&$$, 0, sizeof($$));
				$$.family	= $1;
			}
			;
```
There's an OR operation there:  *empty* or *family_spec_explicit*.

Expanding Vim `list ruleset` syntaxes, latest would be:
```vim
syntax keyword nftables__ruleset_spec__family_spec_explicit contained
\ ruleset skipwhite nextgroup=nftables__family_spec_explicit,nftables_EOS
```
or we can simplify as:
```vim
let famspec_exp =  Nftables_FamilySpecExplicit(
\                      'LIST__ruleset_spec',
\                      'family_spec_explicit',
\                      'String',
\                      'nftables_EOS')

let rulespec = Nftables_RulesetSpec(
\                  'LIST',
\                  'ruleset_spec',
\                  'Type',
\                  l:famspec_exp.',nftables_EOS')

call Nftables_top_keyword('list', l:rulespec_group)
```

Noticed the use of return value  applys toward the next function?
That is connector between the child-node to its node.

That is the basic virtual function constructor.

Problem, Problem Solving
------------------------
OK.  Each function must be able to figure out the full Vim group name
based on the terse variant in each parameter of its function.

For the `pathway` argument, that is pretty easy to do: we add
the package prefix via `NPrefix('')` string generating function.

For the `thisnode` argument, we prefix it as usual, append
the pathway, then add `thisnode` to make:

```console
   let new_groupname = NPrefix('').'_'.a:pathway.'_'.a:thisnode
```

For the hightlight color name, we call the `Nftables_Hilite()` function:
```vim
   call Nftables_Hilite( l:new_groupname, a:color )
```

So Far, so good.  Nice and simple.

The thorny problem is the `next_groups` argument.  It gets made to
contain either a single long string containing comma-separated values
(CSV) or broken up into multiple arguments (and at the end of
the function
argument list) using `varg` technique (think C-language `printf()`).

Note: One couldn't pass a set list variable through a function argument.
I've tried and failed.  Vim documentation has horrible examples too.
StackOverflow didn't help either.

Also another thorny but orthogonal problem of `next_groups` is
do we support the simplified terse (`thisnode`) version of the
group name or the full-spec group name, which
included `NPrefix()`, `pathway`, as well as `thisnode`.

I've tried to model the 'terse' variant of the group name but
it doesn't have ability to figure out its pathway before its expansion.
This means that the onus is on the developer to painstakingly type
out in full the entire Vim group name in the `next_groups`
for all their virtual Vim programming.  Might not be a bad idea there,
a longer reading but concise.

VARGS or Long-CSV-String
========================
Back to the problem of function argument for `next_groups`:
variable function (`vargs`) arguments or a single long-CSV-string?

Long CSV string makes it nice to drop in next to the Vim syntax
`nextgroup=` options.  No string manipulation needed there.

The real question is that is there a reason to work with individual
group inside this `next_groups` argument? The answer is yes.
Ensure that ERROR CHECKING occurs to ensure that such a group name
is properly and typed and that such a group name EXISTS!
Ahhhhh, existance test.  Remember the previous problem, we've decided
on full-spec Vim group name as an approach so this works here as well.

I've got a story to tell you about my
3400-line ISC Bind9 vim syntax file and its lack of existance test.
But nevermind that, trust me, you'll want this existance test
as this is a serious timesaver and a
debug-session-avoidance exercise here.

I actually prototyped the long-CSV-string approach for a bit and ran
into a bit of a coding challenge earlier on with the overall design. I couldn't
get a satisfactory breakout of a long CSV string into
each individual group name so that an existence test of its group
name gets performed against. StackOverflow to the rescue!

```vim
function Nftables_top_keywords(thisnode, keywords, next_groups)
  " thisnode:
  let nxtgrps = split(a:next_groups,',')
  for s:a in l:nxtgrps
    if !exists('*'.s:a)
      echoerr 'Groupname: '.s:a.' does not exist.'
    endif
  endfor
  let cmd_sk = 'syn keyword '.a:thisnode.' '.a:keywords.' skipwhite nextgroup='.string(a:next_groups)
  exec l:cmd_sk
endfunction
```


