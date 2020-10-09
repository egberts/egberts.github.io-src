title: Setting up UNIX lp on Debian9 for Brother HL-D5470DW laser printer
date: 2020-07-08 13:55
status: published
tags: lp, printer, laster printer, Brother
slug: unix-lp-brother-hl-d5470DW
category: HOWTO
summary: How to set up an lp queue to Brother HL-DS470DW laser printer on Debian


The Brother HL-D5470DW already has IPP network protocol set up.  But this
article is for the ordinary UNIX lp "feed print job to print daemon" and
said Brother printer.

Configuration File
------------------

Edit the `/etc/printcap` file:

```bash
vim /etc/printcap
```

Add the following entry to the `/etc/printcap` file:
```console
# /etc/printcap: printer capability database. See printcap(5).
# You can use the filter entries df, tf, cf, gf etc. for
# your own filters. See /etc/filter.ps, /etc/filter.pcl and
# the printcap(5) manual page for further details.

# Key   Replaced By
# %P    printcap entry primary name (printer)
# %Q    queue requested
# %h    short host name (host)
# %H    fully qualified host name (host.dns.whatever)
# %R    remote printer (rp value)
# %M    remote host (rm value)
# %D    date in YYYY-MM-DD format

# Replace `rm=` value with IP address of Brother printer
# Add `|lp` to first field to make this your default printer, 
#    if more than one exists.

rlp|lp|Remote printer entry:\
        :lp=:\
        :cm=Dungeon printer:\
        :rm=192.168.1.253:\
        :rp=brother-hl0-5470dw:\
        :lf=/var/log/lpd-errs:\
        :sd=/var/spool/lpd/%P:\
        :mx#0:\
        :sh:
```

Logging File
------------
Then create a log file:
```bash
touch /var/log/lpd-errs
```

Who Can Use This Printer
------------------------
To allow non-root user(s) to use the printer, add that user name to 
the `lp` group in `/etc/group`.

Edit the `/etc/group`:
```bash
vigr -g
```
The `vigr` command will use the editor that your `EDITOR` environment is set to
otherwise fallback to `nano`.

Scroll down to the row containing the `lp` entry.
```passwd
disk:x:6:
lp:x:7:
mail:x:8:
news:x:9:
```

Note: If more than one user are being added, separate them by a comma symbol.

And add name of user account at the end of `lp:x:7:` row:
```passwd
disk:x:6:
lp:x:7:johndoe,janedoe
mail:x:8:
news:x:9:
```

Exit editor and save.

Final Step
----------
Log out of the desktop or terminal account and re-login to make effective the
new `lp` group into the authorized user account(s).

Try it out by printing the file:

```bash
unix2dos < /etc/hosts | lp -d rlp
```
