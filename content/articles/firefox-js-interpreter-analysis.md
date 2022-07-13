title: JavaScript Interperter Analysis, Mozilla Unified
date: 2022-07-04 09:14
status: published
tags: JavaScript, Firefox
category: research
lang: en
private: False

This article details the analysis of available datum associated with each bytecode of the JavaScript interpreter in Mozilla Unified repo (that is also being used in Firefox).

# Datum

The focus of the bytecode interpreter is the loop (`INTERPRETER_LOOP()` C macro).

Available structures are given in `Interpreter()` function:

- Run State machine
- JavaScript context

# `RunState` Datum

and for `RunState`, we have the following:
```console
(gdb)  p state
$6 = (js::RunState &) @0x7fffffffdaf8: {kind_ = js::RunState::Execute, 
  script_ = 0x208b86a060}
```

A simple two variable structure comprising of:

* `kind_`
* `script_`

The `state->kind_` is a simple 2-state machine value containing an enumeration of  `js::RunState::Execute`.  Both are defined by `MOZ_RAII` class in `js/src/vm/Interpreter.h`.  As a reference, the other state is `js::RunState::Invoke`.

Unfortunately, `state->script_` is untyped in `gdb` session (thanks to C++ `private`).  But in `Interpreter.h`, this variable is a `JSScript` structure as defined by `JSScript : public js::BaseScript` class in `js/src/vm/JSScript.h` source file.



# JavaScript Context Datum


General breakdown of the JSContext are:

* options
* errors
* status
* memory
    * `JS::RootingContext`
    * garbage collector
    * Nursery
    * WatchTower
    * memory usage security
* compiler
    * JavaScript Interpreter
    * JavaScript Intermediate Representation bytecoding
    * JavaScript Baseline Interpreter (Inline Cache)
    * JavaScript Baseline Compiler
    * WarpMonkey
    * Web Assembly (wasm)
* process
    * threads
    * async
    * JS Promise
    * Job Queue
    * Interrupt handling
* runtime
    * `jitActivation`
    * ION-Monkey (optimized JS IR reordering)
    * Futex (fx)
    * GDB support

# Options

```
options_ = {
    <js::ProtectedData<js::CheckContextLocal, JS::ContextOptions>> = {
        value = {
            asmJS_ = true, 
            wasm_ = true, 
            wasmForTrustedPrinciples_ = true, 
            wasmVerbose_ = false, 
            wasmBaseline_ = true, 
            wasmIon_ = true, 
            wasmCranelift_ = false, 
            wasmSimd_ = true, 
            wasmExtendedConst_ = false, 
            wasmExceptions_ = true, 
            wasmFunctionReferences_ = false, 
            wasmGc_ = false, 
            wasmRelaxedSimd_ = true, 
            wasmMemory64_ = true, 
            wasmMozIntGemm_ = false, 
            wasmTestSerialization_ = false, 
            wasmSimdWormhole_ = false, 
            testWasmAwaitTier2_ = false, 
            throwOnAsmJSValidationFailure_ = false, 
            disableIon_ = false, 
            disableEvalSecurityChecks_ = false, 
            asyncStack_ = true, 
            asyncStackCaptureDebuggeeOnly_ = false, 
            sourcePragmas_ = true, 
            throwOnDebuggeeWouldRun_ = true, 
            dumpStackOnDebuggeeWouldRun_ = false, 
            strictMode_ = false, 
            fuzzing_ = false, 
            arrayGrouping_ = false, 
            importAssertions_ = false},
         check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 
```


# Errors and Status

```
errors_ = 0xe4e4e4e4e4e4e4e4, 

status = {
    <js::ProtectedData<js::CheckContextLocal, JS::ExceptionStatus>> = {
        value = JS::ExceptionStatus::None, 
        check = {
            cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 
```


# Memory 


# `JS::RootingContext` Memory

