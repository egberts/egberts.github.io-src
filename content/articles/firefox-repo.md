title: Mozilla Repository
date: 2022-06-23 07:16
status: published
tags: Mozilla, Firefox, Mach, repository
category: HOWTO
lang: en
private: False


Project: Firefox
Version: 103
Date: 2022-06-23

# Setup

To setup Firefox on Linux:

```bash
curl https://hg.mozilla.org/mozilla-central/raw-file/default/python/mozboot/bin/bootstrap.py -O
python3 bootstrap.py
```

# Build

To build & run

Once the System is bootstrapped, run:

```console
$ cd mozilla-unified
$ ./mach build
```

# Run

To run it:

```console
$ ./mach run
```

# References:

* [Firefox contributors quick reference](https://firefox-source-docs.mozilla.org/contributing/contribution_quickref.html)
