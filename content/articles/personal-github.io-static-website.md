Title: Personal GitHub Static Website
Tags: github, blog
Date: 2018-12-28 09:25
modified: 2025-07-13T0351
Status: published
Category: HOWTO
Summary: Creating a personal Github.IO website.

How did I created a GitHub.IO personal website using two-repo/git-submodule
approach?


In five general steps:

1.  Created the final-stage website repo
2.  Created the static website generator repo
3.  Install static website generator
4.  Create static webpages
5.  Git-pushed webpages to final-stage website repo

Creating Final-Stage Website Repo
=================================
Need to create a GitHub repo to hold the final-stage, personal, static website.

From upper-right corner of github.com web GUI, there is a "+" plus sign pulldown
menu option, click on "New repository".

In the "Repository name" textbox, enter in "&lt;username&gt;.github.io" after
replacing the &lt;username&gt; with your GitHub account username.

Click on the green "Create Repository" button.

No need to get, clone, nor fill this repo up on our local machine yet.
We let our static website generator do that... later.

Static Website Generator Repo
=============================
For the second part, we create a second repository to hold all things related to
our favorite static website generator tools and our initial blog stuff.

Creating Static Website Repo
----------------------------
From upper-right corner of github.com web GUI, there is a "+" plus sign pulldown
menu option, click on "New repository".

In the "Repository name" textbox, enter in "&lt;username&gt;.github.io-src" after
replacing the &lt;username&gt; with your GitHub account username.

NOTE: the second repo has a "-src" suffix added to the repo name.

Click on the green "Create Repository" button.

```bash
# On local machine

cd ~/work/websites  # we had those already existing subdirectories
git clone https://github.com/<username>/<username>.github.io-src

# This is our main git project
cd <username>.github.io-src
```

Now we add our final-stage repo submodule to our master project
and call it `output` subdirectory

```bash
# output subdirectory = final-stage static website
git submodule add --force \
      --branch master  \
      https://github.com/egberts/egberts.github.io.git output
```

WARNING: If you used `git submodule update` instead of 'add', you will find yourself
in a world of hurt with regard to trying to 'git push' your final website back
up; `git submodule update` will only take a fixed point of your final website
and leave that repo as "branch-less".   Better to stay on the master branch
and let your static website generator put all their updates to the latest
branch named 'master'... automatically.

Installing Static Website Generator
===================================
Now we can add our static website generator in here.
I use Pelican, which uses `output` to hold my final-stage website

```bash
cd ~/work/websites/<username>.github.io-src  # note the '-src' suffix
pelican-quickstart
```

This `pelican-quickstart` utility will ask you a series of questions to make
things easier.

```
    Welcome to pelican-quickstart v4.0.1.

    This script will help you create a new Pelican-based website.

    Please answer the following questions so this script can generate the files
    needed by Pelican.


    > Where do you want to create your new web site? [.]
```

You are already within the main project repo (whose repository name ended with a
"-src" suffix) subdirectory.  This is what the "`[.]`" means: current directory.
We want that.  Press ENTER to continue.

Next is the title of the website:

```
    > What will be the title of this web site?
```

I typically enter in "Egbert Network".  Most people put in "Blogs of &lt;Your
Name&gt;" or something like that.  This data entry is used to put title of your
main webpage (as in HTML &lt;title&gt;).  `SITENAME` is the Python variable
being updated in `pelicanconf.py` configuration file.
Often used in many website template for various purposes, most commonly
in the HTML &lt;title&gt; of the main index.html page.

Next is the author of this website:

```
    > Who will be the author of this web site?
```

Some will give a long form of their name here.
This is only useful for a website who have multiples of
authors.
I leave it empty/blank and simply press ENTER.

`AUTHOR` is the Python variable updated in `pelicanconf.py` configuration file.

Language default is asked next:

```
    > What will be the default language of this web site? [en]
```

Press ENTER to continue unless you are posting a non-English website then you
choose a two-letter notation representing your choice of language.  Look at the
ISO 639-1 column in https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes.

