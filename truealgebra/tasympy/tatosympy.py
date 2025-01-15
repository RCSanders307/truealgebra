from truealgebra.tasympy.evalnum import definedfunction_dict

from truealgebra.core.expressions import (
    Symbol, isSymbol, isCommAssoc, isNumber, isContainer,
)
from truealgebra.core.translate import TranslateParent, TranslateChild

import sympy

from IPython import embed

# This class will probaly be deleted
class OneToOneSymbolMap:
    def __init__(self):
        self.tomap = dict()
        self.frommap = dict()
        self.num = 0

    def add_tasy(self, sy):
        if isSymbol(sy) and sy not in self.tomap:
            self.num += 1
            sympy_sy = sympy.symbols('sy' + str(self.num))
            self.tomap[sy] = sympy_sy
            self.frommap[sympy_sy] = sy
            

# =============================

class TAToSympy(TranslateParent):
    def __init__(self, *child_classes, **kwargs):
#       self.symbolmap = kwargs['symbolmap']
#       self.symbolmap = OneToOneSymbolMap()

        super().__init__(*child_classes, **kwargs)


class StarTranslate(TranslateChild):
    def predicate(self, expr):
        return isCommAssoc(expr, '*')

    def body(self, expr):
        newunits = list()
        for item in expr.items:
            newunits.append(self.parent(item))
        return sympy.Mul(*newunits)


class PlusTranslate(TranslateChild):
    def predicate(self, expr):
        return isCommAssoc(expr, '+')

    def body(self, expr):
        newunits = list()
        for item in expr.items:
            newunits.append(self.parent(item))
        return sympy.Add(*newunits)


class DivTranslate(TranslateChild):
    def predicate(self, expr):
        return isContainer(expr, '/', 2)

    def body(self, expr):
        return sympy.Mul(
            self.parent(expr[0]),
            sympy.Pow(self.parent(expr[1]), sympy.core.numbers.NegativeOne())
        )


class NegTranslate(TranslateChild):
    def predicate(self, expr):
        return isContainer(expr, '-', 1)

    def body(self, expr):
        return sympy.Mul(
            sympy.core.numbers.NegativeOne(),
            self.parent(expr[0]),
        )


class SubTranslate(TranslateChild):
    def predicate(self, expr):
        return isContainer(expr, '-', 2)

    def body(self, expr):
        return sympy.Add(
            self.parent(expr[0]),
            sympy.Mul(
                sympy.core.numbers.NegativeOne(),
                self.parent(expr[1]),
            ),
        )


class SymbolTranslate(TranslateChild):
    def predicate(self, expr):
        return isSymbol(expr)

    def body(self, expr):
        return sympy.symbols(expr.name)


class NumberTranslate(TranslateChild):
    def predicate(self, expr):
        return isNumber(expr)

    def body(self, expr):
        return expr.value


class DefinedFunctionTranslate(TranslateChild):
    def predicate(self, expr):
        return isContainer(expr) and expr.name in definedfunction_dict

    def body(self, expr):
        newunits = list()
        for item in expr.items:
            newunits.append(self.parent(item))
        return definedfunction_dict[expr.name](*newunits)


class UndefinedFunctionTranslate(TranslateChild):
    def predicate(self, expr):
        return isContainer(expr)

    def body(self, expr):
        newunits = list()
        for item in expr.items:
            newunits.append(self.parent(item))
        return sympy.Function(expr.name)(*newunits)


tatosympy = TAToSympy(
    StarTranslate,
    PlusTranslate,
    NegTranslate,
    SubTranslate,
    DivTranslate,
    SymbolTranslate,
    NumberTranslate,
    DefinedFunctionTranslate,
    UndefinedFunctionTranslate, 
)