```
<JS::RootingContext> = {
    stackRoots_ = {
        static kSize = 15, 
        mArray = {
            mArr = {0x0, 0x0, 0x7fffffffd750, 0x7fffffffd7c8, 
                    0x7fffffffd768, 0x0, 0x7fffffffd798, 0x0, 0x0, 0x0, 
                    0x0, 0x0, 0x7fffffffd780, 0x7fffffffd810, 0x7fffffffd898}, 
            static Length = 15}}, 
    autoGCRooters_ = {
        static kSize = 3, 
        mArray = {
            mArr = {0x0, 0x0, 0x0}, 
            static Length = 3}}, 
    geckoProfiler_ = {
        profilingStack_ = 0x0, 
        profilingStackIfEnabled_ = 0x0}, 
    realm_ = 0x7ffff770b800, 
    zone_ = 0x7ffff774c200, 
    nativeStackLimit = {
        140737486251873, 
        140737486251873, 
        140737486251873}},
```


## `runtime` Memory

```
runtime_ = {
    <js::ProtectedData<js::CheckUnprotected, JSRuntime*>> = {
        value = 0x7ffff7718000, 
        check = {<No data fields>}},
     <No data fields>}, 
```


# JavaScript compilation

## JavaScript Just-In-Time

```
// JavaScript Compiler
// Just-In-Time 

jitActivation = {
    <js::ProtectedData<js::CheckContextLocal, 
    js::jit::JitActivation*>> = {
        value = 0x0, 
        check = {
            cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

jitStackLimit = {
    <mozilla::detail::AtomicBaseIncDec<unsigned long, mozilla::Relaxed>> = {
        <mozilla::detail::AtomicBase<unsigned long, mozilla::Relaxed>> = {
            mValue = {
                <std::__atomic_base<unsigned long>> = {
                    static _S_alignment = 8, 
                    _M_i = 140737486251873}, 
                static is_always_lock_free = true}}, 
        <No data fields>}, 
    <No data fields>}, 

jitStackLimitNoInterrupt = {
    <js::ProtectedData<js::CheckContextLocal, unsigned long>> = {
        value = 140737486251873, 
        check = {
            cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 
```


## Web Assembly (WASM)

```
// Web-Assembly

wasm_ = {
    triedToInstallSignalHandlers = true, 
    haveSignalHandlers = true}, 
```

## Process-related

```
kind_ = {
    value = js::ContextKind::MainThread, check = {<No data fields>}, 
    nwrites = 1}, 

currentThread_ = {
    platformData_ = {0x7ffff7a58c40, 0xaaaaaaaaaaaaaa01}}, 

isExecuting_ = {
    <mozilla::detail::AtomicBase<unsigned int, 
    mozilla::ReleaseAcquire>> = {
        mValue = {
            <std::__atomic_base<unsigned int>> = {
                static _S_alignment = 4, _M_i = 1}, 
            static is_always_lock_free = true}}, 
    <No data fields>}, 
```


## Promise - Process Handling

```
promiseRejectionTrackerCallback = {
    <js::ProtectedData<js::CheckContextLocal, void (*)(JSContext*, bool, JS::Handle<JSObject*>, JS::PromiseRejectionHandlingState, void*)>> = {
        value = 0x555557184ee0 <ForwardingPromiseRejectionTrackerCallback(JSContext*, bool, JS::Handle<JSObject*>, JS::PromiseRejectionHandlingState, void*)>, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

promiseRejectionTrackerCallbackData = {
    <js::ProtectedData<js::CheckContextLocal, void*>> = {
        value = 0x0, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 
```


## Async - Process Handling

```
asyncCauseForNewActivations = {
    <js::ProtectedData<js::CheckContextLocal, char const*>> = {
        value = 0x0, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

asyncCallIsExplicit = {
    <js::ProtectedData<js::CheckContextLocal, bool>> = {
        value = false, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

asyncStackForNewActivations_ = {
    <js::ProtectedData<js::CheckContextLocal, JS::PersistentRooted<js::SavedFrame*> >> = {
        value = {
            <js::TypedRootedGCThingBase<js::PersistentRootedBase, js::SavedFrame*>> = {
                <js::PersistentRootedBase> = {
                    <mozilla::LinkedListElement<js::PersistentRootedBase>> = {
                        mNext = 0x7ffff7718400, 
                        mPrev = 0x7ffff7735580, 
                        mIsSentinel = false}, 
                    <No data fields>}, 
                <No data fields>}, 
            <js::RootedOperations<js::SavedFrame*, JS::PersistentRooted<js::SavedFrame*> >> = {
                <js::MutableWrappedPtrOperations<js::SavedFrame*, JS::PersistentRooted<js::SavedFrame*> >> = {
                    <js::WrappedPtrOperations<js::SavedFrame*, JS::PersistentRooted<js::SavedFrame*>, void>> = {<No data fields>}, 
                    <No data fields>}, 
                <No data fields>}, 
            ptr = 0x0}, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 
```


