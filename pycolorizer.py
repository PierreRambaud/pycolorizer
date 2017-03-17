import os
import re


class NoStyleFoundError(BaseException):
    """
    No style found
    """
    pass


class InvalidStyleNameError(BaseException):
    """
    Invalid style name
    """
    pass


class RecursionInThemeError(BaseException):
    """
    Recursion in user style
    """
    pass


class Color:
    STYLE_NAME_PATTERN = r'^[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*$'
    NUMBER_PATTERN = r'[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]'
    STYLE_PATTERN = r'^((?:bg_)?)color\[(' + NUMBER_PATTERN + ')\]$'
    FORMAT_PATTERN = r'<([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)>(.*?)</\1>'
    EOL = "\n"
    ESC = "\033\["
    ESC_SEQ_PATTERN = "\033[{}m"

    styles = {
        'reset':             '0',
        'bold':              '1',
        'dark':              '2',
        'italic':            '3',
        'underline':         '4',
        'blink':             '5',
        'reverse':           '7',
        'concealed':         '8',
        'default':           '39',
        'black':             '30',
        'red':               '31',
        'green':             '32',
        'yellow':            '33',
        'blue':              '34',
        'magenta':           '35',
        'cyan':              '36',
        'light_gray':        '37',
        'dark_gray':         '90',
        'light_red':         '91',
        'light_green':       '92',
        'light_yellow':      '93',
        'light_blue':        '94',
        'light_magenta':     '95',
        'light_cyan':        '96',
        'white':             '97',
        'bg_default':        '49',
        'bg_black':          '40',
        'bg_red':            '41',
        'bg_green':          '42',
        'bg_yellow':         '43',
        'bg_blue':           '44',
        'bg_magenta':        '45',
        'bg_cyan':           '46',
        'bg_light_gray':     '47',
        'bg_dark_gray':      '100',
        'bg_light_red':      '101',
        'bg_light_green':    '102',
        'bg_light_yellow':   '103',
        'bg_light_blue':     '104',
        'bg_light_magenta':  '105',
        'bg_light_cyan':     '106',
        'bg_white':          '107',
    }

    themes = {}
    wrapped = ''
    initial = ''

    style_forced = False

    # Magic methods
    def __init__(self, string: str = ''):
        self.__call__(string)

    def __call__(self, string: str = None, *args):
        if string is not None:
            self.set_internal_state(string)
        return self

    def __getattr__(self, method):
        def apply_attr(*args):
            if len(args) >= 1:
                return self.apply(method, args[0])
            return self.apply(method)

        return apply_attr

    def __get__(self, name: str):
        return self.apply(name)

    def __str__(self):
        return self.wrapped

    # Public methods
    def set_force_style(self, force: bool):
        self.style_forced = bool(force)
        return self

    def is_style_forced(self):
        return self.style_forced

    def is_supported(self):
        return not bool(os.getenv('ANSI_COLORS_DISABLED'))

    def are_256_colors_supported(self):
        return re.search('/256color/', os.getenv('TERM'))

    def set_internal_state(self, string: str):
        self.initial = self.wrapped = str(string)

    def apply(self, style: str, text: str = None):
        if text is None:
            self.wrapped = self.__stylize__(style, self.wrapped)
            return self
        return self.__stylize__(style, text)

    def fg(self, color, text: str = None):
        return self.apply(color, text)

    def bg(self, color: str, text: str = None):
        return self.apply('bg_' + color, text)

    def highlight(self, color, text: str = None):
        return self.bg(color, text)

    def reset(self):
        self.wrapped = self.initial
        return self

    def center(self, width: int = 80, text: str = None):
        if text is None:
            text = self.wrapped

        centered = ''
        for line in text.split(self.EOL):
            line = line.strip()
            centered += line.center(width) + self.EOL
        self.set_internal_state(centered.strip(self.EOL))
        return self

    def clean(self, text: str = None):
        if text is None:
            self.wrapped = self.__strip_colors__(self.wrapped)
            return self

        return self.__strip_colors__(text)

    def is_a_valid_style_name(self, name):
        return re.search(re.compile(self.STYLE_NAME_PATTERN), name)

    def add_theme(self, name: str, styles):
        self.__verify_themes__({name: styles})
        self.themes[name] = styles

    def set_themes(self, themes: dict):
        self.__verify_themes__(themes)
        self.themes = themes
        return self

    def colorize(self, text: str = None):
        if text is None:
            self.wrapped = self.__colorize_text__(self.wrapped)
            return self
        return self.__colorize_text__(text)

    # Private methods
    def __verify_themes__(self, themes: dict):
        for name, styles in themes.items():
            if not self.is_a_valid_style_name(name):
                raise InvalidStyleNameError()

            if name in styles:
                raise RecursionInThemeError()

    def __strip_colors__(self, text: str):
        return re.sub(re.compile(self.ESC + '\d+m'), '', text)

    def __colorize_text__(self, text: str):
        return re.sub(
            re.compile(self.FORMAT_PATTERN, re.MULTILINE),
            self.__replace_style__,
            text
        )

    def __replace_style__(self, matches):
        return self.apply(
            matches.group(1),
            self.colorize(matches.group(2))
        )

    def __stylize__(self, style: str, text: str) -> str:
        if not (self.is_style_forced() or self.is_supported()):
            return text

        style = style.lower()
        if style in self.themes.keys():
            return self.__apply_theme__(style, text)

        if style in self.styles.keys():
            return self.__apply_style__(style, text)

        matches = re.search(
            re.compile(self.STYLE_PATTERN),
            style
        )
        if matches:
            option = 48 if matches.group(1) == 'bg_' else 38
            return self.__build_esc_seq__(
                "{};5;{}".format(option, matches.group(2))
            ) + str(text) + self.__build_esc_seq__(self.styles['reset'])

        raise NoStyleFoundError()

    def __apply_style__(self, style: str, text: str):
        return self.__build_esc_seq__(
            self.styles[style]
        ) + str(text) + self.__build_esc_seq__(self.styles['reset'])

    def __build_esc_seq__(self, style: str):
        return self.ESC_SEQ_PATTERN.format(style)

    def __apply_theme__(self, theme: str, text: str):
        styles = self.themes[theme]
        if isinstance(styles, str):
            styles = [styles]

        for style in styles:
            text = self.__stylize__(style, text)
        return text
