""" expression module

ExprBase match methods
----------------------
The purpose of a match method is to match a pattern (represented by self)
to an expression which can be called the target.
A NaturalRule and HalfNaturalRule instance initiate a call
to the match method of its pattern. The match method of Container instances
can call match the method of its sub-expressions.
There are four parameters besides self in all match methods:

self : ExprBase
    Self represents the pattern or a sub-expression of the pattern.
subdict : dict
    Created empty at the very beginneng of a matching process.
    If a variable from vardict is found to match an expression,
    it becomes a subdict key and its value becomes the expression
vardict : dict
    vardict is created by a NaturalRule instance.
    It was the var_defn attribute of a NaturalRule instance
    vardict is not modified during the matching process.
    vardict keys are Symbol instances and are called variables.
    vardict values are either a predicate expression
    or the null expression. A predicate expression can be evaluated
    to a truealgebra true or false.
pred_rule : RuleBase
    pred_rule evalutes the predicate expressions in vardict
expr : ExprBase
    Called the target that is being matched to the pattern.
    All sub-expressions in the target expr must be found
    to match the corresponding sub-expression in the pattern self.

A match method will return True or False and in some cases
will modify the subdict dictionary.

"""
from truealgebra.core.rulebase import Substitute, TrueThing
from truealgebra.core.constants import isoperatorname, issymbolname
from truealgebra.core.err import ta_logger


class TrueThingCAM(TrueThing):
    """Used with CommAssocMatch instances.
    """
    def __init__(self, subdict, target_list):
        self.subdict = subdict
        self.target_list = target_list


class UnParse():
    """
    string
        string reprecentaion of a truealgebra expression
    albp and arbp
        apparent binding powers used to determine if string
        should be inside parenthesis if it is contained inside
        another expression.

        albp and arbp are always 0 except in the two cases below

    albp
    ----
        * The string attribute presents a sequence of two or more tokens
        containing operators.
        * The first token of the sequence is complete, (rlb, lbp =  0, 0)
        * The second token of the sequence is an operator with a nonzero lbp
        * The second token's lbp becomes the UnParse instance albp

    A parenthesis pair is required if
        [containing expression rbp] > [child expression albp]

    albp
    ----
        * The string attribute presents a sequence of two or more tokens
        containing operators.
        * The last token of the sequence is complete, (rlb, lbp =  0, 0).
        * The second to last token of the sequence
        is an operator with a nonzero lbp.
        * The second to last  token's rbp becomes the UnParse instance arbp.

    A parenthesis pair is required if
        [child expression arbp] <= [containing expression lbp]

    CommAssoc Instances
    -------------------
    If the string attribute represents a child expression inside a
    CommAssoc instance of two or more arguments the situation is similar.
    The albp and arbp are defined in the same manner.
    The albp and arbp are compared to the CommAssoc instance binding powers
    to determine if a pair of parenthesis are required
    around the child expression.
    """
    def __init__(self, string, albp=0, arbp=0):
        self.string = string
        self.albp = albp
        self.arbp = arbp


class ExprBase(object):
    """ Base Class for Representing mathematic expressions
        instances of subclasses are called expressions

    Attributes:
        lbp     left binding power,
                used when parsing python strings to create expressions
        rbp     right binding power,
                used when parsing python strings to create expressions
        name    python string, such as symbol name, function name
        value   number of varied type, such as float, int, complex, fraction?
        items   tuple, containing other expressions

    """
    settings = None
    name = ""
    value = None
    items = None
    lbp = 0     # left binding power
    rbp = 0     # right binding power

    def __setattr__(self, name, value):
        if name in ('lbp', 'rbp', 'settings'):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError("This object should not be mutated")

# googled the subject. Not sure if this is needed.
    def __delattr__(self, name, value):
        raise AttributeError("This object should not be mutated")

    def __bool__(self):
        return True

    def bottomup(self, rule):
        return rule(self, _pathinhibit=True, _buinhibit=True)

    def apply2path(self, path, rule, _buinhibit=False):
        if path:
            ta_logger.log("Path too long, cannot enter atom expressions.")
            return null
        return rule(self, _pathinhibit=True, _buinhibit=_buinhibit)

    def match(self, vardict, subdict, pred_rule, expr):
        return self == expr

    def __eq__(self, other):
        return (
            self.name == other.name
            and type(self) == type(other)
            and self.value == other.value
        )

    def __hash__(self):
        return hash((type(self), self.name, self.value))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return " <EXPR> "

    def __str__(self):
        if self.settings is None:
            return self.__repr__()
        else:
            return self._unparse().string

    def _unparse(self):
        return UnParse(" <EXPRBASE> ")

    def strr(self):
        return self._unparse().string


