from truealgebra.core.parse import Parse
from truealgebra.core.settings import settings

import sympy


class MakeFloat:
    accuracy = 10

    def set_accuracy(self, num):
        self.accuracy = num

    def __call__(self, value):
        return sympy.core.numbers.Float(value, self.accuracy)

makefloat = MakeFloat()

def tasympy_setup_func():
#   commonsettings.evalnum = evalnum
#   commonsettings.evalnumbu = evalnumbu
#   commonsettings.num0 = num0
#   commonsettings.num1 = num1
#   commonsettings.neg1 = neg1
    
    settings.parse = Parse()
    settings.unparse = None

    settings.float_class = makefloat
    settings.integer_class = sympy.core.numbers.Integer

