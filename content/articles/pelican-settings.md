title: Pelican Configuration Settings
date: 2020-10-10 10:00
status: published
tags: pelican
category: HOWTO
summary: Details on use of configuration settings in Pelican

The legends used to describe settings are:
[jtable caption="Legend"]
string, a text-based string; may use `'{}'` variables.
boolean, a binary type that only accepts '`True`' or '`False`'
filename, a filename that has no directory path nor slash symbol.
filespec, a relative directory path and a filename 
abs\_filepath, a full, complete (absolute) directory path and a filename 
dirspec, a directory name or an incomplete path to the directory (relative)
abs\_dirpath, a full, complete path to the directory (absolute)
dict of, a Python type that uses '`{`' and '`}`' to contain all its comma-separated key AND values (looks like '`key_name : key_value`').
list of, a Python type that uses '`[`' and '`]`' to contain all its comma-separated values
tuples of, a Python type that uses '`(`' and '`)`' to contain all its comma-separated values
varname, the variable name in which to use for metadata
ip\_address, IP address
[/jtable]

abs\_dirpath, abs\_filepath, dirspec, filename, and filespec can use
and embedded any of the following string variables:


[jtable caption="Variables" separator=',']
variable name, description
`{attach}`, the full absolute URL specification to where all articles are found under.  Useful for image or a link.  Same as `ARTICLES_URL_PATH`.
`{author}`, the full URL path AND closing QUERY/parameters to add toward its author.  Expanded from `AUTHOR_URL`.  Any period symbol found gets removed here before its usage.
`{category}`, the directory name of a category that this article/page is metadata as.  Same as `CATEGORY_URL`.  Any period symbol found outside of the `{category}` gets removed here before its usage.
`{filename}`, the full absolute URL specification toward this generated article/page. Any relative URL will be expanded to a full URL path, including its slug filename.
`{index}`, the full URL specification to this article/page's index.html file.  Same as `$INDEX_SAVE_AS`.  Any other character other than `{index}` will be ignored.
`{static}`, the full absolute URL specification to its article/page.  Any other character outside of `{static}` shall be ignored.
`{tag}`, the full URL specification to where all tags are kept in.  Any period symbol found outside of  the `{tag}` part gets removed before its usage.
[/jtable]

Common Settings
==========
Many of the Pelican configuration key name have a common suffix.

[jtable caption="Pelican Generic Settings" separator=',']
suffix , value type , description
\_EXCLUDES , string , what to omit
\_PATHS , string , filesystem path either file or directory.
\_REGEX_SUBSTITUTIONS , string , what to search for
\_SAVE_AS , string , the dirpath to use in the `$OUTPUT` directory.
\_URL , string , the dirpath to use in the URL ending with a filename/filetype.  You can customize the URLs and locations where files will be saved. The `*_URL` and `*_SAVE_AS` variables use Python's format strings. These variables allow you to place your articles in a location such as `{slug}/index.html` and link to them as `{slug}` for clean URLs. These settings give you the flexibility to place your articles and pages anywhere you want.
\_URL_PATH , string , the dirpath to use in the URL but without the filespec.
\_SUBSTITUTIONS , string , what to substitute
[/jtable]

The common suffixes found in most Pelican's Python-based configuration key
names are:

[jtable caption="Pelican Settings" separator=u',']
name , type , default , description
`ARCHIVES_SAVE_AS`, filespec , `'archives/index.html'`, The location to save the article archives page.
`ARCHIVES_URL`, filespec , `'archives/index.html'`,
`ARCHIVES_URL_PATH`, filespec , `'archives'`,
`ARCHIVE_SAVE_AS`, filespec , `'archives/{slug}.html'`,
`ARCHIVE_URL`, filespec , `'archives/{slug}.html'`,
`ARTICLE_EXCLUDES`, list of dirspec , `['pages']`, the subdirectory name under \$PATH where selected directories are to be excluded from chronological indexing.
`ARTICLE_LANG_URL`, filespec , `'{slug}-{lang}.html'`, {lang} denotes the two-letter country code
`ARTICLE_ORDER_BY`, string , `'reversed-date'`,  How you want your ordering done for chronological (article) content.  Three choices:  `'reversed-date'`; `'basename'`. Defines how the articles (articles_page.object_list in the template) are sorted. Valid options are: metadata as a string (use reversed- prefix the reverse the sort order) then special option 'basename' which will use the basename of the file (without path) or a custom function to extract the sorting key from articles. The default value 'reversed-date' will sort articles by date in reverse order (i.e. newest article comes first).
`ARTICLE_PATHS`, list of dirspec , `['articles']`, the subdirectory name under \$PATH where all chronological pages are being kept at
`ARTICLE_PERMALINK_STRUCTURE`, string , `''`,
`ARTICLE_SAVE_AS`, filespec , `'articles/{slug}.html'`, The place where we will save an article.
`ARTICLE_LANG_SAVE_AS`, filespec , `'{slug}-{lang}.html'`, The place where we will save an article which doesn't use the default language.
`ARTICLE_LANG_URL`, filespec, `'{slug}-{lang}.html'`,  The URL to refer to an article which doesn’t use the default language.
`ARTICLE_TRANSLATION_ID`, varname , `'slug'`,
`ARTICLE_URL`, filespec , `'articles/{slug}.html'`, The URL to refer to an article.
`ARTICLES_URL`, filespec , `'articles/index.html'`, 
`ARTICLES_URL_PATH`, filespec , `'articles'`, 
`AUTHOR`, string , (must define) ,  Default author (put your name)
`AUTHOR_FEED_ATOM`, filespec , `'feeds/%s.atom.xml'`, Where to put the author Atom feeds.
`AUTHOR_FEED_RSS`, filespec , `'feeds/%s.rss.xml'`, Where to put the author RSS feeds.
`AUTHOR_REGEX_SUBSTITUTIONS`, list of tuple of regex , `None`, 
`AUTHOR_SAVE_AS`, string , `'authors/{slug}.html?and&in&url=""'`, The location to save an author.
`AUTHOR_URL`, string , `'authors/{slug}.html?and&in&url=""'`, The URL to use for an author.
`AUTHORS_SAVE_AS`, string , `'authors/index.html'`, The location to save the author list.
`AUTHORS_URL`, string , `'authors/index.html'`,
`AUTHORS_URL_PATH`, string , `'authors'`,
`AUTORELOAD_IGNORE_CACHE`,  ,  ,
`BIND`, ip\_address ,  ,
`CACHE_CONTENT`, boolean , `False`, If True, saves content in caches. See [Reading only modified content](https://docs.getpelican.com/en/3.6.3/settings.html#reading-only-modified-content) for details about caching.
`CACHE_PATH`, abs\_filespec , `${PWD}/cache`, Directory in which to store cache files.
`CATEGORY_FEED_ATOM`, filespec , `'feeds/{slug}.atom.xml'`, Where to put the category Atom feeds.
`CATEGORY_FEED_ATOM_URL`, filespec , `'/feeds/{slug}.atom.xml'`,
`CATEGORY_FEED_RSS`, filespec , `None`, Where to put the category RSS feeds.
`CATEGORY_FEED_RSS_URL`, filespec , `None`,
`CATEGORY_URL`, filespec , `'categories/{slug}.html'`, The URL to use for a category.
`CATEGORY_SAVE_AS`, filespec , `'categories/{slug}.html'`, The location to save a category.
`CATEGORIES_SAVE_AS`, filespec , `'categories/index.html'`, The location to save the category list.
`CATEGORIES_TO_COLLATE`, list of string , `['category-of-interest', 'another-cool-category']`,
`CATEGORIES_URL`, filespec , `'categories/index.html'`,
`CATEGORIES_URL_PATH`, filespec , `'categories'`,
`CHECK_MODIFIED_METHOD`, string , `'mtime'`, What checksum methods to use when checking wether a file has been modified or not.  `'mtime'` uses your filesystem modified time of the file in question.  Otherwise, not specifying `'mtime'` will attempt to consult your specified function name of `hashlib` module.  At this moment using Python3.8 the additional available options are: `'blake2b'`; `'blake2s'`; `'md5'`; `'pbkdf2_hmac'`; `'sha1'`; `'sha224'`; `'sha256'`; `'sha384'`; `'sha3_224'`; `'sha3_256'`; `'sha3_384'`; `'sha3_512'`; `'sha512'`; `'shake_128'`; `'shake_256'`.
`CLEAN_URLS`,  ,  ,
`CONTENT_CACHING_LAYER`, string , `'reader'`, If set to `'reader'` then save only the raw content and metadata returned by readers. If set to `'generator'` then save processed content objects.
`CSS_FILE`, filename , `'main.css'`, Specify the CSS file you want to load.  The filename of CSS used by this theme (`$THEME`).
`DATE_FORMATS`, dict of string , `{}`,  A dictionary of string of date format whose key is in by two-char country code.  If left blank, [ISO-8601](https://www.w3.org/TR/NOTE-datetime) is used.  If you manage multiple languages, you can set the date formatting here. 
`DAY_ARCHIVE_SAVE_AS`, filespec , `''`, The location to save per-day archives of
your posts.
`DAY_ARCHIVE_URL`, filespec , `''`, The URL to use per-day archives of your posts.
`DEBUG`, boolean , `False`,
`DEFAULT_CATEGORY`, string , `'misc'`,  The category name to use if a content file did not have `category: ` metadata in its file.   	The default category to fall back on.
`DEFAULT_CONFIG`,  ,  ,
`DEFAULT_CONFIG_NAME`,  ,  ,
`DEFAULT_DATE`, string , `None`,  The default date format for all two-char country code, unless overriden by `DATE_FORMATS`.  If `fs` is specified then modified timestamp of file is used.  The default date you want to use. If 'fs', Pelican will use the file system timestamp information (mtime) if it can't get date information from the metadata. If set to a tuple object the default datetime object will instead be generated by passing the tuple to the `datetime.datetime()` constructor.
`DEFAULT_DATE_FORMAT`, string , '%a %d %B %Y' , the date format to use that is located before the summary line  of each chronological (article) contents.  The default date format you want to use.
`DEFAULT_LANG`, string , `'en'`, The default language to use.  
`DEFAULT_METADATA`, dict of string , `{}`, If your articles should be automatically published as a draft (to not accidentally publish an article before it is finished) include the status in the `DEFAULT_METADATA`.  Key name is the metadata label and its key value is the metadata value (e.g. `DEFAULT_METADATA = { 'status': 'draft', }`.
`DEFAULT_ORPHANS`, integer , `0`, The minimum number of articles allowed on the last page. Use this when you don't want the last page to only contain a handful of articles.
`DEFAULT_PAGINATION`, integer , `20`, The maximum number of articles to include on a page, not including orphans. False to disable pagination.  Numbers of chronological (article) content to list per page.
`DELETE_OUTPUT_DIRECTORY`, boolean , `True`, Every time that Pelican is executed, purge the output directory before starting anew.  Delete the output directory, and all of its contents, before generating new files. This can be useful in preventing older, unnecessary files from persisting in your output. However, this is a destructive setting and should be handled with extreme care.
`DESCRIPTION`, string , (must define) ,
`DIRECT_TEMPLATES`, tuples of string , `('index', 'categories', 'tags', 'archives', 'authors')`, List of templates that are used directly to render content. Typically direct templates are used to generate index pages for collections of content (e.g., tags and category index pages). If the tag and category collections are not needed then set `DIRECT_TEMPLATES = ['index', 'archives']`
`DISPLAY_PAGES_ON_MENU`, boolean , `True`, Put the `Pages` on navigation menu.
 Whether to display pages on the menu of the template. Templates may or may not honor this setting.
`DISPLAY_CATEGORIES_ON_MENU`, boolean , `True`, Put the `Categories` on primary navigation menu. You can use the `DISPLAY_PAGES_ON_MENU` setting to control whether all those pages are displayed in the primary navigation menu.  Whether to display categories on the menu of the template. Templates may or not honor this setting.
`DOCUTILS_SETTINGS`, dict of string , `{}`, Extra configuration settings for the docutils publisher (applicable only to reStructuredText). See [Docutils Configuration settings](https://docutils.sourceforge.io/docs/user/config.html) for more details.
`DRAFT_ARTICLES_SAVE_AS`, filespec , `'drafts/articles/index.html'`,
`DRAFT_ARTICLES_URL`, filespec , `'drafts/articles/index.html'`,
`DRAFT_ARTICLES_URL_PATH`, filespec , `'drafts/articles'`,
`DRAFT_LANG_URL`, filespec , `'drafts/{slug}-{lang}.html'`, The URL to refer to an article draft which doesn't use the default language.  `{lang}` denotes the two-letter country code
`DRAFT_LANG_SAVE_AS`, filespec , `'drafts/{slug}-{lang}.html'`, The place where we will save an article draft which doesn't use the default language.
`DRAFT_PAGE_LANG_URL`, filespec , `'drafts/pages/{slug}-{lang}.html'`, {lang} denotes the two-letter country code
`DRAFT_PAGE_LANG_SAVE_AS`, filespec , `'drafts/pages/{slug}-{lang}.html'`, {lang} denotes the two-letter country code
`DRAFT_PAGE_SAVE_AS`, filespec , `'drafts/pages/{slug}.html'`,
`DRAFT_PAGE_URL`, filespec , `'drafts/pages/{slug}.html'`, 
`DRAFT_PAGES_SAVE_AS`, filespec , `'drafts/pages/index.html'`,
`DRAFT_PAGES_URL`, filespec , `'drafts/pages/index.html'`, 
`DRAFT_PAGES_URL_PATH`, filespec , `'drafts/pages'`, 
`DRAFT_SAVE_AS`, filespec , `'drafts/{slug}.html'`, The place where we will save an article draft.
`DRAFT_URL`, filespec , `'drafts/articles/{slug}.html'`, The URL to refer to an article draft.
`DRAFTS_SAVE_AS`, filespec , `'drafts/index.html'`,
`DRAFTS_URL`, filespec , `'drafts/index.html'`,
`EACH_SLUG_HAS_SUBDIR`, boolean , `False`, Instead of a markdown file, you could have a slug subdirectory and put all your related images under that subdir.
`EXTRA_PATH_METADATA`, dict of items , `{}`, Extra metadata dictionaries keyed by relative path. Relative paths require correct OS-specific directory separators (i.e. / in UNIX and \ in Windows) unlike some other Pelican file settings. See Path metadata.
`EXTRA_TEMPLATES_PATHS`, list of dirspec , '`[]`' , A list of paths you want Jinja2 to search for templates. Can be used to separate templates from the theme. Example: projects; resume; profile ... These templates need to use `DIRECT_TEMPLATES` setting.
`FEED_ALL_ATOM`, string , `feeds/all.atom.xml`, Relative URL to output the all-posts Atom feed: this feed will contain all posts regardless of their language.
`FEED_ALL_ATOM_URL`, string , `'feeds/atom.xml'`,
`FEED_ALL_RSS`, string , `''`, Relative URL to output the all-posts RSS feed: this feed will contain all posts regardless of their language.
`FEED_ALL_RSS_URL`, string , `''`,
`FEED_ATOM`, string , `''`, Relative URL to output the Atom feed.
`FEED_DOMAIN`, string , (must define) , The domain prepended to feed URLs. Since feed URLs should always be absolute, it is highly recommended to define this (e.g. `'http://feeds.example.com'`). If you have already explicitly defined `SITEURL` (see above) and want to use the same domain for your feeds then you can just set: `FEED_DOMAIN = SITEURL`.
`FEED_MAX_ITEMS`, string , `''`, Maximum number of items allowed in a feed. Feed item quantity is unrestricted by default.
`FEED_RSS`, string , `''`, Relative URL to output the RSS feed.
`FEED_RSS_URL`, string , `''`,
`FILENAME_METADATA`, string , `'(?P<date>\\d{4}-\\d{2}-\\d{2}).*'`, You can also extract any metadata from the filename through a regular expression to be set in the `FILENAME_METADATA` setting. All named groups that are matched will be set in the metadata object. The default value for the `FILENAME_METADATA` setting will only extract the date from the filename. For example, if you would like to extract both the date and the slug, you could set something like: `'(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'`
`FORMATTED_FIELDS`, list of string , `['summary', 'description', 'landing']`, A list of metadata fields found in reST/Markdown content that are to be parsed and translated into HTML.
`GZIP_CACHE`, boolean , `False`,  Enables gzipping of cache.  If `True`, use gzip to (de)compress the cache files.
`IGNORE_FILES`, list of string , `['.#*', '.ipynb_checkpoints', '__pycache__']`,  Files to skip during processing.  A list of glob patterns. Files and directories matching any of these patterns will be ignored by the processor. For example, the default `['.#*']` will ignore emacs lock files, and `['__pycache__']` would ignore Python 3's bytecode caches.
`INDEX_SAVE_AS`, string , `'articles/index.html'`,  The location to save the list of all articles.
`INTRASITE_LINK_REGEX`, string , `'[{,](?P<what>.*?)[,}]'`, Regular expression that is used to parse internal links. Default syntax when linking to internal files; tags; etc., is to enclose the identifier let us say filename in `{}` or `||`. Identifier between `{` and `}` goes into the what capturing group. For details see [Linking to internal content](https://docs.getpelican.com/en/3.6.3/content.html#ref-linking-to-internal-content).
`JINJA_ENVIRONMENT`,  ,  ,
`JINJA_EXTENSIONS`,  ,  ,
`JINJA_FILTERS`,  ,  ,
`LOAD_CONTENT_CACHE`, boolean , `False`, If `True`, load unmodified content from caches.  When experimenting with different settings (especially the metadata ones) caching may interfere and the changes may not be visible. In such cases disable caching with `LOAD_CONTENT_CACHE = False` or use the `--ignore-cache` command-line switch.
`LOCALE`, list of string , `['']`,
`LOG_FILTER`, list of string , `[]`, A list of tuples containing the logging level (up to warning) and the message to be ignored. For example: `[(logging.WARN, 'TAG_SAVE_AS is set to False')]`
`MARKDOWN`,  ,  ,
`MD_EXTENSIONS`, list of string , `['.md', '.markdown', '.mkd', or '.mdown'`, the Markdown filetype extension(s) for its content file to be recognized by a Markdown reader.
`MINIBIO`, string , `None`, a minibiography about the author
`MONTH_ARCHIVE_SAVE_AS`, filespec , `''`, The location to save per-month archives of your posts.
`MONTH_ARCHIVE_URL`, filespec , `''`, The URL to use per-month archives of your posts.
`NEWEST_FIRST_ARCHIVES`, boolean , `True`, Order archives by newest first by date. (`False`: orders by date with older articles first.)
`OUTPUT_PATH`, dirspec , `${PWD}/output`, The output directory that contains the fully-formatted HTML pages, and is ready for uploading to websites or viewing by a local webbrowser directly.
`OUTPUT_RETENTION`, list of string , `[]`, A list of outputted files that you want to keep despite `$DELETE_OUTPUT_DIRECTORY` being enabled.  A list of filenames that should be retained and not deleted from the output directory. One use case would be the preservation of version control data. For example: `[".hg", ".git", ".bzr"]`.
`OUTPUT_SOURCES`, boolean , False , Put all of the original, untranslated contents into the output directories for later export to the website.  Any such directory must be added to both STATIC_PATHS and PAGE_PATHS (or STATIC_PATHS and ARTICLE_PATHS).  Set to `True` if you want to copy the articles and pages in their original format (e.g. Markdown or reStructuredText) to the specified OUTPUT_PATH.
`OUTPUT_SOURCES_EXTENSION`, filetype , `'.txt'`, Add this filetype toward its filename of all original, untranslated contents.
`PAGE_EXCLUDES`, list of dirspec , `['articles']`, the subdirectory where selected contents are not included for static page viewing.
`PAGE_LANG_SAVE_AS`, filespec , `pages/{slug}-{lang}.html'`, The location we will save the page which doesn't use the default language. {lang} denotes the two-letter country code
`PAGE_LANG_URL`, filespec , `pages/{slug}-{lang}.html'`, The URL we will use to link to a page which doesn't use the default language. {lang} denotes the two-letter country code
`PAGE_ORDER_BY`, string , `'date'`, How do you want your pages sorted by at the 'Pages' menu?  Defines how the pages (PAGES variable in the template) are sorted. Options are same as `ARTICLE_ORDER_BY`. The default value `'basename'` will sort pages by their basename.
`PAGE_PATHS`, list of dirspec , `['pages']`, the subdirectory(s) where all non-chronological pages are stored at.
`PAGE_SAVE_AS`, filespec , `'pages/{slug}.html'`, The location we will save the page. This value has to be the same as `PAGE_URL` or you need to use a rewrite in your server config.
`PAGE_TRANSLATION_ID`, varname , `'slug'`,
`PAGE_URL`, filespec , `'pages/{slug}.html'`, The URL we will use to link to a page.
`PAGES_SAVE_AS`, filespec , `'pages/index.html'`,
`PAGES_URL`, filespec , `'pages/index.html'`,
`PAGES_URL_PATH`, filespec , `'pages'`,
`PAGINATED_DIRECT_TEMPLATES`, list of filename  , `['index']`, Provides the direct templates that should be paginated.
`PAGINATED_TEMPLATES`,  ,  ,
`PAGINATION_PATTERNS`, tuples of tuples,`''` , A set of patterns that are used to determine advanced pagination output.
`PATH`, dirspec , `${PWD}/content`, Where you keep all your original, unformatted website contents at (mostly Markdowns/RST/images documents).
`PATH_KEY`,  ,  ,
`PATH_METADATA`, string , `''`, Like `FILENAME_METADATA`, but parsed from a page's full path relative to the content source directory. See Path metadata.
`PDF_PROCESSOR`, boolean , `False`,
`PDF_STYLE`, string , `''`,
`PDF_STYLE_PATH`, string , `''`,
`PELICAN_CLASS`,  ,  ,
`PLUGINS`, list of string , `[]`, The list of plugins to load. See [Plugins](https://docs.getpelican.com/en/3.6.3/plugins.html#plugins).
`PLUGIN_PATHS`, list of abs\_filespec , (must define) ,
`PORT`, integer , `8000`,  Port number of TCP socket to use
`PYGMENTS_RST_OPTIONS`, dict of items , `{}`, A list of default Pygments settings for your reStructuredText code blocks. See [Syntax highlighting](https://docs.getpelican.com/en/3.6.3/content.html#internal-pygments-options) for a list of supported options.
`READERS`, dict of str , `{'html': None}`, A list of special readers, keyed by filetype.  A dictionary of file extensions / Reader classes for Pelican to process or ignore. For example, to avoid processing '`.html`' files, set: `READERS = {'html': None}`. To add a custom reader for the foo extension, set: `READERS = {'foo': FooReader}`
`RELATIVE_URLS`, boolean , `False`, Defines whether Pelican should use document-relative URLs or not. Only set this to `True` when developing/testing and only if you fully understand the effect it can have on links/feeds.  Never used in publish mode.
`REVERSE_CATEGORY_ORDER`, boolean , `False`, Reverse the category order. (`True`: lists by reverse alphabetical order; default lists alphabetically.)
`RSS_FEED_SUMMARY_ONLY`, boolean , True , RSS outputs only the summary of chronological ('articles') contents.
`SITE_DIR`, dirname , (must define) ,
`SITE_SUBPATH`, dirname , `$SITE_DIR/`,
`SITEMAP`, dict of items , , 
`SITENAME`, string , (must define) , The formal name of your website
`SITESUBTITLE`, dict of items , , 
`SITEURL`, url , (must define) , The top-level part of the destination URL. Base URL of your website. Not defined by default, so it is best to specify your `SITEURL`; if you do not then feeds will not be generated with properly-formed URLs. You should include http:// and your domain along with no trailing slash at the end. Example: `SITEURL = 'http://mydomain.com'`
`SLUG_SUBSTITUTIONS`, list of tuples, `[]`, Substitutions to make prior to stripping out non-alphanumerics when generating slugs. Specified as a list of 2-tuples of (from, to) which are applied in order.
`SLUGIFY_SOURCE`, string , `'title'`, The process of turning a content file into a slug name is based on one of two options: `'basename'` or `'title'`.  Specifies where you want the slug to be automatically generated from. Can be set to title to use the `Title:` metadata tag or `basename` to use the article's file name when creating this slug.
`SLUG_REGEX_SUBSTITUTION`,  ,  ,
`STATIC_CHECK_IF_MODIFIED`,  ,  ,
`STATIC_CREATE_LINKS`,  ,  ,
`STATIC_EXCLUDE`, list of filespec  , `''`, A list of files to be excluded if found in `STATIC_PATHS`.
`STATIC_EXCLUDE_SOURCES`, boolean , `True`, Ignore the source files.
`STATIC_PATHS`, list of dirspec , `''`, A list of relative subdirectory(s) that are not to be pre-processed and copied as-is.  A list of directories (relative to `$PATH`) in which to look for static files. Such files will be copied to the output directory without modification. Articles, pages, and other content source files will normally be skipped, so it is safe for a directory to appear both here and in `PAGE_PATHS` or `ARTICLE_PATHS`. Pelican's default settings include the "`images`" directory here.
`STATIC_URL`, dirspec , `'{path}'`, (Per-file save\_as and url overrides can
still be set in `EXTRA_PATH_METADATA`.)
`STATIC_SAVE_AS`, dirspec , `'{path}'`, (Per-file save\_as and url overrides can still be set in `EXTRA_PATH_METADATA`.)
`STATIC_CREATE_LINKS`, boolean , `False`,
`STATIC_CHECK_IF_MODIFIED`, boolean , `True`,
`SUMMARY_MAX_LENGTH`, integer , `50`, If you do not explicitly specify summary metadata for a given post, the `SUMMARY_MAX_LENGTH` setting can be used to specify how many words from the beginning of an article are used as the summary.  When creating a short summary of an article then this will be the default length (measured in words) of the text created. This only applies if your content does not otherwise specify a summary. Setting to `None` will cause the summary to be a copy of the original content.
`TAG_CLOUD_BADGE`, boolean , `True`, 
`TAG_CLOUD_MAX_ITEMS`, integer , `100`, 
`TAG_CLOUD_SORTING`, string , `size`, 
`TAG_CLOUD_STEPS`, integer , `10`, 
`TAG_FEED_ATOM`, dirspec , `None`, Relative URL to output the tag Atom feed. It should be defined using a `"%s"` match in the tag name.
`TAG_FEED_ATOM_URL`, dirspec , `None`,
`TAG_FEED_RSS`, dirspec , `None`, Relative URL to output the tag RSS feed. It
should be defined using a `"%s"` match in the tag name.
`TAG_FEED_RSS_URL`, dirspec , `None`,
`TAG_SAVE_AS`, dirspec , `'tags/{slug}.html'`, The location to save the tag page.
`TAG_URL`, dirspec , `'tags/{slug}.html'`, The URL to use for a tag.  
`TAGS_SAVE_AS`, dirspec , `'tags/index.html'`, The location to save the tag list.
`TAGS_URL`, dirspec , `'tags/index.html'`, The URL to use the tag list.
`TAGS_URL_PATH`, dirspec , `'tags'`, the file path to use inside HTML links.
`TEMPLATE_EXTENSIONS`, list of string , `['html']`,
`TEMPLATE_PAGES`, dict of items ,  , Useful for a different styled home page.  A mapping containing template pages that will be rendered with the blog entries. See [Template](https://docs.getpelican.com/en/3.6.3/settings.html#template-pages) pages.
`THEME`, dirpath, `'theme'`, Directory location of a selected theme. Theme to use to produce the output. Can be a relative or absolute path to a theme folder, or the name of a default theme or a theme installed via pelican-themes.
`THEME_STATIC_DIR`, dirpath , `''`, Destination directory in the output path where Pelican will place the files collected from THEME_STATIC_PATHS. Default is theme.
`THEME_STATIC_PATHS`, list of dirspec , `['static']`, Static theme paths you want to copy. Default value is static, but if your theme has other static paths then you can put them here. If files or directories with the same names are included in the paths defined in this settings then they will be progressively overwritten.
`THEME_TEMPLATES`,  ,  ,
`THEME_TEMPLATES_OVERRIDES`, list of filespec , `[]`,
`TIMEZONE`, string , (must define) , The timezone used in the date information, to generate Atom and RSS feeds. See the Timezone section below for more info.
`TRANSLATION_FEED_ATOM`, string , `None`, Where to put the Atom feed for translations.
`TRANSLATION_FEED_RSS`, string , `None`, Where to put the RSS feed for translations.
`TRANSLATION_FEED_RSS_URL`, string , `None`, {lang} denotes the two-letter ISO country
`TYPOGRIFY`, boolean , `False`,  Perform spelling correction and proper hypenation.  If set to `True`, several typographical improvements will be incorporated into the generated HTML via the Typogrify library, which can be installed via: `pip install typogrify`
`TYPOGRIFY_IGNORE_TAGS`, list of string , `['pre', 'code']`, A list of tags for Typogrify to ignore. By default Typogrify will ignore `pre` and `code` tags. This requires that Typogrify version 2.0.4 or later is installed
`USE_FOLDER_AS_CATEGORY`, boolean , `True`, If you would like to organize your files in other ways where the name of the subfolder would not be a good category name, you can set the setting USE_FOLDER_AS_CATEGORY to False.   When you don't specify a category in your post metadata; set this setting to True; and organize your articles in subfolders; the subfolder will become the category of your post. If set to False; DEFAULT_CATEGORY will be used as a fallback.
`WITH_FUTURE_DATES`, boolean , False , If `False`, contents with metadata date that are in the future will get a default status of "`draft`". See [Reading only modified content](https://docs.getpelican.com/en/3.6.3/settings.html#reading-only-modified-content) for caveats.
`WRITE_SELECTED`, list of string , `[]`, If this list is not empty then only output files with their paths in this list get written into the output directory. Paths should be either absolute or relative to the current Pelican working directory. For possible use cases see [Writing only selected content](https://docs.getpelican.com/en/3.6.3/settings.html#writing-only-selected-content).
`YEAR_ARCHIVE_SAVE_AS`, dirspec , `''`, The location to save per-year archives of your posts.
`YEAR_ARCHIVE_URL`, dirspec , `''`, The URL to use per-year archives of your posts.
[/jtable]


