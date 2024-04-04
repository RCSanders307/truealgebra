from truealgebra.core.rule import (
    HalfNaturalRule, Rules, RulesBU, JustOne, JustOneBU
)
from truealgebra.core.rulebase import RuleBase
from truealgebra.core.expression import Number, Container, null, true
from truealgebra.core.err import ta_logger
from truealgebra.core.abbrv import isCo, isNu, isCA

from truealgebra.std.predicate import isfraction, iscomplex, isnumber
from truealgebra.std.std_settings import parse
from truealgebra.std.eval_commassoc import multiply, add

import math
import cmath
from fractions import Fraction

def eval_logger(msg):
    ta_logger.log('Numerical Evaluation Error\n' + msg)

# Operator Functions
# ==================
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


def clean(n0):
    if isinstance(n0, Fraction) and n0.denominator == 1:
        return n0.numerator
    elif isinstance(n0, complex) and n0.imag == 0:
        return n0.real
    else:
        return n0


# Class MathFunctions
# ===================
class MathFunctions:
    def __init__(self, pwr, div, sub, neg, mul, add):
        self._pwr = pwr
        self._div = div
        self._sub = sub
        self._neg = neg
        self._mul = mul
        self._add = add

    @property
    def pwr(self):
        return self._pwr

    @pwr.setter
    def set_pwr(self, func):
        self._pwr = func

    @property
    def div(self):
        return self._div

    @div.setter
    def set_div(self, func):
        self._div = func

    @property
    def sub(self):
        return self._sub

    @sub.setter
    def set_sub(self, func):
        self._sub = func

    @property
    def neg(self):
        return self._neg

    @neg.setter
    def set_neg(self, func):
        self._neg = func

    @property
    def mul(self):
        return self._mul

    @mul.setter
    def set_mul(self, func):
        self._mul = func

    @property
    def add(self):
        return self._add

    @add.setter
    def set_add(self, func):
        self._add = func

math = MathFunctions(
    lambda n0, n1: clean(power_function(n0, n1)),
    lambda n0, n1: clean(divide_function(n0, n1)),
    lambda n0, n1: clean(subtract_function(n0, n1)),
    lambda n0: clean(negative_function(n0)),
    lambda n0, n1: clean(multiply_function(n0, n1)),
    lambda n0, n1: clean(add_function(n0, n1)),
)

# Clean Rules
# ===========
class CleanFraction(HalfNaturalRule):
    parse = parse
    predicate_rule = isfraction
    var_defn = ' @fract | isfraction(fract) '
    pattern = ' fract '

    def body(self, expr, var):
        if var.fract.value.denominator == 1:
            return Number(var.fract.value.numerator)
        else:
            return expr


class CleanComplex(HalfNaturalRule):
    parse = parse
    predicate_rule = iscomplex
    var_defn = ' @cnum | iscomplex(cnum) '
    pattern = ' cnum '

    def body(self, expr, var):
        if var.cnum.value.imag == 0:
            return Number(var.cnum.value.real)
        else:
            return expr


cleanfraction = CleanFraction()
cleancomplex = CleanComplex()


# ============
# EvalMathDict
# ============
class EvalMathDictSingle(RuleBase):
    arity = 1

    def __init__(self, *args, **kwargs):
        self.namedict = kwargs['namedict']
        super().__init__(*args, **kwargs)

    def predicate(self, expr):
        return (
            isCo(expr, arity=self.arity)
            and expr.name in self.namedict
            and self.item_predicate(expr)
        )

    def body(self, expr):
        func = self.namedict[expr.name]
        try:
            return Number(self.calculation(func, expr))
        except ZeroDivisionError:
            eval_logger('Division by zero.')
            return null
        except TypeError:  # complex number
            eval_logger('Complex number cannot be handled.')
            return null
        except AttributeError:  # value eroror
            eval_logger('Number instance must have value attribute.')
            return null

    def calculation(self, func, expr):
        return clean(func(expr[0].value))

    def item_predicate(self, expr):
        for item in expr:
            if not isNu(item):
                return False
        return True


class EvalMathDictDouble(EvalMathDictSingle):
    arity = 2

    def calculation(self, func, expr):
        return clean(func(expr[0].value, expr[1].value))


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
        '-': lambda x: -x,
    }
)


evalmathdouble = EvalMathDictDouble(
    namedict={
        '**': lambda n0, n1: n0 ** n1,
        '/': lambda n0, n1: n0 / n1,
        '-': lambda n0, n1: n0 - n1,
    }
)

evalnumeric = JustOne(multiply, add, evalmathsingle, evalmathdouble)
evalnumeric_bu = JustOneBU(multiply, add, evalmathsingle, evalmathdouble)
