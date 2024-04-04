# TrueAlgebra
TrueAlgebra is a computer algebra program written in Python and intended to be used in an interactive environment such as ipython or Jupyter.

Website: to be developed.
Author: Robert C Sanders, rcsanders307@gmail.com

TrueAlgebra is free software licensed under the 3 clause version of the BSD license.

The current development work has been done using python 3.11.2. There has been no recent tests using earlier versions of python. TrueAlgebra is a work in progress.

## Overview
TrueAlgebra represents mathematical expression with ``ExprBase`` class objects called truealgebra expressions. Mathematical operations are implemented through ``RuleBase`` class instances called truealgebra rules. The Basic design, borrowed from the algebra program Yacas, closely follows the natural process of mathematics. 

In mathematics, conducted using paper and pen, mathematical expressions are written down on paper. These expressions are of course, passive and inanimate, they sit on the paper and do nothing but be observed. The syntax and format of these written mathematical expressions are governed by very precise definitions which varies depending on the branch of mathematics. Then the written expressions are manipulated in accordance with mathematical theorems and new expressions are created, often further down on the same piece of paper. The process is repeated as long as needed. That is how mathematics is done.

An interactive session of TrueAlgebra duplicates the above process, hence the name "TrueAlgebra". A TrueAlgebra user enters a python string as an argument into a TrueAlgebra ``FrontEnd`` instance call. The string has a mathematical syntax and is parsed into a TrueAlgebra expression and TrueAlgebra rules are applied to it to create new expressions.

The TrueAlgebra core modules are very flexible and extendable. The core modules allow extension of TrueAlgebra to a wide range of algebras and applications. The parsing is controlled by ``Settings`` instance that can be changed.

## Install
To install latest release of TrueAlgebra with pip run

``pip install truealgebra``

or from the source tree

``pip install .``

## Documentation
TrueAlgebra documentation is written in reStructuredText format. The final documentation are html files generated using the ``sphinx-build``command. The ``TrueAlgebra/docs/README.md`` file describes how to build the documentation.

Future plans include creating a website will be to display the documentation.

