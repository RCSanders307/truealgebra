from truealgebra.core.unparse import (
    unparse, ReadableString, UnparseSymbol, UnparseNumber, ReadableHandlerBase
)
from truealgebra.core.settings import SettingsSingleton
from truealgebra.core.expressions import CommAssoc, Symbol, NullSingleton
from truealgebra.core.abbrv import Sy, Co, Nu
from truealgebra.core.rules import Rule
from truealgebra.core.parse import Parse
import pytest

parse = Parse()


@pytest.fixture
def settings(scope='module'):
    settings = SettingsSingleton()
    settings.reset()
    settings.set_custom_bp('+', 0, 10)
    settings.set_custom_bp('-', 6, 100)
    settings.set_custom_bp('*', 10, 0)
    settings.set_custom_bp('@', 9, 9)
    settings.set_custom_bp('/', 8, 0)

    settings.set_symbol_operators('prefix0', 0, 6)
    settings.set_symbol_operators('postfix0', 10, 0)
    settings.set_symbol_operators('postfix1', 100, 0)
    settings.set_symbol_operators('and', 12, 12)
    settings.set_symbol_operators('infix0', 12, 6)
    settings.set_symbol_operators('infix1', 6, 6)
    settings.set_bodied_functions('D', 15)
    settings.set_container_subclass('@', CommAssoc)

    settings.set_default_bp(300, 301)

    yield settings
    settings.reset()


@pytest.fixture
def flatten(scope='module'):
    class Flatten(Rule):
        def predicate(self, expr):
            return isinstance(expr, CommAssoc)

        def body(self, expr):
            newitems = []
            for item in expr.items:
                if isinstance(item, CommAssoc) and item.name == expr.name:
                    newitems.extend(item.items)
                else:
                    newitems.append(item)
            return CommAssoc(expr.name, newitems)

    return Flatten()


@pytest.fixture
def SpecialObject(scope='module'):
    class SpecialObject:
        def __str__(self):
            return 'I am a special object'
    return SpecialObject


@pytest.fixture
def readspecial(SpecialObject, settings):
    rs = ReadableString(UnparseNumber, UnparseSymbol)

    class UnparseSpecial(ReadableHandlerBase):
        def handle_expr(self, expr):
            if isinstance(expr, SpecialObject):
                return 'unparsed special object'

    rs.addhandler(UnparseSpecial)
    return rs


# Functional Tests of unparse
# ===========================
# The class structure is very simple.
# So the ReadableHandlerBase instances re tested.
@pytest.mark.parametrize(
    "string",
    [
        '+ bj',
        'a *',
        'a - b',
        '+ (a - b)',
        '(a infix1 b) *',
        'x - (a and b)',
        'D(x) (y and z)',
    ]
)
def test_operators(string, settings):
    expr = parse(string)
    str_out = unparse(expr)

    assert string == str_out


@pytest.mark.parametrize(
    'string',
    [
        'q @ w @ e @ w @ r',
        'q @ (w - e) @ r',
        'q @ (w infix0 e) @ r',
        'q @ (w infix1 e) @ r',
        '+ q @ r',
        '(prefix0 q) @ r',
        'q @ r *',
        'q @ (r /)',
        'q @ w and e @ r',
    ]
)
def test_commassoc(flatten, string, settings):
    expr = flatten(parse(string))
    outstr = unparse(expr)

    assert outstr == string


@pytest.mark.parametrize(
    'expr, string',
    [
        (CommAssoc('@', (Symbol('x'),)), '@(x)'),
        (CommAssoc('@', ()), '@()'),
    ]
)
def test_commassoc_special(expr, string, settings):
    outstr = unparse(expr)

    assert outstr == string


@pytest.mark.parametrize(
    'string',
    [
        # test Function form
        'func(x, y, z)',
        'func()',
        # test symbol
        'abc',
        # test number
        '3.56',
        '54',
        # test bodied function
        'D(x, y) z',
        'D(x) y postfix0',
        'D(x) y postfix1',
        '(D(x) y) postfix1',
    ],
)
def test_assorted_expressions(string, settings):
    expr = parse(string)
    str_out = unparse(expr)

    assert string == str_out


def test_null(settings):
    expr = NullSingleton()
    strout = unparse(expr)

    assert strout == '<NULL>'


# Test unparse Methods
# ====================

