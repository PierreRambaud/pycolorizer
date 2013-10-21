#!/usr/bin/env python

from color import Color

c = Color()
for fgcolor in c.get_fgcolors():
    for bgcolor in c.get_bgcolors():
        c.cprint(fgcolor + " " + bgcolor, fgcolor, bgcolor)
