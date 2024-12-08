from truealgebra.common.commonsettings import commonsettings
from truealgebra.common.eval_commassoc import EvalCommAssocBase

from truealgebra.core.expressions import (
    Container, CommAssoc, 
)

evalnum = commonsettings.evalnum
num0 = commonsettings.num0
num1 = commonsettings.num1


def addnums(num0, num1):
    return commonsettings.evalnum(CommAssoc('+', (num0, num1)))


def mulnums(num0, num1):
    return commonsettings.evalnum(CommAssoc('*', (num0, num1)))


def divnums(num0, num1):
    return commonsettings.evalnum(Container('/', (num0, num1)))


def subnums(num0, num1):
    return commonsettings.evalnum(Container('-', (num0, num1)))


def pwrnums(num0, num1):
    return commonsettings.evalnum(Container('**', (num0, num1)))


def negnum(num0):
    return commonsettings.evalnum(Container('-', (num0)))


class FlattenCommAssoc(EvalCommAssocBase):
    def body(self, expr):
        outlist = list()
        for item in self.gen(expr):
            outlist.append(item)
        return self.prep_output(outlist)


flattenstar = FlattenCommAssoc(name='*', ident=num1, bottomup=True)
flattenplus = FlattenCommAssoc(name='+', ident=num0, bottomup=True)


