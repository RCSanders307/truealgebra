"""Facilitate algebraic simplification of TrueAlgebra expressions.

The rule Converts expressions into a SPP form, described below.
Note that a ConvertToSPP rule is meant to be applied only with
bottomup attribute equal to True. The ConvertToSPP rule is  written
assuming that all subexpressions in the expression being evaluated
are already in SPP form.

The SPP (StarPwr Plus) form is described below:

Numeric Evaluations
===================

    * All numeric evaluations are made

StarPwr
=======
The following Container instances will become part of a StarPwr instance.

    * Those with names '*' and '/'
    * Those with name '-' and one item only (negative operator)
    * Those with name '**' and numeric exponents

Requirements for StarPwr Instances
----------------------------------

    * Cannot be: coef is num1, exp_dict has length of 1, value is num1
    * There is an exception to the above requiremnet inside Plus objects.
    * exp_dict cannot be empty
    * exp_dict values cannot be num0
    * exp_dict values must be a Number object
    * coef cannot be num0
    * coef must be a Number object
    * keys cannot be StarPwr or Number objects
    * keys cannot be '**' containers with Number object as exponent.

Plus
====

The following Container instances will become part of a Plus instance.
    Those with the name '+'
    Those with name '-' and two item only (subtraction operator)

Requirements for Plus Instances
-------------------------------

    * cannot have empty items attribute (becomes Number(0))
    * If num = 0, cannot have only one item (becomes items[0])
    * No Number objects in the items attribute
    * There will not be Plus instances inside the items attribute.
    * Only StarPwr objects inside the items attribute (see below).
    * These StarPwr objects may violate first rule above for StrPwr.

General Comments
================
The conversion process does implement mathematical factoring
or the distributive property.
"""

from truealgebra.common.commonsettings import commonsettings
from truealgebra.common.utility import (
    addnums, mulnums, divnums, subnums, pwrnums, negnum
)

from truealgebra.core.expressions import (
    ExprBase, Number, Container, CommAssoc, isNumber, isContainer,
    isCommAssoc, null
)
from truealgebra.core.rules import Rule, Rules, RulesBU, JustOneBU
from truealgebra.core.err import ta_logger

from types import MappingProxyType

from IPython import embed

evalnum = commonsettings.evalnum
num0 = commonsettings.num0
num1 = commonsettings.num1
neg1 = commonsettings.neg1


