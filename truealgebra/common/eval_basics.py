from truealgebra.core.rules import Rule
from truealgebra.core.expressions import (
    Number, CommAssoc, isCommAssoc, isContainer, isNumber
)


class EvalCommAssocBase(Rule):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name']
        self.ident = kwargs['ident']
        super().__init__(*args, **kwargs)

    def iscommassoc(self, expr):
        return isinstance(expr, CommAssoc) and expr.name == self.name

    def gen(self, ca_expr):
        for item in ca_expr.items:
            if isCommAssoc(item, name=self.name):
                for inner_item in self.gen(item):
                    yield inner_item
            else:
                yield item

    def predicate(self, expr):
        return isCommAssoc(expr, name=self.name)

    def body(self, expr):
        return expr

    def prep_output(self, outlist):
        if not len(outlist):
            return self.ident
        elif len(outlist) == 1:
            return outlist[0]
        else:
            return CommAssoc(self.name, outlist)


class CalcCommAssoc(EvalCommAssocBase):
    def __init__(self, *args, **kwargs):
        self.func = kwargs['func']
        super().__init__(*args, **kwargs)

    def body(self, expr):
        outlist = list()
        num = self.ident.value
        for item in self.gen(expr):
            if isinstance(item, Number):
                num = self.func(num, item.value)
            else:
                outlist.append(item)
        if num != self.ident.value:
            outlist.insert(0, Number(num))
        return self.prep_output(outlist)


# Python Operator Functions
# ==================
def power_function(n0, n1):
    if isinstance(n0, int) and isinstance(n1, int) and n1 < 0:
        return Fraction(1, n0 ** - n1)
    else:
        return n0 ** n1


def divide_function(n0, n1):
    if isinstance(n0, int) and isinstance(n1, int):
       return Fraction(n0, n1)
    else:
        return n0 / n1


def subtract_function(n0, n1):
    return n0 - n1


def negative_function(n0):
    return - n0


def multiply_function(n0, n1):
    return n0 * n1


def add_function(n0, n1):
    return n0 + n1


# ============
# EvalMathDict
# ============
class EvalMathDictSingle(Rule):
    arity = 1

    def __init__(self, *args, **kwargs):
        self.namedict = kwargs['namedict']
        super().__init__(*args, **kwargs)

    def predicate(self, expr):
        return (
            isContainer(expr, arity=self.arity)
            and expr.name in self.namedict
            and self.item_predicate(expr)
        )

    def body(self, expr):
        func = self.namedict[expr.name]
        try:
            return Number(self.calculation(func, expr))
        except ZeroDivisionError:
            eval_logger('Division by zero.')
            return null
        except TypeError:  # complex number
            eval_logger('Complex number cannot be handled.')
            return null
        except AttributeError:  # value eroror
            eval_logger('Number instance must have value attribute.')
            return null

    def calculation(self, func, expr):
        return func(expr[0].value)

    def item_predicate(self, expr):
        for item in expr:
            if not isNumber(item):
                return False
        return True


class EvalMathDictDouble(EvalMathDictSingle):
    arity = 2

    def calculation(self, func, expr):
        return func(expr[0].value, expr[1].value)

