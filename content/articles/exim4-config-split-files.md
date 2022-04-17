title: Double `conf.conf` filetype in Exim4 Config File
date: 2022-03-23 03:58
modified: 2022-04-04 10:34
status: published
tags: Exim4, SMTP
category: HOWTO
summary: Why is the Exim4 configuration file have a strange filetype of `.conf.conf`?
slug:
lang: en
private: False


Firstly, what are the files used when using the Split-File Configuration for Exim4?

Output
======

First, let us go into the single output file that Exim4 uses:

   `/var/lib/exim4/config.autogenerated`

Every time you start or restart Exim4, that auto-generated config file gets read in.

To update that file, read on.

Input
=====

Three input methods are used to create the auto-generated config file that Exim4 daemon relies on.

* Your settings: `/etc/exim4/update-exim4.conf.conf`
* Template engine: `/etc/exim4/exim4.conf.template`
* All Settings: `/etc/exim4/conf.d` subdirectory

Your Settings
-------------
Naturally, you would go to your own site-specific settings in `/etc/exim4/update-exim4.conf.conf`.

Why is the file type named `...conf.conf`, simply because the tool used to generate all this split-files is called `update-exim4.conf`.   

Yeah, it seems counter-intuitive but that is a utility script, not a config file, so add that extra `.conf` when editing.

