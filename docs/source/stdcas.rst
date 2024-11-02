
============
Standard CAS
============
The Standard CAS (Computer Algebra System) only imports packages and modules
available from python itself. Essentially it only usee only standard python
with no third party packages or modules required. 
For example, all ``stdcas`` Number objects contain only standard python objects.
Integers and reals are represented by python ``int``  and ``float`` objects.
Fraction are iare represented by ``Fraction`` objects from the ``fractions`` module.
The stdcas complex numbers are represented by the python ``complex`` class.


Import
======

Import as shown below from ``truealgebra.stdcas`` to get the standard CAS (Computer Algebra System).

.. ipython::

    In [0]: from truealgebra.stdcas import (
       ...:     frontend, Rules, RulesBU, JustOne, JustOneBU, toform0
       ...: )
       ...: fe = frontend
       ...: Ex = frontend.history

Above, the shorter name ``fe`` was defined for ``frontend``. It is highly desirable to have a very short name for the ``frontend``, as the name will be typed often in a TrueAlgebra session. 

Frontend
========
The ``FrontEnd`` class is developed in the module ``truealgebra.core.frontend``. In the import section above, the name ``fe`` refers to an instance of ``FrontEnd``. Use the word **frontend** to refer to any general instance of ``FrontEnd``.

A frontend is the primary user interface tool for TrueAlgebra. It provides a platform for the user to create TrueAlgebra expressions from python strings that represent mathematical expressions. The frontend also provides the means to create and apply TrueAlgebra rules to these expressions. Users have access to and can use the history of TrueAlgebra expressions previously created and transformed.

The frontend was designed for use in an interactive environment such as
ipython. The frontend ``__call__`` method is defined and frontend acts like a
function. A user can make a frontend call, then observe the consequences of
that call then repeat the process for as long as needed.

The use of a frontend will become a session of a series of user actions and
the frontend response.

What a Frontend Does
--------------------
When  a frontend is called, it takes a python string as a positional argument. That string  represents a mathematical expression and is parsed into a TrueAlgebra expression. Then, depending on the frontend instantiation and possible keyword arguments, TrueAlgebra rules are applied to the expression.

The typical steps during and following a ``fe`` function call are listed below. There are variations of
this process depending on the parameters passed by the user and changes to the settings of ``fe``.

    #. The user calls the frontend with a string argument and possibly keyword arguments.
    #. The string input is parsed into a TrueAlgebra expression, call it the expression
    #. The **history rule** ``fe.history_rule`` is applied to expression.
    #. The **assignment rule** ``fe.active_assign_rule`` is applied to the expression.
    #. The **default rule** ``fe.default_rule`` is applied to the expression.
    #. If the user passed a **user rule** in the function call to ``fe`` then it is applied to the expression.
    #. The ``fe.active_assign_rule`` is updated
    #. The expression is appended to the history list ``fe.history`` .
    #. The expression is printed in a user readable format.
    #. The result of a ``fe`` function call is ``None``
 
Take notice of the last step. The final TrueAlgebra expression is NOT
an output of ``ex`` but is instead stored into the frontend history list.

Frontend Example
----------------
Consider the following example Where only a string positional argument is provided.

.. ipython::

    In [0]: fe('  x := 5 + 3.2 * sin(1.57)**2 + cos(3.14/2)  ')

The printed output show the string representation of the final ``frontend``
expression. On the left of the printed line of the ipython cell above 
are the characters ``Ex(5)`` indicating that this is the number ``5``
(zero based index) expression that ``fe`` stored into its history.
For brevity, the python ``Ex`` has been assigned to ``fe.history``.
Look at the history at index 0.

.. ipython::

    In [0]: Ex[0]

In the above execution of ``fe`` there had been numeric calculations performed by the
rule ``evalnumeric`` inside ``fe.default_rule`` of the frontend. The default rule is easily setup by a user.

 
Next look at the assignment rule of the frontend.

