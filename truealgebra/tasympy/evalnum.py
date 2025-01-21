from truealgebra.core.rules import Rule, Rules, JustOneBU, JustOne
from truealgebra.common.utility import (
    CalcCommAssoc, EvalMathDictSingle, EvalMathDictDouble,
)
from truealgebra.tasympy.utility import snum, definedfunction_dict

import sympy


num0 = snum.integer('0')
num1 = snum.integer('1')
neg1 = snum.integer('-1')


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


# Evaluation Rules
# ================

#       'log10': lambda x: sympy.log(x, 10),
#       '-': negative_function,





multiply= CalcCommAssoc(name='*', ident=num1, func=multiply_function)
add = CalcCommAssoc(name='+', ident=num0, func=add_function)

evalnamedfunction = EvalMathDictSingle(namedict=definedfunction_dict)

evalmathsingle = EvalMathDictSingle(
    namedict={
        'log10': lambda x: sympy.log(x, 10),
        '-': negative_function,
    }
)

evalmathdouble = EvalMathDictDouble(
    namedict={
        '**': power_function,
        '/': divide_function,
        '-': subtract_function,
        'log': sympy.log,
    }
)

evalnum = JustOne(
    multiply, add, evalnamedfunction, evalmathsingle, evalmathdouble
)

evalnumbu = JustOneBU(
    multiply, add, evalnamedfunction, evalmathsingle, evalmathdouble
)
