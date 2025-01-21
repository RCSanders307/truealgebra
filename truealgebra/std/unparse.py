from truealgebra.core.unparse import (
    ReadableHandlerBase, UnparseNumber, UnparseOperator, UnparseBodiedFunct,
    UnparseFunctForm, UnparseSymbol, UnparseNull, ReadableString
)
from truealgebra.common.unparse import (
    UnparseCommAssocPlus, UnparseCommAssocStar,
)
from truealgebra.core.expressions import (isNumber)
from fractions import Fraction


class UnparseComplexNumber(ReadableHandlerBase):
    def handle_expr(self, expr):
        if isNumber(expr) and isinstance(expr.value, complex):
            if expr.value.real == 0:
                return self.display_int_if_can(expr.value.imag) + 'j'
            else:
                if expr.value.imag < 0:
                    return (
                        self.display_int_if_can(expr.value.real)
                        + self.display_int_if_can(expr.value.imag)
                        + 'j'
                     )
                else:
                    return (
                        self.display_int_if_can(expr.value.real)
                        + '+'
                        + self.display_int_if_can(expr.value.imag)
                        + 'j'
                     )

    def display_int_if_can(self, num):
        intnum = int(num)
        if intnum == num:
            return str(intnum)
        else:
            return str(num)


class UnparseFractionNumber(ReadableHandlerBase):
    def handle_expr(self, expr):
        if isNumber(expr) and isinstance(expr.value, Fraction):
            return (
                str(expr.value.numerator)
                + '/'
                + str(expr.value.denominator)
            )


alg_unparse = ReadableString(
    UnparseComplexNumber,
    UnparseFractionNumber,
    UnparseNumber,
    UnparseCommAssocPlus,
    UnparseCommAssocStar,
    UnparseOperator,
    UnparseBodiedFunct,
    UnparseFunctForm,
    UnparseSymbol,
    UnparseNull,
)
