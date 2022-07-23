title: Environment Variables for Mozilla Mach
date: 2022-06-23 07:28
status: published
tags: Mozilla, Mach, environment variables
category: research
lang: en
private: False


# Main

[jtable caption="This is caption" separator="," th=0 ai="1"]
`USERNAME`, uriloader/exthandler/nsExternalHelperAppServer.cpp
`USER`, uriloader/exthandler/nsExternalHelperAppServer.cpp
`LOGNAME`, uriloader/exthandler/nsExternalHelperAppServer.cpp
`PATH`, uriloader/exthandler/unix/nsOSHelperAppServer.cpp, modules/freetype2/builds/unix/ltmain.sh
`MOZ_DEFAULT_PREFS`, modules/libpref/Preferences.cpp
`MOZ_ANDROID_CPU_ABI`, modules/libpref/Preferences.cpp
`COMSPEC`, modules/freetype2/builds/unix/ltmain.sh
`JARLOG_FILE`, build/pgo/profileserver.py
`MOZ_JAR_LOG_FILE`, modules/libjar/nsZipArchive.cpp
`GRE_HOME`, xpcom/io/nsDirectoryService.cpp
`XDG_CONFIG_HOME`, xpcom/io/SpecialSystemDirectory.cpp
`TMPDIR`, xpcom/io/SpecialSystemDirectory.cpp
`TMP`, xpcom/io/SpecialSystemDirectory.cpp
`TEMP`, xpcom/io/SpecialSystemDirectory.cpp
`MOZ_CC_RUN_DURING_SHUTDOWN`, xpcom/build/XPCOMInit.cpp
`MOZ_IGNORE_NSS_SHUTDOWN_LEAKS`, xpcom/build/XPCOMInit.cpp
`XPCOM_MEM_BLOAT_LOG`, xpcom/build/XPCOMInit.cpp
`XPCOM_MEM_REFCNT_LOG`, xpcom/build/XPCOMInit.cpp
`MOZ_DISABLE_POISON_IO_INTERPOSER`, xpcom/build/IOInterposer.cpp
`MOZ_ANDROID_LIBDIR`, xpcom/build/BinaryPath.h
`MOZ_MAIN_THREAD_IO_LOG`, xpcom/build/MainThreadIOLogger.cpp
`MOZ_TASKCONTROLLER_THREADCOUNT`, xpcom/threads/TaskController.cpp
`MOZ_KILL_CANARIES`, xpcom/threads/nsThreadManager.cpp
`XPCOM_MEM_BLOAT_LOG`, xpcom/ds/nsAtomTable.cpp
`MOZ_RUN_GTEST`, xpcom/glue/standalone/nsXPCOMGlue.cpp
`FUZZER`, xpcom/glue/standalone/nsXPCOMGlue.cpp
`G_SLICE`, xpcom/glue/standalone/nsXPCOMGlue.cpp
`DOWNLOADS_DIRECTORY`, xpcom/base/nsDumpUtils.cpp
`MOZ_GC_LOG_SIZE`, xpcom/base/CycleCollectedJSRuntime.cpp
`MOZ_CC_LOG_ALL`, xpcom/base/nsCycleCollector.cpp
`MOZ_CC_LOG_SHUTDOWN`, xpcom/base/nsCycleCollector.cpp
`MOZ_CC_LOG_THREAD`, xpcom/base/nsCycleCollector.cpp
`MOZ_CC_LOG_PROCESS`, xpcom/base/nsCycleCollector.cpp
`MOZ_CC_ALL_TRACES`, xpcom/base/nsCycleCollector.cpp
`MOZ_CC_LOG_DIRECTORY`, xpcom/base/nsCycleCollector.cpp
`CACHE_DIRECTORY`, netwerk/cache2/CacheFileIOManager.cpp
`MOZ_DISABLE_SOCKET_PROCESS_SANDBOX`, netwerk/ipc/SocketProcessHost.cpp
`MOZ_SANDBOX_SOCKET_PROCESS_LOGGING`, netwerk/ipc/SocketProcessHost.cpp
`MOZ_DEBUG_SOCKET_PROCESS`, netwerk/ipc/SocketProcessImpl.cpp
`NECKO_ERRORS_ARE_FATAL`, netwerk/ipc/NeckoCommon.h
`MOZ_CRASHREPORTER_SHUTDOWN`, netwerk/ipc/SocketProcessParent.cpp
`NECKO_SOCKET_TRACE_LOG`, netwerk/base/nsSocketTransport2.cpp
`MOZ_DISABLE_SOCKET_PROCESS`, netwerk/base/nsIOService.cpp
`MOZ_FORCE_USE_SOCKET_PROCESS`, netwerk/base/nsIOService.cpp
`MOZ_DUMP_AUDIO`, dom/media/WavDumper.h
`MOZ_DISABLE_RDD_SANDBOX`, dom/media/ipc/RDDProcessHost.cpp
`MOZ_DEBUG_CHILD_PROCESS`, dom/media/ipc/RDDProcessHost.cpp
`MOZ_DEBUG_CHILD_PAUSE`, dom/media/ipc/RDDProcessHost.cpp
`MOZ_SANDBOX_RDD_LOGGING`, dom/media/ipc/RDDProcessHost.cpp
`R_LOG_LEVEL`, dom/media/webrtc/transport/third_party/nrappkit/src/log/r_log.c
`R_LOG_DESTINATION`, dom/media/webrtc/transport/third_party/nrappkit/src/log/r_log.c
`R_LOG_VERBOSE`, dom/media/webrtc/transport/third_party/nrappkit/src/log/r_log.c
`GMP_LOGGING`, dom/media/gmp-plugin-openh264/gmp-fake-openh264.cpp
`MOZ_SANDBOX_GMP_LOGGING`, dom/media/gmp/GMPProcessParent.cpp
`MOZ_SANDBOX_LOGGING`, dom/media/gmp/GMPProcessParent.cpp
`MOZ_GMP_PATH`, dom/media/gmp/GMPServiceParent.cpp
`MOZ_DISABLE_GMP_SANDBOX`, dom/media/gmp/GMPLoader.cpp
`MOZ_SANDBOX_LOGGING`, dom/ipc/ContentParent.cpp
`XPCSHELL_TEST_PROFILE_DIR`, dom/ipc/ContentParent.cpp
`MOZ_GDK_DISPLAY`, dom/ipc/ContentChild.cpp
`DISPLAY`, dom/ipc/ContentChild.cpp
`MOZ_DEBUG_APP_PROCESS`, dom/ipc/ContentChild.cpp
`XDG_RUNTIME_DIR`, dom/ipc/ContentChild.cpp
`XDG_CONFIG_HOME`, dom/ipc/ContentChild.cpp
`XDG_CACHE_HOME`, dom/ipc/ContentChild.cpp
`XDG_DATA_HOME`, dom/ipc/ContentChild.cpp
`DBUS_SESSION_BUS_ADDRESS`, dom/ipc/ContentChild.cpp
`MOZ_LOG_MESSAGEMANAGER_SKIP`, dom/ipc/MMPrinter.cpp
`XPCSHELL_TEST_PROFILE_DIR`, dom/quota/QuotaManager.h
`MOZ_RUN_GTEST`, dom/quota/QuotaManager.h
`LSNG_CRASH_ON_CANCEL`, dom/localstorage/ActorsParent.cpp
`MOZ_DISABLE_OOP_TABS`, dom/base/nsFrameLoader.cpp

