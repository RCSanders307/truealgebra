
#First set up the settings
from truealgebra.core.settings import settings
from truealgebra.common.commonsettings import commonsettings
from truealgebra.tasympy.setup_func import tasympy_setup_func
from truealgebra.common.setup_func import common_setup_func

def setup_func():
    settings.reset()
    commonsettings.reset()
    common_setup_func()
    tasympy_setup_func()

setup_func()

#Now start the imports

from truealgebra.core.settings import settings
from truealgebra.core.frontend import FrontEnd
from truealgebra.core.expressions import (
    ExprBase, Container, Symbol, Number, CommAssoc, Restricted,
    Assign, isContainer, isSymbol, isNumber, isCommAssoc
)
from truealgebra.core.rules import (
    Rule, Rules, RulesBU, JustOne, JustOneBU, donothing_rule
)
from truealgebra.core.naturalrules import NaturalRule, HalfNaturalRule

from truealgebra.common.simplify import simplify
from truealgebra.common import utility
from truealgebra.common.utility import (
    create_frontend as common_create_frontend,
)

from .predicate import predicate_rule, predicate_rule_bu
from .evalnum import (
    num0, num1, neg1, evalnum, evalnumbu,
)
from .calculas import diff, integrate
from .utility import snum
from .unparse import unparse, floatunparse4, makefloatunparse, ApplyN

parse = settings.parse

def create_frontend(
    prerule=donothing_rule,
    postrule=donothing_rule,
):
    return common_create_frontend(
        pred_rule=predicate_rule_bu,
        prerule=prerule,
        postrule=postrule,
    )

