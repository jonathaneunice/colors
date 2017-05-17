# -*- encoding: utf-8 -*-

"""
Tests for colors module
"""

from colors import *
from pytest import raises


def test_nocolors():
    """We should have the original text with no parameters"""
    assert color("RED") == "RED"


def test_redcolor():
    """Test if we get a correct red"""
    assert color("RED", fg="red") == '\x1b[31mRED\x1b[0m'


def test_default_color():
    assert color('test', fg='default') == '\x1b[39mtest\x1b[0m'
    assert color('test', bg='default') == '\x1b[49mtest\x1b[0m'
    assert color('test', fg='default', bg='default') == \
        '\x1b[39;49mtest\x1b[0m'


def test_error_on_bad_color_string():
    """Test if we have an exception with a bad string color"""
    with raises(ValueError):
        color("RED", "bozo")


def test_integer_color():
    """Test if we can use a integer as a color"""
    assert color("RED", 1) == '\x1b[38;5;1mRED\x1b[0m'


def test_error_on_bad_color_int():
    """Test if we have an exception with a bad color number"""
    with raises(ValueError):
        color("RED", 911)


def test_tuple_color():
    orange = (255, 165, 0)
    assert color('ORANGE', fg=orange) == '\x1b[38;2;255;165;0mORANGE\x1b[0m'


def test_css_color():
    assert color('ORANGE', fg='orange') == '\x1b[38;2;255;165;0mORANGE\x1b[0m'


def test_background_color():
    """Test the background color with string"""

    assert color("RED", bg="red") == '\x1b[41mRED\x1b[0m'
    assert color('PURPLE', bg='purple') == '\x1b[48;2;128;0;128mPURPLE\x1b[0m'


def test_mixed_color():
    assert color('PINK/GRAY', fg='pink', bg='gray') == \
        '\x1b[38;2;255;192;203;48;2;128;128;128mPINK/GRAY\x1b[0m'
    assert color('GRAY/PINK', fg='gray', bg='pink') == \
        '\x1b[38;2;128;128;128;48;2;255;192;203mGRAY/PINK\x1b[0m'


def test_style_color():
    """Test the style with a string"""
    assert color('BOLD', style='bold') == '\x1b[1mBOLD\x1b[0m'


def test_error_setting_style_color():
    """Test if we have an exception setting the style"""
    with raises(ValueError):
        color("BOLD", style="MAY")


def test_error_on_bad_color_notint():
    """Test if we have an exception with a bad color number"""
    with raises(ValueError):
        color("RED", 911.11)


def test_error_on_bad_style():
    """Test if we have an exception with a bad color number"""
    with raises(ValueError):
        color("RED", bg="cursivas")


def test_remove_color():
    """We can get the original message without the colors"""
    assert strip_color(color("RED", "red")) == "RED"


def test_parse_rgb():
    peachpuff = (255, 218, 185)
    assert parse_rgb('peachpuff') == peachpuff
    assert parse_rgb('#ffdab9') == peachpuff
    assert parse_rgb('rgb(255, 218, 185)') == peachpuff
    assert parse_rgb('peachpuff') == peachpuff

    rebeccapurple = (102, 51, 153)
    assert parse_rgb('rebeccapurple') == rebeccapurple
    assert parse_rgb('#639') == rebeccapurple
    assert parse_rgb('rgb(102,51,153)') == rebeccapurple


def test_partial_functions():
    # a few spot-checks
    assert black('test') == color('test', 'black')
    assert red('test') == color('test', 'red')
    assert green('test') == color('test', 'green')

    assert bold('test') == color('test', style='bold')
    assert underline('test') == color('test', style='underline')


def test_doc_example():

    assert color('my string', fg='blue') == \
           '\x1b[34mmy string\x1b[0m'
    assert color('some text', fg='red', bg='yellow', style='underline') == \
           '\x1b[31;43;4msome text\x1b[0m'


def test_custom_partial():
    important = partial(color, fg='red', style='bold+underline')
    boldul = partial(color, style='bold+underline')

    text = 'very important'
    answer = '\x1b[31;1;4mvery important\x1b[0m'

    assert color(text, fg='red', style='bold+underline') == answer
    assert red(text, style='bold+underline') == answer
    assert boldul(text, fg='red') == answer
    assert important(text) == answer