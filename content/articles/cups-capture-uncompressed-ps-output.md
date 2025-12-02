title: Capturing Uncompressed PostScript Output through CUPS
date: 2022-02-25 10:38
status: published
tags: CUPS, printing, PostScript
category: HOWTO
summary: Capturing uncompressed PostScript output through CUPS
lang: en
private: False

POSTSCRIPT PRINTING DEBUG MODE

Sometimes a PostScript printer's interpreter errors, crashes, or
somehow else misbehaves on Ghostscript's output. To find
workarounds (currently we have already workarounds for Brother and
Kyocera) it is much easier to work with uncompressed PostScript.

To get uncompressed PostScript as output, send a job with the
`psdebug` option, with commands like the following:

```bash
lpr -P <printer> -o psdebug <file>
lp -d <printer> -o psdebug <file>
```

If you want to send your job out of a desktop application, run

```bash
lpoptions -p <printer> -o psdebug
```

to make `psdebug` a personal default setting for you.

To extract the PostScript output for a developer to analyze it,
clone your print queue to a one which prints into a file:

```bash
cupsctl FileDevice=yes
lpadmin -p test -E -v file:/tmp/printout \
      -P /etc/cups/ppd/<name of original queue>.ppd
```

and print into this queue as described above. The PostScript
output is in /tmp/printout after the job has completed.

This option does not change anything if Poppler's pdftops is used
as renderer.
