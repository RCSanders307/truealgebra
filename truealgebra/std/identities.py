from truealgebra.core.rule import NaturalRule
from truealgebra.std.std_settings import parse


trig_ident0 = NaturalRule(
    parse=parse,
    var_defn=' forall(ex0) ',
    pattern=' sin(ex0) ** 2 + cos(ex0) ** 2 ',
    outcome=' 1 '
)
