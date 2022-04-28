title: Lint and Code Checking Python
date: 2020-05-04 17:00
status: published
tags: Python, lint, static analyzer
category: HOWTO
summary: How to lint and code check Python codes

* [coverage](http://nedbatchelder.com/code/coverage/)
* [pyflakes](https://launchpad.net/pyflakes)
* [flake8](https://gitlab.com/pycqa/flake8)
* [pycodestyle](https://pypi.python.org/pypi/pycodestyle)

# Example Runs #


Pyflakes
```shell
pyflakes bin/ config/ fail2ban/
```

Coverage
```shell
coverage run bin/fail2ban-testcases
coverage report
coverage html    # optionally
```