[/jtable]

# Debug Support
Environment variables used for testing

[jtable]
`FT2_DEBUG`, modules/freetype2/src/base/ftdebug.c
`FT_LOGGING_FILE`, modules/freetype2/src/base/ftdebug.c
`FT2_DEBUG_MEMORY`, modules/freetype2/src/base/ftdbgmem.c
`FT2_ALLOC_TOTAL_MAX`, modules/freetype2/src/base/ftdbgmem.c
`FT2_ALLOC_COUNT_MAX`, modules/freetype2/src/base/ftdbgmem.c
`FT2_KEEP_ALIVE`, modules/freetype2/src/base/ftdbgmem.c
`FREETYPE_PROPERTIES`, modules/freetype2/src/base/ftinit.c
`XPCOM_DEBUG_BREAK`, xpcom/base/nsDebugImpl.cpp
`MOZ_IGNORE_WARNINGS`, xpcom/base/nsDebugImpl.cpp
`XPCOM_DEBUG_DLG`, xpcom/base/nsDebugImpl.cpp
`MOZ_CONSOLESERVICE_DISABLE_DEBUGGER_OUTPUT`, xpcom/base/nsDebugImpl.cpp
`XUL_APP_FILE`, xpcom/base/AppShutdown.cpp
`MOZ_LOG`, xpcom/base/Logging.cpp
`MOZ_LOG_MODULES`, xpcom/base/Logging.cpp
`NSPR_LOG_MODULES`, xpcom/base/Logging.cpp
`MOZ_LOG_FILE`, xpcom/base/Logging.cpp
`NSPR_LOG_FILE`, xpcom/base/Logging.cpp
`MOZ_FATAL_STATIC_XPCOM_CTORS_DTORS`, xpcom/base/nsTraceRefcnt.cpp
`XPCOM_MEM_LOG_CLASSES`, xpcom/base/nsTraceRefcnt.cpp
`XPCOM_MEM_LOG_CLASSES`, xpcom/base/nsTraceRefcnt.cpp
`XPCOM_MEM_COMPTR_LOG`, xpcom/base/nsTraceRefcnt.cpp
`XPCOM_MEM_LOG_OBJECTS`, xpcom/base/nsTraceRefcnt.cpp
`XPCOM_MEM_LOG_JS_STACK`, xpcom/base/nsTraceRefcnt.cpp
`MOZ_DMD_SHUTDOWN_LOG`, xpcom/base/nsTraceRefcnt.cpp
`MOZ_DMD_LOG_PROCESS`, xpcom/base/nsTraceRefcnt.cpp
`XPCOM_MEM_BLOAT_LOG`, xpcom/base/IntentionalCrash.h
`MOZ_WEBGL_DUMP_SHADERS`, dom/canvas/WebGLShader.cpp
`MOZ_WEBGL_FORCE_EGL`, dom/canvas/WebGLContext.cpp
`MOZ_WEBGL_FORCE_OPENGL`, dom/canvas/WebGLContext.cpp