## Job Queue - Process Handling

```
jobQueue = {
    <js::ProtectedData<js::CheckContextLocal, JS::JobQueue*>> = {
        value = 0x7ffff7737c00, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 
internalJobQueue = {
    <js::ProtectedData<js::CheckContextLocal, mozilla::UniquePtr<js::InternalJobQueue, JS::DeletePolicy<js::InternalJobQueue> > >> = {
        value = [(js::InternalJobQueue *) 0x7ffff7737c00], 
        check = {
            cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

canSkipEnqueuingJobs = {
    <js::ProtectedData<js::CheckContextLocal, bool>> = {
        value = false, 
        check = {
            cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 
```


## Interupts - Process Handling

```
interruptCallbacks_ = {
    <js::ProtectedData<js::CheckContextLocal, mozilla::Vector<bool (*)(JSContext*), 2ul, js::SystemAllocPolicy> >> = {
        value = {
            <js::SystemAllocPolicy> = {
                <js::AllocPolicyBase> = {<No data fields>}, 
                <No data fields>}, 
            static kElemIsPod = true, 
            static kMaxInlineBytes = 999, 
            static kInlineCapacity = 2, 
            mBegin = 0x7ffff772d7d0, 
            mLength = 1, 
            mTail = {<mozilla::Vector<bool (*)(JSContext*), 2ul, js::SystemAllocPolicy>::CapacityAndReserved> = {mCapacity = 2, mReserved = 1}, mBytes = "\320C\030WUU\000\000\344\344\344\344\344\344\344", <incomplete sequence \344>}, 
            mEntered = false, 
            static sMaxInlineStorage = 2}, 
        check = {cx_ = 0x7ffff772cc00}},
    <No data fields>}, 

interruptCallbackDisabled = {
    <js::ProtectedData<js::CheckContextLocal, bool>> = {
        value = false, check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

interruptBits_ = {
    <mozilla::detail::AtomicBaseIncDec<unsigned int, mozilla::Relaxed>> = {
        <mozilla::detail::AtomicBase<unsigned int, mozilla::Relaxed>> = {
            mValue = {
                <std::__atomic_base<unsigned int>> = {
                    static _S_alignment = 4, 
                    _M_i = 0}, 
                static is_always_lock_free = true}}, 
        <No data fields>}, 
    <No data fields>}, 

```


## Futex - Process Handling

```
fx = {
    cond_ = 0x7ffff77321c0, 
    state_ = js::FutexThread::Idle, 
    static lock_ = {
        <mozilla::detail::AtomicBaseIncDec<js::Mutex*, mozilla::SequentiallyConsistent>> = {
            <mozilla::detail::AtomicBase<js::Mutex*, mozilla::SequentiallyConsistent>> = {
                mValue = {
                    _M_b = {_M_p = 0x7ffff7706380}, 
                    static is_always_lock_free = <optimized out>}}, 
            <No data fields>}, 
        <No data fields>}, 
    canWait_ = {
        <js::ProtectedData<js::CheckThreadLocal, bool>> = {
            value = true, 
            check = {
                id = {
                    platformData_ = {0x7ffff7a58c40, 0xaaaaaaaaaaaaaa01}}}}, 
        <No data fields>}}, 
```

# Memory


## Nursery - Memory

