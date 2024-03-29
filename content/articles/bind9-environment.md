Title: ISC Bind9 Environment Names
Date: 2018-10-17 13:16
Modified: 2022-02-24 08:41
Status: published
Tags: Bind9, environment variables
Category: research
summary: Environment Name Used by ISC Bind9

Environment variables
=====================

`named` Bind9 environment variables
---------------------------

[jtable separator=","]
variable name , description , source
`KRB5_KTNAME`, Used to minimize memory leakage associated with KRB5 API calls , `gssapictx.c`
`PATH` , The sequence of path prefixes that certain functions and utilities apply in searching for an executable file known only by a filename. The prefixes are separated by a colon (:) When a non-zero-length prefix is applied to this filename; a slash is inserted between the prefix and the filename. A zero-length prefix is a legacy feature that indicates the current working directory. It appears as two adjacent colons (::); as an initial colon preceding the rest of the list; or as a trailing colon following the rest of the list. A portable application must use an actual pathname (such as .) to represent the current working directory in PATH. The list is searched from beginning to end; applying the filename to each prefix; until an executable file with the specified name and appropriate execution permissions is found. If the pathname being sought contains a slash; the search through the path prefixes will not be performed. If the pathname begins with a slash; the specified path is resolved (see pathname resolution ). If PATH is unset or is set to null; the path search is implementation-dependent.  <p>The path separator on Windows is a semicolon; not a colon; as in the Unix world. Setting the path has the effect of automatically locating; say; dig or nsupdate. However there is a Windows version of nslookup that will be found first. Using the BIND version of nslookup either requires a full path command such as C:\Program Files\ISC BIND 9\bin\nslookup.exe (or C:\Program Files (x86)\ISC BIND 9\bin\nslookup.exe for a 32-bit BIND install on a Windows 64 bit platform) when running it from the command line. Alternatively the preceding path directive can be placed first in the path list which in turn has the disadvantage that it will add an extra check for all other program loading operations that use normal Windows locations. , `pk11.c`
`LANG` , This variable determines the locale category for native language, local customs and coded character set in the absence of the `LC_ALL` and other `LC_*` (<code>LC_COLLATE</code>, <code>LC_CTYPE</code>, <code>LC_MESSAGES</code>, <code>LC_MONETARY</code>, <code>LC_NUMERIC</code>, <code>LC_TIME</code>) environment variables. This can be used by applications to determine the language to use for error messages and instructions, collating sequences, date formats, and so forth. Always use a value for LANG that is supported by the UNIX or Linux operating system you are using. To obtain the locale names for your UNIX or Linux system, enter the following command: locale -a.</p> <p>If you specify the LANG environment variable and also modify the regional settings then the LANG environment variable will override the regional setting. As specified by open systems standards, other environment variables override LANG for some or all locale categories. These variables include the following:</p> <p><code>   LC_COLLATE</code><br /> <code>   LC_CTYPE</code><br /> <code>   LC_MONETARY</code><br /> <code>   LC_NUMERIC</code><br /> <code>   LC_TIME</code><br /> <code>   LC_MESSAGES</code><br /> <code>   LC_ALL</code></p> <p>If any of the previous variables are set, you must remove their setting for the LANG variable to have full effect. Some values found on Linux platforms (via <code>locale</code> <code>-a</code>) are: C C.UTF-8 en_US en_US.iso88591 en_US.iso885915 en_US.utf8 POSIX ,
`LC_ALL` , This variable determines the values for all locale categories. The value of the LC_ALL environment variable has precedence over any of the other environment variables starting with LC_ (LC_COLLATE, LC_CTYPE, LC_MESSAGES, LC_MONETARY, LC_NUMERIC, LC_TIME) and the LANG environment variable. ,
`LC_CTYPE` , This variable determines the locale category for character handling functions, such as <code>tolower()</code>, <code>toupper()</code> and <code>isalpha()</code>. This environment variable determines the interpretation of sequences of bytes of text data as characters (for example, single- as opposed to multi-byte characters), the classification of characters (for example, alpha, digit, graph) and the behavior of character classes. Additional semantics of this variable, if any, are implementation-dependent. ,
`NET_ORDER` , Set the sorting order of multiple IP addresses being displayed. Valid values are &quot;<code>inet4</code>&quot; or &quot;<code>inet6</code>&quot;. ,
`PKCS11_PROVIDER` , "Declares the PKCS11 provider being used. Valid values are: &quot;<code>undefined</code>&quot;, &quot;<code>libsofthsm2</code>&quot;, &quot;<code>openssl</code>&quot;" ,
`TEMP` , A pathname of a directory made available for programs that need a place to create temporary files. ,
`TERM` , The terminal type for which output is to be prepared. This information is used by utilities and application programs wishing to exploit special capabilities specific to a terminal. The format and allowable values of this environment variable are unspecified. ,
`TZ` , Timezone information. The contents of the environment variable named `TZ` are used by the `ctime()`, <code>localtime()</code>, <code>strftime()</code> and <code>mktime()</code> functions, and by various utilities, to override the default timezone. The value of <code>TZ</code> has one of the two forms (spaces inserted for clarity):</p> <p><code>   :characters</code></p> <p>or:</p> <p><code>   std offset dst offset, rule</code></tt></p> <p>If <code>TZ</code> is of the first format (that is, if the first character is a colon), the characters following the colon are handled in an implementation-dependent manner. The expanded format (for all TZs whose value does not have a colon as the first character) is as follows:</p> <p><code>   stdoffset\[dst\[offset\]\[,start\[/time\],end\[/time\]\]\]</code> ,
`ZKT_CONFFILE` , "Specifies the name of the default global configuration files.</p> <p><code>/var/lib/named/dnssec.conf</code>: Built-in default global configuration file. The name of the default global config file is settable via the environment variable <code>ZKT_CONFFILE</code>. (For non-Debian platform, file is <code>/var/named/dnssec.conf</code>). Man page is dnssec.zkt(5). ,
[/jtable]