@pytest.mark.parametrize(
    'expr, correct',
    [
        (Co('-', (Sy('x'), Sy('y'))), 6),  # custom
        (Co('+++', (Sy('x'), Sy('y'))), 300),  # default
        (Co('D', (Sy('x'), Sy('y'))), 0),  # bodied
        (Co('and', (Sy('x'), Sy('y'))), 12),  # symbol op
        (Co('abc', (Sy('x'), Sy('y'))), 0),  # funct
        (Sy('x'), 0),   # symbol
        (Nu(5), 0),   # number
    ]
)
def test_token_left_binding_power(expr, correct, settings):
    lbp = unparse.tlbp(expr)

    assert lbp == correct


@pytest.mark.parametrize(
    'expr, correct',
    [
        (Co('-', (Sy('x'), Sy('y'))), 100),  # custom
        (Co('+++', (Sy('x'), Sy('y'))), 301),  # default
        (Co('D', (Sy('x'), Sy('y'))), 15),  # bodied
        (Co('and', (Sy('x'), Sy('y'))), 12),  # symbol
        (Co('abc', (Sy('x'), Sy('y'))), 0),  # funct
        (Sy('x'), 0),   # symbol
        (Nu(5), 0),   # number
    ]
)
def test_token_right_binding_power(expr, correct, settings):
    rbp = unparse.trbp(expr)

    assert rbp == correct


@pytest.mark.parametrize(
    'items, correct',
    [
        ((Sy('w'), Sy('x'), Sy('y'), Sy('z')), 'abc(w, x, y, z)'),
        ((Sy('w'), Sy('z')), 'abc(w, z)'),
        ((Sy('w'),), 'abc(w)'),
        ((), 'abc()'),
    ]
)
def test_funct_form(items, correct, settings):
    outstr = unparse.funct_form('abc', items)

    assert outstr == correct


@pytest.mark.parametrize(
    'string, correct',
    [
        (' 7 ', 0),
        (' x ', 0),
        (' f(x, y)', 0),
        (' x - y * *', 6),
        (' x * - y  *', 6),
        (' x *  / *  ', 8),
    ]
)
def test_least_left_binding_power(string, correct, settings):
    expr = parse(string)
    llbp = unparse.llbp(expr)

    assert llbp == correct


@pytest.mark.parametrize(
    'string, correct',
    [
        (' 7 ', 0),
        (' x ', 0),
        (' f(x, y) ', 0),
        (' + prefix0 + x', 6),
        (' y and + prefix0 x ', 6),
        (' + y and + + x ', 10),
    ]
)
def test_least_right_binding_power(string, correct, settings):
    expr = parse(string)
    lrbp = unparse.lrbp(expr)

    assert lrbp == correct


# need_parenthesis_on_right
@pytest.mark.parametrize('string', ['x * and y / ', 'x @ y / * '])
@pytest.mark.parametrize('rbp, correct', [(6, False), (8, True), (10, True)])
def test_need_parenthesis_on_right(string, correct, rbp, settings):
    expr = parse(string)
    out = unparse.need_parenthesis_on_right(rbp, expr)

    assert out is correct


# need_parenthesis_on_left
@pytest.mark.parametrize('string', ['prefix0 + + x', '+ prefix0 + x'])
@pytest.mark.parametrize('lbp, correct', [(4, False), (6, False), (8, True)])
def test_need_parenthesis_on_left(string, correct, lbp, settings):
    expr = parse(string)
    out = unparse.need_parenthesis_on_left(lbp, expr)

    assert out is correct


# deal with right
@pytest.mark.parametrize(
    'rbp, correct',
    [
        (6, ' x * and y /'),
        (8, ' (x * and y /)'),
        (10, ' (x * and y /)')
    ]
)
def test_deal_with_right(correct, rbp, settings):
    string = 'x * and y /'
    expr = parse(string)
    out = unparse.deal_with_right(rbp, expr)

    assert out == correct


# deal with left
@pytest.mark.parametrize(
    'lbp, correct',
    [
        (4, 'prefix0 + + x '),
        (6, 'prefix0 + + x '),
        (8, '(prefix0 + + x) ')
    ]
)
def test_deal_with_left(correct, lbp, settings):
    string = ' prefix0 + + x '
    expr = parse(string)
    out = unparse.deal_with_left(lbp, expr)

    assert out == correct


# Test addhandler and last_handler Methods
# ========================================
def test_last_handler(SpecialObject, settings):
    specialobject = SpecialObject()
    out = unparse(specialobject)

    assert out == 'I am a special object'


def test_addhandler(SpecialObject, readspecial, settings):
    specialobject = SpecialObject()
    out = readspecial(specialobject)

    assert out == 'unparsed special object'
