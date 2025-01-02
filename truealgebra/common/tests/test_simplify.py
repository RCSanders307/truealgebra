from truealgebra.core.settings import SettingsSingleton
from truealgebra.core.abbrv import Nu, Sy, CA, Co
from truealgebra.core.rules import Rule, JustOneBU, Substitute
from truealgebra.common.commonsettings import commonsettings
from truealgebra.common.commonsettings import commonsettings as comset
from truealgebra.common.setup_func import common_setup_func
from truealgebra.common.simplify import (
    simplify, SP, isSP, Pl, isPl, PseudoSP, PseudoP,
    StarToSPP, DivToSPP, PwrToSPP, NegToSPP, AddToSPP, MinusToSPP,
    convertfromstarpwr
)
from truealgebra.common.utility import mulnums, addnums
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
    return SP(coef=Nu(4), expdict=input_dict)


def test_starpwr_init(settings, input_dict, starpwr):
    assert starpwr.coef == Nu(4)
    assert starpwr.expdict == input_dict
    assert isinstance(starpwr.expdict, MappingProxyType)


def test_starpwr_repr(starpwr):
    repr_out = repr(starpwr)

    assert repr_out == 'StarPwr(4, {x: 2, y: 6})'


def test_starpwr_eq(settings, input_dict, starpwr):
    class SPSubClass(SP):
        pass

    spsubclass = SPSubClass(coef=Nu(4), expdict=input_dict)

    assert not (starpwr == spsubclass)
    assert not (starpwr == SP(coef=Nu(3), expdict=input_dict))
    assert not (starpwr == SP(coef=Nu(4), expdict={
        Sy('x'): Nu(3), Sy('y'): Nu(6)
    }))
    assert starpwr == SP(coef=Nu(4), expdict={
        Sy('x'): Nu(2), Sy('y'): Nu(6)
    })


@pytest.fixture
def sp_bottomup_rule(settings):
    subber = Substitute(subdict={Sy('x'): Sy('w'), Sy('y'): Sy('z')},)

    class SPRule(Rule):
        def predicate(self, expr):
            return isSP(expr)

        def body(self, expr):
            return SP(mulnums(expr.coef, Nu(2)), expr.expdict)

    return JustOneBU(subber, SPRule())


def test_starpwr_bottomup(settings, starpwr, sp_bottomup_rule):
    out = sp_bottomup_rule(starpwr)
    other = SP(Nu(8), {Sy('w'): Nu(2), Sy('z'): Nu(6)})

    assert out == other


@pytest.fixture
def sp_bottomup_rule2(settings):
    subber = Substitute(subdict={Sy('x'): Sy('y')},)

    class SPRule(Rule):
        def predicate(self, expr):
            return isSP(expr)

        def body(self, expr):
            return SP(mulnums(expr.coef, Nu(2)), expr.expdict)

    return JustOneBU(subber, SPRule())


# Test use of pseudoSP in bottomup method 
def test_starpwr_bottomup2(starpwr, sp_bottomup_rule2):
    out = sp_bottomup_rule2(starpwr)
    other = SP(Nu(8), {Sy('y'): Nu(8),})

    assert out == other


# =============
# Test PseudoSP
# =============
@pytest.fixture
def pseudoSP(settings):
    return PseudoSP(coef=Nu(3), expdict={Sy('x'): Nu(2), Sy('y'): Nu(3)})


@pytest.mark.parametrize(
    "key, value, correct",
    [
        (
            Sy('x'),
            Nu(-2),
            PseudoSP(coef=Nu(3), expdict={Sy('y'): Nu(3)})
        ),
        (
            Sy('x'),
            Nu(2),
            PseudoSP(Nu(3), {Sy('x'): Nu(4), Sy('y'): Nu(3)})
        ),
        (
            Sy('z'),
            Nu(2),
            PseudoSP(Nu(3), {Sy('x'): Nu(2), Sy('y'): Nu(3), Sy('z'): Nu(2)})
        ),
    ],
)
def test_mul_keyvalue(settings, pseudoSP, key, value, correct):
    pseudoSP.mul_keyvalue(key, value)

    assert pseudoSP.coef == correct.coef
    assert pseudoSP.expdict == correct.expdict


def test_merge_starpwr(settings, pseudoSP):
    starpwr = SP(Nu(2), {Sy('z'): Nu(2), Sy('x'): Nu(1)})

    pseudoSP.merge_starpwr(starpwr)

    assert pseudoSP.coef == Nu(6)
    assert pseudoSP.expdict == {
        Sy('z'): Nu(2), Sy('x'): Nu(3), Sy('y'): Nu(3)
    }