class Null(ExprBase):

    def __repr__(self):
        return " <NULL> "

    def __bool__(self):
        return False

    def _unparse(self):
        return UnParse(" <NULL> ")


null = Null()


class End(ExprBase):
    name = "end"

    def __repr__(self):
        return " <END> "

    def _unparse(self):
        return UnParse(" <END> ")


end = End()


class Number(ExprBase):
    def __init__(self, value):
        object.__setattr__(self, "value", value)

    def __repr__(self):
        return repr(self.value)

    def _unparse(self):
        return UnParse(str(self.value))


class Symbol(ExprBase):
    def __init__(self, name=""):
        object.__setattr__(self, "name", name)

    @classmethod
    def isspecialsymbol(cls, expr):
        return (
            isinstance(expr, cls)
            and len(expr.name) >= 2
            and expr.name[:2] == '__'
        )

    def __repr__(self):
        return self.name

    def _unparse(self):
        return UnParse(self.name)

    def match(self, vardict, subdict, pred_rule, expr):
        if self in vardict:
            return self.match_variable(vardict, subdict, pred_rule, expr)
        else:
            return self == expr

    def match_variable(self, vardict, subdict, pred_rule, expr):
        """Find a pattern match when the Symbol instance is in self.vardict.

        The input parameters and purpose are described in the module docstring.
        """
        if self in subdict:
            return subdict[self] == expr
        elif vardict[self]:
            pred_subdict = {self: expr, any__: expr}
            sub_rule = Substitute(subdict=pred_subdict, bottomup=True)
            pred_eval = pred_rule(sub_rule(vardict[self]))
            if pred_eval == true:
                subdict[self] = expr
                return True
            else:
                return False
        else:
            subdict[self] = expr
            return True


# truealgebra boolean expressions
true = Symbol('true')
false = Symbol('false')

# special symbol used
# when substituting into predicates during pattern matching
any__ = Symbol('__any')


