from truealgebra.core.rules import Rule, RulesBU
from truealgebra.core.expression import (
    CommAssoc, Number, Container, Symbol, CommAssocMatch,
    null, true, false, any__
)
import pytest
#import truealgebra.std.settings


class Num:
    i0 = Number(0)
    i1 = Number(1)
    i2 = Number(2)
    i3 = Number(3)
    r4 = Number(4.0)


num = Num()


class Sym:
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    sp0 = Symbol('__special')
    sp1 = Symbol('__1special')
    sp2 = Symbol('__2special')
    sp3 = Symbol('__3special')
    sp45 = Symbol('__45special')
    not_sp = Symbol('_2special')
    short = Symbol('_')


sym = Sym()


class Ex:
    @property
    def trig0(self):
        cosx = Container('cos', (sym.x,))
        cosx_2 = Container('**', (cosx, num.i2))
        siny = Container('sin', (sym.y,))
        siny_2 = Container('**', (siny, num.i2))
        return Container('-', (cosx_2, siny_2))

    ca0 = CommAssoc('*', (num.r4, sym.x, sym.sp1, sym.sp0))
    ca1 = CommAssoc('*', (num.i1, num.i2, num.r4))

    fx = Container('f', (sym.x,))
    fy = Container('f', (sym.y,))
    gx = Container('g', (sym.x,))

    gy = Container('g', (sym.y,))
    hz = Container('h', (sym.z,))
    f1 = Container('f', (num.i1,))
    g3 = Container('g', (num.i3,))
    h4 = Container('h', (num.r4,))

    f3 = Container('f', (num.i3,))
    g1 = Container('g', (num.i1,))


ex = Ex()


class Pred:
    any__ = Container('isint', (any__,))
    x = Container('isint', (sym.x,))
    y = Container('isint', (sym.y,))
    z = Container('hasone', (sym.z,))


pred = Pred()


