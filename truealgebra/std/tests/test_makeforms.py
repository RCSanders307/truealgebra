from truealgebra.core.abbrv import Sy, Co, Nu, CA
from truealgebra.core.expression import null
from truealgebra.core.rules import Rule, RulesBU
#from truealgebra.std.std_settings import parse

from truealgebra.std.stdsettings_function import set_stdsettings
from truealgebra.core.settings import settings

# The statement below generates an error from std.eval
# the import must be done inside of a fixture that has the proper environment
#   @pytest.fixture
#   def mf(stdsettings, scope='module'):
#       from truealgebra.std import makeforms
#       return makeforms

# then StarPwrModify can be accessed by mf.StarPwrModify
from truealgebra.std.makeforms import (
    SP, PSP, Pl, PPl, isSP, isPl, spfinalcheck, plfinalcheck,
    StarPwr, PseudoStarPwr, Plus, PseudoPlus, ConvertTo, ChainBase,
    StarPwrModify, StarPwrModifier, SPBasePwr, PlRecheckSP,
    PlusModify, PlusModifier, toform0
)

from types import MappingProxyType
from fractions import Fraction
from collections import defaultdict

import pytest
#from IPython import embed
#import ipdb

@pytest.fixture
def stdsettings(scope='module'):
    yield set_stdsettings()
    settings.reset()


@pytest.fixture
def makeforms(stdsettings, scope='module'):
    from truealgebra.std import makeforms
    return makeforms

# =============================
# Expression and Pseudo Classes
# =============================

# Test StarPwr
# ============
@pytest.fixture
def input_dict():
    return {Sy('x'): 2, Sy('y'): 6}


def test_starpwr_init(input_dict):
    starpwr = SP(coef=4, exp_dict=input_dict)
    repr_out = repr(starpwr)
    hash_out = hash(starpwr)

    assert starpwr.coef == 4
    assert starpwr.exp_dict == input_dict
    assert isinstance(starpwr.exp_dict, MappingProxyType)
    assert repr_out == 'SP(4, {x: 2, y: 6})'
    assert hash_out == hash((
        4,
        SP,
        frozenset(MappingProxyType(input_dict).items())
    ))


def test_starpwr_init_default():
    starpwr = SP()

    assert starpwr.coef == 1
    assert starpwr.exp_dict == dict()
    assert isinstance(starpwr.exp_dict, MappingProxyType)


def test_starpwr_copy():
    psp = PSP(5, {Sy('x'): 2, Sy('y'): 1})

    sp = SP.copy(psp)

    assert type(sp) == SP
    assert sp.coef == 5
    assert sp.exp_dict == {Sy('x'): 2, Sy('y'): 1}


@pytest.fixture
def tmprulebu():
    class TmpRuleBU(Rule):
        def predicate(self, expr):
            return isinstance(expr, Sy) or isSP(expr) or isPl(expr)

        def body(self, expr):
            if expr == Sy('w'):
                return Nu(2)
            elif expr == Sy('x'):
                return Nu(2)
            elif expr == Sy('y'):
                return Nu(3)
            elif isSP(expr):
                return SP(expr.coef + 1, expr.exp_dict)
            elif isPl(expr):
                return Pl(expr.num + 1, expr.items)
            else:
                return expr

        bottomup = True

    return TmpRuleBU()


def test_starpwr_bottomup(tmprulebu):
    sp = SP(3, {Sy('w'): 3, Sy('x'): 4, Sy('y'): 2, Sy('z'): 2, })

    out = tmprulebu(sp)

    assert out == SP(4, {Nu(2): 7, Nu(3): 2, Sy('z'): 2})


def test_starpwr_eq(input_dict):
    starpwr = SP(coef=4, exp_dict=input_dict)
    class SPSubClass(SP):
        pass

    spsubclass = SPSubClass(coef=4, exp_dict=input_dict)

    assert not (starpwr == spsubclass)
    assert not (starpwr == SP(coef=3, exp_dict=input_dict))
    assert not (starpwr == SP(coef=4, exp_dict={Sy('x'): 3, Sy('y'): 6}))
    assert starpwr == SP(coef=4, exp_dict={Sy('x'): 2, Sy('y'): 6})


# Test PseudoStarPwr
# ==================
def df():  # default function for defaultdict
    return 0