class Container(ExprBase):
    def __init__(self, name, items=(), lbp=None, rbp=None):
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "items", tuple(items))
        if lbp is not None:
            object.__setattr__(self, "lbp", lbp)
        if rbp is not None:
            object.__setattr__(self, "rbp", rbp)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, item):
        return self.items[item]

    def __iter__(self):
        for item in self.items:
            yield item

    def __repr__(self):
        out = self.name + "("
        if self.items:
            out = out + repr(self.items[0])
            for item in self.items[1:]:
                out += ', ' + repr(item)
        return out + ")"

    def bottomup(self, rule):
        return rule(
            self.__class__(
                self.name,
                tuple([item.bottomup(rule) for item in self.items])),
            _pathinhibit=True,
            _buinhibit=True)

    def apply2path(self, path, rule, _buinhibit=False):
        if not path:
            return rule(self, _pathinhibit=True, _buinhibit=_buinhibit)
        try:
            nxt = path[0]
            path = path[1:]
            result = self[nxt].apply2path(path, rule, _buinhibit=_buinhibit)
            newitems = (self[:nxt] + (result,) + self[nxt:][1:])
            return self.__class__(self.name, newitems)
        except IndexError:
            ta_logger.log("index error in path")
            return null
        except TypeError:
            ta_logger.log("type error in path")
            return null

    def __eq__(self, other):
        if (
            self.name != other.name
            or type(self) != type(other)
            or len(self) != len(other)
        ):
            return False
        else:
            for ndx, item in enumerate(self):
                if item != other[ndx]:
                    return False
        return True

    def __hash__(self):
        return hash((
            self.name,
            type(self),
            len(self),
            tuple(map(hash, self.items)),
        ))

    def match(self, vardict, subdict, pred_rule, expr):
        if (
            type(expr) != type(self)
            or expr.name != self.name
            or len(expr) != len(self)
        ):
            return False

        iterexpr = iter(expr)
        for item in self:
            if not item.match(vardict, subdict, pred_rule, next(iterexpr)):
                return False
        return True

    def _append_item(self, item):
        """ Used only in parsing"""
        object.__setattr__(self, "items", self.items + (item,))

    def _bind_left(self, token):
        """ Used only in parsing"""
        self.lbp = 0
        object.__setattr__(self, "items", (token,) + self.items)

    def _bind_right(self, token):
        """ Used only in parsing"""
        self.rbp = 0
        object.__setattr__(self, "items", self.items + (token,))

    def _unparse(self):
        """
        The 'a' in variables albp and arbp,
        stands for apparent binding power.
        An operator (called parent) can have a left and a right argument.
        the apparent binding powers of parent, left, and right
        determine if an argument must be put inside parenthesis

        The left and right are complete Unparse instances.
        The parent unparse instance will be modified as needed
        left and right are or will be children of parent.
        """
        if isoperatorname(self.name):
            left, parent, right = self._unparse_operatorname()
        elif self.name in self.settings.symbol_operators:
            left, parent, right = self._unparse_operatorname()
        else:
            # This is a catch all.
            # Names that are not symbol names are sent here.
            left, parent, right = self._unparse_symbolname()
        return self._unparse_parenthesis_or_not(left, parent, right)

    def _unparse_parenthesis_or_not(self, left, parent, right):
        # In paarsing, the left operator wins ties.
        # In unparsing, that must be remebered
        if parent.albp:
            if left.arbp and left.arbp < parent.albp:
                left.string = '(' + left.string + ')'
            elif left.albp:
                parent.albp = left.albp
            parent.string = left.string + parent.string
        if parent.arbp:
            if right.albp and parent.arbp >= right.albp:
                right.string = '(' + right.string + ')'
            elif right.arbp:
                parent.arbp = right.arbp
            parent.string = parent.string + right.string
        return parent

    def _unparse_find_albp_arbp(self):
        if self.name in self.settings.infixprefix and len(self.items) == 1:
            albp, arbp = 0, self.settings.infixprefix[self.name]
        elif self.name in self.settings.custom_bp:
            albp, arbp = self.settings.custom_bp[self.name]
        elif self.name in self.settings.symbol_operators:
            albp, arbp = self.settings.symbol_operators[self.name]
        else:
            albp, arbp = self.settings.default_bp
        return (albp, arbp)

    def _unparse_operatorname(self):
        albp, arbp = self._unparse_find_albp_arbp()
        left, right = None, None

        if albp and arbp and len(self.items) == 2:
            left = self.items[0]._unparse()
            right = self.items[1]._unparse()
            parent = UnParse(' ' + self.name + ' ', albp, arbp)
        elif albp and not arbp and len(self.items) == 1:
            left = self.items[0]._unparse()
            parent = UnParse(' ' + self.name, albp, arbp)
        elif not albp and arbp and len(self.items) == 1:
            right = self.items[0]._unparse()
            parent = UnParse(self.name + ' ', albp, arbp)
        else:
            # This option is for when there is an error
            # The albp and arbp do not match the number of items
            parent = self._unparse_function_notation(self)

        return (left, parent, right)

    def _unparse_function_notation(self, items=None):
        if items is None:
            items = [item._unparse() for item in self.items]
        else:
            items = [item._unparse() for item in items]
        out = self.name + "("
        for item in items[:1]:
            out += item.string
        for item in items[1:]:
            out += ", " + item.string
        return UnParse(out + ")")

    def _unparse_symbolname(self):
        left, right = None, None
        if self.name in self.settings.bodied_functions and len(self.items):
            parent = self._unparse_function_notation(self.items[:-1])
            if len(self.items) >= 2:
                parent.string = parent.string + ' '
            parent.arbp = self.settings.bodied_functions[self.name]
            right = self.items[-1]._unparse()
        else:
            parent = self._unparse_function_notation()

        return (left, parent, right)


# this has not been completely unit tested
class Assign(Container):
    """Assign class instance and used to modify the Assign_Rule instances 
    inside instanes fo FrontEnd.
    """

    def bottomup(self, rule):
        newitems = list(self.items[:-1])
        try:
            newitems.append(self.items[-1].bottomup(rule))
        except IndexError:
            ta_logger.log("Assigned requires at least one argument")
            return null
        return rule(
            self.__class__(self.name, newitems),
            _pathinhibit=True,
            _buinhibit=True
        )
# you can Yank from anywhere, the Put is restricted

    def apply2path(self, path, rule, _buinhibit=False):
        if not path:
            return rule(self, _pathinhibit=True, _buinhibit=_buinhibit)
        try:
            nxt = path[0]
            path = path[1:]
            if nxt == -1 or nxt == len(self.items) - 1:
                result = self[nxt].apply2path(
                    path, rule, _buinhibit=_buinhibit
                )
                newitems = (self[:nxt] + (result,))
                return self.__class__(self.name, newitems)
            else:
                ta_logger.log("Assign argument closed to bottomup")
                return null
        except IndexError:
            ta_logger.log("index error in path")
            return null
        except TypeError:
            ta_logger.log("type error in path")
            return null

    def match(self, vardict, subdict, pred_rule, expr):
        """ match cannot enter protected items.
        This prevents NaturalRules from being applied inside
        """
        if (
            type(expr) != type(self)
            or expr.name != self.name
            or len(expr) != len(self)
        ):
            return False

        if len(self) == 0:
            return True
        if not self[0].match(vardict, subdict, pred_rule, expr[0]):
            return False
        for ndx, item in enumerate(self[1:]):
            if item != expr[1:][ndx]:
                return False
        return True