# Predicate rules
class IsIntRule(Rule):
    def predicate(self, expr):
        return (isinstance(expr, Container)
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


class HasOneRule(Rule):
    def predicate(self, expr):
        return (
            isinstance(expr, Container)
            and expr.name == 'hasone'
            and len(expr) == 1
        )

    def body(self, expr):
        if (
            isinstance(expr[0], Container)
            and len(expr[0]) == 1
            and expr[0][0] == Number(1)
        ):
            return true
        else:
            return expr


# Define the predicate rule
# which evalutaes predicate expressions to true or false.
pred_rule = RulesBU(IsIntRule(), IsRealRule(), HasOneRule())


class EmptyCommAssocMatch(CommAssocMatch):
    def __init__(self):
        self.pattern = null
        self.vardict = {}
        self.subdict = dict()
        self.pred_rule = pred_rule
        self.target_list = []


# Testing Starts Below
#
def test_pattern_match_0():
    cam = EmptyCommAssocMatch()
    cam.vardict = {sym.x: pred.x, sym.z: pred.z}

    match = cam.pattern_match(
        [ex.fx, sym.z],  # pattern list
        {},  # subdict
        [ex.f1, ex.f3],  # target list
    )

    assert bool(match) is True
    assert match.subdict == {sym.x: Number(3), sym.z: ex.f1}
    assert match.target_list == list()


def test_pattern_match_1():
    cam = EmptyCommAssocMatch()
    cam.vardict = {sym.x: pred.x, sym.z: pred.z}
    subdict = {}
    target_list = [ex.f1, ex.f3]

    match = cam.pattern_match(
        [sym.z, ex.fx],  # pattern list
        subdict,  # subdict
        target_list,  # target list
    )

    assert bool(match) is True
    assert match.subdict == {sym.x: Number(3), sym.z: ex.f1}
    assert match.target_list == list()
    assert id(match.subdict) != id(subdict)
    assert id(match.target_list) != id(target_list)


def test_pattern_match_2():
    cam = EmptyCommAssocMatch()
    cam.vardict = {sym.x: pred.x, sym.z: pred.z}
    subdict = {}
    target_list = [ex.f1]

    match = cam.pattern_match(
        [sym.z],  # pattern list
        subdict,  # subdict
        target_list,  # target list
    )

    assert bool(match) is True
    assert match.subdict == {sym.z: ex.f1}
    assert match.target_list == list()
    assert id(match.subdict) != id(subdict)
    assert id(match.target_list) == id(target_list)


def test_pattern_match_2a():
    cam = EmptyCommAssocMatch()
    cam.vardict = {sym.x: pred.x, sym.z: pred.z}
    subdict = {}
    target_list_0 = [ex.f3]
    target_list_1 = target_list_0.copy()

    match = cam.pattern_match(
        [sym.z],  # pattern list
        subdict,  # subdict
        target_list_1,  # target list
    )

    assert match is False
    assert target_list_1 == target_list_0


def test_pattern_match_3():
    cam = EmptyCommAssocMatch()
    cam.vardict = {sym.x: pred.x, sym.y: pred.y}

    match = cam.pattern_match(
        [ex.fx, ex.gy, ex.fy],  # pattern list
        {sym.short: pred.any__},  # subdict
        [ex.f1, sym.a, ex.g1, sym.b, ex.f3],  # target list
    )

    assert bool(match) is True
    assert match.subdict == {
        sym.short: pred.any__, sym.x: num.i3, sym.y: num.i1
    }
    assert match.target_list == [sym.a, sym.b]


def test_pattern_match_4():
    cam = EmptyCommAssocMatch()
    cam.vardict = {sym.x: pred.x, sym.y: pred.y}

    match = cam.pattern_match(
        [ex.gy, ex.fy, ex.fx],  # pattern list
        {sym.short: pred.any__},  # subdict
        [ex.f1, sym.a, ex.g1, sym.b, ex.f3],  # target list
    )

    assert bool(match) is True
    assert match.subdict == {
        sym.short: pred.any__, sym.x: num.i3, sym.y: num.i1
    }
    assert match.target_list == [sym.a, sym.b]


def test_init():
    cam = CommAssocMatch(
        pattern=ex.ca0,
        vardict={sym.sp1: pred.any__, sym.sp0: null, sym.x: null},
        subdict=dict(),
        pred_rule=pred_rule,
        target=ex.ca1,
    )

    assert cam.pattern == ex.ca0
    assert cam.vardict == {sym.sp1: pred.any__, sym.sp0: null, sym.x: null}
    assert cam.subdict == dict()
    assert cam.pred_rule == pred_rule
    assert cam.target_list == [num.i1, num.i2, num.r4]


def test_find_minimum_length():
    cam = EmptyCommAssocMatch()

    assert cam.find_minimum_length(sym.sp0) == 0
    assert cam.find_minimum_length(sym.sp2) == 2
    assert cam.find_minimum_length(sym.sp45) == 45


def test_does_contain_variable():
    cam = EmptyCommAssocMatch()
    cam.vardict = {sym.sp1: pred.any__, sym.sp0: null, sym.x: null}

    con0 = Container('f', (sym.x, sym.a))
    con1 = Container('f', (con0, sym.a))
    con2 = Container('f', (sym.a, sym.b))
    con3 = Container('f', (con2, sym.a))

    assert cam.does_contain_variable(sym.x) is True
    assert cam.does_contain_variable(sym.y) is False
    assert cam.does_contain_variable(num.r4) is False
    assert cam.does_contain_variable(con1) is True
    assert cam.does_contain_variable(con3) is False


# Minimum instance length satisfied. vardict value not null
def test_special_match0():
    m0 = CommAssocMatch(
        pattern=CommAssoc('*', (sym.sp1, sym.sp0)),
        vardict={sym.sp1: pred.any__, sym.sp0: null},
        subdict=dict(),
        pred_rule=pred_rule,
        target=CommAssoc('*', (sym.a, num.i1, sym.b, num.i2, num.r4)),
    )

    out = m0.special_match(sym.sp1)

    assert out is True
    assert m0.subdict == {sym.sp1: CommAssoc('*', (num.i1, num.i2))}
    assert m0.target_list == [sym.a, sym.b, num.r4]


# Minimum instance length not satisfied. vardict value not null
def test_special_match1():
    m0 = CommAssocMatch(
        pattern=CommAssoc('*', (sym.sp3, sym.sp0)),
        vardict={sym.sp3: pred.any__, sym.sp0: null},
        subdict=dict(),
        pred_rule=pred_rule,
        target=CommAssoc('*', (sym.a, num.i1, sym.b, num.i2, num.r4)),
    )

    out = m0.special_match(sym.sp3)

    assert out is False
    assert m0.subdict == dict()
    assert m0.target_list == [sym.a, sym.b, num.r4]


# variable is key in subdict, ca_intance not equal to subdict value
def test_special_match2():
    m0 = CommAssocMatch(
        pattern=CommAssoc('*', (sym.sp1, sym.sp0)),
        vardict={sym.sp1: pred.any__, sym.sp0: null},
        subdict={sym.sp1: CommAssoc('*', (sym.a, sym.b))},
        pred_rule=pred_rule,
        target=CommAssoc('*', (sym.a, num.i1, sym.b, num.i2, num.r4)),
    )

    out = m0.special_match(sym.sp1)

    assert out is False
    assert m0.subdict == {sym.sp1: CommAssoc('*', (sym.a, sym.b))}
    assert m0.target_list == [sym.a, sym.b, num.r4]


# variable is key in subdict, ca_intance equal to subdict value
def test_special_match3():
    m0 = CommAssocMatch(
        pattern=CommAssoc('*', (sym.sp1, sym.sp0)),
        vardict={sym.sp1: pred.any__, sym.sp0: null},
        subdict={sym.sp1: CommAssoc('*', (num.i1, num.i2))},
        pred_rule=pred_rule,
        target=CommAssoc('*', (sym.a, num.i1, sym.b, num.i2, num.r4)),
    )

    out = m0.special_match(sym.sp1)

    assert out is True
    assert m0.subdict == {sym.sp1: CommAssoc('*', (num.i1, num.i2))}
    assert m0.target_list == [sym.a, sym.b, num.r4]


# value of variable in vardict is null
def test_special_match4():
    m0 = CommAssocMatch(
        pattern=CommAssoc('*', (sym.sp0,)),
        vardict={sym.sp1: pred.any__, sym.sp0: null},
        subdict=dict(),
        pred_rule=pred_rule,
        target=CommAssoc('*', (sym.a, num.i1, sym.b, num.i2, num.r4)),
    )

    out = m0.special_match(sym.sp0)

    assert out is True
    assert m0.subdict == {
        sym.sp0: CommAssoc('*', (sym.a, num.i1, sym.b, num.i2, num.r4))
    }
    assert m0.target_list == []


def test_plain_expr_match0():
    con0 = Container('f', (sym.a, sym.b))
    m0 = CommAssocMatch(
        pattern=CommAssoc('*', (sym.sp0,)),
        vardict={sym.sp1: pred.any__, sym.sp0: null},
        subdict=dict(),
        pred_rule=pred_rule,
        target=CommAssoc('*', (sym.a, num.i1, sym.b, con0, num.i2, num.r4)),
    )

    match0 = m0.plain_expr_match(con0)

    assert match0 is True
    assert m0.target_list == [sym.a, num.i1, sym.b, num.i2, num.r4]


def test_plain_expr_match1():
    con0 = Container('f', (sym.a, sym.b))
    con1 = Container('f', (sym.a, sym.c))
    m0 = CommAssocMatch(
        pattern=CommAssoc('*', (sym.sp0,)),
        vardict={sym.sp1: pred.any__, sym.sp0: null},
        subdict=dict(),
        pred_rule=pred_rule,
        target=CommAssoc('*', (sym.a, num.i1, sym.b, con0, num.i2, num.r4)),
    )

    match0 = m0.plain_expr_match(con1)

    assert match0 is False
    assert m0.target_list == [sym.a, num.i1, sym.b, con0, num.i2, num.r4]


def test_process_plain_expr_list_0():
    cam = EmptyCommAssocMatch()
    cam.target_list = [ex.f3, ex.g1, num.i0, sym.a]
    plain_expr_list = [num.i0, sym.a, ex.g1]

    out = cam.process_plain_expr_list(plain_expr_list)

    assert out is True
    assert cam.target_list == [ex.f3]


def test_process_plain_expr_list_1():
    cam = EmptyCommAssocMatch()
    cam.target_list = [ex.f3, ex.g1, num.i0]
    plain_expr_list = [num.i0, sym.a, ex.g1]

    out = cam.process_plain_expr_list(plain_expr_list)

    assert out is False


@pytest.mark.parametrize(
    'special_list, target_list, match_bool',
    [
        ([sym.sp1, sym.sp0], [sym.a, num.i1, sym.b, num.i2, num.r4], True),
        ([sym.sp1, sym.sp0], [sym.a, sym.b, num.r4], False),
        ([], [sym.a, sym.b, num.r4], True),
    ]
)
def test_process_special_list(special_list, target_list, match_bool):
    cam = EmptyCommAssocMatch()
    cam.pattern = CommAssoc('*', ())  # name attribute '*' is needed
    cam.vardict = {sym.sp1: pred.any__, sym.sp0: null}
    cam.subdict = dict()
    cam.pred_rule = pred_rule
    cam.target_list = target_list

    match = cam.process_special_list(special_list)

    assert match is match_bool


def test_process_pattern_list_0():
    cam = EmptyCommAssocMatch()
    cam.vardict = {sym.x: pred.x, sym.z: pred.z}
    cam.subdict = {sym.b: sym.c}
    cam.target_list = [ex.f1, ex.f3, sym.a]
    pattern_list = [ex.fx, sym.z]

    match = cam.process_pattern_list(pattern_list)

    assert match is True
    assert cam.subdict == {sym.b: sym.c, sym.x: Number(3), sym.z: ex.f1}
    assert cam.target_list == [sym.a]


def test_process_pattern_list_1():
    cam = EmptyCommAssocMatch()
    cam.vardict = {sym.x: pred.x, sym.z: pred.z}
    cam.subdict = {sym.b: sym.c}
    cam.target_list = [ex.f3, sym.a]
    pattern_list = [ex.fx, sym.z]

    match = cam.process_pattern_list(pattern_list)

    assert match is False


@pytest.mark.parametrize(
    'pattern, vardict, target, correct',
    [
        (
            CommAssoc('+', (num.i0, sym.a)),
            dict(),
            CommAssoc('+', (num.i0, sym.a)),
            True,
        ),
        (
            CommAssoc('+', (num.i0, sym.a)),
            dict(),
            CommAssoc('+', (num.i0,)),
            False,
        ),
        (
            CommAssoc('+', (sym.x, ex.fx)),
            {sym.x: pred.x},
            CommAssoc('+', (ex.f1, num.i1,)),
            True,
        ),
        (
            CommAssoc('+', (sym.x, ex.fx)),
            {sym.x: pred.x},
            CommAssoc('+', (ex.f1,)),
            False,
        ),
        (
            CommAssoc('+', (sym.sp1, sym.sp0)),
            {sym.sp1: pred.any__, sym.sp0: null},
            CommAssoc('+', (sym.a, num.i1,)),
            True,
        ),
        (
            CommAssoc('+', (sym.sp1, sym.sp0)),
            {sym.sp1: pred.any__, sym.sp0: null},
            CommAssoc('+', (sym.a, sym.b,)),
            False,
        ),
        (
            CommAssoc('+', (sym.sp1,)),
            {sym.sp1: pred.any__},
            CommAssoc('+', (num.i1, sym.b,)),
            False,
        ),
    ]
)
def test_find_matches(pattern, vardict, target, correct):
    cam = CommAssocMatch(
        pattern=pattern,
        vardict=vardict,
        subdict=dict(),
        pred_rule=pred_rule,
        target=target,
    )

    output = cam.find_matches()

    assert output == correct
