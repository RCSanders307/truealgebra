========================
TrueAlgebra Introduction
========================
TrueAlgebra is a computer algebra system written entirely in Python. Knowledge and experience with python is essential for its use. TrueAlgebra was written to be very flexible and extendable. The core modules allow extension of TrueAlgebra to a wide range of algebras and applications.

The overall design was heavily influenced by the computer algebra system Yacas. TrueAlgebra create expression objects through parsing. The expression objects are manipulated and created by function like rules. Each rule has a predicate and a body. The predicate determines if the rule applies to a particular expression and the body will, if needed, perform the desired operation. This use of rules and expressions is analogous to the application of mathematical theorems to mathematical expressions. Thus the name True-Algebra.

The TrueAlgebra package is intended to be used in an interactive environment. It has already been used extensively with ipython and Jupyter. TrueAlgebra should work with Jupyterlab. In an interactive session, A user creates TrueAlgebra expressions and applies TrueAlgebra rules to the expressions.

Depending on the environment, a TrueAlgebra sessions can be saved and distributed to others as a document. One goal of TrueAlgebra is to expedite the creation of mathematical documents.

This Documentation was created using sphinx with an IPython ipython_directive installed as an extension in the sphinx configuration file. For the documentation below ipython input statements were entered into the source files. When html files were created from the source files, the ipython inputs were evaluated. It is as though a reader of the documentation is seeing an interactive ipython session.


