
class TrueThing:
    """Boolean evaluation to True. Carries information between methods.

    TrueThing instance is the output of a rule's predicate method 
    and the sole input into the body method of the same rule.

    Attributes
    ----------
    input_expression : ExprBase
        The input expression is the sole argument the rule's __call__ method.

    selected_truething : bool
        The class attribute is always False. Used as a reference by JustOne instances.
    """
    def __init__(self, input_expression):
        self.input_expression = input_expression
    selected_truething = False
    def __bool__(self):
        return True

class TrueThingJO(TrueThing):
    """Used with JustOne instances.
    """
    def __init__(self, input_expression, selected_truething=False, ndx=None):
        self.input_expression = input_expression
        self.selected_truething = selected_truething
        self.ndx = ndx

class TrueThingNR(TrueThing):
    """Used with NaturalRule instances.
    """
# revisit subdict
    def __init__(self, input_expression, subdict=None):
        self.input_expression = input_expression
        self.subdict = subdict

class TrueThingHNR(TrueThing):
    """Used with HalfNaturalRule instances.
    """
    def __init__(self, input_expression, var=None):
        self.input_expression = input_expression
        self.var = var

class RuleBase:
    bottomup = False
    path = ()

    def __init__(self, *args, **kwargs):
        if "bottomup" in kwargs:
            self.bottomup = kwargs["bottomup"]
        if "path" in kwargs:
            self.path = tuple(kwargs["path"])
        self.postinit(*args, **kwargs)

    def postinit(self, *args, **kwargs):
        pass

    def predicate(self, expr):
        return False

    def tpredicate(self, expr):
        predicate_out = self.predicate(expr)
        if predicate_out:
            return TrueThing(expr)
        else:
            return False

    def tbody(self, truething):
        return self.body(truething.input_expression)

    def body(self, expr):
        return expr

    def __call__(self, input_expression, _pathinhibit=False, _buinhibit=False):
        expr = input_expression
        if self.path and not _pathinhibit:
            return expr.apply2path(self.path, self , _buinhibit=_buinhibit)

        if self.bottomup and not _buinhibit:
            return expr.bottomup(self)

        tpredicate_out = self.tpredicate(expr)
        if tpredicate_out:
            return self.tbody(tpredicate_out)
        else:
            return expr

# Useful for a default rule that always does nothing.
placebo_rule = RuleBase()

class Substitute(RuleBase):
    """substitute expressions from a dictionary.
    """
    def postinit(self, *args, **kwargs):
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

    def predicate(self, expr):
        """Is the input expression a key in the dictionary?
        """
        return expr in self.subdict

    def body(self, expr):
        """Replace input expression
        """
        return self.subdict[expr]
