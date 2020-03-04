#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import sys
import importlib

DEBUG =  True

AUTHOR = 'egbert'

#  SITENAME - Your site name.  Used as {{ SITENAME }} in
#  templates or during FEED generate_outputs.
#*default*  SITENAME = ''
SITENAME = 'Egbert Networks'

#  SITEURL - Base URL of your web site. Not defined
#  by default, so it is best to specify your SITEURL;
#  if you do not, feeds will not be generated with
#  properly-formed URLs. If your site is available
#  via HTTPS, this setting should begin with
#  https:// — otherwise use http://. Then append your
#  domain, with no trailing slash at the end.
#  Example: SITEURL = 'https://example.com'
#  Used in most themed template files.
SITEURL = 'https://egbert.net'

#  PATH - Path to content directory to be processed
#  by Pelican. If undefined, and content path is not
#  specified via an argument to the pelican command,
#  Pelican will use the current working directory.
#*default*  PATH = '.'
PATH = 'content'

# MY_TEMPLATE_IS = 'bootstrap3'
MY_TEMPLATE_IS = 'm.css'


TIMEZONE = 'America/Los_Angeles'

#  DEFAULT_LANG used in base.html as <html lang=> declarector value.
DEFAULT_LANG = 'en'

#  LOG_FILTER - A list of tuples containing the
#  logging level (up to warning) and the message to
#  be ignored.
#  Example:
#    LOG_FILTER = [(logging.WARN, 'TAG_SAVE_AS is set to False')]
#*default*  LOG_FILTER = []
LOG_FILTER = [] # [(logging.DEBUG)]


# main.__init__()/run.__init__()/get_generator_classes()

######################################################
#  NETWORK SERVER
######################################################
PORT = 8000
BIND = '127.0.0.1'

#
#  TEMPLATE_PAGES - A mapping containing template
#  pages that will be rendered with the blog
#  entries. See Template pages.
#  https://docs.getpelican.com/en/stable/settings.html#template-pages
#
#  If you want to generate custom pages besides your
#  blog entries, you can point any Jinja2 template
#  file with a path pointing to the file and the
#  destination path for the generated file.
#
#  For instance, if you have a blog with three static
#  pages — a list of books, your resume, and a
#  contact page — you could have:
#
#    TEMPLATE_PAGES = {'src/books.html': 'dest/books.html',
#                      'src/resume.html': 'dest/resume.html',
#                      'src/contact.html': 'dest/contact.html'}
#  Yes, metadata do get translated here for they're not static-static
#
#*default*  TEMPLATE_PAGES = None
TEMPLATE_PAGES = {
    'extra/root_home_page.html': './index.html',
    }

#  OUTPUT_SOURCES - Set to True if you want to copy
#  the articles and pages in their original format
#  (e.g. Markdown or reStructuredText) to the
#  specified OUTPUT_PATH.
#*default*  OUTPUT_SOURCES = False
OUTPUT_SOURCES = False

# ArticlesGenerator.__init__.CachingGenerator.__init__

#  CACHE_CONTENT - Enable caching.
#  Also enables the selection of CONTENT_CACHING_LAYER.
#*default*  CACHE_CONTENT = False
CACHE_CONTENT = False

#  CONTENT_CACHING_LAYER - Set to either 'generator'
#  or 'reader' for selection of caching mechanism.
#  This setting is ignored if CACHE_CONTENT is False.
#*default*  CONTENT_CACHING_LAYER = 'reader'
CONTENT_CACHING_LAYER = 'reader'


# ArticlesGenerator.__init__.CachingGenerator.__init__.Generator.__init__()


#  THEME_TEMPLATES_OVERRIDES - A list of paths you
#  want Jinja2 to search for templates before
#  searching the theme’s templates/ directory.
#  Allows for overriding individual theme template
#  files without having to fork an existing theme.
#  Jinja2 searches in the following order: files in
#  THEME_TEMPLATES_OVERRIDES first, then the
#  theme’s templates/.
#
#  You can also extend templates from the theme using
#  the {% extends %} directive utilizing the !theme
#  prefix as shown in the following example:
#
#    {% extends '!theme/article.html' %}
#*default*  THEME_TEMPLATES_OVERRIDES = []
THEME_TEMPLATES_OVERRIDES = []

#  JINJA_ENVIRONMENT - A dictionary of custom Jinja2
#  environment variables you want to use. This also
#  includes a list of extensions you may want to
#  include. See Jinja Environment documentation.
#  https://jinja.palletsprojects.com/en/master/api/#jinja2.Environment
#*default*  JINJA_ENVIRONMENT = {'trim_blocks': True, 'lstrip_blocks': True}
JINJA_ENVIRONMENT = {
    'extensions': [
#        'jinja2.ext.i18n'
    ],
    'trim_blocks': True,
    'lstrip_blocks': True
}

#  JINJA_FILTERS - A dictionary of custom Jinja2
#  filters you want to use. The dictionary should map
#  the filtername to the filter function.
#  Example:
#
#    JINJA_FILTERS = {'urlencode': urlencode_filter}
#  See Jinja custom filter documentation.
#  https://jinja.palletsprojects.com/en/2.11.x/api/#custom-filters
#*default*  JINJA_FILTERS = {}
JINJA_FILTERS = {}

