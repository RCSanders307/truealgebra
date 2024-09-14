=====
Rules
=====

.. _Yacas:

.. rubric:: Rules, Yacas and Mathematical Theorems

TrueAlgebra rules have a similar approach as the rules in the computer algebra
system Yacas yacas.org. There are differences in the nomenclature. Yacas rules
have a predicate and body which correspond to the truealgebra rule's tpredicate
and tbody methods.

The Yacas procedure mimics very well the application of mathematical theorems to
mathematical expression.
In Yacas, a rule has a predicate and a body. The predicate determines if the body can be applied to a Yacas mathematical object.

The Yacas rule predicate evaluate the input expression. If the predicate outputs true then the body of the rule evaluates the input expression and transforms it into the output expression of the rule. If the predicate returns false, then the input expression of the rule becomes its output expression.

When applied to mathematics, the predicate of a rule performs the role of the introduction to a mathematical theorem which specifies the scope, and specific stipulations for the theorem to be true. When a predicate returns true, it has verified that the input expression meets the conditions for the mathematical theorem. The body of the rule then transforms the input expression into an output expressions in accordance with the theorem statement.


Import and Setup
================
Import the necessary packages, modules, and objects.

.. ipython::

    In [1]: from truealgebra.core.rules import (
       ...:     Rule, Rules, RulesBU, JustOne, JustOneBU, Substitute,
       ...:     donothing_rule 
       ...: )
       ...: from truealgebra.core.naturalrules import (
       ...:     NaturalRuleBase, NaturalRule, HalfNaturalRule
       ...: )
       ...: from truealgebra.core.expression import (
       ...:     ExprBase, Symbol, Number, true, false,
       ...:     Container,Restricted, Assign, Null, End, CommAssoc,
       ...: ) 
       ...: from truealgebra.core.settings import settings
       ...: from truealgebra.core.parse import parse
       ...: from truealgebra.core.unparse import unparse 
       ...:
       ...: settings.active_parse = parse 
       ...: settings.set_symbol_operators("and", 75, 75)
       ...: settings.set_custom_bp("=", 50, 50) 
       ...: settings.set_container_subclass("*", CommAssoc) 
       ...: ExprBase.set_unparse(unparse) 


RuleBase Class
==============
RuleBase is an abstract class that provides the basis for all truealgebra rules.
All RuleBase objects are called rules or truealgebra rules.

Rule, NaturalRule, and HalfNaturalRule are important RuleBase subclasses used
to create rules that modify truealgebra expressions. The Rules and JustOne
subclasses create rules that apply groups of other rules to truealgebra
expressions.

Never say never, but it is highly unlikely at least in the near future that
additional major subclasses of RuleBase will be added to TrueAlgebra. 
The five subclasses mentioned in the above paragraph should be sufficient
for creating rules.

The RuleBase class is the basis for all truealgebra rules.  All truealgebra rules have their  __call__ method defined and will take arguments in the same manner as functions. All rules will take one and only one argument which has to be a truealgebra expression. The result of a rule will always be a truealgebra expression.


.. _tpred-and-tbody-tag:

Abstract Methods: tpredicate and tbody
--------------------------------------
The tbody and tpredicate methods were developed using techniques from
the :ref:`Yacas Computer Algebra System<Yacas>`.

All rules have tpredicate and tbody methods. The first character "t" of both
names stands for "truealgebra". A user does not need to know
anything about these methods. They are hidden inside of every rule object and
a user does not interact directly with them. 

However it is easier to explain coherently how rules work when references are
made to
the tpredicate and tbody methods as in the step by step procedure below. 

Primarily because of the complexity of the JustOne class, The steps used
in applying TrueAlgebra rules are a more complicated than in Yacas. When a
truealgebra rule takes a truealgebra expression as an argument, the steps are:

    * step 1. The rule's __call__ method calls the tpredicate method and passes the input expression as an argument. 

    * step 2a. If tpredicate returns False, then __call__ returns the input expression with no further evaluation.

    * step 2b. Otherwise, tpredicate returns a ``TrueThing`` object. The ``TrueThing`` object contains the input expression and any other pertinent information. Continue to step 3.

    * step 3. The __call__ method calls the tbody method, passing to it the TrueThing object as an argument.

    * step 4. The tbody method evaluates the input expression (and any other information in the TrueThing object) and returns (in most cases) a new algebraic expression.

    * step 5. The __call__ method returns the result of the tbody method.


The Concrete __call__ Method
----------------------------
The __call__ method is defined in RuleBase. As a result, rules behave like
functions. Consider a python expression of the form ``rule(expr)`` where
``rule`` is a truealgebra rule
and ``expr`` is a truealgebra expression. The ``rule`` here takes ``expr``
as an argument and evaluates it. The intent is that rules be viewed 
iand used as fancy functions.

The__call__ method. It is a fundamental part of the
five step procedure outlined above. It can also implement the path and 
bottomup procedures.

.. _rulebase-path-bottomup:

path and bottomup Attributes
----------------------------
path attribute
    When path is a tuple of integers representing a path to a specific
    sub-expression inside the expression. The rule will be applied to to
    that specific sub-expression.

    RuleBase path is an empty tuple, and the expression will be applied to
    the top level expression.

    RuleBase and all of its subclasses, when instantiated, will take a
    ``path`` keyword argument which can be  a list, tuple, or other
    collection. The ``path`` argument can only be positive or negative
    integers. The value of the ``path`` argument is assigned as a tuple
    to the ``path`` attribute.

