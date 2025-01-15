from truealgebra.core.translate import TranslateParent, TranslateChild
from truealgebra.common.utility import create_starCA
from truealgebra.tasympy.evalnum import reverse_dict

#class SympyToTA(TranslateParent):
#   def __init__(self, *child_classes, **kwargs):
#       self.symbolmap = kwargs['symbolmap']

#       super().__init__(*child_classes, **kwargs)



class MulTranslate(TranslateChild):
    def predicate(self, expr):
        return expr.is_Mul

    def body(self, expr):
        items = list()
        for arg in expr.args:
            items.append(self.parent(arg))

        return create_starCA(items)


class AddTranslate(TranslateChild):
    def predicate(self, expr):
        return expr.is_Add

    def body(self, expr):
        items = list()
        for arg in expr.args:
            items.append(self.parent(arg))

        return create_plus(items)


class SymbolTranslate(TranslateChild):
    def predicate(self, expr):
        return expr.is_Symbol

    def body(self, expr):
        return self.Symbol(expr.name)


class NumberTranslate(TranslateChild):
    def predicate(self, expr):
        return expr.is_number

    def body(self, expr):
        return Number(expr)


class DefinedFunctionTranslate(TranslateChild):
    def predicate(self, expr):
        return expr.is_DefinedFunction

    def body(self, expr):
        items = list()
        for arg in expr.args:
            items.append(self.parent(arg))
        return Container(reverse_dict[type(expr)],  items)


class FunctionTranslate(TranslateChild):
    def predicate(self, expr):
        return expr.is_Function

    def body(self, expr):
        items = list()
        for arg in expr.args:
            items.append(self.parent(arg))
        return Container(expr.name,  items)


sympytota = TranslateParent(
    MulTranslate,
    AddTranslate,
    SymbolTranslate,
    NumberTranslate,
    DefinedFunctionTranslate,
    FunctionTranslate,
)
