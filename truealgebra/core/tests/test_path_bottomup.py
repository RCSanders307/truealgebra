from truealgebra.core.expression import Symbol, Number, Container, Null
from truealgebra.core.rules import Rule

null = Null()

class PathRule(Rule):
    def predicate(self, expr):
        return isinstance(expr, Symbol)
    def body(self, expr):
        return Symbol('x')

class SymbolXRule(Rule):
    """ Convert all symbols to the symbol x. """
    def predicate(self, expr):
        return isinstance(expr, Symbol)
    def body(self, expr):
        return Symbol('x')

class Number7Rule(Rule):
    """ Convert all numbers to the number 7. """
    def predicate(self, expr):
        return isinstance(expr, Number)
    def body(self, expr):
        return Number(7)

num_5 = Number(5)
num_7 = Number(7)
sym_a = Symbol('a')
sym_x = Symbol('x')

def test_path_atoms_1():
    """Apply empty path to atom expressions.

    Number and Symbol instances are atoms.
    Applying a rule with an empty path has same output as applying the rule.
    When a path is applied to nested Containers,
    its length is reduced at each expression level.
    """
    expr3 = Container('f', (Container('f', (num_5, sym_a)),))
    expr4 = Container('f', (Container('f', (num_7, sym_a)),))
    expr5 = Container('f', (Container('f', (num_5, sym_x)),))

    out1 = Number7Rule(path=())(num_5)
    out2 = SymbolXRule(path=())(sym_a)
    out4 = Number7Rule(path=(0, 0))(expr3)
    out5 = SymbolXRule(path=(0, 1))(expr3)

    assert out1 == num_7
    assert out2 == sym_x
    assert out4 == expr4
    assert out5 == expr5

def test_path_atoms_2():
    """Errors when non-empty path to atom expressions.

    Number and Symbol instances are atoms.
    The output is ``null`` when non-empty paths are applied.
    The ``null`` occurs where the error occurs inside an expression
    """
    expr3 = Container('f', (Container('f', (num_5, sym_a)),))
    expr4 = Container('f', (Container('f', (null, sym_a)),))
    expr5 = Container('f', (Container('f', (num_5, null)),))

    out1 = Number7Rule(path=(0,))(num_5)
    out2 = SymbolXRule(path=(0,))(sym_a)
    out4 = Number7Rule(path=(0, 0, 5))(expr3)
    out5 = SymbolXRule(path=(0, 1, 7))(expr3)

    assert out1 == null
    assert out2 == null
    assert out4 == expr4
    assert out5 == expr5

def test_path():
    expr0 = Symbol('a')
    expr1 = Container('f', (expr0, expr0))
    expr2 = Container('f', (expr1, expr1))
    expr3 = Symbol('x')
    expr4 = Container('f', (expr0, expr3))
    expr5 = Container('f', (expr4, expr1))
    expr6 = Container('f', (null, expr1))
    expr7 = Container('f', (expr0, null))
    expr8 = Container('f', (expr7, expr1))

    good_rule = PathRule(path=(0, 1))
    neg_good_rule = PathRule(path=(0, -1))
    type_err_rule = PathRule(path=(0, 'one'))
    long_err_rule = PathRule(path=(0, 1, 1))
    index_err_rule = PathRule(path=(0, 7))

    assert good_rule(expr2) == expr5
    # demontrate that path is not chnaged
    assert good_rule(expr2) == expr5
    assert neg_good_rule(expr2) == expr5
    assert type_err_rule(expr2) == expr6
    assert index_err_rule(expr2) == expr6
    assert long_err_rule(expr2) == expr8
