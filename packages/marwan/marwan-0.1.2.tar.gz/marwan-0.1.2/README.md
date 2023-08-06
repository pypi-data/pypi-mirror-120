<p>
  <img width=60% height=auto src="https://github.com/marwanhawari/marwan/blob/main/docs/marwan_logo.png" alt="marwan logo"/>
</p>

[![PyPI version](https://badge.fury.io/py/marwan.svg)](https://badge.fury.io/py/marwan)
[![Build Status](https://github.com/marwanhawari/marwan/actions/workflows/build.yml/badge.svg)](https://github.com/marwanhawari/marwan/actions)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![GitHub](https://img.shields.io/github/license/marwanhawari/marwan?color=blue)](LICENSE)

# Description
This tool allows me to conveniently access some of my frequently used webpages from the command line.

# Installation
The `marwan` package can be installed directly using `pip`.
```
pip install marwan
```

# Usage
`marwan` can be run from the command line and will automatically open your web browser.

* Open one of my GitHub repositories:
```
$ marwan -g pyinterview
Opening https://www.github.com/marwanhawari/pyinterview
```

* Open my PyPI page:
```
$ marwan -p
Opening https://pypi.org/user/marwanhawari/
```

### Options
```
usage: marwan [-h] [-g [REPO]] [-l] [-p] [-w]

optional arguments:
  -h, --help            show this help message and exit
  -g [REPO], --github [REPO]
                        Open my GitHub page. You can specify the repository or leave empty for my homepage.
  -l, --linkedin        Open my LinkedIn page.
  -p, --pypi            Open my PyPI page.
  -w, --website         Open my personal website.
```

