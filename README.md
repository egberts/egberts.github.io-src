# egberts.github.io-src
Source page for egberts.github.io website

visit [this link](https://egberts.github.io/)


REBUILD
=======
To recreate build environment for this website, execute:

  gh repo clone egberts/egberts.github.io-src
  cd egberts.github.io-src
  gh repo clone egberts/m.css
  cd ..

  make html
  make serve
  firefox http://localhost:8000/blog
  make rsync\_upload
