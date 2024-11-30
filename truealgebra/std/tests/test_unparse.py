from truealgebra.core.abbrv import *

from truealgebra.std.settings_functions import set_commonsettings, set_parse
from truealgebra.common.settings_function import set_settings
from truealgebra.core.expressions import ExprBase
from truealgebra.std.unparse import alg_unparse

from truealgebra.core.settings import settings
from truealgebra.common.commonsettings import commonsettings

import pytest
from fractions import Fraction


@pytest.fixture
def stdsettings(scope='module'):
    set_settings()
    set_parse()
    set_commonsettings()
    ExprBase.set_setting_str_func(alg_unparse)
    yield settings
    settings.reset()
    commonsettings.reset()
    ExprBase.set_setting_str_func(None)



@pytest.fixture
def unparse_list(stdsettings):
    temp0 = Co('!', (Sy('x'),))
    temp1 = Co('!', (temp0,))
    temp2 = Co('-', (Sy('x'),))
    temp3 = Co('-', (temp2,))
    temp4 = Co('-', (Co('=', (Sy('a'), Sy('b'))),))
    temp5 = Co('=', (Sy('a'), Sy('b')))
    op0 = Co('D', (Sy('z'),))
    op1 = CA('*', (op0, temp5))
    nc0 = Nu(complex(3, 4))
    nc1 = Nu(complex(-3.5, -4.6))
    nc2 = Nu(complex(0, 4.8))
    nf0 = Nu(Fraction(9, 1))
    nf1 = Nu(Fraction(3, 4))
    nf2 = Nu(Fraction(3, 6))
    neg0 = Co('-', (Sy('x'),))

    unparse_list = [
# ndx = 0, postfix operators
        (temp1, 'x ! !'),
# ndx = 1, prefix operators
        (temp3, '- - x'),
# ndx = 2, subtraction and negative operators
        (Co('-', (temp0, temp2)), 'x ! - - x'),
# ndx = 3, Container 'f' with int and real numbers
        (Co('f', (Nu(4), Nu(4.7), Nu(.7))), 'f(4, 4.7, 0.7)'),
# ndx = 4, Bodied function with complex numbers
        (Co('D', (nc0, nc1, nc2)), 'D(3+4j, -3.5-4.6j) 4.8j'),
# ndx = 5, function form, Container 'f' with fractions
        (Co('f', (nf0, nf1, Co('/', (nf2, Sy('x'))))), 'f(9/1, 3/4, 1/2 / x)'),
# ndx = 6, CommAssoc '+'
        (CA('+', (neg0, temp4, neg0, Sy('z'), neg0)), '- x - (a = b) - x + z - x'),
# ndx = 7, CommAssoc '*'
        (CA('*', (temp5, Sy('x'), Sy('y'), temp5)), '(a = b) * x * y * (a = b)'),
# ndx = 8, null
        (null, '<NULL>'),
# ndx = 9, operators
        (
            Co('**', (Co('and', (Sy('a'), Sy('b'))),Co('>', (Sy('x'), Sy('y'))))),
            '(a and b) ** (x > y)',
        )
    ]
    return unparse_list

def test_alg_unparse_integration(stdsettings, unparse_list):
    for item in unparse_list:
        string = alg_unparse(item[0])

        assert string == item[1]