@pytest.mark.parametrize(
    'instance, coef, exp_dict',
    [
        (PseudoStarPwr(), 1, defaultdict(df)),
        (PseudoStarPwr(coef=7), 7, defaultdict(df)),
        (
            PseudoStarPwr(exp_dict={Sy('x'): 3}), 
            1,
            defaultdict(df, {Sy('x'): 3})
        ),
    ],
    ids=[
        'no arguments',
        'coef parameter only',
        'exp_dict parameter only',
    ]
)
def test_pseudostarpwr_init(instance, coef, exp_dict):
    assert instance.coef == coef
    assert instance.exp_dict == exp_dict
    assert type(instance.exp_dict) == defaultdict


def test_pseudostarpwr_copy():
    sp = SP(5, {Sy('x'): 2, Sy('y'): 1})

    psp = PSP.copy(sp)

    assert type(psp) == PSP
    assert psp.coef == 5
    assert psp.exp_dict == sp.exp_dict


def test_pseudostarpwr_copy():
    psp = PSP(5, {Sy('x'): 2, Sy('y'): 1})

    assert repr(psp) == 'PSP(5, {x: 2, y: 1})'


def test_pseudostarpwr_hash(input_dict):
    psp = PSP(coef=4, exp_dict=input_dict)
    hash_out = hash(psp)

    assert hash_out == hash((
        4,
        PSP,
        frozenset(input_dict.items())
    ))


def test_pseudostarpwr_eq(input_dict):
    psp = PSP(coef=4, exp_dict=input_dict)
    class PSPSubClass(PSP):
        pass

    pspsubclass =PSPSubClass(coef=4, exp_dict=input_dict)

    assert not (psp == pspsubclass)
    assert not (psp == PSP(coef=3, exp_dict=input_dict))
    assert not (psp == PSP(coef=4, exp_dict={Sy('x'): 3, Sy('y'): 6}))
    assert psp == PSP(coef=4, exp_dict={Sy('x'): 2, Sy('y'): 6})


def test_pseudostarpwr_merge():
    sp = SP(5, {Sy('x'): 2, Sy('y'): 1})
    psp = PSP(4, {Sy('y'): 3})

    psp.merge(sp)

    psp.coef = 20
    psp.exp_dict == {Sy('x'): 2, Sy('y'): 4}


@pytest.mark.parametrize(
    'base, exp, correct',
    [
        (Sy('x'), 1, {Sy('x'): 3}),
        (Sy('y'), 3, {Sy('x'): 2, Sy('y'): 3}),
    ],
    ids=[
        'same base',
        'different base'
    ],
)
def test_pseudostarpwr_append(base, exp, correct):
    psp = PseudoStarPwr(3,{Sy('x'): 2})

    psp.append(base, exp)

    assert psp.exp_dict == correct
    assert psp.coef == 3


def test_pseudostarpwr_mul_by_num():
    psp = PSP(3, {Sy('x'): 2})
    num = Fraction(5, 3)

    psp.mul_by_num(num)

    assert psp == PSP(5, {Sy('x'): 2})


def test_pseudostarpwr_apply_exponent():
    psp = PSP(3, {Sy('x'): 2, Sy('y'): 3})

    psp.apply_exponent(3)

    assert psp.coef == 27
    assert psp.exp_dict == {Sy('x'): 6, Sy('y'): 9}


# Test Plus
# =========
def test_plus_init():
    plus = Pl(4, [Sy('x'), Sy('y')])
    repr_out = repr(plus)
    hash_out = hash(plus)

    assert plus.num == 4
    assert plus.items == (Sy('x'), Sy('y'))
    assert repr_out == 'Plus(4, (x, y))'
    assert hash_out == hash((
        Pl,
        '_+',
        4,
        tuple(sorted((hash(Sy('x')), hash(Sy('y')))))
    ))


def test_plus_init_default():
    plus = Pl()

    assert plus.num == 0
    assert plus.items == tuple()


def test_plus_copy():
    pplus = PPl(7, (Sy('x'), Sy('y')))
    
    plus = Pl.copy(pplus)

    assert type(plus) == Pl
    assert plus.num == 7
    assert plus.items == (Sy('x'), Sy('y'))


