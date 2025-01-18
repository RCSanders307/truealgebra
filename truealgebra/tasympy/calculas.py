from truealgebra.core.rules import Rule
from truealgebra.core.expressions import isContainer, isSymbol
from truealgebra.tasympy.tatosympy import tatosympy
from truealgebra.tasympy.sympytota import sympytota

import sympy
from IPython import embed

class Diff(Rule):
    def predicate(self, expr):
        return isContainer(expr, 'D', 2) and isSymbol(expr[0])

    def body(self, expr):
        sy_expr = tatosympy(expr[1])
        sy_var = tatosympy(expr[0])

        sy_out = sympy.diff(sy_expr, sy_var)
        return sympytota(sy_out)

diff = Diff()

class Integrate(Rule):
    def predicate(self, expr):
        return isContainer(expr, 'I', 2) and isSymbol(expr[0])

    def body(self, expr):
        sy_expr = tatosympy(expr[1])
        sy_var = tatosympy(expr[0])

        sy_out = sympy.integrate(sy_expr, sy_var)
        return sympytota(sy_out)

integrate = Integrate()
