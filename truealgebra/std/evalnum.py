from truealgebra.core.rules import Rule, Rules, RulesBU, JustOne
from truealgebra.core.expressions import Number, null, isNumber, isContainer
from truealgebra.core.err import ta_logger

from truealgebra.common.utility import (
    CalcCommAssoc, 
    EvalMathDictSingle, EvalMathDictDouble,
)

import math
import cmath
from fractions import Fraction


# =========================
# Python Operator Functions
# =========================
def power_function(n0, n1):
    if isinstance(n0, int) and isinstance(n1, int) and n1 < 0:
        return Fraction(1, n0 ** - n1)
    else:
        return n0 ** n1


def divide_function(n0, n1):
    if isinstance(n0, int) and isinstance(n1, int):
       return Fraction(n0, n1)
    else:
        return n0 / n1


def subtract_function(n0, n1):
    return n0 - n1


def negative_function(n0):
    return - n0


def multiply_function(n0, n1):
    return n0 * n1


def add_function(n0, n1):
    return n0 + n1





# Clean Rules
# ===========
class CleanFraction(Rule):
    def predicate(self, expr):
        return isNumber(expr) and isinstance(expr.value, Fraction)

    def body(self, expr):
        if expr.value.denominator == 1:
            return Number(expr.value.numerator)
        else:
            return expr


class CleanComplex(Rule):
    def predicate(self, expr):
        return isNumber(expr) and isinstance(expr.value, complex)

    def body(self, expr):
        if expr.value.imag == 0:
            return Number(expr.value.real)
        else:
            return expr


cleanfraction = CleanFraction()
cleancomplex = CleanComplex()


# Eval Math Function Single Arity
# ===============================
evalmathsingle = EvalMathDictSingle(
    namedict={
        'sin': cmath.sin,
        'cos': cmath.cos,
        'tan': cmath.tan,
        'csc': lambda x: 1.0 / cmath.sin(x),
        'sec': lambda x: 1.0 / cmath.cos(x),
        'cot': lambda x: 1.0 / cmath.tan(x),
        'asin': cmath.asin,
        'acos': cmath.acos,
        'atan': cmath.atan,
        'acsc': lambda x: cmath.asin(1.0 / x),
        'asec': lambda x: cmath.acos(1.0 / x),
        'acot': lambda x: cmath.atan(1.0 / x),
        'exp': cmath.exp,
        'log': cmath.log,
        'log10': cmath.log10,
        'sqrt': cmath.sqrt,
        '-': negative_function,
    }
)


evalmathdouble = EvalMathDictDouble(
    namedict={
        '**': power_function,
        '/': divide_function,
        '-': subtract_function
    }
)

num0 = Number(0)
num1 = Number(1)
neg1 = Number(-1)

multiply = CalcCommAssoc(name='*', ident=num1, func=multiply_function)
add = CalcCommAssoc(name='+', ident=num0, func=add_function)

evalnum = Rules(
    JustOne(multiply, add, evalmathsingle, evalmathdouble),
    JustOne(cleanfraction, cleancomplex)
)
evalnumbu = RulesBU(
    JustOne(multiply, add, evalmathsingle, evalmathdouble),
    JustOne(cleanfraction, cleancomplex)
)
