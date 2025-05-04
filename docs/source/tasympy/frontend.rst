.. _frontend-docs-tag:

========
Frontend
========
The FrontEnd class is developed in the module ``truealgebra.core.frontend``.
In the import section above, the name ``cas.fe`` refers to a FrontEnd
instance.
When  a frontend is called, it takes a python string as a positional argument.
That string represents a mathematical expression and is parsed into a
TrueAlgebra expression. Then, depending on particular details of the frontend,
TrueAlgebra rules csn be applied to the parsed expression and other operstions
occur..

A frontend is the user interface tool for TrueAlgebra. It provides a platform
for the user to create TrueAlgebra expressions from python strings that
represent mathematical expressions. The frontend also provides the means to
create and apply TrueAlgebra rules to these expressions.
Users have access to and can use the history of TrueAlgebra expressions
previously created and transformed.

The frontend was designed for use in an interactive environment such as
ipython. The frontend ``__call__`` method is defined and frontend acts like a
function. A user can make a frontend call, then observe the consequences of
that call then repeat the process for as long as needed.

The use of a frontend will become a session of a series of user actions and
the frontend response.

Import below from ``truealgebra.tasympy`` to get the tasymp CAS (Computer Algebra System).

.. ipython::

    In [0]: from truealgebra import tasympy as cas
       ...: cas.setup_func()
       ...: fe = cas.create_frontend()
       ...: Ex = fe.history

Above, the shorter name ``fe`` was defined for ``frontend``. It is highly desirable to have a very short name for the ``frontend``, as the name will be typed often in a TrueAlgebra session. 

Frontend Event
==============
An event is defined here as what happens when ``cas.frontend`` or the much 
shorter name ``fe`` is called with 
a python string as its first positional argument.
That string  represents a mathematical expression and is parsed into
TrueAlgebra expression and stored into frontend.expr.

The attribute ``fe.actions`` is a list of Action class instances called here
an action. The action attribute of every action in ``fe.actions`` is executed.
Below is a brief description of what each action does and the order they occur.

``fe.historyrule``, index: 0
    This action apples the rule fe.historyrule.rule to fe.expr. The rule is a
    truealgebra.core.frontend.HistoryRule object. The rule can substitute
    expressions from fe.history into fe.expr.

.. _assgnrule-tag:

``fe.assignrule``, index: 1
    Applies the rule ``fe.assgnrule.rule`` to fe.expr. This rule is an instance
    of truealgebra.core.frontend.ssignRule and
    makes substitutions into fe.expr using the dictionary fe.assigndict as 
    a map.

``fe.naturalrule``, index: 2
    Applies the rule ``fe.assgnrule.rule`` to fe.expr. This rule is an instance

``fe.prerule``, index: 3
    Applies the rule assigned to the attribute ``fe.prerule.rule`` to fe.expr.
    This rule can be reassigned. The prefix 'pre' indicates fe.prerule
    is executed before fe.eventrule.

``fe.eventrule``, index: 4
    During an frontend event, all ssstatic arguments after the first string
    arguments for the fe.__call__ method are stored in order in fe.rules.
    The fe.eventrule action applies the rules in fe.rules to fe.expr

    Note that in every event, the fe.rules attribute is reassigned before any
    actions are executed.

``fe.postrule``, index: 5
    Applies the rule assigned to the attribute ``fe.postrule.rule`` to fe.expr.
    This rule can be reassigned. The prefix 'post' indicates fe.prerule
    is executed after fe.eventrule.

.. _historyupdate-tag:

``fe.historyupdate``, index: 6
    The list fe.history is updated (appended) with fe.expr

.. _assgnupdate-tag:

``fe.assignupdate``, index: 7
    If fe.expr is an Assign expression with two items, The dictionary
    fe.assigneddict is updted.

.. _naturalruleupdate-tag:

``fe.naturalupdate``, index: 8
    If fe.expr is a Restricted expression with the name "Rule", and is
    formatted correctly, a NaturalRule instances is created and stored
    into the list fe.naturalrules.

.. _print-tag:

``fe.print``, index: 9
    The expression fe.expr is printed.
    
The above description is specific to the FrontEnd instance ``fe``. However the 
the process of creating an FrontEnd instqnce is very extendable. The actions
iand thier order can be adjusted as needed and new Action and FrontEnd
subclasses created to generate customized frontends for partictular purposes.

Print Action
============
The ``fe.print`` :ref:`action<print-tag>` prints the final expression ``fe.expr``.
But as demostared below, The frontend \_\_call\_\_ method result is None.

.. ipython:: python

    frontend_result = fe(' cos(x) ') 
    frontend_result is None

History
=======
The frontend histoty is
the list ``fe.history`` which contains the final expression ``fe.expr`` for
each event. The history can be thought of as a list of outputs from each event.
Below, the first item in the history list is the expression from the above
event. The ``fe.historyupate`` :ref:`action<historyupdate-tag>`
appends the event's ``fe.expr`` to the
history list.

.. ipython:: python

    print('history=  ', fe.history)

The ``fe.historyrule`` applies a rule to ``fe.expr`` makes subsitutes into
subexpressions that meet the floowing criteria:

    #. A Container instance with name 'Ex'. (The name can be set to something else)
    #. There is only one item in the items atttribute. That item is a Number instance.
    #. The value attribute of the Number object must be an integer.
    #. The integer must be in the range of acceptable indexes for the history list.

When the above conditions are met, the rule substitutes the appropriate expression
in the history rule. For example:

.. ipython:: python

    #fe(' f(Ex(0), Ex(-1)) ') 


