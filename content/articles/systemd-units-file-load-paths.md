title: Systemd Unit File Load Paths
date: 2018-10-14T10:14
modified: 2025-12-30T05:38
status: published
category: research
tags: systemd
Summary: How to load systemd unit files using Load Paths

Unit File Load Path
===================

Unit files loads from a set of paths determined during compilation,
described in the two tables below. Unit files found in directories
listed, earlier override files with the same name in directories lower in
the list.

When the variable `$SYSTEMD_UNIT_PATH` gets set, the contents of this
variable overrides the unit load path. If `$SYSTEMD_UNIT_PATH` ends with
an empty component (":"), the usual unit load path appends to
the contents of the variable.

Table 1. Load path when running in system mode (`--system`).

```console
    Path    Description
    /etc/systemd/system.control Persistent and transient configuration created using the dbus API
    /run/systemd/system.control
    /run/systemd/transient  Dynamic configuration for transient units
    /run/systemd/generator.early    Generated units with high priority (see early-dir in system.generator(7))
    /etc/systemd/system Local configuration
    /run/systemd/system Runtime units
    /run/systemd/generator  Generated units with medium priority (see normal-dir in system.generator(7))
    /usr/local/lib/systemd/system   Units of installed packages
    /usr/lib/systemd/system
    /run/systemd/generator.late Generated units with low priority (see late-dir in system.generator(7))
```

Table 2. Load path when running in user mode (`--user`).

```console
    Path    Description
    $XDG_CONFIG_HOME/systemd/user.control or ~/.config/systemd/user.control
    Persistent and transient configuration created using the dbus API
    ($XDG_CONFIG_HOME if set, ~/.config otherwise)
    $XDG_RUNTIME_DIR/systemd/user.control
    /run/systemd/transient  Dynamic configuration for transient units
    /run/systemd/generator.early    Generated units with high priority (see
    early-dir in system.generator(7))
    $XDG_CONFIG_HOME/systemd/user or $HOME/.config/systemd/user User configuration
    ($XDG_CONFIG_HOME if set, ~/.config otherwise)
    /etc/systemd/user   Local configuration
    $XDG_RUNTIME_DIR/systemd/user   Runtime units (used with $XDG_RUNTIME_DIR
    set)
    /run/systemd/user   Runtime units
    $XDG_RUNTIME_DIR/systemd/generator  Generated units with medium priority (see
    normal-dir in system.generator(7))
    $XDG_DATA_HOME/systemd/user or $HOME/.local/share/systemd/user  Units of
    packages installed in the home directory ($XDG_DATA_HOME
    if set, ~/.local/share otherwise)
    $dir/systemd/user for each $dir in $XDG_DATA_DIRS, with more locations for
    installed user units, one for each entry in $XDG_DATA_DIRS
    /usr/local/lib/systemd/user Units of packages installed system-wide
    /usr/lib/systemd/user
    $XDG_RUNTIME_DIR/systemd/generator.late Generated units with low priority (see late-dir in system.generator(7))
```

The set of load paths for the user manager instance gets augmented or
changed using environment variables. And environment variables
gets created using environment generators, see
`systemd.environment-generator(7)`. In particular, `$XDG_DATA_HOME` and
`$XDG_DATA_DIRS` gets set using
`systemd-environment-d-generator(8)`. Thus, directories listed here are
defaults. To see the actual list based on
compilation options and current environment, use


```shell
systemd-analyze --user unit-paths
```

Moreover, other units gets loaded into `systemd` ("linked") from
directories not on the unit load path. See the link command for
`systemctl(1)`.
