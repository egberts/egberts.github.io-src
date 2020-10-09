title: How to disable screen clearing at Linux bootup
date: 2020-08-16 10:01
status: published
tags: systemd, Linux, bootup, screen
category: HOWTO
summary: How to disable screen clearing during Linux bootup.

Disabling Screen Clearing at Boot Time
======================================


The normal behavior for `systemd` is to clear the screen at the 
end of the boot sequence. 
If desired, this behavior may be changed by running the following command:

```bash
mkdir -pv /etc/systemd/system/getty@tty1.service.d

cat > /etc/systemd/system/getty@tty1.service.d/noclear.conf << EOF
[Service]
TTYVTDisallocate=no
EOF
```

The boot messages can always be reviewed by using the 
`journalctl -b` command as the root user. 