# SitemapGenerator.__init__()
SITEMAP =  {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5},
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'monthly',
        'pages': 'weekly'}}

# PLUGIN - pdf_processor

PDF_PROCESSOR =  False
PDF_STYLE =  ''
PDF_STYLE_PATH =  ''

# run.__init__()

#  DELETE_OUTPUT_DIRECTORY - Delete the output
#  directory, and all of its contents, before
#  generating new files. This can be useful in
#  preventing older, unnecessary files from persisting
#  in your output. However, this is a destructive
#  setting and should be handled with extreme care.
#*default*  DELETE_OUTPUT_DIRECTORY = False
DELETE_OUTPUT_DIRECTORY = False

# OUTPUT_PATH - Where to output the generated files.
#*default*  OUTPUT_PATH = 'output/'
OUTPUT_PATH = '/home/steve/work/github/egberts.github.io-src/output'

#  OUTPUT_RETENTION - A list of filenames that should
#  be retained and not deleted from the output
#  directory. One use case would be the preservation
#  of version control data.
#*default*  OUTPUT_RETENTION = []
OUTPUT_RETENTION = []

#  ArticlesGenerator.get_file()

#  IGNORE_FILES - A list of glob patterns. Files and
#  directories matching any of these patterns will be
#  ignored by the processor. For example, the
#  default ['.#*'] will ignore emacs lock files,
#  and ['__pycache__'] would ignore Python 3’s
#  bytecode caches.
#*default*  IGNORE_FILES = ['.#']
IGNORE_FILES = ['.#*', '.ipynb_checkpoints', '__pycache__']


######################################################
#  ArticlesGenerator.generate_context()
######################################################

#  ARTICLE_PATHS - A list of directories and files to
#  look at for articles, relative to PATH.
#*default*  ARTICLE_PATHS = ['']
ARTICLE_PATHS = ['articles']

#  ARTICLE_EXCLUDES - A list of directories to exclude
#  when looking for articles in addition to PAGE_PATHS.
#*default*  ARTICLE_EXCLUDES = []
ARTICLE_EXCLUDES = ['pages']

######################################################
#  ArticlesGenerator.generate_context.default_metadata()
######################################################

#  DEFAULT_CATEGORY - The default category to fall
#  back on.
#*default*  DEFAULT_CATEGORY = 'misc'
DEFAULT_CATEGORY = 'misc'

#  DEFAULT_DATE - The default date you want to use.
#  If 'fs', Pelican will use the file system
#  timestamp information (mtime) if it can’t get
#  date information from the metadata. If given any
#  other string, it will be parsed by the same method
#  as article metadata. If set to a tuple object, the
#  default datetime object will instead be generated
#  by passing the tuple to the datetime.datetime
#  constructor.
#*default*  DEFAULT_DATE = None
DEFAULT_DATE = None

######################################################
#  ArticlesGenerator.generate_context.path_metadata()
######################################################

#  EXTRA_PATH_METADATA = {}
#  EXTRA_PATH_METADATA - Extra metadata dictionaries
#  keyed by relative path. Relative paths require
#  correct OS-specific directory separators
#  (i.e. / in UNIX and \ in Windows) unlike some
#  other Pelican file settings. Paths to a directory
#  apply to all files under it.
#  The most-specific path wins conflicts.
#
#  Not all metadata needs to be embedded in source
#  file itself. For example, blog posts are often
#  named following a YYYY-MM-DD-SLUG.rst pattern, or
#  nested into YYYY/MM/DD-SLUG directories. To
#  extract metadata from the filename or path, set
#  FILENAME_METADATA or PATH_METADATA to regular
#  expressions that use Python’s group name
#  notation (?P<name>...). If you want to attach
#  additional metadata but don’t want to encode it in
#  the path, you can set EXTRA_PATH_METADATA:
#
# EXTRA_PATH_METADATA = {
#     'relative/path/to/file-1': {
#         'key-1a': 'value-1a',
#         'key-1b': 'value-1b',
#         },
#     'relative/path/to/file-2': {
#         'key-2': 'value-2',
#         },
#     }
#
#  This can be a convenient way to shift the installed
#  location of a particular file:
#
#      # Take advantage of the following defaults
#      # STATIC_SAVE_AS = '{path}'
#      # STATIC_URL = '{path}'
#      STATIC_PATHS = [
#          'static/robots.txt',
#          ]
#      EXTRA_PATH_METADATA = {
#          'static/robots.txt': {'path': 'robots.txt'},
#          }
#  Note:  Also THEME_STATIC_DIR does mass-relocation
#         of its subdirectories (/fonts, /images, /css)
#         so no need to specify theme-related files
#         in EXTRA_PATH_METADATA.
EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'css/custom.css'},
    'extra/robots.txt': {'path': './robots.txt'},
    'extra/keybase.txt': {'path': './keybase.txt'},
    'extra/ss-css.css': {'path': 'css/ss-css.css'},
    'extra/ss-site.css': {'path': 'css/ss-site.css'},
    'extra/ss-squarespace-font.css': {'path': 'css/ss-squarespace-font.css'},
}

