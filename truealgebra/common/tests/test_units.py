from truealgebra.core.settings import SettingsSingleton
from truealgebra.core.abbrv import Re, Co, Nu, Sy, CA
from truealgebra.core.err import TrueAlgebraError
from truealgebra.common.commonsettings import commonsettings as comset
from truealgebra.std.setup_func import std_setup_func
from truealgebra.common.setup_func import common_setup_func
from truealgebra.common.units import (
    simplifyunits, simplifyunitsbu, evalunitsub, evalunitneg, evalunitpwr,
    evalunitdiv, evalunitmul, evalunitplus, UnitDimension, ConvertDimension,
    ConvertUnity
)

import pytest
from IPython import embed


@pytest.fixture
def settings(scope='module'):
    settings = SettingsSingleton()
    settings.reset()
    comset.reset()
    std_setup_func()
    common_setup_func()
    yield settings
        
    settings.reset()
    comset.reset()


# ==================
# Test SimplifyUnits
# ==================
@pytest.mark.parametrize(
    "expr, correct",
    [
        (Re('`', (Nu(3.0), Sy('m'))), True),
        (Co('`', (Nu(3.0), Sy('m'))), False),
        (Re('``', (Nu(3.0), Sy('m'))), False),
        (Re('`', (Nu(3.0),)), False),
    ],
    ids=[
        'actual unit',
        'Co should be Re',
        'wrong name',
        'only one argument',
    ]
)
def test_simplifyunits_predicate(settings, expr, correct):
    output = simplifyunits.predicate(expr)
#   xxx = 100; embed()

    assert output == correct

@pytest.mark.parametrize(
    "expr, correct",
    [
#       (' 3.5 ` 2.0 ', ' 7.0 '),
        (' 2.0 ` star(3.0, m, N)', ' 6.0 ` m * N'),
#       (' 2.0 ` star(3.0, N)', ' 6.0 ` N'),
#       (' 2.0 ` 3.0 / s ', '6.0 ` 1 / s'),
#       (' 6.0 ` 1 / s ', '6.0 ` 1 / s'),
#       (' 2.0 ` star(3.0, N) / s ', '6.0 ` N / s'),
#       (' 2.0 ` star(3.0, N, m) / s ', '6.0 ` (N * m) / s'),
#       (' 3.5 ` ((m * m / s) / (1 / s)) ', '3.5 ` m ** 2'),
#       (' 1.5 ` star(m, 2.0, N, 3.0, 1 / s)', '9.0 ` (m * N) / s'),
    ],
#   ids=[
#       '2nd argument of a unit expression is a number',
#       '2nd arg is star with number',
#       '2nd arg is star with number and one unit',
#       '2nd arg is number divided by unit',
#       '2nd arg is one divided by unit',
#       '2nd arg is number and one unit in dividend',
#       '2nd arg is number and two units in dividend',
#       'simple case, unit number does not change',
#       'Major simplification',
#   ]
)
def test_simplifyunits_body(settings, expr, correct):
#   output = simplifyunits.body(settings.parse(expr))
    newexpr = settings.parse(expr)
    output = simplifyunits.body(newexpr)
    correct_expr  = settings.parse(correct)

    assert output == correct_expr


# ================
# Test EvalUnitSub
# ================
@pytest.mark.parametrize(
    "expr, correct",
    [
        (Co('-', (Nu(3.0), Sy('m'))), True),
        (Co('--', (Nu(3.0), Sy('m'))), False),
        (Co('-', (Nu(3.0),)), False),
    ],
)
def test_evalunitsub_predicate(settings, expr, correct):
    output = evalunitsub.predicate(expr)

    assert output == correct


@pytest.mark.parametrize(
    "expr, correct",
    [
        ('(7 ` m) - (2 ` m)', ' 5 ` m '),
        ('6 - (2 ` m)', ' 6 -  2 ` m '),
        ('(7 ` m) - 4', ' (7 ` m) - 4 '),
    ],
)
def test_evalunitsub_body(settings, expr, correct):
    output = evalunitsub.body(settings.parse(expr))
    correct_expr = settings.parse(correct)

    assert output == correct_expr


# ================
# Test EvalUnitNeg
# ================
@pytest.mark.parametrize(
    "expr, correct",
    [
        ('- (7 ` m) ', ' (-7) ` m '),
        (' - 7 ', ' - 7'),
        (' - x ', ' - x'),
        (' 2 ** m ', ' 2 ** m '),
    ],
)
def test_evalunitneg(settings, expr, correct):
    output = evalunitneg(settings.parse(expr))
    correct_expr = settings.parse(correct)

    assert output == correct_expr


# ================
# Test EvalUnitPwr
# ================
@pytest.mark.parametrize(
    "expr, correct",
    [
        (Co('**', (Sy('a'), Sy('b'))), True),
        (Co('*', (Sy('a'), Sy('b'))), False),
        (Co('**', (Sy('a'), Sy('b'), Sy('c'))), False),
    ],
)
def test_evalunitpwr_predicate(settings, expr, correct):
    output = evalunitpwr.predicate(expr)

    assert output == correct


