=====
Rules
=====
To provide TrueAlgebra examples in a python script, modify the sys.path and import the necessary packages, modules, and objects.

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

__call__ Method
---------------
The __call__ method is defined in RuleBase. As a result, rules behave like functions.
Consider a python expression of the form ``rule(expr)`` where ``rule`` is a truealgebra rule
and ``expr`` is a truealgebra expression. The ``rule`` here takes ``expr`` as an argument and
evaluates it. The intent is that rules be viewed as fancy functions.

.. _tpred-and-tbody-tag:

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

donothing_rule Rule
-------------------
The  donothing_rule rule is a Rule instance. All Rule instances have the same charachteristics
as  donothing_rule. A  donothing_rule rule always returns its  input expressions, unchanged.
The donothing_rule always does nothing.

The  donothing_rule rule is sometimes useful as a default rule, For example it is
the value for the NaturalRule predicate_rule attribute which act as a default
for NaturalRule instances.

Substitute Rule
---------------

How to Create Rule Instances
----------------------------
To create rules that actually do something, unlike the  donothing_rule rule, first
create a Rule subclass. Three methods are over written below in the IsSym class.

__init__ method
    The __init__ method allows for passing arguments for use by the rule.
    The last line of the __init__ metod in the example below is very imporatant
    and must always be included, otherwise the __init__ methods of parent classes
    will not be executd.
predicate method
    The predicate method requires one positional parameter, which will be the 
    input expression of the rule. The method must returns either True or False.
    If True, the body method will be involked.
body method
    The predicate method requires one positional parameter, which will be the 
    input expression of the rule. The method must return a truealgebra
    expression. If this method is involked, its output will be the output
    of the rule.

.. ipython::

    In [1]: class IsSym(Rule):
       ...:     def __init__(self, *args, **kwargs):
       ...:         self.names = args
       ...:         # The line below must be included
       ...:         super().__init__(*args, **kwargs)
       ...:
       ...:     def predbcate(self, expr):  # expr is rule input expresion
       ...:         # This method must return True or False
       ...:         return (
       ...:             isinstance(expr, Container)
       ...:             and expr.name == 'issym'
       ...:             and len(expr.items) > 0
       ...:         )
       ...:
       ...:     def body(self, expr):  # expr is rule input expresion
       ...:         if isinstance(expr[0], Symbol) and expr[0].name in self.names:
       ...:             return Symbol('true')
       ...:         else:
       ...:             return Symbol('false')
       ...:         # This method must return a truealgebra expression 


The example below creates and tests the rule issym_rule from the class IsSym.

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

In the above first two cases, the rule predicate method evaluated to True and
as a result, the body method evaluated the input algebraic expression and the rule returned
the result. However in the third case, the predicate method returned False
resulting in the rule returning its input expression unevaluated by the body method.
expression.

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
       ...:     Substitute(subdict={a: b})  # convert a to b 
       ...:     Substitute(subdict={b: c})  # convert b to c 
       ...:     Substitute(subdict={c: d})  # convert c to d 
       ...: ) 
