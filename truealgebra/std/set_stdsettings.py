from truealgebra.std.stdsettings_function import set_stdsettings


set_stdsettings()

from truealgebra.common.commonsettings import commonsettings
from truealgebra.std.evalnum import evalnum, evalnumbu, num0, num1

commonsettings.evalnum = evalnum
commonsettings.evalnumbu = evalnumbu
commonsettings.num0 = num0
commonsettings.num1 = num1

