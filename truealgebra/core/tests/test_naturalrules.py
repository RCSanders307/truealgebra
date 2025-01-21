from truealgebra.core.abbrv import (
    Nu, Sy, Co, CA, NR, HNR, Ru, RsBU
)
from truealgebra.core.expressions import (
    null, true, false, CommAssoc, Container, Number
)
from truealgebra.core.rules import (
    donothing_rule, Rule, RulesBU
)
from truealgebra.core.parse import Parse
from truealgebra.core.settings import SettingsSingleton
from truealgebra.core import setsettings
from truealgebra.core.naturalrules import(
    TrueThingNR, TrueThingHNR, NaturalRuleBase, NaturalRule, HalfNaturalRule
)
import types
import pytest

#Delete Me
from IPython import embed


@pytest.fixture
def settings(scope='module'):
    settings = SettingsSingleton()
    settings.reset()

    setsettings.set_custom_bp("=", 50, 50)
    setsettings.set_custom_bp("*", 1000, 1000)

    setsettings.set_container_subclass("*", CA)
    setsettings.set_complement('star', '*')

    setsettings.set_categories('suchthat', '|')
    setsettings.set_categories('forall', '@')
    settings.parse = Parse()

    yield settings
    settings.reset()

@pytest.fixture
def badsettings(scope='module'):
    settings = SettingsSingleton()
    settings.reset()
    yield settings
    settings.reset()


# Predicate Rule
# ==============
class IsIntRule(Rule):
    def predicate(self, expr):
        return (isinstance(expr, Co)
                and expr.name == 'isint'
                and len(expr) >= 1)

    def body(self, expr):
        if isinstance(expr[0], Number) and isinstance(expr[0].value, int):
            return true
        else:
            return false


class IsRealRule(Rule):
    def predicate(self, expr):
        return (isinstance(expr, Container)
                and expr.name == 'isreal'
                and len(expr) == 1)

    def body(self, expr):
        if (
            isinstance(expr[0], Number)
            and isinstance(expr[0].value, float)
        ):
            return true
        else:
            return false


predrule = RulesBU(IsIntRule(), IsRealRule())

# outcome_rule
# ============
class Flatten(Rule):
    """ Flattens nested ComAssoc expressions"""
    def predicate(self, expr):
        return isinstance(expr, CommAssoc)

    def body(self, expr):
        name = expr.name
        newitems = []
        for item in expr.items:
            if isinstance(item, CA) and item.name == name:
                newitems.extend(item.items)
            else:
                newitems.append(item)
        return CommAssoc(expr.name, newitems)


flatten = Flatten(bottomup=True)


# ================
# Test TrueThingNR
# ================
def test_truethingnr(settings):
    thing = TrueThingNR(Sy('x'), subdict={Sy('x'): Sy('y')})
    empty = TrueThingNR(Sy('x'))

    assert thing.expr == Sy('x')
    assert thing,subdict == {Sy('x'): Sy('y')}
    assert thing.__bool__() is True
    assert empty.subdict == types.MappingProxyType(dict())


def test_truethinghnr(settings):
    subdict={Sy('x'): Sy('y')}
    var=HalfNaturalRule.VarNames(subdict)
    thing = TrueThingHNR(Sy('x'), var=var)

    assert thing.expr == Sy('x')
    assert thing.var == var
    assert thing.__bool__() is True


# ====================
# Test NaturalRuleBase
# ====================
# Test Create Variable Dictionary
@pytest.mark.parametrize(
    'varstring, vardict',
    [
        (' forall(x, 7, y, sin(z)) ', {Sy('x'): true, Sy('y'): true}),
        ('suchthat(forall(x), isint(x))', {Sy('x'): Co('isint', (Sy('x'),))}),
        (
            'forall(x, y); forall(z) ',
            {Sy('x'): true, Sy('y'): true, Sy('z'): true}
        ),
    ],
    ids=[
        'forall intro',
        'suchthat intro',
        'meta_parser',
    ],
)
def test_create_vardict(varstring, vardict, settings):
#   xxx = 100; embed()
    out = NaturalRuleBase.create_vardict(varstring)

    assert out == vardict


def test_create_vardict_exception(capsys, settings):
    msg = 'Index Error in forall or suchthat container expression'
    out = NaturalRule.create_vardict('suchthat()')
    output = capsys.readouterr()

    assert msg in output.out
    assert out == dict()



def test_naturalrulebase_default(settings):
    assert NaturalRuleBase.predicate_rule is donothing_rule
    assert NaturalRuleBase.pattern is null
    assert NaturalRuleBase.vardict == dict()
    assert type(NaturalRuleBase.vardict) is types.MappingProxyType


