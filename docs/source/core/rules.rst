=====
Rules
=====
To provide TrueAlgebra examples in a python script, modify the sys.path and import the necessary packages, modules, and objects.

.. ipython::

    In [1]: from truealgebra.core.rules import (
       ...:     Rule, Rules, RulesBU, JustOne, JustOneBU
       ...: )
       ...: from truealgebra.core.naturalrules import (
       ...:     NaturalRule, HalfNaturalRule
       ...: )
       ...: from truealgebra.core.expression import (
       ...:     ExprBase, Symbol, Number, true, false,
       ...:     Container,Restricted, Assign, Null, End)
       ...: from truealgebra.core.settings import settings
       ...: from truealgebra.core.parse import parse
       ...:
       ...: settings.active_parse = parse 
       ...: settings.set_symbol_operators("and", 75, 75)


RuleBase
========
RuleBase is an abstract class that provides the basis for all truealgebra rules.
All RuleBase objects are called rules or truealgebra rules.

Rule, NaturalRule, and HalfNaturalRule are important RuleBase subclasses used to create rules that
modify truealgebra expressions. The Rules and JustOne subclasses create rules that apply groups
of other rules to truealgebra expressions.

Never say never, but it is highly unlikely at least in the near future that additional major
subclasses of RuleBase will be added to TrueAlgebra. 
The five subclasses mentioned in the above paragraph should be sufficient for creating rules.

__call__ Method
---------------
The __call__ method is defined in RuleBase. As a result, rules behave like functions.
Consider a python expression of the form ``rule(expr)`` where ``rule`` is a truealgebra rule
and ``expr`` is a truealgebra expression. The ``rule`` here takes ``expr`` as an argument and
evaluates it. The intent is that rules be viewed as fancy functions.

tpredicate and tbody Methods
----------------------------
A user does not need to know anything about the tbody and tpredicate methods.
They are hidden inside of every rule object but a user does not
interact with them. However it is easier to explain coherently how rules work when references are made to
the tpredicate and tbody methods. The first character "t" of tpredicate and tbody stands for "truealgebra".

The tbody and tpredicate methods were developed using techniques from the Yacas Computer
Algebra System. The Yacas procedure mimics very well the application of mathematical theorems to
mathematical expression.
In Yacas, a rule has a predicate and a body. The predicate determines if the body can be applied to a Yacas mathematical object.

Primarily because of the complexity of the JustOne class, The steps used
in TrueAlgebra are a more complicated than in Yacas. When a truealgebra rule
takes a truealgebra expression as an argument, the steps are:

    * step 1. The rule's __call__ method calls the tpredicate method and passes the input expression as an argument. 

    * step 2a. If tpredicate returns False, then __call__ returns the input expression with no further evaluation.

    * step 2b. Otherwise, tpredicate returns a ``TrueThing`` object. The ``TrueThing`` object contains the input expression and any other pertinent information. Continue to step 3.

    * step 3. The __call__ method calls the tbody method, passing to it the TrueThing object as an argument.

    * step 4. The tbody method evaluates the input expression (and any other information in the TrueThing object) and returns (in most cases) a new algebraic expression.

    * step 5. The __call__ method returns the result of the tbody method.

donothing Rule
=======
The donothing rule is the instance of Rule. The donothing rule has all the featurs of a rule
but it always does nothing

Example
=======
Rule is a subclass of RuleBase and is the primary means of generating rules.

.. ipython::

    In [1]: class IsSym(Rule):
       ...:     def __init__(self, *args, **kwargs):
       ...:         self.names = args
       ...:         super().__init__(*args, **kwargs)
       ...:
       ...:     def predicate(self, expr):
       ...:         return (
       ...:             isinstance(expr, Container)
       ...:             and expr.name == 'issym'
       ...:             and len(expr.items) > 0
       ...:         )
       ...:
       ...:     def body(self, expr):
       ...:         if isinstance(expr[0], Symbol) and expr[0].name in self.names:
       ...:             return Symbol('true')
       ...:         else:
       ...:             return Symbol('false')

Next create the rule

.. ipython::

    In [1]: issym_rule = IsSym('x', 'y', 'z')
       ...:
       ...: print('    Case 1 assign expr to a truealgebra expression.')
       ...: expr = parse('  issym(y)  ')
       ...: print('expr =  ', expr)
       ...: print('    Apply the rule issym_rule to the truealgebra expression.')
       ...: print('issym_rule(expr) =  ', issym_rule(expr))
       ...: print('    The result is the truealgebra expression "true".')
       ...: print('')
       ...: 
       ...: print('    Case 2 assign expr to a truealgebra expression.')
       ...: expr = parse('  issym(b)  ')
       ...: print('expr =  ', expr)
       ...: print('    Apply the rule issym_rule to the truealgebra expression.')
       ...: print('issym_rule(expr) =  ', issym_rule(expr))
       ...: print('    The result is the truealgebra expression "false".')
       ...: print('')
       ...: 
       ...: print('    Case 3 assign expr to a truealgebra expression.')
       ...: expr = parse('  (x + 7 * y)  ')
       ...: print('expr =  ', expr)
       ...: print('    Apply the rule issym_rule to the truealgebra expression.')
       ...: print('issym_rule(expr) =  ', issym_rule(expr))
       ...: print('    The result is the truealgebra expression "false".')
       ...: 
       ...:

In the above first two cases, the rule predicate method evaluated to True and
as a result, the body method evaluated the input algebraic expression and the rule returned
the result. However in the third case, the predicate method returned False
resulting in the rule returning its input expression unevaluated by the body method.
expression.


NaturalRule
===========

Instatiation
------------

