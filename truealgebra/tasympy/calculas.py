from truealgebra.core.rules import Rule
from truealgebra.core.expressions import isContainer
from truealgebra.tasympy.tatosympy import tatosympy

class Diff(Rule):
    def predicate(self, expr):
        return isContainer(expr, 'D', 2) and isSymbol(expr[0])

    def body(self, expr):
        sy_expr = tatosympy(expr[1])


