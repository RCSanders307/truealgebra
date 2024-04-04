from truealgebra.core.abbrv import *   # import abbreviations
from truealgebra.core.expression import null
from truealgebra.core.rule import RulesBU
from truealgebra.std.unit import (
    UnitForm, SimplifyUnits, ConvertToBasis, MultiplyUnitsByBasis, 
    AffineConvert
)
from truealgebra.core.settings import Settings
from truealgebra.core.parse import Parse
import pytest
from IPython import embed

settings = Settings()

settings.set_custom_bp('=', 50, 50)
settings.set_custom_bp(':=', 10, 10)
settings.set_custom_bp('*', 1000, 1000)
settings.set_custom_bp('**', 1200, 1200)
settings.set_custom_bp('@', 0, 3000)
settings.set_custom_bp('|', 10, 10)
settings.set_custom_bp('`', 1500, 10)
settings.set_infixprefix('-', 200)


settings.set_container_subclass('*', CA)
settings.set_complement('star', '*')

settings.set_container_subclass(':=', Asn)
settings.set_container_subclass('`', Re)

settings.set_categories('suchthat', '|')
settings.set_categories('suchthat', 'suchthat')
settings.set_categories('forall', '@')

settings.set_categories('forall', 'forall')

parse = Parse(settings)


# =============
# Test UnitForm
# =============
def test_UnitForm_plain():
    """The dafault instance which is very simple"""
    unitform = UnitForm()

    assert unitform.coeff == 1
    assert unitform.units == dict()


def test_UnitForm_fancy():
    """Create a complicated specific instance"""
    unitform = UnitForm(coeff=3, units={Sy('m'): 2})

    assert unitform.coeff == 3
    assert unitform.units == {Sy('m'): 2}


# =================
# Test SimplifyUnits
# =================
simplifyunits = SimplifyUnits('`')


# Test SimplifyUnits predicate
# ===========================
@pytest.mark.parametrize(
    'expr, correct',
    [
        (Re('`', (Nu(3), Sy('m'))), True),
        (Re('*', (Nu(3), Sy('m'))), False),
        (Co('`', (Nu(3), Sy('m'))), False),
    ],
    ids=[
        'correct name and class',
        'wrong name and correct class',
        'correct name and wrong class',
    ],
)
def test_UnitSimiplify_predicate(expr, correct):
    out = simplifyunits.predicate(expr)

    assert out == correct


# Test SimplifyUnits eval Methods
# ==============================
class SetMakeEvalOut(SimplifyUnits):
    """ Homemade mockup of make_eval method which outputs an iterator.
    """
    def postinit(self, *args, **kwargs):
        self.name = args[0]
        self.make_eval_out = iter(kwargs['make_eval_out'])

    def make_eval(self, expr):
        return next(self.make_eval_out)


def test_SimplifyUnits_eval_num():
    """ Test eval_num method."""
    out = simplifyunits.eval_num(Nu(6))

    assert out.coeff == 6
    assert out.units == dict()


@pytest.mark.parametrize(
    'expr, coeff, units',
    [
        (Sy('m'), 1, {Sy('m'): 1}),
        (Co('sin', (Sy('x'),)), 1, {Co('sin', (Sy('x'),)): 1}),
    ],
    ids=[
        'standard case of a Symbpl instance representing a unit',
        'garbage case of a non-symbol expression',
    ]
)
def test_SimplifyUnits_eval_sym(expr, coeff, units):
    """ Test eval_sym method."""
    out = simplifyunits.eval_sym(expr)

    assert out.coeff == coeff
    assert out.units == units


@pytest.mark.parametrize(
    'expr, make_eval_out, coeff, units',
    [
        (Co('**', (Nu(2), Nu(3))), (), 8, dict()),
        (
            Co('**', (Sy('m'),Nu(2))),
            (UnitForm(coeff=3, units={Sy('m'): 3, Sy('J'): 1}),),
            9,
            {Sy('m'): 6, Sy('J'): 2},
        ),
        (
            Co('**', (Sy('m'),Sy('J'))),
            (),
            1,
            {Co('**', (Sy('m'),Sy('J'))): 1},
        ),
    ],
    ids=[
        'base and exponent are numbers',
        'exponent is a number',
        'exponent is not a number',
    ],
)
def test_SimplifyUnits_eval_power(expr, make_eval_out, coeff, units):
    """ Test eval_power method."""
    local_simplifyunits = SetMakeEvalOut('`', make_eval_out=make_eval_out)
    
    out = local_simplifyunits.eval_power(expr)

    assert out.coeff == coeff
    assert out.units == units


