from truealgebra.core.err import ta_logger
from truealgebra.core.expressions import Container, null
from truealgebra.core.constants import (
    isbindingpower, issymbolname, isoperatorname,
)
from truealgebra.core.settings import settings

def set_default_bp(lbp, rbp):
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
    settings.default_bp = bp(lbp, rbp)

def set_custom_bp(name, lbp, rbp):
    """ Add key and value pair to the settings.custom_bp dictionary.

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
    settings.custom_bp[name] = bp(lbp, rbp)

def set_infixprefix(name, rbp):
    """ Add key and value pair to the settings.infixprefix dictionary.

        name : str
            operator name that will be parsed as either an infix
            or prefix operator.
        rbp : int
            right binding power for prefix form.
    """
    if name in settings.custom_bp:
        bp = settings.custom_bp[name]
    else:
        bp = settings.default_bp
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

    settings.infixprefix[name] = rbp

def set_symbol_operators(name, lbp=None, rbp=None):
    """Specify Container instances that parse as mathematical operators.

    name : str
        name attribute of a Container instance.
    lbp : int
        left binding power
    rbp : int
        right binding power
    """
    if lbp is None:
        lbp = settings.default_bp.lbp
    if rbp is None:
        rbp = settings.default_bp.rbp

    bool_tuple = (
        not issymbolname(name),
        name in settings.bodied_functions,
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

    settings.symbol_operators[name] = bp(lbp, rbp)

def set_bodied_functions(name, rbp=None):
    """Set which Container instance will parse as a bodied function.

    name : str
        Container instance name attribute.
    rbp : int
        Right binding power for parsing purposes.
    """
    if rbp is None:
        rbp = settings.default_bp.rbp

    bool_tuple = (
        not issymbolname(name),
        name in settings.symbol_operators,
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

    settings.bodied_functions[name] = rbp

def set_sqrtneg1(a_string):
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

    settings.sqrtneg1 = a_string

def set_container_subclass(name, cls):
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

    settings.container_subclass[name] = cls

def set_complement(complementname, targetname):
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

    settings.complement[complementname] = targetname

def set_categories(category, name=None):
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

    set_ = settings.categories[category]
    if name is not None:
        set_.add(name)