def test_plus_bottomup(tmprulebu):
    plus = Pl(3, (Sy('w'), Sy('x'), Sy('y'), Sy('z')))

    out = tmprulebu(plus)

    assert out == Pl(4, (Nu(2), Nu(2), Nu(3), Sy('z')))


def test_plus_eq():
    input_list = [Sy('x'), Sy('y')]
    plus = Pl(4, input_list)
    class PlSubClass(Pl):
        pass

    plsubclass = PlSubClass(4, input_list)

    assert not (plus == plsubclass)
    assert not (plus == Pl(3, input_list))
    assert not (plus == Pl(3, [Sy('w'), Sy('y')]))
    assert plus == Pl(4, (Sy('x'), Sy('y')))


# Test PseudoPlus
# ===============
@pytest.mark.parametrize(
    'instance, num, items',
    [
        (PseudoPlus(), 0, list()),
        (PseudoPlus(num=7), 7, list()),
        (
            PseudoPlus(items=[Sy('x')]), 
            0,
            [Sy('x')], 
        ),
    ],
    ids=[
        'no arguments',
        'num parameter only',
        'items parameter only',
    ]
)
def test_pseudoplus_init(instance, num, items):
    assert instance.num == num
    assert instance.items == items


def test_pseudoplus_copy():
    plus = Pl(5,[Sy('x'), Sy('y')])

    pplus = PPl.copy(plus)

    assert type(pplus) == PPl
    assert pplus.num == 5
    assert pplus.items == list(plus.items)


@pytest.mark.parametrize(
    'term, modified_items',
    [
        (
            StarPwr(coef=3, exp_dict={Sy('x'): 2, Sy('y'): 1}),
            [
                StarPwr(coef=5, exp_dict={Sy('x'): 2, Sy('y'): 1}),
                StarPwr(coef=3, exp_dict={Sy('x'): 1, Sy('y'): 1}),
            ],
        ),
        (
            StarPwr(coef=7, exp_dict={Sy('x'): 2}),
            [
                StarPwr(coef=2, exp_dict={Sy('x'): 2, Sy('y'): 1}),
                StarPwr(coef=3, exp_dict={Sy('x'): 1, Sy('y'): 1}),
                StarPwr(coef=7, exp_dict={Sy('x'): 2}),
            ],
        ),
    ],
    ids=[
        'found common term',
        'no common term',
    ]
)
def test_pseudoplus_common_term(term, modified_items):
    pplus = PseudoPlus(items=[
        StarPwr(coef=2, exp_dict={Sy('x'): 2, Sy('y'): 1}),
        StarPwr(coef=3, exp_dict={Sy('x'): 1, Sy('y'): 1}),
    ])

    pplus.find_common_term(term)

    assert pplus.items == modified_items


def test_pseudoplus_remove_sp_zeros():
    ppl = PPl(3, [
        SP(1, {Sy('x'): 2}), 
        SP(0, {Sy('y'): 2}), 
        Co('f',())
    ])

    ppl.remove_sp_zeros()

    assert ppl.num == 3
    assert ppl.items == [SP(1, {Sy('x'): 2}), Co('f',())]


def test_pseudoplus_merge():
    pplus = PPl(4, [Sy('x')])
    plus = Pl(5, (Sy('y'),))

    pplus.merge(plus)

    assert pplus.num == 9
    assert pplus.items == [Sy('x'), Sy('y')]


def test_pseudoplus_combine_nums():
    pplus = PPl(4, [Sy('x'), Nu(3), Nu(4), Sy('y')])

    pplus.combine_nums()

    assert pplus.num == 11
    assert pplus.items == [Sy('x'), Sy('y')]

# ======
# Step 1
# ======

# ConvertTo
# =========
# NOTE:
# The ConvertTo body method is tested in the functional/integration tests.
@pytest.fixture
def convertto():
    return ConvertTo()


@pytest.mark.parametrize(
    'expr, correct',
    [
        (Co('/', (Sy('x'), Sy('y'))), True),
        (CA('*', (Sy('x'), Sy('y'))), True),
        (CA('+', (Sy('x'), Sy('y'))), True),
        (Co('-', (Sy('x'), Sy('y'))), True),
        (Co('**', (Sy('x'), Sy('y'))), True),
        (Co('f', (Sy('x'), Sy('y'))), False),
        (Sy('**'), False)
    ],
    ids=[
        '/ container',
        '* container',
        '+ container',
        '- container',
        '** container',
        'f container',
        'funky symbol',
    ]
)
def test_convertto_predicate(expr, correct, convertto):
    out = convertto.predicate(expr)


