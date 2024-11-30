from truealgebra.core.parse import Parse
from truealgebra.core.settings import settings
from truealgebra.core.rules import Rule, JustOneBU
from truealgebra.core.expressions import Number, Container

from truealgebra.common.commonsettings import commonsettings
from truealgebra.std.evalnum import evalnum, evalnumbu, num0, num1, neg1
from truealgebra.core.err import ta_logger
from fractions import Fraction

def set_commonsettings():
    commonsettings.evalnum = evalnum
    commonsettings.evalnumbu = evalnumbu
    commonsettings.num0 = num0
    commonsettings.num1 = num1
    commonsettings.neg1 = neg1
    


def eval_logger(msg):
    ta_logger.log('Numerical Evaluation Error\n' + msg)

class NegativeNumber(Rule):
    def predicate(self, expr):
        return (
            expr.name == '-'
            and isinstance(expr, Container) 
            and len(expr) == 1
            and isinstance(expr[0], Number)
            and (
                isinstance(expr[0].value, int)
                or isinstance(expr[0].value, float)
            )
        )

    def body(self, expr):
        return Number(-expr[0].value)

negativenumber = NegativeNumber()

class MakeFraction(Rule):
    def predicate(self, expr):
        return (
            expr.name == '/'
            and isinstance(expr, Container) 
            and len(expr) == 2
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

makefraction = MakeFraction()
        
parse = Parse(
    postrule=JustOneBU(negativenumber, makefraction)
)

def set_parse():
    settings.parse = parse
