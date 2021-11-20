title: Python is dead; `py3compile` not found.
date: 2021-11-16 16:00
status: published
tags: Python, Debian
category: HOWTO
summary: How to rebuild Python in Debian ... intensively.
lang: en
private: False


Ahhhh, yes.  The venerable "Catch-22" situation of Debian package management.  I had a case that boils down to Debian depending on `py3compile` as part of the `libpython3.x` package when that package provides the `py3compile` as well; it's a no-go, there.

I too was bitten by this unable to get `py3compile` working again for I had too deleted the entire `/usr/[/local]/lib/python3*` directories.  

Once done, nothing in Debian package management tool can help you get back to a working Python3 environment.  You must do meat-ball surgery.

Reconstruction of Python3 in Debian entails three critical things:

* Restoring `py3compile` script (for most of you, you already have this)
* Restoring libpython3.7
* Restoring python binary

One could do the RE-copying of `/usr[/local]/lib` directory from another working Debian host/system. But this time, I shall detail the steps from within the broken host in question (as if you do NOT have another working host).

# Step 1 - Download Packages
Download the impacted Debian packages:

```bash
cd /tmp
apt-get download libpython3.7-minimal
apt-get download python3.7-minimal
apt-get download python3-minimal # (this is important)
apt-get download libpython3.7-stdlib
apt-get download python3.7
```

# Step 2 - Cleanup
Clean up old stuff

```sh
rm -rf /usr[/local]/lib/python3.7*
rm -rf /usr[/local]/bin/python3.7*
update-alternatives --remove python3 /usr[/local]/bin/python3.7
hash -r  # removes cached python3 binary path
```

# Step 3 - Extract files from packages

Let us extract the missing `py3compile`

```bash
cd /tmp
dpkg-deb -x python3-minimal_3.7.3-1_amd64.deb missing
dpkg-deb -x python3.7-minimal_3.7.3-2_amd64.deb missing
dpkg-deb -x libpython3.7-minimal_3.7.3-2_amd64.deb missing
dpkg-deb -x libpython3.7-stdlib_3.7.3-2_amd64.deb missing
dpkg-deb -x python3.7_3.7.3-2_amd64.deb missing
```

# Step 3 
Manually install over your root filesystem

```bash
cd /tmp/missing
ls -lR /tmp/missing  # if you are curious about overwriting your HD
sudo cp -rpfv /tmp/missing/*  /
```
    
# Step 4 - Verification
Start up Python3

```python
python3
Python 3.7.3 (default, Apr  3 2019, 05:39:12) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Test import and show version

```python
>>> import sys
>>> print(sys.version_info)
sys.version_info(major=3, minor=7, micro=3, releaselevel='final', serial=0)
>>>
>>> quit()
```

# Step 5 - Clean up ourselves

```bash
rm -rf /tmp/missing
```

# Step 6 - Officially reinstall Python via Debian APT

```bash
dpkg -s -a  | grep  reinstreq
# Any listing also needs to be reinstalled along with python3
apt-get install --reinstall python3
```

Most likely, you got MANY packages that are in that stuck state of "reinstreq" state.

```bash
apt-get autoclean
apt-get autoremove
# (MANY PACKAGES FAILED TO BE INSTALLED)
```

At this point, you will have to manually reinstall each and every one of those listed by `apt-get autoremove`...

```bash
apt-get install --fix-broken --reinstall <list-of-many-failed-packages>
```

# Last Step - Reinstalling impacted half-state Debian packages
Let me guess, you got the following error:

```console
E: Internal Error, No file name for XXXXXX
```

I will tell you that you probably had a newer Debian release in your `/etc/apt/sources.list` for awhile, it went all down south (bad), and took that newer release out of the `sources.list` file (in effort to revert back to a 'stable' release): that's not an unrecoverable thing to me here, just that you jerked the Debian package database around a bit there ... rather brusquely. 

The resolution of the last step entails a restoration and stabilization of the Debian package management database by reinstalling nearly everything.  I will detail it later but the link to follow is given [here](https://askubuntu.com/questions/266450/how-to-fix-e-internal-error-no-file-name-for-libc6).
