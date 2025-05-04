from truealgebra.core.settings import SettingsSingleton
from truealgebra.common.commonsettings import commonsettings

from truealgebra.tasympy.setup_func import tasympy_setup_func
from truealgebra.tasympy.predicate import (
    number_type_rules, logic_rules, comparison_rules
)
from truealgebra.common.setup_func import common_setup_func

from truealgebra.core.abbrv import *   # import abbreviations
from truealgebra.core.expressions import true, false

import sympy
import pytest


@pytest.fixture
def settings(scope='module'):
    settings = SettingsSingleton()
    settings.reset()
    commonsettings.reset()
    tasympy_setup_func()
    common_setup_func()

    yield settings
        
    settings.reset()
    commonsettings.reset()


# ======================
# Test Number Type Rules
# ======================
@pytest.mark.parametrize(
    'string, correct',
    [
        (' isnumber(2) ', true),
        (' isnumber(3.5) ', true),
        (' isnumber(I) ', true),
        (' isnumber(x) ', false),
        (' isinteger(2) ', true),
        (' isinteger(2.3) ', false),
        (' isinteger(x) ', false),
        (' isrational(2/3) ', true),
        (' isrational(2.0) ', false),
        (' isrational(2) ', true),
        (' iscomplex(I) ', true),
        (' iscomplex(oo) ', false),
        (' isreal(2) ', true),
        (' isreal(3.7) ', true),
        (' isreal(I) ', false),
    ],
)
def test_number_type_rules(string, correct, settings):
    expr = settings.parse(string)

    out = number_type_rules(expr)

    assert out == correct


# ================
# Test Logic Rules
# ================
@pytest.mark.parametrize(
    'string, correct',
    [
        ('true and true', true),
        ('false and true', false),
        ('true and false', false),
        ('false and false', false),
        ('true and 5', Co('and', (Sy('true'), Nu(5)))),
        ('true or true', true),
        ('false or true', true),
        ('true or false', true),
        ('false or false', false),
        ('true or 5', Co('or', (Sy('true'), Nu(5)))),
        ('not true', false),
        ('not false', true),
        ('not 5', Co('not', (Nu(5),))),
    ],
    ids=[
        'true and true',
        'true and false',
        'false and true',
        'false and false',
        'true and 5',
        'true or true',
        'true or false',
        'false or true',
        'false or false',
        'true or 5',
        'not true',
        'not false',
        'not 5',
    ],
)
def test_logic_rules(string, correct, settings):
    pattern = settings.parse(string)

    outcome = logic_rules(pattern)

    outcome == correct

# =====================
# Test Comparison Rules
# =====================
@pytest.mark.parametrize(
    'string, correct',
    [
        ('2 == 2', true),
        ('1 == 2', false),
        ('x == x', true),
        ('x == y', Co('==', (Sy('x'), Sy('y')))),

        ('1 > 2', false),
        ('2 > 2', false),
        ('3 > 2', true),
        ('x > y', Co('>', (Sy('x'), Sy('y')))),

        ('1 >= 2', false),
        ('2 >= 2', true),
        ('3 >= 2', true),
        ('x >= y', Co('>', (Sy('x'), Sy('y')))),

        ('1 < 2', true),
        ('2 < 2', false),
        ('3 < 2', false),
        ('x < y', Co('>', (Sy('x'), Sy('y')))),

        ('1 <= 2', true),
        ('2 <= 2', true),
        ('3 <= 2', false),
        ('x <= y', Co('>', (Sy('x'), Sy('y')))),
    ],
    ids=[
        'areequal, equal num',
        'areequal, not equal num',
        'areequal, equal Symbol',
        'areequal, not equal Symbol',

        'greaterthan, lesser number',
        'greaterthan, equal number',
        'greaterthan, greater number',
        'greaterthan, symbols',

        'greaterthanequal, lesser number',
        'greaterthanequal, equal number',
        'greaterthanequal, greater number',
        'greaterthanequal, symbols',

        'lesserthan, lesser number',
        'lesserthan, equal number',
        'lesserthan, greater number',
        'lesserthan, symbols',

        'lesserthanequal, lesser number',
        'lesserthanequal, equal number',
        'lesserthanequal, greater number',
        'lesserthanequal, symbols',
    ]
)
def test_comparison_rules(string, correct, settings):
    pattern = settings.parse(string)

#   outcome = logic_rules(pattern)
    outcome = comparison_rules(pattern)

    outcome == correct

