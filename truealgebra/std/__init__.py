# std stands for standard. Basis for CAS that depends only on python packages that come standard.

import truealgebra.std.setup
from truealgebra.core.settings import settings
from truealgebra.core.frontend import FrontEnd
from truealgebra.core.expressions import (
    ExprBase, Container, Symbol, Number, CommAssoc, Restricted,
    Assign, isContainer, isSymbol, isNumber, isCommAssoc
)
from truealgebra.core.rules import Rule, Rules, RulesBU, JustOne, JustOneBU
from truealgebra.core.naturalrules import NaturalRule, HalfNaturalRule
from truealgebra.std.predicate import (
    isnumber, iscomplex, isreal, isinteger, isfraction, isfloat,
    if_, greaterthan, greaterthanequal,
    lessthan, lessthanequal,
    logic_rules, number_type_rules, comparison_rules,
    predicate_rule, predicate_rule_bu, if_rules
)
from truealgebra.std.evalnum import (
    num0, num1, neg1, evalnum, evalnumbu,
)
from truealgebra.std.eqnmath import eqnmath, eqnflip
from truealgebra.common.simplify import simplify


from truealgebra.std.unparse import alg_unparse
parse = settings.parse

frontend = FrontEnd(
    default_rule=RulesBU(evalnum, predicate_rule,)
)
