========
Settings
========
Perform the necessary Imports.

.. ipython::

    In [1]: import sys
       ...: from truealgebra.core.settings import(
       ...:     settings, bp 
       ...: ) 
       ...: from truealgebra.core import setsettings
       ...: from truealgebra.core.constants import (
       ...:     DIGITS, LETTERS, WHITE_SPACE, OPERATORS, META_DELIMITERS
       ...: ) 
       ...: from truealgebra.core import expressions as expr

From The module truealgebra.core.settings is imported the settings object which
is a singleton. 

.. ipython::

    In [1]: type(settings) 

The data inside seettings provides the envioroment for a truealgebra session.
It primarily controls the parsing that creates truealgebra expressions from
python strings.

To avoid confuion, for a truealgebra session, there should be only one
environment. At the beginning of a truealgebra session the settings should
be adjusted as desired at the beginning of the session and kept unchanged
throughout the rest of the session.

Constants
=========

The five python constants shown below are used during parsing or when a user
manually creates truealgebra expressions. The first three constants are
required knowledge for a user writing code to instantiate expressions through
application of a rule.

.. ipython::

    In [1]: print('DIGITS =  ' + str(DIGITS))
       ...: print('LETTERS =  ' + str(LETTERS))
       ...: print('OPERATORS =  ' + str(OPERATORS))
       ...: print('WHITE_SPACE =  ' + str(WHITE_SPACE))
       ...: print('META_DELIMITERS =  ' + str(META_DELIMITERS))

These constant are sets and the characters are printed without order. The 
``settings.DIGITS`` set contains the digits 0 through 9.
The ``settings.LETTERS`` set contains the lower and upper case alphabet
characters as well as the number sign and underscore characters.


Definitions
===========
In order to facilitate the discussion, the following definitions have been made.

.. _binding-power-label:

Binding Power
-------------
A binding power is a python object of type int and equal to or greater than 0. Binding powers are used during parsing.

Every truealgebra expression has two binding powers assigned to lbp (*left binding power*) and rbp (*right binding power*) attributes. These attributes can be either class or instance attributes. See :ref:`lbp and rbp attributes<lbp-and-rbp-attributes-label>`.

.. _symbol-name-label:

Symbol Name
-----------
A symbol name is a nonempty python string made up of characters from the constants LETTERS and DIGITS. There is no limit on the length of a symbol name. The first character must be one of the characters in the set LETTERS.  The remaining characters can only be from the set LETTERS or the set DIGITS.

The :ref:`name attribute of a Symbol instance<symbol-class-label>` must be a symbol name.  A symbol name is also the :ref:`first naming convention <container-name-1-label>` for name attributes of Container instances.

.. _operator-name-label:

Operator Name
-------------
An operator name is a nonempty python string made up of characters from the set ``settings.OPERATORS``. Operator names are the :ref:`second naming convention <container-name-2-label>` for name attributes of Container instances.

Settings are python objects that should be modified as needed by users. 


bp
==
bp is a namedtuble, used  to create immutable objects that holds
left and right binding powers.

An instance of the bp named tuple class below, holds two binding powers. The object ``my_bp_tuple`` is a ``bp`` instance. The ``250`` parameter becomes the ``lbp`` attribute of the instance and the ``600`` parameter becomes the ``rbp`` attribute. The ``lbp`` stands for left binding power and ``rbp`` stands for right binding power.

.. ipython::

    In [1]: my_bp_tuple = bp(250, 600)
       ...: print(my_bp_tuple.lbp)
       ...: print(my_bp_tuple.rbp)

Settings Attributes
===================
The attributes of the settings object hold the actual data that is set. 

It is strongly recomended that users do not modify the attributes directly.
To prevent hidden errors that are difficult to debug, 
use the :ref:`set-functions-label`.

.. _default_bp-label:

default_bp
----------
This setting is used during parsing to provide the default left and right binding powers for Container instances with operator names. 

The ``default_bp`` settings attribute is a ``bp`` class instance containing two positive binding powers. The default value for ``default_bp`` is ``bp(250, 250)``.

.. ipython::

    In [1]: print(settings.default_bp)
       ...: settings.default_bp = bp(275, 276)
       ...: print(settings.default_bp)


.. _custom_bp-label:

custom_bp
---------
The ``custom_bp`` setting is used during parsing to specify custom binding powers for Container instances with operator names to be parsed as operators.

The ``custom_bp`` attribute is a dictionary which by default is empty. A dictionary key must be an operator name. A dictionary values must be an instance of ``bp`` containing two binding powers. Both binding powers cannot be 0. If the dictionary key is also a key for ``settings.infixprefix`` then both binding powers must be positive.

.. ipython:: 

    In [1]: print(settings.custom_bp)
       ...: settings.custom_bp['*'] = bp(400, 400)
       ...: settings.custom_bp['!'] = bp(600, 0)
       ...: print(settings.custom_bp)


.. _infixprefix-label:

infixprefix
-----------
The ``infixprefix`` settings attribute is used during parsing to specify Container instances that can be both infix and prefix operators. 

This setting is a dictionary and by default it is empty. A dictionary key must be an operator name. The dictionary value must be a positive binding power. The infix form of the Container instance must have both binding powers positive.

.. ipython::

    In [1]: print(settings.infixprefix)
       ...: settings.infixprefix['-'] = 800
       ...: print(settings.infixprefix)


.. _symbol_operators-label:

symbol_operators
----------------
This setting is used during parsing to specify Container instances with symbol names that will be parsed as operators.

The ``symbol_operator`` setting is a dictionary which by default is empty. The dictionary key must be a symbol name. The dictionary value must be a ``settings.bp`` instance that contains two binding powers. Both binding powers cannot be 0. A dictionary key cannot also be a key in ``settings.bodied_functions``.

.. ipython::

    In [1]: print(settings.symbol_operators)
       ...: settings.symbol_operators['and'] = bp(325, 425)
       ...: print(settings.symbol_operators)


.. _bodied_functions-label:

bodied_functions
----------------
The ``bodied_functions`` setting is used during parsing to specify Container instances that will parsed as bodied functions.

The ``bodied_functions`` setting is a dictionary which is by default empty. A dictionary key must be an symbol name. A dictionary value must be a positive integer.Both binding powers cannot be 0. A dictionary key cannot also be a key in ``settings.symbol_operators``.

.. ipython::

    In [1]: print(settings.bodied_functions)
       ...: settings.bodied_functions['D'] = 100
       ...: print(settings.bodied_functions)


.. _container_subclass-label:

container_subclass
------------------
The ``container_subclass`` setting links name attributes with Container subclasses. This setting is used during parsing when Container instances are instantiated.

This setting is a dictionary that is by default empty. The dictionary key must be symbol or operator name. The dictionary value must be a Container subclass.

.. ipython::

    In [1]: print(settings.container_subclass)
       ...: settings.container_subclass['*'] = expr.CommAssoc
       ...: print(settings.container_subclass)

.. _complement-label:

complement
-----------
The ``complement`` setting is used to specify an attribute name of a Container instance that complements an attribute name of a CommAssoc instance. During parsing, A Container instance will be converted to a CommAssoc instance that it complements.

The ``complement`` setting is a dictionary that is by default empty. A dictionary key must be either a symbol name or operator name. The dictionary value must be a ``settings.commassoc_tuple`` named tuple instance.

The name attribute of the named tuple must also be the name attribute of CommAssoc instances. The identity attribute of the named tuple must be an expression that represents the mathematical identity of the mathematical operation represented by the CommAssoc instances.

The string ``'*'``,  was assigned :ref:`above<container_subclass-label>` as an attribute name for CommAssoc instances. 

In the example below, Container instances with a attribute name of ``'star'`` complement CommAssoc instances with name ``'*'``.

SKIP::

    .. ipython::

        In [1]: print(settings.complement)
           ...: settings.complement['star'] = settings.commassoc_tuple(
           ...:     name='*',
           ...:     identity=expr.Number(1),
           ...: ) 
           ...: print(settings.complement)


.. _container_categories-label:

container_categories
--------------------
The ``container_categories`` setting can used by rules to identify the name attribute of Container instances that fall in a particular category. Categories are strings and there are no predefined categories. Any string can be used for a category.

Consider the example below where the category is ``suchthat_names``. Any Container instance with a name attribute in the set  ``settings.container_categories['suchthat_names']`` is said to be in the ``suchthat_names`` category. A rule that has been written for the ``suchthat_names`` category would apply to Container instances with a name attribute of ``':'`` or ``'|'``.

