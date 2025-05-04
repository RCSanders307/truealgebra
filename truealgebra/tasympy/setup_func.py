import sympy

from truealgebra.core.parse import Parse, RestrictedChild, AssignChild
from truealgebra.core.rules import (RecursiveChild, RecursiveParentBU)
from truealgebra.core.settings import settings
from truealgebra.core.expressions import (
    isContainer, isSymbol, isNumber,  Number, CommAssoc,
)
from truealgebra.common.commonsettings import commonsettings

from .evalnum import evalnum, evalnumbu, num0, num1, neg1
from .utility import snum
from .unparse import unparse


class MakeRational(RecursiveChild):
    def predicate(self, expr):
        return (
            isContainer(expr, '/', 2)
            and isNumber(expr[0])
            and isinstance(expr[0].value, sympy.core.numbers.Integer)
            and isNumber(expr[1])
            and isinstance(expr[1].value, sympy.core.numbers.Integer)
        )

    def body(self, expr):
        return Number(sympy.Rational(expr[0].value, expr[1].value))


class PlusComplement(RecursiveChild):
    def predicate(self, expr):
        return isContainer(expr, 'plus')

    def body(self, expr):
        return CommAssoc('+', expr.items)


class StarComplement(RecursiveChild):
    def predicate(self, expr):
        return isContainer(expr, 'star')

    def body(self, expr):
        return CommAssoc('*', expr.items)


class SpecialSymbols(RecursiveChild):
    specialsymbols = {
        'I': sympy.I,
        'pi': sympy.pi,
        'E': sympy.E,
        'EulerGamma': sympy.EulerGamma,
        'oo': sympy.oo
    }

    def predicate(self, expr):
        return isSymbol(expr) and expr.name in self.specialsymbols

    def body(self, expr):
        return Number(self.specialsymbols[expr.name])


class MakeFloat:
    accuracy = 10

    def set_accuracy(self, num):
        self.accuracy = num

    def __call__(self, value):
        return sympy.core.numbers.Float(value, self.accuracy)


makefloat = MakeFloat()


def tasympy_setup_func():
    commonsettings.evalnum = evalnum
    commonsettings.evalnumbu = evalnumbu
    commonsettings.num0 = num0
    commonsettings.num1 = num1
    commonsettings.neg1 = neg1

    settings.parse = Parse(postrule=RecursiveParentBU(
        RestrictedChild, AssignChild, PlusComplement, StarComplement,
        SpecialSymbols, MakeRational,
    ))

#   settings.unparse = None
    settings.float_class = snum.rawfloat
#   settings.float_class = snum.float
    settings.integer_class = sympy.core.numbers.Integer
#   settings.integer_class = snum.rawinteger
    settings.unparse = unparse