######################################################
#  ArticlesGenerator.generate_context.parse_path_metadata()
######################################################

#  FILENAME_METADATA - The regexp that will be used
#  to extract any metadata from the filename. All
#  named groups that are matched will be set in the
#  metadata object. The default value will only
#  extract the date from the filename.
#  For example, to extract both the date and the slug:
#    FILENAME_METADATA = r'(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'
#  See also SLUGIFY_SOURCE.
#*default*  FILENAME_METADATA = r'(?P<date>d{4}-d{2}-d{2}).*'
FILENAME_METADATA = '(?P<date>\\d{4}-\\d{2}-\\d{2}).*'

#  PATH_METADATA - Like FILENAME_METADATA, but parsed
#  from a page’s full path relative to the content
#  source directory.
#*default*  PATH_METADATA = ''
PATH_METADATA = ''

#  USE_FOLDER_AS_CATEGORY - When you don’t specify a
#  category in your post metadata, set this setting
#  to True, and organize your articles in subfolders,
#  the subfolder will become the category of your
#  post. If set to False, DEFAULT_CATEGORY will be
#  used as a fallback.
#*default*  USE_FOLDER_AS_CATEGORY = True
USE_FOLDER_AS_CATEGORY = True

######################################################
#  ArticlesGenerator.generate_context()
######################################################

#  TYPOGRIFY - If set to True, several typographical
#  improvements will be incorporated into the
#  generated HTML via the Typogrify library, which
#  can be installed via: pip install typogrify
#*default*  TYPOGRIFY = False
TYPOGRIFY = False

######################################################
#  ArticlesGenerator.generate_context.Article.__init__()
######################################################

#  WITH_FUTURE_DATES - If disabled, content with
#  dates in the future will get a default status of
#  draft. See Reading only modified content for
#  caveats.
#*default*  WITH_FUTURE_DATES = True
WITH_FUTURE_DATES = False

######################################################
#  PagesGenerator.generate_content_generators
######################################################

#  PAGE_PATHS - A list of directories and files to
#  look at for pages, relative to PATH.
#*default*  PAGE_PATHS = ['pages']
PAGE_PATHS = ['pages']

#  PAGE_EXCLUDES - A list of directories to exclude
#  when looking for pages in addition to
#  ARTICLE_PATHS.
#*default*  PAGE_EXCLUDES = []
PAGE_EXCLUDES = ['articles']

######################################################
#  PagesGenerator.generate_content_generators.read_file.default_metadata()
######################################################

#  DEFAULT_METADATA - The default metadata you want
#  to use for all articles and pages.
#*default*  DEFAULT_METADATA = {}
DEFAULT_METADATA = {}

######################################################
#  PagesGenerator.generate_content_generators.read_file.path_metadata()
######################################################

#  SLUGIFY_SOURCE - Specifies where you want the slug
#  to be automatically generated from. Can be set to
#  title to use the ‘Title:’ metadata tag or basename
#  to use the article’s file name when creating
#  the slug.
#*default*  SLUGIFY_SOURCE = 'title'
SLUGIFY_SOURCE = 'title'


#  SLUG_REGEX_SUBSTITUTIONS - Regex substitutions to
#  make when generating slugs of articles and pages.
#  Specified as a list of pairs of (from, to) which
#  are applied in order, ignoring case. The default
#  substitutions have the effect of removing
#  non-alphanumeric characters and converting
#  internal whitespace to dashes. Apart from these
#  substitutions, slugs are always converted to
#  lowercase ascii characters and leading and
#  trailing whitespace is stripped. Useful for
#  backward compatibility with existing URLs.
#*default* SLUG_REGEX_SUBSTITUTIONS = [
#*default*   (r'[^\w\s-]', ''), # remove non-alphabetical/whitespace/'-' chars
#*default*   (r'(?u)\A\s*', ''), # strip leading whitespace
#*default*   (r'(?u)\s*\Z', ''), # strip trailing whitespace
#*default*   (r'[-\s]+', '-'), # reduce multiple whitespace or '-' to single '-'
#*default*   ]
SLUG_REGEX_SUBSTITUTIONS = [('[^\\w\\s-]', ''), ('(?u)\\A\\s*', ''), ('(?u)\\s*\\Z', ''), ('[-\\s]+', '-')]

# AUTHOR_REGEX_SUBSTITUTIONS - Regex substitutions to
#  make when generating slugs of author pages.
AUTHOR_REGEX_SUBSTITUTIONS = SLUG_REGEX_SUBSTITUTIONS

# CATEGORY_REGEX_SUBSTITUTIONS - Regex substitutions to
#  make when generating slugs of categories pages.
CATEGORY_REGEX_SUBSTITUTIONS = SLUG_REGEX_SUBSTITUTIONS

# TAG_REGEX_SUBSTITUTIONS - Regex substitutions to
#  make when generating slugs of tags pages.
TAG_REGEX_SUBSTITUTIONS = SLUG_REGEX_SUBSTITUTIONS

