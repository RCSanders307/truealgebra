import logging

from truealgebra.core.rulebase import (
    TrueThingJO, TrueThingNR, TrueThingHNR, RuleBase, placebo_rule, Substitute
)
from truealgebra.core import expression as e
from truealgebra.core.expression import Container, null
from truealgebra.core.expression import Symbol
from truealgebra.core.parse import Parse, meta_parser
from truealgebra.core.err import ta_logger
from truealgebra.core.settings import SettingsSingleton
import types

logger = logging.getLogger('rules logger')
logger.setLevel(logging.ERROR)
# logger.setLevel(logging.DEBUG)

settings = SettingsSingleton()

class Rules(RuleBase):
    def postinit(self, *rules, **kwargs):
        self.rule_list = list(rules)

    def predicate(self, expr):
        return True

    def body(self, expr):
        for rule in self.rule_list:
            expr = rule(expr)
        return expr


class RulesBU(Rules):
    bottomup = True


class JustOne(RuleBase):
    """Apply at most, just one rule in a list of rules.

    Attributes
    ----------
    rulelist : list
        a list of rules which are the *args arguments of self.__init__.
    """
    def postinit(self, *args, **kwargs):
        self.rule_list = list(args)

    def tpredicate(self, expr):
        """ Select a rule that gets applied to the input expression.

        The selected rule in the list self.rules is the first rule found whose
        tpredicate method returns a TrueThing instance.

        parameters
        ----------
        expr : ExprBase
            This is the rule input expression.

        result
        ------
        truething : TrueThingJO
            The selected_truething attribute will be the TrueThing
            instance of the selected rule. The ndx attribute will be the
            self.rule_list index where the selected rule is found.

            The TrueThingJO instance will nest other TrueThing instance to
            mirror the structure of nested JustOne selected rules.

        False : bool
            Indicates there is no selected rule in self.rules.
        """
        for ndx, rule in enumerate(self.rule_list):
            truething = rule.tpredicate(expr)
            if truething:
                return TrueThingJO(expr, selected_truething=truething, ndx=ndx)
        return False

    def tbody(self, truething):
        return self.eval_selected(self, truething)

    def eval_selected(self, rule, truething):
        """recursive method finds and evelauates selected rule.

        parameters
        ----------
        rule : RuleBase
            nested layer of JustOne intance

        truesomething : TrueSomething
            nested layer of JustOne intance

        result
        ------
        expression : ExprBase
            From selected rule
        """
        if truething.selected_truething:
            ndx = truething.ndx
            rule = rule.rule_list[ndx]
            return self.eval_selected(rule, truething.selected_truething)
        else:
            return rule.tbody(truething)

    def predicate(self, expr):
        pass

    def body(self, expr):
        pass


class JustOneBU(JustOne):
    bottomup = True


class NaturalRule(RuleBase):
    parse = None
    predicate_rule = placebo_rule
    outcome_rule = placebo_rule
    pattern = e.null
    outcome = e.null
    # as per:
    # https://adamj.eu/tech/2022/01/05/how-to-make-immutable-dict-in-python/
    # the default var_defn below is a immutable dictioary
    var_defn = types.MappingProxyType(dict())  # var_defn is not changed after it is created

    def postinit(self, *args, **kwargs):
        if 'parse' in kwargs:
            self.parse = kwargs['parse']
        elif self.parse is None:
            self.parse = Parse()

        if "predicate_rule" in kwargs:
            self.predicate_rule = kwargs["predicate_rule"]

        # not used in HalfNaturalRUle
        if "outcome_rule" in kwargs:
            self.outcome_rule = kwargs["outcome_rule"]

        if 'pattern' in kwargs:
            self.pattern = kwargs['pattern']
        if isinstance(self.pattern, str):
            self.pattern = self.parse(self.pattern)

        if "var_defn" in kwargs:
            self.var_defn = kwargs['var_defn']
        if isinstance(self.var_defn, str):
            self.var_defn = self.create_var_dict(self.var_defn, self.parse)

        # Not used with HalfNaturalRule
        if 'outcome' in kwargs:
            self.outcome = kwargs['outcome']
        if isinstance(self.outcome, str):
            self.outcome = self.parse(self.outcome)

    @classmethod
    def create_var_dict(cls, string, parse):
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
        parsed_string = meta_parser(string, parse)
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


class HalfNaturalRule(NaturalRule):
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

# This should probably be trashed.
#class ContainerConvert(RuleBase):
#    def postinit(self, *args, **kwargs):
#        try:
#            self.old_name = kwargs["old_name"]
#            self.new_name = kwargs["new_name"]
#            self.old_etype = kwargs["old_etype"]
#            self.new_class = kwargs["new_class"]
#            if "identity" in kwargs:
#                self.identity = kwargs["identity"]
#            else:
#                self.identity = None
#        except AttributeError:
#            logger.exception(" attributes must be set")
#        # add exception
#
#    def predicate(self, expr):
#        return expr.etype == self.old_etype and expr.name == self.old_name
#
#    def body(self, expr):
#        if self.identity and len(expr.items) == 0:
#            return self.identity
#        elif self.dentity and len(expr.items) == 1:
#            return expr.items[0]
#        else:
#            return self.new_class(name=self.new_name, items=expr.items)