def test_convertto_star(convertto):
    expr = CA('*', (
        Co('f', ()),
        StarPwr(coef=2, exp_dict={Co('f', ()): 2}),
        Co('g', ()),
        Co('f', ()),
    ))

    out = convertto.star(expr)
    correct = StarPwr(coef=2,exp_dict={Co('f', ()): 4, Co('g', ()): 1})


    assert out == correct

@pytest.mark.parametrize(
    'expr, correct',
    [
        (
            Co('/', (Sy('y'), Sy('x'))), 
            StarPwr(exp_dict={Sy('y'): 1, Sy('x'): -1})
        ),
        (
            Co('/', (StarPwr(coef=3, exp_dict={Sy('y'): 2}), Sy('y'))),
            StarPwr(coef=3, exp_dict={Sy('y'): 1})
        ),
        (
            Co('/', (Sy('y'), StarPwr(coef=2, exp_dict={Sy('y'): 2}))),
            StarPwr(coef=0.5, exp_dict={Sy('y'): -1})
        ),
        (
            Co('/', (
                StarPwr(coef=4, exp_dict={Sy('y'): 2}),
                StarPwr(coef=2, exp_dict={Sy('y'): 2})
            )),
            StarPwr(coef=2, exp_dict={Sy('y'): 0})
        ),
    ],
    ids=[
        'non starpwr arguments',
        'upstairs strpwr argument',
        'downstairs strpwr argument',
        'both starpwr arguments',
    ]
)
def test_convertto_div(expr, correct, convertto):
    out = convertto.div(expr)

    assert out == correct

@pytest.mark.parametrize(
    'expr, correct',
    [
        (
            Co('-', (StarPwr(2, {Sy('x'): 3}),)),
            StarPwr(-2, {Sy('x'): 3}),
        ),
        (
            Co('-', (Sy('x'),)),
            StarPwr(-1, {Sy('x'): 1}),
        ),
    ],
    ids=[
        'StarPwr instance',
        'no StarPwr instance',
    ]
)
def test_convertto_neg(expr, correct, convertto):
    out = convertto.neg(expr)

    assert out == correct


