from truealgebra.core.abbrv import (
    Nu, Sy, Co, CA, NR, HNR, RB, RsBU
)
from truealgebra.core.expression import null
from truealgebra.core.rules import donothing_rule
from truealgebra.core.parse import parse
#from truealgebra.core.settings import settings
from truealgebra.core.settings import SettingsSingleton
from truealgebra.core.naturalrules import(
    TrueThingNR, NaturalRuleBase, NaturalRule
)
import types
import pytest


@pytest.fixture
def settings(scope='module'):
    settings = SettingsSingleton()
    settings.reset()

    settings.set_custom_bp("=", 50, 50)
    settings.set_custom_bp("*", 1000, 1000)

    settings.set_container_subclass("*", CA)
    settings.set_complement('star', '*')

    settings.set_categories('suchthat', '|')
    settings.set_categories('forall', '@')
    settings.active_parse = parse

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


predrule = RsBU(IsIntRule(), IsRealRule())


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


# ====================
# Test NaturalRuleBase
# ====================
# Test Create Variable Dictionary
@pytest.mark.parametrize(
    'varstring, vardict',
    [
        (' forall(x, 7, y, sin(z)) ', {Sy('x'): null, Sy('y'): null}),
        ('suchthat(forall(x), isint(x))', {Sy('x'): Co('isint', (Sy('x'),))}),
        (
            'forall(x, y); forall(z) ',
            {Sy('x'): null, Sy('y'): null, Sy('z'): null}
        ),
    ],
    ids=[
        'forall intro',
        'suchthat intro',
        'meta_parser',
    ],
)
def test_create_vardict(varstring, vardict, settings):
    out = NaturalRuleBase.create_vardict(varstring)

    assert out == vardict


def test_naturalrulebase_default(settings):
    assert NaturalRuleBase.predicate_rule is donothing_rule
    assert NaturalRuleBase.pattern is null
    assert NaturalRuleBase.varstring == ''
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

    assert 'settings.active_parse must point to a Parse instance' in output.out


def test_naturalrulebase_init_varstring(settings):
    rule = NaturalRule(varstring='forall(x)')

    assert rule.vardict == {Sy('x'): null}


def test_naturalrulebase_convert_classvar(settings):
    class NewClass(NaturalRule):
        varstring = 'foral(x, y)'

    newinstance = NewClass()

    assert NewClass.varstring == ''
    assert NewClass,vardict == {Sy('x'): null, Sy('y'): null}
    assert newinstance,vardict == {Sy('x'): null, Sy('y'): null}


def test_naturalrulebase_convert_classvar_2(settings):
    class NewClass(NaturalRule):
        varstring = ''

    newinstance = NewClass()

    assert NewClass.varstring == ''
    assert newinstance.varstring == ''
    assert NewClass.vardict ==  dict()
    assert newinstance.vardict ==  dict()
