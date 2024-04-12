from truealgebra.core.abbrv import (
    Co, CA, Sy, Nu
)
from truealgebra.core.parse import Parse
from truealgebra.core.expression import (
    ExprBase, Null, End, UnParse
)
from truealgebra.core.settings import SettingsSingleton, DIGITS, OPERATORS
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

parse = Parse(settings)


# Done
@pytest.mark.parametrize(
    ('expr, repr_'),
    [
        (ExprBase(), ' <EXPR> '),
        (Null(), ' <NULL> '),
        (End(), ' <END> '),
        (Nu(57.3), '57.3'),
        (Sy('abc'), 'abc'),
        (Co('f', (Nu(43), Sy('x'), Sy('y'))), 'f(43, x, y)'),
        (Co('f', (Nu(43),)), 'f(43)'),
        (Co('f', ()), 'f()'),
    ],
)
def test_repr(expr, repr_):
    assert repr(expr) == repr_


@pytest.fixture
def assign_exprbase_settings(settings):
    ExprBase.settings = settings
    parse = Parse(settings)
    yield parse
    ExprBase.settings = None


@pytest.mark.parametrize(
    'expr, albp, arbp',
    [
        (Co('-', (Nu(3),)), 0, 999),
        (Co('**', (Nu(3), (Sy('n')))), 1251, 1250),
        (Co('and', (Sy('A'), (Sy('B')))), 75, 76),
        (Co('@@', (Sy('A'), (Sy('B')))), 251, 252),
        (Co('#', (Sy('A'), (Sy('B')))), 251, 252),
    ],
)
def test_unparse_find_albp_arbp(expr, albp, arbp, assign_exprbase_settings):
    albp_out, arbp_out = expr._unparse_find_albp_arbp()

    assert albp == albp_out
    assert arbp == arbp_out


# Done
@pytest.mark.parametrize(
    'expr, unp, items',
    [
        (Co('f', (Sy('a'), Sy('b'), Sy('c'))), 'f(a, b, c)', None),
        (Co('f', (Sy('a'),)), 'f(a)', None),
        (Co('f', ()), 'f()', None),
        (Co('D', (Sy('x'), Sy('y'))), 'D(x)', (Sy('x'),)),
    ],
)
def test_unparse_function_notation(expr, unp, items, assign_exprbase_settings):
#   parse = assign_exprbase_settings
    if items is None:
        out = expr._unparse_function_notation()
    else:
        out = expr._unparse_function_notation(items)

    assert out.string == unp
    assert out.albp == 0
    assert out.arbp == 0


    # done
@pytest.mark.parametrize(
    'expr, parent, right, arbp',
    [
        (Co('f', (Sy('x'), Nu(2))), 'f(x, 2)', None, 0),
        (Co('D', ()), 'D()', None, 0),
        (Co('D', (Sy('x'),)), 'D()', 'x', 481),
        (Co('D', (Sy('x'), Sy('y'))), 'D(x) ', 'y', 481),
    ],
)
def test_unparse_symbolname(
    expr, parent, right, arbp, assign_exprbase_settings
):
    out = expr._unparse_symbolname()

    assert out[0] is None
    if isinstance(out[2], UnParse):
        assert out[2].string == right
    else:
        assert out[2] is None
    assert out[1].string == parent
    assert out[1].albp == 0
    assert out[1].arbp == arbp


# Functional TEsting
# data
unp_ex00 = ExprBase()
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
unp_ex09 = Co('@@', (unp_ex06, Co('%', (Sy('k'), unp_ex06))))
unp_ex10 = Co('%', (Sy('k'), unp_ex06))
unp_ex11 = Co('%', (Sy('k'),))
unp_ex12 = Co('%', (unp_ex06,))
unp_ex13 = Co('D', (Sy('x'), Co('f', (Sy('x'),))))
unp_ex14 = Co('D', (Sy('x'), Co('@@', (Sy('x'), Sy('y')))))