bottomup attribute
    If the attribute is True, the rule will be applied at all levels of an
    expression, starting at the lowest levels and proceeding progressively
    up to the top most level. 

    RuleBase sets bottomup to False, in which case the rule will be applied
    only to the top level of an expression.

ChangeSymbolName Example
------------------------
Create the Rule subclass ``ChangeSymbolName``. The rules from this class server no mathematical purpose but illustrates the features of rules.

The ``ChangeSymbolName`` class overrides the ``postinit``, ``predicate``, and ``body`` methods. The ``postinit`` method  takes two arguments and assigns them to the attributes ``from_`` and ``to_`` which should be python strings. The ``predicate`` method returns ``True`` if the input expression is a Symbol instance with a name equal to ``from_``. The ``body`` method creates a new `Symbol` instance with name ``to_``.

The ``predicate`` method does not use python duck typing, ``expr`` is tested to see if it is an instance of Symbol. The technique used in this method is not object orientated programming.


Rule Class
==========
Rule is a subclass of RuleBase. Rule and its subclasses are the primary means
of generating rules.

All Rule instanace have a predicate method, that is called by its tpredicate 
method. The predicate method detemrines if the rule's tbody method will be 
applied to the input expression.

There is also a body meod which is called by the tbody method. The output of
the body method will be the output of the tbody body and in may cases the
output of the rule itself.

.. _donothing-tag:

The Rule Instance donothing_rule
--------------------------------
The  donothing_rule rule is a Rule instance. All Rule instances have the same
characteristics as  donothing_rule. A  donothing_rule rule always returns its
input expressions, unchanged. The donothing_rule always does nothing.

The  donothing_rule rule is sometimes useful as a default rule, For example it is
the value for the NaturalRule predicate_rule attribute which act as a default
for NaturalRule instances.

How to Create Rule Instances
----------------------------
To create rules other than the  donothing_rule rule, a Rule subclass must be
created.

IsSymEval Example
+++++++++++++++++
As an example create the Rule subclass IsSymEval. The Instances can be called
:ref:`predicate rules<logic-and-predicate>`. They evaluate truealgebra Container expressions named
``issym`` that meet certain criteria and return ``true`` or ``False``.

Three methods are over written below in the IsSymeval subclass.

__init__ method
    The __init__ method allows for passing arguments for use by the rule.
    The last line of the __init__ method in the example below is very important
    and must always be included, otherwise the __init__ methods of parent classes
    will not be executed.
predicate method
    The predicate method requires one positional parameter, which will be the 
    input expression of the rule. The method must returns either True or False.
    If True, the body method will be invoked.
    If False, the input expression will be the output of the rule.

    As with mathematical theorems the code in the predicate must be precise
    and exact, if need be using isinstance or even type functions.
    Mathematical theorems do not follow python duck typing conventions.
body method
    The predicate method requires one positional parameter, which will be the 
    input expression of the rule. The method must return a truealgebra
    expression. If this method is invoked, its output will be the output
    of the rule.
    
.. ipython::

    In [1]: class IsSymEval(Rule):
       ...:     def __init__(self, *args, **kwargs):
       ...:         self.names = args
       ...:         # The line below must be included
       ...:         super().__init__(*args, **kwargs)
       ...:
       ...:     def predicate(self, expr):  # expr is the rule input expression
       ...:         # This method must return True or False
       ...:         return (
       ...:             isinstance(expr, Container)
       ...:             and (expr.name == 'issym')
       ...:             and (len(expr.items) > 0)
       ...:         )
       ...:
       ...:     def body(self, expr):  # expr is the rule input expression
       ...:         if isinstance(expr[0], Symbol) and expr[0].name in self.names:
       ...:             return Symbol('true')
       ...:         else:
       ...:             return Symbol('false')
       ...:         # This method must return a truealgebra expression 

Demonstrate an IsSymEval rule
+++++++++++++++++++++++++++++
Create the rule issym_eval_rule from IsSymEval. This rule will evaluate
``issym(x)``, ``issym(y)``, or  ``issym(x)`` to ``true``. 


.. ipython::

    In [1]: issym_eval_rule = IsSymEval('x', 'y', 'z')

**Case 1** - predicate not satisfied.

Create an expression with a Container instance with the name 'wrongname'.

.. ipython::

    In [1]: expr = parse('  wrongname(x)  ') 
       ...: expr

Next, apply issym_eval_rule to expr. The input ``expr`` is returned.

.. ipython::

    In [1]: issym_eval_rule(expr) 

The name attribute of the Container instance is ``wrongname`` instead of
``issym`` as required by the predicate method. So the predicate returns False,
and the rule returned the input expression without change.

**Case 2** - predicate satisfied, return true

.. ipython::

    In [1]: expr = parse('  issym(y)  ')
       ...: expr

Next, apply issym_eval_rule to expr.

.. ipython::

    In [1]: issym_eval_rule(expr) 

The result is the truealgebra expression "true".

**Case 3** - predicate satisfied, return false

.. ipython::

    In [1]: expr = parse('  issym(a)  ')
       ...: expr

Next, apply issym_eval_rule to expr.

.. ipython::

    In [1]: issym_eval_rule(expr) 

The result is the truealgebra expression "false".


Flatten Rule
------------