#  DATE_FORMATS = {}
#  DATE_FORMATS - If you manage multiple languages,
#  you can set the date formatting here.
#
#  If no DATE_FORMATS are set, Pelican will fall back
#  to DEFAULT_DATE_FORMAT. If you need to maintain
#  multiple languages with different date formats,
#  you can set the DATE_FORMATS dictionary using the
#  language name (lang metadata in your post content)
#  as the key.
#
#  In addition to the standard C89 strftime format
#  codes that are listed in Python strftime
#  documentation, you can use the - character
#  between % and the format character to remove any
#  leading zeros. For example, %d/%m/%Y will
#  output 01/01/2014 whereas %-d/%-m/%Y will result
#  in 1/1/2014.
#
#       DATE_FORMATS = {
#           'en': '%a, %d %b %Y',
#           'jp': '%Y-%m-%d(%a)',
#       }
#
#  It is also possible to set different locale
#  settings for each language by using
#  a (locale, format) tuple as a dictionary value
#  which will override the LOCALE setting:
#
#       # On Unix/Linux
#       DATE_FORMATS = {
#           'en': ('en_US','%a, %d %b %Y'),
#           'jp': ('ja_JP','%Y-%m-%d(%a)'),
#       }
#
#       # On Windows
#       DATE_FORMATS = {
#           'en': ('usa','%a, %d %b %Y'),
#           'jp': ('jpn','%Y-%m-%d(%a)'),
#       }
#*default*  DATE_FORMATS = {}
DATE_FORMATS = {}

#  DEFAULT_DATE_FORMAT - The default date format
#  you want to use.
#*default*  DEFAULT_DATE_FORMAT = '%a %d %B %Y'
DEFAULT_DATE_FORMAT = '%a %d %B %Y'

######################################################
#  StaticGenerator.generate_context.read_file()
######################################################

#  STATIC_PATHS - A list of directories (relative to
#  PATH) in which to look for static files. Such
#  files will be copied to the output directory
#  without modification. Articles, pages, and other
#  content source files will normally be skipped, so
#  it is safe for a directory to appear both here and
#  in PAGE_PATHS or ARTICLE_PATHS. Pelican’s default
#  settings include the “images” directory here.
#
#  Absolutely need an entry in both STATIC_PATHS and
#  EXTRA_PATH_METADATA just to relocate a file.
#*default*  STATIC_PATHS = [ 'images' ]
STATIC_PATHS = [
    'images',
#    'static/images',
    'extra/robots.txt',
    'extra/keybase.txt',
    'extra/egbert.net.gpg',
    'extra/ss-css.css',
    'extra/ss-site.css',
    'extra/ss-squarespace-font.css',
    'fonts/poppins-regular.woff2',
    'fonts/poppins-light.woff2',
    'fonts/poppins-medium.woff2',
    'fonts/poppins-bold.woff2',
    'fonts/typekit1.woff2',
]

#  STATIC_EXCLUDES - A list of directories to exclude
#  when looking for static files.
#*default*  STATIC_EXCLUDES = []
STATIC_EXCLUDES = []

#  STATIC_EXCLUDE_SOURCES - If set to False, content
#  source files will not be skipped when copying
#  files found in STATIC_PATHS. This setting is for
#  backward compatibility with Pelican releases
#  before version 3.5. It has no effect unless
#  STATIC_PATHS contains a directory that is also in
#  ARTICLE_PATHS or PAGE_PATHS. If you are trying to
#  publish your site’s source files, consider using
#  the OUTPUT_SOURCES setting instead.
#*default*  STATIC_EXCLUDE_SOURCES = True
STATIC_EXCLUDE_SOURCES = True


######################################################
#  StaticGenerator.ArticlesGenerator.refresh_metadata_intrasite()
######################################################

#  FORMATTED_FIELDS - A list of metadata fields
#  containing reST/Markdown content to be parsed and
#  translated to HTML.
#*default*  FORMATTED_FIELDS = ['summary']
FORMATTED_FIELDS = ['summary', 'description', 'landing']


######################################################
#  ArticleGenerator.generate_output.generate_feeds()
######################################################

#  FEED_DOMAIN used in most templates' base.html as
#  URL in hyperlink reference (href=)
FEED_DOMAIN =  'egbert.net'

#  FEED_MAX_ITEMS - Maximum number of items allowed
#  in a feed. Feed item quantity is unrestricted by
#  default.
FEED_MAX_ITEMS = ''

RSS_FEED_SUMMARY_ONLY = True

FEED_ATOM = None
FEED_ATOM_URL = None
FEED_RSS = None
FEED_RSS_URL = None

#  FEED_ALL_ATOM used in most templates' base.html to
#  contain all ATOMs used within a template.
#  Type: FileSpec
FEED_ALL_ATOM = 'atom.xml'

FEED_ALL_RSS = None

ARTICLE_ORDER_BY = 'reversed-date'

#  FEED_ALL_ATOM_URL used in most templates' base.html
#  to contain an URL of all ATOMs.
#  Type: FileSpec
FEED_ALL_ATOM_URL = 'feeds/atom.xml'