# NaturalRuleBase cannot be instantiated,
# The subclass NaturalRule will be used for testing
def test_naturalrulebase_init_predrule(settings):
    natrule = NaturalRule(predicate_rule=predrule)

    assert natrule.predicate_rule is predrule


@pytest.mark.parametrize(
    'pat',
    ['x + y', Co('+', (Sy('x'), Sy('y')))]
)
def test_naturalrulebase_init_pattern(pat, settings):
    natrule = NaturalRule(pattern=pat)

    assert natrule.pattern == Co('+', (Sy('x'), Sy('y')))


def test_naturalrulebase_init_pattern_error(badsettings, capsys):
    NaturalRule(pattern='x + y')
    output = capsys.readouterr()

    assert 'Change settings.parse from noparse to something useful.' in output.out


def test_naturalrulebase_init_vardict(settings):
    rule = NaturalRule(vardict='forall(x)')

    assert rule.vardict == {Sy('x'): true}


def test_naturalrulebase_convert_classvar(settings):
    class NewClass(NaturalRule):
        vardict = 'forall(x, y)'

    newinstance = NewClass()

    assert NewClass.vardict == {Sy('x'): true, Sy('y'): true}
    assert newinstance.vardict == {Sy('x'): true, Sy('y'): true}


def test_naturalrulebase_convert_classvar_2(settings):
    class NewClass(NaturalRule):
        vardict = ''

    newinstance = NewClass()

    assert NewClass.vardict ==  dict()
    assert newinstance.vardict ==  dict()


# ensure that bottomup and path parameters still work in __init__
def test_naturalrulebase_init_super(settings):
    newinstance = NaturalRule(bottomup=True, path = (1,))

    assert newinstance.bottomup is True
    assert newinstance.path is (1,)


# ================
# Test NaturalRule
# ================
# Test default values, which are class attributes.
def test_naturalrule_init_default(settings):
    """ This test only looks at attributes not tested for NaturalRuleBase"""
    nr = NaturalRule()

    assert nr.outcome_rule is donothing_rule
    assert nr.outcome is null


def test_naturalrule_init_outcome_params(settings):
    """ Test assignment of values to the outcome, and outcome_rule. """
    nr = NaturalRule(
        outcome_rule=flatten,
        outcome='x * y'
    )

    assert nr.outcome_rule is flatten
    assert nr.outcome == CA('*', (Sy('x'), Sy('y')))


@pytest.mark.parametrize(
    'outcome, ocorrect',
    [
        (
            ' sin(x) ',
            Co('sin', (Sy('x'),)),
        ),
        (
            Co('sin', (Sy('x'),)),
            Co('sin', (Sy('x'),)),
        ),
    ],
    ids=[
        'string input',
        'expression input',
    ],
)
def test_naturalrule_init_outcome(outcome, ocorrect, settings):
    """ Test pattern, outcome, and var_defn parameters."""
    nr = NaturalRule(outcome=outcome,)

    assert nr.outcome == ocorrect


# Test NaturalRule tpredicate
# ===============
@pytest.mark.parametrize(
    'expr, thing',
    [
        (Nu(7), TrueThingNR(Nu(7), {Sy('n'): Nu(7)})),
        (Nu(3.4), False),
    ],
    ids=[
        'found match',
        'no match',
    ],
)
def test_tpredicate(expr, thing, settings):
    rule = NaturalRule(
        predicate_rule=predrule,
        pattern=' n ',
        vardict='suchthat(forall(n), isint(n))',
    )

    out = rule.tpredicate(expr)

    if out:
        assert out.expr == thing.expr
        assert out.subdict == thing.subdict
    else:
        assert out is False


# Test NaturalRule tbody
# ======================
def test_naturalrule_tbody(settings):
    """Test NaturalRule tbody method """
    nr0 = NR(
        vardict={Sy('x'): Co('isint', (Sy('x'),))},
        outcome_rule=flatten,
        predicate_rule=predrule,
        outcome=CA('*', (Nu(3), CA('*', (Sy('x'), Nu(7))))),
    )
    truething = TrueThingNR(
        expr=null,  # This parameter does not affect the test
        subdict={Sy('x'): Nu(2)},
    )

    out = nr0.tbody(truething)

    assert out == CA('*', (Nu(3), Nu(2), Nu(7)))


# ==============================
# NaturalRule Functional Testing
# ==============================
def test_naturalrule_functional_case_0(settings):
    rule = NaturalRule(
        vardict=" forall(ex0, ex1, ex2, ex3) ",
        pattern=" (ex0 = ex1) * (ex2 = ex3) ",
        outcome=" ex0 * ex2 = ex1 * ex3  ",
    )
    argument0 = '(a = b) * (c = d)'
    correct0 = 'a * c = b * d'

    argument = settings.parse(argument0)
    correct = settings.parse(correct0)
    output = rule(argument)

    assert output == correct