class StarPwr(ExprBase):
    """Represents multiplication, division and power functions.

    self.coef: python number
        The numerical coeffient of the expression

    self.exp_dict: dict, inside of a MappingProxyType
        The exp_dict keys must be TrueAlgebra expressions
        They are the base of a power function.
        The exp_dict values must be python Number objects
        they are the exponent of a power function.

    The static methods are utility functions used by ConvertToSPP methods
    to convert expressions with names '*', '**', '/' , and '-',
    into StarPwr objects.
    """
    def __init__(self, coef=num1, exp_dict=None):
        object.__setattr__(self, "coef", coef)
        if exp_dict is not None:
            exp_dict = MappingProxyType(exp_dict)
            object.__setattr__(self, "exp_dict", exp_dict)
        # Above,a shallow copy is made of a dictionary
        # That is OK in this case since all dict values are unmutable

    exp_dict = MappingProxyType(dict())

    def __repr__(self):
        out = 'SP(' + repr(self.coef) + ', {'
        for ndx, item in enumerate(self.exp_dict):
            if ndx:
                out = (
                    out
                    + ', '
                    + repr(item)
                    + ': '
                    + repr(self.exp_dict[item])
                )
            else:
                out = out + repr(item) + ': ' + repr(self.exp_dict[item])
        out = out + '})'
        return out

    def bottomup(self, rule):
        newdict = dict()
        for key in self.exp_dict:
            newkey = rule(key)
            newdict[newkey] = self.exp_dict[key]
        return rule(
            self.__class__(coef=self.coef, exp_dict=newdict),
            _pathinhibit=True,
            _buinhibit=True
        )

    def apply2path(self, path, rule, _buinhibit=False):
        if path:
            ta_logger.log("path cannot enter StarPwr instnce")
            return null
        else:
            return rule(self, _pathinhibit=True, _buinhibit=True)

    def __eq__(self, other):
        if (
            type(self) is not type(other)
            or self.coef != other.coef
            or len(self.exp_dict) != len(other.exp_dict)
        ):
            return False

        for key in self.exp_dict:
            if (
                key not in other.exp_dict
                or self.exp_dict[key] != other.exp_dict[key]
            ):
                return False
        return True

    def match(self, vardict, subdict, pred_rule, expr):
        return self == expr

    def __hash__(self):
        return hash((
            self.coef,
            type(self),
            # stackoverflow question 5884066, user Imran answer
            frozenset(self.exp_dict.items())
        ))

    @staticmethod
    def merge_starpwr(starpwr, pseudo):
        pseudo.coef = mulnums(pseudo.coef, starpwr.coef)

        for key, value in starpwr.exp_dict.items():
            StarPwr.mul_keyvalue(key, value, pseudo)

    @staticmethod
    def mul_key(key, pseudo):
        if key in pseudo.exp_dict:
            newvalue = addnums(num1, pseudo.exp_dict[key])
            if newvalue == num0:
                del pseudo.exp_dict[key]
            else:
                pseudo.exp_dict[key] = newvalue
        else:
            pseudo.exp_dict[key] = num1

    @staticmethod
    def mul_keyvalue(key, value, pseudo):
        if key in pseudo.exp_dict:
            newvalue = addnums(value, pseudo.exp_dict[key])
            if newvalue == num0:
                del pseudo.exp_dict[key]
            else:
                pseudo.exp_dict[key] = newvalue
        else:
            pseudo.exp_dict[key] = value

    @staticmethod
    def div_starpwr(starpwr, pseudo):
        pseudo.coef = divnums(pseudo.coef, starpwr.coef)
        for key, value in starpwr.exp_dict.items():
            StarPwr.div_keyvalue(key, value, pseudo)

    @staticmethod
    def div_keyvalue(key, value, pseudo):
        if key in pseudo.exp_dict:
            newvalue = subnums(pseudo.exp_dict[key], value)
            if newvalue == num0:
                del pseudo.exp_dict[key]
            else:
                pseudo.exp_dict[key] = newvalue
        else:
            newvalue = mulnums(neg1, value)
            pseudo.exp_dict[key] = newvalue

    @staticmethod
    def div_key(key, pseudo):
        if key in pseudo.exp_dict:
            newvalue = subnums(pseudo.exp_dict[key], num1)
            if newvalue == num0:
                del pseudo.exp_dict[key]
            else:
                pseudo.exp_dict[key] = newvalue
        else:
            pseudo.exp_dict[key] = neg1

    @staticmethod
    def appy_exponent(starpwr, exp, pseudo):
        # It is assumed that exp is not num0 or num1
        pseudo.coef = pwrnums(starpwr.coef, exp)
        for key, value in starpwr.exp_dict.items():
            pseudo.exp_dict[key] = mulnums(value, exp)

    @staticmethod
    def return_SP(pseudoSP_or_SP):
        if pseudoSP_or_SP.coef == num0:
            return num0
        if len(pseudoSP_or_SP.exp_dict) == 0:
            return pseudoSP_or_SP.coef
        if (
            len(pseudoSP_or_SP.exp_dict) == 1
            and list(pseudoSP_or_SP.exp_dict.values())[0] == num1
            and pseudoSP_or_SP.coef == num1
        ):
            return list(pseudoSP_or_SP.exp_dict.keys())[0]
        if type(pseudoSP_or_SP) is StarPwr:
            return pseudoSP_or_SP
        return pseudoSP_or_SP.makeSP()


class PseudoSP():
    """ Mutable bjects of this class are shared between conversion rules
    and StarPwr static methods to exchange data. The data structure is similar
    to that of StarPwr, but is mutable.
    """

    def __init__(self, coef=num1, exp_dict=None):
        self.coef = coef
        if exp_dict is None:
            self.exp_dict = dict()
        else:
            self.exp_dict = exp_dict

    def makeSP(self):
        return StarPwr(self.coef, self.exp_dict)


