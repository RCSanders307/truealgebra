from truealgebra.core.expression import (
    ExprBase, Number, Container, CommAssoc
)
from truealgebra.core.rulebase import RuleBase
from truealgebra.core.rule import JustOne, JustOneBU, Rules, RulesBU
from truealgebra.core.abbrv import isNu, isCo, num0, num1

from truealgebra.std.eval import evalmathsingle, evalmathdouble, math

from types import MappingProxyType
from collections import defaultdict
from abc import ABC, abstractmethod
import numbers

# shortcuts
# ---------
def isSP(expr):
    return isinstance(expr, StarPwr)


def isPl(expr):
    return isinstance(expr, Plus)


# StarPwr and PseudoStarPwr
# =========================
class StarPwr(ExprBase):
    """Represents multiplication of power functions.

    self.coef: python number
        The numerical coeffient of the expression

    self.exp_dict: dict, inside a MappingProxyType
        The exp_dict keys must be TrueAlgebra expressions and they
        are the base of a power function.
        The exp_dict values must be python numbers that represent
        the exponent of a power function.

    This class is not complete. There are no unparse, match, and apply2path
    methods.
    """
    def __init__(self, coef=1, exp_dict=None):
        object.__setattr__(self, "coef", coef)
        if exp_dict is not None:
            # Below, a shallow copy is made of a dictionary
            # That is OK in this case since all dict values are numbers
            exp_dict = MappingProxyType(exp_dict)
            object.__setattr__(self, "exp_dict", exp_dict)

    exp_dict = MappingProxyType(dict())

    @classmethod
    def copy(cls, source):
        return cls(
            source.coef,
            MappingProxyType(source.exp_dict)
        )

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

    def default_function(self):
        return 0

    def bottomup(self, rule):
        newdict = defaultdict(self.default_function)
        for key in self.exp_dict:
            newkey = rule(key)
            newdict[newkey] = math.add(
                self.exp_dict[key],
                newdict[newkey]
            )
        return rule(
            self.__class__(coef=self.coef, exp_dict=newdict),
            _pathinhibit=True,
            _buinhibit=True
        )

    def __eq__(self, other):
        if (
            type(self) != type(other)
            or self.coef != other.coef
            or len(self.exp_dict) != len(other.exp_dict)
        ):
            return False

        for key in self.exp_dict:
            if(
                key not in other.exp_dict
                or self.exp_dict[key] != other.exp_dict[key]
            ):
                return False

        return True

    
    def __hash__(self):
        return hash((
            self.coef,
            type(self),
            # stackoverflow question 5884066, user Imran answer
            frozenset(self.exp_dict.items())
        ))


class PseudoStarPwr:
    """ Quasi StarPwr class used for building a StarPwr instance.

    The data attributes for this class are similar to those of StrPwr,
    however they are mutable allowing for changes to be made easily.
    Once a PseudoStarPwr instance has beenn completely formed, it is
    coverted to a StarPwr instance using
    ``StarPwr.copy(<pseudostarpwr instance>)``.

    One difference is the exp_dict attribute here is a defaultdict.

    A PseudoStarPwr instance is for temporary programming needs only.
    Because it is mutable, it should never be used as a TrueAlgebra
    expression.
    """

    def __init__(self, coef=1, exp_dict=None):
        self.coef = coef
        if exp_dict is None:
            self.exp_dict = defaultdict(self.default_function)
        else:
            self.exp_dict = defaultdict(self.default_function, exp_dict)

    @classmethod
    def copy(cls, source):
        return cls(
            source.coef,
            defaultdict(cls.default_function, source.exp_dict)
        )


    def __eq__(self, other):
        if (
            type(self) != type(other)
            or self.coef != other.coef
            or len(self.exp_dict) != len(other.exp_dict)
        ):
            return False

        for key in self.exp_dict:
            if(
                key not in other.exp_dict
                or self.exp_dict[key] != other.exp_dict[key]
            ):
                return False

        return True

    
    def __hash__(self):
        return hash((
            self.coef,
            type(self),
            # stackoverflow question 5884066, user Imran answer
            frozenset(self.exp_dict.items())
        ))
    @classmethod
    def default_function(self):
        return 0

    def __repr__(self):
        out = 'PSP(' + repr(self.coef) + ', {'
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

    def merge(self, starpwr):
        self.coef = math.mul(self.coef, starpwr.coef)
        for key in starpwr.exp_dict:
            self.exp_dict[key] = math.add(
                self.exp_dict[key], starpwr.exp_dict[key]
            )

    def append(self, base, exp):
        self.exp_dict[base] = math.add(self.exp_dict[base], exp)

    def mul_by_num(self, num):
        self.coef = math.mul(self.coef, num)

    def apply_exponent(self, exp):
        for key in self.exp_dict:
            self.exp_dict[key] = math.mul(self.exp_dict[key], exp)
        self.coef = math.pwr(self.coef, exp)