.. ipython::

    In [1]: class Flatten(Rule):
       ...:     def predicate(self, expr):  
       ...:         return isinstance(expr, CommAssoc) and expr.name == '*'
       ...:  
       ...:     def body(self, expr):
       ...:         newitems = list()
       ...:         for item in expr.items:
       ...:             if isinstance(item, CommAssoc) and item.name == '*':
       ...:                 newitems.extend(item.items)
       ...:             else:
       ...:                 newitems.append(item)
       ...:         return CommAssoc('*', newitems)
       ...:  
       ...:     bottomup = True
       ...:  
       ...: flatten = Flatten() 

Substitute Rule
---------------
Blah blah blah.



ChangeSymbolName Example
------------------------
Create the RuleBase subclass ``ChangeSymbolName``. The rules from this class server no mathematical purpose but illustrates the features of rules.

The ``ChangeSymbolName`` class overrides the ``postinit``, ``predicate``, and ``body`` methods. The ``postinit`` method  takes two arguments and assigns them to the attributes ``from_`` and ``to_`` which should be python strings. The ``predicate`` method returns ``True`` if the input expression is a Symbol instance with a name equal to ``from_``. The ``body`` method creates a new `Symbol` instance with name ``to_``.

The ``predicate`` method does not use python duck typing, ``expr`` is tested to see if it is an instance of Symbol. The technique used in this method is not object orientated programming.

.. ipython::

   In [1]: class ChangeSymbolName(Rule):
      ...:     def __init__(self, *args, **kwargs):
      ...:         if "from_" in kwargs:
      ...:             self.from_ = kwargs["from_"]
      ...:         if "to_" in kwargs:
      ...:             self.to_ = kwargs["to_"]
      ...:         super().__init__(*args, **kwargs)
      ...:     def predicate(self, expr):
      ...:         return isinstance(expr, Symbol) and expr.name == self.from_
      ...:     def body(self, expr):
      ...:         return Symbol(self.to_)

Create three rules from ``ChangeSymbolName``\:

    * ``a_b_rule`` changes a Symbol instance with name attribute ``"a"`` to a Symbol instance with name attribute ``"b"``.
    * ``b_c_rule`` changes a Symbol instance with name attribute ``"b"`` to a Symbol instance with name attribute ``"c"``.
    * ``c_d_rule`` changes a Symbol instance with name attribute ``"c"`` to a Symbol instance with name attribute ``"d"``.

.. ipython::

   In [1]: a_b_rule = ChangeSymbolName(from_="a",to_="b")
      ...: b_c_rule = ChangeSymbolName(from_="b",to_="c")
      ...: c_d_rule = ChangeSymbolName(from_="c",to_="d")

Apply the ``a_b_rule`` to the Symbol instance ``expr_a`` which has the ``name`` attribute ``"a"``. The output is an all new expression Symbol instance with the ``name`` attribute `"b"`.

.. ipython::

   In [1]: # create expr_a which is a Symbol instance with name "a"
      ...: expr_a = parse(" a ")
      ...: print("expr_a = " + str(expr_a))
      ...: # apply a_b_rule to expr_a
      ...: out = a_b_rule(expr_a)
      ...: print("a_b_rule(expr_a)= " + str(out))

What happened internally with ``a_b_rule`` when it evaluated ``expr_a``? The ``predicate`` method returned ``True`` and the ``body`` method was called. The output of ``body`` becomes the output of the rule.

