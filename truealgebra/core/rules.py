from abc import ABC, abstractmethod


class TrueThing:
    """Boolean evaluation to True and carries information.

    TrueThing instance is the output of a rule's tpredicate method
    and the sole input into the tbody method of the same rule.

    Attributes
    ----------
    expr : ExprBase
        The input expression is the sole argument the rule's __call__ method.

    """
    def __init__(self, expr):
        self.expr = expr
    selected_truething = False

    def __bool__(self):
        return True


class TrueThingJO(TrueThing):
    """Used with JustOne instances.

    selected_truething : bool
        The class attribute is always False.
        Used as a reference by JustOne instances.
    """
    def __init__(self, expr, selected_truething=False, ndx=None):
        self.expr = expr
        self.selected_truething = selected_truething
        self.ndx = ndx


class RuleBase(ABC):
    bottomup = False
    path = ()

    def __init__(self, *args, **kwargs):
        if "bottomup" in kwargs:
            self.bottomup = kwargs["bottomup"]
        if "path" in kwargs:
            self.path = tuple(kwargs["path"])

    @abstractmethod
    def tpredicate(self, expr):
        pass

    @abstractmethod
    def tbody(self, truething):
        pass

    def __call__(self, expr, _pathinhibit=False, _buinhibit=False):
        """Primary means of executing a rule.

        When a expression apply2path method calls a rule
        only the _pathinhibit parameter must be set True.

        When a expression botttomup method calls a rule
        both the _pathinhibit and _buinhibit parameters must be set True.
        """
        if self.path and not _pathinhibit:
            return expr.apply2path(self.path, self)

        if self.bottomup and not _buinhibit:
            return expr.bottomup(self)

        tpredicate_out = self.tpredicate(expr)
        if tpredicate_out:
            return self.tbody(tpredicate_out)
        else:
            return expr


class Rule(RuleBase):
    def tpredicate(self, expr):
        if self.predicate(expr):
            return TrueThing(expr)
        else:
            return False

    def tbody(self, truething):
        return self.body(truething.expr)

    def predicate(self, expr):
        return False

    def body(self, expr):
        return expr


donothing_rule = Rule()


class Substitute(Rule):
    """substitute expressions from a dictionary.
    """
    def __init__(self, *args, **kwargs):
        """ Define substitute dictionary as attribute

        Attributes
        ----------
        subdict : dict
            Both keys and values are Truealgebra expressions.
        """
        if "subdict" in kwargs:
            self.subdict = kwargs["subdict"]
        else:
            self.subdict = dict()
        super().__init__(*args, **kwargs)

    def predicate(self, expr):
        """Is the input expression a key in the dictionary?
        """
        return expr in self.subdict

    def body(self, expr):
        """Replace input expression
        """
        return self.subdict[expr]


class Rules(RuleBase):
    def __init__(self, *rules, **kwargs):
        self.rule_list = list(rules)
        super().__init__(*rules, **kwargs)

    def tpredicate(self, expr):
        return TrueThing(expr)

    def tbody(self, truething):
        expr = truething.expr
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
    def __init__(self, *rules, **kwargs):
        self.rule_list = list(rules)
        super().__init__(*rules, **kwargs)

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


class JustOneBU(JustOne):
    bottomup = True
