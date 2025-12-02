title: Vim Syntax Development: A Faster Reloading of Syntax File
date: 2020-04-01 10:45
status: published
tags: vim, syntax, debugging
category: HOWTO
summary: How to reload Vim syntax file faster.

This blog is one of a series of HOWTOs for debugging of Vim syntax development.

Development Setup
=================

Typical debugging and development of a new Vim syntax is using the dual-window Vim sessions.  Each Vim editor will be editing:

* to DEVELOP a syntax for new highlighting
* to VIEW the new highlighting

Note:  Some of you may prefer to single-Vim session using split windows, 
instead of my suggested dual-Vim terminal session:
I prefer my simplistic X-WindowManager `ALT-Tab` key sequence here.  

Developing Syntax File
----------------------
Syntax file is where all the development of highlighting goes into.  
One won't be able to see any visible effect here.   

Let us call this Vim edit session in our first 
terminal console, our DEVELOPMENT window.
If I am creating a new syntax file, such as ISC Bind9 named configuration), I
would be editing `~/.vim/syntax/bind-named.vim`) file in this
DEVELOPMENT window.

Viewing Highlighted File
------------------------
Text file (example or under test)  is where we can view our new 
highlighting.  Second terminal console host the
second Vim editor session.  Let us VIEW the new highlights in VIEW window, from
reading syntax files changed by our effort made within DEVELOPMENT window.

Develop in one window; view in another window.  DEVELOP, VIEW, DEVELOP, VIEW.

Interactions
------------
To see any new highlighting, the VIEW edit session needs to reload 
the syntax file (that has been changed).  
One way to see new/changed highlighting is to perform closing and opening of this same test file.

At the beginning of my development cycle, lots of closing and opening files were going there.

I got tired.  I got tired of executing the following Vim command 
sequences to reload this syntax file in my edit session:

```vim
:wq
```

I am trying to show the new highlighting efforts made in VIEW window.  Fast.  I
made a single character change, and I need to see this change FAST.

At the same shell prompt to reopen the test example file, typing in:

```
vim named.conf
```

18 keystroke, sigh.  Each time I wish to view this edit change of a single character into my syntax file, 18 keystrokes.

Same Vim edit terminal session, same test example file; lot's of typing.

Of course, there is this bash shell history.  Let's try the bash history
approach (which sounds and works way better after the first few laborious times).

The new command sequences now are given below:

The same vim command:

```vim
:wq
```

Then new shell command:

```shell
# Press UP arrow key to recall last line from bash history
# Press ENTER to execute: vim named.vim
```

just to VIEW a change to the syntax file.  Now, it is minimized to seven (7) keystrokes.  

Bah.  Surely, there is that single keystroke method to do all that jazz somewhere.  

And there is.  One could do one of the followings:

* Forget the Vim write/quit `:wq` command
* Forget the bash shell command to open file in Vim editor session.

And replace all that with a single keystroke.

A single keystroke for viewing new syntaxes, instead of 18 or 7.

A keystroke that will reload the new Vim syntax within your VIEW, impacted by that very syntax file we are developing.


Single-Key Stroke Syntax Reloading
==================================

For this single keystroke to work well, we need to stay 
within the same VIEW (editor session of Vim editor) window 
throughout the whole time during our entire syntax
development:  Same Vim edit session.  No opening, no closing.

So, let us move those reloading of syntax commands back into a single Vim session.

Selecting Available Function Key
--------------------------------

To execute our command sequences of reloading new syntax with a single
keystroke, we need one available key.

Preferably that key is not hogged by others.  
That key may be already snagged by one of your many applications,
a window manager, or this Vim editor.

Function key is a common choice for remapping of such a key.

To choose a function key, we need to know what keys are available.  
Vim can list
what keys they have already defined; we must figure out what is not taken yet.

To list defined function keys, execute in Vim session:

```vim
:verbose map
```

And select a function key that is NOT defined from examining that `:verbose map` output.

I chose F12 for this example.

Defining Function Key
---------------------

With your choice of function key noted (or in mind), open the `~/.vimrc`.

```shell
vim ~/.vimrc
```

And inserted the following Vim script near the end of that file:

```vim
" Toggle reload of syntax files
"
noremap <F12> <Esc>:source $MYVIMRC<CR>
inoremap <F12> <C-o>:source $MYVIMRC<CR>
```

Replace my <F12\> example with your choice of available function key(s).

Save and quit the Vim edit session, by executing within Vim session:

```
:wq
```

Next time the vim is executed, F12 key is now active and ready to use.

VIEW, VIEW, VIEW
================
In the VIEW window, it will be able to stay up .... forever.  
Never closing, never re-opening.  

Pressing the `F12` key will now be able to reload your `.vimrc` and 
ALL of your local (`~/.vim/syntax/*`) and system-wide
(`/usr/share/vim/vim81/syntax/*`) syntax files..

Instant highlighting change(s).

Easier development.

Easier debugging.

Single keystroke.

Enjoy.