@pytest.mark.parametrize(
    "pseudo, correct",
    [
        (PseudoSP(Nu(0), {Sy('x'): Nu(2)}), Nu(0)),
        (PseudoSP(Nu(3), dict()) , Nu(3)),
        (PseudoSP(Nu(1), {Sy('x'): Nu(1)}), Sy('x')),
        (
            PseudoSP(Nu(3), {Sy('x'): Nu(2), Sy('y'): Nu(4)}),
            SP(Nu(3), {Sy('x'): Nu(2), Sy('y'): Nu(4)}),
        ),
    ],
)
def test_return_sp(settings, pseudo, correct):
    out = pseudo.return_SP()

    assert out == correct


@pytest.mark.parametrize(
    "key, value, correct",
    [
        (Sy('x'), Nu(2), PseudoSP(Nu(3), {Sy('y'): Nu(3),})),
        (
            Sy('x'),
            Nu(-2),
            PseudoSP(Nu(3), {Sy('x'): Nu(4), Sy('y'): Nu(3)})
        ),
        (
            Sy('z'),
            Nu(2),
            PseudoSP(Nu(3), {Sy('x'): Nu(2), Sy('y'): Nu(3), Sy('z'): Nu(-2)})
        ),
    ],
)
def test_div_keyvalue(settings, pseudoSP, key, value, correct):
    pseudoSP.div_keyvalue(key, value)

    assert pseudoSP.coef == correct.coef
    assert pseudoSP.expdict == correct.expdict


def test_div_starpwr(settings, pseudoSP):
    starpwr = SP(Nu(3), {Sy('z'): Nu(2), Sy('x'): Nu(1)})

    pseudoSP.div_starpwr(starpwr)

    assert pseudoSP.coef == Nu(1)
    assert pseudoSP.expdict == {
        Sy('z'): Nu(-2), Sy('x'): Nu(1), Sy('y'): Nu(3)
    }


def test_apply_exponent(settings, pseudoSP):
    pseudo = PseudoSP(Nu(3), {Sy('x'): Nu(2), Sy('y'): Nu(3)})

    pseudo.apply_exponent(Nu(3))

    assert pseudo.coef == Nu(27)
    assert pseudo.expdict == {Sy('x'): Nu(6), Sy('y'): Nu(9)}


# =========
# Test Plus
# =========
@pytest.fixture
def plus(settings):
    return Pl(num=Nu(3), items=[
        SP(coef=Nu(2), expdict={Sy('x'): Nu(3)}),
    ])


def test_plus_init(settings, plus):
    assert plus.num == Nu(3)
    assert plus.items == (SP(Nu(2), {Sy('x'): Nu(3)}),)


def test_plus_init_default():
    plus = Pl()

    assert plus.num == comset.num0
    assert plus.items == tuple()


def test_plus_repr(settings, plus):
    assert repr(plus) == 'Plus(3, (StarPwr(2, {x: 3})))'


def test_plus_eq(settings, plus):
    class PlSubClass(Pl):
        pass

    plsubclass = PlSubClass(plus.num, plus.items)
    plus0 = Pl(Nu(2), plus.items)
    plus1 = Pl(plus.num, (SP(Nu(2), {Sy('y'): Nu(3)}),))
    plus2 = Pl(plus.num, plus.items)

    assert not (plus == plsubclass)
    assert not (plus == plus0)
    assert not (plus == plus1)
    assert plus == plus2


@pytest.fixture
def pl_bottomup_rule(settings):
    class PlRule(Rule):
        def predicate(self, expr):
            return isPl(expr)

        def body(self, expr):
            return Pl(addnums(expr.num, Nu(2)), expr.items)

    class SPRule(Rule):
        def predicate(self, expr):
            return isSP(expr)

        def body(self, expr):
            return SP(addnums(expr.coef, Nu(2)), expr.expdict)

    return JustOneBU(PlRule(), SPRule())
        
        
def test_plus_bottomup(settings, plus, pl_bottomup_rule):
    correct = Pl(Nu(5), (SP(Nu(4), {Sy('x'): Nu(3)}),))

    out = pl_bottomup_rule(plus)
    
    assert out == correct

# =============
# Test PseudoP
# =============
@pytest.fixture
def pseudoP(settings):
    return PseudoP(num=Nu(3), items=[
        SP(Nu(1), {Sy('x'): Nu(2)}),
        SP(Nu(2), {Sy('y'): Nu(3)})
    ])


