import pytest

from truealgebra.core.expressions import (
    ExprBase, NullSingleton, null, Symbol, Container, CommAssoc,
    Assign, Restricted, Number, any__, true, false
)
from truealgebra.core.rules import Rule, donothing_rule

# ===================
# Non pytest fixtures
# ===================

null2 = NullSingleton()
x = Symbol('x')

class ApplyF(Rule):
    """ encapsulate all expressions and subexpressions inside of a 
    Container instance with name 'F'.
    """

    def predicate(self, expr):
        return True

    def body(self, expr):
        return Container("F", (expr,))


#applyF = ApplyF(bottomup=True)
applyF = ApplyF()

class ARule(Rule):
    def predicate(self, expr):
        return True
    def body(self, expr):
        return Symbol('x')

arule = ARule(bottomup=True)
brule = ARule(path=(0, 1))

# ===================
# Test aspects of ExprBase, requres use of other objects
def test_exprbase_mutate():
    expr = Symbol('a')
    with pytest.raises(AttributeError) as error0:
        expr.name = 'abc'
    expr.rbp = 100
    expr.lbp = 101

    assert "This object should not be mutated" in str(error0.value)
    assert expr.name == 'a'
    assert expr.rbp == 100
    assert expr.lbp == 101




# Test the null object
def test_null_singleton():
    assert null2 is null

def test_null_bottomup():
    assert arule(null) is null

def test_null_path():
    assert brule(null) is null

def test_null_match():
    match1 = null.match(dict(), dict(), donothing_rule, null2)
    match2 = null.match(dict(), dict(), donothing_rule, x)

    assert match1 is True
    assert match2 is False

def test_null_eq():
    assert null == null2
    assert null != x


# ===========
# Test Symbol
# ===========
# Include tests of Atom

def test_simple_bottmup():
    expr = Symbol('a')

    assert expr.bottomup(applyF) == Container('F', (expr,))

def test__eq__name():
    assert Symbol("a") != Symbol("b")
    assert Symbol("c") == Symbol("c")

# ===========
# Test Number
# ===========

def test__eq__value():
    assert Number(3) != Number(4.5)
    assert Number(4) == Number(4)




# ==============
# Test Container
# ==============

def test_commassoc_bottomup():
    expr = CommAssoc("comas", (Number(0), Number(1), Number(2)))
    a = Container('F', (Number(0),))
    b = Container('F', (Number(1),))
    c = Container('F', (Number(2),))
    correct = Container('F', (CommAssoc('comas', (a, b, c)),))

    new = expr.bottomup(applyF)

    assert new == correct

# ===============
# Test Restricted
# ===============
def test_restricted_bottomup():
    expr = Restricted('`', (Number(2.3), Symbol('ft')))
    correct = Container("F", (expr,))

    new = expr.bottomup(applyF)

    assert new == correct


# ==============
# Test CommAssoc
# ==============

def test_inner_eq():
    ca = CommAssoc("comas", ())

    assert ca.inner_eq(
        [], 
        []
    )
    assert ca.inner_eq(
        [Number(3)],
        [Number(3)]
    )
    assert ca.inner_eq(
        [Number(0), Number(1), Number(2)],
        [Number(2), Number(0), Number(1)]
    )
    assert not (ca.inner_eq(
        [Number(0), Number(1), Number(3)],
        [Number(3), Number(1), Number(2)]
    ))

def test_commassoc__eq__():
    ca = CommAssoc("comas", (Symbol("a"), Symbol("b")))
    ca2 = CommAssoc("comas2", (Symbol("a"), Symbol("b"), Symbol("c")))
    ca3 = CommAssoc("comas", (Symbol("b"), Symbol("a")))
    ns = Container("sin", (Symbol("a"), Symbol("b")))

    assert ca != ns
    assert ca != ca2
    assert ca == ca3




#################################
# Below Are the old testss
#################################

rule = Rule()
base_msg = 'TRUEALGEBRA ERROR!\n'


