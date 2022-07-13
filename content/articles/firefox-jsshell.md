title: Building `jsshell`
date: 2022-06-23 -7:14
status: published
tags: Firefox, Mozilla, Mach, JavaScript
category: HOWTO
lang: en
private: False


After Mercuralizing the Mozilla Firefox repository, the next focus
is to create a MOZCONFIG.  MOZCONFIG is a term and also an
environment variable that holds various build settings for Mozilla
projects (such as Firefox).

# `MOZCONFIG`

we make use of a $HOME/mozconfigs directory to hold our generic but
personalized build settings.

    mkdir $HOME/mozconfigs

Then we created a debug-variant of MOZCONFIG

```console
#
# File: debug
# Path: $HOME/mozconfigs
# Title: Mozilla Mach build config file
#
#
#To activate a particular MOZCONFIG, set the environment variable:
#
#    export MOZCONFIG=$HOME/mozconfigs/debug



# Build only the JS shell
ac_add_options --enable-application=js

# Enable the debugging tools: Assertions, debug only code etc.
ac_add_options --enable-debug

# Enable optimizations as well so that the test suite runs much faster. If
# you are having trouble using a debugger, you should disable optimization.
ac_add_options --enable-optimize

# Use a dedicated objdir for SpiderMonkey debug builds to avoid
# conflicting with Firefox build with default configuration.
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-debug-@CONFIG_GUESS@
```

and an optimized-variant of MOZCONFIG for our personalized use:

```console
#
# File: optimized
# Path: $HOME/mozconfigs
# Title: Mozilla Mach build config file for Optimized runs
#
#
#To activate a particular MOZCONFIG, set the environment variable:
#
#    export MOZCONFIG=$HOME/mozconfigs/optimized


# Build only the JS shell
ac_add_options --enable-application=js

# Enable optimization for speed
ac_add_options --enable-optimize

# Disable debug checks to better match a release build of Firefox.
ac_add_options --disable-debug

# Use a separate objdir for optimized builds to allow easy
# switching between optimized and debug builds while developing.
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-opt-@CONFIG_GUESS@
```

# Build Area

Then head over to our project area:

```bash
cd  ~/work/firefox/repo/mozilla-unified
```

and start the build process:

```bash
./mach build
```

# Testing

Once built, you can then use mach to run the jit-tests:

$ ./mach jit-test

Similarly you can use also run jstests. These include a local, intermittently updated, copy of all test262 tests.

$ ./mach jstests

# Using JSSHELL

To start using `jsshell`, execute:

```console
./mach run
```

# `jsshell` Binary

The location of the newly-built `jsshell` binary file is under:

```console
$ cd $HOME/work/firefox/repo/mozilla-unified/obj-debug-x86_64-pc-linux-gnu/dist/bin/js'

$ file ./js
/home/test/work/firefox/repo/mozilla-unified/obj-debug-x86_64-pc-linux-gnu/dist/bin/js: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=e00e66bdefeae80e7f027e8c9898d1c1d51f7a77, with debug_info, not stripped
$
$ ldd ./js
	linux-vdso.so.1 (0x00007ffd7f9cb000)
	libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007efc41802000)
	libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007efc3e8bc000)
	libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007efc417fc000)
	libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007efc417df000)
	libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007efc3e6ef000)
	libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007efc417c5000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007efc3e516000)
	/lib64/ld-linux-x86-64.so.2 (0x00007efc41845000)

```

# Hello, World! in `jsshell`

With a quick "Hello, World!" source file:
```javascript
// the hello world program
console.log('Hello World');
```

stored into a `hello-world.js` file, we can then execute:

```console
$ ./js hello-world.js
```


# Debugging `jsshell`

There is a `js-gdb.py` Python script (also in the same directory as `jsshell`.

But that script requires the Python `gdb` library, which Debian does not provie.