@pytest.mark.parametrize(
    "item, correct",
    [
        (SP(Nu(3), {Sy('x'): Nu(2)}), SP(Nu(3), {Sy('x'): Nu(2)})),
    (Sy('y'), SP(Nu(1), {Sy('y'): Nu(1)})),
    ],
)
def test_make_item_sp(settings, pseudoP, item, correct):
    out = pseudoP.make_item_SP(item)

    assert out == correct


@pytest.mark.parametrize(
    "itemsp, correctitems",
    [
        (
            SP(Nu(4), {Sy('x'): Nu(2)}),
            [
                SP(Nu(5), {Sy('x'): Nu(2)}),
                SP(Nu(2), {Sy('y'): Nu(3)})

            ]
        ),
        (
            SP(Nu(4), {Sy('z'): Nu(2)}),
            [
                SP(Nu(1), {Sy('x'): Nu(2)}),
                SP(Nu(2), {Sy('y'): Nu(3)}),
                SP(Nu(4), {Sy('z'): Nu(2)}),

            ]
        ),
    ],
)
def test_append_itemSP(settings, pseudoP, itemsp, correctitems):
    pseudoP.append_itemSP(itemsp)

    assert pseudoP.num == Nu(3)
    assert pseudoP.items == correctitems


def test_merge_plus(settings, pseudoP):
    plus = PseudoP(Nu(2), [
        SP(Nu(4), {Sy('x'): Nu(2)}),
        SP(Nu(4), {Sy('z'): Nu(2)}),
    ])

    pseudoP.merge_plus(plus)

    assert pseudoP.num == Nu(5)
    assert pseudoP.items == [
        SP(Nu(5), {Sy('x'): Nu(2)}),
        SP(Nu(2), {Sy('y'): Nu(3)}),
        SP(Nu(4), {Sy('z'): Nu(2)}),
    ]


def test_clean_items(settings):
    pseudo = PseudoP(Nu(2), [
        SP(Nu(0), {Sy('x'): Nu(3)}),
        SP(Nu(1), {Sy('x'): Nu(2)}),
        SP(Nu(0), {Sy('y'): Nu(2)}),
        SP(Nu(1), {Sy('y'): Nu(3)}),
        SP(Nu(0), {Sy('z'): Nu(3)}),
    ])

    pseudo.clean_items()

    assert pseudo.num == Nu(2)
    assert pseudo.items == [
        SP(Nu(1), {Sy('x'): Nu(2)}),
        SP(Nu(1), {Sy('y'): Nu(3)}),
    ]


@pytest.mark.parametrize(
    "pseudo, correct",
    [
        (PseudoP(Nu(7), {}), Nu(7)),
        (
            PseudoP(Nu(0), [SP(Nu(1), {Sy('x'): Nu(1)})]),
            Sy('x')
        ),
        (
            PseudoP(Nu(0), [SP(Nu(3), {Sy('x'): Nu(2)})]),
            SP(Nu(3), {Sy('x'): Nu(2)})
        ),
        (
            PseudoP(Nu(5), [SP(Nu(2), {Sy('x'): Nu(2)})]),
            Pl(Nu(5), [SP(Nu(2), {Sy('x'): Nu(2)})]),
        ),
    ],
)
def test_return_P(settings, pseudo, correct):
    out = pseudo.return_P()

    assert out == correct


# ===================
# Test StarToSPP Rule
# ===================
@pytest.fixture
def startospp(scope='module'):
    return StarToSPP()


@pytest.mark.parametrize(
    "expr, correct",
    [
        (CA('*', (Sy('x'), Sy('y'))), True),
        (CA('+', (Sy('x'), Sy('y'))), False),
        (Co('*', (Sy('x'), Sy('y'))), False),
    ],
)
def test_startospp_predicate(settings, startospp, expr, correct):
    assert  startospp.predicate(expr) == correct


