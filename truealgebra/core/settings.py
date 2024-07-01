"""
TrueAlgebra Settings
====================
This module contains constants, utility functions and the Settings class,
all used to control the operation of TrueAlgebra.

constants
---------
the intent is that constants are not changed.

digits : set containing str
    characters representing the 10 digits.
letters : set containing str
    upper and lower case letters and the character '_'.
operators : set containing str
    characters that can be used for name attribute of objects
    that represent mathematical operators.
white_space : set containing str
    space and tab characters.
meta_delimiters : set containing str
    new line and semicolon characters

definitions
-----------
binding power :
    a binding power must be an int instance and non-negative.

    the function isbindingpower returns true when applied to a binding power.
    binding powers are used in parsing python strings
    into truealgebra expressions.
    a binding power must be type int and equal to or greater than 0.
symbol name :
    a symbol name must be a string. the first character must be in letters.
    the remaining characters must be either in letters or digits.

    a string that returns true when evaluated by the method issymbolname.
    a symbol name can be the name attribute of a symbol instance.
    a symbol name can also be the name attribute of a container instance
    that normally has a function form when being parsed.
    an example of a function form is the string 'f(a, b c)',
    where 'f' is the name attribute attribute of a container instance.
operator name :
    an operator name must be a string with all of the characters in operators.

    a string that returns true when evaluated by the method isoperatorname.
    an operator name can be the name attribute of a container instance
    that is used to model a mathematical operator.
    for example in `2 + 3`, '+' is an operator name.

binding power named tuple
-------------------------
bp : namedtuple
    Contains left `lbp` and right `rbp` binding powers.
    This object used as a value in Settings dictionaries.
"""
from collections import namedtuple, defaultdict
from truealgebra.core.err import ta_logger
from truealgebra.core.expression import Container
from truealgebra.core.constants import (
    isbindingpower, issymbolname, isoperatorname,
)


# a bp object stores two binding powers
bp = namedtuple("bp", ["lbp", "rbp"])


def _msg_function(bool_tuple, msg_tuple, msg=''):
    for ndx, bool_value in enumerate(bool_tuple):
        if bool_value:
            msg += msg_tuple[ndx]
    return msg


