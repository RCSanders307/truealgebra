from truealgebra.std.settings_functions import set_commonsettings, set_parse
from truealgebra.common.settings_function import set_settings
from truealgebra.core.expressions import ExprBase
from truealgebra.std.unparse import alg_unparse


set_settings()
set_parse()
set_commonsettings()
ExprBase.set_setting_str_func(alg_unparse)

#####


