from truealgebra.core.unparse import (
    ReadableHandlerBase, UnparseOperator, UnparseBodiedFunct, UnparseNumber,
    UnparseFunctForm, UnparseSymbol, UnparseNull, ReadableString,
    UnparseMultiExprs,
)
from truealgebra.common.unparse import (
    UnparseCommAssocPlus, UnparseCommAssocStar,
)
from truealgebra.core.expressions import (isNumber, Number)
from truealgebra.core.rules import (Rule)
import sympy

from IPython import embed

class SympyReadableString(ReadableString):
    def does_num_need_paren(self, item):
        return (
            isNumber(item)
            and(
                isinstance(item.value, sympy.Mul)
                or isinstance(item.value, sympy.Add)
                or isinstance(item.value, sympy.Pow)
            )
        )
    

unparse = SympyReadableString(
    UnparseNumber,
    UnparseCommAssocPlus,
    UnparseCommAssocStar,
    UnparseOperator,
    UnparseBodiedFunct,
    UnparseFunctForm,
    UnparseSymbol,
    UnparseNull,
    UnparseMultiExprs,
)

class ApplyN(Rule):
    def __init__(self, *args, digits=None, **kwargs):
        self.digits = digits
        super().__init__(*args, **kwargs)

    def predicate(self, expr):
        return isNumber(expr) and isinstance(expr.value, sympy.Float)

    def body(self, expr):
        if self.digits is None:
            return Number(sympy.N(expr.value))
        else:
            return Number(sympy.N(expr.value, self.digits))

    bottomup = True


def makefloatunparse(digits):
    applyn = ApplyN(digits=digits)
    def floatunparse(expr):
#       xxx = 100; embed()
        expr = applyn(expr)
#       xxx = 101; embed()
        return unparse(expr)
    return floatunparse


floatunparse4 = makefloatunparse(4)