class CommAssoc(Container):
    def __hash__(self):
        # another way to hash the self.items is to use the xor function ^
        # xor is both associative and communative
        return hash((
            type(self),
            self.name,
            tuple(sorted(map(hash, self.items)))
        ))

    def __eq__(self, other):
        if (self.name != other.name
                or type(self) != type(other)
                or len(self) != len(other)):
            return False
        else:
            return self.inner_eq(list(self.items), list(other.items))

# this is perhaps not the most clear or effecient method
# This will work quickly if self.items and other.items are ordered the same
    def inner_eq(self, selflist, otherlist):
        if not selflist:
            return True
        for item in selflist:
            ndx = -1
            for nndex, otem in enumerate(otherlist):
                if otem == item:
                    ndx = nndex
                    break
            if ndx == -1:
                return False
            del otherlist[ndx]
        return True

    def _unparse(self):
        operbp = None
        if isoperatorname(self.name):
            if self.name in self.settings.custom_bp:
                operbp = self.settings.custom_bp[self.name]
            else:
                operbp = self.settings.default_bp
            return self._unparse_commassoc(operbp)
        elif (
            issymbolname(self.name)
            and self.name in self.settings.symbol_operators
        ):
            operbp = self.settings.symbol_operators[self.name]
            return self._unparse_commassoc(operbp)
        else:
            return self._unparse_function_notation()

    def _unparse_commassoc(self, operbp):
        gap = " "
        items = [item._unparse() for item in self.items]

        # look at the beginning of items
        # settings needs to include the identity for when length = 0
        if not items:
            return self._unparse_function_notation()
        elif len(items) == 1:
            return items[0]
        # during parsing, a left operator wins ties with a right operator.
        # during unparsing, if arbp were to lose, a parenthesis is required
        elif items[0].arbp and items[0].arbp < operbp.lbp:
            outstr = "(" + items[0].string + ")" + gap
            albp = operbp.lbp
        else:
            outstr = items[0].string + gap
            if items[0].albp:
                albp = items[0].albp
            else:
                albp = operbp.lbp
        # look at the middle of items
        for item in items[1:-1]:
            if (
                 (item.albp and operbp.rbp >= item.albp)
                 or (item.arbp and item.arbp < operbp.lbp)
            ):
                outstr += self.name + gap + "(" + item.string + ")" + gap
            else:
                outstr += self.name + gap + item.string + gap

        # look at the end of items
        if items[-1].albp and operbp.rbp >= items[-1].albp:
            outstr += self.name + gap + "(" + items[-1].string + ")"
            arbp = operbp.rbp
        else:
            outstr += self.name + gap + items[-1].string
            if items[-1].arbp:
                arbp = items[-1].arbp
            else:
                arbp = operbp.rbp

        return UnParse(outstr, albp, arbp)

    def match(self, vardict, subdict, pred_rule, expr):
        if (
            type(expr) != type(self)
            or expr.name != self.name
        ):
            return False

        cam = CommAssocMatch(self, vardict, subdict, pred_rule, expr)
        return cam.find_matches()


