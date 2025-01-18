from truealgebra.core.expressions import (
    Number, Container, Symbol
)
from truealgebra.core.translate import ParentTranslate, ChildTranslate
from truealgebra.common.utility import create_starCA, create_plusCA
from truealgebra.tasympy.utility import reversed_definedfunction_dict

#class SympyToTA(ParentTranslate):
#   def __init__(self, *child_classes, **kwargs):
#       self.symbolmap = kwargs['symbolmap']

#       super().__init__(*child_classes, **kwargs)



class MulTranslate(ChildTranslate):
    def predicate(self, expr):
        return expr.is_Mul

    def body(self, expr):
        items = list()
        for arg in expr.args:
            items.append(self.parent(arg))

        return create_starCA(items)


class AddTranslate(ChildTranslate):
    def predicate(self, expr):
        return expr.is_Add

    def body(self, expr):
        items = list()
        for arg in expr.args:
            items.append(self.parent(arg))

        return create_plusCA(items)


class PowTranslate(ChildTranslate):
    def predicate(self, expr):
        return expr.is_Pow

    def body(self, expr):
        base = self.parent(expr.args[0])
        exp = self.parent(expr.args[1])

        return Container('**', (base, exp))


class SymbolTranslate(ChildTranslate):
    def predicate(self, expr):
        return expr.is_Symbol

    def body(self, expr):
        return Symbol(expr.name)


class NumberTranslate(ChildTranslate):
    def predicate(self, expr):
        return expr.is_number

    def body(self, expr):
        return Number(expr)


class DefinedFunctionTranslate(ChildTranslate):
    def predicate(self, expr):
        return type(expr) in reversed_definedfunction_dict

    def body(self, expr):
        items = list()
        for arg in expr.args:
            items.append(self.parent(arg))
        return Container(reversed_definedfunction_dict[type(expr)],  items)


class FunctionTranslate(ChildTranslate):
    def predicate(self, expr):
        return expr.is_Function

    def body(self, expr):
        items = list()
        for arg in expr.args:
            items.append(self.parent(arg))
        return Container(expr.name,  items)


sympytota = ParentTranslate(
    MulTranslate,
    AddTranslate,
    PowTranslate,
    SymbolTranslate,
    NumberTranslate,
    DefinedFunctionTranslate,
    FunctionTranslate,
)
