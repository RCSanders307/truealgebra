from truealgebra.core.rulebase import RuleBase
from truealgebra.core.expression import Number, CommAssoc


class EvalCommAssocBase(RuleBase):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name']
        self.ident = kwargs['ident']
        super().__init__(*args, **kwargs)

    def iscommassoc(self, expr):
        return isinstance(expr, CommAssoc) and expr.name == self.name

    def gen(self, ca_expr):
        for item in ca_expr.items:
            if self.iscommassoc(item):
                for inner_item in self.gen(item):
                    yield inner_item
            else:
                yield item

    def predicate(self, expr):
        return self.iscommassoc(expr)

    def body(self, expr):
        return expr

    def prep_output(self, outlist):
        if not len(outlist):
            return self.ident
        elif len(outlist) == 1:
            return outlist[0]
        else:
            return CommAssoc(self.name, outlist)


class FlattenCommAssoc(EvalCommAssocBase):
    def body(self, expr):
        outlist = list()
        for item in self.gen(expr):
            outlist.append(item)
        return self.prep_output(outlist)


flattenstar = FlattenCommAssoc(name='*', ident=Number(1))
flattenplus = FlattenCommAssoc(name='+', ident=Number(0))


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


multiply = CalcCommAssoc(name='*', ident=Number(1), func=lambda x, y: x*y)
add = CalcCommAssoc(name='+', ident=Number(0), func=lambda x, y: x+y)
