title: Debugging Detection & Prevention
date: 2018-11-14T12:00
status: published
category: research
research tags: debugger, malware
summary: Detection and Prevention of Debuggers

Debugger Detection/Prevention

* [Ferrie](http://anti-reversing.com/Downloads/Anti-Reversing/The_Ultimate_Anti-Reversing_Reference.pdf), some source in [LordNoteworthy@github Anti_Debug](https://github.com/LordNoteworthy/al-khaser/tree/master/al-khaser/Anti%20Debug). Most common/interesting ones:
    * `IsDebuggerPresent()`, `CheckRemoteDebuggerPresent()`, etc. (quite silly, mostly as a kinda-decoy)
        * OS calls are not 100% obfuscatable =\>; using them (unless they’re actually inlines or macros) is a Bad Idea™ (Bad Example: [zer0fl4g@github](https://github.com/zer0fl4g/DebugDetector). IF using them – obfuscate system calls and literals (such as obfuscating “OllyDbg” for `FindWindow()`, and obfuscating “`FindWindow`” for `GetProcAddress()`); more on obfuscating system calls below.
    * Not-so-obvious system calls, such as `OpenProcess(“csrss.exe”)`, `OutputDebugString()`, `UnhandledExceptionFilter()` 
    * `FindWindow()` (silly, but…)
    * Memory reads. `NtGlobalFlag`, heap flags, `KdDebuggerEnabled`, `GetLastError()` (`cmp fs:\[ebp+34h\], ebp, cmp gs:\[rbp+68h\], ebp`), TODO – anything else?  Reading from RAM without function call(!). 
        * DON’T use directly for comparisons; instead – use as a part of data obfuscation (in particular, will look similar to ‘global read of known value’ used to prevent optimizing out). Effective partial compares when using for data obfuscation (using &mask1 in one place, |mask2 in another place).  
        * More devious: use the value to generate decryption key, then try to decrypt several pieces of code (with one decrypted by “correct” key, and another by “being-debugged” key, other combinations of “being-debugged” flags also can be accounted for). Then use this code to communicate to the server – which now can distinguish clients which are being debugged (gotcha!). Hare wondering if you are crazy:“
        * Even more devious: use the value to generate encryption key, which is used to encrypt a well-defined constant, which is sent to the server – which then can try different keys to decrypt (gotcha!).
        * Even more devious: use the value to generate encryption key, which is used to encrypt a well-defined constant, which is sent to the server – which then can try different keys to decrypt (gotcha!)
    * “self-debug” (actually – debug a copy of the process). Only one ring 3 debugger allowed at least in Windows.
    * Hiding thread from debugger: NtSetInformationThread, NtCreateThreadEx (reportedly used by Steam at least at some point)
    * `MOV SS`
    * `INT 2D`
    * “check within TLS callback” trick
    * NB: using Zw\* counterparts \[TODO – elaborate\]
    * Messing with debuggers: 
        * BlockInput; Not really detection, but… 
        * `REP \<some-op\>`
    * \[Kulchytskyy\] Most interesting techniques (beyond \[Ferrie\]) 
        * NtCreateThreadEx to hide threads 
        * Asm to set SEH handlers (32-bit only); on table-based SEH in x64 Windows – see \[NTInsider\]
        * `KiUserExceptionDispatcher`
    * \[Falliere\]. Techniques going beyond previous refs: 
        * `PUSH SS/POP SS` (Actually, it is described in \[FERRIE\], but imo explanation here is better) 
        * ICE breakpoint (0xF1); not to be confused with SoftICE.
        * Scanning for INT 3 (0xCC). False positives. Also should scan for 0xFA \[Falliere\] and probably others. Checksums are generally preferred.
    * \[OpenRCE\] Techniques going beyond previous refs: 
        * `LOCK CMPXCHG8B` as an invalid instruction to raise SEH
        *  Lots of debugger-specific trickery
    * \[Tully\]. Techniques going beyond previous refs: 
        * Removing PE header
        *  messing with debuggers:
            * `OutputDebugString` Exploit for OllyDbg (TODO: is it still up-to-date?)
    * SoftICE detection (doesn’t make much sense now, esp. if your program is 64-bit, but some ideas might be applicable to other debuggers): lots of discussion in \[Crackproof your software\]

