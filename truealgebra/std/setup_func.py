from truealgebra.core.parse import Parse, RestrictedChild, AssignChild
from truealgebra.core.settings import settings
from truealgebra.core.rules import (
    Rule, JustOneBU,
    RecursiveChild, RecursiveParentBU,
)
from truealgebra.core.expressions import (
    Number, Container, isRestricted, isSymbol, isContainer, isNumber,
    Restricted, CommAssoc, null
)

from truealgebra.common.commonsettings import commonsettings
from truealgebra.std.evalnum import evalnum, evalnumbu, num0, num1, neg1
from truealgebra.core.err import ta_logger
from truealgebra.std.unparse import unparse
from fractions import Fraction

from IPython import embed


def eval_logger(msg):
    ta_logger.log('Numerical Evaluation Error\n' + msg)


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
        'j': complex(0, 1),
    }

    def predicate(self, expr):
        return isSymbol(expr) and expr.name in self.specialsymbols

    def body(self, expr):
        return Number(self.specialsymbols[expr.name])


class MakeFraction(RecursiveChild):
    def predicate(self, expr):
        return (
            isContainer(expr, '/', 2)
            and isinstance(expr[0], Number)
            and isinstance(expr[0].value, int)
            and isinstance(expr[1], Number)
            and isinstance(expr[1].value, int)
        )

    def body(self, expr):
        try:
            out = Number(Fraction(expr[0].value, expr[1].value))
        except ZeroDivisionError:
            eval_logger('Division by zero.')
            out = null
        return out
        


def std_setup_func():
    commonsettings.evalnum = evalnum
    commonsettings.evalnumbu = evalnumbu
    commonsettings.num0 = num0
    commonsettings.num1 = num1
    commonsettings.neg1 = neg1
    
    settings.parse = Parse(postrule=RecursiveParentBU(
        RestrictedChild, AssignChild,  PlusComplement, StarComplement,
        SpecialSymbols, MakeFraction,
    ))
    settings.unparse = unparse