```
noNurseryAllocationCheck = {
    <js::ProtectedData<js::CheckContextLocal, unsigned long>> = {
        value = 0, check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

nurserySuppressions_ = {
    <js::ProtectedData<js::CheckContextLocal, unsigned long>> = {
        value = 0, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 
```


## Malloc Replacement Support

```
<js::MallocProvider<JSContext>> = {<No data fields>}, 
```


## Memory Handling

```
freeLists_ = {
    <js::ProtectedData<js::CheckContextLocal, js::gc::FreeLists*>> = {
        value = 0x7ffff774c498, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

allocsThisZoneSinceMinorGC_ = 2, 

freeUnusedMemory = {
    <mozilla::detail::AtomicBase<unsigned int, mozilla::ReleaseAcquire>> = {
        mValue = {
            <std::__atomic_base<unsigned int>> = {
                static _S_alignment = 4, _M_i = 0}, 
                static is_always_lock_free = true}}, 
    <No data fields>}, 

nativeStackBase_ = {
    <mozilla::detail::MaybeStorage<unsigned long, true>> = {
        <mozilla::detail::MaybeStorageBase<unsigned long, true>> = {
            mStorage = {val = 140737488349024, dummy = 96 '`'}}, 
        mIsSome = 1 '\001'}, 
    <mozilla::detail::Maybe_CopyMove_Enabler<unsigned long, true, true, true>> = {
        <No data fields>}, 
    <No data fields>}, 

