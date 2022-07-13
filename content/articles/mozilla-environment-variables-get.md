title: Mozilla Environment Variables, getting
date: 2022-06-27 05:30
status: published
tags: environment variables, Mozilla, Firefox
category: research
lang: en
private: False

Everything you need to know about environment variables in the Mozilla Unified repository.  Mozilla Unified covers the following applications/products:

* Firefox
* Thunderbird


# References

* https://firefox-source-docs.mozilla.org/security/nss/legacy/reference/nss_environment_variables/index.html


# Environment Variables

Environment variables are broken up into getting and setting the environment variables.


# Setting Environment Variables

For setting the environment variable, a separate page is maintained for ease of maintability: See [Mozilla Environment Variables, Setting]({filename}mozilla-environment-variables-set.md)


# Getting Environment Variables



Environment variables that got read (via `getenv()`) in Mozilla Unified repository, git HEAD branch:

[jtable]
environment variable name, description, source file
 `A11YLOG`,, accessible/base/Logging.cpp
 `all_proxy`,, toolkit/system/unixproxy/nsUnixSystemProxySettings.cpp
 `ANDROID_ROOT`,, gfx/skia/patches/archive/0004-Bug-777614-Re-apply-bug-719872-Fix-crash-on-Android-.patch gfx/skia/patches/archive/0007-Bug-719872-Old-Android-FontHost.patch gfx/skia/patches/archive/old-android-fonthost.patch gfx/skia/skia/src/ports/SkFontMgr_android_parser.cpp gfx/thebes/gfxFT2FontList.cpp third_party/python/virtualenv/\__virtualenv__/platformdirs-2.2.0-py3-none-any/platformdirs/\__init__.py
 `ANGLE_DEFAULT_PLATFORM`,, gfx/angle/checkout/src/libANGLE/Display.cpp
 `ANGLE_WAIT_FOR_DEBUGGER`,, gfx/angle/checkout/src/libGLESv2/global_state.cpp
 `AOM_SIMD_CAPS_MASK`,, third_party/aom/aom_ports/arm_cpudetect.c third_party/aom/aom_ports/ppc_cpudetect.c third_party/aom/aom_ports/x86.h
 `AOM_SIMD_CAPS`,, third_party/aom/aom_ports/arm_cpudetect.c third_party/aom/aom_ports/ppc_cpudetect.c third_party/aom/aom_ports/x86.h
 `AR`,filepath specification to the `ar` archive binary executable file, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `ARM_ASM_NOP_FILL`,, js/src/jit/arm/Assembler-arm.cpp
 `ARM_SIM_DEBUGGER`,, js/src/jit/arm/Simulator-arm.cpp
 `ARM_SIM_ICACHE_CHECKS`,, js/src/jit/arm/Simulator-arm.cpp
 `ARM_SIM_STOP_AT`,takes a non-negative integer to indicate when to stop the ARM-based simulator, js/src/jit/arm/Simulator-arm.cpp
 `ARMHWCAP`,, js/src/jit/arm/Architecture-arm.cpp
 `ASM_POOL_MAX_OFFSET`,a positive integer indicating the maximum offset to the AssemblyShared memory pool used for disassembly.  Default is 1024.  Internally starts at 0xe320f000 and ends at 0xeaffffff., js/src/jit/arm/Assembler-arm.cpp
 `AUDIO_DEVICE`,sassembly.  Default is 1024.  Internally starts at 0xe320f000 and ends at 0xeaffffff., media/libcubeb/src/cubeb-jni-instances.h
 `AUDIODEVICE`,filepath specification to the sound audio device name.  Defaults to `snd/0`., media/libcubeb/src/cubeb_sndio.c third_party/rust/cubeb-sys/libcubeb/src/cubeb_sndio.c
 `aus_server`, `https://aus5.mozilla.org`, tools/update-verify/scripts/async_download.py, 
 `AUTOCONFIG_TEST_GETENV`,, extensions/pref/autoconfig/test/unit/autoconfig-all.cfg extensions/pref/autoconfig/test/unit/test_autoconfig.js
 `AV_LOG_FORCE_256COLOR`,if defined then forcibly use 256-color on media streaming, media/ffvpx/libavutil/log.c, 
 `AV_LOG_FORCE_COLOR`,if defined then forcibly use 16-color on media streaming, media/ffvpx/libavutil/log.c
 `AV_LOG_FORCE_NOCOLOR`,if defined then forcibly use no color on media streaming, media/ffvpx/libavutil/log.c
 `bindir`,, toolkit/crashreporter/breakpad-client/linux/minidump_writer/minidump_writer_unittest_utils.cc
 `BUMBLEBEE_SOCKET`,filepath specification to the UNIX socket for Primus to contact the Bumblebee daemon to manage CPU on NVIDIA Optimus systems.  Default is `/var/run/bumblebee.socket`., security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp
 `CACHE_DIRECTORY`,filepath specification to the cache directory for Android Widget system.  Useful for profile-less setups., netwerk/cache2/CacheFileIOManager.cpp
 `CACHEIR_LOG_FLUSH`,positive integer of JIT instruction interval count before flushing to a cache.  Only available if `JS_CACHEIR_SPEW` C macro is defined., js/src/jit/CacheIRSpewer.cpp
 `CACHEIR_LOGS`, filepath specification to the JSON-formatted file containing cached intermediate representation of JavaScript code. Defaults to `$JIT_SPEW_DIR/cacheir${PID}.json`, js/src/jit/JitContext.cpp, 
 `CAIRO_DEBUG_DRM`, if defined then enables the debug flag to the video synch state of Cairo-based DRM device driver to the Intel i915 graphic hardware, gfx/cairo/cairo/src/drm/cairo-drm-i915-surface.c, 
 `CAIRO_DEBUG_EVENTS`, if defined then output and append debug statements related to `libevent` into the `bo-events.txt` file into the current working directory. Available if `DEBUG_EVENT` macro is defined during C compilation., gfx/cairo/cairo/src/cairo-bentley-ottmann.c, 
 `CAIRO_DEBUG_PDF`, if defined then Deflate compression gets disabled during surface rendering and `/Filter` and `/Flatedecode` are not PDF-outputted., gfx/cairo/cairo/src/cairo-pdf-surface.c, 
 `CAIRO_DEBUG_TAG`, if defined then all error messages related to PDF tag are outputted to `stdout`., gfx/cairo/cairo/src/cairo-tag-stack.c, 
 `CAIRO_DEBUG_TRAPS`, if defined then output and append debug statements related to polygon edges into the `bo-polygon-edges.txt` file and tesselates into the `bo-polygon-in.txt` and traps into the `bo-polygon-out.txt` file into the current working directory. Available if `DEBUG_EVENT` macro is defined during C compilation., gfx/cairo/cairo/src/cairo-bentley-ottmann.c gfx/cairo/cairo/src/cairo-bentley-ottmann-rectangular.c gfx/cairo/cairo/src/cairo-boxes-intersect.c, 
 `CAIRO_DEBUG`, if defined and has the `xrender-version=X` where X is the version string then the Cairo render driver is limited to that set of driver functionality by version number., gfx/cairo/cairo/src/cairo-xcb-connection.c gfx/cairo/cairo/src/cairo-xlib-display.c, 
 `CAIRO_GALLIUM_FORCE`, if defined then use all of the graphic device memory map. Only available if `CARIO_HAS_GALLIUM_SURFACE` macro is defined during C compilation., gfx/cairo/cairo/src/drm/cairo-drm.c, 
 `CAIRO_GALLIUM_LIBDIR`, filepath specification to the i915 device driver shared library. Default is `/usr/lib/dri/i915_dri.so`., gfx/cairo/cairo/src/drm/cairo-drm-gallium-surface.c, 
 `CAIRO_GL_COMPOSITOR`, if defined and contains the `msaa` value then force use the multi-sample anti-alias compositor function otherwise use the standard compositor., gfx/cairo/cairo/src/cairo-gl-device.c, 
 `CAIRO_GL_VBO_SIZE`, if defined and has a positive number for number of bytes to allocate for usage by the vertex buffer object (VBO). Default is `1048576`. If embedded GL is used then 16384 is defined., gfx/cairo/cairo/src/cairo-gl-info.c, 
 `CARGO_CFG_TARGET_FEATURE`, if defined and contains `cargo` options then incorporated during rust build, third_party/rust/cc/src/lib.rs, 
 `CARGOFLAGS`, if defined and contains `cargo` options then incorporated during rust build, gfx/wr/wrench/script/headless.py, 
 `CLEARKEY_LOG_FILE`, if defined and contains a filepath specification to the log file then all `stdout` print output will be redirected to this file for `gmp-clearkey` library., media/gmp-clearkey/0.1/ClearKeyUtils.cpp, 
 `COMSPEC`,, js/src/ctypes/libffi/ltmain.sh modules/freetype2/builds/unix/ltmain.sh
 `CRASHES_EVENTS_DIR`, if defined and contains directory path specification then directory path is created and `ProfD`/`UAppData`/`ProfDS` subdirectory are created to capture all events found during a Mozilla-type crash., toolkit/crashreporter/nsExceptionHandler.cpp, 
 `CRATE_CC_NO_DEFAULTS`, if defined then no defaults are used when building the rust compiler for use by Mozilla Unified repository, third_party/rust/cc/src/lib.rs, 
 `CROSS_CCTOOLS_PATH`, if defined and contains filepath specification then all compiler-related tools for cross-compilation to a different platform get stored here for use by building within Mozilla Unified repository, build/build-clang/build-clang.py, 
 `CROSS_COMPILE`, if defined and contains filepath specification then all compiler-related tools for cross-compilation to a different platform get stored here for use by building within Mozilla Unified repository, third_party/rust/cc/src/lib.rs, 
 `CROSS_SYSROOT`, if defined and contains filepath specification then all compiler-related tools for cross-compilation to a different platform get stored here for use by `chroot()` building within Mozilla Unified repository, build/build-clang/build-clang.py, 
 `DBUS_SESSION_BUS_ADDRESS`, if defined then accessibility state is obtained using `org.a11y.Status` from the DBUS. Only available if `GNOME_ACCESSIBILITY` macro not defined during C compiler stage., accessible/atk/Platform.cpp dom/ipc/ContentChild.cpp, 
 `DEBUG`, if defined then all debug output are enabled during rust compiling within Mozilla Unified repository, third_party/rust/cc/src/lib.rs, 
 `DESKTOP_AUTOSTART_ID`, if defined and contains the X11 session ID then the same X11 session is reused during restart. Only available in UNIX platforms having X11 and Gtk v2.10+ support. `SESSION_MANAGER` must be defined before this takes effect., toolkit/xre/nsNativeAppSupportUnix.cpp, 
 `DESKTOP_SESSION`, if defined and contains `budgie` value then use special GNOME desktop otherwise contains `gnome`/`kde`/`xfce`/`cinnamon`/`enlightenment`/`lxde`/`lubuntu`/`openbox`/`i3`/`swap`/`mate`/`unity`/`pantheon`/`lxqt`/`deepin`/`dwm` then redirect to its specified window manager. `XDG_CURRENT_DESKTOP` must be defined before this takes effect., widget/gtk/GfxInfo.cpp, 
 `DESKTOP_STARTUP_ID`, To communicate the startup sequence information from a launcher, toolkit/xre/nsAppRunner.cpp
 `DICPATH`, filepath specification to a UTF-8 text file containing a dictionary of words used by Mozilla spell-checker., extensions/spellcheck/hunspell/glue/mozHunspell.cpp, 
 `DOWNLOADS_DIRECTORY`,, xpcom/base/nsDumpUtils.cpp
 `DUMP_DEBUG`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `DYLD_INSERT_LIBRARIES`,, ipc/glue/GeckoChildProcessHost.cpp
 `DYLD_LIBRARY_PATH`,, ipc/glue/GeckoChildProcessHost.cpp
 `EVENT_EPOLL_USE_CHANGELIST`,, ipc/chromium/src/third_party/libevent/epoll.c
 `EVENT_PRECISE_TIMER`,, ipc/chromium/src/third_party/libevent/event.c
 `EVENT_SHOW_METHOD`,, ipc/chromium/src/third_party/libevent/event.c
 `EXPAT_ENTROPY_DEBUG`,, parser/expat/lib/xmlparse.c
 `FAULTY_AS_WHITELIST`,, tools/fuzzing/faulty/Faulty.cpp
 `FAULTY_BLACKLIST`,, tools/fuzzing/faulty/Faulty.cpp
 `FAULTY_CHILDREN`,, tools/fuzzing/faulty/Faulty.cpp
 `FAULTY_ENABLE_LOGGING`,, tools/fuzzing/faulty/Faulty.cpp
 `FAULTY_LARGE_VALUES`,, tools/fuzzing/faulty/Faulty.cpp
 `FAULTY_MESSAGE_PATH`,, tools/fuzzing/faulty/Faulty.cpp
 `FAULTY_MESSAGES`,, tools/fuzzing/faulty/Faulty.cpp
 `FAULTY_MUTATION_FACTOR`,, tools/fuzzing/faulty/Faulty.cpp
 `FAULTY_PARENT`,, tools/fuzzing/faulty/Faulty.cpp
 `FAULTY_PICKLE`,, tools/fuzzing/faulty/Faulty.cpp
 `FAULTY_PIPE`,, tools/fuzzing/faulty/Faulty.cpp
 `FAULTY_PROBABILITY`,, tools/fuzzing/faulty/Faulty.cpp
 `FAULTY_SEED`,, tools/fuzzing/faulty/Faulty.cpp
 `foo`,, nsprpub/pr/include/prenv.h
 `FORCE_COLOR`,, third_party/wasm2c/src/color.cc
 `FREETYPE_PROPERTIES`,, modules/freetype2/src/base/ftinit.c
 `FT_LOGGING_FILE`,, modules/freetype2/src/base/ftdebug.c
 `FT2_ALLOC_COUNT_MAX`,, modules/freetype2/src/base/ftdbgmem.c
 `FT2_ALLOC_TOTAL_MAX`,, modules/freetype2/src/base/ftdbgmem.c
 `FT2_DEBUG_MEMORY`,, modules/freetype2/src/base/ftdbgmem.c
 `FT2_DEBUG`,, modules/freetype2/src/base/ftdebug.c modules/freetype2/src/base/ftdebug.c
 `FT2_KEEP_ALIVE`,, modules/freetype2/src/base/ftdbgmem.c
 `ftp_server_to`, `http://stage.mozilla.org/pub/mozilla.org`, tools/update-verify/scripts/async_download.py, 
 `FUZZER`,, browser/app/nsBrowserApp.cpp js/src/fuzz-tests/tests.cpp js/src/shell/js.cpp js/src/shell/jsrtfuzzing/jsrtfuzzing.cpp js/xpconnect/src/xpcrtfuzzing/xpcrtfuzzing.cpp js/xpconnect/src/XPCShellImpl.cpp toolkit/xre/nsAppRunner.cpp tools/fuzzing/interface/harness/FuzzerRunner.cpp xpcom/glue/standalone/nsXPCOMGlue.cpp
 `FUZZER`,, js/src/shell/js.cpp
 `G_BROKEN_FILENAMES`,, browser/components/shell/nsGNOMEShellService.cpp
 `G_SLICE`,, xpcom/glue/standalone/nsXPCOMGlue.cpp
 `GCOV_CHILD_PREFIX`,, ipc/chromium/src/base/process_util_linux.cc
 `GDB_DOT`,, js/src/gdb/mozilla/IonGraph.py
 `GDB_IONGRAPH`,, js/src/gdb/mozilla/IonGraph.py
 `GDB_PNGVIEWER`,, js/src/gdb/mozilla/IonGraph.py
 `GDK_BACKEND`,, toolkit/xre/nsAppRunner.cpp
 `GECKO_BLOCK_DEBUG_FLAGS`,, layout/generic/nsBlockFrame.cpp
 `GECKO_DISPLAY_REFLOW_ASSERT`,, layout/generic/nsIFrame.cpp
 `GECKO_DISPLAY_REFLOW_FLAG_PIXEL_ERRORS`,, layout/generic/nsIFrame.cpp
 `GECKO_DISPLAY_REFLOW_INDENT_START`,, layout/generic/nsIFrame.cpp
 `GECKO_DISPLAY_REFLOW_INDENT_UNDISPLAYED_FRAMES`,, layout/generic/nsIFrame.cpp
 `GECKO_DISPLAY_REFLOW_PROCESSES`,, layout/generic/nsIFrame.cpp
 `GECKO_DISPLAY_REFLOW_RULES_FILE`,, layout/generic/nsIFrame.cpp
 `GECKO_FRAMECTOR_DEBUG_FLAGS`,, layout/base/nsCSSFrameConstructor.cpp
 `GECKO_REFLOW_INTERRUPT_CHECKS_TO_SKIP`,, layout/base/nsPresContext.cpp
 `GECKO_REFLOW_INTERRUPT_FREQUENCY`,, layout/base/nsPresContext.cpp
 `GECKO_REFLOW_INTERRUPT_MODE`,, layout/base/nsPresContext.cpp
 `GECKO_REFLOW_INTERRUPT_SEED`,, layout/base/nsPresContext.cpp
 `GECKO_REFLOW_MIN_NOINTERRUPT_DURATION`,, layout/base/nsPresContext.cpp
 `GECKO_VERIFY_REFLOW_FLAGS`,, layout/base/PresShell.cpp
 `GMP_LOGGING`,, dom/media/gmp-plugin-openh264/gmp-fake-openh264.cpp
 `GNOME_ACCESSIBILITY`,, accessible/atk/Platform.cpp
 `GNOME_DESKTOP_SESSION_ID`,, browser/components/shell/nsGNOMEShellService.cpp widget/gtk/GfxInfo.cpp
 `GRE_HOME`,, gfx/gl/GLLibraryEGL.cpp xpcom/io/nsDirectoryService.cpp
 `GTK_CSD`,, widget/gtk/nsWindow.cpp
 `GTK_USE_PORTAL`,, widget/gtk/nsFilePicker.cpp widget/gtk/WidgetUtilsGtk.cpp
 `HAZARD_RUN_INTERNAL_TESTS`,, js/src/devtools/rootAnalysis/computeGCTypes.js
 `HB_OPTIONS`,, gfx/harfbuzz/src/hb-common.cc
 `HB_SHAPER_LIST`,, gfx/harfbuzz/src/hb-shaper.cc
 `HBHEADERS`,, gfx/harfbuzz/src/check-c-linkage-decls.py gfx/harfbuzz/src/check-externs.py gfx/harfbuzz/src/check-header-guards.py
 `HBSOURCES`,, gfx/harfbuzz/src/check-c-linkage-decls.py gfx/harfbuzz/src/check-header-guards.py
 `HOME`,, gfx/vr/service/openvr/src/pathtools_public.cpp gfx/vr/service/openvr/src/vrpathregistry_public.cpp  browser/components/shell/nsGNOMEShellService.cpp security/nss/cmd/lib/secutil.c security/nss/cmd/signtool/util.c security/nss/gtests/sysinit_gtest/getUserDB_unittest.cc security/nss/lib/sysinit/nsssysinit.c security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp security/sandbox/mac/Sandbox.mm testing/mozbase/mozproxy/mozproxy/backends/mitm/android.py testing/mozbase/mozproxy/mozproxy/backends/mitm/desktop.py toolkit/crashreporter/client/crashreporter_gtk_common.cpp toolkit/xre/nsAppRunner.cpp toolkit/xre/nsXREDirProvider.cpp widget/nsPrinterListCUPS.cpp widget/nsPrintSettingsImpl.cpp xpcom/io/nsAppFileLocationProvider.cpp xpcom/io/SpecialSystemDirectory.cpp
 `HOST`,, third_party/rust/cc/src/lib.rs
 `http_proxy`,, toolkit/crashreporter/client/crashreporter_gtk_common.cpp
 `IBUS_ENABLE_SYNC_MODE`,, widget/gtk/IMContextWrapper.cpp
 `ICU_DATA`,, intl/icu/source/common/putil.cpp
 `ICU_PDS_NAME_SUFFIX`,, intl/icu/source/tools/pkgdata/pkgdata.cpp
 `ICU_PDS_NAME`,, intl/icu/source/tools/pkgdata/pkgdata.cpp
 `ICU_PLUGINS`,, intl/icu/source/common/icuplug.cpp
 `ICU_TIMEZONE_FILES_DIR`,, intl/icu/source/common/putil.cpp
 `INSIDE_EMACS`,, js/examples/jorendb.js
 `INTGEMM_CPUID`,, third_party/intgemm/intgemm/intgemm.cc
 `ION_SPEW_BY_PID`,, js/src/jit/JitSpewer.cpp
 `ION_SPEW_FILENAME`,, js/src/jit/JitSpewer.cpp
 `IONFILTER`,, js/src/jit/JitSpewer.cpp
 `IONFLAGS`,, js/src/jit/JitSpewer.cpp
 `IONPERF`,, js/src/jit/PerfSpewer.cpp
 `JAR_HOME`,, security/nss/cmd/signtool/util.c
 `JPEG_MEM`,, media/libjpeg/jinclude.h media/libjpeg/jmemmgr.c
 `JS_GC_ZEAL`,, js/src/gc/GC.cpp
 `JS_NO_UNALIGNED_MEMCPY`,, js/src/jit/shared/AtomicOperations-shared-jit.cpp
 `JS_TRACELOGGER_SPEW`,, js/src/vm/TraceLogging.cpp
 `JSGC_EXTRA_POISONING`,, js/src/vm/Initialization.cpp
 `JSGC_MARK_STACK_LIMIT`,, js/src/gc/GC.cpp
 `JSGC_PRETENURE_THRESHOLD`,, js/src/gc/GC.cpp
 `JSIMB_FASTLD3`,, media/libjpeg/simd/arm/aarch32/jsimd.c
 `JSIMB_FASTST3`,, media/libjpeg/simd/arm/aarch32/jsimd.c
 `JSIMB_FORCE3DNOW`,, media/libjpeg/simd/arm/aarch32/jsimd.c
 `JSIMB_FORCEAVX2`,, media/libjpeg/simd/arm/aarch32/jsimd.c
 `JSIMB_FORCEMMX`,, media/libjpeg/simd/arm/aarch32/jsimd.c
 `JSIMB_FORCENEON`,, media/libjpeg/simd/arm/aarch32/jsimd.c
 `JSIMB_FORCENONE`,, media/libjpeg/simd/arm/aarch32/jsimd.c
 `JSIMB_FORCESSE`,, media/libjpeg/simd/arm/aarch32/jsimd.c
 `JSIMB_FORCESSE2`,, media/libjpeg/simd/arm/aarch32/jsimd.c
 `JSIMB_NOHUFFENC`,, media/libjpeg/simd/arm/aarch32/jsimd.c
 `JSIMD_FORCEALTIVEC`,, media/libjpeg/simd/powerpc/jsimd.c
 `JSIMD_FORCEDSPR2`,, media/libjpeg/simd/mips/jsimd.c
 `JSIMD_FORCEMMI`,, media/libjpeg/simd/mips64/jsimd.c
 `JSIMD_FORCENONE`,, media/libjpeg/simd/mips64/jsimd.c media/libjpeg/simd/mips/jsimd.c media/libjpeg/simd/powerpc/jsimd.c
 `KDE_FULL_SESSION`,, widget/gtk/GfxInfo.cpp
 `LANG`,, editor/spellchecker/EditorSpellCheck.cpp intl/icu/source/common/putil.cpp
 `LANGUAGE`,, gfx/thebes/gfxFcPlatformFontList.cpp
 `LC_ALL`,, intl/icu/source/common/putil.cpp
 `LC_CTYPE`,, intl/icu/source/common/putil.cpp
 `LC_MESSAGES`,, intl/icu/source/common/putil.cpp
 `LD_PRELOAD`,, security/sandbox/linux/launch/SandboxLaunch.cpp
 `LDD`,, gfx/harfbuzz/src/check-libstdc++.py
 `LIBGL_DEBUG`,, third_party/rust/glslopt/glsl-optimizer/src/mesa/main/context.c
 `libs`,, gfx/harfbuzz/src/check-libstdc++.py gfx/harfbuzz/src/check-symbols.py
 `LIBYUV_DISABLE_MIPS_DSP`,, third_party/aom/third_party/libyuv/source/cpu_id.cc
 `LIBYUV_DISABLE_MIPS_DSPR2`,, third_party/aom/third_party/libyuv/source/cpu_id.cc
 `LIBYUV_DISABLE_MIPS`,, third_party/aom/third_party/libyuv/source/cpu_id.cc
 `LIBYUV_DISABLE_MSA`,, media/libyuv/libyuv/source/cpu_id.cc
 `LOADMOD`,, intl/icu/source/tools/pkgdata/pkgdata.cpp
 `LOCALE_DECIMAL_POINT`,, js/src/jsnum.cpp
 `LOCALE_GROUPING`,, js/src/jsnum.cpp
 `LOCALE_THOUSANDS_SEP`,, js/src/jsnum.cpp
 `LOCALTIME`,, third_party/libwebrtc/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_lookup.cc
 `LOGNAME`,, toolkit/components/remote/nsXRemoteClient.cpp toolkit/components/remote/nsXRemoteServer.cpp uriloader/exthandler/nsExternalHelperAppService.cpp
 `LOONG64_SIM_ICACHE_CHECKS`,, js/src/jit/loong64/Simulator-loong64.cpp
 `LOONG64_SIM_STOP_AT`, takes a non-negative integer to indicate which line to stop the LOONG64-based just-in-time (JIT) simulator. `--loong64-sim-stop-at` CLI option to `jsshell`., js/src/jit/loong64/Simulator-loong64.cpp, 
 `LOONG64_SIM_STOP_AT`,, js/src/jit/loong64/Simulator-loong64.cpp
 `LSNG_CRASH_ON_CANCEL`,, dom/localstorage/ActorsParent.cpp
 `LXQT_SESSION_CONFIG`,, widget/gtk/GfxInfo.cpp
 `MALLOC_FAIL_AT`,, media/libwebp/src/utils/utils.c
 `MALLOC_LIMIT`,, media/libwebp/src/utils/utils.c
 `MALLOC_LOG_MINIMAL`,, memory/replace/logalloc/LogAlloc.cpp
 `MALLOC_LOG`,, memory/replace/logalloc/LogAlloc.cpp
 `MALLOC_OPTIONS`,, ipc/glue/GeckoChildProcessHost.cpp memory/build/mozjemalloc.cpp nsprpub/pr/src/malloc/prmalloc.c
 `MATE_DESKTOP_SESSION_ID`,, widget/gtk/GfxInfo.cpp
 `MESA_EXTENSION_OVERRIDE`,, third_party/rust/glslopt/glsl-optimizer/src/compiler/glsl/shader_cache.cpp
 `MESA_GLSL_CACHE_DIR`,, third_party/rust/glslopt/glsl-optimizer/src/util/disk_cache.c
 `MESA_GLSL_CACHE_MAX_SIZE`,, third_party/rust/glslopt/glsl-optimizer/src/util/disk_cache.c
 `MESA_INFO`,, third_party/rust/glslopt/glsl-optimizer/src/mesa/main/context.c
 `MESA_TEX_PROG`,, third_party/rust/glslopt/glsl-optimizer/src/mesa/main/context.c
 `MESA_TNL_PROG`,, third_party/rust/glslopt/glsl-optimizer/src/mesa/main/context.c
 `MESSAGEMANAGER_FUZZER_BLACKLIST`,, tools/fuzzing/messagemanager/MessageManagerFuzzer.cpp
 `MESSAGEMANAGER_FUZZER_ENABLE_LOGGING`,, tools/fuzzing/messagemanager/MessageManagerFuzzer.cpp
 `MESSAGEMANAGER_FUZZER_ENABLE`,, tools/fuzzing/messagemanager/MessageManagerFuzzer.cpp
 `MESSAGEMANAGER_FUZZER_MUTATION_PROBABILITY`,, tools/fuzzing/messagemanager/MessageManagerFuzzer.cpp
 `MESSAGEMANAGER_FUZZER_STRINGSFILE`,, tools/fuzzing/messagemanager/MessageManagerFuzzer.cpp
 `MIPS_SIM_ICACHE_CHECKS`,, js/src/jit/mips32/Simulator-mips32.cpp js/src/jit/mips64/Simulator-mips64.cpp
 `MIPS_SIM_STOP_AT`, takes a non-negative integer to indicate which line to stop the MIPS-based just-in-time (JIT) simulator. `--mips-sim-stop-at` CLI option to `jsshell`., js/src/jit/mips32/Simulator-mips32.cpp js/src/jit/mips64/Simulator-mips64.cpp, 
 `MIPS_UNALIGNED`,, js/src/jit/mips64/Simulator-mips64.cpp
 `MOZ_ACCELERATED`,, gfx/thebes/gfxPlatform.cpp
 `MOZ_ANDROID_CPU_ABI`,, modules/libpref/Preferences.cpp
 `MOZ_ANDROID_CRASH_HANDLER`,, toolkit/crashreporter/nsExceptionHandler.cpp
 `MOZ_ANDROID_DEVICE_SDK_VERSION`,, toolkit/crashreporter/nsExceptionHandler.cpp
 `MOZ_ANDROID_LIBDIR_OVERRIDE`,, mozglue/android/APKOpen.cpp
 `MOZ_ANDROID_LIBDIR`,, mozglue/android/APKOpen.cpp xpcom/build/BinaryPath.h
 `MOZ_ANDROID_USER_SERIAL_NUMBER`,, mobile/android/geckoview/src/main/java/org/mozilla/gecko/process/GeckoProcessManager.java toolkit/crashreporter/nsExceptionHandler.cpp
 `MOZ_APP_ALLOW_WINDOWLESS`,, toolkit/components/startup/nsAppStartup.cpp
 `MOZ_APP_LAUNCHER`,, browser/components/shell/nsGNOMEShellService.cpp toolkit/crashreporter/nsExceptionHandler.cpp toolkit/xre/nsNativeAppSupportUnix.cpp
 `MOZ_APP_NO_DOCK`,, widget/cocoa/nsAppShell.mm
 `MOZ_APP_RESTART`,, mozglue/misc/TimeStamp.cpp toolkit/components/startup/nsAppStartup.cpp
 `MOZ_APP_SILENT_START`,, toolkit/components/startup/nsAppStartup.cpp toolkit/xre/nsUpdateDriver.cpp
 `MOZ_BUILDID_MATCH_DONTSEND`,, ipc/glue/MessageChannel.cpp
 `MOZ_BYPASS_CSSOM_ORIGIN_CHECK`,, dom/base/nsContentUtils.cpp
 `MOZ_CAIRO_FORCE_BUGGY_REPEAT`,, gfx/cairo/buggy-repeat.patch
 `MOZ_CC_ALL_TRACES`,, xpcom/base/nsCycleCollector.cpp
 `MOZ_CC_LOG_ALL`,, xpcom/base/nsCycleCollector.cpp
 `MOZ_CC_LOG_DIRECTORY`,, xpcom/base/nsCycleCollector.cpp
 `MOZ_CC_LOG_PROCESS`,, xpcom/base/nsCycleCollector.cpp
 `MOZ_CC_LOG_SHUTDOWN`,, xpcom/base/nsCycleCollector.cpp
 `MOZ_CC_LOG_THREAD`,, xpcom/base/nsCycleCollector.cpp
 `MOZ_CC_RUN_DURING_SHUTDOWN`,, xpcom/build/XPCOMInit.cpp
 `MOZ_CCTIMER`,, dom/base/nsJSEnvironment.cpp
 `MOZ_CHAOSMODE`,, js/xpconnect/src/XPCShellImpl.cpp toolkit/xre/nsAppRunner.cpp
 `MOZ_CONSOLESERVICE_DISABLE_DEBUGGER_OUTPUT`,, xpcom/base/nsConsoleService.cpp
 `MOZ_CRASHREPORTER_AUTO_SUBMIT`,, toolkit/crashreporter/client/crashreporter.cpp
 `MOZ_CRASHREPORTER_DATA_DIRECTORY`,, toolkit/crashreporter/client/crashreporter.cpp
 `MOZ_CRASHREPORTER_DISABLE`,, toolkit/crashreporter/nsExceptionHandler.cpp
 `MOZ_CRASHREPORTER_DUMP_ALL_THREADS`,, toolkit/crashreporter/client/crashreporter.cpp
 `MOZ_CRASHREPORTER_EVENTS_DIRECTORY`,, toolkit/crashreporter/client/crashreporter.cpp
 `MOZ_CRASHREPORTER_FULLDUMP`,, toolkit/crashreporter/nsExceptionHandler.cpp
 `MOZ_CRASHREPORTER_NO_DELETE_DUMP`,, toolkit/crashreporter/client/crashreporter.cpp
 `MOZ_CRASHREPORTER_NO_REPORT`,, toolkit/crashreporter/nsExceptionHandler.cpp
 `MOZ_CRASHREPORTER_PING_DIRECTORY`,, toolkit/crashreporter/client/crashreporter.cpp
 `MOZ_CRASHREPORTER_RESTART_XUL_APP_FILE`,, toolkit/crashreporter/client/crashreporter.cpp
 `MOZ_CRASHREPORTER_STRINGS_OVERRIDE`,, toolkit/crashreporter/client/crashreporter.cpp
 `MOZ_CRASHREPORTER_URL`,, toolkit/crashreporter/client/crashreporter.cpp
 `MOZ_DEBUG_APP_PROCESS`,, dom/ipc/ContentChild.cpp
 `MOZ_DEBUG_BROWSER_PAUSE`,, browser/app/winlauncher/LauncherProcessWin.cpp
 `MOZ_DEBUG_CHILD_PAUSE`,, dom/media/ipc/RDDProcessHost.cpp gfx/ipc/GPUProcessHost.cpp gfx/vr/ipc/VRProcessParent.cpp ipc/glue/MessageChannel.cpp ipc/glue/UtilityProcessHost.cpp toolkit/xre/nsEmbedFunctions.cpp
 `MOZ_DEBUG_CHILD_PROCESS`,, dom/media/ipc/RDDProcessHost.cpp gfx/ipc/GPUProcessHost.cpp gfx/vr/ipc/VRProcessParent.cpp ipc/glue/UtilityProcessHost.cpp toolkit/xre/nsEmbedFunctions.cpp
 `MOZ_DEBUG_PAINTS`,, widget/gtk/nsAppShell.cpp
 `MOZ_DEBUG_SHADERS`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_DEBUG_SOCKET_PROCESS`,, netwerk/ipc/SocketProcessImpl.cpp
 `MOZ_DEFAULT_PREFS`,, modules/libpref/Preferences.cpp
 `MOZ_DESKTOP_FILE_NAME`,, toolkit/system/gnome/nsAlertsIconListener.cpp
 `MOZ_DEVELOPER_REPO_DIR`,, security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp security/sandbox/win/src/sandboxbroker/sandboxBroker.cpp
 `MOZ_DISABLE_ACCESSIBLE_BLOCKLIST`,, accessible/windows/msaa/CompatibilityUIA.cpp accessible/windows/msaa/LazyInstantiator.cpp
 `MOZ_DISABLE_AUTO_SAFE_MODE`,, toolkit/components/startup/nsAppStartup.cpp
 `MOZ_DISABLE_CONTENT_SANDBOX`,, gfx/thebes/gfxFcPlatformFontList.cpp security/sandbox/common/SandboxSettings.cpp security/sandbox/linux/SandboxInfo.cpp
 `MOZ_DISABLE_CONTEXT_SHARING_GLX`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_DISABLE_CRASH_GUARD`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_DISABLE_EXCEPTION_HANDLER_SIGILL`,, toolkit/crashreporter/breakpad-client/linux/handler/exception_handler.cc
 `MOZ_DISABLE_FORCE_PRESENT`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_DISABLE_GMP_SANDBOX`,, dom/media/gmp/GMPLoader.cpp ipc/glue/GeckoChildProcessHost.cpp security/sandbox/linux/SandboxInfo.cpp ipc/glue/GeckoChildProcessHost.cpp
 `MOZ_DISABLE_GMP_SANDBOX`,, ipc/glue/GeckoChildProcessHost.cpp
 `MOZ_DISABLE_MAR_CERT_VERIFICATION`,, taskcluster/docker/funsize-update-generator/scripts/funsize.py
 `MOZ_DISABLE_OOP_TABS`,, dom/base/nsFrameLoader.cpp
 `MOZ_DISABLE_POISON_IO_INTERPOSER`,, xpcom/build/IOInterposer.cpp
 `MOZ_DISABLE_RDD_SANDBOX`,, dom/media/ipc/RDDProcessHost.cpp ipc/glue/GeckoChildProcessHost.cpp security/sandbox/linux/launch/SandboxLaunch.cpp security/sandbox/linux/Sandbox.cpp
 `MOZ_DISABLE_SOCKET_PROCESS_SANDBOX`,, ipc/glue/GeckoChildProcessHost.cpp netwerk/ipc/SocketProcessHost.cpp security/sandbox/common/SandboxSettings.cpp security/sandbox/linux/Sandbox.cpp
 `MOZ_DISABLE_SOCKET_PROCESS`,, netwerk/base/nsIOService.cpp
 `MOZ_DISABLE_UTILITY_SANDBOX`,, ipc/glue/GeckoChildProcessHost.cpp ipc/glue/UtilityProcessHost.cpp security/sandbox/linux/launch/SandboxLaunch.cpp security/sandbox/linux/Sandbox.cpp
 `MOZ_DISABLE_VR_SANDBOX`,, ipc/glue/GeckoChildProcessHost.cpp
 `MOZ_DISABLE_WALKTHESTACK`,, mozglue/misc/StackWalk.cpp
 `MOZ_DMD_LOG_PROCESS`,, xpcom/base/nsTraceRefcnt.cpp
 `MOZ_DMD_SHUTDOWN_LOG`,, xpcom/base/nsTraceRefcnt.cpp
 `MOZ_DONT_UNBLOCK_PARENT_ON_CHILD_CRASH`,, toolkit/xre/nsSigHandlers.cpp
 `MOZ_DRM_DEVICE`,, widget/gtk/DMABufLibWrapper.cpp
 `MOZ_DUMP_AUDIO`,, dom/media/WavDumper.h
 `MOZ_DUMP_COMPOSITOR_TEXTURES`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_DUMP_INVALIDATION`,, layout/base/nsLayoutUtils.h
 `MOZ_DUMP_LAYER_SORT_LIST`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_DUMP_PAINT_INTERMEDIATE`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_DUMP_PAINT_ITEMS`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_DUMP_PAINT_TO_FILE`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_DUMP_PAINT`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_ENABLE_HANDLE_VERIFIER`,, security/sandbox/win/SandboxInitialization.cpp
 `MOZ_ENABLE_WAYLAND`,, toolkit/xre/nsAppRunner.cpp
 `MOZ_FAKE_NO_SANDBOX`,, security/sandbox/linux/SandboxInfo.cpp
 `MOZ_FAKE_NO_SECCOMP_TSYNC`,, security/sandbox/linux/SandboxInfo.cpp
 `MOZ_FATAL_STATIC_XPCOM_CTORS_DTORS`,, xpcom/base/nsTraceRefcnt.cpp
 `MOZ_FORCE_CRASH_GUARD_NIGHTLY`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_FORCE_DISABLE_E10S`,, toolkit/xre/nsAppRunner.cpp
 `MOZ_FORCE_DOUBLE_BUFFERING`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_FORCE_USE_SOCKET_PROCESS`,, netwerk/base/nsIOService.cpp
 `MOZ_FORKSERVER_WAIT_GDB_NEWPROC`,, ipc/glue/ForkServer.cpp
 `MOZ_FORKSERVER_WAIT_GDB`,, ipc/glue/ForkServer.cpp
 `MOZ_FUZZ_CRASH_ON_LARGE_ALLOC`,, js/public/Utility.h
 `MOZ_FUZZ_DEBUG`,, dom/base/nsJSUtils.cpp js/src/shell/js.cpp js/xpconnect/src/XPCShellImpl.cpp
 `MOZ_FUZZ_LARGE_ALLOC_LIMIT`,, js/src/util/Utility.cpp
 `MOZ_FUZZ_LOG`,, tools/fuzzing/interface/FuzzingInterface.cpp
 `MOZ_FUZZ_TESTFILE`,, tools/fuzzing/interface/FuzzingInterface.h tools/fuzzing/interface/FuzzingInterfaceStream.h tools/fuzzing/nyx/Nyx.cpp
 `MOZ_FUZZ_WAIT_BEFORE_REPLAY`,, tools/fuzzing/nyx/Nyx.cpp
 `MOZ_FUZZING_CCOV`,, build/build-clang/fuzzing_ccov_build_clang_12.patch
 `MOZ_FUZZING_SAFE`, alternatively can use `--fuzzing-safe` option by `jsshell`, js/src/shell/js.cpp, 
 `MOZ_GC_LOG_SIZE`,, xpcom/base/CycleCollectedJSRuntime.cpp
 `MOZ_GDB_SLEEP`,, toolkit/xre/nsSigHandlers.cpp
 `MOZ_GDK_DISPLAY`,, dom/ipc/ContentChild.cpp gfx/ipc/GPUParent.cpp
 `MOZ_GFX_CRASH_MOZ_CRASH`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_GFX_CRASH_TELEMETRY`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_GFX_SPOOF_DEVICE_ID`,, widget/windows/GfxInfo.cpp
 `MOZ_GFX_SPOOF_DRIVER_VERSION`,, widget/windows/GfxInfo.cpp
 `MOZ_GFX_SPOOF_GL_RENDERER`,, widget/android/GfxInfo.cpp widget/gtk/GfxInfo.cpp
 `MOZ_GFX_SPOOF_GL_VENDOR`,, widget/android/GfxInfo.cpp widget/gtk/GfxInfo.cpp
 `MOZ_GFX_SPOOF_GL_VERSION`,, widget/android/GfxInfo.cpp widget/gtk/GfxInfo.cpp
 `MOZ_GFX_SPOOF_OS_RELEASE`,, widget/gtk/GfxInfo.cpp
 `MOZ_GFX_SPOOF_OS`,, widget/gtk/GfxInfo.cpp
 `MOZ_GFX_SPOOF_VENDOR_ID`,, widget/windows/GfxInfo.cpp
 `MOZ_GFX_SPOOF_WINDOWS_VERSION`,, widget/windows/GfxInfo.cpp
 `MOZ_GFX_VR_NO_DISTORTION`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_GL_DEBUG_ABORT_ON_ERROR`, Thebes GFX debug, gfx/thebes/gfxEnv.h gfx/gl/GLContext.cpp, 
 `MOZ_GL_DEBUG_VERBOSE`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_GL_DEBUG`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_GL_DUMP_EXTS`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_GL_SPEW`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_GLX_DEBUG`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_GMP_PATH`,, dom/media/gmp/GMPServiceParent.cpp
 `MOZ_GPU_SWITCHING_SPEW`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_GTK_TITLEBAR_DECORATION`,, widget/gtk/nsWindow.cpp
 `MOZ_HEADLESS_HEIGHT`,, widget/headless/HeadlessScreenHelper.cpp
 `MOZ_HEADLESS_WIDTH`,, widget/headless/HeadlessScreenHelper.cpp
 `MOZ_HEADLESS`,, gfx/thebes/gfxPlatform.cpp
 `MOZ_IGNORE_NSS_SHUTDOWN_LEAKS`,, xpcom/build/XPCOMInit.cpp
 `MOZ_IGNORE_WARNINGS`,, xpcom/base/nsDebugImpl.cpp
 `MOZ_INSTALLED_AND_RELAUNCHED_FROM_DMG`,, toolkit/xre/MacRunFromDmgUtils.mm
 `MOZ_INSTRUMENT_EVENT_LOOP_INTERVAL`,, toolkit/xre/EventTracer.cpp
 `MOZ_INSTRUMENT_EVENT_LOOP_OUTPUT`,, toolkit/xre/EventTracer.cpp
 `MOZ_INSTRUMENT_EVENT_LOOP_THRESHOLD`,, toolkit/xre/EventTracer.cpp
 `MOZ_INSTRUMENT_EVENT_LOOP`,, toolkit/xre/nsAppRunner.cpp
 `MOZ_IPC_MESSAGE_LOG`,, ipc/glue/ProtocolUtils.h
 `MOZ_JAR_LOG_FILE`,, modules/libjar/nsZipArchive.cpp
 `MOZ_KILL_CANARIES`,, xpcom/threads/nsThreadManager.cpp
 `MOZ_LAYERS_ALLOW_SOFTWARE_GL`,, widget/gtk/GfxInfo.cpp
 `MOZ_LAYERS_ENABLE_XLIB_SURFACES`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_LAYERS_PREFER_EGL`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_LAYERS_PREFER_OFFSCREEN`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_LINKER_CACHE`,, mozglue/linker/Mappable.cpp
 `MOZ_LINKER_EXTRACT`,, mozglue/linker/ElfLoader.cpp
 `MOZ_LOG_FILE`,, ipc/glue/GeckoChildProcessHost.cpp xpcom/base/Logging.cpp
 `MOZ_LOG_MESSAGEMANAGER_SKIP`,, dom/ipc/MMPrinter.cpp
 `MOZ_LOG_MODULES`,, xpcom/base/Logging.cpp
 `MOZ_LOG`,, security/sandbox/win/src/sandboxbroker/sandboxBroker.cpp xpcom/base/Logging.cpp
 `MOZ_MAIN_THREAD_IO_LOG`,, xpcom/build/MainThreadIOLogger.cpp
 `MOZ_MEM_LIMIT`,, toolkit/xre/nsSigHandlers.cpp
 `MOZ_NO_VR_RENDERING`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_NURSERY_BIGINTS`,, js/src/gc/Nursery.cpp
 `MOZ_NURSERY_STRINGS`,, js/src/gc/Nursery.cpp
 `MOZ_ORIG_LD_PRELOAD`,, security/sandbox/linux/Sandbox.cpp
 `MOZ_PERMISSIVE_CONTENT_SANDBOX`,, security/sandbox/linux/SandboxInfo.cpp
 `MOZ_PROFILER_STARTUP`,, devtools/client/performance-new/test/browser/head.js mozglue/baseprofiler/core/platform.cpp
 `MOZ_PURGE_CACHES`,, toolkit/xre/nsAppRunner.cpp
 `MOZ_REPLACE_MALLOC_LIB`,, memory/build/mozjemalloc.cpp
 `MOZ_REQUIRE_KEYED_MUTEX`,, gfx/gl/SharedSurfaceANGLE.cpp
 `MOZ_RUN_GTEST`,, dom/quota/QuotaManager.h ipc/glue/GeckoChildProcessHost.cpp toolkit/xre/nsAppRunner.cpp toolkit/xre/nsEmbedFunctions.cpp xpcom/glue/standalone/nsXPCOMGlue.cpp
 `MOZ_SANDBOX_ALLOW_SYSV`,, security/sandbox/linux/SandboxFilter.cpp
 `MOZ_SANDBOX_CRASH_ON_ERROR`,, security/sandbox/linux/Sandbox.cpp
 `MOZ_SANDBOX_LOGGING`,, dom/ipc/ContentParent.cpp dom/media/gmp/GMPProcessParent.cpp ipc/glue/GeckoChildProcessHost.cpp security/sandbox/chromium-shim/sandbox/win/loggingCallbacks.h security/sandbox/linux/SandboxInfo.cpp
 `MOZ_SANDBOX_RDD_LOGGING`,, dom/media/ipc/RDDProcessHost.cpp
 `MOZ_SANDBOX_SOCKET_PROCESS_LOGGING`,, netwerk/ipc/SocketProcessHost.cpp
 `MOZ_SANDBOX_USE_CHROOT`,, security/sandbox/linux/Sandbox.cpp
 `MOZ_SANDBOX_UTILITY_LOGGING`,, ipc/glue/UtilityProcessHost.cpp
 `MOZ_SANDBOXED`,, ipc/chromium/src/base/shared_memory_posix.cc security/sandbox/linux/Sandbox.cpp security/sandbox/linux/SandboxReporterClient.cpp
 `MOZ_SEPARATE_CHILD_PROCESS`,, toolkit/xre/nsAppRunner.cpp
 `MOZ_SHM_NO_SEALS`,, ipc/chromium/src/base/shared_memory_posix.cc
 `MOZ_SHMEM_PAGESIZE_16K`,, ipc/glue/SharedMemory_posix.cpp
 `MOZ_SHOW_ALL_JS_FRAMES`,, js/src/vm/FrameIter.cpp
 `MOZ_SKIA_DISABLE_ASSERTS`,, gfx/skia/skia/src/ports/SkMemory_mozalloc.cpp
 `MOZ_SKIPCOMPOSITION`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_SKIPRASTERIZATION`, Thebes GFX debug, gfx/thebes/gfxEnv.h, 
 `MOZ_STARTUP_CACHE`,, startupcache/StartupCache.cpp
 `MOZ_TASKCONTROLLER_THREADCOUNT`,, xpcom/threads/TaskController.cpp
 `MOZ_TIMESTAMP_MODE`,, mozglue/misc/TimeStamp_windows.cpp
 `MOZ_UPLOAD_DIR`,, js/src/gc/Statistics.cpp js/src/util/StructuredSpewer.cpp testing/raptor/raptor/output.py testing/raptor/raptor/perftest.py testing/raptor/raptor/power.py testing/raptor/test/test_power.py testing/talos/talos/ffsetup.py
 `MOZ_USE_XINPUT2`,, toolkit/xre/nsAppRunner.cpp
 `MOZ_WAYLAND_DUMP_DIR`,, widget/gtk/WaylandBuffer.cpp
 `MOZ_WAYLAND_DUMP_WL_BUFFERS`,, widget/gtk/WaylandBuffer.cpp
 `MOZ_WEBGL_DUMP_SHADERS`,, dom/canvas/WebGLShader.cpp
 `MOZ_WEBGL_FORCE_EGL`,, dom/canvas/WebGLContext.cpp
 `MOZ_WEBGL_FORCE_OPENGL`,, dom/canvas/WebGLContext.cpp
 `MOZ_WINDOW_OCCLUSION`,, gfx/thebes/gfxPlatform.cpp
 `MOZ_X_SYNC`,, toolkit/xre/nsGDKErrorHandler.cpp toolkit/xre/nsX11ErrorHandler.cpp
 `MOZ_X11_EGL`,, gfx/thebes/gfxPlatformGtk.cpp
 `MOZSEARCH_PLATFORM`,, build/clang-plugin/mozsearch-plugin/MozsearchIndexer.cpp
 `NECKO_ERRORS_ARE_FATAL`,, netwerk/ipc/NeckoCommon.h
 `NECKO_SOCKET_TRACE_LOG`,, netwerk/base/nsSocketTransport2.cpp
 `NISCC_TEST`,, security/nss/lib/ssl/ssl3con.c
 `NO_AT_BRIDGE`,, accessible/atk/Platform.cpp
 `no_proxy`,, toolkit/system/unixproxy/nsUnixSystemProxySettings.cpp
 `NOTEBOOK_PLUGIN`,, python/mozperftest/mozperftest/metrics/notebook/perftestetl.py
 `NSPR_AIX_SEND_FILE_USE_DISABLED`,, nsprpub/pr/src/md/unix/aix.c
 `NSPR_ATOMIC_HASH_LOCKS`,, nsprpub/pr/src/misc/pratom.c
 `NSPR_ENVIRONMENT_TEST_VARIABLE`, part of `nsprpub` test, nsprpub/tests/env.c, 
 `NSPR_FD_CACHE_SIZE_HIGH`,, nsprpub/pr/src/io/prfdcach.c
 `NSPR_FD_CACHE_SIZE_LOW`,, nsprpub/pr/src/io/prfdcach.c
 `NSPR_INHERIT_FDS`,, nsprpub/pr/src/misc/prinit.c
 `NSPR_LOG_FILE`,, ipc/glue/GeckoChildProcessHost.cpp nsprpub/pr/src/io/prlog.c xpcom/base/Logging.cpp
 `NSPR_LOG_MODULES`,, nsprpub/pr/src/io/prlog.c xpcom/base/Logging.cpp
 `NSPR_NATIVE_THREADS_ONLY`,, nsprpub/pr/src/misc/prinit.c
 `NSPR_NO_MMAP`,, nsprpub/pr/src/md/unix/unix.c
 `NSPR_NOCLOCK`,, nsprpub/pr/src/md/unix/unix.c
 `NSPR_OS2_NO_HIRES_TIMER`, OS2 platform-specific, nsprpub/pr/src/md/os2/os2inrval.c, 
 `NSPR_SIGABRT_HANDLE`,, nsprpub/pr/src/md/unix/unix.c
 `NSPR_SIGBUS_HANDLE`,, nsprpub/pr/src/md/unix/unix.c
 `NSPR_SIGSEGV_HANDLE`,, nsprpub/pr/src/md/unix/unix.c
 `NSPR_TRACE_LOG`,, nsprpub/pr/src/misc/prtrace.c
 `NSPR_USE_ZONE_ALLOCATOR`,, nsprpub/pr/src/malloc/prmem.c
 `NSRANDCOUNT`, An integer byte count that sets the maximum number of bytes to read from the file named in the environment variable `NSRANDFILE`.  Makes `NSRANDFILE` usable with `/dev/urandom`., security/nss/lib/freebl/unix_rand.c, 
 `NSRANDFILE`, filepath specification to the random number device in which to seed the Pseudo Random Number Generator., security/nss/lib/freebl/unix_rand.c, 
 `NSS_ALLOW_WEAK_SIGNATURE_ALG`, if defined to any value then this enables the use of MD2 and MD4 inside signatures. This was allowed by default before NSS 3.12.3., security/nss/lib/util/secoid.c, 
 `NSS_DEBUG_PKCS11_MODULE`, String value of the PKCS#11 module name to be traced.`mozilla _projects_nss_nss_tech _notes_nss_tech_note2`, security/nss/lib/pk11wrap/pk11load.c, 
 `NSS_DEBUG_TIMEOUT`, , security/nss/cmd/strsclnt/strsclnt.c security/nss/cmd/tstclnt/tstclnt.c, 
 `NSS_DEFAULT_DB_TYPE`, A labeled string value to determines the default Database type to open if the app does not specify. The value can be `dbm` or `sql` or `extern`. More details in https://wiki.mozilla.org/NSS_Shared_DB, security/nss/lib/pk11wrap/pk11pars.c security/nss/lib/util/utilpars.c, 
 `NSS_DISABLE_ARENA_FREE_LIST`, Any non-empty string value to start to get accurate leak allocation stacks when using leak reporting software. `mozilla_projects_ nss_memory_allocation`, security/nss/cmd/smimetools/cmsutil.c security/nss/lib/util/secport.c, 
 `NSS_DISABLE_ARM_NEON`,, security/nss/lib/freebl/blinit.c
 `NSS_DISABLE_AVX`,, security/nss/lib/freebl/blinit.c
 `NSS_DISABLE_AVX2`,, security/nss/lib/freebl/blinit.c
 `NSS_DISABLE_HW_AES`,, security/nss/lib/freebl/blinit.c
 `NSS_DISABLE_HW_SHA`,, security/nss/lib/freebl/blinit.c
 `NSS_DISABLE_HW_SHA1`,, security/nss/lib/freebl/blinit.c
 `NSS_DISABLE_HW_SHA2`,, security/nss/lib/freebl/blinit.c
 `NSS_DISABLE_PCLMUL`,, security/nss/lib/freebl/blinit.c
 `NSS_DISABLE_PMULL`,, security/nss/lib/freebl/blinit.c
 `NSS_DISABLE_PPC_GHASH`,, security/nss/lib/freebl/blinit.c
 `NSS_DISABLE_SSE4_1`,, security/nss/lib/freebl/blinit.c
 `NSS_DISABLE_SSE4_2`,, security/nss/lib/freebl/blinit.c
 `NSS_DISABLE_SSSE3`,, security/nss/lib/freebl/blinit.c
 `NSS_DISABLE_UNLOAD`, If set to any non-empty string value then it starts to disable the unloading of dynamically loaded NSS shared libraries during shutdown. Necessary on some platforms to get correct function names when using leak reporting software., security/nss/cmd/pk11mode/pk11mode.c security/nss/cmd/pk11util/pk11util.c security/nss/cmd/shlibsign/shlibsign.c security/nss/lib/freebl/loader.c security/nss/lib/pk11wrap/pk11load.c security/nss/lib/softoken/legacydb/lginit.c security/nss/lib/softoken/lgglue.c, 
 `NSS_ENABLE_AUDIT`, If set to `1` then this enables auditing of activities of the NSS cryptographic module in FIPS mode. See https://wiki.mozilla.org/FIPS_Operational_Environment, security/nss/lib/softoken/fipstokn.c, 
 `NSS_ENABLE_PKIX_VERIFY`, If set to any non-empty string value then it starts to use `libPKIX` rather than the old cert library to verify certificates., security/nss/lib/nss/nssinit.c, 
 `NSS_FIPS`, If set to `true` or `on` or `1` then it starts to use `NSS` in FIPS mode., security/nss/lib/sysinit/nsssysinit.c, 
 `NSS_FORCE_TOKEN_LOCK`, , security/nss/lib/pk11wrap/pk11load.c, 
 `NSS_HASH_ALG_SUPPORT`, A string value that specifies algorithms allowed to be used in certain applications, such as in signatures on certificates and CRLs. See https://bugzilla.mozilla.org/show_bug.cgi?id=483113#c0, security/nss/lib/util/secoid.c, 
 `NSS_IGNORE_SYSTEM_POLICY`,, security/nss/lib/nss/nssinit.c
 `NSS_MAX_MP_PBE_ITERATION_COUNT`,, security/nss/lib/softoken/sftkpwd.c
 `NSS_MIN_MP_PBE_ITERATION_COUNT`,, security/nss/lib/softoken/sftkpwd.c
 `NSS_OUTPUT_FILE`, Filepath specification to an output file for the `mozilla_ projects_nss_nss_tech_ notes_nss_tech_note2`. Default is `stdout`., security/nss/lib/pk11wrap/debug_module.c, 
 `NSS_POLICY_FAIL`,, If set to `no` or `yes` or `auto` then it changes the controls of whether NSS uses a local cache of SQL database contents. Default is “auto”.security/nss/cmd/nss-policy-check/nss-policy-check.c
 `NSS_POLICY_LOADED`,, security/nss/cmd/nss-policy-check/nss-policy-check.c
 `NSS_POLICY_WARN`,, security/nss/cmd/nss-policy-check/nss-policy-check.c
 `NSS_SDB_USE_CACHE`,, security/manager/ssl/nsNSSComponent.cpp
 `NSS_SSL_CBC_RANDOM_IV`, Controls the workaround for the BEAST attack on SSL 3.0 and TLS 1.0. `0` disables it, `1` enables it. It is also known as 1/n-1 record splitting. Default is `1`., security/nss/lib/ssl/sslsock.c, 
 `NSS_SSL_ENABLE_RENEGOTIATION`, See https://firefox-source-docs.mozilla.org/security/nss/legacy/reference/nss_environment_variables/index.html, security/nss/lib/ssl/sslsock.c, 
 `NSS_SSL_REQUIRE_SAFE_NEGOTIATION`, If set to `1` then it enables the safe renegotiation indication for initial handshake. In other words a connection will be dropped at initial handshake if a server or client do not support safe renegotiation. The default setting for this option is FALSE., security/nss/lib/ssl/sslsock.c, 
 `NSS_SSL_SERVER_CACHE_MUTEX_TIMEOUT`, Timeout time to detect dead or hung process in multi-process SSL server. Default is 30 seconds., security/nss/lib/ssl/sslsnce.c, 
 `NSS_STRICT_NOFORK`,, security/nss/lib/softoken/softoken.h
 `NSS_STRICT_SHUTDOWN`, If set to any non-empty string value then will trigger an assertion failure in debug builds when a program tries to shutdown NSS before freeing all the resources it acquired from NSS while NSS was initialized., security/nss/cmd/smimetools/cmsutil.c security/nss/lib/libpkix/pkix_pl_nss/system/pkix_pl_lifecycle.c security/nss/lib/pk11wrap/pk11util.c, 
 `NSS_TRACE_OCSP`, If set to any non-empty string value then it enables OCSP tracing. The trace information is written to the file pointed by `NSPR_LOG_FILE`. Default is `stderr`., security/nss/lib/certhigh/ocsp.c, 
 `NSS_USE_DECODED_CKA_EC_POINT`, If set to any non-empty string value then it tells NSS to send EC key points across the PKCS#11 interface in the non-standard unencoded format that was used by default before NSS 3.12.3., security/nss/lib/pk11wrap/pk11akey.c security/nss/lib/softoken/legacydb/lgattr.c security/nss/lib/softoken/pkcs11c.c, 
 `NSS_USE_SHEXP_IN_CERT_NAME`, If set to any non-empty string value then it tells NSS to allow shell-style wildcard patterns in certificates to match SSL server host names. This behavior was the default before NSS 3.12.3., security/nss/lib/certdb/certdb.c, 
 `NYX_FUZZER`,, tools/fuzzing/nyx/Nyx.cpp
 `OPT_LEVEL`,, third_party/rust/cc/src/lib.rs
 `OVR_LIB_NAME`,, gfx/vr/service/OculusSession.cpp gfx/vr/service/OculusSession.cpp
 `OVR_LIB_PATH`,, gfx/vr/service/OculusSession.cpp
 `PATH`,, js/src/ctypes/libffi/ltmain.sh js/src/gdb/mozilla/IonGraph.py js/src/tests/shell/os.js modules/freetype2/builds/unix/ltmain.sh nsprpub/pr/tests/foreign.c nsprpub/pr/tests/lazyinit.c toolkit/xre/nsWindowsWMain.cpp uriloader/exthandler/unix/nsOSHelperAppService.cpp xpcom/build/BinaryPath.h
 `PDS_NAME_PREFIX`,, intl/icu/source/tools/pkgdata/pkgdata.cpp
 `PERF_SPEW_DIR`,, js/src/jit/PerfSpewer.cpp
 `PIXMAN_DISABLE`,, gfx/cairo/libpixman/src/pixman-implementation.c
 `PKIX_OBJECT_LEAK_TEST_ABORT_ON_LEAK`, If set to any non-empty string value then it output-debug variables for PKIX leak checking. Note: The code must be built with PKIX_OBJECT_LEAK_TEST defined to use this functionality., security/nss/lib/certhigh/certvfypkix.c, 
 `PLAIN_LIST`,, gfx/harfbuzz/src/gen-def.py
 `ProgramFiles`,, dom/media/platforms/wmf/WMFUtils.cpp
 `ProgramW6432`,, dom/media/platforms/wmf/WMFUtils.cpp
 `PWD`,, widget/nsPrinterListCUPS.cpp widget/nsPrintSettingsImpl.cpp
 `QEMU_EMULATING`,, security/nss/lib/freebl/blinit.c
 `R_LOG_DESTINATION`,, dom/media/webrtc/transport/third_party/nrappkit/src/log/r_log.c
 `R_LOG_LEVEL`,, dom/media/webrtc/transport/third_party/nrappkit/src/log/r_log.c
 `R_LOG_VERBOSE`,, dom/media/webrtc/transport/third_party/nrappkit/src/log/r_log.c
 `RENDERDOC_CAPTUREOPTS`,, security/sandbox/linux/launch/SandboxLaunch.cpp security/sandbox/linux/SandboxFilter.cpp
 `RUST_LOG_CHILD`,, ipc/glue/GeckoChildProcessHost.cpp
 `RUST_LOG`,, ipc/glue/GeckoChildProcessHost.cpp
 `SESSION_MANAGER`,, toolkit/xre/nsNativeAppSupportUnix.cpp
 `SHM_ID`,, js/src/shell/js.cpp
 `SHMEM_FUZZER_ENABLE_LOGGING`,, tools/fuzzing/shmem/SharedMemoryFuzzer.cpp
 `SHMEM_FUZZER_ENABLE`,, tools/fuzzing/shmem/SharedMemoryFuzzer.cpp
 `SHMEM_FUZZER_MUTATION_FACTOR`,, tools/fuzzing/shmem/SharedMemoryFuzzer.cpp
 `SHMEM_FUZZER_MUTATION_PROBABILITY`,, tools/fuzzing/shmem/SharedMemoryFuzzer.cpp
 `SIGNTOOL_DUMP_PARSE`,, security/nss/cmd/signtool/javascript.c
 `SMOOSH_BENCH_AS_JSON`,, third_party/rust/jsparagus/benchmarks/compare-spidermonkey-parsers.js
 `SNAP_DESKTOP_RUNTIME`,, security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp
 `SNAP_INSTANCE_NAME`,, widget/gtk/WidgetUtilsGtk.cpp
 `SNAP_NAME`,, widget/gtk/WidgetUtilsGtk.cpp
 `SOCKETTRACE`, If set to `1` then it enables the control tracing of socket activity by `libPKIX`. Messages sent and received will be timestamped and dumped (to `stdout`) in standard hex-dump format., security/nss/lib/libpkix/pkix_pl_nss/module/pkix_pl_socket.c, 
 `SPEW_FILE`,, js/src/util/StructuredSpewer.cpp
 `SPEW_FILTER`,, js/src/util/StructuredSpewer.cpp
 `SPEW`,, js/src/util/StructuredSpewer.h
 `SQLITE_FORCE_PROXY_LOCKING`, If set to `1` then it means to force always use proxy; `0` means to never use proxy, `NULL` means use proxy for non-local files only., security/nss/lib/sqlite/sqlite3.c third_party/rust/libsqlite3-sys/sqlcipher/sqlite3.c third_party/rust/libsqlite3-sys/sqlite3/sqlite3.c third_party/sqlite3/src/sqlite3.c, 
 `SQLITE_FORCE_PROXY_LOCKING`,, security/nss/lib/sqlite/sqlite3.c third_party/rust/libsqlite3-sys/sqlcipher/sqlite3.c third_party/rust/libsqlite3-sys/sqlite3/sqlite3.c third_party/sqlite3/src/sqlite3.c
 `SQLITE_TMPDIR`,, security/nss/lib/sqlite/sqlite3.c third_party/rust/libsqlite3-sys/sqlcipher/sqlite3.c third_party/rust/libsqlite3-sys/sqlite3/sqlite3.c third_party/sqlite3/src/sqlite3.c
 `SSH_CLIENT`,, python/mozbuild/mozbuild/telemetry.py
 `SSL_DIR`,, security/nss/cmd/lib/secutil.c security/nss/cmd/lib/secutil.h
 `SSLBYPASS`,, Uses PKCS#11 bypass for performance improvement. Do not set this variable if FIPS is enabled.
 `SSLDEBUG`, An integer value to denote the severity level of its debug output. Note: The code must be built with DEBUG macro defined to use this functionality., security/nss/lib/ssl/sslsock.c, 
 `SSLFORCELOCKS`, Forces NSS to use locks for protection. Overrides the effect of SSL_NO_LOCKS (see ssl.h)., security/nss/lib/ssl/sslsock.c, 
 `START_AT`,, security/nss/lib/ssl/ssl3con.c
 `STOP_AT`,, security/nss/lib/ssl/ssl3con.c
 `SU_SPIES_DIRECTORY`,, gfx/gl/GLContextProviderWGL.cpp
 `TARGET`,, third_party/rust/cc/src/lib.rs
 `TERM_PROGRAM`,, python/mozbuild/mozbuild/telemetry.py
 `TLDIR`,, js/src/vm/TraceLoggingGraph.cpp
 `TLLOG`,, js/src/vm/TraceLogging.cpp
 `TLOPTIONS`,, js/src/vm/TraceLogging.cpp
 `tmp`,, js/src/devtools/automation/autospider.py toolkit/crashreporter/nsExceptionHandler.cpp tools/crashreporter/injector/injector.cc tools/fuzzing/libfuzzer/FuzzerIOPosix.cpp xpcom/io/SpecialSystemDirectory.cpp
 `TMP`,, security/nss/cmd/httpserv/httpserv.c security/nss/cmd/selfserv/selfserv.c security/nss/lib/dbm/src/h_page.c security/nss/lib/sqlite/sqlite3.c third_party/rust/libsqlite3-sys/sqlcipher/sqlite3.c third_party/rust/libsqlite3-sys/sqlite3/sqlite3.c third_party/sqlite3/src/sqlite3.c xpcom/io/SpecialSystemDirectory.cpp
 `TQDM_DISCORD_CHANNEL_ID`,, third_party/python/tqdm/tqdm/contrib/bells.py third_party/python/tqdm/tqdm/contrib/discord.py
 `TQDM_DISCORD_TOKEN`,, third_party/python/tqdm/tqdm/contrib/discord.py
 `TQDM_TELEGRAM_CHAT_ID`,, third_party/python/tqdm/tqdm/contrib/bells.py
 `TYPECACHE`,, js/src/devtools/rootAnalysis/analyzeHeapWrites.js
 `TZDIR`,, third_party/libwebrtc/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_info.cc
 `TZFILE`,, intl/icu/source/common/putil.cpp
 `U_FAKETIME_START`,, intl/icu/source/common/putil.cpp
 `U_RBBIDEBUG`,, intl/icu/source/common/rbbi.cpp intl/icu/source/common/rbbidata.cpp intl/icu/source/common/rbbirb.cpp
 `UPLOAD_DIR`,, build/build-clang/build-clang.py
 `USE_DEBUGGER`,, js/src/jit/arm64/vixl/MozSimulator-vixl.cpp
 `USEARCH_DEBUG`,, intl/icu/source/i18n/usearch.cpp
 `USERNAME`,, uriloader/exthandler/nsExternalHelperAppService.cpp
 `VGL_ISACTIVE`,, security/sandbox/linux/launch/SandboxLaunch.cpp
 `VIXL_STATS`,, js/src/jit/arm64/vixl/MozSimulator-vixl.cpp
 `VIXL_TRACE`,, js/src/jit/arm64/vixl/MozSimulator-vixl.cpp
 `VPX_SIMD_CAPS_MASK`,, media/libvpx/libvpx/vpx_ports/arm_cpudetect.c media/libvpx/libvpx/vpx_ports/ppc_cpudetect.c media/libvpx/libvpx/vpx_ports/x86.h
 `VPX_SIMD_CAPS`,, media/libvpx/libvpx/vpx_ports/arm_cpudetect.c media/libvpx/libvpx/vpx_ports/ppc_cpudetect.c media/libvpx/libvpx/vpx_ports/x86.h
 `VR_PATHREG_OVERRIDE`,, gfx/vr/service/openvr/src/vrpathregistry_public.cpp
 `WAYLAND_DISPLAY`,, gfx/angle/checkout/src/libANGLE/renderer/driver_utils.cpp third_party/libwebrtc/modules/desktop_capture/desktop_capturer.cc toolkit/xre/nsAppRunner.cpp widget/gtk/GfxInfo.cpp
 `wayland`,, gfx/angle/checkout/src/libANGLE/renderer/driver_utils.cpp
 `WR_RESOURCE_PATH`,, gfx/thebes/gfxPlatform.cpp
 `WRENCH_HEADLESS_TARGET`,, gfx/wr/wrench/script/headless.py
 `XAUTHORITY`,, security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp
 `XDG_CACHE_HOME`,, dom/ipc/ContentChild.cpp third_party/rust/glslopt/glsl-optimizer/src/util/disk_cache.c toolkit/xre/nsXREDirProvider.cpp third_party/python/setuptools/pkg_resources/\_vendor/appdirs.py third_party/python/pip/pip/\_vendor/appdirs.py third_party/python/appdirs/appdirs.py
 `XDG_CONFIG_DIRS`,, security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp third_party/python/appdirs/appdirs.py third_party/python/pip/pip/\_vendor/appdirs.py third_party/python/setuptools/pkg_resources/\_vendor/appdirs.py
 `XDG_CONFIG_HOME`,, dom/ipc/ContentChild.cpp gfx/vr/service/openvr/src/vrpathregistry_public.cpp security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp security/sandbox/test/browser_content_sandbox_fs_tests.js security/sandbox/test/browser_content_sandbox_fs_xdg.js xpcom/io/SpecialSystemDirectory.cpp
 `XDG_CURRENT_DESKTOP`,, browser/components/shell/nsGNOMEShellService.cpp intl/locale/gtk/OSPreferences_gtk.cpp widget/gtk/GfxInfo.cpp widget/gtk/nsLookAndFeel.cpp widget/gtk/nsWindow.cpp widget/gtk/ScreenHelperGTK.cpp
 `XDG_RUNTIME_DIR`,, dom/ipc/ContentChild.cpp
 `XMODIFIERS`,, widget/gtk/IMContextWrapper.cpp
 `XPCOM_DEBUG_BREAK`,, xpcom/base/nsDebugImpl.cpp
 `XPCOM_DEBUG_DLG`,, xpcom/base/nsDebugImpl.cpp
 `XPCOM_MEM_COMPTR_LOG`,, xpcom/base/nsTraceRefcnt.cpp xpcom/build/XPCOMInit.cpp
 `XPCOM_MEM_LEAK_LOG`,, xpcom/base/nsMacUtilsImpl.cpp xpcom/build/XPCOMInit.cpp
 `XPCOM_MEM_LOG_CLASSES`,, xpcom/base/nsTraceRefcnt.cpp
 `XPCOM_MEM_LOG_JS_STACK`,, xpcom/base/nsTraceRefcnt.cpp
 `XPCOM_MEM_LOG_OBJECTS`,, xpcom/base/nsTraceRefcnt.cpp
 `XRE_CONSOLE_LOG`,, toolkit/xre/nsConsoleWriter.cpp
 `XRE_MAIN_BREAK`,, toolkit/xre/nsAppRunner.cpp
 `XRE_NO_DLL_READAHEAD`,, toolkit/xre/nsAppRunner.cpp
 `XRE_NO_WINDOWS_CRASH_DIALOG`, Windows XP-specific, js/src/shell/js.cpp toolkit/xre/nsAppRunner.cpp toolkit/xre/nsSigHandlers.cpp, 
 `XUL_APP_FILE`,, browser/app/nsBrowserApp.cpp toolkit/crashreporter/nsExceptionHandler.cpp xpcom/base/AppShutdown.cpp toolkit/xre/nsAppRunner.cpp
 `YYDEBUG`,, security/nss/cmd/modutil/installparse.c
