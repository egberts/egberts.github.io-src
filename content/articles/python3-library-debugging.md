title: Debugging Python executable and libraries
date: 2020-10-13 12:00
status: published
category: HOWTO
tags: Python, debug, Pelican
keywords: Pelican, Python
summary: How to debug package-installed Python executable and libraries.
lang: en
private: False

You've installed a Python package into `/usr[/local]` and it blows up.

Now, how to debug it?  There are several ways, but this one is the easiest.

It does require `ipython` because of its built-in debugger (via `--pdb` option).

In my real-world example, Pelican, static website generator, is blowing up.

Easiest
=======
So, let us show the way on how to debug an installed Pelican package without 
having to pull down a copy of Pelican Git repo, or recreating your 
development environment: the price for that is installing `ipython` package.

```bash
cd mywebsite
ipython --pdb -m pelican -c -- \
    -s pelicanconf.py -o output  \
    content
```
Change `mywebsite` to where your Pelican website directory is.
Also change `output`, `pelicanconf.py`,  and `content` as needed
if you used your own naming convention.


A generic bash script is given below:
```bash
WEBSITE_DIR=${HOME}/work/github/mywebsite

MYPELICAN_CONF=${WEBSITE_DIR}/pelicanconf.py
CONTENT_DIR=${WEBSITE_DIR}/content
OUTPUT_DIR=${WEBSITE_DIR}/output

ipython --pdb -m pelican -c -- \
    ${CONTENT_DIR} \
    -o ${OUTPUT_DIR} \
    -s ${MYPELICAN_CONF}
```

Command Line Approaches
======================

PDB CLI Approach
-------------
With a traditional debugger such as pdb, this supports commands 
such as `c` for continue, `n` for step-over, `s` for step-into etc.), 
but you don't have direct access to an IPython shell which can be 
extremely useful for inspection of many objects.

```bash
cd project/my_python/this_python
python -pdb this_python
```

IPDB CLI Approach
-------------
With a traditional debugger such as ipdb. This supports commands such as c for continue, n for step-over, s for step-into etc.), but you don't have direct access to an IPython shell which can be extremely useful for object inspection.

```bash
cd project/my_python/this_python
python -ipdb this_python
```

Modified Source Approaches
=========================

PDB Line Magic
--------------
You can always add this in any cell:
```python
import pdb; pdb.set_trace()
```
and the debugger will stop on that line.

IPython Line Magic
------------------
At beginning of same Python source file, add this line
```python
from IPython.core.debugger import set_trace
```
then add a tracer near where you have trouble at:
```
set_trace()
```


Drop-Down Approaches
====================

IPython Drop-Down
-----------------
Using IPython by embedding an IPython shell in your Python script code. 
You can do from IPython `import embed`, and then use `embed()` in your code. 

When your program/script hits an `embed()` statement, you are dropped into 
an IPython shell. 

This allows the full inspection of objects and testing of Python code 
using all the IPython goodies. 

However, when using `embed()`, you can't step-by-step through the code 
anymore with handy keyboard shortcuts.

IPython Magic Mode
------------------

You can use IPython's `%pdb` magic. Just call `%pdb` in IPython and when 
an error occurs, you're automatically dropped to ipdb. 
While you don't have the stepping immediately, you're in `ipdb` afterwards.
All pdb command options are then available.

This makes debugging individual functions easy, as you can just load 
a file with `%load` and then run a function. 
You could force an error with an assert at the right position.

`%pdb` is a line magic. Call it as `%pdb on`, `%pdb 1`, `%pdb off` 
or `%pdb 0`. If called without argument it works as a toggle.

When an exception is triggered, IPython can optionally call the interactive pdb debugger after the traceback printout. %pdb toggles this feature on and off.

The initial state of this feature is set in your configuration file (the option is InteractiveShell.pdb).

If you want to just activate the debugger AFTER an exception has fired, without having to type ‘%pdb on’ and rerunning your code, you can use the %debug magic.


Esoteric Approaches
===================

Debugging IPython from Python3.
```bash
python3 -m pdb /usr/bin/ipython notebook
```