[/jtable]

# Test Support
Testing Environment

[jtable]
`WRITE_ARGUMENT_FILE`, uriloader/exthandler/tests/WriteArgument.cpp
`FREETYPE_TESTS_DATA_DIR`, modules/freetype2/tests/issue-1063/main.c
`MOZ_XRE_DIR`, xpcom/tests/TestHarness.h
`TURN_SERVER_ADDRESS`, dom/media/webrtc/transport/test/gtest_utils.h
`TURN_SERVER_USER`, dom/media/webrtc/transport/test/gtest_utils.h
`TURN_SERVER_PASSWORD`, dom/media/webrtc/transport/test/gtest_utils.h
`STUN_SERVER_ADDRESS`, dom/media/webrtc/transport/test/gtest_utils.h
`STUN_SERVER_HOSTNAME`, dom/media/webrtc/transport/test/gtest_utils.h
`MOZ_DISABLE_NONLOCAL_CONNECTIONS`, dom/media/webrtc/transport/test/gtest_utils.h
`MOZ_UPLOAD_DIR`, dom/media/webrtc/transport/test/gtest_utils.h
`MOZ_IPC_MESSAGE_FUZZ_BLACKLIST`, dom/ipc/fuzztest/content_parent_ipc_libfuzz.cpp
[/jtable]

# Architecture-Specific
Architecture specific environment variable names

## Apple macOS
[jtable]
`XPCOM_MEM_BLOAT_LOG`, xpcom/base/nsMacUtilsImpl.cpp
`XPCOM_MEM_LEAK_LOG`, xpcom/base/nsMacUtilsImpl.cpp

[/jtable]
