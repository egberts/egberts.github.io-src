title: Developing Mozilla on Debian 11
date: 2022-06-23 07:27
modified: 2025-07-13 02:09
status: published
tags: Mozilla, Firefox, Debian
summary: Developing Mozilla on Debian 11
category: HOWTO
lang: en
private: False


Project: Firefox
Version: 103
Date: 2022-06-23

Dependencies needed for Firefox development on Debian 11

```bash
sudo apt-get install clang11 llvm
sudo apt-get install libnotify-dev
sudo apt-get install curl python3 python3-dev python3-pip
python3 -m pip install --user mercurial
```


# Caching of object file (Optional)

for faster debug cycle, optionally add the following cargo package:

```bash
gh repo clone https://github.com/mozilla/sccache.git
cd sccache
cargo build --release [--no-default-features
```


