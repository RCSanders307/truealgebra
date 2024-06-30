from truealgebra.core.rules import JustOne, JustOneBU
from truealgebra.core.naturalrules import HalfNaturalRule, NaturalRule
from truealgebra.core.expression import Number, true, false
from fractions import Fraction

# =================
# Number Type Rules
# =================
class HalfNaturalRulePred(HalfNaturalRule):
    """Base class, defines one variable."""
    varstring = ' @ex '


class IsNumber(HalfNaturalRulePred):
    pattern = ' isnumber(ex) '

    def body(self, expr, var):
        if isinstance(var.ex, Number):
            return true
        else:
            return false


class IsInteger(HalfNaturalRulePred):
    pattern = ' isint(ex) '

    def body(self, expr, var):
        if isinstance(var.ex, Number) and isinstance(var.ex.value, int):
            return true
        else:
            return false


class IsFraction(HalfNaturalRulePred):
    pattern = ' isfraction(ex) '

    def body(self, expr, var):
        if isinstance(var.ex, Number) and isinstance(var.ex.value, Fraction):
            return true
        else:
            return false


class IsReal(HalfNaturalRulePred):
    pattern = ' isreal(ex) '

    def body(self, expr, var):
        if (
            isinstance(var.ex, Number)
            and not isinstance(var.ex.value, complex)
        ):
            return true
        else:
            return false


class IsComplex(HalfNaturalRulePred):
    pattern = ' iscomplex(ex) '

    def body(self, expr, var):
        if isinstance(var.ex, Number) and isinstance(var.ex.value, complex):
            return true
        else:
            return false


class IsFloat(HalfNaturalRulePred):
    pattern = ' isfloat(ex) '

    def body(self, expr, var):
        if isinstance(var.ex, Number) and isinstance(var.ex.value, float):
            return true
        else:
            return false


isnumber = IsNumber()
isinteger = IsInteger()
isfraction = IsFraction()
isreal = IsReal()
iscomplex = IsComplex()
isfloat = IsFloat()

number_type_rules = JustOne(
    isnumber, isinteger, isfraction, isreal, iscomplex, isfloat,
)


# ===========
# Logic Rules
# ===========
class NaturalRulePredicate(NaturalRule):
    varstring = ' @ex '


not_true = NaturalRulePredicate(
    pattern=' not true ',
    outcome=' false ',
)
not_false = NaturalRulePredicate(
    pattern=' not false ',
    outcome=' true ',
)

true_and_true = NaturalRulePredicate(
    pattern=' true and true ',
    outcome=' true ',
)
true_and_false = NaturalRulePredicate(
    pattern=' true and false ',
    outcome=' false ',
)
false_and_true = NaturalRulePredicate(
    pattern=' false and true ',
    outcome=' false ',
)
false_and_false = NaturalRulePredicate(
    pattern=' false and false ',
    outcome=' false ',
)

true_or_true = NaturalRulePredicate(
    pattern=' true or true ',
    outcome=' true ',
)
true_or_false = NaturalRulePredicate(
    pattern=' true or false ',
    outcome=' true ',
)
false_or_true = NaturalRulePredicate(
    pattern=' false or true ',
    outcome=' true ',
)
false_or_false = NaturalRulePredicate(
    pattern=' false or false ',
    outcome=' false ',
)

logic_rules = JustOne(
    not_true, not_false,
    true_and_true, true_and_false, false_and_true, false_and_false,
    true_or_true, true_or_false, false_or_true, false_or_false,
)


# ================
# Comparison Rules
# ================
class AreEqual(HalfNaturalRulePred):
    """Test equality of any two expressions."""
    var_dict = ' @ex0; @ex1 '
    pattern = ' ex0 == ex1 '

    def body(expr, var):
        if var.ex0 == var.ex1:
            return true
        else:
            return false


class RealPredicate(HalfNaturalRulePred):
    """ Base class with two real variables defined."""
    predicate_rule = isreal
    var_dict = ' @r0 | isreal(r0) ; @r1 | isreal(r1) '


class GreaterThan(RealPredicate):
    pattern = ' r0 > r1 '

    def body(self, expr, var):
        if var.r0.value > var.r1.value:
            return true
        else:
            return false


class GreaterThanEqual(RealPredicate):
    pattern = ' r0 >= r1 '

    def body(self, expr, var):
        if var.r0.value >= var.r1.value:
            return true
        else:
            return false


class LessThan(RealPredicate):
    pattern = ' r0 < r1 '

    def body(self, expr, var):
        if var.r0.value < var.r1.value:
            return true
        else:
            return false


class LessThanEqual(RealPredicate):
    pattern = ' r0 <= r1 '

    def body(self, expr, var):
        if var.r0.value <= var.r1.value:
            return true
        else:
            return false


areequal = AreEqual()
greaterthan = GreaterThan()
greaterthanequal = GreaterThanEqual()
lessthan = LessThan()
lessthanequal = LessThanEqual()

comparison_rules = JustOne(
    areequal, greaterthan, greaterthanequal, lessthan, lessthanequal,
)

# ==============
# Predicate Rule
# ==============
predicate_rule = JustOne(number_type_rules, comparison_rules, logic_rules,)
predicate_rule_bu = JustOneBU(
     number_type_rules, comparison_rules, logic_rules,
)


# ========
# If Rules
# ========

class IfRule(NaturalRule):
    varstring = ' forall(ex0, ex1) '

if_ = IfRule(
    pattern = ' if(true, ex0) ',
    outcome = 'ex0',
)

elif_true = IfRule(
    pattern = ' if(true, ex0, ex1) ',
    outcome = 'ex0',
)

elif_false = IfRule(
    pattern = ' if(false, ex0, ex1) ',
    outcome = 'ex1',
)

if_rules = JustOne(if_, elif_true, elif_false)
