from fractions import Fraction

from truealgebra.core import expressions as e
from truealgebra.core import rule as r

# This module contains functions and expressions used inside rule body and inner_body methods.
# This module does not create Rule classes or Rule class instances

import logging
logger = logging.getLogger('std.eval logger')
logger.setLevel(logging.ERROR)

# These functions take Number class istances as arguments
# The arguments are not checked to see if they are Number class instances
# The function outputs are Number call instances
def starf(n0, n1):
    return e.Number(n0.value * n1.value)

def plusf(n0, n1):
    return e.Number(n0.value + n1.value)

def subtf(n0, n1):
    return e.Number(n0.value - n1.value)

def negf(n0):
    return e.Number(- n0.value)

def divf(n0, n1):
    try:
        if isinstance(n0.value, int) and isinstance(n1.value, int):
            return Fraction(n0.value, n1.value)
        else:
            return e.Number(n0.value / n1.value)
    except ZeroDivisionError:
        logger.exception("divide function, {0} / {1}".format(n0.value, n1.value))
        return e.Container(name="/", items=(n0, n1))

def powf(n0, n1):
    if isinstance(n0.value, int) and isinstance(n1.value, int) and n1.value < 0:
        return e.Number(Fraction(1, n0.value ** -n1.value))
    else:
        return e.Number(n0.value ** n1.value)
       
# a function that returns True or False, ex is assumed to be an Expression
def isnumf(ex):
    return ex.etype == "number"
def isstarf(ex):
    return ex.etype == "function" and ex.name == "*"
def isdivf(ex):
    return ex.etype == "function" and ex.name == "/"
def ispowf(ex):
    return ex.etype == "function" and ex.name == "**"

def mkplusf(items):
    if len(items) == 0:
        return plus_ident
    elif len(items) == 1:
        return items[0]
    else:
        return e.CommAssoc(name="+", items = tuple(items))

def mkstarf(items):
    if len(items) == 0:
        return star_ident
    elif len(items) == 1:
        return items[0]
    else:
        return e.CommAssoc(name="*", items = tuple(items))

def mkpowf(ex0, ex1):
    return e.Container(name="**", items=(ex0, ex1))
    
def mkdivf(ex0, ex1):
    return e.Container(name="/", items=(ex0, ex1))
    
# Expression class instances
plus_ident = e.Number(0)
star_ident = e.Number(1)