def test_naturalrule_functional_case_12(settings):
    rule = NaturalRule(
        predicate_rule=predrule,
        vardict=" suchthat( forall(__x), isint(__x)); forall(__1) ",
        pattern=" star(__x, 3.7, __1) ",
        outcome=" star( 3.7, __x, __1) ",
    )
    argument1 = ' star(3, 3.7, 4, a, 5) '
    correct1 = ' star(3.7, star(3, 4, 5), star(a)) '
    argument2 = ' star(3, 3.7, 4, 5) '
    correct2 = ' star(3, 3.7, 4, 5) '

    argument11 = settings.parse(argument1)
    correct11 = settings.parse(correct1)
#   xxx = 234; embed()
    output11 = rule(argument11)
    argument22 = settings.parse(argument2)
    correct22 = settings.parse(correct2)
    output22 = rule(argument22)

    assert output11 == correct11
    assert output22 == correct22


def test_naturalrule_functional_case_3(settings):
    rule = NaturalRule(
        predicate_rule=predrule,
        pattern=" star(1, 2, 3) ",
        outcome=" 6 ",
    )
    argument3 = ' star(3, 1, 2) '
    correct3 = '6'
    argument = settings.parse(argument3)
    correct = settings.parse(correct3)
    output = rule(argument)

    assert output == correct


def test_naturalrule_functional_case_4(settings):
    rule = NaturalRule(
        vardict=" suchthat( forall(x), isint(x)); forall(y) ",
        predicate_rule=predrule,
        pattern=" star(x, y, 3) ",
        outcome=" f(3, x, y) ",
    )
    argument4 = ' star(3, 1, a) '
    correct4 = ' f(3, 1, a) '

    argument = settings.parse(argument4)
    correct = settings.parse(correct4)
    output = rule(argument)

    assert output == correct


# =====================
# Test HalfeNaturalRule
# =====================
def test_hnr_varnames(settings):
    vn = HalfNaturalRule.VarNames({Sy('n'): Nu(3.4)})

    assert vn.n == Number(3.4)
 

@pytest.fixture
def HNR0(settings):
    class HNR0(HalfNaturalRule):
        vardict = (
            ' suchthat(forall(x), isint(x)); '
            ' suchthat(forall(y), isreal(y)); '
            ' forall(_) '
        )
        pattern = settings.parse(' _ ++ (y ** x) ')
        predicate_rule = predrule

        def body(self, expr, var):
            num = var.y.value ** var.x.value
            return Co('++', (var._, Nu(num)))

    return HNR0
 

@pytest.fixture
def halfnaturalrule0(settings, HNR0):
    return HNR0()
 

@pytest.fixture
def halfnaturalrule1(settings, HNR0):
    class HNR1(HNR0):
        def body(self, expr):
            return Number(77)

    return HNR1()

    
def test_hnr_tpredicate(settings, halfnaturalrule0):
    expr0 = settings.parse(' y ++ (3.0 ** 2) ')
    expr1 = settings.parse(' y ++ (4 ** a) ')

    pred_out0 = halfnaturalrule0.tpredicate(expr0)
    pred_out1 = halfnaturalrule0.tpredicate(expr1)

    assert pred_out0.__bool__() is True
    assert pred_out0.expr == expr0
    assert pred_out0.var.x == Nu(2)
    assert pred_out0.var.y == Nu(3.0)
    assert pred_out0.var._ == Sy('y')

    assert pred_out1 is False


def test_hnr_tbody(settings, halfnaturalrule0):
    expr0 = settings.parse(' y ++ (3.0 ** 2) ')
    var = HalfNaturalRule.VarNames(
        {Sy('_'): Sy('y'), Sy('x'): Nu(2), Sy('y'): Nu(3.0)}
    )
    pred_out0 = TrueThingHNR(expr0, var=var)

    out = halfnaturalrule0.tbody(pred_out0)

    assert out == Co('++', (Sy('y'), Nu(9.0)))


def test_hnr_tbody_error(settings, halfnaturalrule1, capsys):
    expr0 = settings.parse(' y ++ (3.0 ** 2) ')
    var = HalfNaturalRule.VarNames(
        {Sy('_'): Sy('y'), Sy('x'): Nu(2), Sy('y'): Nu(3.0)}
    )
    pred_out1 = TrueThingHNR(expr0, var=var)

    out = halfnaturalrule1.tbody(pred_out1)
    output = capsys.readouterr()

    assert 'HalfNaturalRule body method requires three arguments' in output.out
