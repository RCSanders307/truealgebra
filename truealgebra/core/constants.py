"""
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
"""
# These are the constants, used mostly in truealgebra.core.parser
# These constants should not be changed
DIGITS = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
LETTERS = set([
    "_", "A", "a", "B", "b", "C", "c", "D", "d", "E", "F", "G", "H", "I",
    "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W",
    "X", "Y", "Z", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
    "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
])
WHITE_SPACE = set([" ", "\t"])
OPERATORS = set([
    ":",  "\\",  "*", "+", "-", '"', "^", "&", "%", "@", "!", "~", "/",
    "?", "<", ">", "=",  "`",  "|"
])
META_DELIMITERS = set(["\n", ";"])


# utility functions
def isbindingpower(num):
    """ Determine if argument is a binding power.

    num : int :
        Evaluate if num can be a binding power.
    """
    return isinstance(num, int) and 0 <= num


def issymbolname(name):
    """ Determines symbol name.

    name : str
        Evaluate if name is a symbol name

    """
    if not isinstance(name, str):
        return False
    try:
        if name[0] not in LETTERS:
            return False
    except IndexError:
        return False
    for nam in name[1:]:
        if nam not in LETTERS and nam not in DIGITS:
            return False
    return True


def isoperatorname(name):
    """ Determines operator name.

    name : str
        Evaluate if name is a operator name
    """
    if not isinstance(name, str):
        return False
    try:
        if name[0] not in OPERATORS:
            return False
    except IndexError:
        return False
    for nam in name[1:]:
        if nam not in OPERATORS:
            return False
    return True
