===============================
Predicate Expressions and Rules
===============================
A predicate expression is a truealgebra expression that asserts
a mathematical property of its subexpression(s). Often Included with predicate
expressions are logical expressions such as ``and``, ``or``, and ``not``.

The symbols ``true`` and ``false`` are used to represent truth and falsehood.
Predicate rules evalute predicate and logic expressions to one of three
results:

Symbol ``true``
    indicating that the predicate/logic expression is true. 
    Truealgebra ``true`` is lower case to avoid confusion with
    python True.

Symbol ``false`` 
    indicating that the predicate/logic expression is false. 
    Truealgebra ``false`` is lower case to avoid confusion with
    python False.
 
Input expressio , unevaluated
    indicating the predicate/logic expression cannot be evaluated.

.. _predicate_rules-tag:

Setup Frontend with Predicate Rule
==================================
Import and set up the tasympy cas.

.. ipython::

    In [1]: import truealgebra.tasympy as cas
       ...: cas.setup_func()

Next create a frontend with ``fe.postrule.rule`` pointing to the pedicate
rule. The ``fe.prerule.rule`` is by default the ``donothing_rule``.

.. ipython::

    In [1]:  fe = cas.create_frontend(postrule = cas.predicate_rule_bu)



Number Predicate Expressions
=============================

isnumber
--------
The expression ``isnumber`` is a predicate function with one argument. When
evaluated by the predicate rule it determines if its argument is a number
or not 

.. ipython:: python

    fe(' isnumber(x); isnumber(2.0); isnumber(2/3); isnumber(I); isnumber(pi) ')

As shown above, ``isnumber`` returns ``false`` when its argument is not a
number. All the other predicate expressions below  differ in that they are not
evaluated when the predicate argument is not a number.

Next look at ``num`` below, which is a truealgebra Number object.
Its value attribute is a ``sympy.core.mul.Mul`` object containing
sympy numbers.  The expression ``isnumber(num)`` evaluates to ``true``. 

.. ipython:: python

   fe(' num := star(4, 2, pi, I) ', cas.evalnumbu)
   type(fe.history[-1][1].value)
   fe(' isnumber(num) ')

isrational
----------
The expression ''isrational`` evaluates to ``true`` whenever its argument
is an integer or a fraction.

.. ipython:: python

    fe(' isrational(2.3); isrational(I); isrational(2); isrational(4/5) ')

When the argument of ``isrational`` is not a number, the expression is
returned unevaluated as seen below.

.. ipython:: python

    fe(' isrational(x) ')

isinteger
----------
The expression ''isinteger`` evaluates to ``true`` whenever its argument
is an integer or a fraction.

.. ipython:: python

    fe(' isinteger(2.3); isinteger(I); isinteger(2); isinteger(4/5) ')

When the argument of ``isinteger`` is not a number, the expression is
returned unevaluated as seen below.

.. ipython:: python

    fe(' isinteger(x) ')

isreal
----------
The expression ''isreal`` evaluates to ``true`` whenever its argument
is an integer or a fraction.

.. ipython:: python

    fe(' isreal(2.3); isreal(I); isreal(2); isreal(4/5) ')

When the argument of ``isreal`` is not a number, the expression is
returned unevaluated as seen below.

.. ipython:: python

    fe(' isreal(x) ')


iscomplex
----------
The expression ''iscomplex`` evaluates to ``true`` whenever its argument
is an integer or a fraction.

.. ipython:: python

    fe(' iscomplex(2.3); iscomplex(I); iscomplex(2); iscomplex(4/5) ')



The infinity number is not complex.

.. ipython:: python

   fe(' iscomplex(oo) ')

When the argument of ``iscomplex`` is not a number, the expression is
returned unevaluated as seen below.

.. ipython:: python

    fe(' iscomplex(x) ')

