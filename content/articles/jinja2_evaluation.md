title: Jinja2 evaluation
date: 2021-09-06 15:32
status: published
tags: jinja2, pattern
category: research
summary: Evaluating Jinja2 for text-based configuration files
lang: en
private: False


Jinja2 v2.12

Jinja2 (v2.12) has an excellent templating system in which to fill in 
the text of parameters for various text-based configuration file.

Problem lies is the clutter caused by adding Jinja2 programming within
its template file (toward the original configuration file in question)
and its degree of difficulty in maintainability when it comes
to adding complex options and the extensive validation needed to go with it.

Adding Jinja2 construct into a configuration file used in templating would
result in nearly 2x (or even 3x) explosion in size of its file.

Validation would be compounded by multiple options (for example,
ssh_comments, ssh_comments_short, ssh_comments_detailed, and 
ssh_comments_developer).

To troubleshoot a missing or extra line-feed/carriage-return, 
it would require tracking down the missing '-' in '-%} terminator
or the free-standing line-feed/carriage-return.  This is a noted
downside when prototyping a new template file and even more so
when making changes as application evolves with adding/deleting
configuration keyvalue settings.

This jinja2 templating is essentially a no-go when it comes to
maintainability of the sshd_config/ssh_config configuration files.

Unfortunately, Ansible/Chef/Puppet make intensive use of Jinja2.

= SUMMARY =
There has to be a more simpler way to deal with this forking of
configuration text files.

Like with Bind9 named.conf file, it may be better
to use an (Python) array to maintain each configuration
item and its name, description, default value, value range,
and secondary action enforcement of its value based on
other configuration item(s).

Using an array template makes for easier fixing/addition/deletion
of configuration items based on verisioning, user preference of
its output of its final configuration text file.

A working example for Bind9 named.conf is given 
by my Github python code [namedconfglobal.py](https://github.com/egberts/bind9_parser/blob/master/examples/rough-draft/namedconfglobal.py).