frontendCollectionPool_ = {
    <js::ProtectedData<js::CheckContextLocal, 
    js::frontend::NameCollectionPool>> = {
        value = {
        mapPool_ = {
            <js::frontend::CollectionPool<js::frontend::RecyclableNameMap<unsigned int>, 
            js::frontend::InlineTablePool<js::frontend::RecyclableNameMap<unsigned int> > >> = {
                all_ = {
                    <js::SystemAllocPolicy> = {
                        <js::AllocPolicyBase> = {<No data fields>}, 
                        <No data fields>}, 
                    static kElemIsPod = true, 
                    static kMaxInlineBytes = 999, 
                    static kInlineCapacity = 32, 
                    mBegin = 0x7ffff772ce90, 
                    mLength = 18, 
                    mTail = {
                        <mozilla::Vector<void*, 32ul, js::SystemAllocPolicy>::CapacityAndReserved> = {
                            mCapacity = 32, mReserved = 18}, 
                        mBytes = "\300\003u\367\377\177\000\000\200\005u\367\377\177\000\000@\au\367\377\177\000\000\000\tu\367\377\177\000\000\300\nu\367\377\177\000\000\200\fu\367\377\177\000\000@\016u\367\377\177\000\000@\340\177\367\377\177\000\000\300\343\177\367\377\177\000\000\200\345\177\367\377\177\000\000@\347\177\367\377\177\000\000\000\351\177\367\377\177\000\000\300\352\177\367\377\177\000\000\200\354\177\367\377\177\000\000@\356\177\367\377\177\000\000@\000|\367\377\177\000\000\000\002|\367\377\177\000\000\300\003|\367\377\177\000\000", '\344' <repeats 111 times>...}, 
                    mEntered = false, 
                    static sMaxInlineStorage = 32}, 
                recyclable_ = {
                    <js::SystemAllocPolicy> = {
                        <js::AllocPolicyBase> = {<No data fields>}, 
                        <No data fields>}, 
                    static kElemIsPod = true, 
                    static kMaxInlineBytes = 999, 
                    static kInlineCapacity = 32, 
                    mBegin = 0x7ffff772cfb8, 
                    mLength = 18, 

                    mTail = {<mozilla::Vector<void*, 32ul, js::SystemAllocPolicy>::CapacityAndReserved> = {mCapacity = 32, mReserved = 18}, mBytes = "\300\003|\367\377\177\000\000@\000|\367\377\177\000\000\000\002|\367\377\177\000\000@\347\177\367\377\177\000\000@\356\177\367\377\177\000\000\300\352\177\367\377\177\000\000\000\351\177\367\377\177\000\000\200\354\177\367\377\177\000\000@\340\177\367\377\177\000\000\300\343\177\367\377\177\000\000\300\nu\367\377\177\000\000@\016u\367\377\177\000\000\200\fu\367\377\177\000\000\000\tu\367\377\177\000\000\200\345\177\367\377\177\000\000@\au\367\377\177\000\000\200\005u\367\377\177\000\000\300\003u\367\377\177\000\000", '\344' <repeats 111 times>...}, 
                    mEntered = false, static sMaxInlineStorage = 32}},
            <No data fields>}, 
        atomVectorPool_ = {
            <js::frontend::CollectionPool<mozilla::Vector<js::frontend::TrivialTaggedParserAtomIndex, 24ul, js::SystemAllocPolicy>, js::frontend::VectorPool<mozilla::Vector<js::frontend::TrivialTaggedParserAtomIndex, 24ul, js::SystemAllocPolicy> > >> = {
                all_ = {
                    <js::SystemAllocPolicy> = {
                        <js::AllocPolicyBase> = {<No data fields>}, 
                        <No data fields>}, 
                    static kElemIsPod = true, 
                    static kMaxInlineBytes = 999, 
                    static kInlineCapacity = 32, 
                    mBegin = 0x7ffff772d0e0, 
                    mLength = 7, 
                    mTail = {
                        <mozilla::Vector<void*, 32ul, js::SystemAllocPolicy>::CapacityAndReserved> = {
                        mCapacity = 32, mReserved = 7}, 
                        mBytes = " Xu\367\377\177\000\000\340^u\367\377\177\000\000\260Xu\367\377\177\000\000p_u\367\377\177\000\000@Pu\367\377\177\000\000\240Su\367\377\177\000\000\200[u\367\377\177\000\000", '\344' <repeats 199 times>...}, 
                    mEntered = false, 
                    static sMaxInlineStorage = 32}, 
                recyclable_ = {
                    <js::SystemAllocPolicy> = {
                        <js::AllocPolicyBase> = {<No data fields>}, 
                        <No data fields>}, 
                    static kElemIsPod = true, 
                    static kMaxInlineBytes = 999, 

                    static kInlineCapacity = 32, 
                    mBegin = 0x7ffff772d208, 
                    mLength = 7, 
                    mTail = {<mozilla::Vector<void*, 32ul, js::SystemAllocPolicy>::CapacityAndReserved> = {
                        mCapacity = 32, mReserved = 7}, 
                    mBytes = "\200[u\367\377\177\000\000\240Su\367\377\177\000\000@Pu\367\377\177\000\000p_u\367\377\177\000\000\260Xu\367\377\177\000\000\340^u\367\377\177\000\000 Xu\367\377\177\000\000", '\344' <repeats 199 times>...}, mEntered = false, static sMaxInlineStorage = 32}},
            <No data fields>}, 
        functionBoxVectorPool_ = {
            <js::frontend::CollectionPool<mozilla::Vector<js::frontend::FunctionBox*, 24ul, js::SystemAllocPolicy>, js::frontend::VectorPool<mozilla::Vector<js::frontend::FunctionBox*, 24ul, js::SystemAllocPolicy> > >> = {
                all_ = {
                    <js::SystemAllocPolicy> = {
                        <js::AllocPolicyBase> = {<No data fields>}, 
                        <No data fields>}, 
                    static kElemIsPod = true, 
                    static kMaxInlineBytes = 999, 
                    static kInlineCapacity = 32, 
                    mBegin = 0x7ffff772d330, 
                    mLength = 0, 
                    mTail = {
                        <mozilla::Vector<void*, 32ul, js::SystemAllocPolicy>::CapacityAndReserved> = {
                            mCapacity = 32, mReserved = 0}, 
                        mBytes = '\344' <repeats 255 times>...}, 
                    mEntered = false, 
                    static sMaxInlineStorage = 32}, 
                recyclable_ = {
                    <js::SystemAllocPolicy> = {
                            <js::AllocPolicyBase> = {<No data fields>}, 
                            <No data fields>}, 
                    static kElemIsPod = true, 
                    static kMaxInlineBytes = 999, 
                    static kInlineCapacity = 32, 
                    mBegin = 0x7ffff772d458, 
                    mLength = 0, 
                    mTail = {
                        <mozilla::Vector<void*, 32ul, js::SystemAllocPolicy>::CapacityAndReserved> = {
                            mCapacity = 32, mReserved = 0}, 
                        mBytes = '\344' <repeats 255 times>...}, 
                    mEntered = false, 
                    static sMaxInlineStorage = 32}}, 
            <No data fields>}, 
        activeCompilations_ = 0}, 
    check = {cx_ = 0x7ffff772cc00}}, <No data fields>}, 
