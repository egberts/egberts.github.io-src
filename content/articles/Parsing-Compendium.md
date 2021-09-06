title: Parsing in Python Compendium
date: 2020-12-29 12:27EST
status: published
tags: parsing, python
category: research
lang: en
private: False

A link collection of parsing for Python.

* https://tomassetti.me/parsing-in-python/

Feature comparison
[jtable]
Library, Algorithm, Grammar, Builds tree?, Supports ambiguity?, Can handle every CFG?, Line/Column tracking, Generates Stand-alone, License
[ANTLR](https://www.antlr.org/), LL(\*), EBNF, Yes, No, Yes?, Yes, No, Proprietary
[Lark](https://github.com/lark-parser/lark), Earley/LALR(1), EBNF, Yes, Yes, Yes, Yes, Yes (LALR only), MIT
[PLY](http://www.dabeaz.com/ply/), LALR(1), BNF, No, No, No, No, No, Copyrighted
[PlyPlus](https://github.com/erezsh/plyplus), Earley/LALR(1), EBNF, Yes, Yes, Yes, Yes, No, MIT
[Parsimonious](https://github.com/erikrose/parsimonious), PEG, EBNF, Yes, No, No\*, No, No, MIT
[Parsley](https://github.com/pyga/parsley), PEG, EBNF, No, No, No\*, No, No, ReST
[PyParsing](https://github.com/pyparsing/pyparsing/), PEG, Combinators, No, No, No\*, No, No, MIT
[/jtable]