Next, apply the rule `a_b_rule`` to a Container instance containing a lone argument: a Symbol with ``name`` attribute ``a``.  

.. ipython::

   In [1]: expr_sin = parse(" sin(a) ")
      ...: print("expr_sin= " + str(expr_sin))
      ...: out = a_b_rule(expr_sin)
      ...: print("a_b_rule(expr_sin)= " + str(out))

In this example, the input expression ``expr_sin`` was returned by the rule ``a_b_rule`` because the ``predicate`` method of the rule returned ``False``. The ``body`` method was not executed. 

This example also illustrates that the ``a2a_symbol_rule`` only acts on the top level of an expression. The lower level Symbol instance with name attribute ``a`` was unaffected by the rule, whereas in the previous example, the same expression (which was top level) was modified. 

This behavior of ``a_b_rule`` results from  its bottomup attribute being ``False``.

.. ipython::

   In [1]: print("a_b_rule.bottomup=  " + str(a_b_rule.bottomup))

ChangeContainerName Example
---------------------------
Create a second subclass of RuleBase that will take any Container class instance with a certain ``name`` and create a new Container class instance with a specified ``name``. 

.. ipython::

   In [1]: class ChangeContainerName(Rule):
      ...:     def __init__(self, *args, **kwargs):
      ...:         if "from_" in kwargs:
      ...:             self.from_ = kwargs["from_"]
      ...:         if "to_" in kwargs:
      ...:             self.to_ = kwargs["to_"]
      ...:         super().__init__(*args, **kwargs)
      ...:     def predicate(self, expr):
      ...:         return isinstance(expr, Container) and expr.name == self.from_
      ...:     def body(self, expr):
      ...:         return Container(self.to_, items=tuple(expr.items))

Create three rules from ``ChangeContainerName`` for use in examples below\:

    * ``f_f1_rule`` changes a Container instance with name attribute ``"f"`` to  a ``Conainer`` instance with name attribute ``"f1"``.
    * ``g_g1_rule`` changes a Container instance with name attribute ``"g"`` to  a ``Conainer`` instance with name attribute ``"g1"``. 
    * ``h_h1_rule`` changes a Container instance with name attribute ``"h"`` to  a ``Conainer`` instance with name attribute ``"h1"``.

.. ipython::

   In [1]: f_g_rule = ChangeContainerName(from_="f",to_="g")
      ...: f_f1_rule = ChangeContainerName(from_="f",to_="f1")
      ...: g_g1_rule = ChangeContainerName(from_="g",to_="g1")
      ...: h_h1_rule = ChangeContainerName(from_="h",to_="h1")

.. _logic-and-predicate:

Logic and Predicate Rules
=========================
Predicate rules are rules that evaluaate truealgebra expressions that represent
logic to either ``true`` or ``false``.
The Symbol ``true`` represents  mathematical truth and the Symbol ``false``
represents mathematical falsehood. Lower case names are used to prevent
confusion with python True and False.

A logical expression would be expressions such as `` 3 < 7 ``, ``true and false``,
or ``isint(6)`` that are mathematically meaningful to be evaluated to true or false..
When a predicate rule cannot evaluate an input expression to either
true or false, it returns the input expression.

In the example below, the predicate rule ``isintrule`` evaluates expressions
of the form ``isint(x)``. The evaluation is to ``true`` if ``x`` is an
integer and ``false`` otherwise. ``isintrule`` will return but not 
evaluate any other expressions.

Predicate Rule isintrule
------------------------
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
---------------------------
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

Predicate Rule andrule
------------------------
Next look at the andrule which evaluates expressions such as ``true and false``.

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

Combine Multiple Prredicate Rules
---------------------------------
Create the predicate rule ``predrule`` by combining isintrule, lessthanrule,
and andrule.

.. ipython::

    In [1]: predrule = JustOneBU(isintrule, lessthanrule, andrule) 

The predrule will be used in the examples below.

NaturalRule Class
=================
The name 'NaturualRule' for this class is used because the natural
mathematical-like syntax of the pattern, vardict and outcome arguments used to
instantiate its rules. 

Natural Rule Example
--------------------
In order to illustrate more features of a NaturalRule rule, the following example is a bit
contrived.

.. ipython::

    In [1]: natrule = NaturalRule( 
       ...:     predicate_rule = predrule,
       ...:     vardict = (
       ...:         'forall(e0, e1);'
       ...:         'suchthat(forall(n0), isint(n0) and (n0 < 7))'
       ...:     ), 
       ...:     pattern='  (e0 = e1) + (x = n0)  ',
       ...:     outcome='  (e0 + x) = (e1 + n0)  ',
       ...:     outcome_rule = Substitute(
       ...:         subdict={Symbol('theta'): Symbol('phi')}, 
       ...:         bottomup=True 
       ...:     ) 
       ...: )

Apply the rule ``natrule`` , below, to the expression``ex1``. 
The result, ``out1``,  of the rule is algebraically equal to ``ex1``.

.. ipython::

    In [1]: ex1 = parse('  (cos(theta) = exp(7)) + (x = 6)  ')
       ...: print('ex1 =  ', ex1)
       ...: out1 = natrule(ex1) 
       ...: print('natrule(ex1) =  ', out1)
       
How a NaturalRule Rule Works
----------------------------

Variable Dictionary
+++++++++++++++++++
Initially a user enters a string as a vardict class attribute or an
instantiation vardict argument. The string gets converted to a variable
dictionary by a somewhat involved process. The variable dictionary is
created when a NaturalRule instance is instantiated, and it remains unchanged
afterwards.

A variable dictionary is a python dictionary. The dictionary keys must be
truealgebra Symbol instances which will be called variables. The dictionary
values must be truealgebra expressions. The values represent logic that must be 
satisfied in order for the variable to be matched during the matching process.

Conversion
''''''''''
The first step in the conversion is to parse the string
The function meta_parse parses the string with line breaks and ';'
charaters into a sequence of python expressions. Each parsed expression if it
has proper syntax will add to the variable dictionary.

In the second step an empty dictionary named vardict is defined.
Each parsed expression is looked at for truealgebra Container objects named 
forall and suchthat. The content of the forall and suchthat
objects are inspected and if the syntax is correct are made into the
variable dictionary.

forall Function 
'''''''''''''''
The class method create_vardict does the conversion process. This method
is usful to a user for debugging and investigations.

Below the ``vardict_string_1`` gets parsed into a  ``forall`` Container object
that represents a mathematical function. The ``forall`` contains two symbols
``e0`` and ``e1``. These two symbols become keys in the 
``vardict_dict_1`` dictionary with values of ``true``.

.. ipython::

    In [1]: vardict_string_1 = ' forall(e0, e1) '
       ...: vardict_1 = NaturalRule.create_vardict(vardict_string_1) 
       ...: vardict_1 

suchthat Function
'''''''''''''''''
The ``suchthat`` function below is the top level of the expression and
contains two arguments. The first argument is a forall function with one
argument that is a symbol.

.. ipython::

    In [1]: vardict_2 = NaturalRule.create_vardict( 
       ...:     '  suchthat( forall(n0),  isint(n0) and (n0 < 7) )  ' 
       ...:  )
       ...:  vardict_2
       ...:  
       ...: #aa = Substitute(xx, var)(vardict_dict_1[var])
       ...: #out = predrule(aa) 

The ``vardict_dict_2`` dictionary has one key the symbol ``n0``. The value for
that key is the logical expression  for ``n0``. The logical expression contains
the key, which is typical.

.. _matching-tag:

Pattern Matching
++++++++++++++++
The :ref:`tpredicate method<tpred-and-tbody-tag>` implements the pattern method
process desribed in this section. 

The input expression is compared to the rule's pattern attribute to
determine if the input expression matches the pattern expression.

For a pattern to match the input expressions, both expressions and all of the subexpressions must essentially be the same or equal to each other. 

Matching Without Variables
''''''''''''''''''''''''''
The following rules apply when the pattern or pattern or pattern subexpression is not a variable.

    * For Container expressions to match, they must be of the same python type, have the same name attribute, and have the same number of items in thier items attribute.  

    * Also each item in the items attribute of the inut expression must match the
      corresponding item in the patern's items attribute. 

    * Number instances match Number instances. Thier value attributes must
      muust be equal.

    * Symbol instances will match Symbol instances if they have the same
      name attribute.

Matching With Variables
'''''''''''''''''''''''
For an example look at the vardict and pattern attributes of natrule.

.. ipython::

    In [1]: print('vardict =   ', natrule.vardict)
       ...: print('vardict[e0]=  ', natrule.vardict[Symbol('e0')])
       ...: print('vardict[e1]=  ', natrule.vardict[Symbol('e1')]) 
       ...: print('vardict[n0]=  ', natrule.vardict[Symbol('n0')]) 
    
The variables ``e0`` and ``e1`` in  the variable dictionary ``vardict``,
each have a value of ``true``.
which makes these variables essentially wild, to use a card playing
term. These variables  can match any truealgebra expression during pattern matching.

The variable ``n0`` in the dictionary has a value of ``isint(n0) and n0 < 7``.
This value is the logical requirement that any expression must satisfy in order
to match ``n0``. The variable ``n0`` can only match expressions that are and intreger and less than 7.

The code below shows if the number ``5`` can match the variable ``n0``.

.. ipython::

    In [1]: input_5 = parse(' 5 ') 
       ...: n0 = parse('  n0  ') 
       ...: logic = natrule.vardict[n0]
       ...: subrule = Substitute(subdict={n0: input_5}, bottomup=True)
       ...: subed_logic = subrule(logic)
       ...: evaluation = natrule.predicate_rule(subed_logic)
       ...: print(logic) 
       ...: print(subed_logic) 
       ...: print(evaluation)

It is a two step process, First ``5`` is substituted for ``n0`` into the
logic. Then the result is evaluated by the predicat_rule. The second result
is``true`` which means that ``5`` matches ``n0``.

Next investigate if the real ``5.0`` matches ``n0``

.. ipython::

    In [1]: input_5_real = parse(' 5.0 ') 
       ...: subrule = Substitute(subdict={n0: input_5_real}, bottomup=True)
       ...: subed_logic = subrule(logic)
       ...: evaluation = natrule.predicate_rule(subed_logic)
       ...: print('logic =       ', logic) 
       ...: print('subed_logic = ', subed_logic) 
       ...: print('evaluation =  ', evaluation)

The real ``5.0`` does not match ``n0`` because it is not an integer.

match Method
''''''''''''
The matching process is initiated by rules, but the heavy lifting is done the
match methods of expressions. Normally TrueAlgebra user does not directly involk
expression match methods. A user does not need to even know of the
existance of the match methods.

However match methods can be used for debugging, and experience with match
methods can help explain some of the magic behind natural rules.

   .. ipython::

    In [1]: 
       ...: subdict = dict()
       ...: matchout = natrule.pattern.match(  
       ...:     natrule.vardict,
       ...:     subdict, 
       ...:     predrule, 
       ...:     ex1 
       ...: ) 
       ...: print('matchout=  ', matchout) 
       ...: print('subdict=   ', subdict) 

The ``matchout`` is True, which causes the rule ``natrule`` to call the rule's
tbody method. The ``subdict`` dictiionary is passed to the tbobody method as
well.

If ``matchout`` had been False, the rule would returned the input expression ``ex1`` unchanged.


Substitution
++++++++++++
When the rule's tbody method is called, A substitution is initially performed.
Look at ``subdict`` from above. subdict stands for substitution dictionary:

.. ipython::

    In [1]: print('subdict=   ', subdict) 

Replaces any variables in the outcome expression with the appropriate expressions from the pattern
matching process. The apply the outcome_rule to the outcome expression.

NaturalRule instance trys to match its pattern attribute to the input expression. 


The tpredicate returns a truthy result when the input expression (ex1)  matches the pattern subject to 
the conditions of the variable dictionary (vardict). Consider the following:

If the pattern matches the input expression, the tbody method is involked

NauralRule Subclasses
---------------------
When a group of natural rules must be create that will share common attributes,
it is expediant to create a NaturalRule subclass that has the common
attributes and then instantiate the rules from the subclass.

NaturalRule Class Attributes
++++++++++++++++++++++++++++
These are the NaturalRule class attribute:

predicate_rule attribute
    :ref:`donothing_rule<donothing-tag>`
vardict attribute
    empty dictionary
pattern attribute
    null expression
outcome attribute
    null expression
outcome_rule attribute
    :ref:`donothing_rule<donothing-tag>`

Create a NaturalRule Subclass
++++++++++++++++++++++++++++++++++++
The quasi python code below illustrates how to create a NaturalRule subclass. A
subclass is useful when a group of rules must be created that share
common attributes. All of the attribute assignments below, are optional.

.. code-block:: python
    :linenos:

    class NaturalRuleSubclass(NaturalRule):
        predicate_rule = <a predicate rule>
        vardict = <string >
                  # after the first instance is instantiated, this class
                  # attribute is converted to a variable dictionary
        pattern = <string>
                  # after the first instance is instantiated, this class
                  # attribute is parsed into a truealgebra expression
        outcome = <string>
                  # after the first instance is instantiated, this class
                  # attribute is parsed into a truealgebra expression
        outcome_rule = <a truealgebra rule>

HalfNaturalRule Class
=====================
The HalfNaturalRule is similar to the NaturalRule. Below shows the creatiion
of the PlusIntEval subclass and its instance, the rule plus_int_eval. This
rule preforms a numeric evaluation, when two integers are added together.

In a HalfNaturalRule rule there are no outcome or outcome_rule attributes.
But there is a body method defined which has (besides self) two positional
parameters, ``expr`` and ``var``. The ``expr`` parameter will be the rule
input expression.

The ``var`` parameter will is a var object. It will have a parmeter for every
variable in the substitution dictionry ``subdict`` in [[match method]].
The attribute name will be the variable name. Each var attribute points to the
value of the variable in the sustitution dictionary.

In the body method below:

``var.n0``
    is the expression that matches the variable ``n0``.
``var.n1``
    is the expression that matches the variable ``n1``.

.. ipython::

    In [1]: class PlusIntEval(HalfNaturalRule): 
       ...:     predicate_rule = predrule 
       ...:     vardict = ( 
       ...:         '  suchthat(forall(n0), isint(n0));' + 
       ...:         '  suchthat(forall(n0), isint(n0))' 
       ...:     ) 
       ...:     pattern = '  n0 + n1  ' 
       ...:  
       ...:     def body(self, expr, var):
       ...:         n0 = var.n0.value 
       ...:         n1 = var.n1.value 
       ...:         return Number(n0 + n1) 
       ...:  
       ...: plus_int_eval = PlusIntEval()

In a HalfNaturalRule, the body method is called by the tbody method. When a
rule is applied to an input expression and
finds a match, the body method result will be the result of the rule.

Rules Class
===========
A Rules Class instance is a rule that applies other rules.
The quasi python code below shows ``newrule`` being assigned a sequence
of rules.
rule below 

.. code-block:: python

   newrule = Rules(rule0, rule2, rule3, ..., rule_max)

A Rules instance
can take any number of other rules as arguments. These rules are executed
from left to right. The firat rule takes the input expression as an argument.
The rest of the rules take the previous rule's result as an input. The
reuslt of the last rule is the resut of 

.. ipython::

    In [1]: a = parse('a')
       ...: b = parse('b')
       ...: c = parse('c')
       ...: d = parse('d')

.. ipython::

    In [1]: cyclerule = Rules( 
       ...:     Substitute(subdict={a: b}),  # convert a to b 
       ...:     Substitute(subdict={b: c}),  # convert b to c 
       ...:     Substitute(subdict={c: d}),  # convert c to d 
       ...: ) 




Rules and RulesBU
=================

``Rules`` is a subclass of ``RulesBase`` and ``RulesBU`` is a subclass or ``Rules``. ``Rules`` and ``RulesBU`` are the same except the former has a bottomup attribute of ``True``.

Instances of the ``Rules`` and ``RulesBU`` classes have a ``rule_list`` attribute that is a list containing rules. ``Rules``  and ``RulesBU`` provide to users a powerful means of organizing and grouping rules to perform mathematical operations.

Rules
-----
When a Rules instance is instantiated, all position arguments (which must be rules) are placed in the ``rule_list`` attribute. The order of the position arguments is preserved in the list.

When a ``Rules`` instance is applied to an expression, the rules in ``rule_list`` will be applied in sequence from left to right. The process is the first rule in ``rule_list`` is applied to the input expression. Its output becomes the input for the next rule in ``rule_list`` . The process continues until the output of last rule in ``rule_list`` becomes the output of the ``Rules`` instance.

Below, the ``rule`` is a ``Rules`` instance that contains three rules defined in the RuleBase section above. The ``test_expr`` is a Symbol instance with name ``a``. The ``rule`` is applied to the ``test_expr`` and the result is the symbol ``d``.

.. ipython::

    In [1]: rule = Rules(a_b_rule, b_c_rule, c_d_rule)
       ...: test_expr = Symbol('a')
       ...: rule(test_expr)

What happened in the above example, is ``a_b_rule`` replaced the name ``a`` with the name ``b``.  The ``b_c_rule`` then replaced the name ``b`` with the name  ``c`` Then ``c_d_rule`` replaced the name ``c`` with the name ``d`` which was the final output of ``rule``.

RulesBU
-------
``RulesBU`` is useful for applying one or more rules bottom up. For a demonstration of ``RulesBU``, create below the expression ``another_test_expr``.

.. ipython::

    In [1]: sym_a = Symbol('a')
       ...: another_test_expr = Container('f', (sym_a, sym_a, sym_a))
       ...: another_test_expr

Create a rule using ``RuleBU`` that contains the sames three rules as the previous example with ``Rules``. Apply the new ``RuleBU`` rule to ``another_test_expr``.

.. ipython::

    In [1]: rule = RulesBU(a_b_rule, b_c_rule, c_d_rule)
       ...: rule(another_test_expr)

The three rules inside ``rule`` changed the all of the Symbol expressions names from ``a`` to ``b`` to ``c`` to ``d``.

Consider the case when there is a need to apply a single existing rule bottom up and the rule's bottomup attribute is ``False``. The recomended procedure is not to change the bottomup attribute but instead to wrap the rule in ``RulesBU`` as was done above. 

Bottom Up Rules Inside RulesBU
------------------------------
Consider the case when a RulesBU instance contains a rule that has its bottomup attribute set to ``True``.  When the RulesBU instance is applied to an expression, the internal rule can be applied numerous times to the same sub-expressions inside the expression. This can lead to a great increase in the execution time for a script. This behavior is in most cases, probably not useful.

JustOne and JustOneBU
=====================
``JustOne`` is a subclass of RuleBase that is similar to ``Rules``.  A  ``JustOne`` instance has a ``rule_list`` attribute that is a list. When a ``JustOne`` instance is instantiated, ``rule_list`` is filled with truealgebra rules, the same as with a ``Rules`` instance.

The unique feature of ``JustOne`` is that, in order to save on execution time, its instance will fully apply at most just one of the rules in its ``rule_list`` attribute.

When a ``JustOne`` instance is applied to an expression, the internal rules in the ``rule_list`` attribute are tested one by one, applying the predicate to the input expression. When an internal rule's predicate returns true it becomes the selected rule and the testing stops. The selected rule`s body is applied to the input expression and that result becomes the result of the ``JustOne`` rule.

