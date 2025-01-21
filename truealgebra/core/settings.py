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


# a bp object stores two binding powers
# bp works as the class in isinstace. Also I can make a suclass of it.
# bp appears to be like a class
bp = namedtuple("bp", ["lbp", "rbp"])


def noparse(anystring):
    ta_logger.log("Change settings.parse from noparse to something useful.")
    return None


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
    parse : None
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
        self.default_bp = bp(250, 250)
        self.custom_bp = dict()
        self.infixprefix = dict()
        self.symbol_operators = dict()
        self.bodied_functions = dict()
        self.container_subclass = dict()
        self.complement = dict()
        self.categories = defaultdict(set)
        self.categories['suchthat'].add('suchthat')
        self.categories['forall'].add('forall')
        self.parse = noparse
        self.unparse = None
        self.float_class = None
        self.integer_class = None


settings = SettingsSingleton()
