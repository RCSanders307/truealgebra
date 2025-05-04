from truealgebra.core.rules import Rule, JustOne, JustOneBU
from truealgebra.core.expressions import (
    Number, isNumber, isContainer, true, false
)

import sympy
#from IPython import embed

class IsNumberRule(Rule):
    def predicate(self, expr):
        return isContainer(expr, 'isnumber', 1)

    def body(self, expr):
        if isNumber(expr[0]):
            return true
        else:
            return false


isnumber_rule = IsNumberRule()


class IsInteger(Rule):
    def predicate(self, expr):
        return isContainer(expr, 'isinteger', 1) and isNumber(expr[0])

    def body(self, expr):
        if  expr[0].value.is_integer:
            return true
        else:
            return false


isinteger_rule = IsInteger()


class IsRational(Rule):
    def predicate(self, expr):
        return isContainer(expr, 'isrational', 1) and isNumber(expr[0])

    def body(self, expr):
        if expr[0].value.is_rational:
            return true
        else:
            return false


isrational_rule = IsRational()


class IsReal(Rule):
    def predicate(self, expr):
        return isContainer(expr, 'isreal', 1) and isNumber(expr[0])

    def body(self, expr):
        if expr[0].value.is_real:
            return true
        else:
            return false


isreal_rule = IsReal()


class IsComplex(Rule):
    def predicate(self, expr):
        return isContainer(expr, 'iscomplex', 1) and isNumber(expr[0])

    def body(self, expr):
        if expr[0].value.is_complex:
            return true
        else:
            return false


iscomplex_rule = IsComplex()


number_type_rules = JustOne(
    isnumber_rule, isinteger_rule, isrational_rule, isreal_rule,
    iscomplex_rule,
)


class AndRule(Rule):
    def predicate(self, expr):
        return isContainer(expr, 'and', 2)

    def body(self, expr):
        if expr[0] == false:
            return false
        elif expr[1] == false:
            return false
        elif expr[0] == true and expr[1] == true:
            return true
        else:
            return expr


and_rule = AndRule()


class OrRule(Rule):
    def predicate(self, expr):
        return isContainer(expr, 'or', 2)

    def body(self, expr):
        if expr[0] == true:
            return true
        elif expr[1] == true:
            return true
        elif expr[0] == false or expr[1] == false:
            return false
        else:
            return expr


or_rule = OrRule()


class NotRule(Rule):
    def predicate(self, expr):
        return isContainer(expr, 'not', 1)

    truthtable = {
        true: false,
        false: true,
    }

    def body(self, expr):
        return self.truthtable.get(expr[0], expr)


not_rule = NotRule()

logic_rules = JustOne(and_rule, or_rule, not_rule)


class GreaterThan(Rule):
    def predicate(self, expr):
        return (
            isContainer(expr, '>', 2)
            and isNumber(expr[0])
            and expr[0].value.is_real
            and isNumber(expr[1])
            and expr[1].value.is_real
        )

    def body(self, expr):
        if expr[0].value > expr[1].value:
            return true
        else:
            return false
        

greaterthan_rule = GreaterThan()


class GreaterThanEqual(Rule):
    def predicate(self, expr):
        return (
            isContainer(expr, '>=', 2)
            and isNumber(expr[0])
            and expr[0].value.is_real
            and isNumber(expr[1])
            and expr[1].value.is_real
        )

    def body(self, expr):
        if expr[0].value >= expr[1].value:
            return true
        else:
            return false
        

greaterthanequal_rule = GreaterThanEqual()


class LessThan(Rule):
    def predicate(self, expr):
        return (
            isContainer(expr, '>', 2)
            and isNumber(expr[0])
            and expr[0].value.is_real
            and isNumber(expr[1])
            and expr[1].value.is_real
        )

    def body(self, expr):
        if expr[0].value > expr[1].value:
            return true
        else:
            return false
        

lessthan_rule = LessThan()


class LessThanEqual(Rule):
    def predicate(self, expr):
        return (
            isContainer(expr, '>=', 2)
            and isNumber(expr[0])
            and expr[0].value.is_real
            and isNumber(expr[1])
            and expr[1].value.is_real
        )

    def body(self, expr):
        if expr[0].value >= expr[1].value:
            return true
        else:
            return false
        

lessthanequal_rule = LessThanEqual()


class Equal(Rule):
    """ Mathematical equality, not programming equality.
    """
    def predicate(self, expr):
        return isContainer(expr, '==', 2)

    def body(self, expr):
        if isNumber(expr[0]) and isNumber(expr[1]):
            if expr[0].value == expr[1].value:
                return true
            else:
                return false
        elif expr[0] == expr[1]:
            return true
        else:
            return expr

equal_rule = Equal()

comparison_rules = JustOne(
    equal_rule, greaterthan_rule, greaterthanequal_rule,
    lessthan_rule, lessthanequal_rule
)


# ==============
# Predicate Rule
# ==============
predicate_rule = JustOne(number_type_rules, comparison_rules, logic_rules,)
predicate_rule_bu = JustOneBU(
     number_type_rules, comparison_rules, logic_rules,
)

