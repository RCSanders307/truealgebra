import truealgebra.std.set_stdsettings
from truealgebra.core.settings import settings
from truealgebra.core.frontend import FrontEnd
from truealgebra.core.expression import (
    ExprBase, Container, Symbol, Number,
)
from truealgebra.core.unparse import unparse

from truealgebra.core.rules import Rule, Rules, RulesBU, JustOne, JustOneBU
from truealgebra.core.naturalrules import NaturalRule, HalfNaturalRule
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

ExprBase.set_unparse(unparse)

parse = settings.active_parse

frontend = FrontEnd(
    parse=parse,
    default_rule=RulesBU(evalnumeric, predicate_rule,)
)
