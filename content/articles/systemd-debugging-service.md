title: Debugging a service in systemd
date: 2022-04-30 08:51
status: published
tags: systemd, debugging
category: HOWTO
summary: How to debug a service in systemd

# Debugging the Service Unit 

Into the service unit file, insert the following:

```ini
[Service]
Environment=SYSTEMD_LOG_LEVEL=debug
```

Or equivalently, set the environment variable manually:

```bash
SYSTEMD_LOG_LEVEL=debug /lib/systemd/systemd-networkd
```

# Debugging systemd-home

```bash
SYSTEMD_HOME_DEBUG_SUFFIX=foo \
    SYSTEMD_HOMEWORK_PATH=/home/lennart/projects/systemd/build/systemd-homework \
    SYSTEMD_HOME_ROOT=/home.foo/ \
    SYSTEMD_HOME_RECORD_DIR=/var/lib/systemd/home.foo/ \
    /home/lennart/projects/systemd/build/systemd-homed
```

# References

* [Environment variables in systemd](https://systemd.io/ENVIRONMENT/)
* [Hacking systemd](https://systemd.io/HACKING/)
* [Troubleshooting systemd (ArchLinux)](https://wiki.archlinux.org/title/Systemd#systemd-tmpfiles-setup.service_fails_to_start_at_boot)
