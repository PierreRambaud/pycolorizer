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
c.cprint("message", "red")
c.cprint("message", fgcolor="red")
c.cprint("message", "red", "green")
```

## Running tests

In project root directory, run following command to
install requirements for testing:
`$ pip install -r tests_requirements.txt`

To run unittests:
`$ nosetests`

To check code style:
`$ pep8 ./`
