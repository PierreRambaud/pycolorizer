import unittest
from pycolorizer import (
    Color,
    NoStyleFoundError,
    InvalidStyleNameError,
    RecursionInThemeError
)


class ColorTest(unittest.TestCase):
    color = None

    def setUp(self):
        self.color = Color()

    def test_given_string_should_apply_style(self):
        self.assertEqual(
            "\033[31mfoo\033[0m",
            str(self.color('foo').red())
        )

    def test_given_string_should_apply_more_than_one_style(self):
        self.assertEqual(
            "\033[1m\033[97mfoo\033[0m\033[0m",
            str(self.color('foo').white().bold())
        )

    def test_style_name_is_not_case_sensitive(self):
        self.assertEqual(
            "\033[31mfoo\033[0m",
            str(self.color('foo').RED())
        )

    def test_state_is_initialized(self):
        self.assertEqual('foo', str(self.color('foo')))
        self.assertEqual('bar', str(self.color('bar')))

    def test_given_styled_string_should_be_able_to_reused(self):
        self.assertEqual('foo', str(self.color('foo').blue().reset()))

    def test_raise_error_when_style_not_found(self):
        self.assertRaises(
            NoStyleFoundError,
            lambda: self.color.color('foo bar').foo()
        )

    def test_style_can_contain_text(self):
        self.assertEqual(
            str(self.color('foo').blue()),
            self.color().blue('foo')
        )

    def test_shortcut_foreground(self):
        self.assertEqual(
            str(self.color('Hello').blue()),
            str(self.color('Hello').fg('blue'))
        )

    def test_shortcut_background(self):
        self.assertEqual(
            str(self.color('Hello').bg_red()),
            str(self.color('Hello').bg('red'))
        )

    def test_has_highlight_shortcut_for_background(self):
        self.assertEqual(
            str(self.color('Hello').bg_blue()),
            str(self.color('Hello').highlight('blue'))
        )

    def test_should_support_themes(self):
        self.color.set_themes({'error': 'red'})
        self.assertEqual(
            str(self.color('Error...').red()),
            str(self.color('Error...').error())
        )

    def test_thmes_can_override_default_styles(self):
        self.color.set_themes({'white': 'red'})
        self.assertEqual(
            str(self.color('Warning...').red()),
            str(self.color('Warning...').white())
        )

    def test_given_invalid_them_name_should_raise_error(self):
        self.assertRaises(
            InvalidStyleNameError,
            lambda: self.color('foo bar').set_themes({'&é""': "white"})
        )

    def test_given_styled_string_can_be_cleaned(self):
        self.assertEqual(
            'some text',
            str(self.color(str(self.color('some text').red())).clean())
        )

    def test_given_string_with_style_tags_should_be_interpret(self):
        text = 'This is <red>some text</red>'
        self.assertEqual(
            'This is ' + str(self.color('some text').red()),
            str(self.color(text).colorize())
        )

    def test_given_string_with_nested_tags_should_be_interpret(self):
        actual = str(
            self.color('<cyan>Hello <bold>World!</bold></cyan>')
            .colorize()
        )
        expected = str(
            self.color('Hello ' + str(self.color('World!').bold()))
            .cyan()
        )
        self.assertEqual(expected, actual)

    def test_apply(self):
        self.assertEqual(
            str(self.color('foo').blue()),
            str(self.color().apply('blue', 'foo'))
        )

    def test_apply_center(self):
        width = 80
        for text in ('', 'hello', 'hellow world', '✩'):
            current_width = len(
                str(self.color(text).center(width))
            )

            self.assertEqual(width, current_width)
            current_width = len(
                str(
                    self.color(text)
                    .center(width)
                    .bg('blue')
                    .clean()
                )
            )
            self.assertEqual(width, current_width)

    def test_apply_center_multiline(self):
        width = 80
        color = Color()
        text = 'hello' + "\n" + '✩' + "\n" + 'world'
        actual = str(color(text).center(width))
        for line in actual.split("\n"):
            self.assertEqual(width, len(line))

    def test_should_support_256_colors(self):
        self.assertEqual(
            "\033[38;5;3mfoo\033[0m",
            self.color().apply('color[3]', 'foo')
        )
        self.assertEqual(
            "\033[48;5;3mfoo\033[0m",
            self.color().apply('bg_color[3]', 'foo')
        )

    def test_given_invalid_color_number_should_raise_error(self):
        self.assertRaises(
            NoStyleFoundError,
            lambda: self.color().apply('color[-1]', 'foo')
        )

        self.assertRaises(
            NoStyleFoundError,
            lambda: self.color().apply('color[256]', 'foo')
        )

    def test_should_handle_recursion_in_theme_with_list(self):
        self.assertRaises(
            RecursionInThemeError,
            lambda: self.color().set_themes(
                {
                    'green': ['green'],
                }
            )
        )

    def test_should_handle_recursion_in_theme_with_string(self):
        self.assertRaises(
            RecursionInThemeError,
            lambda: self.color().set_themes(
                {
                    'green': 'green',
                }
            )
        )
