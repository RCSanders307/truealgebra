from truealgebra.core.settings import SettingsSingleton
from truealgebra.common.commonsettings import commonsettings

from truealgebra.std.setup_func import std_setup_func
from truealgebra.common.setup_func import common_setup_func

from truealgebra.core.abbrv import *   # import abbreviations
from truealgebra.core.expressions import true, false

from fractions import Fraction
import pytest

from IPython import embed


@pytest.fixture
def settings(scope='module'):
    settings = SettingsSingleton()
    settings.reset()
    commonsettings.reset()
    std_setup_func()
    common_setup_func()

    yield settings
        
    settings.reset()
    commonsettings.reset()


#@pytest.fixture
#def stdsettings(scope='module'):
#    yield set_stdsettings()
#   settings.reset()
    

@pytest.fixture
def predicate(settings, scope='module'):
    from truealgebra.std import predicate
    return predicate


@pytest.fixture
def parse(settings, scope='module'):
    return settings.parse


# ======================
# Test Number Type Rules
# ======================
@pytest.mark.parametrize(
    'string, correct',
    [
        (' isnumber(2) ', true),
        (' isnumber(3.5) ', true),
        (' isnumber(j) ', true),
        (' isnumber(x) ', false),
        (' isint(2) ', true),
        (' isint(2.3) ', false),
        (' isfloat(2.3) ', true),
        (' isfloat(2) ', false),
        (' iscomplex(j) ', true),
        (' iscomplex(2) ', false),
        (' isreal(2) ', true),
        (' isreal(3.7) ', true),
        (' isreal(j) ', false),

    ],
    ids=[
        'isnumber, int',
        'isnumber, float',
        'isnumber, complex',
        'isnumber, Sy',
        'isint, int',
        'isint, real',
        'isfloat, float',
        'isfloat, int',
        'iscomplex, complex',
        'iscomplex, int',
        'isreal, int',
        'isreal, float',
        'isreal, complex',
    ]
)
def test_number_type_rules(string, correct, predicate, parse):
    expr = parse(string)

    out = predicate.number_type_rules(expr)

    assert out == correct


@pytest.mark.parametrize(
    'expr, correct',
    [
        (Co('isnumber',(Nu(Fraction(1, 2)),)), true),
        (Co('isfraction',(Nu(Fraction(1, 2)),)), true),
        (Co('isfraction',(Nu(3),)), false),
        (Co('isreal',(Nu(Fraction(1, 2)),)), true),
    ],
    ids=[
        'isnumber, Fraction',
        'isfraction, Fraction',
        'isfraction, int',
        'isreal, Fraction',
    ]
)
def test_number_type_rules_fraction(expr, correct, predicate):
    out = predicate.number_type_rules(expr)

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
def test_logic_rules(string, correct, predicate, parse):
    pattern = parse(string)

    outcome = predicate.logic_rules(pattern)

    outcome == correct


# =====================
# Test Cobaprison Rules
# =====================
@pytest.mark.parametrize(
    'string, correct',
    [
        ('2 == 2', true),
        ('1 == 2', false),
        ('x == x', true),
        ('x == y', false),

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
def test_comparison_rules(string, correct, predicate, parse):
    pattern = parse(string)

    outcome = predicate.comparison_rules(pattern)

    outcome == correct


# =============
# Test If Rules
# =============
@pytest.mark.parametrize(
    'string, correct_string',
    [
        ('if(true, x:=7)', 'x:=7'),
        ('if(false, x:=7)', 'if(false, x:=7)'),
        ('if(true, x:=7, x:=9)', 'x:=7'),
        ('if(false, x:=7, x:=9)', 'x:=9'),
    ],
    ids=[
        'if true',
        'if false',
        'elif true',
        'elif false',
    ]
)
def test_if(string, correct_string, predicate, parse):
    ex = parse(string)
    correct = parse(correct_string)
    out = predicate.if_rules(ex)

    assert out == correct
