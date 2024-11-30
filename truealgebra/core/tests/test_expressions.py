import pytest

from truealgebra.core.expressions import (
    ExprBase, NullSingleton, null, Symbol, Container, CommAssoc,
    Assign, Restricted, Number, any__, true, false
)
from truealgebra.core.rules import Rule, donothing_rule

from truealgebra.core.abbrv import (
    Co, Nu, Sy, CA, Re, Asn, CA
)

from IPython import embed

# ===================
# Non pytest fixtures
# ===================

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

base_msg = 'TRUEALGEBRA ERROR!\n'

#=================================== ===================
# Test aspects of ExprBase, requres use of other objects
#=================================== ===================
def test_exprbase_mutate():
    expr = Symbol('a')
    exprb = Symbol('b')
    with pytest.raises(AttributeError) as error0:
        expr.name = 'abc'
    with pytest.raises(AttributeError) as error1:
        del expr.name
    expr.rbp = 100
    expr.lbp = 101

    assert "This object should not be mutated" in str(error0.value)
    assert "This object should not be mutated" in str(error1.value)
    assert expr != exprb
    assert expr.rbp == 100
    assert expr.lbp == 101

def test_exprbase_abstract():
    class BadClass(ExprBase):
        pass

    with pytest.raises(TypeError) as error0:
        badinstance = BadClass()

    assert (
        "Can't instantiate abstract class BadClass " +
        "with abstract methods __eq__, __hash__, apply2path, bottomup, match"
        in str(error0.value)
    )


@pytest.fixture()  # The scope has to be function
def str_func():
    str_func = ExprBase.str_func
    # Set up ends
    yield str_func
    # tear down begins
    ExprBase.str_func = None

def unparse_func(sym):
    return 'The new unparse'

# if fixture _uunparse is used in another test
# That new test mus duplicate lines 1 and 8 of the test below
def test_exprbasestr_func(str_func):
    original_str_func = str_func
    syma = Symbol('a')
    out1 = syma.__str__()
    ExprBase.set_str_func(unparse_func)
    out2 = syma.__str__()

    assert original_str_func is None
    assert out1 == 'a'
    assert out2 == 'The new unparse'


# =========
# Test null
# =========
null2 = NullSingleton()
x = Symbol('x')

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

def test_null():
    assert repr(null) == " <NULL> "


# =========
# Test path
# =========
class Test_Apply2path_Metho:d
    expr0 = Nu(3.5)
    expr0F = Co('F', (expr0,))
    expr1 = CA("comas", (Sy('a'), Sy('b')))
    expr1F = Co('F', (Sy('b'),))
    expr1FF = CA("comas", (Sy('a'), expr1F))
    expr2 = Re("'", (Nu(2.5), Sy("m")))
    expr2F = Co('F', (expr2,))

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


def test_good_path_assign():
    expr = Assign(':=', (Sy('a'), Sy('a')))
    path = (1,)
    out = expr.apply2path(path, applyF)

    assert out == Assign(':=', (Sy('a'), Co('F', (Sy('a'),))))

def test_bad_path_assign(capsys):
    expr = Assign(':=', (Sy('a'), Sy('a')))
    path = (0,)
    out = expr.apply2path(path, applyF)
    output = capsys.readouterr()

    assert out == null
    assert  "Assign 0 item closed to path" in output.out

# ==========
# Test match
# ==========
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
    Sy('c') : Co('isint', (Sy('c'),)),
    Sy('d') : Co('isint', (any__,)),
    Sy('e') : true,
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
        (Nu(0.0), dict(), Nu(0.0), True, dict()),
        (Nu(0.0), dict(), Nu(2), False, dict()),
        (Nu(0.0), dict(), Sy('a'), False, dict()),
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
        (Sy('f'), dict(),    Sy('f'), True,  dict()), # pattern equals expression
        (Sy('f'), dict(),    Nu(4.0), False, dict()), # pattern does not equal expression
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
        (Sy('c'), dict(),    Nu(2), True,  {Sy('c') : Nu(2)}), # pattern in vardict, expr not in sdict
        (Sy('c'), {Sy('c') : Nu(2)}, i3, False, {Sy('c') : Nu(2)}), # pattern in vardict and sdict, match
        (Sy('c'), {Sy('c') : Nu(2)}, Nu(2), True,  {Sy('c') : Nu(2)}), # pattern in vardict and sdict, no match
        (Sy('c'), dict(),    Nu(4.0), False,  dict()),   # pattern in vardict, 
                                               # pred_rule not satisfied
        (Sy('e'), dict(),    Nu(4.0), True,  {Sy('e') : Nu(4.0)}), # pattern in vardict, null predicate
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


# ===========
# Test Symbol
# ===========
# Include tests of Atom

def test_symbol():
    sym = Symbol("a")
    symb = Symbol("b")

    symb.rbp = 100
    symb.lbp = 101
    with pytest.raises(AttributeError) as error0:
        symb.name = 'abc'

    assert sym.name ==  "a"
    assert repr(sym) ==  "a"
    assert Symbol("true") ==  true
    assert Symbol("false") ==  false
    assert sym.lbp == 0
    assert sym.rbp == 0
    assert symb.rbp == 100
    assert symb.lbp == 101
    assert "This object should not be mutated" in str(error0.value)

def test_symbol_number_bottmup():
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


def test_number():
    num = Number(5.7)

    assert num.value  == 5.7
    assert repr(num) == "5.7"


# ==============
# Test Container
# ==============
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


def test_namedseq__eq__():
    ns = Container("sin", (Symbol("a"),))
    ns1 = Container("sin", (Symbol("a"), Symbol("b")))
    ns2 = Container("sin", (Symbol("a"),))
    le = Restricted("`", (Number(3.7), Symbol("m")))
    le2 = Restricted("`", (Number(3.5), Symbol("m")))
    le3 = Restricted("`", (Number(3.7), Symbol("m")))

    assert ns != ns1
    assert ns == ns2
    assert le != le2
    assert le == le3


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