def test__eq__name():
    assert Symbol("a") != Symbol("b")
    assert Symbol("c") == Symbol("c")


def test__eq__value():
    assert Number(3) != Number(4.5)
    assert Number(4) == Number(4)



def test_namedseq__eq__():
    ns = Container("sin", (Symbol("a"),))
    ns1 = Container("sin", (Symbol("a"), Symbol("b")))
    ns2 = Container("sin", (Symbol("a"),))
    object.__setattr__(ns2, 'lbp', 370)
    le = Restricted("`", (Number(3.7), Symbol("m")))
    le2 = Restricted("`", (Number(3.5), Symbol("m")))

    assert ns != ns1
    assert ns == ns2
    assert le != le2
    assert le == le


class Test_Apply2path_Method:
    expr0 = Number(3.5)
    expr0F = Container('F', (expr0,))
    expr1 = CommAssoc("comas", (Symbol('a'), Symbol('b')))
    expr1F = Container('F', (Symbol('b'),))
    expr1FF = CommAssoc("comas", (Symbol('a'), expr1F))
    expr2 = Restricted("'", (Number(2.5), Symbol("m")))
    expr2F = Container('F', (expr2,))

    @pytest.mark.parametrize(
        ('expr', 'path', 'correct'),
        [
            (expr0, [], expr0F),
            (expr1, [1], expr1FF),
            (expr2, [], expr2F),
        ]
    )
    def test_good_path(self, expr, path, correct):
        new_expr = expr.apply2path(path, applyF)

        assert new_expr == correct

    @pytest.mark.parametrize(
        ("expr", "path", "err_msg"),
        [
            (expr0, [0], base_msg + 
                'Path too long, cannot enter atom expressions.\n'
            ),
            (expr1, ['a'], base_msg + 'type error in path\n'),
            (expr1, [3], base_msg + 'index error in path\n'),
            (expr2, [1], base_msg + 'path cannot enter Restricted instnce\n'),
        ]
    )
    def test_bad_path(self, expr, path, err_msg, capsys):
        new_expr = expr.apply2path(path, applyF)
        output = capsys.readouterr()

        assert new_expr == null
        assert output.out == err_msg 
#############

class IsInt(Rule):
    def predicate(self, expr):
        return (isinstance(expr, Container)
                and expr.name == 'isint'
                and len(expr) >=1)


    def body(self,expr):
        if isinstance(expr[0], Number) and isinstance(expr[0].value, int):
            return true
        else:
            return false


pred_rule = IsInt(bottomup=True)


vardict = {
    Symbol('c') : Container('isint', (Symbol('c'),)),
    Symbol('d') : Container('isint', (any__,)),
    Symbol('e') : true,
}


i2 = Number(2)
i3 = Number(3)
r0 = Number(0.0)
r00 = Number(0.0)
r4 = Number(4.0)
sa = Symbol('a')
sc = Symbol('c')
sd = Symbol('d')
se = Symbol('e')
sf = Symbol('f')


#Number match test
@pytest.mark.parametrize(
    ('pattern', 'sdict', 'expr', 'correct_match', 'sdict2'),
    [
        (r0, dict(), r00, True, dict()),
        (r0, dict(), i2, False, dict()),
        (r0, dict(), sa, False, dict()),
    ]
)
def test_number_match( pattern, sdict, expr, correct_match, sdict2):
    match = pattern.match(vardict, sdict, pred_rule, expr)

    assert match is correct_match
    assert sdict == sdict2


#Symbol match test
@pytest.mark.parametrize(
    ('pattern', 'sdict', 'expr', 'correct_match', 'sdict2'),
    [
        (sf, dict(),    sf, True,  dict()), # pattern equals expression
        (sf, dict(),    r4, False, dict()), # pattern does not equal expression
    ]
)
def test_symbol_match( pattern, sdict, expr, correct_match, sdict2):
    match = pattern.match(vardict, sdict, pred_rule, expr)

    assert match is correct_match
    assert sdict == sdict2


