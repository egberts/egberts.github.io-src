Title: Tight Multiversion Python Re-development Cycle
Tags: python
Date: 2018-12-12 10:45
Modified: 2020-03-04 16:53
Status: published
Category: research
Summary: Toward a tigher redevelopment cycle on Python.

Tight Multiversion Python Re-development Cycle
==============================================

Set up a new Python virtual environment
---------------------------------------

```python
cd \~/work/python
mkdir env3
```

Create the virtual environment support

```bash
python3 -m venv env
```

subdirectory bin created with all symlink'd executables (ie., pytest, python3, activate)

Following source command CANNOT be done from a script file but only from the CURRENT shell

```bash
source bin/activate
```

Now ready to add new (or existing) Python package to within Python3 environment

```shell
git clone https://github.com/jdoe/myrepo.git
```

Go into newly created package repo

```shell
cd myrepo
```

Depending if package is ready, make said package 'pseudo-installed' and live edit-able.
This enables you to skip the "install" part of the tight "edit python source→pip install→ pytest → edit python source" development loop.

```shell
if [[ -r setup.py ]]; then
  pip install -e .
else
  echo "No setup.py file found; must be a new environment or incorrect subdirectory."
fi
```

Nice, uh?