@pytest.mark.parametrize(
    "expr, correct",
    [
        (
            CA('*', (
                Nu(3), Sy('x'),
                SP(Nu(2), {Sy('y'): Nu(2), Sy('z'): Nu(1)}),
                Nu(5),
            )),
            SP(Nu(30), {Sy('x'): Nu(1), Sy('y'): Nu(2), Sy('z'): Nu(1)})
        ),
        (
            CA('*', (
                Sy('x'),
                SP(comset.num1, {Sy('y'): Nu(2)}),
                SP(comset.num1, {Sy('y'): Nu(-2)})
            )),
            Sy('x')
        ),
        (CA('*', (Nu(2), Nu(3))), Nu(6)),
        (CA('*', (Nu(0), Sy('x'), Sy('y'))), Nu(0)),
    ],
    ids=[
        'inputs: symbol, StarPlus object, numbers',
        "Sy('y') terms cancel, coef is 1, sy('x') exponent is 1.",
        'numbers multiplied, no Starplus',
        'output is 0',
    ]
)
def test_startospp_body(settings, startospp, expr, correct):
    newexpr = startospp.body(expr)

    assert newexpr == correct


# ===================
# Test DivToSPP Rule
# ===================
@pytest.fixture
def divtospp(scope='module'):
    return DivToSPP()


@pytest.mark.parametrize(
    "expr, correct",
    [
        (Co('/', (Sy('x'), Sy('y'))), True),
        (Co('+', (Sy('x'), Sy('y'))), False),
        (Co('/', (Sy('x'), Sy('y'), Sy('z'))), False),
    ],
)
def test_divtospp_predicate(settings, divtospp, expr, correct):
    assert  divtospp.predicate(expr) == correct


@pytest.mark.parametrize(
    'expr, correct',
    [
        (
            Co('/', (Sy('y'), Sy('x'))), 
            SP(expdict={Sy('y'): Nu(1), Sy('x'): Nu(-1)})
        ),
        (
            Co('/', (SP(coef=Nu(3), expdict={Sy('y'): Nu(2)}), Sy('y'))),
            SP(coef=Nu(3), expdict={Sy('y'): Nu(1)})
        ),
        (
            Co('/', (Sy('y'), SP(coef=Nu(2), expdict={Sy('y'): Nu(2)}))),
            SP(coef=Nu(0.5), expdict={Sy('y'): Nu(-1)})
        ),
        (
            Co('/', (
                SP(coef=Nu(4), expdict={Sy('y'): Nu(2)}),
                SP(coef=Nu(2), expdict={Sy('y'): Nu(2)})
            )),
            Nu(2)
        ),
    ],
    ids=[
        'non starpwr arguments',
        'upstairs strpwr argument',
        'downstairs strpwr argument',
        'both starpwr arguments',
    ]
)
def test_divtospp_body(settings, divtospp, expr, correct):
    out = divtospp(expr)

    assert out == correct


#==============
# Test pwrtospp
#==============
@pytest.fixture
def pwrtospp(scope='module'):
    return PwrToSPP()


@pytest.mark.parametrize(
    "expr, correct",
    [
        (Co('**', (Sy('x'), Sy('y'))), True),
        (Co('+', (Sy('x'), Sy('y'))), False),
        (Co('**', (Sy('x'), Sy('y'), Sy('z'))), False),
    ],
)
def test_pwrtospp_predicate(settings, pwrtospp, expr, correct):
    assert  pwrtospp.predicate(expr) == correct


@pytest.mark.parametrize(
    'expr, correct',
    [
        (
            Co('**', (SP(Nu(3), {Sy('x'): Nu(3)}), Nu(2))),
            SP(Nu(9), {Sy('x'): Nu(6)}),
        ),
        (
            Co('**', (Sy('x'),Sy('n'))),
            Co('**', (Sy('x'),Sy('n'))),
        ),
    ],
    ids=[
        'numeric exponent',
        'no numeric exponent',
    ]
)
def test_pwrtospp_body(settings, expr, correct, pwrtospp):
    out = pwrtospp.body(expr)

    assert out == correct

# ==============
# Test negtospp
#==============
@pytest.fixture
def negtospp(scope='module'):
    return NegToSPP()


@pytest.mark.parametrize(
    "expr, correct",
    [
        (Co('-', (Sy('x'),)), True),
        (Co('+', (Sy('x'),)), False),
        (Co('-', (Sy('x'), Sy('y'), Sy('z'))), False),
    ],
)
def test_negtospp_predicate(settings, negtospp, expr, correct):
    assert  negtospp.predicate(expr) == correct


@pytest.mark.parametrize(
    "expr0, correct",
    [
        (Nu(7), Nu(-7)),
        (SP(Nu(3), {Sy('x'): Nu(2)}), SP(Nu(-3), {Sy('x'): Nu(2)})),
        (Sy('x'), SP(Nu(-1), {Sy('x'): Nu(1)})),
        (SP(Nu(-1), {Sy('x'): Nu(1)}), Sy('x')),
    ],
)
def test_negtospp_body(settings, negtospp, expr0, correct):
    out = negtospp.body(Co('-', (expr0,)))

    assert out == correct

