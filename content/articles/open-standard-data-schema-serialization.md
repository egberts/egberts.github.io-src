Title: Open standard on Data Schema and Serialization
Tags: schema, xsd, serialization
Date: 2015-08-31 05:00
Modified: 2018-12-20 12:00
Status: published
Category: research
Summary: A short list on open standard on Data Schema and Serialization

Doing a bit of research with regard to data schema and serializaton,
preferably without being JSON_centric.

[jtable]
Name, Defining Structure/Type, Structure is Extensible, Data Serialization, Data Validation, Human-Friendly
XML/XBRL,         YES, YES,  , YES,
Protocol Buffers, YES, ?, YES, YES, YES
JSON,              ,  ,  ,  , YES
Avro,             YES,YES?, YES, YES, sort of
CSV,               ,  ,  ,  , YES
Kwalify (YAML+JSON),YES, YES, YES, YES, YES
XML/NEIM,         YES, YES, n?, YES, YES
OKFN/CSV + JSON,  YES, ?, n, n, YES
[/jtable]