FEED_ALL_RSS_URL = None

CATEGORY_FEED_ATOM = '{slug}.atom.xml'
CATEGORY_FEED_ATOM_URL = '/feeds/{slug}.atom.xml'
CATEGORY_FEED_RSS = None
CATEGORY_FEED_RSS_URL = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_ATOM_URL = None
AUTHOR_FEED_RSS = None
AUTHOR_FEED_RSS_URL = None
TAG_FEED_ATOM = None
TAG_FEED_ATOM_URL = None
TAG_FEED_RSS = None
TAG_FEED_RSS_URL = None
TRANSLATION_FEED_ATOM = None
TRANSLATION_FEED_ATOM_URL = None
TRANSLATION_FEED_RSS = None
TRANSLATION_FEED_RSS_URL = None

######################################################
#  ArticleGenerator.generate_output.generate_pages()
######################################################

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
RELATIVE_URLS = True

######################################################
#  ArticleGenerator.generate_output.generate_pages.generate_articles()
######################################################

TEMPLATE_EXTENSIONS = ['.html']

######################################################
#  .generate_output.generate_pages.generate_articles.write_file()
######################################################

PAGINATED_TEMPLATES = {
    'index': None,
    'tag': None,
    'category': None,
    'author': None}

#  DEFAULT_PAGINATION used in pagination.html template.
DEFAULT_PAGINATION = 20

######################################################
#  .generate_output.generate_pages.generate_period_archives()
######################################################

YEAR_ARCHIVE_SAVE_AS = ''
MONTH_ARCHIVE_SAVE_AS = ''
DAY_ARCHIVE_SAVE_AS = ''

YEAR_ARCHIVE_URL = ''
MONTH_ARCHIVE_URL = ''
DAY_ARCHIVE_URL = ''

######################################################
#  .generate_output.generate_pages.generate_direct_templates()
######################################################

DIRECT_TEMPLATES = ('index', 'categories', 'tags', 'archives', 'authors')

# If there is no XXXX_SAVE_AS, then file will not get written
INDEX_SAVE_AS = 'blog/articles/index.html'
# INDEX_URL = ''

CATEGORIES_SAVE_AS = 'blog/categories/index.html'
CATEGORIES_URL = 'blog/categories/index.html'
TAGS_SAVE_AS = 'blog/tags/index.html'
TAGS_URL = 'blog/tags/index.html'
ARCHIVES_SAVE_AS = 'blog/archives/index.html'
ARCHIVES_URL = 'blog/archives/index.html'
AUTHORS_SAVE_AS = 'blog/authors/index.html'
AUTHORS_URL = 'blog/authors/index.html'

######################################################
#  StaticGenerator.generate_output
######################################################

#  THEME_STATIC_PATHS - Static theme paths you want
#  to copy. Default value is static, but if your
#  theme has other static paths, you can put them
#  here. If files or directories with the same names
#  are included in the paths defined in this
#  settings, they will be progressively overwritten.
#*default*  THEME_STATIC_PATHS = ['static']
# THEME_STATIC_PATHS = ['static/images', 'static/js', 'static/css', 'static/media', 'static/fonts']

#  THEME_STATIC_DIR - Destination directory in the
#  output path where Pelican will place the files
#  collected from THEME_STATIC_PATHS.'
#*default*  THEME_STATIC_DIR = 'theme'
THEME_STATIC_DIR = ''

#  READERS - A dictionary of file extensions / Reader
#  classes for Pelican to process or ignore.
#  For example, to avoid processing .html files, set:
#     READERS = {'html': None}
#  Other options are:
#     READERS = {'asc': None}
#*default*  READERS = {}
READERS = {'html': None}

#  MARKDOWN - Extra configuration settings for the
#  Markdown processor. Refer to the Python Markdown
#  documentation’s Options section for a complete
#  list of supported options. The extensions option
#  will be automatically computed from the
#  extension_configs option.
#*default*  MARKDOWN = {
#*default*   'extension_configs': {
#*default*     'markdown.extensions.codehilite': {'css_class': 'highlight'},
#*default*     'markdown.extensions.extra': {},
#*default*     'markdown.extensions.meta': {},
#*default*   },
#*default*   'output_format': 'html5',
#*default* }
MARKDOWN = {
  'extension_configs': {
    'markdown.extensions.smarty': {},
    'markdown.extensions.extra': {},
    'markdown.extensions.footnotes': {},
    'markdown.extensions.meta': {},
    'markdown.extensions.toc': {'baselevel': 1},
    'markdown.extensions.codehilite': {'css_class': 'codehilite'}
  },
  'output_format': 'html5'}


# XXXXXXXXXXXX
#  PLUGIN_PATHS - A list of directories where to look
#  for plugins. See Plugins.
#*default*  PLUGIN_PATHS = []
PLUGIN_PATHS = [ 'plugins', 'm.css/plugins/m' ]

