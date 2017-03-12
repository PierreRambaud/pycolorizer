#!/usr/bin/env python

from pycolorizer import Color

c = Color()

# highlight('green') == bg('green') == bg_green()
# white() == fg('white')

print(c('Hello World!').white().bold().highlight('blue'))

# Create your own styles
c.set_themes(
    {
        'welcome': ('yellow', 'bg_cyan'),
        'bye': 'blue',
    }
)

print(c('Hello world!').welcome().bold())
print(c('Bye!').bye())

# Use style tags
text = """
1 : <welcome>Hello <bold>World!</bold></welcome>
2 : <bye>Bye!</bye>
"""

print(c(text).colorize())

# Center text
text = 'hello' + '✩' + 'world'
print(c(text).bg_blue().red().center())

# Use standard API
message = c.apply('bold', c.green('Hello World!'))
print(message)
print(c.clean(message))
