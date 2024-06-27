from truealgebra.core.rules import (
    RuleBase, TrueThing, Rule, donothing_rule, Substitute, Rules, RulesBU,
    JustOne, JustOneBU, TrueThingJO
)
from truealgebra.core.expression import ExprBase
import pytest

# =============
# Test RuleBase
# =============
class Datum(ExprBase):
    def __init__(self, datum):
        object.__setattr__(self, "datum", datum)

    def bottomup(self, rule):
        return rule(self, _pathinhibit=True, _buinhibit=True)

    def apply2path(self, path, rule):
        return rule(self, _pathinhibit=True)

    def __eq__(self, other):
        return  type(self) is type(other) and self.datum == other.datum

    def __hash__(self):
        return hash((type(self), self.datum))


class Data(ExprBase):
    def __init__(self, name, datum0, datum1):
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "data", (datum0, datum1))

    def bottomup(self, rule):
        return rule(
            self.__class__(
                self.name,
                self.data[0].bottomup(rule),
                self.data[1].bottomup(rule),
            ),
            _pathinhibit=True,
            _buinhibit=True
        )

    def apply2path(self, path, rule):
        if not path:
            return rule(self, _pathinhibit=True)
        nxt = path[0]
        newpath = path[1:]
        if nxt == 0:
            datum0 = self.data[0].apply2path(newpath, rule)
            datum1 = self.data[1]
        elif nxt == 1:
            datum0 = self.data[0]
            datum1 = self.data[1].apply2path(newpath, rule)
        return self.__class__(self.name, datum0, datum1)

    def __eq__(self, other):
        return (
            type(self) is type(other)
            and self.name == other.name
            and self.data[0] == other.data[0]
            and self.data[1] == other.data[1]
        )

    def __hash__(self):
        return hash((
            type(self),
            self.name,
            self.data[0],
            self.data[1],
        ))


class XToY(RuleBase):
    def tpredicate(self, expr):
        if isinstance(expr, Datum) and expr.datum == 'x':
            return TrueThing(expr)
        elif isinstance(expr, Data) and expr.name == 'x':
            return TrueThing(expr)
        else:
            return False
    def tbody(self, truething):
        expr = truething.expr
        if isinstance(expr, Datum):
            return Datum('y')
        elif isinstance(expr, Data):
            return Data('y', expr.data[0], expr.data[1])



xtoy = XToY()
xtoy0 = XToY(path = [0])
xtoy1 = XToY(bottomup=True)
xtoy2 = XToY(path = [1], bottomup=True)

dw = Datum('w')
dx = Datum('x')
dy = Datum('y')
dz = Datum('z')


@pytest.mark.parametrize(
    "expr_in, correct",
    [
        (dx, dy),
        (dz, dz),
    ]
)
# Test RuleBase without bottomup or path
def test_rulebase_plain_0(expr_in, correct):
    out = xtoy(expr_in)

    assert out.datum == correct.datum


@pytest.mark.parametrize(
    "expr_in, correct",
    [
        (Data('x', dx, dx), Data('y', dx, dx)),
        (Data('z', dx, dx), Data('z', dx, dx)),
    ]
)
# Test RuleBase without bottomup or path
def test_rulebase_plain_1(expr_in, correct):
    out = xtoy(expr_in)

    assert out.name == correct.name
    assert out.data[0].datum == correct.data[0].datum
    assert out.data[1].datum == correct.data[1].datum


expr_bu_path = Data('x', dx, Data('x', dx, dx))


@pytest.mark.parametrize(
    "rule, correct, bu, path",
    [
        (xtoy0, Data('x', dy, Data('x', dx, dx)), False, (0,)),
        (xtoy1, Data('y', dy, Data('y', dy, dy)), True, ()),
        (xtoy2, Data('x', dx, Data('y', dy, dy)), True, (1,)),
    ]
)
# Test RuleBase with bottomup and/or path
def test_rulebase_bu_path(rule, correct, bu, path):
    out = rule(expr_bu_path)

    assert out.name == correct.name
    assert out.data[0].datum == correct.data[0].datum
    assert out.data[1].name == correct.data[1].name
    assert out.data[1].data[0].datum == correct.data[1].data[0].datum
    assert out.data[1].data[1].datum == correct.data[1].data[1].datum
    assert rule.path == path
    assert rule.bottomup == bu


