""" Functional Testing of Parse Instance

This testing verififys that that the overall requirements are met for Parse.
Also the tests are broad enough that every method call in Parse is made.

What is new in this pytest file is that ipython or other interactive python
can import it and run the tests for easier developement and debugging.
"""
from truealgebra.core.tests.ipython_three_parse import (
    settings, Co, CA, Sy, Nu
)
from truealgebra.core.parse import Parse
import pytest

parse = Parse(settings)

# Functional Tests
str00 = ' f(2.3j, 4j, j, 37.66, 6., .33, 53, 6, x, a4) '
expr00 = Co('f', (
    Nu(complex(0, 2.3)),
    Nu(complex(0, 4)),
    Nu(complex(0, 1)),
    Nu(37.66),
    Nu(6.),
    Nu(.33),
    Nu(53),
    Nu(6),
    Sy('x'),
    Sy('a4')
))

str01 = ' 3.2E-1 * .2E1 * 4e2 '
expr01 = CA('*', (Nu(0.32), CA('*', (Nu(2.0), Nu(400.0)))))

str02 = ' (3.2E-1 * .2E1) * 4e2 '
expr02 = CA('*', (CA('*', (Nu(.32), Nu(2.0))), Nu(400.0)))

str03 = ' 3E2 E 2.0E3 '
expr03 = Co('E', (Nu(300.0), Nu(2000.0)))

str04 = ' j jj 2.3j '
expr04 = Co('jj', (Nu(complex(0, 1)), Nu(complex(0, 2.3))))

str05 = ' @ @ @ x ! ! ! '
expr05 = Co('!', (Co('!', (Co('!', (Co('@', (Co('@', (Co('@', (
    Sy('x'),
)),)),)),)),)),))

str06 = ' % % % x ! ! ! '
expr06 = Co('%', (Co('%', (Co('%', (Co('!', (Co('!', (Co('!', (
    Sy('x'),
)),)),)),)),)),))

str07 = (' - - - b ')
expr07 = Co('-', (Co('-', ( Co('-',(Sy('b'),)),)),))

str08 = (' a - - - b ')
expr08 = Co('-', (
    Sy('a'),
    Co('-', (Co('-',(Sy('b'),)),)),
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
        (str00, expr00),
        (str01, expr01),
        (str02, expr02),
        (str03, expr03),
        (str04, expr04),
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
def test_parse_functional(string, correct):
    expr = parse(string)

    assert expr == correct