[/jtable]

[jtable]
environment variable name, descrption, source files
 `BUILD_AR`, filepath specification to the `ar` archive binary executable file for WebRTC library, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `BUILD_CC`, filepath specification to the `cc` compiler binary executable file for WebRTC library, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `BUILD_CFLAGS`, compiler options for C (`cc`) compiler for WebRTC library, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `BUILD_CPPFLAGS`, pre-processing compiler options for `cpp` preprocessor for WebRTC library, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `BUILD_CXX`, filepath specification to the `c++` compiler binary executable file for WebRTC library, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `BUILD_CXXFLAGS`, compiler options for C++ (`c++`) compiler for WebRTC library, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `BUILD_LDFLAGS`, link options for linker (`ld`) for WebRTC library, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `BUILD_NM`, filepath specification to the `nm` list symbol binary executable file for WebRTC library, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `BUILD_OPT`,, Do an optimized (not DEBUG) build. Default is to do a DEBUG build.
 `builddir`, directory path specification to the Python build area for HarfBuzz text shaping library, gfx/harfbuzz/src/check-static-inits gfx/harfbuzz/src/check-symbols.py
 `CC`, filepath specification to the `cc` compiler binary executable file for WebRTC library, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `CFLAGS`, compiler options for C (`cc`) compiler for WebRTC library, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `CPPFLAGS`, pre-processing compiler options for `cpp` preprocessor for WebRTC library, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `CXX`, filepath specification to the `c++` compiler binary executable file for WebRTC library, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `CXXFLAGS`, compiler options for C++ (`c++`) compiler for WebRTC library, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `DISTUTILS_USE_SDK`, if defined then distutils user has made an explicit override not to use the default Microsoft Visual C toolkit. Only for Windows platforms and only used by Python `distutils`., third_party/python/setuptools/setuptools/\_distutils/_msvccompiler.py
 `DOMSUF`,, security/nss/mach
 `FORCE_MAC_SDK_MIN`,, third_party/libwebrtc/build/config/mac/mac_sdk_overrides.gni
 `HOST`,, security/nss/mach
 `LDFLAGS`,, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn
 `libs`,, gfx/harfbuzz/src/check-libstdc++.py gfx/harfbuzz/src/check-symbols.py
 `MOZ_DEBUG_FLAGS`, When MOZ_DEBUG_SYMBOLS is set;  you may use MOZ_DEBUG_FLAGS to specify alternative compiler flags to produce symbolic debugging information in a particular format.,, 
 `MOZ_DEBUG_LINKER`,, mozglue/linker/Logging.h
 `MOZ_DEBUG_SYMBOLS`,, Needed on Windows to build with versions of MSVC (such as VC8 and VC9) that do not understand /PDB:NONE
 `MOZ_NO_GLOBAL_MOUSE_MONITOR`,, widget/cocoa/nsToolkit.mm
 `MOZBUILD_STATE_PATH`,, mobile/android/gradle/with_gecko_binaries.gradle
 `MOZILLABUILD`,, python/mozboot/bin/bootstrap.py
 `NM`,, third_party/libwebrtc/build/toolchain/linux/unbundle/BUILD.gn gfx/harfbuzz/src/check-symbols.py
 `OBJDUMP`,, gfx/harfbuzz/src/check-static-inits.py
