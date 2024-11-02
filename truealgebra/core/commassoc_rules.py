# rules for communative/asscocative functions

from . import rule as rule_m
from . import expressions as expr_m


def _index_filter(rmargs, expr):
    new = []
    leng = len(expr)
    for arg in rmargs:
        if arg < 0:
            arg += leng
        if arg not in new:
            new.append(arg)
    return new


class CommAssocBase(rule_m.Rule):
    def predicate(self, expr):
        return expr.etype == 'commassoc'


class ToTheLeft(CommAssocBase):
    def body(self, expr):
        ndex = _index_filter(self.args, expr)
        xx = [aa for (ii, aa) in enumerate(expr) if ii not in ndex]
        yy = [expr[ii] for ii in ndex]
        return expr_m.CommAssoc(expr.name, tuple(yy + xx))


class ToTheRight(CommAssocBase):
    def body(self, expr):
        ndexes = _index_filter(self.args, expr)
        xx = [aa for (ii, aa) in enumerate(expr) if ii not in ndexes]
        yy = [expr[ii] for ii in ndexes]
        return expr_m.CommAssoc(expr.name, tuple(xx + yy))


class GatherLeft(CommAssocBase):
    def body(self, expr):
        ndexes = _index_filter(self.args, expr)
        if not ndexes:
            return expr
        point = ndexes[0]
        xx = [aa for (ii, aa) in enumerate(expr[:point])
                if ii not in ndexes]
        yy = [expr[ii] for ii in ndexes]
        zz = [aa for (ii, aa) in enumerate(expr[point:])
                if (ii + point) not in ndexes]
        return expr_m.CommAssoc(expr.name, tuple(xx + yy + zz))


class GatherRight(CommAssocBase):
    def body(self, expr):
        ndexes = _index_filter(self.args, expr)
        if not ndexes:
            return expr
        point = ndexes[-1]
        xx = [aa for (ii, aa) in enumerate(expr[:point])
                if ii not in ndexes]
        yy = [expr[ii] for ii in ndexes]
        zz = [aa for (ii, aa) in enumerate(expr[point:])
            if (ii + point) not in ndexes
        ]
        return expr_m.CommAssoc(expr.name, tuple(xx + yy + zz))


class Flatten(CommAssocBase):
    def __init__(self, *args, **kwargs):
        self.args = args
        super().__init__(*args, **kwargs)

    def body(self, expr):
        newitems = []
        if not self.args:
            for ex in expr:
                if ex.name == expr.name and ex.etype == 'commassoc':
                    newitems.extend(ex.items)
                else:
                    newitems.append(ex)
            return expr_m.CommAssoc(expr.name, newitems)

        ndexes = _index_filter(self.args, expr)
        for (ii, ee) in enumerate(expr):
            if (ii in ndexes
                    and ee.etype == 'commassoc'
                    and ee.name == expr.name):
                newitems.extend(ee.items)
            else:
                newitems.append(ee)
        return expr_m.CommAssoc(expr.name, newitems)


flatten = Flatten(bottomup=True)


# *rmargs must be monotonically increasing integers
# This rule will require a lot of testing
class Group(CommAssocBase):
    def body(self, expr):
        if not self.args:
            return expr
        indexes = iter(self.args)
        leng = len(expr)
        indx = next(indexes, None)
        items = list(expr[0:indx])

        nex = next(indexes, None)
        while nex:
            new = expr[indx:nex]
            if len(new) > 1:
                items.append(expr_m.CommAssoc(expr.name, new))
                indx = nex
            nex = next(indexes, None)
        items.extend(expr[indx:leng])
        if len(items) == 1:
            return items[0]
        else:
            return expr_m.CommAssoc(expr.name, tuple(items))
