title: Extracting Print Output from CUPS Queue
date: 2022-02-25 10:35
status: published
tags: CUPS
category: HOWTO
summary: Extracting Print Output from CUPS Queue
lang: en
private: False


To extract the PostScript output for a developer to analyze it, clone your print queue to a one which prints into a file:

```console
cupsctl FileDevice=yes
lpadmin -p test -E -v file:/tmp/printout \
      -P /etc/cups/ppd/<name of original queue>.ppd
```

and print into this queue as described above. The PostScript output is in /tmp/printout after the job has completed.


This option does not change anything if Poppler's pdftops is used as renderer.