class Plus(CommAssoc):
    """Represents addition. Unlike StarPwr this class is a subclass of
    CommAssoc.

    self.num: python Number

    self.items: a tuple of StarPwr objects.

    The static methods are utility functions used by ConvertToSPP methods
    to convert expressions with names '+', and '-' into Plus objects
    """
    def __init__(self, num=num0, items=tuple()):
        object.__setattr__(self, "num", num)
        object.__setattr__(self, "items", tuple(items))

    # All CommAssoc instances must have a name attribute.
    # The name '_+' cannot be generated during parsing, as the '_'
    # character is used only in symbol names and '+' is used
    # only in operator names.
    name = '_+'

    def bottomup(self, rule):
        return rule(
            self.__class__(
                self.num,
                tuple([item.bottomup(rule) for item in self.items])),
            _pathinhibit=True,
            _buinhibit=True)

    def __repr__(self):
        out = 'Plus(' + repr(self.num) + ', ('
        for item in self.items[0:-1]:
            out += (repr(item) + ', ')
        if self.items:
            out += repr(self.items[-1])
        out = out + '))'
        return out

    def __hash__(self):
        return hash((
            type(self),
            self.name,
            self.num,
            tuple(sorted(map(hash, self.items)))
        ))

    def __eq__(self, other):
        if (
            type(self) is not type(other)
            or len(self) != len(other)
            or self.num != other.num
            or self.name != other.name
        ):
            return False
        else:
            return self.inner_eq(list(self.items), list(other.items))

    def match(self, vardict, subdict, pred_rule, expr):
        return self == expr

    @staticmethod
    def merge_plus(plus, pseudo):
        pseudo.num = addnums(pseudo.num, plus.num)
        for plusitem in plus.items:
            Plus.append_itemSP(plusitem, pseudo)

    @staticmethod
    def make_item_SP(item):
        if type(item) is StarPwr:
            return item
        else:
            return StarPwr(num1, {item: num1})

    @staticmethod
    def append_itemSP(itemSP, pseudo):
        go = True
        for ndx, pseudoitem in enumerate(pseudo.items):
            if itemSP.exp_dict == pseudoitem.exp_dict:
                new_coef = (addnums(pseudoitem.coef, itemSP.coef))
                pseudo.items[ndx] = StarPwr(new_coef, pseudoitem.exp_dict)
                go = False
                break
        if go:
            pseudo.items.append(itemSP)

    @staticmethod
    def clean_items(pseudo):
        del_ndx_list = list()
        for ndx, item in enumerate(pseudo.items):
            if item.coef == num0:
                del_ndx_list.append(ndx)
        for ndx in reversed(del_ndx_list):
            del pseudo.items[ndx]


class PseudoP():
    """ Mutable objects of this class are shared between conversion rules
    and Plus static methods to exchange data. The data structure is similar
    to that of Plus, but is mutable.
    """
    def __init__(self, num=num0, items=tuple()):
        self.num = num
        self.items = list(items)

    def makeP(self):
        return Plus(self.num, self.items)

    def copy(self):
        return PseudoP(self.num, list(self.items))


class StarToSPP(Rule):
    def predicate(self, expr):
        return isCommAssoc(expr, name='*')

    def body(self, expr):
        pseudo = PseudoSP(num1, dict())
        for item in expr.items:
            if type(item) is Number:
                pseudo.coef = mulnums(pseudo.coef, item)
            elif type(item) is StarPwr:
                StarPwr.merge_starpwr(item, pseudo)
            else:
                StarPwr.mul_key(item, pseudo)
        return StarPwr.return_SP(pseudo)


class DivToSPP(Rule):
    def predicate(self, expr):
        return isContainer(expr, name='/', arity=2)

    def body(self, expr):
        pseudo = PseudoSP()
        top = expr[0]
        bottom = expr[1]

        if type(top) is Number:
            pseudo.coef = mulnums(pseudo.coef, top)
        elif type(top) is StarPwr:
            StarPwr.merge_starpwr(top, pseudo)
        else:
            StarPwr.mul_key(top, pseudo)

        if type(bottom) is Number:
            pseudo.coef = divnums(pseudo.coef, bottom)
        elif type(bottom) is StarPwr:
            StarPwr.div_starpwr(bottom, pseudo)
        else:
            StarPwr.div_key(bottom, pseudo)
        return StarPwr.return_SP(pseudo)


class PwrToSPP(Rule):
    def predicate(self, expr):
        return isContainer(expr, name='**', arity=2)

    def body(self, expr):
        if isNumber(expr[1]):
            if isNumber(expr[0]):
                return pwrnums(expr[0], expr[1])
            elif expr[1] == num1:
                return expr[0]
            elif expr[1] == num0:
                return num1
            elif type(expr[0]) is StarPwr:
                pseudo = PseudoSP()
                StarPwr.apply_exponent(expr[0], expr[1], pseudo)
                return pseudo.makeSP()
            else:
                return StarPwr(num1, {expr[0]: expr[1]})
        else:
            return expr


class PlusToSPP(Rule):
    def predicate(self, expr):
        return isCommAssoc(expr, name='+')

    def body(self, expr):
        pseudo = PseudoP()
        for item in expr:
            if isNumber(item):
                pseudo.num = addnums(pseudo.num, item)
            elif type(item) is Plus:
                Plus.merge_plus(item, pseudo)
            else:
                itemSP = Plus.make_item_SP(item)
                Plus.append_itemSP(itemSP, pseudo)
        Plus.clean_items(pseudo)
        if len(pseudo.items) == 0:
            return pseudo.num
        if pseudo.num == num0 and len(pseudo.items) == 1:
            return StarPwr.return_SP(pseudo.items[0])
        return pseudo.makeP()


