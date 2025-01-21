"""
The simplify and other simplifucation rules depend upon first converting
a truealgebra expressiop into what is called here an SPP (StarPwr Plus) form.
The requirements for a SPP form are below

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

    * Cannot be: coef is num1, expdict has length of 1, value is num1
    * There is an exception to the above requiremnet inside Plus objects.
    * expdict cannot be empty
    * expdict values cannot be num0
    * expdict values must be a Number object
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
The convertoSPP rule (below) converts expressions into a SPP form,

The convertoSPP rule contains rules derived from the following classes:
StarToSPP, DivToSPP, PwrToSPP, NegToSPP, AddToSPP, and MinusToSPP.
All were written assuming that every subexpressions in the expression being
evaluated is already in SPP form. Thus the converttpSPP rule must always be
applied bottomup.

The conversion process does not use mathematical factoring or the distributive
property.
"""

from truealgebra.core.expressions import (
    ExprBase, Number, Container, CommAssoc, isNumber, isContainer,
    isCommAssoc, null
)
from truealgebra.core.rules import Rule, Rules, RulesBU, JustOneBU
from truealgebra.core.err import ta_logger

from truealgebra.common.commonsettings import commonsettings as comset
from truealgebra.common.utility import (
    addnums, mulnums, divnums, subnums, pwrnums, negnum,create_starCA
)

from types import MappingProxyType

from IPython import embed


class StarPwr(ExprBase):
    """Represents multiplication, division and power functions.

    self.coef: python number
        The numerical coeffient of the expression

    self.expdict: dict, inside of a MappingProxyType
        The expdict keys must be TrueAlgebra expressions
        They are the base of a power function.
        The expdict values must be python Number objects
        they are the exponent of a power function.
    """
    def __init__(self, coef=comset.num1, expdict=None):
        object.__setattr__(self, "coef", coef)
        if expdict is not None:
            expdict = MappingProxyType(expdict)
            object.__setattr__(self, "expdict", expdict)
        # Above,a shallow copy is made of a dictionary
        # That is OK in this case since all dict values are unmutable

    expdict = MappingProxyType(dict())

    def __repr__(self):
        out = 'StarPwr(' + repr(self.coef) + ', {'
        for ndx, item in enumerate(self.expdict):
            if ndx:
                out = (
                    out
                    + ', '
                    + repr(item)
                    + ': '
                    + repr(self.expdict[item])
                )
            else:
                out = out + repr(item) + ': ' + repr(self.expdict[item])
        out = out + '})'
        return out

    def bottomup(self, rule):
        pseudo = PseudoSP(coef=self.coef)
        for key in self.expdict:
            newkey = rule(key)
            value = self.expdict[key]
            pseudo.mul_keyvalue(newkey, value)
        return rule(
            StarPwr(pseudo.coef, pseudo.expdict),
            _pathinhibit=True,
            _buinhibit=True
        )

        newdict = dict()
        for key in self.expdict:
            newkey = rule(key)
            newdict[newkey] = self.expdict[key]
        return rule(
            self.__class__(coef=self.coef, expdict=newdict),
            _pathinhibit=True,
            _buinhibit=True
        )

    def apply2path(self, path, rule, _buinhibit=False):
        if path:
            ta_logger.log("path cannot enter StarPwr instance")
            return null
        else:
            return rule(self, _pathinhibit=True, _buinhibit=True)

    def __eq__(self, other):
        if (
            type(self) is not type(other)
            or self.coef != other.coef
            or len(self.expdict) != len(other.expdict)
        ):
            return False

        for key in self.expdict:
            if (
                key not in other.expdict
                or self.expdict[key] != other.expdict[key]
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
            frozenset(self.expdict.items())
        ))


