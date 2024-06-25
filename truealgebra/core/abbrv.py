from truealgebra.core.rules import Rule as Ru
from truealgebra.core.rules import Rules as Rs
from truealgebra.core.rules import RulesBU as RsBU
from truealgebra.core.rules import JustOne as JO
from truealgebra.core.rules import JustOneBU as JOBU
from truealgebra.core.naturalrules import NaturalRule as NR
from truealgebra.core.naturalrules import HalfNaturalRule as HNR

from truealgebra.core.expression import ExprBase as EB
from truealgebra.core.expression import Symbol as Sy
from truealgebra.core.expression import Number as Nu
from truealgebra.core.expression import Container as Co
from truealgebra.core.expression import Restricted as Re
from truealgebra.core.expression import Assign as Asn
from truealgebra.core.expression import CommAssoc as CA


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
