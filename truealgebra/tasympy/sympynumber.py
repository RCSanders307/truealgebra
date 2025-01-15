from truealgebra.core.expressions import Number
import sympy

class SympyNumbers:
    def __init__(self, accuracy=None):
        if accuracy is not None:
            self.accuracy = accuracy

    accuracy = 10

    def integer(self, string):
        return Number(sympy.core.numbers.Integer(string))

    def float(self, string, accuracy=None):
        if accuracy is None:
            return Number(sympy.core.numbers.Float(string, self.accuracy))
        else:
            return Number(sympy.core.numbers.Float(string, accuracy))
            

snum = SympyNumbers()
