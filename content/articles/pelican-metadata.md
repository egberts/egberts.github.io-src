title: Pelican Metadata
date: 2020-10-13 09:30
status: published
tags: pelican
category: HOWTO
keywords: pelican, metadata, markdown
summary: Details on Pelican Metadata
lang: en
private: False

This article details the metadata used by
[Pelican](https://github/getpelican/pelican), a static website generator.

You can also have your own metadata keys (so long as they don't conflict with reserved metadata keywords) for use in your templates. 

The following table contains a list of reserved metadata keywords:

[jtable]
Metadata, Description
`title`, Title of the article or page
`author`, Author of this content file if only one author is used.
`authors`, Authors of this content file if there are more than one author used.  Authors are separated by a comma '`,`'.
`category`, Category that this content file falls under.  Cannot use more than one category.  User-definable and automatically incorporated by Pelican initially from here.
`date`, Publication date of this content file in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format (e.g., `YYYY-MM-DD HH:SS`)
`keywords`, Content keyword(s) whereas if more than one keyword then separated by comma '`,`'.  Used only in HTML context.
`lang`, Two-letter [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) code of the language used in this content file.
`modified`, Modification date of this content file in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format (e.g., `YYYY-MM-DD HH:SS`)
`private`, Exclude such summary of this content file from website's site map.  Used only by `sitemap` plugin.
`save_as`, Save content to this relative file path.  Useful for renaming files into `index.html` or copying to outside of content directory (for example, copying content/pages/website-cover.md to https://website.example/index.html especially if your entire blog is already one-deep (https://website.example/blog/).
`slug`, Filename identifier that are used in its URL and language translation(s).
`status`, Status of this content file: `draft`, `hidden`, or `published`.
`summary`, Brief description of this content file for use by various index pages. Trunction of this summary is set by `SUMMARY_MAX_COUNT` in number of words unit.
`tags`, Content tag(s) whereas if more than one then separated by comma.
`template`, Name of template that is use to generate this content (without the extension filetype).
`translation`, Translated from another content file. Boolean value only: `true` or `false`.  Used to denote which content file has the original translation.
`url`, URL to use for this article/page
[/jtable]