In the example below,  ``justone_rule`` is created containing three other rules defined in the ChangeSymbolName Section above. These internal rules change the names of Symbol expressions.

.. ipython::

    In [1]: justone_rule = JustOne( a_b_rule, b_c_rule, c_d_rule)
       ...: test_expr = Symbol(" b ")
       ...: justone_rule(test_expr)

``justone_rule`` transformed the expression ``b`` to ``c``. The selected rule that accomplished this transformation was the second rule ``b_c_rule``.

It is important to notice above, that the third rule ``c_d_rule`` was not used. If the third rule had been applied, the expression ``c`` would have been transformed to ``d``. 

``JustOne`` rules can be nested. A ``JustOne`` rule can have a ``justOne`` rule in its ``rule_list`` attribute. Consider the ``test_rule`` below with a nested ``JustOne`` rule. 

.. ipython::

    In [1]: new_rule = JustOne(a_b_rule, rule, c_d_rule)
       ...: new_rule(test_expr)

The b_c_rule inside the nested JustOne rule was selected to transform the ``b`` into a ``c``. JustOne instances 

One characteristic of a ``JustOne`` rule is that it will ignore the ``path`` and bottomup attributes of all rules in its ``rule_list``. The reason for this characteristic is that a ``JustOne`` instance does not utilize the __call__ method of the rules in its ``rule_list``. It is the __call__ method that implements  ``path`` and bottomup.

