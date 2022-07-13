title: Debugging `jsshell`
date: 2022-07-04 07:36
status: published
tags: debugging, JavaScript, jsshell
category: research
lang: en
private: False

This article details how to perfom debugging of the `jsshell` in Mozilla Unified repository.

# Setting Up `jsshell` Debug

With the `js` binary built (as described in [Firefox JSSHELL]({filename}firefox-jsshell.md), we can then start debugging.

# Preparing Work Directory

```bash
cd firefox
mkdir test
cd test
DISTDIR=../repo/mozilla-unified/obj-debug-x86_64-pc-linux-gnu/dist/bin/js
ln -s $DISTDIR/js .
ln -s $DISTDIR/js-gdb.py .
ln -s $DISTDIR/.gdbinit  .
ln -s $DISTDIR/.gdbinit.loader  .
```
Create a JavaScript simple assignment of 'Hello World':
```javascript
// the simple string assignment program
//
// This would work with any of Firefox browser, xpconnect or jsshell
//
my_string = 'Hello World';
console.log(my_string);
```

and call that source file `string-assignment-simple.js`.

# Preparing GDB initrc file

Add the following GDB line to `${HOME}/.gdbinit`:

```gdb
set auto-load safe-path /
```

And also update the local `./.gdbinit` file to append the following:

```gdb
set auto-load safe-path /
set args string-assignment-string.js
```

# Starting GDB

Then start the GDB debugger against the `jsshell` executable that is reading the JavaScript `string-assignment-string.js` source file.

```console
$ gdb -q ./js
```

# Jumping to the Bytecode Compiler

```gdb
# first stop 
(gdb) break RunFile
# after reading the source file
(gdb) break js::frontend::CompileGlobalScript
# start of compiling CompileGlobalScriptToStencilAndMaybeInstantiate
(gdb) break js::frontend::InstantiateStencils
# start compiling JavaScript bytecode
(gdb) break js::frontend::FireOnNewScript
# start executing compiled JavaScript bytecode
(gdb) break JS_ExecuteScript
(gdb) break ExecuteScript
(gdb) break js::Execute
(gdb) break ExecuteKernel
(gdb) break js::RunScript
(gdb) break Interpret
(gdb) break JSScript::immutableScriptData
```

Then in `Interpret` shows the following intermediate representation of JavaScript bytecodes:

[jtable]
Mnemonic, description
`JSOp::BindGName`,
`JSOp::String`,
`JSOp::SetGName`,

[/jtable]

You can also add a breakpoint to the program counter incrementer in the bytecode interpreter, the following line is in the `mozilla-unified/js/src/vm/Interpreter.cpp:3063` source file:

```c
      REGS.sp[-2] = REGS.sp[-1];
```

But it is harder to insert a breakpoint at the main loop of the JS inteprefer (as denoted by ``.

Some IR code can be had by using the `--dump-bytecode` or `-D` CLI option:

```console
$ ../repo/mozilla-unified/obj-debug-x86_64-pc-linux-gnu/dist/bin/js \
   --no-jit-backend \
   --no-threads \
   --non-writable-jitcode \
   --blinterp \
   --no-baseline \
   --no-ion \
   -O -D -b \
   --code-coverage \
   string-assignment-simple.js 
Hello World
runtime = 0.852 ms
--- SCRIPT string-assignment-simple.js:1 ---
00000:   6  BindGName "my_string"
                  {"interp": 1}
00005:   6  String "Hello World"
                  {}
00010:   6  SetGName "my_string"
                  {}
00015:   6  Pop
                  {}
00016:   7  GetGName "console"
                  {}
00021:   7  Dup
                  {}
00022:   7  GetProp "log"
                  {}
00027:   7  Swap
                  {}
00028:   7  GetGName "my_string"
                  {}
00033:   7  CallIgnoresRv 1
                  {}
00036:   7  Pop
                  {}
00037:   9  RetRval
                  {}
--- END SCRIPT string-assignment-simple.js:1 ---
```

