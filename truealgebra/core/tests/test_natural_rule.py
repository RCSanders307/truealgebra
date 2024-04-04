#from truealgebra.core.tests.common_test_info import (
#    Co, CA, Sy, Nu, NR, HNR,
#    RB, RsBU
#)
from truealgebra.core.abbrv import *
from truealgebra.core.parse import Parse, meta_parser
from truealgebra.core.settings import Settings
from truealgebra.core.rulebase import placebo_rule, TrueThingNR
from truealgebra.core.expression import null, true, false, CommAssocMatch
import types
import pytest

settings = Settings()

settings.set_custom_bp("=", 50, 50)
settings.set_custom_bp("*", 1000, 1000)

settings.set_container_subclass("*", CA)
settings.set_complement('star', '*')

settings.set_categories('suchthat', '|')
settings.set_categories('suchthat', 'suchthat')
settings.set_categories('forall', '@')

settings.set_categories('forall', 'forall')

parse = Parse(settings)


# outcome_rule
# ============
class Flatten(RB):
    """ Flattens nested ComAssoc expressions"""
    def predicate(self, expr):
        return isinstance(expr, CA)

    def body(self, expr):
        name = expr.name
        newitems = []
        for item in expr.items:
            if isinstance(item, CA) and item.name == name:
                newitems.extend(item.items)
            else:
                newitems.append(item)
        return CA(expr.name, newitems)


flatten = Flatten(bottomup=True)


# Predicate Rule
# ==============
class IsIntRule(RB):
    def predicate(self, expr):
        return (isinstance(expr, Co)
                and expr.name == 'isint'
                and len(expr) >= 1)

    def body(self, expr):
        if isinstance(expr[0], Nu) and isinstance(expr[0].value, int):
            return true
        else:
            return false


class IsRealRule(RB):
    def predicate(self, expr):
        return (isinstance(expr, Co)
                and expr.name == 'isreal'
                and len(expr) == 1)

    def body(self, expr):
        if (
            isinstance(expr[0], Nu)
            and isinstance(expr[0].value, float)
        ):
            return true
        else:
            return false


pred_rule = RsBU(IsIntRule(), IsRealRule())


# NaturalRule Functional Testing
# ==============================
rule0 = NR(
    var_defn=" forall(ex0, ex1, ex2, ex3) ",
    pattern=" (ex0 = ex1) * (ex2 = ex3) ",
    outcome=" ex0 * ex2 = ex1 * ex3  ",
    parse=parse)
arg0 = '(a = b) * (c = d)'
correct0 = 'a * c = b * d'


rule1 = NR(
    predicate_rule=pred_rule,
    var_defn=" suchthat( forall(__x), isint(__x)); forall(__1) ",
    pattern=" star(__x, 3.7, __1) ",
    outcome=" star( 3.7, __x, __1) ",
    parse=parse)


arg1 = ' star(3, 3.7, 4, a, 5) '
correct1 = ' star(3.7, star(3, 4, 5), star(a)) '


arg2 = ' star(3, 3.7, 4, 5) '
correct2 = ' star(3, 3.7, 4, 5) '


rule3 = NR(
    predicate_rule=pred_rule,
    pattern=" star(1, 2, 3) ",
    outcome=" 6 ",
    parse=parse)
arg3 = ' star(3, 1, 2) '
correct3 = '6'


rule4 = NR(
    var_defn=" suchthat( forall(x), isint(x)); forall(y) ",
    predicate_rule=pred_rule,
    pattern=" star(x, y, 3) ",
    outcome=" f(3, x, y) ",
    parse=parse)
arg4 = ' star(3, 1, a) '
correct4 = ' f(3, 1, a) '


@pytest.mark.parametrize(
    'rule, argument, correct',
    [
        (rule0, arg0, correct0),
        (rule1, arg1, correct1),
        (rule1, arg2, correct2),
        (rule3, arg3, correct3),
        (rule4, arg4, correct4),
    ]
)
def test_naturalrule_functional(rule, argument, correct):
    argument = parse(argument)
    correct = parse(correct)

    output = rule(argument)

    assert output == correct


# Test Create Variable Dictionary
# ===============================
@pytest.mark.parametrize(
    'intro, vardict',
    [
        (' forall(x, 7, y, sin(z)) ', {Sy('x'): null, Sy('y'): null}),
        ('suchthat(forall(x), isint(x))', {Sy('x'): Co('isint', (Sy('x'),))}),
    ],
    ids=[
        'forall intro',
        'suchthat intro',
    ],
)
def test_create_vardict(intro, vardict):
    out = NR.create_var_dict(intro, parse)

    assert out == vardict


def test_create_vardict_exception(capsys):
    msg = 'Index Error in forall or suchthat container expression'

    out = NR.create_var_dict('suchthat()', parse)
    err = capsys.readouterr()

    assert msg in err.out


