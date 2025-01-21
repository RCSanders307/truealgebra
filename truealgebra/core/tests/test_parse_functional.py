""" Functional Testing of Parse Instance

This testing verififys that that the overall requirements are met for Parse.
Also the tests are broad enough that every method call in Parse is made.

What is new in this pytest file is that ipython or other interactive python
can import it and run the tests for easier developement and debugging.
"""
from truealgebra.core.abbrv import (
    Co, CA, Sy, Nu, Re, Asn
)
from truealgebra.core.parse import Parse
from truealgebra.core.settings import SettingsSingleton
from truealgebra.core import setsettings
import pytest


@pytest.fixture
def settings(scope='module'):
    settings = SettingsSingleton()
    settings.reset()

    setsettings.set_default_bp(251, 252)
    setsettings.set_custom_bp('!', 2000, 0)
    setsettings.set_custom_bp('!!!', 3000, 0)
    setsettings.set_custom_bp('/', 1100, 1100)
    setsettings.set_custom_bp('**', 1251, 1250)
    setsettings.set_custom_bp('*', 1000, 999)
    setsettings.set_custom_bp('+', 500, 500)
    setsettings.set_custom_bp("@", 0, 3000)
    setsettings.set_custom_bp("%", 0, 10)
    setsettings.set_custom_bp("!**", 1000, 1000)
    setsettings.set_custom_bp("!*", 999, 999)

    setsettings.set_bodied_functions('D', 481)
    setsettings.set_symbol_operators("and", 75, 75)
    setsettings.set_symbol_operators("E")
    setsettings.set_symbol_operators("jj")
    setsettings.set_infixprefix("-", 999)
    setsettings.set_container_subclass('+', CA)
    setsettings.set_container_subclass('*', CA)
    setsettings.set_container_subclass(':=', Asn)
    setsettings.set_container_subclass('Rule', Re)

    setsettings.set_complement('star', '*')
    setsettings.set_complement('!!', '+')
    settings.parse = Parse()

    yield settings
    settings.reset()


parse = Parse()

# Functional Tests
str01 = ' 3.2E-1 * .2E1 * 4e2 '
expr01 = CA('*', (Nu(0.32), CA('*', (Nu(2.0), Nu(400.0)))))

str02 = ' (3.2E-1 * .2E1) * 4e2 '
expr02 = CA('*', (CA('*', (Nu(.32), Nu(2.0))), Nu(400.0)))

str03 = ' 3E2 E 2.0E3 '
expr03 = Co('E', (Nu(300.0), Nu(2000.0)))

str05 = ' @ @ @ x ! ! ! '
expr05 = Co('!', (Co('!', (Co('!', (Co('@', (Co('@', (Co('@', (
    Sy('x'),
)),)),)),)),)),))

str06 = ' % % % x ! ! ! '
expr06 = Co('%', (Co('%', (Co('%', (Co('!', (Co('!', (Co('!', (
    Sy('x'),
)),)),)),)),)),))

str07 = (' - - - b ')
expr07 = Co('-', (Co('-', (Co('-', (Sy('b'),)),)),))

str08 = (' a - - - b ')
expr08 = Co('-', (
    Sy('a'),
    Co('-', (Co('-', (Sy('b'),)),)),
))

str09 = ' star(a, b, c, star(1, 2, 3)) '
expr09 = CA('*', (
    Sy('a'),
    Sy('b'),
    Sy('c'),
    CA('*', (Nu(1), Nu(2), Nu(3)))
))

str10 = ' D(x) y * z '
expr10 = Co('D', (
    Sy('x'),
    CA('*', (Sy('y'), Sy('z')))
))

str11 = ' end '
expr11 = Sy('end')


@pytest.mark.parametrize(
    'string, correct',
    [
        (str01, expr01),
        (str02, expr02),
        (str03, expr03),
        (str05, expr05),
        (str06, expr06),
        (str07, expr07),
        (str08, expr08),
        (str09, expr09),
        (str10, expr10),
        # This next test is to catch a bug that occured once
        # The default value of the delims parameter of the init_parse method
        # was the string 'end', instead of a tuple containing the string.
        (str11, expr11),
    ]
)
def test_parse_functional(string, correct, settings):
    expr = parse(string)

    assert expr == correct