class NegToSPP(Rule):
    """ Convert negative function.
    -x is converted as though it were (-1) * x
    """
    
    def predicate(self, expr):
        return isContainer(expr, name='-', arity=1)

    def body(self, expr):
        if isNumber(expr[0]):
            return negnum(expr[0])
        pseudo = PseudoSP(Number(-1), dict())
        if type(expr[0]) is StarPwr:
            StarPwr.merge_starpwr(expr[0], pseudo)
        else:
            StarPwr.mul_key(expr[0], pseudo)
        return StarPwr.return_SP(pseudo)

negtoSP = NegToSPP()

class MinusToSPP(Rule):
    """ Convert minus and negative functions
    x-y is converted as though it were x + (-1) * y
    """
    def predicate(self, expr):
        return isContainer(expr, name='-', arity=2)

    def body(self, expr):
        if isNumber(expr[0]) and isNumber(expr[1]):
            return subnums(expr[0], expr[1])

        pseudo = PseudoP()
        if isNumber(expr[0]):
            pseudo.num = expr[0]
        elif type(expr[0]) is Plus:
            Plus.merge_plus(expr[0], pseudo)
        else:
            itemSP = Plus.make_item_SP(expr[0])
            Plus.append_itemSP(itemSP, pseudo)

        ex1 = negtoSP(Container('-', (expr[1],)))
        if type(ex1) is Number:
            pseudo.num = addnums(pseudo.num, ex1)
        else:
            Plus.append_itemSP(ex1, pseudo)

        Plus.clean_items(pseudo)
        if len(pseudo.items) == 0:
            return pseudo.num
        if pseudo.num == num0 and len(pseudo.items) == 1:
            return StarPwr.return_SP(pseudo.items[0])
        return pseudo.makeP()


converttoSPP = JustOneBU(
    StarToSPP(), DivToSPP(), PwrToSPP(),
    PlusToSPP(), NegToSPP(), MinusToSPP(), evalnum
)


class ConvertFromStarPwr(Rule):
    def predicate(self, expr):
        return isinstance(expr, StarPwr)

    def body(self, expr):
        items = list()

        if expr.coef != num1:
            items.append(expr.coef)

        for key in expr.exp_dict:
            if expr.exp_dict[key] == num1:
                items.append(key)
            else:
                items.append(Container('**', (key, expr.exp_dict[key])))

        if len(items) == 0:
            return num1
        elif len(items) == 1:
            return items[0]
        else:
            return CommAssoc('*', items)
            

class ConvertFromPlus(Rule):
    def predicate(self, expr):
        return isinstance(expr, Plus)

    def body(self, expr):
        items = list()

        if expr.num != num0:
            items.append(expr.num)

        for item in expr.items:
            items.append(item)

        if len(items) == 0:
            return num0
        elif len(items) == 1:
            return items[0]
        else:
            return CommAssoc('+', items)

simplify0 = Rules(
    converttoSPP,
    JustOneBU(ConvertFromStarPwr(), ConvertFromPlus())
)


class ConvertStarPwrToDiv(Rule):
    def predicate(self, expr):
        return isinstance(expr, StarPwr)

    def body(self, expr):
        complex_list, positive_list, negative_list = self.sort(expr)
        if expr.coef == num1 or expr.coef == neg1:
            upstairs = positive_list + complex_list
        else:
            upstairs = [expr.coef] + positive_list + complex_list
        downstairs = negative_list

        if len(upstairs) > 1:
            up = CommAssoc('*', upstairs)
        elif len(upstairs) == 1:
            up = upstairs[0]
        else:
            up = num1

        if len(downstairs) > 1:
            down = CommAssoc('*', downstairs)
            out = Container('/', (up, down))
        elif len(downstairs) == 1:
            down = downstairs[0]
            out = Container('/', (up, down))
        else:
            out = up

        if expr.coef == neg1:
            return Container('-', (out,))
        else:
            return out

    def sort(self, expr, with_div=True):
        complex_list = list()  # complexx numerator list
        positive_list = list()  # real numerator list
        negative_list = list()  # real denomanator(expr?) list
        for ex, exp in expr.exp_dict.items():
            if isinstance(exp.value, complex):
                complex_list.append(Container('**', (ex, exp)))
            elif exp == num1:
                positive_list.append(ex)
            elif exp.value > 0:
                positive_list.append(Container('**', (ex, exp)))
            elif exp.value == -1 and with_div:
                negative_list.append(ex)
            elif exp.value != 0 and with_div:
                negative_list.append(Container('**', (ex, Number(-exp.value))))
            elif exp.value != 0 and not with_div:
                negative_list.append(Container('**', (ex, exp)))
            # Note: if exp == 0, then ex**0 is 1, and is igmored.
        return complex_list, positive_list, negative_list



simplify = Rules(
    converttoSPP,
    JustOneBU(ConvertStarPwrToDiv(), ConvertFromPlus())
)
