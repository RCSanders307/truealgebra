from truealgebra.core.rules import (
    RuleBase, donothing_rule, TrueThing, Substitute
)
from truealgebra.core.settings import settings
from truealgebra.core.parse import meta_parser
from truealgebra.core.expression import null, Symbol
from truealgebra.core.err import ta_logger
import types

class TrueThingNR(TrueThing):
    """Used with NaturalRule instances.
    """
# revisit subdict
    def __init__(self, expr, subdict=None):
        self.expr = expr
        self.subdict = subdict

class NaturalRuleBase(RuleBase):
    predicate_rule = donothing_rule
    pattern = null
    outcome = null
    # as per:
    # https://adamj.eu/tech/2022/01/05/how-to-make-immutable-dict-in-python/
    # the default var_dict below is a immutable dictioary
    var_dict = types.MappingProxyType(dict()) 
    var_string = ''
    # var_dict is not changed after it is created
    def __init__(self, *args, **kwargs):
        if "predicate_rule" in kwargs:
            self.predicate_rule = kwargs["predicate_rule"]

        if 'pattern' in kwargs:
            self.pattern = kwargs['pattern']
        try:
            if isinstance(self.pattern, str):
                self.pattern = settings.active_parse(self.pattern)
        except TypeError:
            ta_logger.log(
                'settings.active_parse must point to a Parse instance'
            )

        self.convert_class_var()

        if "var_string" in kwargs:
            self.var_dict = self.create_var_dict(kwargs['var_string'])

        super().__init__(*args, **kwargs)

    @classmethod
    def convert_class_var(cls):
        if cls.var_string:
            cls.var_dict = cls.create_var_dict(cls.var_string)
            cls.var_string = ''

    @classmethod
    def create_var_dict(cls, string):
        """Create a variable dictionary used for pattern matching

        string : str instance is parsed into truealgebra expressions
            containing forall and suchthat expressions.

        Output
        ------
        var_dict : dict
            The keys are Symbol instances called variables. 
            A variable was the argument of a forall expression.
            The values are the second arguments of suchthat expressions.
            a variable not in a suchthat expression has null for a value.
        """
        try:
            parsed_string = meta_parser(string, settings.active_parse)
        except TypeError:
            ta_logger.log(
                'settings.active_parse must point to a Parse instance'
            )
        var_dict = dict()
        for ex in parsed_string:
            try:
                if ex.name in settings.categories['forall']:
                    for item in ex.items:
                        if isinstance(item, Symbol):
                            var_dict[item] = null
                elif ex.name in settings.categories['suchthat']:
                    if (
                        ex[0].name in settings.categories['forall']
                        and isinstance(ex[0][0], Symbol)
                    ):
                        var_dict[ex[0][0]] = ex[1]
            except IndexError:
                ta_logger.log(
                    'Index Error in forall or suchthat container expression'
                )
        return var_dict


class NaturalRule(NaturalRuleBase):
    outcome_rule = donothing_rule

    def __init__(self, *args, **kwargs):

        if "outcome_rule" in kwargs:
            self.outcome_rule = kwargs["outcome_rule"]

        if 'outcome' in kwargs:
            self.outcome = kwargs['outcome']
        if isinstance(self.outcome, str):
            self.outcome = settings.active_parse(self.outcome)

        super().__init__(*args, **kwargs)

    def tpredicate(self, expr):
        subdict = dict()
        predresult = self.pattern.match(
            self.var_dict,
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

    def __str__(self):
        return "HalfNaturalRule " + self.name + " instance"

    def tpredicate(self, expr):
        subdict = dict()
        predresult = self.pattern.match(
            self.var_dict,
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
                truething.input_expression,
                truething.var,
            )
        except TypeError:
            ta_logger.log(
                "HalfNaturalRule body method requires three arguments"
            )
            return e.null

    def body(self, expr, var):
        return expr