.. ipython::

    In [0]: fe.active_assign_rule.assign_dict

The symbol ``x`` has been mapped to the number ``8.200794297474795``.

Assignment Rule
---------------
Assignments in the input expression of the frontend are of the form

``<variable> := <expr>``:
    ``<variable>`` and ``expr`` are both TrueAlgebra expressions.
    Although ``<variable>`` is usually a TrueAlgebra symbol. The symbol
    ``<variable>`` is assigned to ``<expr>``

    After assignment is made, Frontend uses a rule (``AssignRule`` instance)
    to convert any ``<variable>`` to ``expr``.

The ``:=``  operator which in this case denotes assignment.  
In the previous execution the symbol ``x`` was assigned

.. ipython::

    In [0]: fe('  f(x) + g(x) + h(x)')

Make another assignment to the symbol ``y``..

.. ipython::

    In [0]: fe('  y := 3  ')

Reassign ``x`` and use it.

.. ipython::

    In [0]: fe('  x := y + 2  ')
       ...: fe(' x  ')

The ``x`` on left side of ``:=`` was not affected by the assignment or any other rule.
But the ``y + 2`` on the right side had the assignment and default rule applied to it.

One requirement is that the ``:=`` expression must be at the top level.
In the example below The ``:=`` sub-expression if embedded inside the
function ``f``. No assignment is made in this case,

.. ipython::

    In [0]: fe('  z := 17  ')
       ...: fe(' z  ')

Frontend History Rule
---------------------
The history rule insert Items in the The ``fe.history`` list into the frontend expression being modified.
In the frontend expression, sub-expressions of the form ``Ex(n)`` where `n` is an integer
are replaced by the expression in history at index ``n`` . Consider the example:

.. ipython::

    In [0]: fe('  f(Ex(8), Ex(-1), Ex(1000), Ex(junk)) ')

The ``fe.history`` items at index's ``0`` and ``-1`` and inserted. But the 
out of range ``Ex(1000)`` and nonsenseial ``Ex(junk)`` are igored by the history rule.  

Frontend Keyword Arguments
--------------------------
Keyword arguments can be passed to a frontend to alter its behavior.

Mute
++++
By default, a frontend will print the final expression. Set the ``mute`` 
to ``True`` to stop the printing.

.. ipython::

    In [0]: fe(" 3*a + cos(b) ", mute=True)

Apply Additional Rule
+++++++++++++++++++++
The call of ``fe`` below  shows the use of the ``apply`` parameter which is
assigned the rule ``toform0``. The rule ``toform0`` algebraically simplifies the
expression to what is called form 0. This is a one time application
of the ``toform0`` rule.

.. ipython::

    In [0]: fe(' a * a**2 / a ', apply=toform0)
    

Hold Keyword Arguments
++++++++++++++++++++++
These arguments will cause frontend rules to not be applied. For demonstration
purposes assign the number ``7`` to the symbol ``z``.

.. ipython::

    In [0]: fe('  z := 7  ')

Below, there are no hold arguments. The assign rule substitutes ``7`` for
``z`` and the default rule performs numerical evaluation.

.. ipython::

    In [0]: fe('  z + 2 + 9  ')

Use the same input expression, but this time hold the assign rule.
The default rule is used, but the assign rule isn't.

.. ipython::

    In [0]: fe('  z + 2 + 9  ', hold_assign=True)

Enter the same input expression, but hod the default rule and there is no
numeric evaluation

.. ipython::

    In [0]: fe('  z + 2 + 9  ', hold_default=True)

With the ``hold_all`` parameter set to ``True``, both assign and default
rules are held. The expression is returned unchanged.

.. ipython::

    In [0]: fe('  z + 2 + 9  ', hold_all=True)


Parsing Line Breaks and Semicolons
----------------------------------
The object ``fe`` will treat strings with line breaks and semicolons as multiple expressions. The python string input below contains a line break.