[/jtable]

[jtable]
environment variable name, descrption, source files
 `DMD`, Only available if `MOZ_PROFILING` macro is defined during build compiling of toolset within Mozilla Unified repository, memory/replace/dmd/DMD.cpp
 `JARLOG_FILE`,, build/pgo/profileserver.py
 `JPROF_FLAGS`,, tools/jprof/stub/libmalloc.cpp
 `JPROF_ISCHILD`,, tools/jprof/stub/libmalloc.cpp
 `MOZ_BACKGROUNDTASKS_PURGE_STALE_PROFILES`,, toolkit/components/backgroundtasks/BackgroundTasks.cpp
 `MOZ_BASE_PROFILER_DEBUG_LOGGING`,, mozglue/baseprofiler/core/platform.cpp
 `MOZ_BASE_PROFILER_HELP`,, mozglue/baseprofiler/core/platform.cpp
 `MOZ_BASE_PROFILER_LOGGING`,, mozglue/baseprofiler/core/platform.cpp
 `MOZ_BASE_PROFILER_VERBOSE_LOGGING`,, mozglue/baseprofiler/core/platform.cpp
 `MOZ_DISABLE_SIG_HANDLER`,, toolkit/profile/nsProfileLock.cpp
 `MOZ_LEGACY_PROFILES`,, toolkit/profile/nsToolkitProfileService.cpp
 `MOZ_LOG_UNKNOWN_TRACE_EVENT_PHASES`,, tools/profiler/core/MicroGeckoProfiler.cpp
 `MOZ_PROFILE_PERF_FLAGS`,, js/src/builtin/Profilers.cpp
 `MOZ_PROFILE_WITH_PERF`,, js/src/builtin/Profilers.cpp
 `MOZ_PROFILER_HELP`,, tools/profiler/core/platform.cpp
 `MOZ_PROFILER_LUL_TEST`,, mozglue/baseprofiler/core/platform-linux-android.cpp tools/profiler/core/platform-linux-android.cpp
 `MOZ_PROFILER_RECORD_OVERHEADS`,, mozglue/baseprofiler/core/ProfileBuffer.cpp tools/profiler/core/ProfileBuffer.cpp
 `MOZ_PROFILER_STARTUP_ACTIVE_TAB_ID`,, tools/profiler/core/platform.cpp
 `MOZ_PROFILER_STARTUP_DURATION`,, mozglue/baseprofiler/core/platform.cpp tools/profiler/core/platform.cpp
 `MOZ_PROFILER_STARTUP_ENTRIES`,, mozglue/baseprofiler/core/platform.cpp tools/profiler/core/platform.cpp
 `MOZ_PROFILER_STARTUP_FEATURES_BITFIELD`,, mozglue/baseprofiler/core/platform.cpp tools/profiler/core/platform.cpp
 `MOZ_PROFILER_STARTUP_FEATURES`,, mozglue/baseprofiler/core/platform.cpp tools/profiler/core/platform.cpp
 `MOZ_PROFILER_STARTUP_FILTERS`,, mozglue/baseprofiler/core/platform.cpp tools/profiler/core/platform.cpp
 `MOZ_PROFILER_STARTUP_INTERVAL`,, mozglue/baseprofiler/core/platform.cpp tools/profiler/core/platform.cpp
 `MOZ_PROFILER_STARTUP_NO_BASE`,, mozglue/baseprofiler/core/platform.cpp tools/profiler/core/platform.cpp
 `MOZ_PROFILER_STARTUP`,, tools/profiler/core/platform.cpp
 `MOZ_PROFILER_SYMBOLICATE`,, mozglue/baseprofiler/core/ProfileBufferEntry.cpp tools/profiler/core/platform.cpp
 `MOZ_UPROFILER_LOG_THREAD_CREATION`,, tools/profiler/public/MicroGeckoProfiler.h
 `SMOOSH_BENCH_AS_JSON`,, third_party/rust/jsparagus/benchmarks/compare-spidermonkey-parsers.js
 `XPCOM_MEM_BLOAT_LOG`,, security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp tools/profiler/core/memory_hooks.cpp tools/profiler/core/platform.cpp xpcom/base/IntentionalCrash.h xpcom/base/nsMacUtilsImpl.cpp xpcom/ds/nsAtomTable.cpp
 `XRE_PROFILE_PATH`,, toolkit/components/startup/nsAppStartup.cpp
