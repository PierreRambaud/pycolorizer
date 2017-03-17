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

print("\n")
print('System colors.')
for i in range(0, 16):
    print(str(c.apply('bg_color[{}]'.format(i), '  ')), end='')

print("\n\n")
print('Color cube, 6x6x6')
for g in range(0, 6):
    for r in range(0, 6):
        for b in range(0, 6):
            color = 16 + (r * 36) + (g * 6) + b
            print(str(c('  ').bg('color[{}]'.format(color))), end='')
        print(str(' '), end='')
    print()


print('Grayscale ramp:')
for i in range(232, 256):
    print(c('  ').bg('color[{}]'.format(i)), end='')
print()