class PseudoSP():
    """ i
    Mutable Objects used to convert expressions to StarPwr objects.

    The data structure is similar to that of StarPwr, but is mutable.
    Rules use the methods to process create new StarPwr objects.

    Attributes:
        expdict (dict): exponent dictionary
        coef (Number): coefficient
    """
    def __init__(self, coef=comset.num1, expdict=None):
        self.coef = coef
        if expdict is None:
            self.expdict = dict()
        else:
            self.expdict = expdict

    def mul_keyvalue(self, key, value):
        """ 
        self is multiplied by a key, value pair.

        Parameters::
            key (ExprBase): key of a expdict map
            value (Number): value of a expdict map

        Returns:
            None
        """
        if key in self.expdict:
            newvalue = addnums(value, self.expdict[key])
            if newvalue == comset.num0:
                del self.expdict[key]
            else:
                self.expdict[key] = newvalue
        else:
            self.expdict[key] = value

    def merge_starpwr(self, starpwr):
        """ 
        self is multiplied by a StarPwr object

        Parameters:
            starpwr (StarPwr):  object that muliplies self

        Return:
            None
        """
        self.coef = mulnums(self.coef, starpwr.coef)

        for key, value in starpwr.expdict.items():
            self.mul_keyvalue(key, value)

    def div_starpwr(self, starpwr):
        """ 
        self is divided by a StarPwr object

        Parameters:
            starpwr (StarPwr):  object that divides self

        Return:
            None
        """
        self.coef = divnums(self.coef, starpwr.coef)
        for key, value in starpwr.expdict.items():
            self.div_keyvalue(key, value)

    def div_keyvalue(self, key, value):
        """
        self is divided by a key, value pair.

        Parameters:
            key (ExprBase): key of a expdict map
            value (Number): value of a expdict map

        Returns:
            None
        """
        if key in self.expdict:
            newvalue = subnums(self.expdict[key], value)
            if newvalue == comset.num0:
                del self.expdict[key]
            else:
                self.expdict[key] = newvalue
        else:
            newvalue = mulnums(comset.neg1, value)
            self.expdict[key] = newvalue

    def apply_exponent(self, exp):
        """
        self is raised to the power of a numeric exponebt

        Parameteers:
            exp (Number): exponent

        Returns:
            None
        """
        # It is assumed that exp is a number and not num0 or num1
        self.coef = pwrnums(self.coef, exp)
        for key, value in self.expdict.items():
            self.expdict[key] = mulnums(value, exp)

    def return_SP(self):
        """
        Convert self to an expression

        No Parameter:

        Returns:
            ExprBase: Usually is a StarPwr object.
                      Could be a Number or other object.
        """
        if self.coef == comset.num0:
            return comset.num0
        elif len(self.expdict) == 0:
            return self.coef
        elif (
            len(self.expdict) == 1
            and list(self.expdict.values())[0] == comset.num1
            and self.coef == comset.num1
        ):
            return list(self.expdict.keys())[0]
        else:
            return StarPwr(self.coef, self.expdict)


class Plus(CommAssoc):
    """Represents addition and sutraction.

    Unlike StarPwr this class is a subclass of CommAssoc.

    Attributes:
        num (Number): python Number
        items (tuple): a tuple of StarPwr objects.
    """
    def __init__(self, num=comset.num0, items=tuple()):
        object.__setattr__(self, "num", num)
        object.__setattr__(self, "items", tuple(items))

    # All CommAssoc instances must have a name attribute.
    name = None

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


class PseudoP():
    """ Mutable Objects used to covert expressions to Plus objects. The data
    structure of this class is similar to that of Plus, but is mutable.
    These objects store data and their methods process the data.
    """
    def __init__(self, num=comset.num0, items=tuple()):
        self.num = num
        self.items = list(items)

    def make_item_SP(self, item):
        if isSP(item):
            return item
        else:
            return StarPwr(comset.num1, {item: comset.num1})

    def append_itemSP(self, itemSP):
        for ndx, pseudoitem in enumerate(self.items):
            if itemSP.expdict == pseudoitem.expdict:
                new_coef = (addnums(pseudoitem.coef, itemSP.coef))
                self.items[ndx] = StarPwr(new_coef, pseudoitem.expdict)
                return
        self.items.append(itemSP)

    def merge_plus(self, plus):
        self.num = addnums(self.num, plus.num)
        for plusitem in plus.items:
            self.append_itemSP(plusitem)

    def clean_items(self):
        """ remove item with attribute coef == 0
            items contains only StarPwr objects
        """
        del_ndx_list = list()
        for ndx, item in enumerate(self.items):
            if item.coef == comset.num0:
                del_ndx_list.append(ndx)
        for ndx in reversed(del_ndx_list):
            del self.items[ndx]

    def return_P(self):
        if len(self.items) == 0:
            return self.num
        elif self.num == comset.num0 and len(self.items) == 1:
            sp = self.items[0]
            if (
                sp.coef == comset.num1
                and list(sp.expdict.values())[0] == comset.num1
            ):
                return list(sp.expdict.keys())[0]
            else:
                return sp
        return Plus(self.num, self.items)


# =====================
# The converttoSPP rule
# =====================
class StarToSPP(Rule):
    """
    Convert a CommAssoc expression with name '*' to a StarPwr expression. 
    """
    def predicate(self, expr):
        return isCommAssoc(expr, name='*')

    def body(self, expr):
        pseudo = PseudoSP()
        for item in expr.items:
            if isNumber(item):
                pseudo.coef = mulnums(pseudo.coef, item)
            elif isSP(item):
                pseudo.merge_starpwr(item)
            else:
                pseudo.mul_keyvalue(item, comset.num1)
        return pseudo.return_SP()


class DivToSPP(Rule):
    """
    Convert a Container expression with name '/' to a StarPwr expression. 
    """
    def predicate(self, expr):
        return isContainer(expr, name='/', arity=2)

    def body(self, expr):
        pseudo = PseudoSP()
        top = expr[0]
        bottom = expr[1]

        if isNumber(top):
            pseudo.coef = mulnums(pseudo.coef, top)
        elif isSP(top):
            pseudo.merge_starpwr(top)
        else:
            pseudo.mul_keyvalue(top, comset.num1)

        if isNumber(bottom):
            pseudo.coef = divnums(pseudo.coef, bottom)
        elif isSP(bottom):
            pseudo.div_starpwr(bottom)
        else:
            pseudo.div_keyvalue(bottom, comset.num1)
        return pseudo.return_SP()


