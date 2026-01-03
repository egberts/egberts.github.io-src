title: Postfix config ChangeLog
date: 2020-12-23 11:00
modified: 2026-01-03T0901
status: published
tags: postfix
category: research
summary: Changes made to Postfix config files
slug: postfix-config-changelog
lang: en
private: False

This research snippet is about the introduction, removal, or changes 
to the various keywords used in `main.cf` config file of Postfix.  
Only version 3.4.11 to 3.5.8 were examined on Debian 11 (bullseye/sid).

Postfix has a utility called `postconf` that will let you examine,
change, or validate the `main.cf` config file, currently in 
`/etc/postfix` or show its compiled-in default settings which we shall use here.

Checked against Postfix from version 3.4.11 to 3.5.8.

[jtable caption="Keyword changes in Postfix"]
keyword , version , action , Description 
maillog\_file\_rotate\_suffix , 3.5.2 , modified , replaced %M with %m (bug) 
info\_log\_address\_format , 3.5.0 , removed , was set to 'external' 
milter\_connect , 3.5.0 , modified , changed to 'j {daemon\_name} {daemon\_addr} v \_' from 'j {daemon\_name} {daemon\_addr} v' # (added underscore)
maillog\_file\_rotate\_suffix , 3.4.12 , modified , replaced %M with %m (bug) 
[/jtable]

How I Did This
==============
Steps to determine changes to Postfix `main.cf` config file.

```bash
THIS_VER=3.5.8
PRIOR_VER=3.5.7
mkdir temp; cd temp
git clone https://github.com/vdukhovni/postfix.git
cd postfix
git checkout v${THIS_VER}
make clean ; make
bin/postconf mail_version  # ascertain correct version
bin/postconf -d > ../postconf-output-defaults/postconf.default.${THIS_VER}
mgdiff postconf.default.${PRIOR_VER} postconf.default.${THIS_VER}
# Observe and note any differences
#
# Ignore keyword process_id
# Ignore keyword mail_release_date
# Ignore keyword mail_version
#
# Repeat above step with different versions
```

The only Debian package that was required was `libdb-dev` for the missing `db.h`
include file.

Exceptions
==========
v3.4.2 thru v3.4.10 did not compile due to major changes in libc include files, so these versions were skipped.

v3.4.0 thru v3.4.1 does not support Linux r5 due to its usage of the obsoleted SOCKADDR\_SIZE macro (and a few other obsoleted macro defines).