#  PLUGINS - The list of plugins to load.
#  See Plugins.
#*default*  PLUGINS = []
PLUGINS = [
#          'i18n_subsites',
          'collate_content',
          'sitemap',
          'dateish',
          'tag_cloud',
          'alias',
          'htmlsanity',
          'just_table',
          'code_include',
]

######################################################
#  PLUGINS - Plugin-specific configurations
######################################################
JTABLE_SEPARATOR = ","

TAG_CLOUD_BADGE = True
TAG_CLOUD_MAX_ITEMS = 100
TAG_CLOUD_SORTING = 'size'
TAG_CLOUD_STEPS = 10

PYGMENTS_STYLE =  'paraiso-dark'
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}


#  DISPLAY_PAGES_ON_MENU used in most templates'
#  base.html file.
#*default*  DISPLAY_PAGES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = True

#  DISPLAY_CATEGORIES_ON_MENU used in most templates'
#  base.html file.
#*default*  DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True

HTML_META_NAMES = {
    ('keywords', 'Egbert, Egbert.net, Cybersecurity, Software Engineering'),
    ('viewport', 'width=device-width,initial-scale=1.0'),
    ('theme-color', '#419a1c'),
    ('google', 'nositelinksearchbox'),
    ('google-site-verification', 'not-given'),
    ('twitter:card', 'summary'),
    ('twitter:site:id', '12345678'),
}

#  OUTPUT_SOURCES_EXTENSION = '.text'
#  OUTPUT_SOURCES_EXTENSION - Controls the extension
#  that will be used by the SourcesGenerator.
#  If not a valid string the default value will be
#  used.
#*default*  OUTPUT_SOURCES_EXTENSION = '.text'
OUTPUT_SOURCES_EXTENSION = '.txt'

NEWEST_FIRST_ARCHIVES = True
REVERSE_CATEGORY_ORDER = False
ARTICLE_URL = 'blog/articles/{slug}.html'
ARTICLE_SAVE_AS = 'blog/articles/{slug}.html'
ARTICLE_LANG_URL = '{slug}-{lang}.html'
ARTICLE_LANG_SAVE_AS = '{slug}-{lang}.html'
DRAFT_URL = 'blog/drafts/articles/{slug}.html'
DRAFT_SAVE_AS = 'blog/drafts/articles/{slug}.html'
DRAFT_LANG_URL = 'drafts/{slug}-{lang}.html'
DRAFT_LANG_SAVE_AS = 'drafts/{slug}-{lang}.html'
PAGE_URL = 'blog/pages/{slug}.html'
PAGE_SAVE_AS = 'blog/pages/{slug}.html'
PAGE_ORDER_BY = 'date'
PAGE_LANG_URL = 'pages/{slug}-{lang}.html'
PAGE_LANG_SAVE_AS = 'pages/{slug}-{lang}.html'
DRAFT_PAGE_URL = 'blog/drafts/pages/{slug}.html'
DRAFT_PAGE_SAVE_AS = 'blog/drafts/pages/{slug}.html'
DRAFT_PAGE_LANG_URL = 'drafts/pages/{slug}-{lang}.html'
DRAFT_PAGE_LANG_SAVE_AS = 'drafts/pages/{slug}-{lang}.html'
STATIC_URL = '{path}'
STATIC_SAVE_AS = '{path}'
CATEGORY_URL = 'blog/categories/{slug}.html'
CATEGORY_SAVE_AS = 'blog/categories/{slug}.html'
TAG_URL = 'blog/tags/{slug}.html'
TAG_SAVE_AS = 'blog/tags/{slug}.html'
AUTHOR_URL = 'blog/authors/{slug}.html?and&in&url=""'
AUTHOR_SAVE_AS = 'blog/authors/{slug}.html'
ARTICLE_TRANSLATION_ID = 'slug'
PAGE_TRANSLATION_ID = 'slug'


LOCALE = ['']
DEFAULT_ORPHANS = 0

# The default metadata you want to use for all articles and pages.
ARTICLE_PERMALINK_STRUCTURE = ''
SUMMARY_MAX_LENGTH = 50
INTRASITE_LINK_REGEX = '[{|](?P<what>.*?)[|}]'
CACHE_PATH = 'cache'
GZIP_CACHE = False
CHECK_MODIFIED_METHOD = 'mtime'
LOAD_CONTENT_CACHE = False
WRITE_SELECTED = []


#  STATIC_CREATE_LINKS - Create links instead of
#  copying files. If the content and output
#  directories are on the same device, then create
#  hard links. Falls back to symbolic links if the
#  output directory is on a different filesystem.
#  If symlinks are created, don’t forget to add
#  the -L or --copy-links option to rsync when
#  uploading your site.
#*default*  STATIC_CREATE_LINKS = False
STATIC_CREATE_LINKS = False

#  STATIC_CHECK_IF_MODIFIED - If set to True, and
#  STATIC_CREATE_LINKS is False, compare mtimes of
#  content and output files, and only copy content
#  files that are newer than existing output files.
#*default*  STATIC_CHECK_IF_MODIFIED = False
STATIC_CHECK_IF_MODIFIED = True


##################################################^^^