``JustOneBU`` is a subclass of ``JustOne`` with the bottomup attribute set to ``True``.


Apply Rules using Path and Bottomup Attributes
==============================================
All rules have :ref:`path and bottomup attributes<rulebase-path-bottomup>`. By default the ``path`` attribute is an empty tuple and the bottomup attribute is ``False``. A rule with inon-default settings to these attributes can be applied to sub-expressions inside of an expression.

Create a new RuleBase subclass to help demonstrate use of the rule ``path`` and bottomup attributes.

.. ipython::

    In [1]: class ContainerNameX(Rule):
       ...:     def predicate(self, expr):
       ...:         return isinstance(expr, Container)
       ...: 
       ...:     def body(self, expr):
       ...:         return Container('X', expr.items)


Below is the definition of the ``test_expr`` expression that will be used to help illustrate the path and bottomup features. The top level of the expression is a Container instance with name ``f0``. Nested inside at increasingly lower levels are Container instances named ``f1``, ``f2``, and ``f3``. The lowest level are the Symbol instances ``a``.

.. ipython::

   In [1]: test_expr = parse(
      ...:      'f0('
      ...:    +    'f1('
      ...:    +         'f2(),'
      ...:    +         'f2(f3(a) , f3(a))'
      ...:    +     ')'
      ...:    +  ')'
      ...: )
      ...: print('test_expr =  ' + str(test_expr))

