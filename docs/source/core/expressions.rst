===========
Expressions
===========
Import the necessary packages, modules, and objects.

.. ipython::

    In [1]: from truealgebra.core.rules import (
       ...:     Rule, Rules, RulesBU, JustOne, JustOneBU, Substitute,
       ...:     donothing_rule 
       ...: )
       ...: from truealgebra.core.naturalrules import (
       ...:     NaturalRuleBase, NaturalRule, HalfNaturalRule
       ...: )
       ...: from truealgebra.core.expressions import (
       ...:     ExprBase, Symbol, Number, true, false,
       ...:     Container,Restricted, Assign, End, CommAssoc,
       ...: ) 
       ...: from truealgebra.core.expressions import NullSingleton as Null
       ...: from truealgebra.core.settings import settings
       ...: from truealgebra.core import setsettings
       ...: from truealgebra.core.parse import Parse
       ...: from truealgebra.core.unparse import unparse 
       ...: from fractions import Fraction
       ...:
       ...:
       ...: settings.parse = Parse()
       ...: settings.unparse = unparse
       ...: setsettings.set_symbol_operators("and", 75, 75)
       ...: setsettings.set_custom_bp("=", 50, 50) 
       ...: setsettings.set_container_subclass("*", CommAssoc) 
       ...:
       ...: parse = settings.parse


Expressions are instances of the ExprBase class..

Expression Classes
===================
As explained above, Instances of ExprBase subclasses are called expression, and they are essentially the data of a TrueAlgebra computer algebra system.

The ExprBase subclasses used to represent mathematical expressions are Symbol, Number, Container, Restricted, Assign and CommAssoc. The subclass Null represents nothingness, much like the python None. The End subclass is used only during parsing to indicate the end of a sequence of tokens. 

In the future, additional classes may be created, for example to represent a matrix. The data structures of these subclasses are fairly simple. 

Creation of Expressions
-----------------------
There are two methods that can be used to create expressions. The preferred method is to use a Parser or Frontend class instance to take python strings that represent mathematical expressions and convert them into truealgebra expressions. This parsing method is much easier to use especially for complicated expressions. Syntax mistakes in the string will be automatically caught by the Parser instance. Below is a simple example of creating a truealgeba expression representing a parabolic equation.

.. ipython::

   In [1]: truealgebra_expression = parse(' 0 = x**2 + 2*x + 1 ')

The `truealgebra.std.env` module imported above set the truealgebra environment which determines, among other things, the parsing rules. The details of parsing will be discuss elsewhere in the documents.

The second method is to create a truealgbra expression by instantiating a ExprBase subclass. This method will be discussed in this section below and will help a person to understand how TrueAlgebra works. This second method is also required knowledge for writing new RuleBase subclasses to create new truealgebra rules.

Manually instantiating a ExprBase subclass is not a foolproof process. Mistakes can be made. In the Symbol Class section below for example The name attribute of a Symbol Class instance is intended to be a python string containing only certain specified characters. A user can manually instantiate a Symbol instance that has an incorrect name.  

Expression Attributes
---------------------

The data structure of ExprBase sub-classes is fairly simple and involves the following attributes:

name attribute :
    The name class attribute of ExprBase is a empty string ''. The Symbol and Container instances will have longer strings assign to their name instance attribute.

value attribute :
    ExprBase attaches None to the value class attribute. A Number class instance will have a python number object assigned to the value instance attribute.

items attribute :
    ExprBase assigns None to items class attribute. The Container instances have tuples for their items instance attribute that contain other expressions.

.. _lbp-and-rbp-attributes-label:

lbp and rbp attributes :
    The ExprBase class assigns the integer 0 to these class attributes which are used only during parsing. The lbp attribute name stands for left binding power and rbp stands for right binding power.

    When Container class instances are created to be used as operators during parsing, :ref:`binding powers<binding-power-label>` are assigned to the Container instance attributes lbp and rbp.

Expression Methods
------------------
Below is a brief summary of the methods of ExprBase subclass instances.

__bool__ method :
    A python truthiness evaluation of any truealgebra expressions will return a python True except for an evaluation of an instance of the Null class, which returns a python False.

__eq__ method :
    The python operator ``==`` returns a python True when comparing two truealgebra expressions that are the same. A python equality between two truealgebra expressions implies that the two mathematical expressions they represent are also equal. However the converse does not always happen. For example, the two mathematical expressions ``2x``  and ``x + x`` are mathematically equal. But the python expression ``parse(' 2 * x ') == parse(' x + x ')`` will evaluate to a python False.

__hash__ method :
    This method is defined and as a result, truealgebra expressions can be used as keys in python dictionaries.

__ne__ method :
   This method will return the Boolean opposite of the __eq__  method.

apply2path method :
    The apply2path method of an expression comes into play when the expression is evaluated by a truealgebra rule that has a non-empty path attribute.  The result will be thw expression with the rule applied only to the sub-expression at the location specified by the rule's path attribute. See :ref:`path-label`.

bottomup method :
   This method is used when a truealgebra rule with a bottomup attribute of True is applied to an expression. There are exceptions, but the rule is applied to every sub-expression inside the expression, starting at the bottom and working its way up until the top most level expression is evaluated. See :ref:`bottomup-label`.

match method :
   This method is used by the NaturalRule instances to find sub-expressions that match patterns in expressions.

yank method :
    This rule is used by Yank class instances to extract sub-expressions at a specified path inside of an expression. 


.. _symbol-class-label:

Symbol Class
------------
Symbol instances represent mathematical symbols. The Symbol instances are atoms, which contain no other truealgebra expressions. To instantiate the Symbol class requires only one parameter, a python string, that will be assigned to the name instance attribute.

