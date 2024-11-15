from truealgebra.std.stdsettings_function import set_stdsettings


set_stdsettings()

from truealgebra.common.commonsettings import commonsettings
from truealgebra.std.evalnum import (
    evalnum, evalnumbu, add, multiply, evalmathsingle, evalmathdouble,
    num0, num1
)

commonsettings.evalnum = evalnum
commonsettings.evalnumbu = evalnumbu
commonsettings.num0 = num0
commonsettings.num1 = num1
commonsettings.add = add
commonsettings.multiply = multiply
commonsettings.evalmathsingle = evalmathsingle
commonsettings.evalmathdouble = evalmathdouble