# Symbol match variable test
@pytest.mark.parametrize(
    ('pattern', 'sdict', 'expr', 'correct_match', 'sdict2'),
    [
        (sc, dict(),    i2, True,  {sc : i2}), # pattern in vardict, expr not in sdict
        (sc, {sc : i2}, i3, False, {sc : i2}), # pattern in vardict and sdict, match
        (sc, {sc : i2}, i2, True,  {sc : i2}), # pattern in vardict and sdict, no match
        (sc, dict(),    r4, False,  dict()),   # pattern in vardict, 
                                               # pred_rule not satisfied
        (se, dict(),    r4, True,  {se : r4}), # pattern in vardict, null predicate
    ]
)
def test_symbol_match_variable( pattern, sdict, expr, correct_match, sdict2):
    match = pattern.match(vardict, sdict, pred_rule, expr)

    assert match is correct_match
    assert sdict == sdict2


# Container Test
cf0 = Container('f', (sc, sd, se, sa,))
cf1 = Container('f', (i2, i3, r4, sa,))
cg1 = Container('g', (i2, i3, r4, sa,))
cf2 = Container('f', (sa, r4,))
cf3 = Container('f', (r4, sa,))
caf0 = CommAssoc('f', (i2, i3, r4, sa,))
cf4 = Container('f', (sc, sd, se,))

@pytest.mark.parametrize(
    ('pattern', 'sdict', 'expr', 'correct_match', 'sdict2'),
    [
        (cf0, dict(), cf1,  True, {sc : i2, sd : i3, se : r4}),
        (cf2, dict(), cf3,  False, dict()),   # different order of items
        (cf0, dict(), caf0, False, dict()),   # different type of object
        (cf0, dict(), cg1,  False, dict()),   # different name attribute
        (cf4, dict(), cf1,  False, dict()),   # different length of items attribute
    ]
)
def test_container_match( pattern, sdict, expr, correct_match, sdict2):
    match = pattern.match(vardict, sdict, pred_rule, expr)

    assert match is correct_match
    assert sdict == sdict2


# Restricted match Test
rf0 = Restricted('f', (i2, i3, r4, sa,))
rf1 = Restricted('f', (i2, i3, r4, sa,))
rf2 = Restricted('f', (i3, r4, sa, i2,))
rf3 = Restricted('f', (sc, i3))
rf4 = Restricted('f', (i2, i3))

@pytest.mark.parametrize(
    ('pattern', 'sdict', 'expr', 'correct_match', 'sdict2'),
    [
        (rf0, dict(), rf1, True,  dict()),
# cannot match different order of items
        (rf0, dict(), rf2, False, dict()),
# cannot match a pattern inside of a Restricted instance
        (rf3, dict(), rf4, False, dict()),
    ]
)
def test_restricted_match( pattern, sdict, expr, correct_match, sdict2):
    match = pattern.match(vardict, sdict, pred_rule, expr)

    assert match is correct_match
    assert sdict == sdict2


# Assign match test
af0 = Assign('f', (i2 , i3, sa,))
af1 = Assign('f', (sc, i3, sa,))
af2 = Assign('f', (sc, sd, sa,))
af3 = Assign('f', (sc, sa, i3,))
cf0 = Container('f', (i2, i3, sa,))
ag0 = Assign('g', (sc, i3, sa,))
af4 = Assign('f', (sc, i3,))

@pytest.mark.parametrize(
    ('pattern', 'sdict', 'expr', 'correct_match', 'sdict2'),
    [
        (af1, dict(), af0,  False, dict()),
        (af2, dict(), af0,  False, {sc : i2}),   # cannot match 2nd item
        (af3, dict(), af0,  False, {sc : i2}),   # different order of items
        (af1, dict(), cf0,  False, dict()),   # different type of object
        (ag0, dict(), ag0,  False, dict()),   # different name attribute of items
        (af4, dict(), af0,  False, dict()),   # different length of items
    ]
)
def test_assign_match(pattern, sdict, expr, correct_match, sdict2):
    match = pattern.match(vardict, sdict, pred_rule, expr)

    assert match is correct_match
    assert sdict == sdict2