.. ipython::

    In [1]: fe(""" cos(x)**2 + sin(x)**2 = 1
       ...:     1 + tan(x)** 2 = sec(x)**2 """,  hold_default=False)


This python string input contains a semicolon.

.. ipython::

    In [1]: fe(" sin(asin(x)) = x; sin(acsc(x)) = 1/x ")


Numerical Evaluation
====================

classes of numbers
add mult sub power div minus
trig
inverse trig
exp, ...

The default rule, ``evalnumeric`` in the frontend ``fe`` automatically evaluates numeric expression.

Fundamental Math Operators
--------------------------
the rule ``evalnumeric`` can deal with the common mathematical operations in the table below. The word "operator" here is used as a programming term.  An infix operator takes two arguments, one on each side. A prefix operator takes one argument, to its right. 

    * multiplication with infix operator symbol ``*``
    * addition with infix operator symbol ``+``
    * division with infix operator symbol ``/``
    * subtraction with infix operator, symbol ``-``
    * minus (unary) with prefix operator symbol ``-``
    * power with infix operator symbol ``**``

The following example demonstrates evaluation of the fundamental mathematical operations.

.. ipython::

    In [1]: fe('  2.3 + 7.1 * 2.0  - 3.0 ** 2 + - 1 ')

Numbers
-------
TrueAlgebra Number objects are wrappers around python number objects.
There are four python classes of numbers used. 

Python ``float`` objects can represent real numbers Any combination of a 
``float`` object with an ``int`` or ``fractions.Fraction`` object produces
a ``float`` object.

.. ipython::

    In [0]: fe('  2.3  ')
       ...: print(type(Ex[-1].value))
       ...: fe(' 2.3 * 2 * 2/3 ')

The python ``int`` class represents integers.
Fundamental mathematical operations between ``int`` objects  (except for
division) will always evaluate to an ``int`` object. 

.. ipython::

    In [0]: fe('  5  ')
       ...: print(type(Ex[-1].value))
       ...: fe(' 2 + 3 * 2 - 1 + 2**3 ')

Python ``fractions.Fraction`` objects represents fractions. Unlike python
division between integers becomes a fraction or  ``fractions.Fraction``
object.
fractions are automatically simplified. Fractions with 1 as a denominator become an integer.

.. ipython::

    In [0]: fe('  3/8  ')
       ...: print(type(Ex[-1].value))
       ...: fe(" 25 / 35 ; 100/60; 5/1 ")

Division by 0 will generate an error message by the python logging module.
The output in this case will be a TrueAlgebra Null object.

.. ipython::

    In [0]: fe('  6/0  ')

Python ``complex`` objects are used for complex numbers.
Complex numbers are created from the symbol j as the square root of negative one.

.. ipython::

    In [1]: fe('  j  ')
       ...: print(type(Ex[-1].value))
       ...: fe(" 2.0*j + 2; (3 + 2*j)* (1-j); 3 + 0*j ")


Evaluation of Trigonometric Functions
-------------------------------------
Trigonometric functions are numerically evaluated.

.. ipython::

    In [1]: fe('  cos(0.1) + sin(0.2) + tan(0.3 * j)  ')
       ...: fe('  sec(0.1) + csc(0.2) + cot(0.3)  ')

Inverse trigonometric functions are numerically evaluated as well.

.. ipython::

    In [1]: fe('  acos(0.1) + asin(0.2) + atan(0.3 * j)  ')
       ...: fe('  asec(0.1) + acsc(0.2) + acot(0.3)  ')

Exponential and logarithm Functions
-----------------------------------
The rule ``evalnumeric`` evaluates the exponential function ``exp``,
the natural log function ``log``, and log base 10 function ``log10``.

.. ipython::

    In [1]: fe('  exp(3.7); log(2.0 + 4.1*j); log10(2.5 *j)  ')

xxx