def test_SimplifyUnits_eval_div():
    """ Test eval_div method. """
    make_eval_out = (
        UnitForm(coeff=4, units={
            Sy('m'): 3,
            Sy('J'): 2,
            Sy('s'): 1,
        }),
        UnitForm(coeff=2, units={
            Sy('J'): 1,
            Sy('s'): 1,
            Sy('K'): -1,
        })
    )
    local_simplifyunits = SetMakeEvalOut('`', make_eval_out=make_eval_out)

    # parameter expr does not matter much here.
    out = local_simplifyunits.eval_div(Co('/', (Sy('m'), Sy('s'))))

    assert out.coeff == 2
    assert out.units == {
        Sy('m'): 3,
        Sy('J'): 1,
        Sy('s'): 0,
        Sy('K'): 1,
    }


def test_SimplifyUnits_eval_mul():
    """ Test eval_mul method. """
    make_eval_out = (
        UnitForm(coeff=4, units={
            Sy('m'): 3,
            Sy('J'): 2,
            Sy('s'): 1,
        }),
        UnitForm(coeff=2, units={
            Sy('J'): -1,
            Sy('s'): 1,
            Sy('K'): -1,
        })
    )
    local_simplifyunits = SetMakeEvalOut('`', make_eval_out=make_eval_out)

    # parameter expr does not as matter much here.
    out = local_simplifyunits.eval_mul(Co('*', (Sy('m'), Sy('s'))))

    assert out.coeff == 8
    assert out.units == {
        Sy('m'): 3,
        Sy('J'): 1,
        Sy('s'): 2,
        Sy('K'): -1,
    }


@pytest.mark.parametrize(
    'expr, coeff, units',
    [
        (Sy('m'), 1, {Sy('m'): 1}),
        (Nu(3), 3, dict()),
        (Co('**', (Sy('s'),Nu(2))), 1, {Sy('s'): 2}),
        (Co('/', (Sy('s'),Nu(2))), 0.5, {Sy('s'): 1}),
        (CA('*', (Sy('s'),Nu(2))), 2, {Sy('s'): 1}),
    ],
    ids=[
        'Symbol instance expression',
        'Number instance expression',
        'power expression',
        'division expression',
        'multiplication expression',
    ]
)
def test_SimplifyUnits_make_eval(expr, coeff, units):
    """Test the make_eval method.

    This is an itegration test as well.
    All of the other eval methods are called.
    """
    out = simplifyunits.make_eval(expr)

    assert out.coeff == coeff
    assert out.units == units


# Test SimplifyUnits cleanup method
# =================================
def test_SimplifyUnits_cleanup():
    """cleanup method converts unitform to lists."""
    unitform = UnitForm(coeff=1, units={
        Sy('m'): 1, 
        Sy('s'): 3,
        Sy('J'): -1,
        Sy('N'): -2,
        Sy('K'): 0,
    })

    up, down = simplifyunits.cleanup(unitform)

    assert up == [Sy('m'), Co('**', (Sy('s'), Nu(3)))]
    assert down == [Sy('J'), Co('**', (Sy('N'), Nu(2)))]


def test_SimplifyUnits_cleanup_error(capsys):
    """ Error occurs when complex numbers are unit exponents"""
    msg = 'Units cannot have complex numbers as exponent'
    unitform = UnitForm(coeff=1, units={
        Sy('m'): complex(0, 1), 
    })

    up, down = simplifyunits.cleanup(unitform)
    err = capsys.readouterr()

    assert msg in err.out
    assert up == [null]
    assert down == list()


