from truealgebra.core.rules import (
    RuleBase, Rule, Rules, RulesBU, JustOne, JustOneBU
)
from truealgebra.core.naturalrules import (
    NaturalRule, HalfNaturalRule
)
from truealgebra.core.expressions import (
    ExprBase, Symbol, Number, Container, Restricted, Assign, CommAssoc, null
)

EB = ExprBase
Sy = Symbol
Nu = Number
Co = Container
Re = Restricted
Asn = Assign
CA = CommAssoc

RB = RuleBase
Ru = Rule
Rs = Rules
RsBU = RulesBU
JO = JustOne
JOBU = JustOneBU
NR = NaturalRule
HNR = HalfNaturalRule


def isNu(expr):
    return isinstance(expr, Nu)


def isCo(expr, name=None, arity=None):
    if not isinstance(expr, Co):
        return False

    if name is None:
        name_ok = True
    else:
        name_ok = expr.name == name
    if arity is None:
        arity_ok = True
    else:
        arity_ok = (len(expr) == arity)

    return name_ok and arity_ok


def isCA(expr, name=None, arity=None):
    if not isinstance(expr, CA):
        return False

    if name is None:
        name_ok = True
    else:
        name_ok = expr.name == name
    if arity is None:
        arity_ok = True
    else:
        arity_ok = (len(expr) == arity)

    return name_ok and arity_ok


num0 = Nu(0)
num1 = Nu(1)