# =========
# Test Rule
# =========
def test_rule_body():
    out = donothing_rule.body(dx)

    assert type(out) == Datum
    assert out.datum == 'x'


def test_rule_predicate():
    out = donothing_rule.predicate(dx)

    assert out is False

def test_rule_tpredicate():
    out = donothing_rule.tpredicate(dx)

    assert out is False


@pytest.fixture
def donothing_rule2():
    class Rule2(Rule):
        def predicate(self, expr):
            return True

    return Rule2()


def test_rule_tpredicate2(donothing_rule2):
    out = donothing_rule2.tpredicate(dx)

    assert type(out) is TrueThing
    assert type(out.expr) is Datum
    assert out.expr.datum == 'x'


def test_rule_tbody():
    thing = TrueThing(dx)
    out = donothing_rule.tbody(thing)

    assert type(out) is Datum
    assert out.datum == 'x'


# ===============
# Test Substitute
# ===============
subdict = {dx: dz, dy: dz}
toz = Substitute(subdict=subdict)
ztow = Substitute(subdict={dz: dw})
wtox = Substitute(subdict={dw: dx})
ytoz = Substitute(subdict={dy: dz})
tozpathbu = Substitute(subdict=subdict, bottomup=True, path=(1,))


@pytest.mark.parametrize(
    'expr, correct',
    [
        (dx, True),
        (dz, False),
    ]
)
def test_substitute_predicate(expr, correct):
    out = toz.predicate(expr)

    assert out is correct

def test_substitute_body():
    out = toz.body(dx)

    assert out == dz


def test_substitute_functional():
    out = tozpathbu(expr_bu_path)

    assert out == Data('x', dx, Data('x', dz, dz))


# ==========
# Test Rules
# ==========
subrules = Rules(toz, ztow)
emptyrules = Rules()
def test_rules_tpredicate():
    out = subrules.tpredicate('garbage')

    assert type(out) is TrueThing
    assert out.expr == 'garbage'


@pytest.mark.parametrize(
    'rules, expr, correct',
    [
        (subrules, dx, dw),
        (emptyrules, dx, dx),
    ]
)
def test_rules_tbody(rules, expr, correct):
    out = rules.tbody(TrueThing(expr))

    assert out == correct


def test_rulesbu():
    rulesbu = RulesBU(toz, ztow)

    assert isinstance(rulesbu, Rules)
    assert rulesbu.bottomup is True
    

# ============
# Test JustOne
# ============
jo0 = JustOne()
jo1 = JustOne(ytoz, ztow, wtox)
jo2 = JustOne(ytoz, ytoz, jo1, ztow)


@pytest.mark.parametrize(
    'rule',
    [jo0, jo1]
)
def test_justone_tpredicate0(rule):
    out = rule.tpredicate(dx)

    assert out is False


def test_justone_tpredicate1():
    out = jo1.tpredicate(dz)

    assert isinstance(out, TrueThingJO)
    assert out.expr == dz
    assert out.ndx == 1

    assert isinstance(out.selected_truething, TrueThing)
    assert out.selected_truething.expr == dz


def test_justone_tpredicate2():
    out = jo2.tpredicate(dz)

    assert isinstance(out, TrueThingJO)
    assert out.expr == dz
    assert out.ndx == 2

    assert isinstance(out.selected_truething, TrueThingJO)
    assert out.selected_truething.expr == dz
    assert out.selected_truething.ndx == 1

    assert isinstance(out.selected_truething.selected_truething, TrueThing)
    assert out.selected_truething.selected_truething.expr == dz


# functional test, and test tbody and eval_selected methods
def test_justone():
    out = jo2(dz)

    assert out == dw


def test_justonebu():
    justonebu = JustOneBU(toz, ztow)

    assert isinstance(justonebu, JustOne)
    assert justonebu.bottomup is True