class CommAssocMatch:
    def __init__(self, pattern, vardict, subdict, pred_rule, target):
        self.pattern = pattern
        self.vardict = vardict
        self.subdict = subdict
        self.pred_rule = pred_rule
        self.target_list = list(target.items)

    def find_matches(self):
        """Find matches for all items in pattern.items where pattern is a
        CommAssoc instance. Each item is put into one of the three lists:

        special_list :
            items that are variables (keys in vardict) and special symbols.
        pattern_list :
            items that contain at least one variable.
        plain_expr_list :
            items that contain no variables

        When a match is made, the ouput is True, otherwise False.
        When a match is made, the following attributes are modified:

        self.target_list :
            The target item that is matched is removed
        self.subdict
            When a variable that is not a key in self_subdict, is matched
            to an expression expr, then self,subdict is updated
            ``self.subdict[varianble] = expr``.
        """
        special_list = list()
        pattern_list = list()
        plain_expr_list = list()

        for pattern in self.pattern:
            if Symbol.isspecialsymbol(pattern) and pattern in self.vardict:
                special_list.append(pattern)
            elif self.does_contain_variable(pattern):
                pattern_list.append(pattern)
            else:
                plain_expr_list.append(pattern)

        if not self.process_plain_expr_list(plain_expr_list):
            return False

        if pattern_list and not self.process_pattern_list(pattern_list):
            return False

        if not self.process_special_list(special_list):
            return False

        return not self.target_list

    def process_plain_expr_list(self, plain_expr_list):
        """ process matches of plain expressions that contain no variables
        in plain_expr_list
        """
        for expr in plain_expr_list:
            if not self.plain_expr_match(expr):
                return False
        return True

    def plain_expr_match(self, expr):
        """ finds match for expression that conatins no variables
        """
        for ndx, item in enumerate(self.target_list):
            if expr == item:
                del self.target_list[ndx]
                return True
        return False

    def process_pattern_list(self, pattern_list):
        """ process matches for items in pattern_list which contain
        one or more variables.
        """
        truething = self.pattern_match(
            pattern_list,
            self.subdict,
            self.target_list
        )
        if truething:
            self.subdict |= truething.subdict
            self.target_list.clear()
            self.target_list.extend(truething.target_list)
            return True
        return False

    def pattern_match(self, pattern_list, subdict, target_list):
        """ Recursive method to find matches for a list of patterns.

        pattern_list : list,
            Items of the list are truealgebra expressions that contain at
            least one variable.

            All patterns in pattern_list must be matched. When sucessful,
            one method called for every pattern. Multiple method calls may
            be required to try all possible combinations.
        subdict : dict
            Subsitution dictionary. When an instance is called, it creates
            local_subdict, a copy of subdict. When a match is found,
            local_subdict is updated.
        target_list : list
            Contains truealgebra expressions to be matched to the patterns.
            Not all targets must be matched.

        Outputs
        -------
        False
            Output when not all patterns have been matched.
        TrueThingCAM instance
            The output is truthy. Its subdict attribute is the substitution
            dictionary resulting from the matches. Its target_list attribute
            conatins targets not matched.
        """
        local_subdict = subdict.copy()
        pattern = pattern_list[0]
        pattern_list = pattern_list[1:]

        for ndx, target in enumerate(target_list):
            match = pattern.match(
                self.vardict, local_subdict, self.pred_rule, target
            )
            if match and pattern_list:
                new_target_list = target_list.copy()
                del new_target_list[ndx]
                truething = self.pattern_match(
                    pattern_list,
                    local_subdict,
                    new_target_list
                )
                if truething:
                    return truething
                else:
                    local_subdict = subdict.copy()  # restart search
            elif match:
                del target_list[ndx]
                return TrueThingCAM(local_subdict, target_list)
        return False

    def process_special_list(self, special_list):
        """ process matches of special symbols in the special_list
        """
        for symbol in special_list:
            if not self.special_match(symbol):
                return False
        return True

    def special_match(self, symbol):
        """symbol must be a special symbol that is a key in self.vardict
        """
        if self.vardict[symbol]:
            new_target_list = list()
            instance_items = list()
            for item in self.target_list:
                sub_rule = Substitute(
                    subdict={symbol: item, any__: item},
                    bottomup=True
                )
                if self.pred_rule(sub_rule(self.vardict[symbol])) == true:
                    instance_items.append(item)
                else:
                    new_target_list.append(item)
            self.target_list = new_target_list
        else:
            instance_items = self.target_list
            self.target_list = list()
        if len(instance_items) < self.find_minimum_length(symbol):
            return False
        instance = CommAssoc(self.pattern.name, instance_items)
        if symbol in self.subdict:
            return instance == self.subdict[symbol]
        self.subdict[symbol] = instance
        return True

    def find_minimum_length(self, symbol):
        """find and output minimum length coded in special name.
        """
        digits = ''
        for char in symbol.name[2:]:
            if char.isdigit():
                digits += char
            else:
                break
        if digits:
            return int(digits)
        else:
            return 0

    def does_contain_variable(self, expr):
        """ determines if expr contains a variable
        """
        if expr in self.vardict:
            return True
        elif isinstance(expr, Container):
            for item in expr:
                if self.does_contain_variable(item):
                    return True
            return False
        else:
            return False


# used with units and complete_natural/-rule
class Restricted(Container):

    def bottomup(self, rule):
        return rule(self, _pathinhibit=True, _buinhibit=True)

    def apply2path(self, path, rule, _buinhibit=False):
        if path:
            ta_logger.log("path cannot enter Restricted instnce")
            return null
        else:
            return rule(self, _pathinhibit=True, _buinhibit=True)

    def match(self, vardict, subdict, pred_rule, expr):
        """ match cannot enter inside the content of individual items
        To do so would allow a NaturalRule rule to be applied inside.
        for example when a Resricted instance represents units.
        """
        return self == expr
