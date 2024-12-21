from truealgebra.common.commonsettings import commonsettings as comset
from truealgebra.common.eval_commassoc import EvalCommAssocBase

from truealgebra.core.expressions import (
    Container, CommAssoc, 
)
from IPython import embed


def addnums(num0, num1):
    return comset.evalnum(CommAssoc('+', (num0, num1)))


def mulnums(num0, num1):
    return comset.evalnum(CommAssoc('*', (num0, num1)))


def divnums(num0, num1):
    return comset.evalnum(Container('/', (num0, num1)))


def subnums(num0, num1):
    return comset.evalnum(Container('-', (num0, num1)))


def pwrnums(num0, num1):
    return comset.evalnum(Container('**', (num0, num1)))


def negnum(num0):
#   xxx = 101; embed()
    return comset.evalnum(Container('-', (num0,)))


class FlattenCommAssoc(EvalCommAssocBase):
    def body(self, expr):
        outlist = list()
        for item in self.gen(expr):
            outlist.append(item)
        return self.prep_output(outlist)


flattenstar = FlattenCommAssoc(name='*', ident=comset.num1, bottomup=True)
flattenplus = FlattenCommAssoc(name='+', ident=comset.num0, bottomup=True)


def create_starCA(alist):
    length = len(alist)
    if length == 0:
        return comset.num1
    elif length == 1:
        return alist[0]
    else:
        return CommAssoc('*', alist)


def create_plusCA(alist):
    length = len(alist)
    if length == 0:
        return comset.num0
    elif length == 1:
        return alist[0]
    else:
        return CommAssoc('+', alist)