.. code-block:: python
    :linenos:

    <new rule> = NaturalRule(
        predicate_rule=<a predicate rule>
        pattern=<string that can be parsed>
        vardict=<string that can be parsed>
        outcome=<string thatcan be parsed>
        outcome_rule=<a rule>
    )

Look at each of the parameters:

    * **predicate_rule**
    * **pattern**


Predicate rules
---------------
TrueAlgebra uses the Symbol ``true`` to represent  mathematical truth and the Symbol ``false``
represents mathematical falsehood. Lower case names are used to prevent confusion with
python True and False.

The pertinent definition here of a predicate "..is a property, characteristic,
or attribute that may be affirmed or denied of something." (the free dictionary).

A **predicate expression** is a Container object with a name that connotes some
specific property, characteristic, or attribute of its one or more arguments.

A predicate rule evaluates a one or more predicate expressions to true or false.
All other expressions are returned without evaluation by a predicate rule.

In the example below, the predicate rule ``isintrule`` evaluates predicate expressions
of the form ``isint(x)``. The evaluation is to ``true`` if ``x`` is an
integer and ``false`` otherwise. ``isintrule`` will return but not 
evaluate any other expressions.

Predicate Rule isintrule
++++++++++++++++++++++++
The ``isintrule`` below will make a predicate evaluation of the ``isint``
predicate expression. This determines if the contents of ``isint`` is an
integer number.

.. ipython::

    In [1]: class IsInt(Rule):
       ...:     def predicate(self, expr):
       ...:         return (
       ...:             isinstance(expr, Container)
       ...:             and expr.name == 'isint'
       ...:             and len(expr.items) >= 1
       ...:         )
       ...:
       ...:     def body(self, expr):
       ...:         if isinstance(expr[0], Number) and isinstance(expr[0].value, int):
       ...:            return true
       ...:         else:
       ...:            return false
       ...:
       ...: isintrule = IsInt()
       ...:
       ...: # Apply isintrule, in three cases.
       ...: print(
       ...:     'case 1, isintrule( isint(4) )=  ',
       ...:     isintrule(parse('  isint(4)  '))
       ...: )
       ...:
       ...: print(
       ...:     'case 2, isintrule( isint(sin(x)) )=  ',
       ...:     isintrule(parse('  isint(sin(x))  '))
       ...: )
       ...:
       ...: print(
       ...:     'case 3, isintrule( cosh(4) )=  ',
       ...:     isintrule(parse('  cosh(4)  '))
       ...: )
       ...:

In case 1 above the predicate rule ``isintrule`` evaluates the ``isint``
predicate and returns ``true``. In case 2, the rule returns ``false``.
In case 3, the rule makes no evaluation and returns its input expression.

Predicate Rule lessthanrule
+++++++++++++++++++++++++++
The ``lessthanrule`` below will make a predicate evaluation of the ``<``
predicate expression. This determines if the first argument of ``<`` is larger than
its second argument. Both arguments must be numbers.

.. ipython::

    In [1]: class LessThan(Rule):
       ...:     def predicate(self, expr):
       ...:         return (
       ...:             isinstance(expr, Container)
       ...:             and expr.name == '<'
       ...:             and len(expr.items) >= 2
       ...:             and isinstance(expr[0], Number)
       ...:             and isinstance(expr[1], Number)
       ...:         )
       ...:
       ...:     def body(self, expr):
       ...:         if expr[0].value < expr[1].value:
       ...:             return true
       ...:         else:
       ...:             return false
       ...:
       ...: lessthanrule = LessThan()
       ...:
       ...: # Apply lessthanrule, in three cases.
       ...: print(
       ...:     'case 1, lessthanrule( 3.4 < 9 )=  ',
       ...:     lessthanrule(parse('  3.4 < 9  '))
       ...: )
       ...:
       ...: print(
       ...:     'case 2, lessthanrule( 7 < 7 )=  ',
       ...:     lessthanrule(parse('  7 < 7  '))
       ...: )
       ...:
       ...: print(
       ...:     'case 3, lessthanrule(x**2)=  ',
       ...:     lessthanrule(parse('  x**2  '))
       ...: )

.. ipython::

    In [1]: class And(Rule):
       ...:     def predicate(self, expr):
       ...:         return (
       ...:             isinstance(expr, Container)
       ...:             and expr.name == 'and'
       ...:             and len(expr.items) >= 2
       ...:         )
       ...:
       ...:     def body(self, expr):
       ...:         if expr[0] == false:
       ...:             return false
       ...:         elif expr[1] == false:
       ...:             return false
       ...:         elif expr[0] == true and expr[1] == true:
       ...:             return true
       ...:         else:
       ...:             return expr
       ...:
       ...: andrule = And()
       ...:
       ...: # Apply andrule, in three cases.
       ...: print(
       ...:     'case 1, andrule( true and true )=  ',
       ...:     andrule(parse('  true and true  '))
       ...: )
       ...:
       ...: print(
       ...:     'case 2, lessthanrule( 7 < 7 )=  ',
       ...:     lessthanrule(parse('  7 < 7  '))
       ...: )
       ...:
       ...: print(
       ...:     'case 3, lessthanrule(x**2)=  ',
       ...:     lessthanrule(parse('  x**2  '))
       ...: )

Create ``predrule``

.. ipython::

    In [1]: predrule = JustOneBU(isintrule, lessthanrule, andrule) 

The end.

Example 1
---------

.. ipython::

    In [1]: convert_xyz = NaturalRule(
       ...:     predicate_rule=issym_rule,
       ...:     varstring='  suchthat(forall(xyz), issym(xyz))  ',
       ...:     pattern='  g(xyz, 7)  ',
       ...:     outcome='  f(7)  ',
       ...: )