The ``container_types`` setting is a default dictionary with a default value of an empty set. The *truealgebra.core.settings* module initializes an empty dictionary. Every dictionary key must be a string.  Every dictionary value is a set that can contain only symbol names or operator names.

SKIP::

    .. ipython::

        In [1]: print(settings.container_categories)
           ...: settings.container_categories['suchthat_names'].add('|')
           ...: settings.container_categories['suchthat_names'].add(':')
           ...: print(settings.container_categories)


Setting Tools
=============
The setting tools are functions related to the environment settings. Setting tools are found in the module *truealgebra.core.setting_tools*.

Utility Functions
-----------------

clear_settings()
    Returns all settings to their default value. This function is especially helpful with unit tests.

isbindingpower(num)
    Returns True if ``num`` is a binding power, otherwise returns False.

issymbolname(name)
    Returns True if ``name`` is a symbol name, otherwise returns False.
    
isoperatorname(name)
    Returns True if ``name`` is an operator name, otherwise returns False.


.. _set-functions-label:

Set Functions
-------------

In the following function definitions, the parameters ``lbp`` and ``rbp`` stand for left and right binding power. If mistakes are made when using these functions, error messages will be printed and no cahnges to the settings will be made,


set_default_bp(lbp, rbp)
    Assigns new named tuple settings.bp instance for setting :ref:`settings.default<default_bp-label>`. The parameters ``lbp`` and ``rbp`` must be positive binding powers.


set_custom_bp(name, lbp, rbp)
    Add or reassign key to :ref:`settings.custom_bp<custom_bp-label>` dictionary. The key is the parameter ``name`` which must be an operator name. The parameters ``lbp`` and ``rbp`` must be binding powers. Both ``lbp`` and ``rbp`` cannot be 0.


set_infixprefix (name, rbp)
    Add or reassign key to :ref:`settings.infixprefix<infixprefix-label>` dictionary. The key is the parameter ``name`` which must be an operator name. The parameter ``rbp`` must be a positive binding power. The infix form of the ``name`` must have both binding powers positive.


set_symbol_operators (name, lbp, rbp)
    Add or reassign key to :ref:`settings.symbol_operators<symbol_operators-label>` dictionary. The key is the parameter ``name`` which must be a symbol name. The parameter ``name`` cannot be a key in the setting ``settings.bodied_functions`` dictionary. The parameters ``lbp`` and ``rbp`` must be binding powers. Both ``lbp`` and ``rbp`` cannot be 0.


set_bodied_functions(name, rbp)
    Add or reassign key to :ref:`settings.bodied_function<bodied_functions-label>` dictionary. The key is the parameter ``name`` which must be a symbol name. The parameter ``name`` cannot be a key in the setting ``settings.symbol_operators`` dictionary. The parameters ``rbp`` must be a positive binding power.
    

set_container_subclass(name, cls)
    Add or reassign key to :ref:`settings.container_subclass<container_subclass-label>` dictionary. The key is the parameter ``name`` which must be a symbol name or an operator name.  The parameter ``cls`` must be a Container subclass.
    

set_complement(complement_name, commassoc_name, identity)
    Add or reassign key to :ref:`settings.complement<complement-label>` dictionary. The key is the parameter ``complement_name`` which must be a symbol name or an operator name. The parameter ``commassoc_name`` must be a key in ``settings.container_subclass`` pointing to CommAssoc.
    The parameter ``identity`` must be a truealgebra expression.


set_container_categories(category, name)
    Add or reassign key to :ref:`settings.container_categories<container_categories-label>` dictionary. The key is the parameter ``catgegory`` which must be a string. The parameter ``name`` which must be  symbol name or operator name is  the corresponding value 
    

.. rubric:: Set Function Error Example

All three parameters of ``settingst.set_custom_bp`` have flaws. Error messages are printed and no changes made to the setting ``settings.custom_bp``.

.. ipython::

    In [1]: print('custom_bp=  ' + str(settings.custom_bp))
       ...: setsettings.set_custom_bp('q@d$', -300, 'four')
       ...: print('custom_bp=  ' + str(settings.custom_bp))