class PwrToSPP(Rule):
    """
    Convert a Container expression with name '**' to a StarPwr expression. 
    """
    def predicate(self, expr):
        return isContainer(expr, name='**', arity=2)

    def body(self, expr):
        if isNumber(expr[1]):
            if isNumber(expr[0]):
                return pwrnums(expr[0], expr[1])
            elif expr[1] == comset.num1:
                return expr[0]
            elif expr[1] == comset.num0:
                return comset.num1
            elif isSP(expr[0]):
                pseudo = PseudoSP(expr[0].coef, dict(expr[0].expdict))
                pseudo.apply_exponent(expr[1])
                return pseudo.return_SP()
            else:
                return StarPwr(comset.num1, {expr[0]: expr[1]})
        else:
            return expr


class NegToSPP(Rule):
    """
    Convert a Container expression with name '-' and one item
    to a StarPwr expression. 

    -x is converted as though it were (-1) * x
    """
    
    def predicate(self, expr):
        return isContainer(expr, name='-', arity=1)

    def body(self, expr):
        if isNumber(expr[0]):
            return negnum(expr[0])
        pseudo = PseudoSP(Number(-1), dict())
        if isSP(expr[0]):
            pseudo.merge_starpwr(expr[0])
        else:
            pseudo.mul_keyvalue(expr[0], comset.num1)
        return pseudo.return_SP()

negtoSP = NegToSPP()


class AddToSPP(Rule):
    """
    Convert a CommAssoc expression with name '+' to a Plus expression. 
    """
    def predicate(self, expr):
        return isCommAssoc(expr, name='+')

    def body(self, expr):
        pseudo = PseudoP()
        for item in expr:
            if isNumber(item):
                pseudo.num = addnums(pseudo.num, item)
            elif isPl(item):
                pseudo.merge_plus(item)
            else:
                itemSP = pseudo.make_item_SP(item)
                pseudo.append_itemSP(itemSP)
        pseudo.clean_items()
        return pseudo.return_P()


class MinusToSPP(Rule):
    """
    Convert a Container expression with name '-' and two items
    to a StarPwr expression. 

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
        elif isPl(expr[0]):
            pseudo.merge_plus(expr[0])
        else:
            itemSP = pseudo.make_item_SP(expr[0])
            pseudo.append_itemSP(itemSP)

        ex1 = negtoSP(Container('-', (expr[1],)))
        if isNumber(ex1):
            pseudo.num = addnums(pseudo.num, ex1)
        elif isPl(ex1):
            pseudo.merge_plus(ex1)
        else:
            ex2 = pseudo.make_item_SP(ex1)
            pseudo.append_itemSP(ex2)

        pseudo.clean_items()
        return pseudo.return_P()


converttoSPP = JustOneBU(
    StarToSPP(), DivToSPP(), PwrToSPP(),
    AddToSPP(), NegToSPP(), MinusToSPP(), comset.evalnum
)


# ================
# Convert From SPP
# ================
class ConvertFromStarPwr(Rule):
    """
    Convert from a StqrPwr expression.
    """
    def predicate(self, expr):
        return isinstance(expr, StarPwr)

    def body(self, expr):
        items = list()

        if expr.coef != comset.num1:
            items.append(expr.coef)

        for key in expr.expdict:
            if expr.expdict[key] == comset.num1:
                items.append(key)
            else:
                items.append(Container('**', (key, expr.expdict[key])))

        return create_starCA(items)


convertfromstarpwr = ConvertFromStarPwr()
            

class ConvertFromPlus(Rule):
    def predicate(self, expr):
        return isinstance(expr, Plus)

    def body(self, expr):
        items = list()

        if expr.num != comset.num0:
            items.append(expr.num)

        for item in expr.items:
            items.append(item)

        if len(items) == 0:
            return comset.num0
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
        if expr.coef == comset.num1 or expr.coef == comset.neg1:
            upstairs = positive_list + complex_list
        else:
            upstairs = [expr.coef] + positive_list + complex_list
        downstairs = negative_list

        if len(upstairs) > 1:
            up = CommAssoc('*', upstairs)
        elif len(upstairs) == 1:
            up = upstairs[0]
        else:
            up = comset.num1

        if len(downstairs) > 1:
            down = CommAssoc('*', downstairs)
            out = Container('/', (up, down))
        elif len(downstairs) == 1:
            down = downstairs[0]
            out = Container('/', (up, down))
        else:
            out = up

        if expr.coef == comset.neg1:
            return Container('-', (out,))
        else:
            return out

    def sort(self, expr, with_div=True):
        complex_list = list()  # complexx numerator list
        positive_list = list()  # real numerator list
        negative_list = list()  # real denomanator(expr?) list
        for ex, exp in expr.expdict.items():
            if isinstance(exp.value, complex):
                complex_list.append(Container('**', (ex, exp)))
            elif exp == comset.num1:
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


# shortcuts
# ---------
def isSP(expr):
    return isinstance(expr, StarPwr)


def isPl(expr):
    return isinstance(expr, Plus)

SP = StarPwr
Pl = Plus
