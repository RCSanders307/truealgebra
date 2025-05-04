from truealgebra.core.rules import (
    RuleBase, donothing_rule, TrueThing, Substitute
)
from truealgebra.core.settings import settings
from truealgebra.core.parse import meta_parser
from truealgebra.core.expressions import (
    null, Symbol, true, isContainer, isSymbol, ExprBase
)
from truealgebra.core.err import ta_logger
import types

from IPython import embed


class TrueThingNR(TrueThing):
    """Used with NaturalRule instances.
    """
    def __init__(self, expr, subdict=types.MappingProxyType(dict())):
        self.expr = expr
        self.subdict = subdict


class TrueThingHNR(TrueThing):
    """Thruething used with HalfNaturalRule instances. """
    def __init__(self, expr, var=None):
        self.expr = expr
        self.var = var


class NaturalRuleBase(RuleBase):
    predicate_rule = donothing_rule
    pattern = null
    # as per:
    # https://adamj.eu/tech/2022/01/05/how-to-make-immutable-dict-in-python/
    # the default vardict below is a immutable dictioary
    vardict = types.MappingProxyType(dict())
    varstring = ''

    # vardict is not changed after it is created
    def __init__(self, *args, **kwargs):
        if "predicate_rule" in kwargs:
            self.predicate_rule = kwargs["predicate_rule"]

        if 'pattern' in kwargs:
            self.pattern = kwargs['pattern']
        try:
            if isinstance(self.pattern, str):
                self.pattern = settings.parse(self.pattern)
        except TypeError:
            ta_logger.log(
                'settings.parse must point to a Parse instance'
            )

        if "vardict" in kwargs:
            if isinstance(kwargs['vardict'], str):
                self.vardict = self.create_vardict(kwargs['vardict'])
            elif isinstance(kwargs['vardict'], ExprBase):
                self.vardict = self.expr_to_vardict(kwargs['vardict'])
            else:
                self.vardict = kwargs['vardict']

        self.convert_classvar()

        super().__init__(*args, **kwargs)

    @classmethod
    def process_forall(cls, vardict, expr):
        if (
            isContainer(expr)
            and expr.name in settings.categories['forall']
        ):
            for item in expr.items:
                if isSymbol(item):
                    vardict[item] = true
                elif (
                    isContainer(item)
                    and item.name in settings.categories['suchthat']
                    and len(item.items) == 2
                    and isSymbol(item[0])
                ):
                    vardict[item[0]] = item[1]
                elif (
                    isContainer(item)
                    and item.name in settings.categories['forall']
                ):
                    cls.process_forall(vardict, item)

    @classmethod
    def expr_to_vardict(cls, expr):
        vardict = dict()
        cls.process_forall(vardict, expr)
        return types.MappingProxyType(vardict)

    @classmethod
    def create_vardict(cls, string):
        expr = settings.parse(string)
        return cls.expr_to_vardict(expr)
                    
    @classmethod
    def convert_classvar(cls):
        """Create a variable dictionary used for pattern matching

        string : str instance is parsed into truealgebra expressions
            containing forall and suchthat expressions.

        Output
        ------
        vardict : dict
            The keys are Symbol instances called variables.
            the values are the predicates that the variables must satisfy
        """
        if isinstance(cls.vardict, str):
            cls.vardict = cls.create_vardict(cls.vardict)


class NaturalRule(NaturalRuleBase):
    outcome_rule = donothing_rule
    outcome = null

    def __init__(self, *args, **kwargs):

        if "outcome_rule" in kwargs:
            self.outcome_rule = kwargs["outcome_rule"]

        if 'outcome' in kwargs:
            self.outcome = kwargs['outcome']
        if isinstance(self.outcome, str):
            self.outcome = settings.parse(self.outcome)

        super().__init__(*args, **kwargs)

    def tpredicate(self, expr):
        subdict = dict()
        predresult = self.pattern.match(
            self.vardict,
            subdict,
            self.predicate_rule,
            expr
        )
        if predresult:
            return TrueThingNR(expr, subdict=subdict)
        else:
            return False

    def tbody(self, truething):
        subdict = truething.subdict
        out = Substitute(subdict=subdict, bottomup=True)(self.outcome)
        return self.outcome_rule(out)


class HalfNaturalRule(NaturalRuleBase):
    class VarNames:
        def __init__(self, subdict):
            for key in subdict:
                name = key.name
                exec('self.' + name + ' = subdict[key]')

    def tpredicate(self, expr):
        subdict = dict()
        predresult = self.pattern.match(
            self.vardict,
            subdict,
            self.predicate_rule,
            expr
        )
        if predresult:
            var = self.VarNames(subdict)
            return TrueThingHNR(expr, var=var)
        else:
            return False

    def tbody(self, truething):
        try:
            return self.body(
                truething.expr,
                truething.var,
            )
        except TypeError:
            ta_logger.log(
                'HalfNaturalRule body method requires three arguments'
            )
            return null

    def body(self, expr, var):
        return expr

# Is this something worth pursuing? Providing names for rules?
#   def __str__(self):
#       return "HalfNaturalRule " + self.name + " instance"