@pytest.mark.parametrize(
    "expr, correct",
    [
        (' (5 ` m) ** 2 ', ' 25 ` m**2 '),
        (' m ** 2 ', ' m ** 2 '),
    ],
)
def test_evalunitpwr_body(settings, expr, correct):
    output = evalunitpwr.body(settings.parse(expr))
    correct_expr = settings.parse(correct)

    assert output == correct_expr


# ================
# Test EvalUnitDiv
# ================
@pytest.mark.parametrize(
    "expr, correct",
    [
        (Co('/', (Sy('a'), Sy('b'))), True),
        (Co('*', (Sy('a'), Sy('b'))), False),
        (Co('/', (Sy('a'), Sy('b'), Sy('c'))), False),
    ],
)
def test_evalunitdiv_predicate(settings, expr, correct):
    output = evalunitdiv.predicate(expr)

    assert output == correct


@pytest.mark.parametrize(
    "expr, correct",
    [
        (' (15 ` m**3) / (3 ` m) ', ' 5 ` m**2 '),
        (' (15 ` m**3) / 3  ', ' 5 ` m**3 '),
        (' 15  / (3 ` m) ', ' 5 ` (1 / m) '),
        (' x / y ', ' x / y '),
    ],
)
def test_evalunitdiv_body(settings, expr, correct):
    output = evalunitdiv.body(settings.parse(expr))
    correct_expr = settings.parse(correct)

    assert output == correct_expr


# ================
# Test EvalUnitMul
# ================
@pytest.mark.parametrize(
    "expr, correct",
    [
        (CA('*', (Sy('a'), Sy('b'))), True),
        (Co('*', (Sy('a'), Sy('b'))), False),
        (CA('/', (Sy('a'), Sy('b'), Sy('c'))), False),
    ],
)
def test_evalunitmul_predicate(settings, expr, correct):
    output = evalunitmul.predicate(expr)

    assert output == correct


def test_evalunitmul_body(settings):
    output = evalunitmul.body(settings.parse(' star(x, 5, 4, 2 ` m, 3 ` N) '))
    correct_expr = settings.parse('star(120 ` (m * N), x)')

    assert output == correct_expr


# =================
# Test EvalUnitPlus
# =================
@pytest.mark.parametrize(
    "expr, correct",
    [
        (CA('+', (Sy('a'), Sy('b'))), True),
        (Co('+', (Sy('a'), Sy('b'))), False),
        (CA('/', (Sy('a'), Sy('b'), Sy('c'))), False),
    ],
)
def test_evalunitplus(settings, expr, correct):
    output = evalunitplus.predicate(expr)

    assert output == correct


@pytest.fixture
def reset_units_dict(scope='function'):
#   evalunitplus2 = evalunitplus
    evalunitplus.units_dict = None
    yield evalunitplus
    evalunitplus.units_dict = None


@pytest.mark.parametrize(
    "start_dict, unitexpr, correct",
    [
        (
            {Sy('m') : Nu(2), Sy('s') : Nu(-1)},
            Re('`', (Nu(3), Sy('m'))),
            {Sy('m') : Nu(5), Sy('s') : Nu(-1)},
        ),
        (
            {Sy('m') : Nu(2), Sy('s') : Nu(-1)},
            Re('`', (Nu(3), Sy('N'))),
            {Sy('m') : Nu(2), Sy('s') : Nu(-1), Sy('N'): Nu(3)},
        ),
    ]
)
def test_add_unitexpr_to_dict(
        settings, reset_units_dict, start_dict, unitexpr, correct
    ):
    evalunitplus.units_dict = start_dict
    evalunitplus.add_unitexpr_to_dict(unitexpr)

    assert evalunitplus.units_dict == correct


def test_convert_dict_to_list(settings, reset_units_dict):
    evalunitplus.units_dict = {Sy('m'): Nu(2), Sy('N'): Nu(1)}
    correct = [Re('`', (Nu(2), Sy('m'))), Re('`', (Nu(1), Sy('N')))]

    ulist = evalunitplus.convert_dict_to_list()

    assert ulist == correct
    assert evalunitplus.units_dict is None


@pytest.mark.parametrize(
    "expr, correct",
    [
        (' plus(2 ` m, 3 ` m, 4 ` m) ', ' 9 ` m '),
        (' plus(2 ` m, 3 ` N, 4 ` m) ', ' plus(6 ` m, 3 `N)'),
        (' plus(2 ` m, x,   4 ` m, y) ', ' plus(6 ` m, x, y)'),
        (' plus(2 ` m, (-2) ` m) ', ' 0 ` m '),
        (' plus(3, x, y) ', ' plus(3, x, y) '),
    ]
)
def test_evalunitplus(settings, expr, correct):
    newcorrect = settings.parse(correct)

    newexpr = evalunitplus(settings.parse(expr))

    assert newexpr == newcorrect