.. _path-label:

Use of Path Attribute
---------------------

Examples
++++++++

.. rubric:: Empty Path

As an example, create a ``ContainerNameX`` rule with an empty ``path``.  This rule has the same capabilities as a rule created with no ``path`` argument. Apply this rule to ``test_expr``. Only the top level ``f0`` container is changed to ``X``.

.. ipython::

   In [1]: rule = ContainerNameX(path=())
      ...: rule(test_expr)


.. rubric:: Index Path

A ``(0,)`` path causes the rule to be applied to the 0 index of the ``f0`` Container instance's ``items`` atrribute. The ``f1`` name changes to ``X``. 

.. ipython::

   In [1]: rule = ContainerNameX(path=(0,))
      ...: rule(test_expr)


.. rubric:: Double Index Path

A ``(0, 1)`` path causes the rule to be applied to the 1 index of the ``f1`` Container instance's ``items`` attribute. The second Container instance named ``f2`` is replaced with the name ``X``.

.. ipython::

   In [1]: rule = ContainerNameX(path=(0, 1))
      ...: rule(test_expr)

.. rubric:: Negative Index Path

Negative indexes can be used in paths in the same way as negative index in
python lists. A ``(0, -1)`` path produces the same result as the last example

.. ipython::

   In [1]: rule = ContainerNameX(path=(0, -1))
      ...: rule(test_expr)

.. rubric:: Index Path Length