`dig` utility Bind9 environment variables
---------------------------

[jtable separator=","]
variable name , description , test source
`IDN_DISABLE` , If you’d like to turn off the IDN support for some reason, defines the `IDN_DISABLE` environment variable. The IDN support is disabled if the variable is set when dig runs. , `dighost.c`
[/jtable]

Test Bind9 environment variables
---------------------------

[jtable separator=","]
variable name , description , test source
`COMSPEC` , `COMSPEC` or `ComSpec` is one of the environment variables used in DOS, OS/2 and Windows, which normally points to the command line interpreter, which is by default `COMMAND.COM` in DOS or CMD.EXE in OS/2 and Windows NT. The variable name is written in all-uppercase under DOS and OS/2. Under Windows, which also supports lowercase environment variable names, the variable name is `COMSPEC` inside the DOS emulator NTVDM and for any DOS programs, and `ComSpec` under `CMD.EXE`.<br /> The variable's contents can be displayed by typing `SET` or `ECHO %COMSPEC%` at the command prompt.<br /> The environment variable by default points to the full path of the command line interpreter. It can also be made by a different company or be a different version. , `libtool.c`
`CONTROLPORT` , Used with customized rndc.conf for shutdown testing , `shutdown/conftest.c`
`EXTRA_PORT1` , Used for statistics channel testing , `statschannel/conftest.c`
`HAVEJSONSTATS` , Used with produce JSON-formatted files for RPZ testing , `rpzextra/conftest.c`
`HAVEXMLSTATS` , Used with produce XML-formatted files for statistics-channel testing , `statschannel/conftest.c`
`ISC_TASK_WORKERS` , Used during unit testing of Bind9. This is not used during production. ,
`ISC_TASKS_MIN` , Used during unit testing of Bind9. This is not used during production. ,
`NAMED` , Used to test shutdown of named daemon , `shutdown/tests-shutdown.c`
`PORT` , Used with customized rndc.conf for RPZ, statistics and shutdown testing , `statschannel/conftest.c`, `shutdown/conftest.c`, `rpzextra/conftest.c`
`RNDC` , Used with customized rndc.conf for shutdown testing , `shutdown/tests-shutdown.c`
`SOURCE_DATE_EPOCH` , Used to generate C include files for library packages , `dns/gen.c`
[/jtable]

References
==========

- [UNIX Specification](http://pubs.opengroup.org/onlinepubs/7908799/xbd/envvar.html)