```


## Garbage Collector, Memory Handling

```
suppressGC = {
    <js::ProtectedData<js::CheckContextLocal, int>> = {
        value = 0, check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 
```


## Security-related, Memory Handling

```
isolate = {
    <js::ProtectedData<js::CheckContextLocal, 
    v8::internal::Isolate*>> = {
        value = 0x7ffff7706470, 
        check = {
            cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

activation_ = {
    <js::ProtectedData<js::CheckContextLocal, 
    js::Activation*>> = {
        value = 0x7fffffffd868, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 
```


## GDB Debugger Support

```
insideDebuggerEvaluationWithOnNativeCallHook = {
    <js::ProtectedData<js::CheckContextLocal, js::Debugger*>> = {
        value = 0x0, 
        check = {
            cx_ = 0x7ffff772cc00}}, 
    <No data fields>}

debuggerMutations = {
    <js::ProtectedData<js::CheckContextLocal, unsigned int>> = {
        value = 0, check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 
```

## Disassembly Output

```
structuredSpewer_ = {
    <js::ProtectedData<js::CheckUnprotected, js::StructuredSpewer>> = {
        value = {
            outputInitializationAttempted_ = false, 
            spewingEnabled_ = 2, 
            output_ = {
                <js::GenericPrinter> = {_vptr$GenericPrinter = 0x555559248668 <vtable for js::Fprinter+16>, hadOOM_ = false}, 
                file_ = 0x0, 
                init_ = false}, 
            json_ = {
                <mozilla::detail::MaybeStorage<js::JSONPrinter, true>> = {
                    <mozilla::detail::MaybeStorageBase<js::JSONPrinter, true>> = {
                        mStorage = {
                            val = { 
                                indentLevel_ = 0, indent_ = false,  
                                first_ = false, out_ = @0x0},  
                            dummy = 0 '\000'}}, 
                    mIsSome = 0 '\000'}, 
                <mozilla::detail::Maybe_CopyMove_Enabler<js::JSONPrinter, true, true, true>> = {
                    <No data fields>}, 
                <No data fields>}, 
            selectedChannel_ = {channel_ = js::SpewChannel::Disabled}, 
            static names_ = {
                static kSize = 3, 
                mArray = {
                    mArr = {
                        0x5555559a10ad "BaselineICStats", 
                        0x5555559f414a "ScriptStats", 
                        0x555555a9bc91 "CacheIRHealthReport"}, 
                    static Length = 3}}}, 
        check = {<No data fields>}}, 
    <No data fields>}, 
```


# Profiling

```
profilingActivation_ = 0x0, 

measuringExecutionTime_ = {
    <js::ProtectedData<js::CheckContextLocal, bool>> = {
        value = true, check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

entryMonitor = {
    <js::ProtectedData<js::CheckContextLocal, 
    JS::dbg::AutoEntryMonitor*>> = {
        value = 0x0, check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

runningOOMTest = {
    <js::ProtectedData<js::CheckContextLocal, bool>> = {
        value = false, check = {cx_ = 0x7ffff772cc00}}, <No data fields>}, 

suppressProfilerSampling = {
    <mozilla::detail::AtomicBase<unsigned int, mozilla::SequentiallyConsistent>> = {
        mValue = {
            <std::__atomic_base<unsigned int>> = {
                static _S_alignment = 4, _M_i = 0}, 
            static is_always_lock_free = true}}, 
    <No data fields>}, 
```

# Logging
```
traceLogger = {
    <js::ProtectedData<js::CheckUnprotected, 
    js::TraceLoggerThread*>> = {
        value = 0x0, check = {<No data fields>}}, 
    <No data fields>}, 
```

# Miscellaneous

```
noExecuteDebuggerTop = {
    <js::ProtectedData<js::CheckContextLocal, 
    js::EnterDebuggeeNoExecute*>> = {
        value = 0x0, check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

inUnsafeCallWithABI = {
    <js::ProtectedData<js::CheckContextLocal, unsigned int>> = {
        value = 0, check = {cx_ = 0x7ffff772cc00}},
     <No data fields>}, 

hasAutoUnsafeCallWithABI = {
    <js::ProtectedData<js::CheckContextLocal, bool>> = {
        value = false, check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

dtoaState = {
    <js::ProtectedData<js::CheckContextLocal, DtoaState*>> = {
        value = 0x0, check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

disableStrictProxyCheckingCount = {
    <js::ProtectedData<js::CheckContextLocal, unsigned long>> = {
        value = 0, check = {cx_ = 0x7ffff772cc00}}, <No data fields>}, 

inUnsafeRegion = {
    <js::ProtectedData<js::CheckContextLocal, int>> = {
        value = 0, check = {cx_ = 0x7ffff772cc00}}, <No data fields>}, 

generationalDisabled = {
    <js::ProtectedData<js::CheckContextLocal, unsigned int>> = {
        value = 0, check = {cx_ = 0x7ffff772cc00}}, <No data fields>}, 

compactingDisabledCount = {
    <js::ProtectedData<js::CheckContextLocal, unsigned int>> = {
        value = 0, check = {cx_ = 0x7ffff772cc00}}, <No data fields>}, 

static TEMP_LIFO_ALLOC_PRIMARY_CHUNK_SIZE = 4096, 
tempLifoAlloc_ = {
    <js::ProtectedData<js::CheckContextLocal, js::LifoAlloc>> = {
        value = {
            chunks_ = {
                head_ = [(js::detail::BumpChunk *) 0x0], 
                last_ = 0x0}, 
            oversize_ = {
                head_ = [(js::detail::BumpChunk *) 0x0], 
                last_ = 0x0}, 
            unused_ = {
                head_ = [(js::detail::BumpChunk *) 0x7ffff77e5000], 
                last_ = 0x7ffff77c1000}, 
            markCount = 0, defaultChunkSize_ = 4096, 
            oversizeThreshold_ = 4096, curSize_ = 3145728, 
            peakSize_ = 3145728, smallAllocsSize_ = 0, 
            fallibleScope_ = true, static HUGE_ALLOCATION = 52428800}, 
        check = {
            cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

ionPcScriptCache = {
    <js::ProtectedData<js::CheckContextLocal, mozilla::UniquePtr<js::jit::PcScriptCache, JS::DeletePolicy<js::jit::PcScriptCache> > >> = {
        value = [(js::jit::PcScriptCache *) 0x0], 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

unwrappedException_ = {
    <js::ProtectedData<js::CheckContextLocal, JS::PersistentRooted<JS::Value> >> = {
        value = {
            <js::TypedRootedGCThingBase<js::PersistentRootedBase, JS::Value>> = {
                <js::PersistentRootedBase> = {
                    <mozilla::LinkedListElement<js::PersistentRootedBase>> = {
                        mNext = 0x7ffff772d618, 
                        mPrev = 0x7ffff772d618, 
                        mIsSentinel = false}, 
                    <No data fields>}, 
                <No data fields>}, 
        <js::RootedOperations<JS::Value, JS::PersistentRooted<JS::Value> >> = {
            <js::MutableWrappedPtrOperations<JS::Value, JS::PersistentRooted<JS::Value> >> = {
                <js::WrappedPtrOperations<JS::Value, JS::PersistentRooted<JS::Value>, void>> = {
                    <No data fields>}, 
                <No data fields>}, 
            <No data fields>}, 
        ptr = $JS::UndefinedValue()}, 
    check = {
        cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

unwrappedExceptionStack_ = {
    <js::ProtectedData<js::CheckContextLocal, JS::PersistentRooted<js::SavedFrame*> >> = {
        value = {
            <js::TypedRootedGCThingBase<js::PersistentRootedBase, js::SavedFrame*>> = {
                <js::PersistentRootedBase> = {
                    <mozilla::LinkedListElement<js::PersistentRootedBase>> = {
                        mNext = 0x7ffff772d640, 
                        mPrev = 0x7ffff772d640, 
                        mIsSentinel = false}, 
                    <No data fields>}, 
                <No data fields>}, 
            <js::RootedOperations<js::SavedFrame*, JS::PersistentRooted<js::SavedFrame*> >> = {
                <js::MutableWrappedPtrOperations<js::SavedFrame*, JS::PersistentRooted<js::SavedFrame*> >> = {
                    <js::WrappedPtrOperations<js::SavedFrame*, JS::PersistentRooted<js::SavedFrame*>, void>> = {
                        <No data fields>}, 
                    <No data fields>}, 
                <No data fields>}, 
            ptr = 0x0}, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

hadNondeterministicException_ = {
    <js::ProtectedData<js::CheckContextLocal, bool>> = {
    value = false, 
    check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

reportGranularity = {
    <js::ProtectedData<js::CheckContextLocal, int>> = {
        value = 3, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

resolvingList = {
    <js::ProtectedData<js::CheckContextLocal, js::AutoResolving*>> = {
        value = 0x0, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

enteredPolicy = {
    <js::ProtectedData<js::CheckContextLocal, js::AutoEnterPolicy*>> = {
        value = 0x0, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

generatingError = {
    <js::ProtectedData<js::CheckContextLocal, bool>> = {
        value = false, check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

cycleDetectorVector_ = {
    <js::ProtectedData<js::CheckContextLocal, JS::GCVector<JSObject*, 8ul, js::TempAllocPolicy> >> = {
        value = {
            vector = {
                <js::TempAllocPolicy> = {
                    <js::AllocPolicyBase> = {<No data fields>}, 
                    cx_ = 0x7ffff772cc00}, 
                static kElemIsPod = true, 
                static kMaxInlineBytes = 992, 
                static kInlineCapacity = 8, 
                mBegin = 0x7ffff772d6e0, 
                mLength = 0, 
                mTail = {
                    <mozilla::Vector<JSObject*, 8ul, js::TempAllocPolicy>::CapacityAndReserved> = {
                        mCapacity = 8, mReserved = 0}, 
                    mBytes = '\344' <repeats 63 times>, <incomplete sequence \344>}, 
                mEntered = false, static 
                sMaxInlineStorage = 8}}, 
        check = {
            cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

watchtowerTestingCallback_ = {
    <js::ProtectedData<js::CheckContextLocal, JS::PersistentRooted<JSFunction*> >> = {
        value = {
            <js::TypedRootedGCThingBase<js::PersistentRootedBase, JSFunction*>> = {
                <js::PersistentRootedBase> = {
                    <mozilla::LinkedListElement<js::PersistentRootedBase>> = {
                        mNext = 0x7ffff772d730, 
                        mPrev = 0x7ffff772d730, 
                        mIsSentinel = false}, 
                    <No data fields>}, 
                <No data fields>}, 
            <js::RootedOperations<JSFunction*, JS::PersistentRooted<JSFunction*> >> = {
                <js::MutableWrappedPtrOperations<JSFunction*, JS::PersistentRooted<JSFunction*> >> = {
                    <js::WrappedPtrOperations<JSFunction*, JS::PersistentRooted<JSFunction*>, void>> = {
                        <No data fields>}, 
                    <No data fields>}, 
                <No data fields>}, 
            ptr = 0x0}, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 

data = {
    <js::ProtectedData<js::CheckUnprotected, void*>> = {
        value = 0x7ffff7735500, 
        check = {<No data fields>}}, 
    <No data fields>}, 

inlinedICScript_ = {
    <js::ProtectedData<js::CheckContextLocal, js::jit::ICScript*>> = {
        value = 0x0, 
        check = {cx_ = 0x7ffff772cc00}}, 
    <No data fields>}, 
```