# Plus and PseudoPlus
# ===================
class Plus(CommAssoc):
    """Models addition operations for algebraic simplifcation purposes

    self.num: python number

    This class is not complete. There are no unparse,and apply2path methods.
    The match method has not been tested.
    """
    def __init__(self, num=0, items=tuple()):
        object.__setattr__(self, "num", num)
        object.__setattr__(self, "items", tuple(items))

    # All CommAssoc instances must have a name attribute.
    # The name '_+' cannot be generated during parsing, as the '_'
    # character is used only in symbol names and '+' is used
    # only in operator names.
    name = '_+'

    @classmethod
    def copy(cls, source):
        return cls(source.num, source.items)

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
            type(self) != type(other)
            or len(self) != len(other)
            or self.num != other.num
            or self.name != other.name
        ):
            return False
        else:
            return self.inner_eq(list(self.items), list(other.items))

    def match(self, vardict, subdict, pred_rule, expr):
        """This method has not been tested"""
        if (
            type(expr) != type(self)
            or expr.name != self.name
            or expr.num != self.num
        ):
            return False

        cam = CommAssocMatch(self, vardict, subdict, pred_rule, expr)
        return cam.find_matches()




class PseudoPlus:
    """A mutable version of CommAssoc with name '+'

    items: list
        A mutable list

    Once a PseudoPlus instance has beenn completely formed, its
    create_plus method will be called creating a CommAssoc instance with
    a name attribute of '+', and the same data.
    """
    def __init__(self, num=0, items=()):
        self.num = num
        self.items = list(items)

    @classmethod
    def copy(cls, source):
        return cls(source.num, source.items)

    def find_common_term(self, term):
        if not isSP(term):
            self.items.append(term)
        else:
            for ndx, item in enumerate(self.items):
                if isSP(item) and item.exp_dict == term.exp_dict:
                    self.items[ndx] = StarPwr(
                        math.add(self.items[ndx].coef, term.coef),
                        term.exp_dict,
                    )
                    return
            self.items.append(term)

    def remove_sp_zeros(self):
        self.items = list(filter(
            lambda item: not (isSP(item) and item.coef == 0),
            self.items
        ))

    def merge(self, pplus):
        self.num = math.add(self.num, pplus.num)
        self.items.extend(pplus.items)

    def combine_nums(self):
        """ This is not used."""
        new_items = list()
        for item in self.items:
            if isNu(item):
                self.num = math.add(self.num, item.value)
            else:
                new_items.append(item)
        self.items = new_items


