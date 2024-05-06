"""Functional testing of unparse.

This is a refactoring of unit tests in previous test_expression_str_repr.py
for an older version of unparse. Some of the test and variable  names might
seem odd.
"""
from truealgebra.core.abbrv import (
    Co, CA, Sy, Nu
)
from truealgebra.core.parse import Parse
from truealgebra.core.expression import (
    ExprBase, Null, End
)
from truealgebra.core.settings import SettingsSingleton
from truealgebra.core.unparse import unparse
import pytest


@pytest.fixture
def settings(scope='module'):
    settings = SettingsSingleton()
    settings.reset()

    settings.set_default_bp(251, 252)
    settings.set_custom_bp('!', 2000, 0)
    settings.set_custom_bp('!!!', 3000, 0)
    settings.set_custom_bp('/', 1100, 1100)
    settings.set_custom_bp('**', 1251, 1250)
    settings.set_custom_bp('*', 1000, 999)
    settings.set_custom_bp("@", 0, 3000)
    settings.set_custom_bp("%", 0, 10)
    settings.set_custom_bp("!**", 1000, 1000)
    settings.set_custom_bp("!!*", 999, 2000)
    settings.set_custom_bp("!!**", 900, 2000)
    settings.set_custom_bp("!!+", 2000, 1000)
    settings.set_custom_bp("!!++", 2000, 900)

    settings.set_bodied_functions('D', 481)
    settings.set_symbol_operators("and", 75, 76)
    settings.set_infixprefix("-", 999)
    settings.set_container_subclass('*', CA)

    settings.set_sqrtneg1('j')

    yield settings
    settings.reset()


parse = Parse()


# Done
@pytest.mark.parametrize(
    ('expr, repr_'),
    [
        (Null(), '<NULL>'),
        (End(), '<END>'),
        (Nu(57.3), '57.3'),
        (Sy('abc'), 'abc'),
        (Co('f', (Nu(43), Sy('x'), Sy('y'))), 'f(43, x, y)'),
        (Co('f', (Nu(43),)), 'f(43)'),
        (Co('f', ()), 'f()'),
    ],
)
def test_repr(expr, repr_):
    assert unparse(expr) == repr_
#   assert repr(expr) == repr_


@pytest.fixture
def assign_exprbase_settings(settings):
    ExprBase.settings = settings
    parse = Parse(settings)
    yield parse
    ExprBase.settings = None


@pytest.mark.parametrize(
    'expr, unp',
    [
        (Co('f', (Sy('a'), Sy('b'), Sy('c'))), 'f(a, b, c)'),
        (Co('f', (Sy('a'),)), 'f(a)'),
        (Co('f', ()), 'f()'),
    ],
)
def test_unparse_function_notation(expr, unp, settings):
    out = unparse(expr)

    assert out == unp


@pytest.mark.parametrize(
    'expr, parent',
    [
        (Co('f', (Sy('x'), Nu(2))), 'f(x, 2)'),
        (Co('D', (Sy('x'),)), 'D() x'),
        (Co('D', (Sy('x'), Sy('y'))), 'D(x) y'),
    ],
)
def test_unparse_symbolname(
    expr, parent, settings
):
    out = unparse(expr)

    assert out == parent


# Functional TEsting
# data
unp_ex01 = Null()
unp_ex02 = End()
unp_ex03 = Nu(2.56)
unp_ex03a = Nu(complex(2, 3))
unp_ex04 = Sy('y')

unp_ex05a = Co('@@', (Nu(2), Nu(3)))
unp_ex05b = Co('abc', (Nu(2), Nu(3)))
unp_ex05c = Co('#', (Nu(2), Nu(3)))


unp_ex06 = Co('!', (Sy('x'),))
unp_ex07 = Co('@', (Sy('y'),))
unp_ex08 = Co('@@', (unp_ex06, unp_ex07))
unp_ex09 = Co('@@', (unp_ex06, Co('%%', (Sy('k'), unp_ex06))))
unp_ex10 = Co('%%', (Sy('k'), unp_ex06))
unp_ex11 = Co('%', (Sy('k'),))
unp_ex12 = Co('%', (unp_ex06,))
unp_ex13 = Co('D', (Sy('x'), Co('f', (Sy('x'),))))
unp_ex14 = Co('D', (Sy('x'), Co('@@', (Sy('x'), Sy('y')))))


