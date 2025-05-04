============
Introduction
============
This needs some work.

Import
======

Import as shown below from ``truealgebra.stdcas`` to get the standard CAS (Computer Algebra System).

.. ipython::

    In [0]: from truealgebra import tasympy as cas
       ...: cas.setup_func()
       ...: fe = cas.create_frontend()
       ...: Ex = fe.history

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
rule ``evalnumeric` inside ``fe.default_rule`` of the frontend. The default rule is easily setup by a user.

 
Next look at the assignment rule of the frontend.

.. ipython::

    In [0]: fe.assigndict

The symbol ``x`` has been mapped to the number ``8.200794297474795``.

Frontend Keyword Arguments
--------------------------
Keyword arguments can be passed to a frontend to alter its behavior.

Mute
++++
By default, a frontend will print the final expression. Set the ``mute`` 
to ``True`` to stop the printing.

.. ipython::

    In [0]: fe.print.wait()
       ...: fe(" 3*a + cos(b) ")

Apply Additional Rule
+++++++++++++++++++++
The call of ``fe`` below  shows the use of the ``apply`` parameter which is
assigned the rule ``toform0``. The rule ``simplify`` algebraically simplifies the
expression to what is called form 0. This is a one time application
of the ``simplify`` rule.

.. ipython::

    In [0]: fe(' a * a**2 / a ', cas.simplify)

    

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

    In [0]: fe.assignrule.wait()
       ...: fe('  z + 2 + 9  ')

Enter the same input expression, but hod the default rule and there is no
numeric evaluation

.. ipython::

    In [0]: fe.prerule.wait()
       ...: fe('  z + 2 + 9  ')


Parsing Line Breaks and Semicolons
----------------------------------
The object ``fe`` will treat strings with semicolons as multiple expressions. 


This python string input contains a semicolon.

.. ipython::

    In [1]: fe(" sin(asin(x)) = x; sin(acsc(x)) = 1/x ")