class ConvertTo(RuleBase):
    """Facilitate algebraic simplification of TrueAlgebra expressions.

    Star-power-plus Form
    ====================
    Convert expressions to star-power-plus form, described below:

    Numeric evaluations will be made of Container instances
    with the any of the following names: '/', '**', '-'.

    StarPlus
    --------
    The following Container instances will become part of a StarPwr instance.
        Those with names '*' and '/'
        Those with name '-' and one item only (negative operator)
        Those with name '**' and numeric exponents

    Expressions that do not satisfy the above requirements should not 
    become StrPwr instances. For example Sy('x') should not become
    SP(1, {Sy('x'): 1}).

    StarPwr exp_dict attribute cannot be an empty dictionary.
    exp_dict values cannot be 0.
    coef attribute cannot be 0 (Becomes Number(0))
    The StrPwr coef attribute must be a python number.

    The StarPwr exp_dict keys cannot be:
        StarPwr instances
        Number instances
        Container instances with name '**' and numeric exponent

    There will not be nested StarPwr instances. Any potentially nested StarPwr
    containers will be merged together.

    Plus
    ----
    The following Container instances will become part of a Plus instance.
        Those with the name '+'
        Those with name '-' and two item only (subtraction operator)

    cannot have empty items attribute (becomes Number(0))
    If num = 0, cannot have only one item (becomes items[0])
    No Number objects in the items attribute

    There will not be nested Plus instances. Any potentially nested Plus
    containers will be merged togrther.

    General Comments
    ----------------
    In the code for creating and modifying StarPwr and Plus instances,
    The above requirements can be temporarily relaxed, with the PseudoStarPwr 
    and PsuedoPlus objects. But the final StarPwr or Plus instance must
    comply with the above requirements.

    The Algebraic simplification process depends of the use of the python
    equality `==` operator. Therefor there must be uniformity throughout the
    conversion process for all identical objects to a star-power-plus format.
    For example, in a conversion/modification process, if a single
    (but not all) instance of `Sy('x')` is converted to to
    `SP(1, {Sy('x'): 1}`, the algebraic simplification can be unsuccessful.
    This is because in the python comparison,
    `Sy('x') != SP(1, {Sy('x'): 1})`, the two expressions are not equal.
    """

    @property
    def method_dict(self):
        return {
            '/': self.div,
            '*': self.star,
            '+': self.plus,
            '-': self.minus,
            '**': self.power,
        }

    def predicate(self, expr):
        return isCo(expr) and expr.name in self.method_dict

    def body(self, expr):
        return self.method_dict[expr.name](expr)

    def star(self, expr):
        psp = PseudoStarPwr()
        for item in expr:
            psp.append(item, 1)
        return spfinalcheck(psp)

    def div(self, expr):
        if isNu(expr[0]) and isNu(expr[1]):
            return Number(math.div(expr[0].value, expr[1].value))

        psp = PseudoStarPwr()
        psp.append(expr[0], 1)
        psp.append(expr[1], -1)
        return spfinalcheck(psp)

    def neg(self, expr):
        if isNu(expr[0]):
            return Number(math.neg(expr[0].value))

        psp = PseudoStarPwr(-1, {expr[0]: 1})
        return spfinalcheck(psp)

    def power(self, expr):
        if isNu(expr[0]) and isNu(expr[1]):
            return Number(math.pwr(expr[0].value, expr[1].value))
        elif isNu(expr[1]):
            psp = PseudoStarPwr(1, {expr[0]: expr[1].value})
            return spfinalcheck(psp)
        else:
            return expr

    def plus(self, expr):
        pplus = PseudoPlus(0, expr.items)
        return plfinalcheck(pplus)

    def minus(self, expr):
        """ Convert minus and negative functions

        Does NOT convert `a+b+c-(a+b+c)` to `a+b+c-a-b-c'
        """
        if len(expr) == 1:
            return self.neg(expr)

        if isNu(expr[0]) and isNu(expr[1]):
            return Number(math.sub(expr[0].value, expr[1].value))

        pplus = PseudoPlus(0, [
            expr[0], 
            self.neg(Container('-', (expr[1],)))
        ])
        return plfinalcheck(pplus)

step1_bu = RulesBU(ConvertTo())
convert2starpwr_bu = ConvertTo(bottomup=True)



class ChainBase(RuleBase):
    """Creates a chain of methods/functions to apply to an expression.

    This is a concrete base class that by itself is not useful.
    It is meant to be subclassed, for example by StarPwrModify.

    *args: sequence of classes (or functions)
        Each class is instantiated using the next class in the
        sequence as an argument. The last class takes self.exit_link
        as an argument. The result is a single function/method, self.chain.

        The self.chain method is used to apply an instance of
        every class listed in args to the input expression.

        This class follows the chain of responsibility design pattern.
    """
    def __init__(self, *args, **kwargs):
        self.chain = self.exit_link
        for cls in reversed(args):
            self.chain = cls(self.chain)
        super().__init__(*args, **kwargs)

    def exit_link(self, expr):
        return expr


