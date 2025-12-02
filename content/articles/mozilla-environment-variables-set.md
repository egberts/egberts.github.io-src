title: Mozilla Environment Variables, setting
date: 2022-06-26 08:28
modified: 2025-07-13T0352
status: published
tags: environment variables, Mozilla, Firefox
category: research
lang: en
private: False



Environment variables that got created (via `setenv()`) in Mozilla Unified repository, git HEAD branch:

[jtable]
environment variable name, description, source file
 `__GL_ALLOW_FXAA_USAGE`, Set to `0` to temporarily disable the FXAA antialiasing on NVidia drivers.  Bug 1714483.,`build/mach_initialize.py`
 `ANDROID_EMU_VK_NO_CLEANUP`, This envvar gets created in implementing commands for running and interacting with Fuschia development on an AEMU VM platform.,`dom/ipc/ContentChild.cpp`
 `ANDROID_EMUGL_LOG_PRINT`, This envvar gets created in implementing commands for running and interacting with Fuschia development on an AEMU VM platform.,`dom/ipc/ContentParent.cpp`
 `ANDROID_EMUGL_VERBOSE`, This envvar gets created in implementing commands for running and interacting with Fuschia development on an AEMU VM platform.,`gfx/gl/GLContextProviderGLX.cpp`
 `DBUS_SESSION_BUS_ADDRESS`, If set to an empty string then do not overwrite an existing session dbus address but ensure that it is set.,`gfx/gl/GLLibraryEGL.cpp`
 `DESKTOP_AUTOSTART_ID`,,`gfx/thebes/gfxPlatformGtk.cpp`
 `force_s3tc_enable`, if set to `true` then forces enabling s3 texture compression. (Bug 774134),`gfx/thebes/gfxPlatformGtk.cpp`
 `G_SLICE`, `always-malloc`,`js/src/vtune/ittnotify_static.c:736:`
 `GTK_CSD`, This envvar gets set when a shell has been created for this app within GTK window environment.,`js/src/vtune/ittnotify_static.c:736:`
 `GTK_USE_PORTAL`, This envvar gets set when a shell has been created for this app within GTK window environment.,`js/xpconnect/src/XPCShellImpl.cpp`
 `INTEL_LIBITTNOTIY32`, For the Intel Parallel Inspector and Intel Inspector XE tools.  Defaults to `data/data/com.intel.vtune/perfrun/lib`.,`mozglue/baseprofiler/core/platform.cpp:2938`
 `INTEL_LIBITTNOTIY64`, For the Intel Parallel Inspector and Intel Inspector XE tools.  Defaults to `data/data/com.intel.vtune/perfrun/lib`.,`mozglue/baseprofiler/core/platform.cpp:2945`
 `JPROF_ISCHILD`, if (!is_child),mozglue/baseprofiler/core/platform.cpp:2952
 `LD_PRELOAD`, Gets redefined from last prior `MOZ_ORIG_LD_PRELOAD` setting.,mozglue/baseprofiler/core/platform.cpp:2955
 `MACH_MAIN_PID`, OS Process ID,mozglue/baseprofiler/core/platform.cpp:2965
 `MACH_STDOUT_ISATTY`, If set to `1` then it allow invoked processes (which may not have a handle on the original stdout file descriptor) to know if the original stdout is a TTY. This provides a mechanism to allow said processes to enable emitting code codes as an example.,mozglue/misc/PreXULSkeletonUI.cpp
 `mesa_glthread`, Set to `false` to temporarily disable the EGL GLThread under X11. Bug 1670545.,`python/mach/mach/main.py:397`
 `MOZ_APP_NO_DOCK`, This envvar gets set when this Mozilla application did not get docked via Cocoa only within macOS platforms.,security/manager/ssl/nsNSSComponent.cpp:1555:
 `MOZ_APP_RESTART=1`, This envvar gets set only as a simple indicator that this shell environment is currently in restart stage.,security/nss/cmd/nss-policy-check/nss-policy-check.c:118
 `MOZ_APP_SILENT_START`, This envvar gets set only for macOS platforms when to suppress prompting the user for escalation.,security/nss/cmd/nss-policy-check/nss-policy-check.c:126
 `MOZ_ASSUME_USER_NS`, This envvar gets created when in a new user namespace that is in a single-thread mode.,security/nss/cmd/nss-policy-check/nss-policy-check.c:128
 `MOZ_CRASHREPORTER_EVENTS_DIRECTORY`, This envvar gets modified if `CRASHES_EVENT_DIR` has been added.,security/nss/lib/pk11wrap/pk11pars.c:525
 `MOZ_DISABLE_ASAN_REPORTER`, Set to `1` to disable the Mozilla ASAN reporter.  Otherwise reports to `https://anf1.fuzzing.mozilla.org/crashproxy/submit/` to Mozilla `nightly-asan` update channel.,security/nss/lib/pk11wrap/pk11pars.c:876
 `MOZ_HEADLESS`," This is for X11-only setup pending a solution for WebGL in Wayland mode.  Takes a value of ""1"" or remains undefined. For MOZ_WIDGET_GTK C define only.  Calls `widget::GdkIsX11Display()`",security/nss/lib/util/secport.c:743:
 `MOZ_INSTALLED_AND_RELAUNCHED_FROM_DMG`, This envvar gets set to `1` during relaunching from its DMG package file only within macOS platforms.,security/sandbox/linux/Sandbox.cpp:474:
 `MOZ_LAUNCHED_CHILD`,  This envvar gets set to `1` during NS App Runner., security/sandbox/linux/SandboxInfo.cpp:148:
 `MOZ_LAUNCHER_PROCESS`,  This envvar gets set to `1` during NS App Runner., `third_party/libwebrtc/build/fuchsia/aemu_target.py:102:`
 `MOZ_NO_REMOTE`,  This envvar gets set to `1` during NS App Runner., `third_party/libwebrtc/build/fuchsia/aemu_target.py:102:`
 `MOZ_PROFILER_SHUTDOWN`, , `third_party/libwebrtc/build/fuchsia/aemu_target.py:102:`
 `MOZ_PROFILER_STARTUP_ACTIVE_TAB_ID`, activeTabIDString.get, `third_party/libwebrtc/build/fuchsia/aemu_target.py:102:`
 `MOZ_PROFILER_STARTUP_ENTRIES`, If MOZ_PROFILER_STARTUP is set then it specifies the number of entries per process in the profiler's circular buffer when the profiler is first started. If unset then the platform default is used: `%u` entries per process or `%u` when MOZ_PROFILER_STARTUP is set. (%u bytes per entry -> %u or %u total bytes per process).  Optional units in bytes: `KB` `KiB` `MB` `MiB` `GB` `GiB`.,toolkit/components/resistfingerprinting/nsRFPService.cpp:697:
 `MOZ_PROFILER_STARTUP_ENTRIES`, capacityString.get()),toolkit/components/startup/nsAppStartup.cpp:1066:
 `MOZ_PROFILER_STARTUP_FEATURES_BITFIELD`, featuresString.get()),toolkit/components/startup/nsAppStartup.cpp:408:
 `MOZ_PROFILER_STARTUP_FILTERS`,If MOZ_PROFILER_STARTUP is set then it specifies the profiling features as a comma-separated list of strings.  Ignored if MOZ_PROFILER_STARTUP_FEATURES_BITFIELD is set.  If unset then the platform default is used.  Features: (`x`=unavailable or `D`/`d`=default/unavailable or `S`/`s`=MOZ_PROFILER_STARTUP extra,toolkit/crashreporter/nsExceptionHandler.cpp:2923:
 `MOZ_PROFILER_STARTUP_FILTERS`, filtersString.c_str()),toolkit/xre/nsAppRunner.cpp
 `MOZ_PROFILER_STARTUP_INTERVAL`, If MOZ_PROFILER_STARTUP is set then specifies the sample interval then it measured in milliseconds when the profiler is first started. If unset then the platform default is used.,toolkit/xre/nsAppRunner.cpp
 `MOZ_PROFILER_STARTUP_INTERVAL`, intervalString.get()),toolkit/xre/nsAppRunner.cpp
 `MOZ_PROFILER_STARTUP_NO_BASE`, `1`,toolkit/xre/nsAppRunner.cpp
 `MOZ_PROFILER_STARTUP`, If set to any value other than empty string or `0`/`N`/`n` then it starts the profiler immediately on start-up.  Useful if you want profile code that runs very early.,toolkit/xre/nsAppRunner.cpp
 `MOZ_RESET_PROFILE_MIGRATE_SESSION`,  This envvar gets set to `1` during NS App Runner.,toolkit/xre/nsAppRunner.cpp
 `MOZ_RESET_PROFILE_RESTART`,  This envvar gets set to `1` during NS App Runner.,toolkit/xre/nsAppRunner.cpp
 `MOZ_SAFE_MODE_RESTART`, If during update then gets set to `1` for updater process to detect that restart is to be performed in safe mode.,toolkit/xre/nsAppRunner.cpp
 `MOZ_SKELETON_UI_RESTARTING`, A state transition for pre-XUL.  Used with lockfile.,toolkit/xre/nsAppRunner.cpp
 `MOZ_TEST_PROCESS_UPDATES`,  This envvar gets set to `1` during NS App Runner.,toolkit/xre/nsAppRunner.cpp
 `MOZ_UNINSTALLER_PROFILE_REFRESH`,  This envvar gets set to `1` during NS App Runner.,toolkit/xre/nsAppRunner.cpp
 `NO_AT_BRIDGE`, Set to `0` before initializing the GTK module to the ATA bridge.,toolkit/xre/nsAppRunner.cpp
 `NSS_IGNORE_SYSTEM_POLICY=1`,,toolkit/xre/nsAppRunner.cpp
 `NSS_POLICY_FAIL=1`, If the requested version is not a recognized variant of supported TLS then this envvar will be set to `1`.,toolkit/xre/nsAppRunner.cpp
 `NSS_POLICY_LOADED`, If the policy is not declared then this envvar shall be set to `0`.  Helps to distinguished between unloaded and loaded but failed scenarios.,toolkit/xre/MacRunFromDmgUtils.mm:258
 `NSS_POLICY_WARN`, If the requested version of TLS is outside the range of its predefined NSS Policy Check range of supported TLS versions then this envvar will be set to `1`.,toolkit/xre/nsAppRunner.cpp
 `NSS_SDB_USE_CACHE`, If the profile is on a networked drive then this envvar is set to enable caching mechanism and minimize network activity.,toolkit/xre/nsNativeAppSupportUnix.cpp:463
 `SSL_INHERITANCE`, If set to `1` then it will inheirent the SSL session cache from its parent process.,toolkit/xre/nsUpdateDriver.cpp:562
 `TRACE_FILE`, contains the `logPath.get()` file path specification.  For XP_WIN Windows platform only as `PR_LoadLibrary()` is not available under XP Windows.,tools/jprof/stub/libmalloc.cpp:637
 `TZ`, If set to `UTC` then universal time coordinate is used.  If set to an empty string then system provides the timezone.  If set to `:/etc/localtime` then the content of that file provides the timezone.  This is used for resisting browser fingerprinting.,tools/profiler/core/platform.cpp:5361
 `VK_ICD_FILENAMES`, This envvar gets created in implementing commands for running and interacting with Fuschia development on an AEMU VM platform.,tools/profiler/core/platform.cpp:5368
 `VK_LOADER_DEBUG`, This envvar gets created in implementing commands for running and interacting with Fuschia development on an AEMU VM platform for WebRTC testing.,tools/profiler/core/platform.cpp:5373
 `XRE_BINARY_PATH`,  This envvar gets set to `1` during NS App Runner.,tools/profiler/core/platform.cpp:5381
 `XRE_PROFILE_LOCAL_PATH`, Save file path specification to the local profile data,tools/profiler/core/platform.cpp:5394
 `XRE_PROFILE_PATH`, Save file path specification to the profile data,widget/cocoa/nsCocoaWindow.mm
 `XRE_RESTART_TO_PROFILE_MANAGER`,  This envvar gets set to `1` during NS App Runner.,widget/gtk/nsAppShell.cpp
 `XRE_RESTARTED_BY_PROFILE_MANAGER`,  This envvar gets set to `1` during NS App Runner.,xpcom/base/AppShutdown.cpp:164
 `XRE_START_OFFLINE`,  This envvar gets set to `1` during NS App Runner.,xpcom/base/AppShutdown.cpp:172
 `XUL_APP_FILE`,  This envvar gets set to `1` during NS App Runner.,xpcom/base/AppShutdown.cpp:175
 PR_SetEnv(newData.get()),,xpcom/base/Logging.cpp:354
 PR_SetEnv(sSavedProfDEnvVar),,xpcom/glue/standalone/nsXPCOMGlue.cpp:369
 PR_SetEnv(sSavedProfLDEnvVar),,xpcom/threads/nsEnvironment.cpp:130
 PR_SetEnv(sSavedXulAppFile),,xpcom/base/AppShutdown.cpp:159
 PR_SetEnv(ToNewCString(env)),,accessible/atk/Platform.cpp
