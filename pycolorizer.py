import os


class Color():
    """
        Color class
    """

    attrs = dict(
        list(
            zip([
                'bold',
                'dark',
                '',
                'underline',
                'blink',
                '',
                'reverse',
                'concealed',
                ], list(range(1, 9))
                )
            )
        )

    bgcolors = dict(
        list(
            zip([
                'grey',
                'red',
                'green',
                'yellow',
                'blue',
                'magenta',
                'cyan',
                'white',
                ], list(range(40, 48))
                )
            )
        )

    fgcolors = dict(
        list(
            zip([
                'grey',
                'red',
                'green',
                'yellow',
                'blue',
                'magenta',
                'cyan',
                'white',
                ], list(range(30, 38))
                )
            )
        )

    begin = '\033[%dm%s'
    reset = '\033[0m'

    def is_supported(self):
        return not bool(os.getenv('ANSI_COLORS_DISABLED'))

    def colored(
        self,
        message,
        fgcolor=None,
        bgcolor=None,
        attrs=None,
        **kwargs
    ):
        value = message
        if self.is_supported():
            if fgcolor is not None:
                value = self.begin % (self.fgcolors[fgcolor], value)

            if bgcolor is not None:
                value = self.begin % (self.bgcolors[bgcolor], value)

            if attrs is not None:
                for attr in attrs:
                    value = self.begin % (self.attrs[attr], value)

            if value != message:
                value += self.reset

        return value

    def cprint(
        self,
        message,
        fgcolor=None,
        bgcolor=None,
        attrs=None,
        **kwargs
    ):
        print(self.colored(message, fgcolor, bgcolor, attrs))

    def get_fgcolors(self):
        return self.__dict_to_tuple__(self.fgcolors)

    def get_bgcolors(self):
        return self.__dict_to_tuple__(self.bgcolors)

    def get_attrs(self):
        return self.__dict_to_tuple__(self.attrs)

    def __dict_to_tuple__(self, items):
        data = []
        for item in items:
            data.append(item)

        return tuple(data)
