from truealgebra.core.naturalrules import NaturalRule
#from truealgebra.core.settings import parse

from truealgebra.core.settings import settings


trig_ident0 = NaturalRule(
    vardict=' forall(ex0) ',
    pattern=' sin(ex0) ** 2 + cos(ex0) ** 2 ',
    outcome=' 1 '
)