# Test SimplifyUnits make_units method
# ====================================
@pytest.mark.parametrize(
    'upstairs, downstairs, correct',
    [
        (list(), list(), Nu(1)),
        (list(), [Sy('m')], Co('/', (Nu(1), Sy('m')))),
        ([Sy('s')], [Sy('m')], Co('/', (Sy('s'), Sy('m')))),
        (
            [Sy('N'), Sy('m')], 
            [Sy('J'), Sy('s')],
            Co('/', (
                CA('*', (Sy('N'), Sy('m'))),
                CA('*', (Sy('J'), Sy('s'))),
            )),
        ),
        ([Sy('m')], list(), Sy('m')),
    ],
    ids=[
        'empty upstairs and downstairs',
        'empty upstairs and one item downstairs',
       ' one item upstairs and one item downstairs',
       ' multiple items upstairs and downstairs',
       ' one item upstairs and empty downstairs',
    ]
)
def test_SimplifyUnits_make_units(upstairs, downstairs, correct):
    units = simplifyunits.make_units(upstairs, downstairs)

    assert units == correct


# Test SimplifyUnits body method
# ==============================
@pytest.mark.parametrize(
    'expr, correct',
    [
        (
            Re('`', (Nu(3.0), CA('*', (Nu(2.0), Sy('m'))))),
            Re('`', (Nu(6.0), Sy('m'))),
        ),
        (
            Re('`', (Nu(3.0), Co('/', (
                CA('*', (Nu(2), Sy('m'))),
                Sy('m')
            )))),
            Nu(6)
        ),

    ],
    ids=[
        'simpliy units',
        'units cancel out'
    ]
)
def test_SimplifyUnits_body(expr, correct):
    """body method working correctly."""
    out = simplifyunits.body(expr)

    out == correct

@pytest.mark.parametrize(
    'expr, msg',
    [
        (Re('`', (Sy('m'),)), 'Unit expression must have two items'),
        (
            Re('`', (Sy('m'), Sy('m'))),
            'First item unit expression must be a number.'
        ),
    ],
    ids=[
        'unit expression must have two items',
        'First items in expression is not a number',
    ]
)
def test_SimplifyUnits_body_error(capsys, expr, msg):
    """expr argument has too few items."""
    out = simplifyunits.body(expr)

    err = capsys.readouterr()

    assert msg in err.out
    assert out == null


# ==============
# Test ConvertTo
# ==============
class ConvertLengthTo(ConvertToBasis):
    unit_dict = {
        'm': 1.0,
        'cm': 0.01,
        'km': 1000,
        'mm': 0.001,
    }


class ConvertTimeTo(ConvertToBasis):
    unit_dict = {
        's': 1.0,
        'min': 60,
        'hr': 3600,
    }


tocm = ConvertLengthTo('cm')
tosec = ConvertTimeTo('s')


def test_ConvertTo_innerrule():
    """General requirements for innerrule."""
    assert tocm.innerrule.bottomup == True
    assert tocm.innerrule.tonum == Nu(0.01)
    assert tocm.innerrule.tounit == Sy('cm')


@pytest.mark.parametrize(
    'expr, correct',
    [
        (Sy('m'), True),
        (Sy('J'), False),
    ],
    ids=[
        'Symbol name in unit_dict',
        'Symbol name not in unit_dict'
    ]
)
def test_ConvertTo_innerrule_predicate(expr, correct):
    """Test the innerrule predicate method."""
    out = tocm.innerrule.predicate(expr)
    
    assert out == correct


def test_ConvertTo_innerrule_body():
    """Test the innerrule body method."""
    expr = Sy('m')
    out = tocm.innerrule.body(expr)

    assert out == Co('/', (
        CA('*', (Sy('cm'), Nu(1.0))),
        Nu(0.01)
    ))


def test_ConvertTo_init():
    """Test the ConvertTo __init__method"""
    assert isinstance(tosec.innerrule, tosec.InnerRule)


@pytest.mark.parametrize(
    'expr, correct',
    [
        (Re('`', (3.0, Sy('m'))), True),
        (Re('**', (3.0, Sy('m'))), False),
        (Co('`', (3.0, Sy('m'))), False),
    ],
    ids=[
        'Correct example',
        'wrong name',
        'wrong class'
    ]
)
def test_ConvertTo_predicate(expr, correct):
    """Test ConvertTo predicate"""
    out = tocm.predicate(expr)

    out == correct