A Symbol name attribute must be a symbol name, as defined in section :ref:`symbol-name-label`.  An example is shown below of the creation of a Symbol instance representing the mathematical symbol ``x``.

.. ipython::

   In [1]: ex1_1 = Symbol("x")
      ...: print('ex1_1.name=  ' + str(ex1_1.name))


Number Class
------------
A Number class instance has a number attribute that refers to a python number object. In the truealgebra.stdcas module there are four types of number objects: float, int, complex and fraction.Fraction. 

.. ipython::

   In [1]: ex1_2 = Number(3.75)
      ...: ex1_3 = Number(17)
      ...: ex1_4 = Number(Fraction(1, 3))
      ...: ex1_5 = Number(2j)
      ...: print('float ex1_2=  ' + str(ex1_2))
      ...: print('integer ex1_3=  ' + str(ex1_3))
      ...: print('fraction ex1_4=  ' + str(ex1_4))
      ...: print('complex ex1_5=  ' + str(ex1_5))

TrueAlgebra places no restrictions on what can be the number attribute of a Number instance. It is intended that in the future there will be modules other than stdcas that use numpy number or mpmath numbers.

Container Class
---------------
The Container class has a **name instance attribute** and a **items instance attribute**. The name attribute is a python string and the items attribute is a tuple which can contain other truealgebra expressions.

A Container instance is useful for representing mathematical functions but it also can represent vectors, ordered pairs, matrix columns or other mathematical objects that contain ordered components. 

A Container instance can be used to model mathematical functions and the tuple elements of the Container attribute items can be referred to as arguments. But the Container instances can also be used to represent non-functions such as vectors, ordered pairs, matrix columns or other mathematical objects that contain ordered components. Container instances can contain other container instances leading to a dendridic or tree-like structure of truealgebra expressions.

An example of instantiating a Container class with name ``f`` is below.

.. ipython::

   In [1]: ex1_6 = Container(name= 'f', items=(ex1_3, ex1_1))
      ...: print('ex1_6=  ' + str(ex1_6))

There are two naming conventions used for name attributes. Each naming convention is related to a different form required for parsing. The two conventions are not mixed, The name instance attributes must follow one or the other convention.

.. _container-name-1-label:

The first naming convention requires the name attribute to be a symbol name, see  section :ref:`symbol-name-label`. In the example below of this naming convention, a mathematical function with name ``funct1`` is parsed with a comma delimited list of arguments enclosed inside of a pair of parenthesis. ``funct1`` becomes the name attribute of a Container instance with the arguments stored inside of the items attribute.

.. ipython::

   In [1]: ex1_7 = parse(' funct1(74, a, bi(3.4) , c0) ')
      ...: print('ex1_7=  ' + str(ex1_7))

.. _container-name-2-label:

In the second naming convention, the name attribute is an operator name, discussed in section :ref:`operator-name-label`. During parsing, strings with operator names are parsed as though they are mathematical operators, combining with adjacent expressions. During parsing of ``a ** 7`` below,  the operator name ``**`` becomes the name attribute of a Container instance with and a items attribute holding the expressions ``a`` and ``7``. 

.. ipython::

   In [1]: ex1_8 = parse(' a ** 7 ') 
      ...: print('ex1_8=  ' + str(ex1_8))

Container instances are iterables, which is a useful feature demonstrated below. The contents of the items attribute, which is a tuple, will be accessed when the instance is iterated.  

.. ipython::

   In [1]: ex1_9 = parse(' func(1, 3, 4.2, x, h(5.4)) ')
      ...: for e in ex1_9:
      ...:     print(e)

Restricted and Assign are subclasses of Container. Both Restricted (see :ref:`restricted-label`) and Assign (see :ref:`assign-label`) have overridden the bottomup, and apply2path methods of Container. These subclasses have overridden the match method as well.

CommAssoc is a subclass of Container. CommAssoc instances can be used to represent mathematical functions that are both commutative and associative. Two exmaples are the mathematical multiplication and addition operations. The boolean operatations of **and** and **or** can also be represented by CommAssoc instances.

End and Null Classes
--------------------
An instance of the Null subclass of ExprBase represents nothingness somewhat similar to the python None object. All instances of Null are essentially identical. Null instances are used as placeholders in the parse code, and sometimes as outputs of rules when errors occur.

.. ipython::

   In [1]: null = Null()
      ...: print('null=  ' + repr(null))

The ``End`` subclass of ExprBase is used only in during parsing. It indicated theend of a sequence of tokens being parsed.

Quasi Immutability
------------------
If truealgebra expressions are mutated during operations with truealgebra rules there could be undesired and unintended effects leading to incorrect results. The reason for this is a truealgebra expression is a Python object that can exist in multiple locations. If a truealgebra expression is mutated in one location, it is mutated in all locations.

If a user attempts to write a new value to an expression attribute then an attribute error is raised, with two exceptions discussed below.

If an expression is to be modified, the general practice is\:

    * A new expression must be created that reflects the changes.

    * All parent expressions that contain the modified expression must also be re-created.

    * All children sub-expressions inside the modified expression can be reused (unless they have to be modified)

    * All sibling expression (that are not parents or children) of the modified expression can be reused (unless they have to be modified).

Truealgbra expression can be described as quasi immutable. Expressions are used as tokens in the parsing process and are sometimes mutated during parsing. The technique for changing these expression attributes, while not unduly complicated, is sufficiently complicated that it will require far more than a few "fat fingered" typing errors to implement. In effect, to cause undesired mutations in truealgebra expressions requires a deliberate act by a user or developer.

All expressions have the attributes ``rbp`` and ``lbp`` which stand for
right and left binding power can be changed at any time without raising errors.
These attributes are used only during parsing and have no effect on anything
outside outside of parsing. And that should remain so.