# Test Natural Rule Init
# ======================
def test_naturalrule_init_default():
    """ Test class attributes, which are essentially the defaults"""
    nr = NR()

    assert isinstance(nr.parse, Parse)
    assert isinstance(nr.parse.settings, Settings)
    assert nr.predicate_rule is placebo_rule
    assert nr.outcome_rule is placebo_rule
    assert nr.pattern is null
    assert nr.outcome is null
    assert isinstance(nr.var_defn, types.MappingProxyType)
    assert len(nr.var_defn) == 0

def test_naturalrule_init_parse_rules():
    """ Test assignment of values to the
    parse, predicate_rule, and  pred_rule, attributes.
    """
    nr = NR(
        parse=parse,
        predicate_rule=pred_rule,
        outcome_rule=flatten,
    )

    assert nr.parse is parse
    assert nr.predicate_rule is pred_rule
    assert nr.outcome_rule is flatten

tnip_str = 'suchthat(forall(x), isint)'
tnip_dict = NR.create_var_dict(tnip_str, parse)


@pytest.mark.parametrize(
    'pattern, pcorrect, outcome, ocorrect, var_defn, vcorrect',
    [
        (
            ' cos(x) ',
            Co('cos', (Sy('x'),)),
            ' sin(x) ',
            Co('sin', (Sy('x'),)),
            tnip_str,
            tnip_dict,
        ),
        (
            Co('cos', (Sy('x'),)),
            Co('cos', (Sy('x'),)),
            Co('sin', (Sy('x'),)),
            Co('sin', (Sy('x'),)),
            tnip_dict,
            tnip_dict,
        ),
    ],
    ids=[
        'string inputs',
        'expression inputs',
    ],
)
def test_naturalrule_init_pov(
    pattern, pcorrect, outcome, ocorrect, var_defn, vcorrect
    ):
    """ Test pattern, outcome, and var_defn parameters."""
    nr = NR(
        parse=parse,
        pattern=pattern,
        outcome=outcome,
        var_defn=var_defn,
    )


    assert nr.pattern == pcorrect
    assert nr.outcome == ocorrect
    assert nr.var_defn == vcorrect


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
def test_tpredicate(expr, thing):
    rule = NR(
        parse = parse,
        predicate_rule=pred_rule,
        pattern=' n ',
        var_defn = 'suchthat(forall(n), isint(n))',
    )

    out = rule.tpredicate(expr)

    if out:
        assert out.input_expression == thing.input_expression
        assert out.subdict == thing.subdict
    else:
        assert out is False


# Test NaturalRule tbody
# ======================
def test_naturalrule_tbody():
    """Test NaturalRule tbody method
    """
    nr0 = NR(
        var_defn={Sy('x'): Co('isint', (Sy('x'),))},
        outcome_rule=flatten,
        predicate_rule=pred_rule,
        outcome=CA('*', (Nu(3), CA('*', (Sy('x'), Nu(7))) )),
    )
    truething = TrueThingNR(
        input_expression=null,  # This parameter does not affect the test
        subdict={Sy('x'): Nu(2)},
    )

    out = nr0.tbody(truething)

    assert out == CA('*', (Nu(3), Nu(2), Nu(7)))


# ====================
# Test HalfNaturalRule
# ====================

# Test HalfNaturalRule var_names
# ==============================
def test_hnr_var_names():
    hnr = HNR()
    subdict = {Sy('x'): Nu(0), Sy('y'): Sy('a'), Sy('_'): Nu(2)}

    var_names = hnr.VarNames(subdict)

    assert var_names.x == Nu(0)
    assert var_names.y == Sy('a')
    assert var_names._ == Nu(2)


# Test HalfNaturalRules tpredicate
# ================================
def test_hnr_tpredicate():
    class HNR0(HNR):
        var_defn = (
            ' suchthat(forall(x), isint(x)); '
            ' suchthat(forall(y), isreal(y)); '
            ' forall(_) '
        )
        pattern = parse(' _ ++ (y ** x) ')
        parse = parse
        predicate_rule = pred_rule

        def body(self, expr, var):
            num = var.y.value ** var.x.value
            return Co('++', (var._, Nu(num)))


    hnr = HNR0()
    expr0 = parse(' y ++ (3.0 ** 2) ')
    expr1 = parse(' y ++ (4 ** a) ')

    pred_out0 = hnr.tpredicate(expr0)
    pred_out1 = hnr.tpredicate(expr1)

    assert pred_out0.__bool__() == True
    assert pred_out0.input_expression == expr0
    assert pred_out0.var.x == Nu(2)
    assert pred_out0.var.y == Nu(3.0)
    assert pred_out0.var._ == Sy('y')

    assert pred_out1 is False