@pytest.mark.parametrize(
    'expr, correct',
    [
        (
            Co('**', (StarPwr(3, {Sy('x'): 3}), Nu(2))),
            StarPwr(9, {Sy('x'): 6}),
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
def test_convertto_power(expr, correct, convertto):
    out = convertto.power(expr)

    assert out == correct


def test_convertto_plus(convertto):
    expr = CA('+', (
        Sy('x'),
        Nu(3),
        StarPwr(3, {Sy('x'): 2}),
        Plus(5, (
            StarPwr(1, {Sy('z'): 2}),
            StarPwr(2, {Sy('z'): 1}),
        ))
    ))
    out = convertto.plus(expr)

    assert out == Plus(8, (
        Sy('x'),
        StarPwr(3, {Sy('x'): 2}),
        StarPwr(1, {Sy('z'): 2}),
        StarPwr(2, {Sy('z'): 1}),
    ))

def test_convertto_minus_neg(convertto):
    expr = Co(-1, (Sy('x'),))

    out = convertto.minus(expr)

    assert out == StarPwr(-1, {Sy('x'): 1})


# calling the neg method is tested in the functioanl tests.
@pytest.mark.parametrize(
    'first, second, correct',
    [
        (
            Plus(0, (StarPwr(1, {Sy('x'): 2}), StarPwr(2, {Sy('y'): 2}))),
            Nu(2),
            Plus(-2, (
                StarPwr(1, {Sy('x'): 2}),
                StarPwr(2, {Sy('y'): 2}),
            )),
        ),
        (
            Sy('x'),
            Sy('y'),
            Plus(0, [Sy('x'), StarPwr(-1, {Sy('y'): 1})])
        ),
    ],
    ids=[
        'with number',
        'without number',
    ]
)
def test_convertto_minus(first, second, correct, convertto):
    expr = Co('-', (first, second))

    out = convertto.minus(expr)

    assert out == correct

# ======
# Step 2
# ======

# ChainBase
# =========
def test_chainbase():
    def make_modifier(fromnum, tonum):
        def modifier(nxt):
            def inner(expr):
                if expr == fromnum:
                    out = tonum
                else:
                    out = expr
                return nxt(out)
            return inner
        return modifier

    mod0 = make_modifier(0, 1)  # change 0 to 1 
    mod1 = make_modifier(1, 2)  # change 1 to 2 
    mod2 = make_modifier(2, 3)  # change 2 to 3 

    mod = ChainBase(mod0, mod1, mod2)

    assert mod.chain(0) == 3
    assert mod.chain(1) == 3
    assert mod.chain(2) == 3
    assert mod.chain(7) == 7


# StarPwrModify Tests
# ===================
@pytest.fixture(scope='module')
def empty_spm():
    return  StarPwrModify()


def test_starpwrmodify_exit_link(empty_spm):
    psp = PseudoStarPwr(17, {Sy('x'): 2})

    out = empty_spm.exit_link(psp)

    assert out.coef == 17
    assert out.exp_dict == {Sy('x'): 2}
    assert type(out) == StarPwr


@pytest.mark.parametrize(
    'expr, correct',
    [
        (StarPwr(), True),
        (Sy('x'), False),
        (PSP(), True),
    ],
    ids=[
        'StarPwr instance',
        'not StarPwr instance',
        'PseudoStarPwr instance'
    ]
)
def test_starpwrmodify_predicate(expr, correct, empty_spm):
    out = empty_spm.predicate(expr)

    assert out is correct


def test_starpwrmodify_body(empty_spm):
    out = empty_spm.body(StarPwr())

    assert out.coef == 1
    assert out.exp_dict == dict()
    assert type(out) == StarPwr

    
# StarPwrModifier Tests
# =====================
@pytest.fixture
def sp_modifier():
    def echo(expr):
        return StarPwr.copy(expr)

    class TempModifier(StarPwrModifier): 
        def body(self, psp):
            if psp.exp_dict == dict():
                return Nu(psp.coef)
            else:
                return psp

    return TempModifier(echo)


@pytest.mark.parametrize(
    'input, correct, outtype',
    [
        (PseudoStarPwr(coef=5), Nu(5), Nu),
        (PseudoStarPwr(5, {Sy('x'): 3}), StarPwr(5, {Sy('x'): 3}), StarPwr),
    ],
    ids=[
        'number',
        'no number',
    ]
)
def test_starpwrmodifier(sp_modifier, input, correct, outtype):
    out = sp_modifier(input)

    assert out == correct
    assert type(out) == outtype


# SPFinalCheck Tests
# ==================
@pytest.mark.parametrize(
    'input, correct',
    [
        (
            PSP(3, {
                Nu(2): 3, 
                SP(1, {Sy('x'): 2, Sy('y'): 3}): 2, 
                Co('sin', (Sy('x'),)): 2
            }),
            SP(24, {
                Sy('x'): 4,
                Sy('y'): 6,
                Co('sin', (Sy('x'),)): 2
            })
        ),
        (PSP(3, {Nu(2): 3,}), Nu(24)),
        (
            PSP(3, {
                Nu(0): 3, 
                SP(1, {Sy('x'): 2, Sy('y'): 3}): 2, 
                Co('sin', (Sy('x'),)): 2
            }),
            Nu(0),
        ),
        (PSP(1, {Sy('x'): 1}), Sy('x')),
    ],
    ids=[
        'PseudoStarPwr out',
        'Number out',
        'Zero out',
        'single key',
    ]
)
def test_spfinalcheck(input, correct):
    out = spfinalcheck(input)

    assert out == correct

# test spbasepwr
def test_spbasepwr():
    spbasepwr = StarPwrModify(SPBasePwr)
    input = StarPwr(3, {
        Co('**', (Sy('x'), Nu(3))): 1,
        Sy('x'): 2,
        Co('**', (Sy('y'), Nu(2))): 3,
        Co('**', (Sy('y'), Sy('z'))): 2,
    })

    output = spbasepwr(input)

    assert output == StarPwr(3, {
        Sy('x'): 5,
        Sy('y'): 6,
        Co('**', (Sy('y'), Sy('z'))): 2,
    })


# test plusmodify
# ===============
## PlusModify Tests
@pytest.fixture(scope='module')
def empty_pm():
    return PlusModify()


def test_plusmodify_exit_link(empty_pm):
    pplus = PseudoPlus(items=[StarPwr(coef=5), StarPwr(3, {Sy('x'): 2})])

    out = empty_pm.exit_link(pplus)

    assert out.items == (StarPwr(coef=5), StarPwr(3, {Sy('x'): 2}))
    assert out.num == 0
    assert type(out) is Pl
    assert out.name == '_+'


@pytest.mark.parametrize(
    'expr, correct',
    [
        (Plus(5, [Sy('x')]), True),
        (PseudoPlus(5, [Sy('x')]), True),
        (Sy('y'), False),
    ],
    ids=[
        'Plus instance',
        'PsudoPlus instance',
        'Symbol instance',
    ]
)
def test_plusmodify_predicate(expr, correct, empty_pm):
    out = empty_pm.predicate(expr)

    assert out is correct


def test_plusmodify_body(empty_pm):
    out = empty_pm.body(Plus())

    assert out.items == ()
    assert out.num == 0
    assert type(out) == Plus
    assert out.name == '_+'


# PlusModifier Tests
# =================
@pytest.fixture
def plusmodifier():
    def echo(expr):
        return Plus.copy(expr)

    class TempModifier(PlusModifier): 
        def body(self, pplus):
            if pplus.items == list():
                return Nu(pplus.num)
            else:
                return pplus

    return TempModifier(echo)


@pytest.mark.parametrize(
    'input, correct',
    [
        (
            PseudoPlus(5), 
            Nu(5),
        ),
        (
            PseudoPlus(6, [Sy('x')]), 
            Plus(6, [Sy('x')]), 
        ),
    ],
    ids=[
        'Number output',
        'PseudoPlus output',
    ]
)
def test_plusmodifier(plusmodifier, input, correct):
    out = plusmodifier(input)

    assert out == correct


# test plfinalcheck
# =================
@pytest.mark.parametrize(
    'input, correct',
    [
        (
            Pl(6, [Nu(3), Pl(2, [Sy('x')]), Sy('y')]),
            Pl(11, [Sy('x'), Sy('y')])
        ),
        (
            Pl(0, [Sy('x')]),
            Sy('x'),
        ),
        (Pl(7, []), Nu(7)),
    ],
    ids=[
        'PseudoPlus out',
        'single item out',
        'no items',
    ],
)
def test_plfinalcheck(input, correct):
    out = plfinalcheck(input)

    assert out == correct


# test PlRecheckSP 
# =================
def test_plrechecksp():
    plrechecksp = PlusModify(PlRecheckSP)
    input = Plus(4, [
        StarPwr(1, {Sy('x'): 1}),
        StarPwr(4, dict()),
        StarPwr(3, {Sy('y'): 2}),
        StarPwr(2, {Sy('z'): 0}),
    ])

    output = plrechecksp(input)

    assert output == Plus(4, [
        Sy('x'),
        Nu(4),
        StarPwr(3, {Sy('y'): 2}),
        Nu(2),
    ])


#
# test CombinePlusTerms(
# =================
#
#
#


# Functional and Integrtion Tests
# ===============================
    

@ pytest.mark.parametrize(
    'input_str, correct_str',
    [
        (' star(a, a, a**2) ', ' a** 4 '),
        (' x * x * x * x * x**2 ', ' x ** 6 '),
        (' 3 * 4 * 5 ', ' 60 '),
        (' 3 * 4 * x * 5 ', ' 60 * x '),
        (' x * x * x * x / x**6 ', ' 1 / x ** 2 '),
        (' y * x * y * 5 * x ** -6 ', ' (5 * y ** 2) / x ** 5 '),
        (
            ' y * x + x * y + 5 + x ** -6 ', 
            ' plus( 5, star(2, x, y), 1 / x**6) '
        ),
        (' x ** 2 + x ** (x + 2 -x) ', ' 2 * x ** 2 '),
        ('  4 + 2 ** (x +2 -x) ', ' 8 '),
        (' sin(x) - sin(x + x - x) ', ' 0 ' ),
    ]
)
def test_functional(input_str, correct_str, stdsettings):
    input = settings.active_parse(input_str)
    correct = settings.active_parse(correct_str)

    out = toform0(input)

    assert out == correct

