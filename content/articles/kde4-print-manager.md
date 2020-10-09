title: kde-add-printer - Failed to get a list of devices 'Invalid argument'
date: 2020-07-08 13:35
status: published
tags: KDE5, Debian9, print-manager 
slug: kde-add-printer-invalid-argument
category: HOWTO
summary: How to fix "Failed to get a list of devices 'Invalid argument'" in KDE5

This is for those who have umask of 0027 at root account level, like this:
```bash
umask 0027
```
in their `/etc/bash.bashrc`.

I was trying to add a printer in Debian9 after installing KDE5 print-manager.

```console
$ umask
0027
$ apt install print-manager
$ kde-print-manager
```
And it started reporting the error 

<p align="center">
<img src="/images/kde5-add-printer-error.png" alt="KDE5 Add Printer Error Message"/ width=320>
</p>

ANALYSIS
========
To dig into the error message, I listed all the processes having the word
"print":

```console
$ ps auxwww | grep print
test     19457  0.0  0.3 524456 14548 ?        Sl   Jul05   0:06 kde-add-printer --add-printer
test     23007  0.0  1.7 521076 70588 ?        Sl   14:18   0:00 /usr/bin/kcmshell5 kcm_printer_manager
test     23828  0.4  0.4  55132 16160 pts/4    S+   14:44   0:00 vim kde5-print-manager.md
root     23843  0.0  0.0   6208   828 pts/3    S+   14:46   0:00 grep print
```

And re-ran the `kde-add-printer` under `strace` to list out all attempts at file
`open()` system calls.

```console
$ strace -f kde-add-printer > /tmp/kde.strace 2>&1
```
Then filtered out the `strace` output file for `open()` statements:

```console
$ strings /tmp/kde.strace | grep open | less
```
Skipped the LD.SO loadings, past the locale-archive, past all the fonts, icons,
and noticed an open error in the CUPS library.

WORKAROUND
==========
After adding my account name `test` to the `lp` group in `/etc/group`, performed
a desktop logout, then re-login.

it works.