class StarPwrModify(ChainBase):
    """Creates rules used to modify StarPwr expressions.

    *args: sequence of StarPowerModifier subclasses

    Example
    =======
    starpwr_rule to modify StarPwr expressions is created by:

    >>> strpwr_rule = StarPwrModiy(A_SPModifier, B_SPModifier, C_SPModifier)

    Where A_SPModifier, B_SPModifier, and C_SPModifier are subclasses of
    StarPwrModifier and their instances (which are rules themselves) will
    be applied in the same order to a TrueAlgebra PseudoStarPwr expression.

    StarPwrModify vs StarPwrModifier
    ================================
    StarPwrModify is a RuleBase subclass, with predicate and base methods that a user
    does not need to overwrite. A StarPwrModify instance contains instances of 
    StarPwrModifier subclasses.

    The StarPwrModifier instance's body methods are over written to provide
    the functionality of the rule. The StarPwrModier instances have no
    predicate method and the body method of every instance is always applied
    to the expression input.
    """
    def exit_link(self, psp):
        return StarPwr.copy(psp)

    def predicate(self, expr):
        return isSP(expr) or isinstance(expr, PseudoStarPwr)

    def body(self, expr):
        return self.chain(PseudoStarPwr.copy(expr))


class StarPwrModifier(ABC):
    """Base method for detailed specific changes to StarPwr instance.

    modify method:
        Argument must be PseudoStarPwr instance

    If output a PseudoStarPwr instance, the output is passed down the chain.
    If output is something else, the chain evalustions are stopped,
    and the output becones the output of the parent instance.

    When creating a subclass, a user modfies only the body method.
    There is no predicate method.
    """

    def __init__(self, nxt):
        self._nxt = nxt

    def __call__(self, psp):
        out = self.body(psp)
        if isinstance(out, PseudoStarPwr):
            return self._nxt(out)
        else:
            return out

    @abstractmethod
    def body(self, psp):
        pass

class SPBasePwr(StarPwrModifier):
    """ All factors whose base is power functions with numeric exponent."""
    def body(self, psp):
        new_psp = PseudoStarPwr(psp.coef)
        for factor in psp.exp_dict:
            if isCo(factor, name='**') and isNu(factor[1]):
                new_psp.exp_dict[factor[0]] = math.add(
                    new_psp.exp_dict[factor[0]], 
                    math.mul(psp.exp_dict[factor], factor[1].value)
                )
            else:
                new_psp.exp_dict[factor] = math.add(
                    new_psp.exp_dict[factor],
                    psp.exp_dict[factor]
                )
        return new_psp



class SPFinalCheck(StarPwrModifier):
    def body(self, psp):
        newpsp = PseudoStarPwr(psp.coef)
        for ex in psp.exp_dict:
            if isNu(ex):
                newpsp.coef = math.mul(
                    newpsp.coef,
                    math.pwr(ex.value, psp.exp_dict[ex])
                )
            elif isSP(ex):
                pseudo_ex = PseudoStarPwr.copy(ex)
                pseudo_ex.apply_exponent(psp.exp_dict[ex])
                newpsp.merge(pseudo_ex)
            elif psp.exp_dict[ex] != 0:
                newpsp.append(ex, psp.exp_dict[ex])
        if newpsp.coef == 0:
            return num0
        elif len(newpsp.exp_dict) == 0:
            return Number(newpsp.coef)
        elif (
            len(newpsp.exp_dict) == 1 
            and newpsp.coef == 1 
            and list(newpsp.exp_dict.values())[0] == 1
        ):
            return list(newpsp.exp_dict.keys())[0]
        else:
            return newpsp

class PlusModify(ChainBase):
    """ Modify CommAssoc instances with name '+'.

    *args: sequence of PlusModifier subclasses

    Each PlusModify instance will have a chain of PlusModifier instances.
    The PlusModifier instances perform the actual modofications.


    Example
    =======

    plus_rule to modify '+' CommAssoc expressions is created by:

    >>> plus_rule = PlusModiy(A_PModifier, B_PModifier, C_PModifier)

    Where A_PModifier, B_PModifier, and C_PModifier are subclassses of
    PlusModifier and their instances (which are rules themselves) will
    be applied in the same order to a PseudoPlus expression.
    
    PlusModify vs PlusModifier
    ================================
    The relationship of PlusModify to PlusModifier mirrors the relationship 
    of StarPwrModify to StarPwrModifier, which is explained above.
    """
    def exit_link(self, pseudoplus):
        return Plus.copy(pseudoplus)

    def predicate(self, expr):
        return isPl(expr) or isinstance(expr, PseudoPlus)

    def body(self, expr):
        return self.chain(PseudoPlus.copy(expr))


