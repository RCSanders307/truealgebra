from truealgebra.core.rules import RuleBase, donothing_rule
from truealgebra.core.settings import settings
from truealgebra.core.parse import meta_parser
from truealgebra.core.expression import null
from truealgebra.core.err import ta_logger
import types

class NaturalRuleBase(RuleBase):
    predicate_rule = donothing_rule
    pattern = null
    outcome = null
    # as per:
    # https://adamj.eu/tech/2022/01/05/how-to-make-immutable-dict-in-python/
    # the default var_defn below is a immutable dictioary
    var_defn = types.MappingProxyType(dict()) 
    # var_defn is not changed after it is created
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

        if "var_defn" in kwargs:
            self.var_defn = kwargs['var_defn']
        try:
            if isinstance(self.var_defn, str):
                self.var_defn = self.create_var_dict(
                    self.var_defn, settings.active_parse
                )
        except TypeError:
            ta_logger.log(
                'settings.active_parse must point to a Parse instance'
            )

        super().__init__(*args, **kwargs)

    @classmethod
    def create_var_dict(cls, string):
        """Create a variable dictionary (var_defn), used for pattern matching

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
        parsed_string = meta_parser(string, settings.active_parse)
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
#   parse = None
    outcome_rule = donothing_rule

    def __init__(self, *args, **kwargs):

        # not used in HalfNaturalRUle
        if "outcome_rule" in kwargs:
            self.outcome_rule = kwargs["outcome_rule"]

        # Not used with HalfNaturalRule
        if 'outcome' in kwargs:
            self.outcome = kwargs['outcome']
        if isinstance(self.outcome, str):
            self.outcome = settings.active_parse(self.outcome)

        super().__init__(*args, **kwargs)

    def tpredicate(self, expr):
        subdict = dict()
        predresult = self.pattern.match(
            self.var_defn,
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
            self.var_defn,
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
