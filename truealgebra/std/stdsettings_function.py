"""Adjust the setting environment for the truealgebra.std (standard) package.

This module is to be executed. It modifies the setting objects in truealgebra.core.env.
This module creates no objects to be imported elsewhere.
"""
from truealgebra.core.settings import SettingsSingleton
from truealgebra.core.expressions import (
    Number, CommAssoc, Restricted, Assign, Container, null
)
from truealgebra.core.parse import Parse
from truealgebra.core.rules import Rule, JustOneBU
from truealgebra.core.err import ta_logger
from fractions import Fraction

settings = SettingsSingleton()

def eval_logger(msg):
    ta_logger.log('Numerical Evaluation Error\n' + msg)

class NegativeNumber(Rule):
    def predicate(self, expr):
        return (
            expr.name == '-'
            and isinstance(expr, Container) 
            and len(expr) == 1
            and isinstance(expr[0], Number)
            and (
                isinstance(expr[0].value, int)
                or isinstance(expr[0].value, float)
            )
        )

    def body(self, expr):
        return Number(-expr[0].value)

negativenumber = NegativeNumber()

class MakeFraction(Rule):
    def predicate(self, expr):
        return (
            expr.name == '/'
            and isinstance(expr, Container) 
            and len(expr) == 2
            and isinstance(expr[0], Number)
            and isinstance(expr[0].value, int)
            and isinstance(expr[1], Number)
            and isinstance(expr[1].value, int)
        )

    def body(self, expr):
        try:
            out = Number(Fraction(expr[0].value, expr[1].value))
        except ZeroDivisionError:
            eval_logger('Division by zero.')
            out = null
        return out

makefraction = MakeFraction()
        
parse = Parse(
    postrule=JustOneBU(negativenumber, makefraction)
)


def set_stdsettings():
    settings.reset()
    # set operator binding power dictionary
    settings.set_custom_bp("%", 0, 10)
    settings.set_custom_bp("=", 50, 50)
    settings.set_custom_bp("|", 3000, 20)
    settings.set_custom_bp("@", 0, 3000)
    settings.set_custom_bp(":=", 2000, 20)
    settings.set_custom_bp(">", 100, 100)
    settings.set_custom_bp("<", 100, 100)
    settings.set_custom_bp(">=", 100, 100)
    settings.set_custom_bp("<=", 100, 100)
    settings.set_custom_bp("!=", 100, 100)
    settings.set_custom_bp("!", 2000, 0)
    settings.set_custom_bp("/", 1100, 1100)
    settings.set_custom_bp("**", 1251, 1250)
    settings.set_custom_bp("*", 1000, 999)
    settings.set_custom_bp("+", 500, 500)
    settings.set_custom_bp("`", 1500, 200)
    settings.set_custom_bp("-", 500, 500)
    settings.set_custom_bp(":", 3001, 20)
    settings.set_custom_bp("@@", 0, 3000)

    settings.set_symbol_operators("and", 75, 75)
    settings.set_symbol_operators("or", 75, 75)
    settings.set_symbol_operators("not", 0, 70)

    settings.set_bodied_functions("D", 70)
    settings.set_bodied_functions("Intergrate", 70)
    settings.set_bodied_functions("Rule", 70)

    settings.set_infixprefix("-", 999)

    settings.set_sqrtneg1("j")

    settings.set_container_subclass("+", CommAssoc)
    settings.set_container_subclass("plus", CommAssoc)
    settings.set_container_subclass("*", CommAssoc)
    settings.set_container_subclass("star", CommAssoc)
    settings.set_container_subclass("and", CommAssoc)
    settings.set_container_subclass("or", CommAssoc)
    settings.set_container_subclass("`", Restricted)
    settings.set_container_subclass(":=", Assign)
    settings.set_container_subclass("==>", Restricted)
    settings.set_container_subclass("Rule", Restricted)

    settings.set_complement('star', '*')
    settings.set_complement('plus', '+')

    settings.set_categories('rule_names', ':=') 
    settings.set_categories('rule_names', '==>') 
    settings.set_categories('eqn_names', '=') 
    settings.set_categories('suchthat', '|') 
    settings.set_categories('suchthat', 'suchthat') 
    settings.set_categories('forall', '@') 
    settings.set_categories('forall', 'forall') 

    settings.active_parse = parse