class PlusModifier(ABC):
    """Base class for modifying PseudoPlus instances.

    Subclasses can be created as needed for custom modifications of
    PseudoPlus instances. In the grand scheme the subclasses are used to
    modify CommAssoc instances with name '+'.

    """
    def __init__(self, nxt):
        self._nxt = nxt

    def __call__(self, pplus):
        out = self.body(pplus)
        if isinstance(out, PseudoPlus):
            return self._nxt(out)
        else:
            return out

    @abstractmethod
    def body(self, pplus):
        pass


class CombinePlusTerms(PlusModifier):
    """Combine common terms."""
    def body(self, pplus):
        newpplus = PseudoPlus(pplus.num)
        for item in pplus.items:
            if isSP(item):
                sp_item = item
            elif isCo(item, name='**') and isNu(item[1]):
                sp_item = (StarPwr(1, {item[0]: item[1].value}))
            else:
                # See General Comments in ConvertTo docstring 
                sp_item = StarPwr(1, {item: 1})
            newpplus.find_common_term(sp_item)
        newpplus.remove_sp_zeros()
        return newpplus


class PlRecheckSP(PlusModifier):
    def body(self, pplus):
        newpplus = PseudoPlus(pplus.num)
        for item in pplus.items:
            if isSP(item):
                newpplus.items.append(spfinalcheck(item))
            else:
                newpplus.items.append(item)
        return newpplus


class PlFinalCheck(PlusModifier):
    def body(self, pplus):
        newpplus = PseudoPlus(pplus.num)
        for item in pplus.items:
            if isNu(item):
                newpplus.num = math.add(newpplus.num, item.value)
            elif isPl(item):
                newpplus.merge(item)
            else:
                newpplus.items.append(item)
        if len(newpplus.items) == 1 and newpplus.num == 0:
            return newpplus.items[0]
        elif not len(newpplus.items):
            return Number(newpplus.num)
        else:
            return newpplus
                
plfinalcheck = PlusModify(PlFinalCheck)
spfinalcheck = StarPwrModify(SPFinalCheck)


step2_bu = JustOneBU(
    StarPwrModify(SPBasePwr, SPFinalCheck),
    PlusModify(CombinePlusTerms, PlRecheckSP, PlFinalCheck),
    evalmathsingle, evalmathdouble,
)


# Step 3
# ======
class ConvertToDiv(RuleBase):
    def predicate(self, expr):
        return isSP(expr)

    def body(self, sp):
        complex_list, positive_list, negative_list = self.sort(sp)
        if sp.coef == 1:
            upstairs = positive_list + complex_list
        else:
            upstairs = [Number(sp.coef)] + positive_list + complex_list
        downstairs = negative_list

        if len(upstairs) > 1:
            up = CommAssoc('*', upstairs)
        elif len(upstairs) == 1:
            up = upstairs[0]
        else:
            up = num1

        if len(downstairs) > 1:
            down = CommAssoc('*', downstairs)
            return Container('/', (up, down))
        elif len(downstairs) == 1:
            down = downstairs[0]
            return Container('/', (up, down))
        else:
            return up

    def sort(self, sp, with_div=True):
        complex_list = list()  # complexx numerator list
        positive_list = list()  # real numerator list
        negative_list = list()  # real denomanator(sp?) list
        for ex, exp in sp.exp_dict.items():
            if isinstance(exp, complex):
                complex_list.append(Container('**', (ex, Number(exp))))
            elif exp == 1:
                positive_list.append(ex)
            elif exp > 0:
                positive_list.append(Container('**', (ex, Number(exp))))
            elif exp == -1 and with_div:
                negative_list.append(ex)
            elif exp != 0 and with_div:
                negative_list.append(Container('**', (ex, Number(-exp))))
            elif exp != 0 and not with_div:
                negative_list.append(Container('**', (ex, Number(exp))))
            # Note: if exp == 0, then ex**0 is 1, and is igmored.
        return complex_list, positive_list, negative_list


class ConvertPlusBack(RuleBase):
    def predicate(self, expr):
        return isPl(expr)

    def body(self, plus):
        if plus.num:
            return CommAssoc('+', (Number(plus.num),) + plus.items)
        else:
            return CommAssoc('+', plus.items)


toform0 = Rules(
    step1_bu, step2_bu, 
    JustOneBU(ConvertToDiv(), ConvertPlusBack())
)


# More Shortcuts
# ==============
SP = StarPwr
PSP = PseudoStarPwr
Pl = Plus
PPl = PseudoPlus