# =====================
# Test ConvertDimension
# =====================
@pytest.fixture
def energy_dim(settings):
    energy_dim = UnitDimension()
    energy_dim.basis = 'J'
    energy_dim.convdict = {
        Sy('J'): Nu(1),
        Sy('kJ'): Nu(1000),
        Sy('mJ'): Nu(0.001),
        CA('*', (Sy('N'), Sy('m'))): Nu(1),

    }
    return energy_dim


@pytest.fixture
def convertdim_rule(settings, energy_dim):
    return ConvertDimension(target=Sy('J'), dimension=energy_dim)


def test_init_target_error(settings, energy_dim,):
    with pytest.raises(TrueAlgebraError) as ta_error:
        arule = ConvertDimension(dimension=energy_dim)

    assert str(ta_error.value) == (
        'ConvertDimension instantiation requres a target argument'
    )


def test_init_dimension_error(settings, energy_dim,):
    with pytest.raises(TrueAlgebraError) as ta_error:
        arule = ConvertDimension(target=Sy('J'))

    assert str(ta_error.value) == (
        'ConvertDimension instantiation requres a dimension argument'
    )


def test_convertdimension_init(settings, convertdim_rule):
    assert convertdim_rule.coef == comset.num1
    assert convertdim_rule.replace.parent == convertdim_rule
    assert isinstance(convertdim_rule.replace, ConvertDimension.Replace)


def test_replace_predicate(settings, convertdim_rule):
    assert convertdim_rule.replace.predicate(Sy('kJ')) == True
    assert convertdim_rule.replace.predicate(Sy('BTU')) == False


@pytest.mark.parametrize(
    "target, units, correct_str",
    [
        ('kJ', 'star(mJ, m)', '(.000001 * kJ) * m'),
        ('kJ', 'star(BTU, m)', 'star(BTU, m)'), 
        ('N * m', 'J * m', '(1 * (N * m)) * m'),
    ],
)
# Note: replace is bottomup=True. Makes it difficult to test replace.body
def test_replace(settings, energy_dim, target, units, correct_str):
    rule = ConvertDimension(
        target=settings.parse(target),
        dimension=energy_dim
    )
    correct = settings.parse(correct_str)

    out = rule.replace(settings.parse(units))

    assert out == correct


@pytest.mark.parametrize(
    "target, unitexpr, correct_str",
    [
        ('kJ', '3 ` star(mJ, m)', '.000003 ` kJ * m'),
        ('N * m', '3 ` (N * m)/ J', '3'),
    ],
)
def test_convertdimension_body(
    settings, energy_dim, target, unitexpr, correct_str
):
    rule = ConvertDimension(
        target=settings.parse(target),
        dimension=energy_dim
    )
    correct = settings.parse(correct_str)

    out = rule.body(settings.parse(unitexpr))

    assert out == correct


@pytest.mark.parametrize(
    "expr, correct",
    [
        (Re('`', (Sy('a'), Sy('b'))), True),
        (Re('*', (Sy('a'), Sy('b'))), False),
        (Re('`', (Sy('a'), Sy('b'), Sy('c'))), False),
    ],
)
def test_convertdimension_predicate(settings, convertdim_rule, expr, correct):
    output = convertdim_rule.predicate(expr)

    assert output == correct


# =================
# Test ConvertUnity
# =================
@pytest.fixture
def convunity_rule(settings):
    return ConvertUnity(unity=settings.parse(' (2.54 * cm) / in '))


def test_init_unity_error(settings, energy_dim,):
    with pytest.raises(TrueAlgebraError) as ta_error:
        arule = ConvertUnity()

    assert str(ta_error.value) == (
        'ConvertUnity instantiation requres a unity argument'
    )


def test_convertunity_init(settings, convunity_rule):
    assert convunity_rule.unity == Co('/', (
        CA('*', (Nu(2.54), Sy('cm'))),
        Sy('in')
    ))


@pytest.mark.parametrize(
    "expr, correct",
    [
        (Re('`', (Sy('a'), Sy('b'))), True),
        (Re('*', (Sy('a'), Sy('b'))), False),
        (Re('`', (Sy('a'), Sy('b'), Sy('c'))), False),
    ],
)
def test_convertunity_predicate(settings, convunity_rule, expr, correct):
    output = convunity_rule.predicate(expr)

    assert output == correct


def test_convertunity_body(settings, convunity_rule):
    expr = Re('`', (Nu(2), Co('**', (Sy('in'), Nu(2)))))
    correct = Re('`', (Nu(5.08), CA('*', (Sy('cm'), Sy('in')))))

    newexpr = convunity_rule.body(expr)

    assert newexpr == correct