@pytest.mark.parametrize(
    'expr, unp, albp, arbp',
    [
        # These unit test ExprBase, Null, End, Number, and Symbol.
        (unp_ex00, ' <EXPRBASE> ', 0, 0),
        (unp_ex01, ' <NULL> ', 0, 0),
        (unp_ex02, ' <END> ', 0, 0),
        (unp_ex03, '2.56', 0, 0),
        (unp_ex03a, '(2+3j)', 0, 0),
        (unp_ex04, 'y', 0, 0),

        # These unit test the Container _unparse method
        (unp_ex05a, '2 @@ 3', 251, 252),
        (unp_ex05b, 'abc(2, 3)', 0, 0),
        (unp_ex05c, '#(2, 3)', 0, 0),

        (unp_ex06, 'x !', 2000, 0),
        (unp_ex07, '@ y', 0, 3000),
        (unp_ex08, 'x ! @@ @ y', 2000, 3000),
        (unp_ex09, 'x ! @@ %(k, x !)', 2000, 252),
        (unp_ex10, '%(k, x !)', 0, 0),
        (unp_ex11, '% k', 0, 10),
        (unp_ex12, '% x !', 0, 10),
        (unp_ex13, 'D(x) f(x)', 0, 481),
        (unp_ex14, 'D(x) (x @@ y)', 0, 481),
    ]
)
def test_unparse_functional(expr, unp, albp, arbp, assign_exprbase_settings):
    out = expr._unparse()

    assert out.string == unp
    assert out.albp == albp
    assert out.arbp == arbp


# done
@pytest.mark.parametrize(
    'left, parent, right, correct',
    [
        (
            UnParse('@ 4', 0, 3000), 
            UnParse(' !!!', 3000, 0),
            None,
            UnParse('@ 4 !!!', 3000, 0),
        ),
        (
            UnParse('% 4', 0, 10), 
            UnParse(' !!!', 3000, 0),
            None,
            UnParse('(% 4) !!!', 3000, 0),
        ),
        (
            UnParse('x ** 4', 1251, 1250), 
            UnParse(' @@ ', 251, 252),
            UnParse('34', 0, 0),
            UnParse('x ** 4 @@ 34', 1251, 252),
        ),
        (
            UnParse('abc(2, 3)', 0, 0), 
            UnParse(' @@ ', 251, 252),
            UnParse('34', 0, 0),
            UnParse('abc(2, 3) @@ 34', 251, 252),
        ),
        (
            None,
            UnParse('@ ', 0, 3000),
            UnParse('4 @@ 3', 251, 252),
            UnParse('@ (4 @@ 3)', 0, 3000),
        ),
        (
            None,
            UnParse('@ ', 0, 3000),
            UnParse('4 !!!', 3000, 0),
            UnParse('@ (4 !!!)', 0, 3000),
        ),
    ]
)
def test_uparse_parenthesis_or_not(left, parent, right, correct):
    expr = Co('abc', ())
    out = expr._unparse_parenthesis_or_not(left, parent, right)

    assert out.string == correct.string
    assert out.albp == correct.albp
    assert out.arbp == correct.arbp



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
    'expr, unp, albp, arbp',
    [
        (ca_ex01, 'x * 4.3 * y', 1000, 999),
        (ca_ex02, 'x', 0, 0),
        (ca_ex03, '*()', 0, 0),
        (ca_ex04, '(t and t) * 3 * (t and t)', 1000, 999),
        (ca_ex05, 't !** t * 3 * (t !* t)', 1000, 999),
        (ca_ex06, '2 * (t !!* t) * 3', 1000, 999),
        (ca_ex07, '2 * (t !!** t) * 3', 1000, 999),
        (ca_ex08, '2 * t ** t * 3', 1000, 999),
        (ca_ex09, '2 * t !!+ t * 3', 1000, 999),
        (ca_ex10, '2 * (t !!++ t) * 3', 1000, 999),
        (ca_ex11, '2 * 3 * (t !!* t)', 1000, 999),
        (ca_ex12, '2 * 3 * (t !!** t)', 1000, 999),
        (ca_ex13, '2 * 3 * t ** t', 1000, 1250),
        (ca_ex14, 't ** t * 2 * 3', 1251, 999),
        # next do the end of items
    ]
)
def test_unparse_commassoc_functional(
    expr, unp, albp, arbp, assign_exprbase_settings
):
    out = expr._unparse()

    assert out.string == unp
    assert out.albp == albp
    assert out.arbp == arbp
