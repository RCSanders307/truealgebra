#import truealgebra.std.settings
from truealgebra.std.std_settings import parse, set_stdsettings

set_stdsettings()

from truealgebra.core.frontend import FrontEnd
from truealgebra.core.expression import (
    ExprBase, Container, Symbol, Number,
)
from truealgebra.core.unparse import unparse

from truealgebra.core.rule import (
    Rules, RulesBU, JustOne, JustOneBU, NaturalRule, HalfNaturalRule,
)
from truealgebra.std.predicate import (
    isnumber, iscomplex, isreal, isinteger, isfraction, isfloat,
    if_, greaterthan, greaterthanequal,
    lessthan, lessthanequal, 
    logic_rules, number_type_rules, comparison_rules,
    predicate_rule, predicate_rule_bu, if_rules
)
from truealgebra.std.eval import (
    add, multiply, math, evalmathsingle, evalmathdouble,
    evalnumeric, evalnumeric_bu, clean
)

from truealgebra.std.eqnmath import eqnmath, eqnflip
from truealgebra.std.makeforms import toform0

#ExprBase.settings = parse.settings
ExprBase.set_unparse(unparse)

frontend = FrontEnd(
#   assign_name = ":=",
#   rule_name = "==>",
#   complete_rule_name = "Rule",
    parse=parse,
    default_rule=
        RulesBU(
            evalnumeric,
            predicate_rule,
#           clean,
    ))