The ``fe.historyrule`` action Now use the history rule

When the history rule will ignore all  Container expressions with inappropiate
indexs. Consider the example below.

The history rule insert Items in the The ``fe.history`` list into the frontend expression being modified.
In the frontend expression, sub-expressions of the form ``Ex(n)`` where `n` is an integer
are replaced by the expression in history at index ``n`` . Consider the example:

.. ipython:: python

    fe('  f(Ex(1.3), Ex(-1000), Ex(1000), Ex(junk)) ')

The history rule ignres entire expreeion.
The first index of ``Ex`` is a Float number.
The next two indexs are integers but are out of range. The index of the 
last ``Ex(junk)`` is parsed as a  Symbol object.


AssignRule Actions
==================

Assign Expression
-----------------
An assign expression is a truealgebras expression of the form
``<lhs> := <rhs>`` where ``<lhs>`` and ``<rhs>`` are any truealgebra 
expressions. The left hand side ``<lhs>`` is usually a truealgebra Symbol
instance. A assign expression means that ``<rhs>`` is assigned to ``<lhs>``.

The ``:=`` infix  operator is a definition of assignment. 
It does not represent mathemetical equality:
https://math.stackexchange.com/questions/25214/what-does-mean.

An assign expression is a Assign class instance and
its left hand side ``<lhs>``  argument will
not be accessed by rules applied bottomup.
The ``<lhs>`` will only be altered by rules specifically designed to do so.
Most rules will not alter the left hand side of a assign function.

AssignUpdate
------------
The ``fe.assignupdate`` :ref:`action<assgnupdate-tag>` updates 
the attribute ``fe.assigndict`` when ``fe.expr`` is an assign
expression: ``fe.assigndict[<lhs>] = <rhs>``.

As an example, ``fe.assigndict`` is  initially empty.
The symbol ``y`` is assigned to the symbol ``x``.
The number ``2`` is assigned to the symbol ``y``,
and the expresion ``g(x)`` is assigned to the expression ``f(z)``.

.. ipython:: python

    fe.assigndict
    fe(' x := a ; y := 2; f(z) := g(x) ')
    fe.assigndict

AssignRule
----------
The AssignRule action has an attribute ``fe.assignrule.rule`` that
makes substitutions based on 
the dictionary ``fe.assigndict``. For example:

.. ipython:: python

    fe('  func0(x) + func0(1) + f(z)  ')

Remap Assigndict Keys
---------------------
When the left hand side argument of an assign function is the same as a key
in ``fe.assigndict``, The value related to the key will become the right hand
side argument as seen below.

.. ipython:: python

    fe('  x := w  ')
    fe.assigndict

Modify Assign Expression
------------------------
The right hand side ``<rhs>`` in a assign expression can be modified by rules 
inside a frontend event. The ``assignupdate`` action
:ref:`action<assgnupdate-tag>` has index 7, and is
applied after all the frontend actions that apply rules.

As an example calculate the volume of a cuboid
First assign numbers to the ``height``, ``width``, and ``depth`` symbols.

.. ipython:: python

   fe(' height := 2.0; width := 3.0; depth := 4.0 ')
   fe.assigndict

Next calculate the volume using a formula.

.. ipython:: python

   fe(' volume := height * width * depth ')
   fe.assigndict

What happened inside the previous frontend event is after parsing``fe.expr``
was
``volume := height * width * depth``. The assignrule action converted
``fe.expr`` to ``volume := 2.0 * 3.0 * 4.0``. Then the ``fe.prerule`` action
converted ``fe.expr`` to ``volume := 24.0``. Then ``fe.assignupdate`` updates
``fe.assigndict``.

Frontend Naturalrule
--------------------
The :ref:`naturalruleupdate action<naturalruleupdate-tag>` allows a user to
create :ref:`NaturalRule instances<naturalrule_class-tag>` within a frontend
session. The :ref:`outcome_rule<naturalrule_attributes-tag>` is set to the
default :ref:`donothing_rule<donothing-tag>`, which does nothing.
The NaturalRule predicate_rule attribute is set to
:ref:`sympy.predicate_rule_bu<predicate_rules-tag>`.

the naturalruleupdate action creates a NaturalRule instance from the three
arguments of a Rule function in the frontend expression.

``forall`` function
    is the :ref:`first Rule argument<forall_function-tag>` that identifies
    variables used
    within the matching process for a NatualRule. A ``forall`` function can
    contain :ref:`suchthat functions<suchthat_function-tag>` that specify
    predicate expressions
    that a variable must satisfy.

pattern expression
    is the :ref:`second Rule argument<matching-tag>`. It is the pattern that
    must be matched for the rule to be applied.

outcome expression
    is the :ref:`third Rule argument<natural_substitution-tag>`.
    When a match is found, the outcome expression replaces the input expression.

Consider the example below.

.. ipython:: python

    fe(' Rule('
        'forall(x, y suchthat isrational(y) and y > 1/2),'
        'f(x, y),'
        'g(x, y)'
    ')' )

Blah blah

.. ipython:: python

   fe(' f(3.5, 2/3) ')



.. ipython:: python

    fe(' Rule(forall(theta), cos(theta)**2, 1 - sin(theta)**2) ')

When any expression matches the pattern, it is replaced by the outcome
In the first example below, the symbol ``z`` matches the vatiable ``theta`` in
the Rule pattern. In the second example, the expression ``cosh(w) ** 1.5``
mathches the variable `theta`` in the Rule pattern.

.. ipython:: python

    fe(' cos(z)**2 ')
    fe(' cos(cosh(w)**1.5)**2 ')
