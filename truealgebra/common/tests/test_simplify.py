from truealgebra.core.settings import SettingsSingleton
from truealgebra.core.abbrv import Nu, Sy
from truealgebra.core.rules import Rule, JustOneBU, Substitute
from truealgebra.common.commonsettings import commonsettings
from truealgebra.common.setup_func import common_setup_func
from truealgebra.common.simplify import (
    simplify, SP, isSP, Pl, isPl
)
from truealgebra.common.utility import mulnums
from truealgebra.std.setup_func import std_setup_func

from types import MappingProxyType
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


# ============
# Test StarPwr
# ============
@pytest.fixture
def input_dict():
    return {Sy('x'): Nu(2), Sy('y'): Nu(6)}

@pytest.fixture
def starpwr(input_dict):
    return SP(coef=Nu(4), exp_dict=input_dict)

def test_starpwr_init(settings, input_dict, starpwr):
    assert starpwr.coef == Nu(4)
    assert starpwr.exp_dict == input_dict
    assert isinstance(starpwr.exp_dict, MappingProxyType)

def test_starpwr_repr(starpwr):
    repr_out = repr(starpwr)

    assert repr_out == 'SP(4, {x: 2, y: 6})'

def test_starpwr_hash(starpwr, input_dict):
    assert hash(starpwr) == hash((
        Nu(4),
        SP,
        frozenset(MappingProxyType(input_dict).items())
    ))


def test_starpwr_eq(input_dict, starpwr):
    class SPSubClass(SP):
        pass

    spsubclass = SPSubClass(coef=Nu(4), exp_dict=input_dict)

    assert not (starpwr == spsubclass)
    assert not (starpwr == SP(coef=Nu(3), exp_dict=input_dict))
    assert not (starpwr == SP(coef=Nu(4), exp_dict={
        Sy('x'): Nu(3), Sy('y'): Nu(6)
    }))
    assert starpwr == SP(coef=Nu(4), exp_dict={
        Sy('x'): Nu(2), Sy('y'): Nu(6)
    })


@pytest.fixture
def sp_bottomup_rule(settings):
    subber = Substitute(subdict={Sy('x'): Sy('w'), Sy('y'): Sy('z')},)

    class SPRule(Rule):
        def predicate(self, expr):
            return isSP(expr)

        def body(self, expr):
            return SP(mulnums(expr.coef, Nu(2)), expr.exp_dict)

    return JustOneBU(subber, SPRule())


def test_starpwr_bottomup(starpwr, sp_bottomup_rule):
    out = sp_bottomup_rule(starpwr)
    other = SP(Nu(8), {Sy('w'): Nu(2), Sy('z'): Nu(6)})
#   xxx = 100; embed()

#   assert out == SP(Nu(8), {Sy('w'): Nu(2), Sy('z'): Nu(6)})
    assert out == other




# ==============================
# These is are integration tests 
# ==============================
@pytest.mark.parametrize(
    "expr, correct",
    [
        ('star(x, 2 * x, y/x, x**2, y**3)', 'star(2, x**3, y**4)'),
        ('star(x, 5, plus( -y, y))', '0'),
        ('star(x/x, y)', 'y'),
        ('star(x/x, y/y)', '1'),
        ('plus(x, -x, y, z, -z)', 'y'),
        ('plus(x, -x, y, -1 * y)', '0'),
        ('x * y/x**2 * (x/2 + x/2)/y', '1'),
        (' (x * y)/(y * x**(-2)) ', ' x**3 '),
        ('star(2, 4, 1/3, 3 ** 2)', '24'),
        ('plus(2, 4, 1/3, 2/3)', '7'),
        ('plus(x, y-x, y, z, -z)', '2*y'),
        ('plus(x, y-x, y, z, - - -z)', '2*y'),
        ('- 5', '-5'),
        ('7-3', '4'),
    ],
    ids=[
        "star function",
        "star with plus function",
        "star with num1 coef",
        "star with two num1",
        "plus with two num0 and y",
        "plus with two num0",
        "star with x's and y's",
        "star with more x's and y's",
        "star with integer math",
        "plus with integer math",
        "plus with '-' operators",
        "plus with more '-' operators",
        "neagative number",
        "subtract number",
    ]
)
def test_integration_simplify(settings, expr, correct):
    output = simplify(settings.parse(expr))
    correct_expr  = settings.parse(correct)

    assert output == correct_expr


#This is an integration test 
def test_real_number_simlify(settings):
    expr = 'star(7.0, 3.5 - 5.7, - 2.1, 1.5 ** 2.1, 4.7 / 3.6, 1.2 + 3.5)'
    output = simplify(settings.parse(expr))
    correct = 464.96993758661546
#   xxx = 105; embed()

    assert output.value == pytest.approx(correct)