@pytest.mark.parametrize(
    ('pattern, target, correct_result, sdict2'),
    [
        (   # types do not match
            CommAssoc('*', (sa, sc)),
            Container('*', (i2, sa)),
            False,
            dict(),
        ),
        (   # names do not match
            CommAssoc('*', (sa, sc)),
            CommAssoc('+', (i2, sa)),
            False,
            dict(),
        ),
        (   # names do not match
            CommAssoc('*', (sa, sc)),
            CommAssoc('*', (i2, sa)),
            True,
            {sc: i2},
        ),
        (   # match of sub-expressions not made
            CommAssoc('*', (sa, sc)),
            CommAssoc('*', (sa, sa)),
            False,
            dict(),
        ),
    ],
)
def test_commassoc_match(pattern, target, correct_result, sdict2):
    subdict = dict()

    match = pattern.match(vardict, subdict, pred_rule, target)

    assert match is correct_result
    assert subdict == sdict2

def test_isspecialsymbol():
    sp0 = Symbol('__special')
    num = Number(0)
    not_sp = Symbol('_2special')
    short = Symbol('_')

    assert Symbol.isspecialsymbol(sp0) is True
    assert Symbol.isspecialsymbol(num) is False
    assert Symbol.isspecialsymbol(short) is False
    assert Symbol.isspecialsymbol(not_sp) is False


def test_exprbase_attributes():
    expr = ExprBase()

    assert expr.name == ""
    assert expr.value == None
    assert expr.items == None
    assert expr.lbp == 0
    assert expr.rbp == 0


def test_expression_setattr():
    expr = ExprBase()

    with pytest.raises(AttributeError) as error0:
        expr.name = 'abc'
    with pytest.raises(AttributeError) as error1:
        expr.value = 7
    with pytest.raises(AttributeError) as error2:
        expr.items = ()
    expr.rbp = 100
    expr.lbp = 101

    assert "This object should not be mutated" in str(error0.value)
    assert "This object should not be mutated" in str(error1.value)
    assert "This object should not be mutated" in str(error2.value)
    assert expr.name == ''
    assert expr.value is None
    assert expr.items is None
    assert expr.rbp == 100
    assert expr.lbp == 101


def test_expression_base():
    expr = ExprBase()

    assert repr(expr) == " <EXPR> "
    assert bool(expr) is True


def test_null():
    null = Null()

    assert repr(null) == " <NULL> "
    assert bool(null) is False
    assert null == Null()

def test_end():
    end = End()

    assert end.name == "end"
    assert repr(end) == " <END> "


def test_number():
    num = Number(5.7)

    assert num.value  == 5.7
    assert repr(num) == "5.7"


def test_symbol():
    sym = Symbol("a")

    assert sym.name ==  "a"
    assert repr(sym) ==  "a"
    assert Symbol("true") ==  true
    assert Symbol("false") ==  false

 
def test_namedseq():
    f = Container("f", (Symbol("a"), Number(5)), 18, 19)

    assert f.name == "f"
    assert f.items == (Symbol("a"), Number(5))
    assert f.lbp == 18
    assert f.rbp == 19
    assert len(f) == 2
    assert f[1] == Number(5)
    assert repr(f) == "f(a, 5)"


def test_append_item():
    f = Container("f", (sa,))

    f._append_item(r4)

    assert f == Container("f", (Symbol("a"), Number(4.0)))


def test_bind_right():
    f = Container("^", (sa,), 200, 300)

    f._bind_right(Container("**", (sc, sd), 0, 0))

    assert f == Container("^", (sa, Container("**", (sc, sd))))
    assert f.rbp == 0
    assert f.lbp == 200


def test_bind_left():
    f = Container("^", (sa,), 200, 300)

    f._bind_left(Container("**", (sc, sd), 0, 0))

    assert f == Container("^", (Container("**", (sc, sd)), sa))
    assert f.rbp == 300
    assert f.lbp == 0