@pytest.mark.parametrize(
    'expr, unp',
    [
        (unp_ex01, '<NULL>'),
        (unp_ex02, '<END>'),
        (unp_ex03, '2.56'),
        (unp_ex03a, '(2+3j)'),
        (unp_ex04, 'y'),

        # These unit test the Container _unparse method
        (unp_ex05a, '2 @@ 3'),
        (unp_ex05b, 'abc(2, 3)'),
        (unp_ex05c, '#(2, 3)'),

        (unp_ex06, 'x !'),
        (unp_ex07, '@ y'),
        (unp_ex08, 'x ! @@ @ y'),
        (unp_ex09, 'x ! @@ (k %% x !)'),
        (unp_ex10, 'k %% x !'),
        (unp_ex11, '% k'),
        (unp_ex12, '% x !'),
        (unp_ex13, 'D(x) f(x)'),
        (unp_ex14, 'D(x) (x @@ y)'),
    ]
)
def test_unparse_functional(expr, unp, settings):
    out = unparse(expr)

    assert out == unp


ca_ex01 = CA('*', (Sy('x'), Nu(4.3), Sy('y')))
ca_ex02 = CA('*', (Sy('x'),))
ca_ex03 = CA('*', ())

ca_ex04 = CA('*', (
        Co('and', (Sy('t'), Sy('t'))),
        Nu(3),
        Co('and', (Sy('t'), Sy('t')))
    )
)
ca_ex05 = CA('*', (
        Co('!**', (Sy('t'), Sy('t'))),
        Nu(3),
        Co('!*', (Sy('t'), Sy('t')))
    )
)
ca_ex06 = CA('*', (
        Nu(2),
        Co('!!*', (Sy('t'), Sy('t'))),
        Nu(3)
    )
)
ca_ex07 = CA('*', (
        Nu(2),
        Co('!!**', (Sy('t'), Sy('t'))),
        Nu(3)
    )
)
ca_ex08 = CA('*', (
        Nu(2),
        Co('**', (Sy('t'), Sy('t'))),
        Nu(3)
    )
)
ca_ex09 = CA('*', (
        Nu(2),
        Co('!!+', (Sy('t'), Sy('t'))),
        Nu(3)
    )
)
ca_ex10 = CA('*', (
        Nu(2),
        Co('!!++', (Sy('t'), Sy('t'))),
        Nu(3)
    )
)
ca_ex11 = CA('*', (
        Nu(2),
        Nu(3),
        Co('!!*', (Sy('t'), Sy('t'))),
    )
)
ca_ex12 = CA('*', (
        Nu(2),
        Nu(3),
        Co('!!**', (Sy('t'), Sy('t'))),
    )
)
ca_ex13 = CA('*', (
        Nu(2),
        Nu(3),
        Co('**', (Sy('t'), Sy('t'))),
    )
)
ca_ex14 = CA('*', (
        Co('**', (Sy('t'), Sy('t'))),
        Nu(2),
        Nu(3),
    )
)


@pytest.mark.parametrize(
    'expr, unp',
    [
        (ca_ex01, 'x * 4.3 * y'),
        (ca_ex02, '*(x)'),
        (ca_ex03, '*()'),
        (ca_ex04, '(t and t) * 3 * (t and t)'),
        (ca_ex05, 't !** t * 3 * (t !* t)'),
        (ca_ex06, '2 * (t !!* t) * 3'),
        (ca_ex07, '2 * (t !!** t) * 3'),
        (ca_ex08, '2 * t ** t * 3'),
        (ca_ex09, '2 * t !!+ t * 3'),
        (ca_ex10, '2 * (t !!++ t) * 3'),
        (ca_ex11, '2 * 3 * (t !!* t)'),
        (ca_ex12, '2 * 3 * (t !!** t)'),
        (ca_ex13, '2 * 3 * t ** t'),
        (ca_ex14, 't ** t * 2 * 3'),
    ]
)
def test_unparse_commassoc_functional(expr, unp, settings):
    out = unparse(expr)

    assert out == unp
