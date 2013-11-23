import unittest
from mock import Mock
from pycolorizer import Color


class ColorlorTest(unittest.TestCase):
    color = None

    def setUp(self):
        self.color = Color()

    def test_is_supported(self):
        self.assertTrue(self.color.is_supported())

    def test_colored_message_without_color_should_return_message(self):
        self.assertEqual(
            "message",
            self.color.colored("message")
        )

    def test_colored_with_fgcolor_should_return_color_data(self):
        self.assertEqual(
            '\033[31mmessage\033[0m',
            self.color.colored("message", "red")
        )

    def test_colored_with_fg_and_bg_should_return_color_data(self):
        self.assertEqual(
            '\x1b[42m\x1b[31mmessage\x1b[0m',
            self.color.colored("message", "red", "green")
        )

    def test_colored_with_named_param_should_return_color_data(self):
        self.assertEqual(
            '\x1b[42m\x1b[31mmessage\x1b[0m',
            self.color.colored("message", bgcolor="green", fgcolor="red")
        )

    def test_colored_with_attrs_should_return_attr_data(self):
        self.assertEqual(
            '\033[7mmessage\033[0m',
            self.color.colored("message", attrs=['reverse'])
        )

    def test_colored_with_undefined_color_raise_exception(self):
        self.assertRaises(
            KeyError,
            lambda: self.color.colored("message", "fake")
        )

    def test_get_fgcolors_should_return_dict(self):
        self.assertIs(type(self.color.get_fgcolors()), tuple)

    def test_get_bgcolors_should_return_dict(self):
        self.assertIs(type(self.color.get_bgcolors()), tuple)

    def test_get_attrs_should_return_dict(self):
        self.assertIs(type(self.color.get_attrs()), tuple)