ARCHIVES_DIRNAME = 'archives'
ARCHIVES_URL_PATH = 'blog/archives'
ARCHIVE_SAVE_AS = 'blog/archives/{slug}.html'
ARCHIVE_URL = 'blog/archives/{slug}.html'
ARTICLES_DIRNAME = 'articles'
ARTICLES_URL = 'blog/articles/index.html'
ARTICLES_URL_PATH = 'blog/articles'

AUTHORS_DIRNAME = 'authors'
AUTHORS_URL_PATH = 'blog/authors'

CATEGORIES_DIRNAME = 'categories'
CATEGORIES_TO_COLLATE = ['category-of-interest', 'another-cool-category']
CATEGORIES_URL_PATH = 'blog/categories'
# CUSTOM_CSS = 'css/custom.css'
DESCRIPTION = 'Egbert Networks conducts researches on bleeding edges of malicious behaviors and its applicability toward multiple compiler languages.  Researching for many customers.'
DRAFTS_DIRNAME = 'drafts'
DRAFTS_SAVE_AS = 'blog/drafts/index.html'
DRAFTS_URL = 'blog/drafts/articles/index.html'

DRAFT_ARTICLES_DIRNAME = 'drafts/articles'
DRAFT_ARTICLES_SAVE_AS = 'blog/drafts/pages/index.html'
DRAFT_ARTICLES_URL = 'blog/drafts/pages/index.html'
DRAFT_ARTICLES_URL_PATH = 'blog/drafts/articles'

DRAFT_PAGES_DIRNAME = 'drafts/pages'
DRAFT_PAGES_SAVE_AS = 'blog/drafts/pages/index.html'
DRAFT_PAGES_URL = 'blog/drafts/pages/index.html'
DRAFT_PAGES_URL_PATH = 'blog/drafts/pages'

EACH_SLUG_HAS_SUBDIR = False

MINIBIO =  'Just a high-speed network backend kind of guy doing deep processing of compiler languages, and detection of malwares'
PAGES_DIRNAME =  'pages'
PAGES_SAVE_AS =  'blog/pages/index.html'
PAGES_URL =  'blog/pages/index.html'
PAGES_URL_PATH =  'blog/pages'
SITE_DIR =  'blog/'
SITE_SUBPATH =  'blog'
SITE_URL_TOP_LVL =  'blog/'
TAGS_DIRNAME = 'tags'
TAGS_URL_PATH = 'blog/tags'

SITESUBTITLE = ''

######################################################
##  Bootstrap3-specific                             ##
######################################################

if MY_TEMPLATE_IS == 'bootstrap3':
    THEME = 'm.css/egbert-theme'
    HIDE_SITENAME = True
    THEME_COLOR = '#22272e'
    BRAND_URL = 'blog/index.html'
    # CSS_FILE = 'main.css'
    FAVICON = 'images/egbert-network.png'
    SITELOGO =  'images/egbert_network_logo.png'
    SITELOGO_SIZE =  100
    #  MENUITEMS display menu items on HTML header section.
    MENUITEMS = [('Blog', 'blog'),
                 ('Articles', 'blog/articles'),
                 ('Tags', 'blog/tags')]
    LINKS = (('Pelican', 'http://getpelican.com/'),
             ('SPLIT-CODE.COM', 'http://split-code.com/external_blogs.html'),
             ('Hexacorn', 'http://www.hexacorn.com/blog/'),
             ('Möbius Strip RE', 'https://www.msreverseengineering.com/blog/'),
             ("Dr. Fu's", 'http://fumalwareanalysis.blogspot.com/p/malware-analysis-tutorials-reverse.html'),
             ('Metova', 'https://metova.com/category/security/'),
             ('Quarkslab', 'https://blog.quarkslab.com/category/reverseengineering.html'),
             ('Reddit RE', 'https://www.reddit.com/r/ReverseEngineering/comments/is2et/can_we_collect_interesting_reverse_engineering/'),
             ('0x1338', 'http://0x1338.blogspot.com/'))
    # `GOOGLE_ANALYTICS` (classic tracking code)
    # `GOOGLE_ANALYTICS_UNIVERSAL` and
      # `GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY` (Universal tracking code)
    # `DISQUS_SITENAME`
    # `PIWIK_URL`, `PIWIK_SSL_URL` and `PIWIK_SITE_ID`
    # GITHUB_URL
    # FACEBOOK_APPID
    # TWITTER_USERNAME
    # FQ_SITEURL
    SEARCH_BASE_URL = 'https://egbert.net/'
    SEARCH_EXTERNAL_URL = 'https://google.com/search?q=site:egbert.net+{query}'
    DUCKDUCKGO_CUSTOM_SEARCH_SIDEBAR = True
    GOOGLE_ANALYTICS = ''
    TWITTER_USERNAME = 'egbertst'
    SOCIAL = (
        ('fab fa-github-square', 'https://github.com/egberts'),
        ('fab fa-stack-overflow', 'https://stackoverflow.com/users/4379130/egbert-s')
    )
    SOCIAL_LABELS = (
        ('Twitter', 'fab fa-twitter', 'https://twitter.com/egbertst'),
        ('GitHub', 'fab fa-github-square', 'https://github.com/egberts'),
        ('StackOverflow', 'fab fa-stack-overflow', 'https://stackoverflow.com/users/4379130/egbert-s'))