A path can be of any length needed. Here, the second Container instance
named``f3`` is renamed as ``X``.

.. ipython::

   In [1]: rule = ContainerNameX(path=(0, 1, 1))
      ...: rule(test_expr)

Path Errors
+++++++++++
An error is created when a path is improper. The default in TrueAlgebra is to capture these errors and print out an error message. Also the sub-expression where the error occurred will become a Null instance.

.. rubric:: Type Error in Path

Below is the error message when an index of a path is of a type other than ``int``.

.. ipython::

   In [1]: rule = ContainerNameX(path=(0, 'one'))
      ...: rule(test_expr)

.. rubric:: Index Error in Path

Below is the error message when an index in the path is too large for the corresponding Container instance ``items`` attribute.

.. ipython::

   In [1]: rule = ContainerNameX(path=(0, 1, 100))
      ...: rule(test_expr)

.. rubric:: Path too Long

Atoms, such as Number and Symbol instances do not contain sub-expressions. When a path leads to an atom and still has superfluous indexes, this error message occurs:

.. ipython::

   In [1]: rule = ContainerNameX(path=(0, 1, 1, 0, 3))
      ...: rule(test_expr)

.. _bottomup-label:

Use of Bottomup Attribute
-------------------------
A rule applied bottom up to an expression will be applied to the expression and all available sub-expressions within the expression. The application of the rule starts at the bottom, lowest achievable level of the expression and progresses up until the rule is applied to the top level of the expression. 

Apply a ContainerNameX rule bottomup.

.. ipython::

   In [1]: rule = ContainerNameX(bottomup=True)
      ...: rule(test_expr)

Every Container instance name throughout ``test_expr`` was changed to ``X``.

Path and Bottomup
-----------------
A rule is applied first to its path if it is non-empty, and second the rule is applied bottom up if its ``bottomup attribute`` is ``True``.

.. ipython::

   In [1]: rule = ContainerNameX(path=(0, 1), bottomup=True)
      ...: rule(test_expr)

In the above example the Container names at path ``(0,1)`` and its sub-expressions are changed to ``X``.

.. _restricted-label:

Restricted Class Expressions
----------------------------
The class Restricted is a subclass of Container. Both classes have the same ``name`` and ``items`` atrributes. But some of their methods differ and as a result the Restricted class instances respond differently to rules applied with to a path or bottom up.

A rule with a nonempty ``path`` can be successfully applied when pointed to a Restricted instance, but will generate an error when pointed to the sub-expressions in the instance's ``items`` attribute. The internal sub-expressions are restricted to rules applied using path.

.. ipython::
   
    In [1]: another_test_expr = Container('f', (Restricted('restricted', (
       ...:     Container('f', ()),
       ...:     Container('f', ()),
       ...:     Container('f', ()),
       ...:     )),))
       ...: another_test_expr

Apply ContainerNameX rule to the Resistriced expression. The application works and the ``restricted`` name chages to ``X``,

.. ipython::

   In [1]: rule = ContainerNameX(path=(0,))
      ...: rule(another_test_expr)

Now apply the rule with a path to all three sub-expressions inside the Restricted expression. In all cases an error is generated.

.. ipython::

   In [1]: rule = ContainerNameX(path=(0,0))
      ...: rule(another_test_expr)

.. ipython::

   In [1]: rule = ContainerNameX(path=(0,1))
      ...: rule(another_test_expr)

.. ipython::

   In [1]: rule = ContainerNameX(path=(0,2))
      ...: rule(another_test_expr)

Apply a ContainerNameX rule bottom up. The Restricted expression's name is changes but not he names of the sub-expressions insde the Restricted expression are not chaged.

.. ipython::

   In [1]: rule = ContainerNameX(bottomup=True)
      ...: rule(another_test_expr)

.. _assign-label:

Assign Class Expressions
------------------------
The class Assign is a subclass of Container. The first item (with index 0) in the
items attribute of an Assign instance is protected from the application of a
rule through path or bottomup actions. 

For demonstraion, create yet another test expression that has an Assign instance
containing sub-expressions ``f()``, ``g()``, and ``h()``.

.. ipython::
   
    In [1]: yet_another_test_expr = Assign('assign', (
       ...:     Container('f', ()),
       ...:     Container('g', ()),
       ...:     Container('h', ()),
       ...:     ))
       ...: yet_another_test_expr

.. rubric:: Path Demonstatration

Now apply the ContainerNameX rule with a path pointing to ``f()``, the first
item in ``assign(f(), g(), h())``:

.. ipython::

   In [1]: rule = ContainerNameX(path=(0,))
      ...: rule(yet_another_test_expr)

The output is ``null`` accompanied by an  error message. The rule cannot be
applied to the first item ``f()``.

Now apply the rule, successfully, using a path attribute to ``g()`` and
```h()``. 

.. ipython::

   In [1]: rule = ContainerNameX(path=(1,))
      ...: rule(yet_another_test_expr)

.. ipython::

   In [1]: rule = ContainerNameX(path=(2,))
      ...: rule(yet_another_test_expr)

The path can be succussfully directed to any item except the first in the items
attribute of an Assign instance.

.. rubric:: Bottomup Demonstration

Apply a ContainerNameX rule bottom up. The Assign expression's name is changed.
All of the names of the sub-expressions inside the Assign expression are
changed except for the first. The first sub-expression is protected.

.. ipython::

   In [1]: rule = ContainerNameX(bottomup=True)
      ...: rule(yet_another_test_expr)