`DEFAULT_LANG` is the Python variable updated in `pelicanconf.py` configuration file.

The next question is not clear but basically it is asking you what the base URL
is that you will be putting your final website at:

    > Do you want to specify a URL prefix? e.g., https://example.com   (Y/n)

`SITEURL` is the Python variable updated in `pelicanconf.py` configuration file.

In my case of deploying a personal GitHub website as described within this
article, we must answer "Y".

    > What is your URL prefix? (see above example; no trailing slash)

The interesting thing about the wording "URL prefix" is that one MAY assume that
you could NOT put anything after the domain name, like in "https://example.com".
Not so.  You CAN (and in our case, SHOULD) put something after a domain name and
a slash, such as https://github.io/&lt;username&gt; in our setup.  Just that it
CANNOT end with a slash symbol.

    > Do you want to enable article pagination? (Y/n)

Article pagination is where you have too many articles and may want to break
that up over several web pages.  Default Yes is a good idea here.

`DEFAULT_PAGINATION` is the Python variable updated in `pelicanconf.py` configuration file.

    > How many articles per page do you want? [10]

Depending on how many articles you put out and how often, you may want to change
this number to either 5 (shallow view) or 100 (long view).

    > What is your time zone? [Europe/Paris]

Timezone.  You can find your available timezone label using the following tools
`tzselect` at another terminal. On macOS/Mac OSX, you can visit the
/usr/share/zoneinfo and determine your choices of timezones.

`TIMEZONE` is the Python variable updated in `pelicanconf.py` configuration file.

    > Do you want to generate a tasks.py/Makefile to automate generation and publishing? (Y/n)

This one is weird to me.  Took a couple of tries before I finally figured it
out.

    > Do you want to upload your website using FTP? (y/N)
    > Do you want to upload your website using SSH? (y/N)
    > Do you want to upload your website using Dropbox? (y/N)
    > Do you want to upload your website using S3? (y/N)
    > Do you want to upload your website using Rackspace Cloud Files? (y/N)
    > Do you want to upload your website using GitHub Pages? (y/N) y
    > Is this your personal page (username.github.io)? (y/N) y

`GITHUB_PAGES_BRANCH` is the Make variable updated in `Makefile` file.

BEFORE YOU EXECUTE 'pelican' command, you must disable the destruction
of the 'output' subdirectory.  Our 'git submodule' setup does not like
its 'output' subdirectory being destroyed.  There is a configuration
for that;  Edit the `pelicanconf.py` file:


```bash
vim pelicanconf.py
```

And add (or change) the `DELETE_OUTPUT_DIRECTORY` option to "False".

```
    ## Delete the output directory, and all of its contents, before generating new
    ## files. This can be useful in preventing
    ## older, unnecessary files from persisting in your output. However, this is a
    ## destructive setting and should be
    ## handled with extreme care.

    DELETE_OUTPUT_DIRECTORY = False
```

IMHO: `DELETE_OUTPUT_DIRECTORY` should have defaulted to False.

Creating Static Web Pages
=========================
This is the easy part.

Create an article.  Create and edit a file.  Its filename must ended with a
".md" or ".rst" suffix, depending on whether you like Markdown format or ReST
format.

I started out with:

```
    Title: Example
    Date: 2018-11-18 05:00
    Tags: sappy
    Status: published
    Category: research

    My First Blog
    =============

    Not much to go on but this is my first blog
```

Then saved the file as "`content/article/example.md`"

I then executed:

```bash
make html
```

To view your newly created webpages, start up a local webserver using port
8000.

```bash
make serve
```
Using your favorite web browser, visit the [http://localhost:8000/](http://localhost:8000/) and view the result
of your first static website.


Feel confident?  Publish the static web pages onto your GitHub personal website.

```bash
make publish
make github
```

And visit [https://username.github.io/username/](https://username.github.io/username)

A workflow diagram is shown as:

![2-Repo Pelican Git Workflow](/images/pelican-2-git-repos.svg "2-Repo Pelican Git Workflow")




Saving It All To Repositories
=============================

5.  Git-pushed webpages to final-stage website repo
