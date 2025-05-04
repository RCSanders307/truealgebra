=======
Numbers
=======
In tasympy, Nunber objects are wrapped around sympy numbers.
There are two recomended ways to create tasympy Number objects

Setup and Accuracy
==================
Before importing tasympy and setting up settings, decide how many 
digit accuracy to use for float numbers. The default number of
digits is 15, the same as for sympy. For an accuracy of 15 digits
nothing special needs done. For an accuracy of 20 digits, the first
two steps must be:

.. ipython:: python

    from truealgebra.tasympy.utility import snum
    snum.accuracy = 20

It is recomended the above two lines be at the very beginning of a truealgebra
session, and the ``snum.accuracy`` not be changed again. The reason is that a
difference in accuracy can affect the equality of two sympy.Float numbers.

.. ipython:: python

   import sympy
   sympy.Float('1.0', 20) == sympy.Float('1.0', 15)
   Number(sympy.Float('1.0', 20)) == Number(sympy.Float('1.0', 15))

As shown above, the equality of truealgebra Number objects can be affected
by changes in accuracy. Truealgebra  often uses truealggebra expressions
in dictionaries, for
example the NaturalRule. So if the accuracy of float numbers is varied, there
is a chamce of incorrect or unexpected results. Therefore in
a session with truealgebra set ``snum.accuracy`` at the very beginning
if it is to be changed and
leave it unchanged throughout the rest of the session.

Next import, set up the tasympy cas, and create a frontend.

.. ipython:: python

    import truealgebra.tasympy as cas
    cas.setup_func()
    fe = cas.create_frontend()
    import sympy


Parsing Numbers
===============
Parsing is the easiest and recommended way to create Number objects
for common and normal needs. Specialized error messages will be diplayed
for many errors.

.. ipython:: python

    fe(' 7.54; 4.21e15 ')

Rational numbers which includes Integers and fractions can be parsed.

.. ipython:: python

    fe(' 3; 415/600; 23/1 ')

the square root of negative one represented by ``I`` can be parsed.
The rule ``cas.evalnumbu`` will combine ``I`` with other
numbers to represent more complex numbers.

.. ipython:: python

    fe(' I; 6 * I; 4 + 6 * I ', cas.evalnumbu)

Special sympy symbols can be parsed:

.. ipython:: python

   fe(' pi; E; EulerGamma; oo ')

Manual Number Creation
======================
Truealgebra Number objects containing symipy objects can be created manally
using methods of the `cas.snum` object. This is useful for the purposes of
testing, exprimenting, or writing new rules.

The `cas.snum.float` method is recomended for floats with a string argument.

.. ipython:: python

    float0 = cas.snum.float('2.3005005005')
    type(float0)
    type(float0.value)
    cas.snum.float(3.3005005005)

The first argument of the `cas.snum.float` method can be a python float.
But As explained in
`this sympy document <https://www.cfm.brown.edu/people/dobrush/am33/SymPy/numeric.html>`_
some python floats are only accurrate to about 15 digits as inputs.

For integers, the first argument of the `cas.snum.integer` method can be a string or a
python integer.

.. ipython:: python

    int0 = cas.snum.integer('237')
    type(int0)
    type(int0.value)

For fractions or rational numbers

.. ipython:: python

    rat0 = cas.snum.rational('7', '9')
    type(rat0)
    type(rat0.value)





.. ipython:: python

    aa = cas.parse(' f(345600000.234, 0.000349, 12340.4) ')
    cas.floatunparse4(aa)
    apn = cas.ApplyN(digits=4)
    apn(aa)


Reset snum.accuracy
===================
Setting ``snum.accuracy`` to ``None`` returns the sympy default accuracy
of 15 digits.

.. ipython:: python

   snum.accuracy = None

This is done here because there are other restructured text files in this
document that use the default accuracy.