[/jtable]


# Test Environment Variables Created

The remainder of Mozilla-setted environment variables are left below and unformatted but as a future reference.

ipc/chromium/src/third_party/libevent/test/regress.c:2701:	`EVENT_NOWAFFLES`, `1`, 1);
ipc/chromium/src/third_party/libevent/test/regress.c:2729: 		`EVENT_NOEPOLL`, `1`, 1);
ipc/chromium/src/third_party/libevent/test/regress.c:2733:		setenv(varbuf, `1`, 1);
js/src/builtin/TestingFunctions.cpp:7025: return `TZ`, value, true) == 0;
js/src/builtin/TestingFunctions.cpp:8935:" NOTE: The input string is not validated and will be passed verbatim to setenv().`,
python/mozbuild/mozbuild/test/test_telemetry_settings.py:140: monkeypatch.`DISABLE_TELEMETRY`, `1`
python/mozlint/test/test_editor.py:64: monkeypatch.`EDITOR`, `generic`
python/mozlint/test/test_editor.py:74: monkeypatch.`EDITOR`, `vim`
python/mozlint/test/test_editor.py:84: monkeypatch.`EDITOR`, `generic`
python/mozlint/test/test_roller.py:156: monkeypatch.`CODE_REVIEW`, `1`
python/mozlint/test/test_roller.py:167: monkeypatch.`CODE_REVIEW`, `1`
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:1735: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "TEMP`, ``
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:1838: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "UnsetVar`, `123`
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:1857: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "VAR`, `1234567891234567891234`
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:475: setenv(("TZ`, time_zone, 1);
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6610: `TERM`, `xterm`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6614: `TERM`, `dumb`, TERM doesn't support colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6620: `TERM`, `dumb`, TERM doesn't support colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6635: `TERM`, `xterm`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6639: `TERM`, `dumb`, TERM doesn't support colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6645: `TERM`, `xterm`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6660: `TERM`, `xterm`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6671: `TERM`, `dumb`,
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6674: `TERM`, ,
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6677: `TERM`, `xterm`,
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6683: `TERM`, `dumb`, TERM doesn't support colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6686: `TERM`, `emacs`, TERM doesn't support colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6689: `TERM`, `vt100`, TERM doesn't support colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6692: `TERM`, `xterm-mono`, TERM doesn't support colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6695: `TERM`, `xterm`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6698: `TERM`, `xterm-color`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6701: `TERM`, `xterm-256color`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6704: `TERM`, `screen`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6707: `TERM`, `screen-256color`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6710: `TERM`, `tmux`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6713: `TERM`, `tmux-256color`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6716: `TERM`, `rxvt-unicode`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6719: `TERM`, `rxvt-unicode-256color`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6722: `TERM`, `linux`, TERM supports colors.
security/nss/gtests/google_test/gtest/test/gtest_unittest.cc:6725: `TERM`, `cygwin`, TERM supports colors.
security/nss/gtests/ssl_gtest/ssl_keylog_unittest.cc:37: PR_SetEnv(env_to_set_.c_str());
security/nss/gtests/sysinit_gtest/getUserDB_unittest.cc:108: ASSERT_EQ(0, `XDG_DATA_HOME`, tmp_home_.c_str(), 1));
security/nss/gtests/sysinit_gtest/getUserDB_unittest.cc:34: ASSERT_EQ(0, `HOME`, tmp_home_.c_str(), 1));
security/nss/gtests/sysinit_gtest/getUserDB_unittest.cc:46: ASSERT_EQ(0, `XDG_DATA_HOME`, old_xdg_data_home_.c_str(), 1));
startupcache/test/TestStartupCache.cpp:65: PR_SetEnv(env);
startupcache/test/TestStartupCache.cpp:72: `MOZ_STARTUP_CACHE=`
taskcluster/gecko_taskgraph/test/test_actions_util.py:164: monkeypatch.`TASK_ID`, task_id)
taskcluster/gecko_taskgraph/test/test_actions_util.py:165: monkeypatch.`TASKCLUSTER_ROOT_URL`, base_url)
taskcluster/gecko_taskgraph/test/test_actions_util.py:166: monkeypatch.`TASKCLUSTER_PROXY_URL`, base_url)
taskcluster/gecko_taskgraph/test/test_try_option_syntax.py:398: def test_setenv(self):
testing/gtest/mozilla/GTestRunner.cpp:109: `XPCOM_DEBUG_BREAK=stack-and-abort`
testing/mochitest/tests/SimpleTest/AccessibilityUtils.js:524: setEnv(env = DEFAULT_ENV) {
testing/mochitest/tests/SimpleTest/AccessibilityUtils.js:531: resetEnv() {
testing/mochitest/tests/SimpleTest/AccessibilityUtils.js:548: this.resetEnv();
testing/mozbase/mozdebug/tests/test.py:29: monkeypatch.`PATH`, os.pathsep.join(dirs))
testing/mozbase/mozfile/tests/test_which.py:27: monkeypatch.`PATH`, bindir)
testing/mozbase/mozfile/tests/test_which.py:57: monkeypatch.`PATH`, bindir)
testing/web-platform/tests/tools/third_party/pytest/doc/en/builtin.rst:158: monkeypatch.setenv(name, value, prepend=None)
testing/web-platform/tests/tools/third_party/pytest/doc/en/how-to/monkeypatch.rst:24: monkeypatch.setenv(name, value, prepend=None)
testing/web-platform/tests/tools/third_party/pytest/doc/en/how-to/monkeypatch.rst:293: monkeypatch.`USER`, `TestingUser`
testing/web-platform/tests/tools/third_party/pytest/doc/en/how-to/monkeypatch.rst:314: monkeypatch.`USER`, `TestingUser`
testing/web-platform/tests/tools/third_party/pytest/doc/en/how-to/monkeypatch.rst:51:4. Use ``monkeypatch.`PATH`, value, prepend=os.pathsep)`` to modify ``$PATH``, and
testing/web-platform/tests/tools/third_party/py/testing/io_/test_terminalwriter.py:319: monkeypatch.`NO_COLOR`, `0`
testing/web-platform/tests/tools/third_party/py/testing/io_/test_terminalwriter.py:321: monkeypatch.`NO_COLOR`, `1`
testing/web-platform/tests/tools/third_party/py/testing/io_/test_terminalwriter.py:323: monkeypatch.`NO_COLOR`, `any`
testing/web-platform/tests/tools/third_party/py/testing/io_/test_terminalwriter.py:327: monkeypatch.`PY_COLORS`, `1`
testing/web-platform/tests/tools/third_party/py/testing/io_/test_terminalwriter.py:329: monkeypatch.`PY_COLORS`, `0`
testing/web-platform/tests/tools/third_party/py/testing/io_/test_terminalwriter.py:332: monkeypatch.`PY_COLORS`, `any`
testing/web-platform/tests/tools/third_party/py/testing/io_/test_terminalwriter.py:36: monkeypatch.setenv('COLUMNS', '42')
testing/web-platform/tests/tools/third_party/py/testing/io_/test_terminalwriter.py:55: monkeypatch.setenv('COLUMNS', '42')
testing/web-platform/tests/tools/third_party/py/testing/path/test_local.py:163: monkeypatch.`HOME`, str(tmpdir))
testing/web-platform/tests/tools/third_party/py/testing/path/test_local.py:416: monkeypatch.`PATH`, str(tmpdir), prepend=os.pathsep)
testing/web-platform/tests/tools/third_party/py/testing/path/test_local.py:428: monkeypatch.`PATH`, noperm, prepend=":`
testing/web-platform/tests/tools/third_party/py/testing/path/test_local.py:440: monkeypatch.setenv('PATH', `%s:%s" % (
testing/web-platform/tests/tools/third_party/py/testing/path/test_local.py:534: monkeypatch.setenv('PY_IGNORE_IMPORTMISMATCH', '1')
testing/web-platform/tests/tools/third_party/py/testing/path/test_local.py:538: monkeypatch.setenv('PY_IGNORE_IMPORTMISMATCH', '0')
testing/web-platform/tests/tools/third_party/py/testing/path/test_local.py:696: monkeypatch.`HOME`, path)
testing/web-platform/tests/tools/third_party/pytest/src/_pytest/monkeypatch.py:282: def setenv(self, name: str, value: str, prepend: Optional[str] = None) -> None:
testing/web-platform/tests/tools/third_party/pytest/src/_pytest/monkeypatch.py:39: monkeypatch.setenv(name, value, prepend=None)
testing/web-platform/tests/tools/third_party/pytest/src/_pytest/pytester.py:710: mp.`PYTEST_DEBUG_TEMPROOT`, str(self._test_tmproot))
testing/web-platform/tests/tools/third_party/pytest/src/_pytest/pytester.py:717: mp.`HOME`, tmphome)
testing/web-platform/tests/tools/third_party/pytest/src/_pytest/pytester.py:718: mp.`USERPROFILE`, tmphome)
testing/web-platform/tests/tools/third_party/pytest/src/_pytest/pytester.py:720: mp.`PY_COLORS`, `0`
testing/web-platform/tests/tools/third_party/pytest/testing/acceptance_test.py:637: monkeypatch.`PYTHONPATH`, str(empty_package), prepend=os.pathsep)
testing/web-platform/tests/tools/third_party/pytest/testing/acceptance_test.py:646: monkeypatch.`PYTHONPATH`, str(pytester), prepend=os.pathsep)
testing/web-platform/tests/tools/third_party/pytest/testing/acceptance_test.py:692: monkeypatch.`PYTHONPATH`, prepend_pythonpath(*search_path))
testing/web-platform/tests/tools/third_party/pytest/testing/acceptance_test.py:772: monkeypatch.`PYTHONPATH`, prepend_pythonpath(*search_path))
testing/web-platform/tests/tools/third_party/pytest/testing/conftest.py:135: monkeypatch.`PYTEST_DISABLE_PLUGIN_AUTOLOAD`, `1`
testing/web-platform/tests/tools/third_party/pytest/testing/io/test_terminalwriter.py:19: monkeypatch.`COLUMNS`, `42`
testing/web-platform/tests/tools/third_party/pytest/testing/python/fixtures.py:3201: monkeypatch.`PYTHONHASHSEED`, `1`
testing/web-platform/tests/tools/third_party/pytest/testing/python/fixtures.py:3203: monkeypatch.`PYTHONHASHSEED`, `2`
testing/web-platform/tests/tools/third_party/pytest/testing/python/fixtures.py:3958: monkeypatch.`FIXTURE_ACTIVATION_VARIANT`, variant)
testing/web-platform/tests/tools/third_party/pytest/testing/test_assertion.py:1234: monkeypatch.`CI`, `1`
testing/web-platform/tests/tools/third_party/pytest/testing/test_assertion.py:463: monkeypatch.`CI`, `true`
testing/web-platform/tests/tools/third_party/pytest/testing/test_assertrewrite.py:1013: monkeypatch.`PYTEST_PLUGINS`, `plugin`
testing/web-platform/tests/tools/third_party/pytest/testing/test_assertrewrite.py:853: monkeypatch.`PYTHONDONTWRITEBYTECODE`, `1`
testing/web-platform/tests/tools/third_party/pytest/testing/test_assertrewrite.py:915: monkeypatch.`PYTHONOPTIMIZE`, `2`
testing/web-platform/tests/tools/third_party/pytest/testing/test_cacheprovider.py:165: monkeypatch.`env_var`, `custom_cache_dir`
testing/web-platform/tests/tools/third_party/pytest/testing/test_cacheprovider.py:510: monkeypatch.`FAILIMPORT`, str(fail_import))
testing/web-platform/tests/tools/third_party/pytest/testing/test_cacheprovider.py:511: monkeypatch.`FAILTEST`, str(fail_run))
testing/web-platform/tests/tools/third_party/pytest/testing/test_cacheprovider.py:558: monkeypatch.`FAILIMPORT`, str(fail_import))
testing/web-platform/tests/tools/third_party/pytest/testing/test_cacheprovider.py:559: monkeypatch.`FAILTEST`, str(fail_run))
testing/web-platform/tests/tools/third_party/pytest/testing/test_cacheprovider.py:78: monkeypatch.`PYTEST_DISABLE_PLUGIN_AUTOLOAD`, `1`
testing/web-platform/tests/tools/third_party/pytest/testing/test_capture.py:1495: monkeypatch.`PYTEST_DISABLE_PLUGIN_AUTOLOAD`, `1`
testing/web-platform/tests/tools/third_party/pytest/testing/test_collection.py:1196: monkeypatch.`PYTHONPATH`, str(pytester.path), prepend=os.pathsep)
testing/web-platform/tests/tools/third_party/pytest/testing/test_config.py:1092: monkeypatch.`PYTEST_DISABLE_PLUGIN_AUTOLOAD`, `1`
testing/web-platform/tests/tools/third_party/pytest/testing/test_config.py:1637: monkeypatch.`PYTEST_ADDOPTS`, `-o cache_dir=%s" % cache_dir)
testing/web-platform/tests/tools/third_party/pytest/testing/test_config.py:1646: monkeypatch.`PYTEST_ADDOPTS`, `-o`
testing/web-platform/tests/tools/third_party/pytest/testing/test_config.py:1771: monkeypatch.`COLUMNS`, `90`
testing/web-platform/tests/tools/third_party/pytest/testing/test_config.py:468: monkeypatch.`PYTEST_PLUGINS`, `myplugin`
testing/web-platform/tests/tools/third_party/pytest/testing/test_config.py:84: monkeypatch.`PYTEST_ADDOPTS`, '--color no -rs --tb="short"')
testing/web-platform/tests/tools/third_party/pytest/testing/test_config.py:962: monkeypatch.`PYTEST_PLUGINS`, `mytestplugin`
testing/web-platform/tests/tools/third_party/pytest/testing/test_debugging.py:28: pytester._monkeypatch.`PDBPP_HIJACK_PDB`, `0`
testing/web-platform/tests/tools/third_party/pytest/testing/test_debugging.py:905: monkeypatch.`PYTHONPATH`, str(pytester.path))
testing/web-platform/tests/tools/third_party/pytest/testing/test_doctest.py:528: monkeypatch.`HELLO`, `WORLD`
testing/web-platform/tests/tools/third_party/pytest/testing/test_helpconfig.py:119: monkeypatch.`PYTEST_DEBUG`, `1`
testing/web-platform/tests/tools/third_party/pytest/testing/test_junitxml.py:1088: monkeypatch.`HOME`, str(tmp_path))
testing/web-platform/tests/tools/third_party/pytest/testing/test_monkeypatch.py:146: monkeypatch.setenv(key, `hello`
testing/web-platform/tests/tools/third_party/pytest/testing/test_monkeypatch.py:173:def test_setenv() -> None:
testing/web-platform/tests/tools/third_party/pytest/testing/test_monkeypatch.py:176: monkeypatch.`XYZ123`, 2) # type: ignore[arg-type]
testing/web-platform/tests/tools/third_party/pytest/testing/test_monkeypatch.py:196: monkeypatch.setenv(name, `3`
testing/web-platform/tests/tools/third_party/pytest/testing/test_monkeypatch.py:221: monkeypatch.setenv(str(self.VAR_NAME), value) # type: ignore[arg-type]
testing/web-platform/tests/tools/third_party/pytest/testing/test_monkeypatch.py:228: monkeypatch.`XYZ123`, `2`, prepend="-`
testing/web-platform/tests/tools/third_party/pytest/testing/test_monkeypatch.py:229: monkeypatch.`XYZ123`, `3`, prepend="-`
testing/web-platform/tests/tools/third_party/pytest/testing/test_parseopt.py:320: monkeypatch.`_ARGCOMPLETE`, `1`
testing/web-platform/tests/tools/third_party/pytest/testing/test_parseopt.py:321: monkeypatch.`_ARGCOMPLETE_IFS`, `\x0b`
testing/web-platform/tests/tools/third_party/pytest/testing/test_parseopt.py:322: monkeypatch.`COMP_WORDBREAKS`, ` \\t\\n\"\\'><=;|&(:`
testing/web-platform/tests/tools/third_party/pytest/testing/test_parseopt.py:325: monkeypatch.`COMP_LINE`, `pytest " + arg)
testing/web-platform/tests/tools/third_party/pytest/testing/test_parseopt.py:326: monkeypatch.`COMP_POINT`, str(len("pytest " + arg)))
testing/web-platform/tests/tools/third_party/pytest/testing/test_parseopt.py:341: monkeypatch.`COMP_LINE`, `pytest " + arg)
testing/web-platform/tests/tools/third_party/pytest/testing/test_parseopt.py:342: monkeypatch.`COMP_POINT`, str(len("pytest " + arg)))
testing/web-platform/tests/tools/third_party/pytest/testing/test_pathlib.py:158: monkeypatch.`PY_IGNORE_IMPORTMISMATCH`, `1`
testing/web-platform/tests/tools/third_party/pytest/testing/test_pathlib.py:162: monkeypatch.`PY_IGNORE_IMPORTMISMATCH`, `0`
testing/web-platform/tests/tools/third_party/pytest/testing/test_pluginmanager.py:269: monkeypatch.`PYTEST_PLUGINS`, `nonexisting`, prepend=`,`
testing/web-platform/tests/tools/third_party/pytest/testing/test_pluginmanager.py:282: monkeypatch.`PYTEST_PLUGINS`, `skipping2`
testing/web-platform/tests/tools/third_party/pytest/testing/test_pluginmanager.py:319: monkeypatch.`PYTEST_PLUGINS`, `pytest_x500`, prepend=`,`
testing/web-platform/tests/tools/third_party/pytest/testing/test_pytester.py:622: monkeypatch.`PYTEST_ADDOPTS`, `--orig-unused`
testing/web-platform/tests/tools/third_party/pytest/testing/test_pytester.py:722: pytester._monkeypatch.`CUSTOMENV`, `42`
testing/web-platform/tests/tools/third_party/pytest/testing/test_session.py:342: monkeypatch.`PY_ROOTDIR_PATH`, str(pytester.path))
testing/web-platform/tests/tools/third_party/pytest/testing/test_terminal.py:1084: monkeypatch.`COLUMNS`, `80`
testing/web-platform/tests/tools/third_party/pytest/testing/test_terminal.py:173: monkeypatch.`PY_COLORS`, `1`
testing/web-platform/tests/tools/third_party/pytest/testing/test_terminal.py:1975: monkeypatch.`PY_COLORS`, `1`
testing/web-platform/tests/tools/third_party/pytest/testing/test_terminal.py:2419: monkeypatch.`PYTEST_THEME`, `solarized-dark`
testing/web-platform/tests/tools/third_party/pytest/testing/test_terminal.py:2420: monkeypatch.`PYTEST_THEME_MODE`, `dark`
testing/web-platform/tests/tools/third_party/pytest/testing/test_terminal.py:2441: monkeypatch.`PYTEST_THEME`, `invalid`
testing/web-platform/tests/tools/third_party/pytest/testing/test_terminal.py:2457: monkeypatch.`PYTEST_THEME_MODE`, `invalid`
testing/web-platform/tests/tools/third_party/pytest/testing/test_terminal.py:330: monkeypatch.`PY_COLORS`, `1`
testing/web-platform/tests/tools/third_party/pytest/testing/test_tmpdir.py:131: monkeypatch.`PYTEST_DEBUG_TEMPROOT`, str(linktemp))
testing/web-platform/tests/tools/third_party/pytest/testing/test_tmpdir.py:448: monkeypatch.`PYTEST_DEBUG_TEMPROOT`, str(tmp_path))
testing/web-platform/tests/tools/third_party/pytest/testing/test_tmpdir.py:468: monkeypatch.`PYTEST_DEBUG_TEMPROOT`, str(tmp_path))
testing/web-platform/tests/tools/third_party/pytest/testing/test_warnings.py:515: monkeypatch.`PYTHONWARNINGS`, `once::UserWarning`
third_party/jpeg-xl/plugins/gdk-pixbuf/pixbufloader_test.cc:19: `GDK_PIXBUF_MODULE_FILE`, loaders_cache, true);
third_party/jpeg-xl/plugins/gdk-pixbuf/pixbufloader_test.cc:23: `XDG_DATA_HOME`, `.`, true);
third_party/jpeg-xl/plugins/gdk-pixbuf/pixbufloader_test.cc:24: `XDG_DATA_DIRS`, ``, true);
third_party/libwebrtc/third_party/abseil-cpp/absl/strings/numbers_test.cc:814: fesetenv(&fp_env_);
third_party/libwebrtc/third_party/abseil-cpp/absl/synchronization/mutex_test.cc:1059: setenv(kVarName, warnings_output_file_.c_str(), 0);
third_party/libwebrtc/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_lookup_test.cc:1033: ASSERT_EQ(0, `TZ`, *np, 1)); // change what "localtime" means
third_party/libwebrtc/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_lookup_test.cc:1100: ASSERT_EQ(0, `TZ`, tz_name.c_str(), 1));
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:1828:static void SetEnv(const char* name, const char* value) {
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:1857: setenv(name, value, 1);
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:1872: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "TEMP`, ``
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:1881: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "TEMP`, `12345678987654321`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:1884: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "TEMP`, `-12345678987654321`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:1893: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "TEMP`, `A1`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:1896: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "TEMP`, `12X`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:1904: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "TEMP`, `123`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:1907: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "TEMP`, `-321`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:1971: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "UnsetVar`, `123`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:1973: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "UnsetVar`, `-123`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:1981: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "VAR`, `xxx`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:1990: SetEnv(GTEST_FLAG_PREFIX_UPPER_ "VAR`, `1234567891234567891234`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2014: SetEnv(index_var_, ``
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2015: SetEnv(total_var_, ``
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2025: SetEnv(index_var_, ``
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2026: SetEnv(total_var_, ``
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2034: SetEnv(index_var_, `0`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2035: SetEnv(total_var_, `1`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2045: SetEnv(index_var_, `4`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2046: SetEnv(total_var_, `22`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2050: SetEnv(index_var_, `8`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2051: SetEnv(total_var_, `9`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2055: SetEnv(index_var_, `0`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2056: SetEnv(total_var_, `9`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2067: SetEnv(index_var_, `4`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2068: SetEnv(total_var_, `4`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2071: SetEnv(index_var_, `4`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2072: SetEnv(total_var_, `-2`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2075: SetEnv(index_var_, `5`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2076: SetEnv(total_var_, ``
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2079: SetEnv(index_var_, ``
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:2080: SetEnv(total_var_, `5`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6392: `TERM`, `xterm` // TERM supports colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6396: `TERM`, `dumb` // TERM doesn't support colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6402: `TERM`, `dumb` // TERM doesn't support colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6417: `TERM`, `xterm` // TERM supports colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6421: `TERM`, `dumb` // TERM doesn't support colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6427: `TERM`, `xterm` // TERM supports colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6442: `TERM`, `xterm` // TERM supports colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6453: `TERM`, `dumb`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6456: `TERM`, ``
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6459: `TERM`, `xterm`
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6465: `TERM`, `dumb` // TERM doesn't support colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6468: `TERM`, `emacs` // TERM doesn't support colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6471: `TERM`, `vt100` // TERM doesn't support colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6474: `TERM`, `xterm-mono` // TERM doesn't support colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6477: `TERM`, `xterm` // TERM supports colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6480: `TERM`, `xterm-color` // TERM supports colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6483: `TERM`, `xterm-256color` // TERM supports colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6486: `TERM`, `screen` // TERM supports colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6489: `TERM`, `linux` // TERM supports colors.
third_party/rust/cubeb-sys/libcubeb/googletest/test/gtest_unittest.cc:6492: `TERM`, `cygwin` // TERM supports colors.
toolkit/modules/subprocess/test/xpcshell/test_subprocess.js:810: libc.setenv(
Environment variables created for testing purposes as found in Mozilla Unified repository, git HEAD branch:

devtools/client/accessibility/test/browser/browser_accessibility_relation_navigation.js:105: AccessibilityUtils.setEnv({
devtools/client/accessibility/test/browser/browser_accessibility_relation_navigation.js:115: AccessibilityUtils.resetEnv();
devtools/client/accessibility/test/browser/browser_accessibility_relation_navigation.js:120: AccessibilityUtils.setEnv({
devtools/client/accessibility/test/browser/browser_accessibility_relation_navigation.js:130: AccessibilityUtils.resetEnv();
devtools/client/accessibility/test/browser/head.js:525: AccessibilityUtils.setEnv({
devtools/client/accessibility/test/browser/head.js:531: AccessibilityUtils.resetEnv();
devtools/client/accessibility/test/browser/head.js:551: AccessibilityUtils.setEnv({
devtools/client/accessibility/test/browser/head.js:560: AccessibilityUtils.resetEnv();
devtools/client/accessibility/test/browser/head.js:576: AccessibilityUtils.setEnv({
devtools/client/accessibility/test/browser/head.js:582: AccessibilityUtils.resetEnv();
devtools/client/framework/test/browser_toolbox_zoom_popup.js:146: AccessibilityUtils.setEnv({
devtools/client/framework/test/browser_toolbox_zoom_popup.js:159: AccessibilityUtils.resetEnv();
devtools/client/netmonitor/test/browser_net_basic-search.js:57: AccessibilityUtils.setEnv({
devtools/client/netmonitor/test/browser_net_basic-search.js:66: AccessibilityUtils.resetEnv();
devtools/client/netmonitor/test/browser_net_header-docs.js:30: AccessibilityUtils.setEnv({
devtools/client/netmonitor/test/browser_net_header-docs.js:41: AccessibilityUtils.resetEnv();
devtools/client/netmonitor/test/browser_net_server_timings.js:32: AccessibilityUtils.setEnv({
devtools/client/netmonitor/test/browser_net_server_timings.js:43: AccessibilityUtils.resetEnv();
devtools/client/netmonitor/test/head.js:1326: AccessibilityUtils.setEnv({
devtools/client/netmonitor/test/head.js:1335: AccessibilityUtils.resetEnv();
devtools/client/webconsole/test/browser/browser_webconsole_clickable_urls.js:78: AccessibilityUtils.setEnv({
devtools/client/webconsole/test/browser/browser_webconsole_clickable_urls.js:91: AccessibilityUtils.resetEnv();
devtools/client/webconsole/test/browser/browser_webconsole_filter_buttons_overflow.js:41: AccessibilityUtils.setEnv({
devtools/client/webconsole/test/browser/browser_webconsole_filter_buttons_overflow.js:54: AccessibilityUtils.resetEnv();
devtools/client/webconsole/test/browser/browser_webconsole_input_focus.js:49: AccessibilityUtils.setEnv({
devtools/client/webconsole/test/browser/browser_webconsole_input_focus.js:56: AccessibilityUtils.resetEnv();
devtools/client/webconsole/test/browser/browser_webconsole_input_focus.js:69: AccessibilityUtils.setEnv({
devtools/client/webconsole/test/browser/browser_webconsole_input_focus.js:76: AccessibilityUtils.resetEnv();
devtools/client/webconsole/test/browser/browser_webconsole_object_ctrl_click.js:100: AccessibilityUtils.resetEnv();
devtools/client/webconsole/test/browser/browser_webconsole_object_ctrl_click.js:30: AccessibilityUtils.setEnv({
devtools/client/webconsole/test/browser/browser_webconsole_object_ctrl_click.js:43: AccessibilityUtils.resetEnv();
devtools/client/webconsole/test/browser/browser_webconsole_object_ctrl_click.js:85: AccessibilityUtils.setEnv({
devtools/client/webconsole/test/browser/browser_webconsole_sidebar_scroll.js:29: AccessibilityUtils.setEnv({
devtools/client/webconsole/test/browser/browser_webconsole_sidebar_scroll.js:44: AccessibilityUtils.resetEnv();
devtools/client/webconsole/test/browser/browser_webconsole_split.js:112: AccessibilityUtils.setEnv({
devtools/client/webconsole/test/browser/browser_webconsole_split.js:117: AccessibilityUtils.resetEnv();
