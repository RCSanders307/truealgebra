========
Overview
========
the RuleBase and ExprBase classes and their subclasses provide the basis for TrueAlgebra. In the interest of brevity, two naming conventions will be used.

    * The word "rule" or phrase "truealgebra rule" identifies an instance of a RuleBase subclass.  
    * The word "expression" or phrase "truealgebra expression"  identifies an instance of an ExprBase subclass.

ExprBase, RuleBase, and their subclasses do not strictly follow object oriented programming practices and commonly accepted recommendations for use of Python classes. 

     "Classes provide a means of bundling data and functionality together. Creating a new class creates a new type of object, allowing new instances of that type to be made. Each class instance can have attributes attached to it for maintaining its state. Class instances can also have methods (defined by its class) for modifying its state."

     -- Section 9 of the Python Tutorial in Python 3.7.0 Documentation, https://docs.python.org/3/tutorial/classes.html

The RuleBase and its subclasses provide a means of bundling functionality and allows use of inheritance, but their instances, the truealgebra rules, contain no true data or state that is maintained. The __call__ method of truealgebra rules is defined and rules can be thought of and are used as fancy functions. The data attributes of these instances are primarily parameters to guide the function-like capabilities.

The ExprBase subclasses also provide a means of bundling functionality and allows use of inheritance. But, their instances, the truealgebra expressions, do not contain the data, and are instead the data. To the user of TrueAlgebra the expressions are passive unchanging objects that just sit there idle, waiting to be acted upon by rule objects. The truealgebra expressions are the state that is maintained by the truealgebra rules.

Under the surface, and not readily apparent to a casual user of TrueAlgebra, expressions and rules are closely intertwined. All expressions have methods,such as bottomup, apply2path, and match that serve to assist rules. Rules will at times call and even pass themselves as arguments to these expression methods.