# ==============
# Test addtospp
#===============
@pytest.fixture
def addtospp(scope='module'):
    return AddToSPP()


@pytest.mark.parametrize(
    "expr, correct",
    [
        (CA('+', (Sy('x'), Sy('y'))), True),
        (CA('*', (Sy('x'), Sy('y'))), False),
        (Co('+', (Sy('x'), Sy('y'))), False),
    ],
)
def test_addtospp_predicate(settings, addtospp, expr, correct):
    assert  addtospp.predicate(expr) == correct


def test_addtospp_body(settings, addtospp):
    plusin = Co('+', (
        Nu(3), Nu(4),
        Pl(Nu(4), [SP(Nu(3), {Sy('x'): Nu(2)}), SP(Nu(-2), {Sy('x'): Nu(1)})]),
        Pl(Nu(0), [SP(Nu(2), {Sy('x'): Nu(1)})]),
        Co('f', (Sy('z'),)),
    ))
    correct = Pl(Nu(11), [
        SP(Nu(3), {Sy('x'): Nu(2)}),
        SP(Nu(1), {Co('f', (Sy('z'),)): Nu(1)})
    ])

    out = addtospp.body(plusin)

    assert out.num == correct.num
    assert out.items == correct.items


# ==============
# Test minustospp
#===============
@pytest.fixture
def minustospp(scope='module'):
    return MinusToSPP()


@pytest.mark.parametrize(
    "expr0, expr1, correct",
    [
        (Nu(4), Nu(3), Nu(1)),
        (
            Sy('x'), Nu(3),
            Pl(Nu(-3), [SP(Nu(1), {Sy('x'): Nu(1)})])
        ),
        (
            Nu(3), Sy('x'),
            Pl(Nu(3), [SP(Nu(-1), {Sy('x'): Nu(1)})])
        ),
        (
            Sy('x'), Sy('y'),
            Pl(Nu(0), [
                SP(Nu(1), {Sy('x'): Nu(1)}),
                SP(Nu(-1), {Sy('y'): Nu(1)}),
            ])
        ),
        (
            Sy('x'), Sy('x'),
            Nu(0)
        ),
        (
            Sy('x'), SP(Nu(-1), {Sy('x'): Nu(1)}),
            SP(Nu(2), {Sy('x'): Nu(1)})
        ),
        (
            SP(Nu(2), {Sy('x'): Nu(1)}), SP(Nu(-1), {Sy('x'): Nu(1)}),
            SP(Nu(3), {Sy('x'): Nu(1)})
        ),
        (
            Pl(Nu(3), [SP(Nu(2),{Sy('x'): Nu(2)}), SP(Nu(2),{Sy('y'): Nu(2)})]),
            SP(Nu(-1), {Pl(Nu(3), [SP(Nu(2),{Sy('x'): Nu(2)}), SP(Nu(2),{Sy('y'): Nu(2)})]): Nu(1)}),
            Pl(Nu(6), [SP(Nu(4),{Sy('x'): Nu(2)}), SP(Nu(4),{Sy('y'): Nu(2)})]),

        ),
    ],
)
def test_minustospp(settings, minustospp, expr0, expr1, correct):
    expr = Co('-', (expr0, expr1))

    out = minustospp.body(expr)

    if isPl(correct):
        assert out.num == correct.num
        assert out.items == correct.items
    else:
        assert out == correct


# =======================
# Test ConvertFromStarPwr
# =======================
def test_convertfromstarpwr_predicate(settings):
    sp = SP(Nu(3), {Sy('x'):Nu(2)})

    assert convertfromstarpwr.predicate(sp) == True


@pytest.mark.parametrize(
    "expr, correct",
    [
        (
            SP(Nu(3), {Sy('x'):Nu(2), Sy('y'): Nu(1)}),
            CA('*', (Nu(3), Co('**', (Sy('x'), Nu(2))), Sy('y')))
        ),
        (
            SP(Nu(1), {Sy('x'):Nu(2), Sy('y'): Nu(1)}),
            CA('*', (Co('**', (Sy('x'), Nu(2))), Sy('y')))
        ),
    ],
)
def test_convertfromstarpwr_body(settings, expr, correct):
    out = convertfromstarpwr.body(expr)

    assert out == correct





# ===========================
# These are integration tests 
# ===========================
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
