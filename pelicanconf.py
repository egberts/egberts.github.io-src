#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'egbert'

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


ABSOLUTE_SITEURL = 'https://egbert.net'

#  PATH - Path to content directory to be processed
#  by Pelican. If undefined, and content path is not
#  specified via an argument to the pelican command,
#  Pelican will use the current working directory.
#*default* PATH = '.'
PATH = '/home/steve/work/github/egberts.github.io-src/content'
PATH = 'content'

THEME = '/home/steve/work/github/egberts.github.io-src/m.css/egbert-theme'

TIMEZONE = 'America/Los_Angeles'

#  DEFAULT_LANG used in base.html as <html lang=> declarector value.
DEFAULT_LANG = 'en'

######################################################
#  PLUGINS
######################################################
PLUGIN_PATHS = [
    '/home/steve/work/github/egberts.github.io-src/plugins',
    '/home/steve/work/github/egberts.github.io-src/m.css/plugins/m']
import sys
sys.path.insert(1, '/home/steve/work/github/egberts.github.io-src/m.css/plugins/m')
sys.path.insert(1, '/home/steve/work/github/egberts.github.io-src/plugins')
import alias
import collate_content
import sitemap
import just_table
import code_include
import tag_cloud
import htmlsanity
# import i18n_subsites
import dateish
PLUGINS = [
#          'i18n_subsites',
          collate_content,
          sitemap,
          dateish,
          tag_cloud,
          alias,
          htmlsanity,
          just_table,
          code_include,
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

JINJA_ENVIRONMENT = {
    'extensions': [
#        'jinja2.ext.i18n'
    ],
    'trim_blocks': True,
    'lstrip_blocks': True
}

JINJA_FILTERS = {}

######################################################
#  BaseReader
######################################################

######################################################
#  RstReader (filetype: .rst)
######################################################

######################################################
#  MarkdownReader (filetype: .md, .mkd, .mdown)
######################################################

######################################################
#  HTMLReader (filetype: .htm, .html)
######################################################

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True


# OUTPUT_PATH - Where to output the generated files.
#*default*  OUTPUT_PATH = 'output/'
OUTPUT_PATH = '/home/steve/work/github/egberts.github.io-src/output'

#  READERS - A dictionary of file extensions / Reader
#  classes for Pelican to process or ignore.
#  For example, to avoid processing .html files, set:
#     READERS = {'html': None}
#  Other options are:
#     READERS = {'asc': None}
#*default*  READERS = {}
READERS = {'html': None}

# THEME_STATIC_URL = 'blog/theme'
FEED_MAX_ITEMS = ''
RSS_FEED_SUMMARY_ONLY = True

#  DISPLAY_PAGES_ON_MENU used in most templates'
#  base.html file.
DISPLAY_PAGES_ON_MENU = True

#  DISPLAY_CATEGORIES_ON_MENU used in most templates'
#  base.html file.
DISPLAY_CATEGORIES_ON_MENU = True
DOCUTILS_SETTINGS = {}
OUTPUT_SOURCES = False
OUTPUT_SOURCES_EXTENSION = '.txt'

WITH_FUTURE_DATES = False
# CSS_FILE = 'main.css'
NEWEST_FIRST_ARCHIVES = True
REVERSE_CATEGORY_ORDER = False
ARTICLE_URL = 'blog/articles/{slug}.html'
ARTICLE_SAVE_AS = 'blog/articles/{slug}.html'
ARTICLE_ORDER_BY = 'reversed-date'
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
RELATIVE_URLS = True
ARTICLE_TRANSLATION_ID = 'slug'
PAGE_TRANSLATION_ID = 'slug'
THEME_TEMPLATES_OVERRIDES = []
PAGINATED_TEMPLATES = {
    'index': None,
    'tag': None,
    'category': None,
    'author': None}
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

LOG_FILTER = [] # [(logging.DEBUG)]
LOCALE = ['']
DEFAULT_ORPHANS = 0

# The default metadata you want to use for all articles and pages.
ARTICLE_PERMALINK_STRUCTURE = ''
SUMMARY_MAX_LENGTH = 50
TEMPLATE_PAGES = {
    'cover_page.html': 'index.html',
    }
INTRASITE_LINK_REGEX = '[{|](?P<what>.*?)[|}]'
CACHE_CONTENT = False
CONTENT_CACHING_LAYER = 'reader'
CACHE_PATH = 'cache'
GZIP_CACHE = False
CHECK_MODIFIED_METHOD = 'mtime'
LOAD_CONTENT_CACHE = False
WRITE_SELECTED = []
FORMATTED_FIELDS = ['summary', 'description', 'landing']

######################################################
# OUTPUT
######################################################

#  DELETE_OUTPUT_DIRECTORY - Delete the output
#  directory, and all of its contents, before
#  generating new files. This can be useful in
#  preventing older, unnecessary files from persisting
#  in your output. However, this is a destructive
#  setting and should be handled with extreme care.
#*default*  DELETE_OUTPUT_DIRECTORY = False
DELETE_OUTPUT_DIRECTORY = False

#  OUTPUT_RETENTION - A list of filenames that should
#  be retained and not deleted from the output
#  directory. One use case would be the preservation
#  of version control data.
#*default*  OUTPUT_RETENTION = []
OUTPUT_RETENTION = []

######################################################
#  GENERATORS - generate_context()
######################################################
# Absolutely need an entry in both STATIC_PATHS and ...
#  STATIC_PATHS - A list of directories (relative to
#  PATH) in which to look for static files. Such
#  files will be copied to the output directory
#  without modification. Articles, pages, and other
#  content source files will normally be skipped, so
#  it is safe for a directory to appear both here and
#  in PAGE_PATHS or ARTICLE_PATHS. Pelican’s default
#  settings include the “images” directory here.
#*default*  STATIC_PATHS = [ 'images' ]
STATIC_PATHS = [
    'images/apple-touch-icon.png',
    'images/Dhcprere.png',
    'images/pelican-2-git-repos.svg',
    'images/shell_interactive_vs_noninteractive.png',
    'images/systemd-dhclient.svg',
    'images/validated-egbert.net.png',
    'extra/robots.txt',
    'extra/keybase.txt',
    'extra/egbert.net.gpg',
    'extra/ss-css.css',
    'extra/ss-site.css',
    'extra/ss-squarespace-font.css',
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

# MarkdownGenerator
DEFAULT_METADATA = {}

#  DEFAULT_CATEGORY - The default category to fall
#  back on.
#*default*  DEFAULT_CATEGORY = 'misc'
DEFAULT_CATEGORY = 'misc'

DEFAULT_DATE_FORMAT = '%a %d %B %Y'

EXTRA_PATH_METADATA = {
    'static/images/apple-touch-icon.png': {'path': 'images/apple-touch-icon.png'},
    'm.css/egbert-theme/static/css/m-components.css': {'path': 'css/m-components.css'},
    'm.css/egbert-theme/static/css/m-dark.compiled.css': {'path': 'css/m-dark.css'},
    'm.css/egbert-theme/static/css/pygments-dark.css':
        {'path': 'css/pygments-dark.css'},
    'extra/tag_cloud.css': {'path': 'css/tag_cloud.css'},
    'extra/justtable.css': {'path': 'css/justtable.css'},
    'extra/custom.css': {'path': 'css/custom.css'},
    'extra/robots.txt': {'path': './robots.txt'},
    'extra/keybase.txt': {'path': './keybase.txt'},
    'extra/ss-css.css': {'path': 'css/ss-css.css'},
    'extra/ss-site.css': {'path': 'css/ss-site.css'},
    'extra/ss-squarespace-font.css': {'path': 'css/ss-squarespace-font.css'},
    'extra/homepage.html': {'path': 'blog/index.html'},
    # 'extra/cover.md': {'path': 'index.html'},
    # 'extra/cover_page.html': {'path': 'index.html'},
# CSS_FILE = 'css/m.dark.css'
}

# generate_context(XXXGenerator)/read_file()/parse_path_metadata()
FILENAME_METADATA = '(?P<date>\\d{4}-\\d{2}-\\d{2}).*'

PATH_METADATA = ''

USE_FOLDER_AS_CATEGORY = True

#  TYPOGRIFY - If set to True, several typographical
#  improvements will be incorporated into the
#  generated HTML via the Typogrify library, which
#  can be installed via: pip install typogrify
#*default*  TYPOGRIFY = False
TYPOGRIFY = False

#  TYPOGRIFY_IGNORE_TAGS - A list of tags for
#  Typogrify to ignore. By default Typogrify will
#  ignore pre and code tags. This requires that
#  Typogrify version 2.0.4 or later is installed
#*default*  TYPOGRIFY_IGNORE_TAGS = []
TYPOGRIFY_IGNORE_TAGS = ['pre', 'code']

SLUGIFY_SOURCE = 'title'

SLUG_REGEX_SUBSTITUTIONS = [('[^\\w\\s-]', ''), ('(?u)\\A\\s*', ''), ('(?u)\\s*\\Z', ''), ('[-\\s]+', '-')]

DATE_FORMATS = {}

######################################################
#  ArticlesGenerator
######################################################
ARTICLE_PATHS = ['articles']
ARTICLE_EXCLUDES = ['pages']

######################################################
#  PagesGenerator
######################################################
PAGE_PATHS = ['pages']
PAGE_EXCLUDES = ['articles']

######################################################
#  TemplatePagesGenerator
######################################################

######################################################
#  SitemapGenerator
######################################################

######################################################
#  AliasGenerator
######################################################

######################################################
#  GENERATORS - generate_output()
######################################################

# generate_output()/generate_feeds()

# Feed generation is usually not desired when developing

#  FEED_ALL_ATOM used in most templates' base.html to
#  contain all ATOMs used within a template.
#  Type: FileSpec
FEED_ALL_ATOM = 'atom.xml'

#  FEED_ALL_ATOM_URL used in most templates' base.html
#  to contain an URL of all ATOMs.
#  Type: FileSpec
FEED_ALL_ATOM_URL = 'feeds/atom.xml'
CATEGORY_FEED_ATOM = '{slug}.atom.xml'
CATEGORY_FEED_ATOM_URL = '/feeds/{slug}.atom.xml'
CATEGORY_FEED_RSS = None
CATEGORY_FEED_RSS_URL = None
TAG_FEED_ATOM = None
TAG_FEED_ATOM_URL = None
TAG_FEED_RSS = None
TAG_FEED_RSS_URL = None
TRANSLATION_FEED_ATOM = None
TRANSLATION_FEED_ATOM_URL = None
TRANSLATION_FEED_RSS = None
TRANSLATION_FEED_RSS_URL = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_ATOM_URL = None
AUTHOR_FEED_RSS = None
AUTHOR_FEED_RSS_URL = None

# generate_output()/generate_direct_templates()

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

#  THEME_STATIC_DIR - Destination directory in the
#  output path where Pelican will place the files
#  collected from THEME_STATIC_PATHS.'


#  THEME_STATIC_PATHS - Static theme paths you want
#  to copy. Default value is static, but if your
#  theme has other static paths, you can put them
#  here. If files or directories with the same names
#  are included in the paths defined in this
#  settings, they will be progressively overwritten.
#*default*  THEME_STATIC_PATHS
# THEME_STATIC_PATHS = ['static/images', 'static/js', 'static/css', 'static/media', 'static/fonts']

#  IGNORE_FILES - A list of glob patterns. Files and
#  directories matching any of these patterns will be
#  ignored by the processor. For example, the
#  default ['.#*'] will ignore emacs lock files,
#  and ['__pycache__'] would ignore Python 3’s
#  bytecode caches.
#*default*  IGNORE_FILES = ['.#']
IGNORE_FILES = ['.#*', '.ipynb_checkpoints', '__pycache__']

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

#  DEFAULT_PAGINATION used in pagination.html template.
DEFAULT_PAGINATION = 20

# generate_output()/generate_articles/generate_pages()/generate_XXXXX()/get_template()/template_extension

TEMPLATE_EXTENSIONS = ['.html']

# generate_output()/generate_articles/generate_pages()/generate_period_archives()

YEAR_ARCHIVE_SAVE_AS = ''
MONTH_ARCHIVE_SAVE_AS = ''
DAY_ARCHIVE_SAVE_AS = ''

YEAR_ARCHIVE_URL = ''
MONTH_ARCHIVE_URL = ''
DAY_ARCHIVE_URL = ''

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

BRAND_URL = 'blog/index.html'
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

DUCKDUCKGO_CUSTOM_SEARCH_SIDEBAR = True
EACH_SLUG_HAS_SUBDIR = False
FAVICON = 'images/egbert-network.png'
GOOGLE_ANALYTICS = ''
HIDE_SITENAME = True
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('SPLIT-CODE.COM', 'http://split-code.com/external_blogs.html'),
         ('Hexacorn', 'http://www.hexacorn.com/blog/'),
         ('Möbius Strip RE', 'https://www.msreverseengineering.com/blog/'),
         ("Dr. Fu's", 'http://fumalwareanalysis.blogspot.com/p/malware-analysis-tutorials-reverse.html'),
         ('Metova', 'https://metova.com/category/security/'),
         ('Quarkslab', 'https://blog.quarkslab.com/category/reverseengineering.html'),
         ('Reddit RE', 'https://www.reddit.com/r/ReverseEngineering/comments/is2et/can_we_collect_interesting_reverse_engineering/'),
         ('0x1338', 'http://0x1338.blogspot.com/'))

#  MENUITEMS display menu items on HTML header section.
MENUITEMS = [('Articles', 'blog/articles/index.html'),
             ('Tags', 'blog/tags/index.html')]
MINIBIO =  'Just a high-speed network backend kind of guy doing deep processing of compiler languages, and detection of malwares'
PAGES_DIRNAME =  'pages'
PAGES_SAVE_AS =  'blog/pages/index.html'
PAGES_URL =  'blog/pages/index.html'
PAGES_URL_PATH =  'blog/pages'
PDF_PROCESSOR =  False
PDF_STYLE =  ''
PDF_STYLE_PATH =  ''
SITELOGO =  'images/logo.png'
SITELOGO_SIZE =  100
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
SITE_DIR =  'blog/'
SITE_SUBPATH =  'blog'
SITE_URL_TOP_LVL =  'blog/'
SOCIAL = (
    ('fab fa-github-square', 'https://github.com/egberts'),
    ('fab fa-stack-overflow', 'https://stackoverflow.com/users/4379130/egbert-s')
)
SOCIAL_LABELS = (
    ('Twitter', 'fab fa-twitter', 'https://twitter.com/egbertst'),
    ('GitHub', 'fab fa-github-square', 'https://github.com/egberts'),
    ('StackOverflow', 'fab fa-stack-overflow', 'https://stackoverflow.com/users/4379130/egbert-s'))
TAGS_DIRNAME = 'tags'
TAGS_URL_PATH = 'blog/tags'
# THEME_DIRNAME = 'theme'
THEME_DIRNAME = ''
THEME_STATIC_URL = ''
TWITTER_USERNAME = 'egbertst'
DEBUG =  True

#  FEED_DOMAIN used in most templates' base.html as
#  URL in hyperlink reference (href=)
FEED_DOMAIN =  'egbert.net'

EXTRA_FILES = [
#    '../css/m-grid.css',
#    '../css/pygments-console.css'
]
THEME_COLOR = '#22272e'

SEARCH_BASE_URL = 'https://egbert.net/'


SEARCH_EXTERNAL_URL = 'https://google.com/search?q=site:egbert.net+{query}'


DEFAULT_PAGINATION = False

M_NEWS_ON_INDEX = ('Latest rants on our blog', 2)


######################################################
#  NETWORK SERVER
######################################################
PORT = 8000
BIND = '127.0.0.1'

AUTHOR_REGEX_SUBSTITUTIONS = SLUG_REGEX_SUBSTITUTIONS
CATEGORY_REGEX_SUBSTITUTIONS = SLUG_REGEX_SUBSTITUTIONS
TAG_REGEX_SUBSTITUTIONS = SLUG_REGEX_SUBSTITUTIONS
DEFAULT_DATE = None

FEED_ATOM = None
FEED_ATOM_URL = None
FEED_RSS = None
FEED_RSS_URL = None
FEED_ALL_RSS = None
FEED_ALL_RSS_URL = None
SITESUBTITLE = ''

#  SITENAME - Your site name.  Used as {{ SITENAME }} in
#  templates or during FEED generate_outputs.
#*default*  SITENAME = ''
SITENAME = 'Egbert Networks'

######################################################
##  M.CSS-specific                                  ##
######################################################

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
M_BLOG_FAVICON = [ 'images/favicon.ico', 'image/x-icon' ]

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
M_SITE_LOGO = 'images/egbert-network.png'

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
# M_NEWS_ON_INDEX = False
