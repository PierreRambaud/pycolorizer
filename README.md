PyColorizer
=====

[![Build Status](https://travis-ci.org/PierreRambaud/pycolorizer.png?branch=master)](https://travis-ci.org/PierreRambaud/pycolorizer)

## Installation

```
pip install pycolorizer
```

## Usage

```
from pycolorizer import Color

c = Color()
print(c('Hello World!').white().bold().highlight('blue'))
c.set_themes(
    {
        'welcome': ('yellow', 'bg_cyan'),
        'bye': 'blue',
    }
)

print(c('Hello world!').welcome().bold())
print(c('Bye!').bye())
```

## Running tests

In project root directory, run following command to
install requirements for testing:
`$ pip install -r reqs/dev.txt`

To run unittests:
`$ nosetests`

To check code style:
`$ flake8 ./`