@pytest.mark.parametrize(
    'expr, correct, msg',
    [
        (
            Re('`', (3.0, Sy('m'))), 
            Re('`', (3.0, Co('/', (
                CA('*', (Sy('cm'), Nu(1))), 
                Nu(0.01)
            )))),
            ''
        ),
        (Re('`', (3.0, Sy('N'))), Re('`', (3.0, Sy('N'))), ''),
        (Co('`', (Sy('m'),)), null, 'units expression requires two items'),
    ],
    ids=[
        'expression gets modified',
        'expression does not get modified',
        'two few items in expression',
    ]
)
def test_ConvertTo_body(capsys, expr, correct, msg):
    """Test ConvertTo body method"""
    out = tocm.body(expr)

    out == correct
    err = capsys.readouterr()

    assert msg in err.out
    assert out == correct


# ====================
# Test MultiplyUnitsBy
# ====================
class MultiplyUnitsBy(MultiplyUnitsByBasis):
    parse = parse

Nm_to_J = MultiplyUnitsBy(' J / N  * m')

def test_MultiplyUnitsBy_postinit():
    """Test postinit method"""
    assert Nm_to_J.factor == Co('/', (Sy('J'), CA('*', (Sy('N'), Sy('m')))))


@pytest.mark.parametrize(
    'expr, correct',
    [
        (Re('`', (3.0, Sy('m'))), True),
        (Re('**', (3.0, Sy('m'))), False),
        (Co('`', (3.0, Sy('m'))), False),
    ],
    ids=[
        'Correct example',
        'wrong name',
        'wrong class'
    ]
)
def test_MultiplyUnitsBy_predicate(expr, correct):
    """Test ConvertTo predicate"""
    out = Nm_to_J.predicate(expr)

    out == correct


@pytest.mark.parametrize(
    'expr, correct, msg',
    [
        (
            Re('`', (3.0, Sy('m'))), 
            Re('`', (3.0, CA('*', (
                Co('/', (Sy('J'), CA('*', (Sy('N'), Sy('m'))))),
                Sy('m')
            )))),
            ''
        ),
        (Co('`', (Sy('m'),)), null, 'units expression requires two items'),
    ],
    ids=[
        'expression gets modified',
        'two few items in expression',
    ]
)
def test_MultiplyUnitsBy_body(capsys, expr, correct, msg):
    """Test ConvertTo body method"""
    out = Nm_to_J.body(expr)

    out == correct
    err = capsys.readouterr()

    assert msg in err.out
    assert out == correct


# ==================
# Functional Testing
# ==================
# Tests of UnitForm, SimplifyUnits, ConvertToBasis, MultiplyUnitsByBasis, 
# and AffineConvert.
C_to_F = AffineConvert(
    from_unit='C',
    to_unit='F',
    to_offset=32,
    factor=9/5,
)


F_to_C = AffineConvert(
    from_unit='F',
    to_unit='C',
    from_offset=-32,
    factor=5/9,
)


@pytest.mark.parametrize(
    'in_string, correct_string, rule',
    [
        (' 5 ` C ', ' 41 ` F', C_to_F),
        (' 5 ` F ', ' 5 ` F', C_to_F),
        (' 41  ` F ', ' 5 ` C', F_to_C),
        (' 41  ` C ', ' 41 ` C', F_to_C),
        (
            ' y = 5 ` m**2 * N * min ',
            ' y = 30000 ` star(cm, J, s) ',
            RulesBU(Nm_to_J, tocm, tosec, simplifyunits),
        ),
    ],
    ids=[
        'convert with C_to_F',
        'C_to_F does nor apply',
        'convert with F_to_C',
        'F_to_C does nor apply',
        'ConvertTo, MultiplyBy, SimplifyUnits',
    ]
)
def test_functional(in_string, correct_string, rule):
    in_ = parse(in_string)
    correct = parse(correct_string)

    out = rule(in_)

    assert out == correct
