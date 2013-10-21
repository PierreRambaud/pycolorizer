Color
=====

## Usage

```
from color import Color

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
