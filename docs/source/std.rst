============
Standard CAS
============
The Standard CAS (Computer Algebra System) only imports packages and modules
available from python itself. Essentially it only usee only standard python
with no third party packages or modules required. 
For example, all Number objects contain only standard python objects.
Integers and reals are represented by python ``int``  and ``float`` objects.
Fraction are iare represented by ``Fraction`` objects from the ``fractions`` module.
The stdcas complex numbers are represented by the python ``complex`` class.

Import as shown below to get the standard CAS (Computer Algebra System).

.. ipython::

    In [0]: from truealgebra import std as cas
       ...: cas.setup_func()
       ...: fe = cas.create_frontend(
       ...:     prerule=JustOneBU(cas.evalnum, cas.predicate_rule),
       ...:     postrule=RulesBU(cas.simplify),
       ...: )
       ...: Ex = fe.history

Frontend
========
The primary means of interacting with truealgebra is the FrontEnd object called
the frontend.

.. ipython:: python

   fe(' height := 25.0; width := 30.0; depth := 2.0 ')
   fe(' volume := height * width * depth ')
   fe.assigndict


For the Standard CAS (truealgebra.std package) frontend, follow the
documentation in the :ref:`frontend documentation<frontend-docs-tag>` of the
tasympy section.



Numbers
=======
In the std CAS, TrueAlgebra Number objects are wrappers around python number
objects. There are four python classes of numbers used.

Float Numbers
-------------
Digits with a decimal point are parsed as python float objects.
If a ``-`` character is in front of a digit it is parserd as a
negative number.
Stings with an exponential foramt are also parsed as python float obejcts.

.. ipython:: python

    fe(' 2.375 ')
    type(Ex[-1].value)
    fe(' -19.6 ')
    type(Ex[-1].value)
    fe(' 4.5e-2 ')
    type(Ex[-1].value)


Integer Numbers
---------------
digits without a decimal point are parsed as Number objects with python int
integers. If a ``-`` character is in front of a digit it is parserd as a
negative number.


.. ipython:: python

    fe(' 57 ')
    type(Ex[-1].value)
    fe(' -107 ')
    type(Ex[-1].value)

Fraction Numbers
----------------
Python ``fractions.Fraction`` objects represents fractions.
Unlike python
division between integers becomes a fraction or  ``fractions.Fraction``
object.
fractions are automatically simplified.
Fractions with 1 as a denominator become an integer.
Divison by 0, creates a error message and an output on ``null``.

.. ipython:: python

    fe(' 2/3 ')
    type(Ex[-1].value)
    fe(' 6/2; 23/46; -4/5 ')
    fe(' 4/0 ')

Division by 0 will generate an error message by the python logging module.
The output in this case will be a TrueAlgebra Null object.

Complex Numbers
---------------
Python ``complex`` objects are used for complex numbers.
Complex numbers are created from the symbol j as the square root of negative one.

.. ipython:: python

    fe(' j ')
    type(Ex[-1].value)
    fe(' 37.5 + 3.0 * j ')
    type(Ex[-1].value)
    fe(' 27.5 + 0.0 * j ')

Numerical Evaluation
====================
The rules ``evalnum`` and evalnumbu from truealgebra.std.evalnum, evaluates
numerical expression.
The frontend action
fe.prerule applies evalnum bottomup. 

Fundamental Math Operators
--------------------------
the rule ``evalnum`` deals with the common mathematical operations listed
below. All evaluations are by the equivalent python operator.
The word "operator" here is used as a programming term.
An infix operator takes two arguments, one on each side.
A prefix operator takes one argument, to its right. 

    * multiplication with infix operator symbol ``*``
    * addition with infix operator symbol ``+``
    * division with infix operator symbol ``/``
    * subtraction with infix operator, symbol ``-``
    * minus (unary) with prefix operator symbol ``-``
    * power with infix operator symbol ``**``

The following example demonstrates evaluation of the fundamental mathematical
operations.

.. ipython:: python

   fe(' 2.3 * 2; 2 ** 1.4; 7 / 1.5; - j; 2 - 2/3; 4/5 + 6/5')

Trigonometric Functions
-----------------------
Trigonometric functions are numerically evaluated. The python cmath module is
used for thr evaluations. The csc, sec, and cot evaluations were calculated
with formulas using other cmath functions.

.. ipython:: python

    fe('  cos(0.1) + sin(0.2) + tan(0.3 * j)  ')
    fe('  sec(0.1) + csc(0.2) + cot(0.3)  ')

Inverse Trigonometric Functions
-------------------------------
Inverse trigonometric functions are numerically evaluated as well.
The acsc, asec, and acot evaluations were calculated
with formulas using other cmath functions.

.. ipython:: python

    fe('  acos(0.1) + asin(0.2) + atan(0.3 * j)  ')
    fe('  asec(0.1) + acsc(0.2) + acot(0.3)  ')

Exponential and logarithm Functions
-----------------------------------
The rule ``evalnum`` evaluates the exponential function ``exp``,
the natural log function ``log``, and log base 10 function ``log10``.

.. ipython:: python

    fe('  exp(3.7); log(2.0 + 4.1*j); log10(2.5 *j)  ')
