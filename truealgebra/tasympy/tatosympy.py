from truealgebra.tasympy.utility import definedfunction_dict
from truealgebra.core.expressions import (
    Symbol, isSymbol, isCommAssoc, isNumber, isContainer,
)
from truealgebra.core.translate import ParentTranslate, ChildTranslate
import sympy

from IPython import embed


class StarTranslate(ChildTranslate):
    def predicate(self, expr):
        return isCommAssoc(expr, '*')

    def body(self, expr):
        newunits = list()
        for item in expr.items:
            newunits.append(self.parent(item))
        return sympy.Mul(*newunits)


class PlusTranslate(ChildTranslate):
    def predicate(self, expr):
        return isCommAssoc(expr, '+')

    def body(self, expr):
        newunits = list()
        for item in expr.items:
            newunits.append(self.parent(item))
        return sympy.Add(*newunits)


class PwrTranslate(ChildTranslate):
    def predicate(self, expr):
        return isContainer(expr, '**', 2)

    def body(self, expr):
        newbase = self.parent(expr[0])
        newexp = self.parent(expr[1])
        return sympy.Pow(newbase, newexp)


class DivTranslate(ChildTranslate):
    def predicate(self, expr):
        return isContainer(expr, '/', 2)

    def body(self, expr):
        return sympy.Mul(
            self.parent(expr[0]),
            sympy.Pow(self.parent(expr[1]), sympy.core.numbers.NegativeOne())
        )


class NegTranslate(ChildTranslate):
    def predicate(self, expr):
        return isContainer(expr, '-', 1)

    def body(self, expr):
        return sympy.Mul(
            sympy.core.numbers.NegativeOne(),
            self.parent(expr[0]),
        )


class SubTranslate(ChildTranslate):
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


class SymbolTranslate(ChildTranslate):
    def predicate(self, expr):
        return isSymbol(expr)

    def body(self, expr):
        return sympy.symbols(expr.name)


class NumberTranslate(ChildTranslate):
    def predicate(self, expr):
        return isNumber(expr)

    def body(self, expr):
        return expr.value


class DefinedFunctionTranslate(ChildTranslate):
    def predicate(self, expr):
        return isContainer(expr) and expr.name in definedfunction_dict

    def body(self, expr):
        newunits = list()
        for item in expr.items:
            newunits.append(self.parent(item))
        return definedfunction_dict[expr.name](*newunits)


class UndefinedFunctionTranslate(ChildTranslate):
    def predicate(self, expr):
        return isContainer(expr)

    def body(self, expr):
        newunits = list()
        for item in expr.items:
            newunits.append(self.parent(item))
        return sympy.Function(expr.name)(*newunits)


tatosympy = ParentTranslate(
    StarTranslate,
    PlusTranslate,
    PwrTranslate,
    NegTranslate,
    SubTranslate,
    DivTranslate,
    SymbolTranslate,
    NumberTranslate,
    DefinedFunctionTranslate,
    UndefinedFunctionTranslate, 
)


