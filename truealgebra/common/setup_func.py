from truealgebra.core.settings import settings
from truealgebra.core import setsettings
from truealgebra.core.expressions import (
    Number, CommAssoc, Restricted, Assign, Container, null
)
from truealgebra.core.rules import Rule, JustOneBU


def common_setup_func():
    # parse and unparse not set
    setsettings.set_custom_bp("%", 0, 10)
    setsettings.set_custom_bp("=", 50, 50)
    setsettings.set_custom_bp("|", 3000, 20)
    setsettings.set_custom_bp("@", 0, 3000)
    setsettings.set_custom_bp(":=", 2000, 20)
    setsettings.set_custom_bp(">", 100, 100)
    setsettings.set_custom_bp("<", 100, 100)
    setsettings.set_custom_bp(">=", 100, 100)
    setsettings.set_custom_bp("<=", 100, 100)
    setsettings.set_custom_bp("!=", 100, 100)
    setsettings.set_custom_bp("!", 2000, 0)
    setsettings.set_custom_bp("/", 1100, 1100)
    setsettings.set_custom_bp("**", 1251, 1250)
    setsettings.set_custom_bp("*", 1000, 999)
    setsettings.set_custom_bp("+", 500, 500)
    setsettings.set_custom_bp("`", 1500, 200)
    setsettings.set_custom_bp("-", 500, 500)
    setsettings.set_custom_bp(":", 3001, 20)
    setsettings.set_custom_bp("@@", 0, 3000)

    setsettings.set_symbol_operators("and", 75, 75)
    setsettings.set_symbol_operators("or", 75, 75)
    setsettings.set_symbol_operators("not", 0, 70)

    setsettings.set_bodied_functions("D", 70)
    setsettings.set_bodied_functions("Intergrate", 70)
    setsettings.set_bodied_functions("Rule", 70)

    setsettings.set_infixprefix("-", 999)


    setsettings.set_container_subclass("+", CommAssoc)
    setsettings.set_container_subclass("plus", CommAssoc)
    setsettings.set_container_subclass("*", CommAssoc)
    setsettings.set_container_subclass("star", CommAssoc)
    setsettings.set_container_subclass("and", CommAssoc)
    setsettings.set_container_subclass("or", CommAssoc)
    setsettings.set_container_subclass("`", Restricted)
    setsettings.set_container_subclass(":=", Assign)
    setsettings.set_container_subclass("==>", Restricted)
    setsettings.set_container_subclass("Rule", Restricted)

    setsettings.set_categories('rule_names', ':=') 
    setsettings.set_categories('rule_names', '==>') 
    setsettings.set_categories('eqn_names', '=') 
    setsettings.set_categories('suchthat', '|') 
    setsettings.set_categories('suchthat', 'suchthat') 
    setsettings.set_categories('forall', '@') 
    setsettings.set_categories('forall', 'forall') 


