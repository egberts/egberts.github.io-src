title: Compiler Predefined Macros
date: 2024-06-19 11:00
status: published
tags: compiler, gcc, cc
category: HOWTO
summary: How to list compiler predefined macros for most OS platforms.
lang: en
private: False

All C/C++ compilers predefined macros indicating the target processor, operating system, language features, compiler name and version, and more. Cross-platform code can use `#if`/`#endif` to wrap OS-specific `#include`s (such as `<Windows.h>` vs. `<unistd.h>`), compiler-specific code (such as inline assembly), or processor-specific optimizations (such as SSE instructions on x86). Macro names are not standardized and nor are methods to get the compiler to list them. This article surveys common desktop and server application compilers and shows how to list their predefined macros.



Command-line options
=====
Most compilers have command-line options to list predefined macros:

[jtable caption="Compiler Predefined Macros" separator="," th=1 ai="1"]
Command lines Compiler,C macros,C++ macros
Clang/LLVM, `clang -dM -E -x c /dev/null`, `clang++ -dM -E -x c++ /dev/null`
GNU GCC/G++,`gcc -dM -E -x c /dev/null`,`g++ -dM -E -x c++ /dev/null`
Hewlett-Packard C/aC++,`cc -dM -E -x c /dev/null`,`aCC -dM -E -x c++ /dev/null`
IBM XL C/C++,`xlc -qshowmacros -E /dev/null`,`xlc++ -qshowmacros -E /dev/null`
Intel ICC/ICPC,`icc -dM -E -x c /dev/null`, `icpc -dM -E -x c++ /dev/null`
Microsoft Visual Studio, (none), (none)
Oracle Solaris Studio, `cc -xdumpmacros -E /dev/null`, `CC -xdumpmacros -E /dev/null`
Portland Group PGCC/PGCPP,`pgcc  -dM -E`, (none)
[/jtable]

Notes:

* The macros listed by the compiler vary with additional language or platform options. For instance, adding `-m32` or `-m64` to GCC dumps macros for 32-bit or 64-bit builds, respectively. Adding "`-mwin32`" to GCC under Cygwin builds Windows applications and dumps macros appropriate for that platform. Without any additional arguments, the above commands dump the compiler's defaults.

Clang, GNU, HP, and Intel compilers:
-----

* `-dM` dumps a list of macros.
* `-E` prints results to stdout instead of a file.
* `-x c` and `-x c++` select the programming language when using a file without a filename extension, such as /dev/null. If you instead compile "`dummy.c`" and "`dummy.cpp`" files, these options aren't needed.

IBM compilers:
-----

* `-qshowmacros` dumps a list of macros.
* `-E` prints results to stdout instead of a file.


Oracle compilers:
-----
* `-xdumpmacros` dumps a list of macros.
* `-E` prints results to stdout instead of a file.


Portland Group compilers:
-----
`-dM` dumps a list of macros. However, it only shows C language macros, even when used on the C++ compiler. There is currently no way to list C++ language macros.

Microsoft compilers:
-----
Visual Studio can be run from the command line, but it doesn't have an option to dump a list of macros. Instead, Microsoft provides detailed on-line documentation.

IDEs
----

Most IDEs (such as JetBrain, (Eclipse)[http://www.eclipse.org/], (Netbeans)[http://netbeans.org/], and (Xcode)[https://developer.apple.com/xcode/]) provide GUI control panels to set command-line options for the underlying compilers. Please check your IDE's manual.

Source code
=====
When compilers support multiple operating systems and target processors, every combination can produce a different set of predefined macros. Documenting every OS and processor combination's macros is impractical. Experimenting with different command line options will yield macro lists for each OS and processor, but this is tedious. A slightly less tedious method is to read the source code, if available.

Clang and LLVM source code is available for free download from (llvm.org)[http://llvm.org/]. Once downloaded, OS and processor macros are defined in `llvm/tools/clang/lib/Basic/Targets.cpp`.

GCC and G++ source code is available for free download from (gnu.org)[http://gnu.org/]. Once downloaded, OS and processor macros are defined in `gcc/config/*`.

Strings in the binary
=====

If nothing else works, the (`strings`)[http://linux.die.net/man/1/strings] command for UNIX-style OSes (AIX, BSD, HP-UX, Linux, OSX, Solaris) or POSIX or GNU environments on Windows (Cygwin, MinGW) scans a file looking for consecutive runs of printable characters. For application binaries, character runs are mostly literal strings embedded in the binary. For a compiler, these strings include error messages, help messages, command-line options, and... predefined macro names.

For example, run strings on GCC on Linux:

```bash
strings /usr/bin/gcc > gcc.txt
```

This produces a 12,000+ line text file with all sorts of strings for help messages and command-line options. But it does not include predefined macro names. `/usr/bin/gcc` is a front-end to the compiler and invokes `/usr/libexec/gcc/cc1` to do the language parsing. It's that program that defines macro names.

```bash
strings /usr/libexec/gcc/cc1 > cc1.txt
```

This produces a 51,000+ line text file! Much of it is garbage, but buried within it are predefined macros, such as:

```cpp
__3dNOW_A__
__3dNOW__
__BASE_FILE__
__CHAR_BIT__
__CHAR_UNSIGNED__
__DATE__
__DECIMAL_DIG__
__DEPRECATED
__ELF__
__EXCEPTIONS
__FAST_MATH__
__FILE__
__FLT_EVAL_METHOD__
__FLT_RADIX__
__FUNCTION__
__GNUC_GNU_INLINE__
__GNUC_MINOR__
__GNUC_PATCHLEVEL__
__GNUC_RH_RELEASE__
__GNUC__
__GNUG__
__GXX_ABI_VERSION
__INCLUDE_LEVEL__
__INTMAX_MAX__
__INTMAX_TYPE__
__INT_MAX__
__LINE__
__LONG_LONG_MAX__
__LONG_MAX__
__LP64__
__MMX__
```

And so forth. Unfortunately, these are just potential predefined macros. A subset of them are defined depending upon the OS, processor, and command-line options. Using strings to find macro names is a crude last resort when compiler help messages, documentation, and source code are all unavailable or unhelpful.


References
-----
* Nadeau Software (archived) - http://web.archive.org/web/20191011040139/http://nadeausoftware.com/articles/2011/12/c_c_tip_how_list_compiler_predefined_macros