[/jtable]

[jtable]
environment variable name, descrption, source files
 `AUTOCONFIG_TEST_GETENV`,, extensions/pref/autoconfig/test/unit/autoconfig-all.cfg extensions/pref/autoconfig/test/unit/test_autoconfig.js
 `bindir`,, toolkit/crashreporter/breakpad-client/linux/minidump_writer/minidump_writer_unittest_utils.cc
 `CUBEB_BACKEND`,, media/libcubeb/test/common.h third_party/rust/cubeb-sys/libcubeb/test/common.h
 `DEBUG_GTEST_OUTPUT_TEST`,, security/nss/gtests/google_test/gtest/test/googletest-output-test.py
 `DISPLAY`,, dom/ipc/ContentChild.cpp gfx/ipc/GPUParent.cpp security/sandbox/common/test/SandboxTestingChildTests.h security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp security/sandbox/linux/launch/SandboxLaunch.cpp toolkit/xre/nsAppRunner.cpp
 `EC_TEST_SEED`,, third_party/aom/test/ec_test.cc
 `EVENT_DEBUG_LOGGING_ALL`,, ipc/chromium/src/third_party/libevent/sample/http-server.c ipc/chromium/src/third_party/libevent/test/regress_main.c ipc/chromium/src/third_party/libevent/test/test-time.c
 `EVENT_DEBUG_MODE`,, ipc/chromium/src/third_party/libevent/test/regress_main.c
 `EVENT_NO_DEBUG_LOCKS`,, ipc/chromium/src/third_party/libevent/test/regress_main.c
 `EVENT_NO_FILE_BUFFERING`,, ipc/chromium/src/third_party/libevent/test/regress_main.c
 `EVENT_NOWAFFLES`,, ipc/chromium/src/third_party/libevent/test/regress.c
 `FREETYPE_TESTS_DATA_DIR`,, modules/freetype2/tests/issue-1063/main.c
 `FUZZER`,, browser/app/nsBrowserApp.cpp js/src/fuzz-tests/tests.cpp js/src/shell/js.cpp js/src/shell/jsrtfuzzing/jsrtfuzzing.cpp js/xpconnect/src/xpcrtfuzzing/xpcrtfuzzing.cpp js/xpconnect/src/XPCShellImpl.cpp toolkit/xre/nsAppRunner.cpp tools/fuzzing/interface/harness/FuzzerRunner.cpp xpcom/glue/standalone/nsXPCOMGlue.cpp
 `GCOV_PREFIX`,, testing/talos/talos/ffsetup.py
 `GTEST_SHARD_INDEX`,, third_party/aom/third_party/googletest/src/googletest/src/gtest.cc
 `GTEST_SHARD_STATUS_FILE`,, third_party/aom/third_party/googletest/src/googletest/src/gtest.cc
 `GTEST_TOTAL_SHARDS`,, third_party/aom/third_party/googletest/src/googletest/src/gtest.cc
 `HOME`,, browser/components/shell/nsGNOMEShellService.cpp security/nss/cmd/lib/secutil.c security/nss/cmd/signtool/util.c security/nss/gtests/sysinit_gtest/getUserDB_unittest.cc security/nss/lib/sysinit/nsssysinit.c security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp security/sandbox/mac/Sandbox.mm testing/mozbase/mozproxy/mozproxy/backends/mitm/android.py testing/mozbase/mozproxy/mozproxy/backends/mitm/desktop.py toolkit/crashreporter/client/crashreporter_gtk_common.cpp toolkit/xre/nsAppRunner.cpp toolkit/xre/nsXREDirProvider.cpp widget/nsPrinterListCUPS.cpp widget/nsPrintSettingsImpl.cpp xpcom/io/nsAppFileLocationProvider.cpp xpcom/io/SpecialSystemDirectory.cpp
 `HOMEDRIVE`,, testing/mozbase/mozproxy/mozproxy/backends/mitm/android.py testing/mozbase/mozproxy/mozproxy/backends/mitm/desktop.py xpcom/io/SpecialSystemDirectory.cpp
 `HOMEPATH`,, testing/mozbase/mozproxy/mozproxy/backends/mitm/android.py testing/mozbase/mozproxy/mozproxy/backends/mitm/desktop.py xpcom/io/SpecialSystemDirectory.cpp
 `HYPOTHESIS_PROFILE`,, testing/web-platform/tests/tools/conftest.py
 `JS_CODE_COVERAGE_OUTPUT_DIR`,, js/src/jit-test/tests/coverage/lcov-enabled-2.js js/src/vm/CodeCoverage.cpp tools/code-coverage/CodeCoverageHandler.cpp testing/talos/talos/ffsetup.py
 `JS_RECORD_RESULTS`,, js/src/tests/non262/extensions/clone-v1-typed-array.js
 `JS_TRACE_LOGGING`,, devtools/client/performance-new/store/actions.js devtools/client/performance-new/test/browser/browser_aboutprofiling-env-restart-button.js js/src/vm/TraceLogging.cpp
 `LD_LIBRARY_PATH`,, ipc/glue/GeckoChildProcessHost.cpp media/libyuv/libyuv/tools_libyuv/valgrind/chrome_tests.py nsprpub/pr/src/linking/prlink.c nsprpub/pr/tests/ipv6.c security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp
 `LDAP`,, security/nss/cmd/libpkix/pkix/top/test_validatechain_NB.c
 `LIBAOM_TEST_DATA_PATH`,, third_party/aom/test/decode_perf_test.cc third_party/aom/test/video_source.h
 `LIBVPX_TEST_DATA_PATH`,, media/libvpx/libvpx/test/decode_perf_test.cc media/libvpx/libvpx/test/video_source.h
 `LIBYUV_CPU_INFO`,, media/libyuv/libyuv/unit_test/unit_test.cc
 `LIBYUV_FLAGS`,, media/libyuv/libyuv/unit_test/unit_test.cc
 `LIBYUV_HEIGHT`,, media/libyuv/libyuv/unit_test/unit_test.cc
 `LIBYUV_REPEAT`,, media/libyuv/libyuv/unit_test/unit_test.cc
 `LIBYUV_WIDTH`,, media/libyuv/libyuv/unit_test/unit_test.cc
 `LOGGING`,, security/nss/cmd/libpkix/pkix/top/test_validatechain_NB.c
 `MOZ_ASSUME_NODE_RUNNING`,, testing/xpcshell/runxpcshelltests.py
 `MOZ_AUTOMATION`,, tools/fuzzing/smoke/test_grizzly.py python/mozrelease/mozrelease/partner_repack.py
 `MOZ_AVOID_OPENGL_ALTOGETHER`,, toolkit/xre/glxtest.cpp
 `MOZ_CRASHREPORTER_SHUTDOWN`,, mobile/android/geckoview/src/androidTest/java/org/mozilla/geckoview/test/util/Environment.java mobile/android/test_runner/src/main/java/org/mozilla/geckoview/test_runner/TestRunnerActivity.java netwerk/ipc/SocketProcessParent.cpp
 `MOZ_CRASHREPORTER`,, testing/gtest/mozilla/GTestRunner.cpp toolkit/crashreporter/nsExceptionHandler.cpp
 `MOZ_DISABLE_NONLOCAL_CONNECTIONS`,, dom/media/webrtc/transport/test/gtest_utils.h  js/xpconnect/src/nsXPConnect.cpp
 `MOZ_DISABLE_STACK_FIX`,, testing/mozbase/mozrunner/mozrunner/utils.py
 `MOZ_FETCHES_DIR`,, testing/xpcshell/runxpcshelltests.py testing/xpcshell/runxpcshelltests.py
 `MOZ_FORCE_ENABLE_FISSION`,, mobile/android/geckoview/src/androidTest/java/org/mozilla/geckoview/test/util/Environment.java
 `MOZ_GTEST_CWD`,, testing/gtest/mozilla/GTestRunner.cpp
 `MOZ_GTEST_LOG_PATH`,, testing/gtest/mozilla/GTestRunner.cpp
 `MOZ_GTEST_MINIDUMPS_PATH`,, testing/gtest/mozilla/GTestRunner.cpp
 `MOZ_IN_AUTOMATION`,, mobile/android/geckoview/src/androidTest/java/org/mozilla/geckoview/test/util/Environment.java
 `MOZ_IPC_MESSAGE_FUZZ_BLACKLIST`,, dom/ipc/fuzztest/content_parent_ipc_libfuzz.cpp gfx/layers/ipc/fuzztest/compositor_manager_parent_ipc_libfuzz.cpp
 `MOZ_NODE_PATH`,, testing/xpcshell/runxpcshelltests.py
 `MOZ_PROFILER_SHUTDOWN`,, devtools/client/performance-new/test/browser/head.js mozglue/baseprofiler/core/platform.cpp tools/profiler/core/platform.cpp
 `MOZ_PROFILER_STARTUP`,, devtools/client/performance-new/test/browser/head.js mozglue/baseprofiler/core/platform.cpp
 `MOZ_TBPL_PARSER`,, testing/gtest/mozilla/GTestRunner.cpp
 `MOZ_TEST_IPC_DEMON`,, ipc/ipdl/test/cxx/TestDemon.cpp
 `MOZ_TLS_SERVER_CALLBACK_PORT`,, security/manager/ssl/tests/unit/tlsserver/lib/TLSServer.cpp
 `MOZ_TLS_SERVER_DEBUG_LEVEL`,, security/manager/ssl/tests/unit/tlsserver/lib/TLSServer.cpp
 `MOZ_UPLOAD_DIR`,, js/src/gc/Statistics.cpp js/src/util/StructuredSpewer.cpp testing/raptor/raptor/output.py testing/raptor/raptor/perftest.py testing/raptor/raptor/power.py testing/raptor/test/test_power.py testing/talos/talos/ffsetup.py
 `MOZ_WEBRENDER`,, gfx/thebes/gfxPlatform.cpp mobile/android/geckoview/src/androidTest/java/org/mozilla/geckoview/test/util/Environment.java
 `MOZ_XRE_DIR`,, tools/fuzzing/interface/harness/FuzzerTestHarness.h xpcom/tests/TestHarness.h
 `MOZHTTP2_PORT`,, testing/xpcshell/runxpcshelltests.py
 `MOZILLA_PKIX_TEST_LOG_DIR`,, security/nss/lib/mozpkix/test-lib/pkixtestutil.cpp
 `MOZPROCESS_DEBUG`,, testing/mozbase/mozprocess/mozprocess/processhandler.py
 `NOTEBOOK_PLUGIN`,, python/mozperftest/mozperftest/metrics/notebook/perftestetl.py
 `NSPR_ENVIRONMENT_TEST_VARIABLE`, part of `nsprpub` test, nsprpub/tests/env.c
 `NSS_GTEST_WORKDIR`,, security/nss/gtests/common/util.h security/nss/gtests/ssl_gtest/ssl_gtest.cc
 `OOM_THREAD`,, js/src/builtin/TestingFunctions.cpp
 `PATH`,, js/src/ctypes/libffi/ltmain.sh js/src/gdb/mozilla/IonGraph.py js/src/tests/shell/os.js modules/freetype2/builds/unix/ltmain.sh nsprpub/pr/tests/foreign.c nsprpub/pr/tests/lazyinit.c toolkit/xre/nsWindowsWMain.cpp uriloader/exthandler/unix/nsOSHelperAppService.cpp xpcom/build/BinaryPath.h
 `PERFHERDER_ALERTING_ENABLED`,, testing/gtest/mozilla/MozGTestBench.cpp
 `PY_IGNORE_IMPORTMISMATCH`,, testing/web-platform/tests/tools/third_party/py/py/\_path/local.py
 `PYTEST_THEME_MODE`,, `dark`testing/web-platform/tests/tools/third_party/pytest/src/\_pytest/\_io/terminalwriter.py testing/web-platform/tests/tools/third_party/pytest/src/\_pytest/\_io/terminalwriter.py
 `PYTEST_THEME`,, testing/web-platform/tests/tools/third_party/pytest/src/\_pytest/\_io/terminalwriter.py
 `PYTHONPATH`,, testing/web-platform/tests/tools/third_party/pytest/testing/acceptance_test.py
 `REPACK_MANIFESTS_URL`,, testing/mozharness/scripts/desktop_partner_repacks.py
 `SCOPED_SET_ENV_TEST_VAR`, `new_value`, third_party/libwebrtc/third_party/abseil-cpp/absl/base/internal/scoped_set_env_test.cc third_party/libwebrtc/third_party/abseil-cpp/absl/base/internal/scoped_set_env_test.cc third_party/libwebrtc/third_party/abseil-cpp/absl/base/internal/scoped_set_env_test.cc
 `SNAP`,, security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp security/sandbox/test/browser_content_sandbox_fs_snap.js security/sandbox/test/browser_content_sandbox_fs_tests.js
 `SQUAMMISH_HILLBILLY_GOAT_SQUEEZERS`,, js/src/tests/shell/os.js
 `srcdir`,, other-licenses/snappy/src/snappy-test.cc toolkit/crashreporter/google-breakpad/src/processor/basic_source_line_resolver_unittest.cc toolkit/crashreporter/google-breakpad/src/processor/exploitability_unittest.cc toolkit/crashreporter/google-breakpad/src/processor/fast_source_line_resolver_unittest.cc toolkit/crashreporter/google-breakpad/src/processor/microdump_processor_unittest.cc toolkit/crashreporter/google-breakpad/src/processor/minidump_processor_unittest.cc toolkit/crashreporter/google-breakpad/src/processor/minidump_unittest.cc gfx/harfbuzz/src/check-c-linkage-decls.py gfx/harfbuzz/src/check-externs.py gfx/harfbuzz/src/check-header-guards.py
 `SSLDEBUGFILE`, filepath specification to the output file where debug or trace information is written. If not set then the debug or trace information is written to `stderr`. Note: `SSLDEBUG` or `SSLTRACE` defines have to be set to use this functionality., security/nss/gtests/ssl_gtest/ssl_debug_env_unittest.cc security/nss/lib/ssl/sslsock.c
 `SSLKEYLOGFILE`, Filepath specification to the key log file for NSS to log RSA pre-master secrets into. This allows packet sniffers to decrypt TLS connections. See mozilla_project s_nss_key_log_format., security/nss/gtests/ssl_gtest/ssl_debug_env_unittest.cc security/nss/lib/ssl/sslsock.c
 `SSLTRACE`, An integer value that denotes the tracing level of its debug output. Note: The code must be built with `TRACE` macro defined to use this functionality., security/nss/gtests/ssl_gtest/selfencrypt_unittest.cc security/nss/gtests/ssl_gtest/tls_hkdf_unittest.ccsecurity/nss/lib/ssl/sslsock.c
 `SSLTUNNEL_LOG_LEVEL`,, testing/mochitest/ssltunnel/ssltunnel.cpp
 `STUN_SERVER_ADDRESS`,, dom/media/webrtc/transport/test/gtest_utils.h
 `STUN_SERVER_HOSTNAME`,, dom/media/webrtc/transport/test/gtest_utils.h
 `TASKCLUSTER_ROOT_URL`,, testing/web-platform/tests/tools/wpt/run.py
 `TASKCLUSTER_WORKER_LOCATION`,, taskcluster/scripts/run-task
 `TEMP`,, media/libvpx/libvpx/third_party/googletest/src/src/gtest.cc security/nss/cmd/httpserv/httpserv.c security/nss/cmd/selfserv/selfserv.c security/nss/gtests/google_test/gtest/src/gtest.cc security/nss/lib/dbm/src/h_page.c security/nss/lib/sqlite/sqlite3.c third_party/aom/third_party/googletest/src/googletest/src/gtest-port.cc third_party/googletest/googletest/src/gtest.cc third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest-filepath_test.cc third_party/rust/libsqlite3-sys/sqlcipher/sqlite3.c third_party/rust/libsqlite3-sys/sqlite3/sqlite3.c third_party/sqlite3/src/sqlite3.c xpcom/io/SpecialSystemDirectory.cpp js/src/editline/editline.c media/ffvpx/libavutil/log.c media/libvpx/libvpx/third_party/googletest/src/src/gtest.cc
 `TERM`, part of `googletest`, security/nss/gtests/google_test/gtest/src/gtest.cc third_party/aom/third_party/googletest/src/googletest/src/gtest.cc third_party/dav1d/tests/checkasm/checkasm.c third_party/googletest/googletest/src/gtest.cc third_party/rust/cubeb-sys/libcubeb/googletest/src/gtest.cc
 `TEST_PREMATURE_EXIT_FILE`, part of `googletest`., media/libvpx/libvpx/third_party/googletest/src/src/gtest.cc security/nss/gtests/google_test/gtest/src/gtest.cc security/nss/gtests/google_test/gtest/test/gtest_premature_exit_test.cc third_party/aom/third_party/googletest/src/googletest/src/gtest.cc third_party/googletest/googletest/src/gtest.cc
 `TEST_TMPDIR`,, media/libvpx/libvpx/third_party/googletest/src/src/gtest.cc security/nss/gtests/google_test/gtest/src/gtest.cc third_party/aom/third_party/libwebm/common/file_util.cc third_party/googletest/googletest/src/gtest.cc
 `TESTBRIDGE_TEST_ONLY`, part of `googletest`, media/libvpx/libvpx/third_party/googletest/src/src/gtest.cc security/nss/gtests/google_test/gtest/src/gtest.cc third_party/googletest/googletest/src/gtest.cc
 `TESTBRIDGE_TEST_RUNNER_FAIL_FAST`,, security/nss/gtests/google_test/gtest/src/gtest.cc third_party/googletest/googletest/src/gtest.cc
 `tmp`,, js/src/devtools/automation/autospider.py toolkit/crashreporter/nsExceptionHandler.cpp tools/crashreporter/injector/injector.cc tools/fuzzing/libfuzzer/FuzzerIOPosix.cpp xpcom/io/SpecialSystemDirectory.cpp
 `TMPDIR`,, security/nss/cmd/httpserv/httpserv.c security/nss/cmd/selfserv/selfserv.c security/nss/gtests/google_test/gtest/src/gtest-port.cc security/nss/lib/dbm/src/h_page.c security/nss/lib/softoken/sdb.c security/nss/lib/sqlite/sqlite3.c third_party/googletest/googletest/src/gtest-port.cc third_party/rust/libsqlite3-sys/sqlcipher/sqlite3.c third_party/rust/libsqlite3-sys/sqlite3/sqlite3.c third_party/sqlite3/src/sqlite3.c 
 `TURN_SERVER_ADDRESS`,, dom/media/webrtc/transport/test/gtest_utils.h
 `TURN_SERVER_PASSWORD`,, dom/media/webrtc/transport/test/gtest_utils.h
 `TURN_SERVER_USER`,, dom/media/webrtc/transport/test/gtest_utils.h
 `TZ`,, intl/icu/source/common/putil.cpp intl/icu/source/tools/tzcode/localtime.c js/src/vm/DateTime.cpp security/nss/gtests/google_test/gtest/test/gtest_unittest.cc security/sandbox/chromium/base/time/time_exploded_posix.cc third_party/libwebrtc/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_lookup.cc third_party/libwebrtc/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_lookup_test.cc toolkit/components/resistfingerprinting/nsRFPService.cpp
 `UPSTREAM_TASKIDS`,, testing/mozharness/scripts/desktop_partner_repacks.py
 `USER`,, testing/marionette/client/marionette_driver/geckoinstance.py testing/web-platform/tests/tools/third_party/pytest/doc/en/how-to/monkeypatch.rst uriloader/exthandler/nsExternalHelperAppService.cpp
 `USERPROFILE`,, media/libyuv/libyuv/tools_libyuv/valgrind/valgrind_test.py security/nss/lib/sqlite/sqlite3.c third_party/rust/libsqlite3-sys/sqlcipher/sqlite3.c third_party/rust/libsqlite3-sys/sqlite3/sqlite3.c third_party/sqlite3/src/sqlite3.c
 `WRITE_ARGUMENT_FILE`,, uriloader/exthandler/tests/WriteArgument.cpp
 `XDG_DATA_DIRS`,, security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp third_party/python/setuptools/pkg_resources/\_vendor/appdirs.py third_party/python/pip/pip/\_vendor/appdirs.py third_party/python/appdirs/appdirs.py
 `XDG_DATA_HOME`,, dom/ipc/ContentChild.cpp security/nss/gtests/sysinit_gtest/getUserDB_unittest.cc security/nss/lib/sysinit/nsssysinit.c security/sandbox/linux/broker/SandboxBrokerPolicyFactory.cpp widget/gtk/MPRISServiceHandler.cpp
 `XDG_SESSION_TYPE`,, third_party/libwebrtc/modules/desktop_capture/desktop_capturer.cc gfx/angle/checkout/src/libANGLE/renderer/driver_utils.cpp widget/gtk/nsWindow.cpp
 `XML_OUTPUT_FILE`, Part of `googletest`, media/libvpx/libvpx/third_party/googletest/src/src/gtest-port.cc security/nss/gtests/google_test/gtest/src/gtest-port.cc third_party/aom/third_party/googletest/src/googletest/src/gtest-port.cc third_party/googletest/googletest/src/gtest-port.cc
 `XPCSHELL_TEST_PROFILE_DIR`,, dom/ipc/ContentParent.cpp dom/quota/QuotaManager.h security/manager/ssl/CommonSocketControl.cpp security/manager/ssl/nsCertOverrideService.cpp toolkit/components/extensions/webidl-api/ExtensionTest.cpp
[/jtable]