class SettingsSingleton():
    """
    TrueAlgebra Settings
    --------------------
    A `setting` attribute can be changed by users
    using the methods named `set_<setting>`.
    All but the last setting `complement` is used during parsing.

    Settings Attributes
    -------------------
    default_bp : bp
        Default binding powers for
        objects that represent mathematical operators.

        the variable default_bp must point to a bp namedtuple
        The bp instance must contain two binding powers
        both binding powers cannot be 0
    custom_bp : dict
        Custom binding powers for Container objects with operator names.

        A key of custom_bp must be an operator name.
        A value of custom_bp must be a bp namedtuple.
        The bp instance must contain two binding powers.
        both binding powers cannot be 0.
    infixprefix : dict
        Designates operator names used as either infix or prefix operators.

        The key to infixprefix must be an operator name.
        The value of infixprefix must be a binding power greater than 0.
        right binding power of infix form cannot be 0.
        left binding power of infix form cannot be 0.
    symbol_operators : dict
        The keys are symbol names that will be operators during parsing.

        A key to symbol_operators must be a symbol name.
        The key cannot also be a key to bodied_functions.
        A value of symbol_operators must be a bp named tuple.
        The bp instance must contain two binding powers.
        both binding powers cannot be 0.
    bodied_functions : dict
        The keys are symbol names for bodied functions.

        A key to bodied_functions must be a symbol name.
        The key cannot be a key in the symbol_operator dictionary.
        The value to bodied_functions must be a positive binding power.
    sqrtneg1 : str
        indicates the square root of negative one.

        sqrtneg1 can only be '', 'i', or 'j'.
        If "",  there is no square root of negative one.
    container_subclass : dict
        Identifies Container subclass, based on name attribute.
        If a name is not in the dictionary, the name
        will be assigned to a Container class during parsing.

        A key can only be a symbol name or operator name
        The value must be a subclass of Container
    complement : dict
        During parsing, Container objects with a name that is a key
        in self.complement will be replaced by a container object with
        a name attribute equal to the corresponding dictionary value.

        Both keys and values of the dictionary must be either
        a symbol name or operator name.
    categories : defaultdict(set)
        This setting is for use by rules to identify categories of expressions.
        The content of the sets in the dictionary specify names attributes
        of Container instances that belong in the category.

        The keys must be a string. Any string will do.
        The values are sets. The contents of the sets must be either
        a symbol names or operator names.
        The set contents represent name attributes of Container instances.
    active_parse : None
        Points to Parse instance that will be used throughout a
        truealgebra session.

    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsSingleton, cls).__new__(cls)
            cls._instance.reset()
        return cls._instance

    def reset(self):
        self.custom_bp = dict()
        self.default_bp = bp(250, 250)
        self.infixprefix = dict()
        self.symbol_operators = dict()
        self.bodied_functions = dict()
        self.sqrtneg1 = ""
        self.container_subclass = dict()
        self.complement = dict()
        self.categories = defaultdict(set)
# THIS HAS YET TO BE TESTED
        self.categories['suchthat'].add('suchthat')
# THIS HAS YET TO BE TESTED
        self.categories['forall'].add('forall')
        self.active_parse = None

    def set_default_bp(self, lbp, rbp):
        """Set default binding powers for operators.

        lbp : str
            left binding power
        rbp : str
            right binding power
        """
        bool_tuple = (
            not isbindingpower(lbp),
            not isbindingpower(rbp),
            lbp == 0 and rbp == 0,
        )
        msg_tuple = (
            '\n    lbp {} must be a binding power'.format(lbp),
            '\n    rbp {} must be a binding power'.format(rbp),
            '\n    lbp and rbp cannot both be 0',
        )
        if any(bool_tuple):
            msg = _msg_function(
                bool_tuple,
                msg_tuple,
                msg='set_default_bp error'
            )
            ta_logger.log(msg)
            return
        self.default_bp = bp(lbp, rbp)

    def set_custom_bp(self, name, lbp, rbp):
        """ Add key and value pair to the self.custom_bp dictionary.

            name : str
                operator name.
            lbp : int
                left binding power.
            rbp : int
                right binding power.
        """
        bool_tuple = (
            not isoperatorname(name),
            not isbindingpower(lbp),
            not isbindingpower(rbp),
            lbp == 0 and rbp == 0,
        )
        msg_tuple = (
            '\n    name {} must be an operator name.'.format(name),
            '\n    lbp {} must be a binding power'.format(lbp),
            '\n    rbp {} must be a binding power'.format(rbp),
            '\n    lbp and rbp cannot both be 0',
        )
        if any(bool_tuple):
            msg = _msg_function(
                bool_tuple, msg_tuple, msg='set_custom_bp error'
            )
            ta_logger.log(msg)
            return
        self.custom_bp[name] = bp(lbp, rbp)

    def set_infixprefix(self, name, rbp):
        """ Add key and value pair to the self.infixprefix dictionary.

            name : str
                operator name that will be parsed as either an infix
                or prefix operator.
            rbp : int
                right binding power for prefix form.
        """
        if name in self.custom_bp:
            bp = self.custom_bp[name]
        else:
            bp = self.default_bp
        bool_tuple = (
            not isoperatorname(name),
            not (isbindingpower(rbp) and rbp >= 1),
            bp.lbp == 0,
            bp.rbp == 0,
        )
        msg_tuple = (
            'name {} must be an operator name'.format(name),
            'rbp {} must be a binding power greater than 0'.format(rbp),
            'left binding power of {} infix form cannot be 0'.format(name),
            'right binding power of {} infix form cannot be 0'.format(name),
        )
        if any(bool_tuple):
            msg = _msg_function(
                bool_tuple, msg_tuple, msg='set_infixprefix error\n    '
            )
            ta_logger.log(msg)
            return

        self.infixprefix[name] = rbp

    def set_symbol_operators(self, name, lbp=None, rbp=None):
        """Specify Container instances that parse as mathematical operators.

        name : str
            name attribute of a Container instance.
        lbp : int
            left binding power
        rbp : int
            right binding power
        """
        if lbp is None:
            lbp = self.default_bp.lbp
        if rbp is None:
            rbp = self.default_bp.rbp

        bool_tuple = (
            not issymbolname(name),
            name in self.bodied_functions,
            not isbindingpower(lbp),
            not isbindingpower(rbp),
            rbp == 0 and lbp == 0,
        )
        msg_tuple = (
            'name {} must be a symbol name.'.format(name),
            'name {} cannot be key in bodied_functions'.format(name),
            'lbp {} must be a binding power'.format(lbp),
            'rbp {} must be a binding power'.format(rbp),
            'lbp and rbp cannot both be 0'
        )
        if any(bool_tuple):
            msg = _msg_function(
                bool_tuple, msg_tuple, msg='set_symbol_operator error\n    '
            )
            ta_logger.log(msg)
            return

        self.symbol_operators[name] = bp(lbp, rbp)

    def set_bodied_functions(self, name, rbp=None):
        """Set which Container instance will parse as a bodied function.

        name : str
            Container instance name attribute.
        rbp : int
            Right binding power for parsing purposes.
        """
        if rbp is None:
            rbp = self.default_bp.rbp

        bool_tuple = (
            not issymbolname(name),
            name in self.symbol_operators,
            not isbindingpower(rbp) or rbp == 0,
        )
        msg_tuple = (
            'name {} must be a symbol name.'.format(name),
            'name {} cannot be key in symbol_operators'.format(name),
            'rbp {} must be a positive binding power'.format(rbp),
        )
        if any(bool_tuple):
            msg = _msg_function(
                bool_tuple, msg_tuple, msg='set_bodied_functions error\n    '
            )
            ta_logger.log(msg)
            return

        self.bodied_functions[name] = rbp

    def set_sqrtneg1(self, a_string):
        """Character representing square root of negative one.

        a_string : str
            'j' or 'k' will represent negative one
            '' implies there is no square root of neagtive one.
        """
        if a_string not in ('i', 'j', ''):
            msg = (
                'a_string {} cannot be used for '
                'square root of -1'.format(a_string)
            )
            ta_logger.log(msg)
            return

        self.sqrtneg1 = a_string

    def set_container_subclass(self, name, cls):
        """Assign name attributes for Container Subclasses

        name : str
            name attribute for Container subclass
        cls : class
            Container subclass
        """
        bool_tuple = (
            not issymbolname(name) and not isoperatorname(name),
            not issubclass(cls, Container),
        )
        msg_tuple = (
            'name {} must b a symbol or operator name'.format(name),
            'cls {} is not a Container subclass'.format(cls),
        )
        if any(bool_tuple):
            msg = _msg_function(
                bool_tuple, msg_tuple, msg='set_container_subclass error\n    '
            )
            ta_logger.log(msg)
            return

        self.container_subclass[name] = cls

    def set_complement(self, complementname, targetname):
        ''' Add key and value pair to the env.complement dictionary.

        complementname : str
            Dictionary key.
            Identifies Container objects named complementname.
        targetname : str
            Dictionary value.
            Identifies Container objects named targetname.

        During parsing, Container objects having a name of complementname are
        replaced by a corresponding Container object with the targetname.
        '''
        bool_tuple = (
            (
                not issymbolname(complementname)
                and not isoperatorname(complementname)
            ),
            not issymbolname(targetname) and not isoperatorname(targetname),
        )
        msg_tuple = (
            (
                'complementname {} must be a symbol '
                'or operator name'.format(complementname)
            ),
            'targetname {} must be a symbol '
            'or operator name'.format(targetname),
        )
        if any(bool_tuple):
            msg = _msg_function(
                bool_tuple, msg_tuple, msg='set_complement error\n    '
            )
            ta_logger.log(msg)
            return

        self.complement[complementname] = targetname

    def set_categories(self, category, name=None):
        """ Add key and value to the categories defaultdict dictionary.

            category : str
                Category
            name : str
                A Container name attribute that is in the category.
        """
        bool_tuple = (
            not isinstance(category, str),
            (
                not issymbolname(name)
                and not isoperatorname(name)
                and name is not None
            ),
        )
        msg_tuple = (
            'category {} must be a string instance'.format(category),
            'name {} must be an operator name or symbol name'.format(name),
        )
        if any(bool_tuple):
            msg = _msg_function(
                bool_tuple,
                msg_tuple,
                msg='set_categories error\n    '
            )
            ta_logger.log(msg)
            return

        set_ = self.categories[category]
        if name is not None:
            set_.add(name)


settings = SettingsSingleton()