######################################################
##  M.CSS-specific                                  ##
######################################################

if MY_TEMPLATE_IS == 'm.css':
    THEME = 'm.css/egbert-theme'
    #  M_BLOG_DESCRIPTION used in archives.html
    M_BLOG_DESCRIPTION = 'Ranting and analysis of Egbert\' mind'

    #  M_BLOG_NAME used in archives.html, author.html,
    #  base_blog.html, category.html, tag.html, article.html,
    #
    M_BLOG_NAME = 'Egbert Blog'

    #  M_BLOG_URL used in archives.html, author.html,
    #  category.html, tag.html, article.html
    #
    M_BLOG_URL = 'blog'

    #  M_SOCIAL_BLOG_SUMMARY used in archives.html
    M_SOCIAL_BLOG_SUMMARY = 'summary of social blog'

    #  M_SOCIAL_BLOG_IMAGE used in archives.html,
    #  author.html, category.html, tag.html, article.html,
    #  page.html,
    M_SOCIAL_IMAGE = 'twitter.png'

    #  M_COLLAPSED_FIRST_ARTICLE used in archives.html, article_header.html
    M_COLLAPSE_FIRST_ARTICLE = False

    #  M_BLOG_FAVICON used in base_blog.html
    M_BLOG_FAVICON = [ 'images/blog_favicon.ico', 'image/x-icon' ]

    #  M_FAVICON used in base_blog.html, page.html
    M_FAVICON = ('images/favicon.ico', 'image/x-icon')

    #  M_SHOW_AUTHOR_LIST used in base_blog.html
    M_SHOW_AUTHOR_LIST = True

    #  M_DISABLE_SOCIAL_MEDIA_TAGS used in base_blog.html
    M_DISABLE_SOCIAL_META_TAGS = True

    #  M_CSS_FILES used in base_blog.html
    M_CSS_FILES =  [
        # 'https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,600,600i%7CSource+Code+Pro:400,400i,600',
        '../../css/m-dark.compiled.css',
        '../../css/pygments-dark.css',
        '../../css/tag_cloud.css',
        '../../css/justtable.css',
    ]

    #  M_THEME_COLOR used in base.html
    M_THEME_COLOR =  '#419a1c'

    #  M_SOCIAL_TWITTER_SITE used in base.html
    M_SOCIAL_TWITTER_SITE = '@egbertst'

    #  M_SOCIAL_TWITTER_SITE_ID used in base.html
    M_SOCIAL_TWITTER_SITE_ID = '123123123'

    #  M_HTML_HEADER used in base.html
    #  M_HTML_HEADER = ''

    #  M_SITE_LOGO used in base.html.
    M_SITE_LOGO = 'images/egbert_network_logo.png'

    #  M_SITE_LOGO_TEXT used in base.html.
    M_SITE_LOGO_TEXT = 'Egbert Network'

    #  M_LINKS_NAVBAR used in base.html.
    M_LINKS_NAVBAR1 = [
        ( 'Articles', 'blog/articles/index.html', 'articles', [] ),
        ( 'Category', 'blog/categories/index.html', 'categories', [] ),
        ( 'Archives', 'blog/archives/index.html', 'archives', [] ),
        ( 'Uses', 'blog/pages/uses.html', 'uses', [] ),
        ( 'About', 'blog/pages/about.html', 'about', [] ),
    ]

    M_LINKS_NAVBAR2 = []

    #  M_LINKS_FOOTER1 used in base.html.
    M_LINKS_FOOTER1 = [
        ( 'Privacy', 'blog/pages/privacy.html' ),
    ]

    #  M_LINKS_FOOTER2 used in base.html.
    # M_LINKS_FOOTER2 = [
    #     ( 'Privacy2', 'blog/pages/privacy.html' ),
    #     ( 'Site Map2', 'blog/pages/sitemap.html' ),
    # ]

    #  M_FINE_PRINT used in base.html.
    M_FINE_PRINT = None

    #  M_HIDE_ARTICLE_SUMMARY used in article_header.html,
    #  article.html,
    #
    M_HIDE_ARTICLE_SUMMARY = True

    #  M_ARCHIVED_ARTICLE_BADGE used in article.html
    M_ARCHIVED_ARTICLE_BADGE = ''

    #  M_NEWS_ON_INDEX used in page.html
    M_NEWS_ON_INDEX = ('Latest rants on our blog', 2)


######################################################
##  DOCUTILS-specific                               ##
######################################################

DOCUTILS_SETTINGS = {}

#  TYPOGRIFY_IGNORE_TAGS - A list of tags for
#  Typogrify to ignore. By default Typogrify will
#  ignore pre and code tags. This requires that
#  Typogrify version 2.0.4 or later is installed
#*default*  TYPOGRIFY_IGNORE_TAGS = []
TYPOGRIFY_IGNORE_TAGS = ['pre', 'code']

