title: Debugging Pelican using PyCharm
date: 2024-06-20 18:00
status: published
tags: Python, Pelican, PyCharm, debug
category: HOWTO
summary: How to debug Pelican in PyCharm
slug: pelican-python-debugging
lang: en
private: False

Pelican croaked.  This is no longer simple as doing:

```bash
python -m pdb  pelican
```

Not anymore.  Too many subprocesses for a CLI-based Python debugger.

Enters in PyCharm: PyCharm Integrated Developer Environment (IDE) is an awesome debugger!

<em class="m-block m-note">Note: This article HOWTO assumes that you have your own Pelican theme ready for with this article: (simply copy recursively)</em>

Unfortunately, the Pelican guidelines correctly wants you to use `~/virtualenv` instead
of PyCharm's `~/venv`: and we can see why; JetBrain PyCharm does not enable 
different venv for different projects (with JetBrain, all your projects share the same venv) ... easily.

But PyCharm is not that easily configurable to let each project have their own virtual environment, but it can be done and will show you how later.

== Installation ==

Create a work area for a plug-in debug session.


```bash
cd ~/admin/websites/example.test/
gh repo clone https://github.com/getpelican/pelican.git
```

=== Setup your static site generator area ===
The location of your static site generator website is not in the `pelican/pelican` nor `pelican` directory, it is a new area (apart from pelican source).

Create a subdirectory of any name (we use `debug-table` here).

```bash
cd ~/admin/websites/example.test/
mkdir debug-table
```

Copy your existing Pelican SSG area into this `debug-table` or create empty directories to start with.

This Pelican website must contain the minimum directories:

* `content`
* `content/articles`
* `plugins`
* `output`

And this Pelican website must contain the minimum files:

* `pelicanconf.py`

The `pelicanconf.py` configuration file is only for non-publishing (`make html` or `invoke build`).

<div class="m-text m-note">Note: If you copied this configuration file, you probably want to reduce the `PLUGINS` variable and, if necessary, its corresponding `PLUGINS_PATH` variable as well.</div>

Copy the lone plugin into your website area.

cd /home/user/admin/websites/example.test/debug-table/plugins
gh repo clone https://github.com/burakkose/just_table.git
```

We will be using just 1 Markdown article file for our debug session:

```bash
# Check `[pelican|publish]conf.py` for `PATH` 
# (not Bash's PATH, but Pelican's, usually `content`)
cd ~/admin/websites/example.test/${PATH}
cd articles
vi tables.md
```
and fill it with
```markdown
title: Table test
date: 2024-06-20 11:00
status: published
tags: table
category: test
summary: testing table 1, table 2, table 3
lang: en
private: False

`jtable]`
[jtable]
1, 2, 3
4, 5, 6
[/jtable]

`jtable caption="This is caption"]`
[jtable caption="This is caption"]
1, 2, 3
4, 5, 6
[/jtable]

`jtable th="0"]`
[jtable th="0"]
1, 2, 3
4, 5, 6
[/jtable]

`jtable th="1"]`
[jtable th="1"]
1, 2, 3
4, 5, 6
[/jtable]

`jtable ai="0"]`
[jtable ai="0"]
1, 2, 3
4, 5, 6
[/jtable]

`jtable ai="1"]`
[jtable ai="1"]
1, 2, 3
4, 5, 6
[/jtable]

`jtable separator=","]`
[jtable separator=","]
1, 2, 3
4, 5, 6
[/jtable]

`jtable separator=":"]`
[jtable separator=":"]
1: 2: 3
4: 5: 6
[/jtable]

`jtable separator="|"]`
[jtable separator="|"]
1 | 2 | 3
4 | 5 | 6
[/jtable]

`jtable caption="This is caption" separator="|" th=0 ai="1"]`
[jtable caption="This is caption" separator="|" th=0 ai="1"]
1, 2, 3
4, 5, 6
[/jtable]

<!--
# caption - the table caption
# separator - default is comma
# th - table header (=0 means disable)
# ai - auto-index, adds a column numbering starts at 1
-->
```

== PyCharm Setup ==

If this is your first time running PyCharm, a dialog will appear to let you create your first project.

Enter in the Location to your newly created `pelican` directory:

   cd ~/admin/websites/example.test/pelican 

=== For a new VirtualEnv direcetory ===
Click the "down" arrow next to "Python Interpreter".

Select the radio button next to "New Environment using".  Change its pulldown textbox to "VirtualEnv".

Under "New environment using 'Virtualenv'", change "Location" to the Pelican's preferred virtual environment:

    /home/wolfe/virtualenvs/pelican

Check the "Inherit global site-packages"

Uncheck the "Create a main.py welcome script" checkbox.

Click "Create" button.

=== For reusing an existing Pelican VirtualEnv directory ===

TBA

=== Import Project ===


=== Debug Run Configuration ===

Add a new Run Configuration for use with your new debugging session

==== Run/Debug Configuration Dialog ====
Select the `toolbar` -> `Run` -> `Edit Configuration` menu subitem to pop up a new `Run/Debug Configuration` dialog box.

At the menu toolbar, press the '+' symbol (or Alt-Insert).

Select `Python` from the menu pull down.

Fill out as below:

Name: pelican table
Store as a project file:  (checked the checkbox)
Run: Pythone 3.11 (venv) ~/venv/bin/python
script: /home/wolfe/admin/websites/egbert.net/debug-table/pelican
script parameters: -D -v -v -v -v -s pelicanconf.py -o output content
working directory: ~/admin/websites/example.test/debug-table

At the Modify Options hyperlink (or Alt-M), select:

* Add source roots to PYTHONPATH


Do not use tilde ("~") in any of your pathspec.  

Pelican hanadles path relatively from your current working directory. Make sure that `plugins` and `content` is in your working directory.

Alternatively, you can use abolute pathspecs like in:
                   /home/user/admin/websites/example.test/debug-table/content \
                   -o /home/user/admin/websites/example.test/debug-table/output \
                   -s /home/user/admin/websites/example.test/debug-table/pelicanconf.py


At the bottom right of your `Run/Debug Configuration` dialog, press the `Apply` button.

Then press then `Run` button and enjoy debugging.


If you are debugging a plugin, you need to add a breakpoint inside the pelican.run() function in `pelican/pelican/__init__.py` due to multi-subprocess boundary.
