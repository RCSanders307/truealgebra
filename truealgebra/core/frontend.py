from truealgebra.core.rules import Rule, Rules, donothing_rule
from truealgebra.core.naturalrules import NaturalRule
from truealgebra.core.expressions import (
    Assign, Container, isContainer, MultiExprs
)
from truealgebra.core.err import ta_logger
from truealgebra.core.abbrv import isNu
from truealgebra.core.settings import settings


from abc import ABC, abstractmethod
from IPython import embed


class Action(ABC):
    def __init__(self, frontend, order):
        self.frontend = frontend
        self.order = order
        self.postinit()

    def postinit(self):
        pass

    _go = True
    _wait = False
    _pulse = False

    rule = donothing_rule

    def go(self):
        self._go = True

    def stop(self):
        self._go = False

    def wait(self):
        self._wait = True

    def pulse(self):
        self._pulse = True

    def control(self):
        if self._pulse:
            self.action()
            self._pulse = False
        elif self._wait:
            self._wait = False
        elif self._go:
            self.action()

    @abstractmethod
    def action(self):
        pass

    def expr_generator(self):
        if isinstance(self.frontend.expr, MultiExprs):
            for expr in self.frontend.expr.exprs:
                yield expr
        else:
            yield self.frontend.expr

    def apply_rule_to_multi(self):
        multilist = list()
        for expr in self.expr_generator():
            multilist.append(self.rule(expr))
        if len(multilist) == 1:
            self.frontend.expr = multilist[0]
        else:
            self.frontend.expr = MultiExprs(multilist)


# show action order
class FrontEnd:
    rules = tuple()

    def __init__(
        self, *Action_pairs, history_name='Ex', pred_rule=donothing_rule,
        **kwargs
    ):
        self.history = list()
        self.actions = list()
        self.history_name = history_name
        self.pred_rule = pred_rule
        self.assigndict = dict()
        self.naturalrules = list()

        ndex = -1
        for pair in Action_pairs:
            ndex =+ 1
            action = pair[0](self, ndex)
            object.__setattr__(self, pair[1], action)
            self.actions.append(action)

    def __call__(self, txt, *rules):
        self.rules = rules
        self.expr = settings.parse.multi(txt)
        for action in self.actions:
            action.control()


class HistoryRule(Rule):
    bottomup = True

    def __init__(self, *args, **kwargs):
        self.frontend = kwargs['frontend']

        super().__init__(*args, **kwargs)

    def predicate(self, expr):
        if (
            isinstance(expr, Container)
            and expr.name == self.frontend.history_name
            and len(expr) == 1
            and isNu(expr[0])
            and isinstance(expr[0].value, settings.integer_class)
        ):
            le = len(self.frontend.history)
            val = expr[0].value
            if (
                (val < 0 and val >= -le)
                or (val >= 0 and val < le)
            ):
                return True
        else:
            return False

    def body(self, expr):
        try:
            if isinstance(expr[0], Container) and expr[0].name == '-':
                num = - expr[0][0].value
            else:
                num = expr[0].value
            return self.frontend.history[num]
        except Exception:
            ta_logger.log('exception with History_Rule instance')
            return expr


class AssignRule(Rule):
    bottomup = True

    def __init__(self, *args, **kwargs):
        self.frontend = kwargs['frontend']
        self.assign_dict = dict()

        super().__init__(*args, **kwargs)

    def predicate(self, expr):
        return expr in self.frontend.assigndict

    def body(self, expr):
        return self.frontend.assigndict[expr]


# Evnt Rule Actions
class EventRuleAction(Action):
    def action(self):
        self.rule = Rules(*self.frontend.rules)
        self.apply_rule_to_multi()


# History Rule Actions
class HistoryUpdateAction(Action):
    def action(self):
        self.frontend.history.append(self.frontend.expr)


class HistoryRuleAction(Action):
    def postinit(self):
        self.rule = HistoryRule(frontend=self.frontend)

    def action(self):
        self.apply_rule_to_multi()


# Print Action
class PrintAction(Action):
    def action(self):
        index_str = str(len(self.frontend.history) - 1)
        prefix = (self.frontend.history_name + "(" + index_str + "):    ")
        if self._once_func is None:
            print(prefix + self._print_func(self.frontend.expr))
        else:
            print(prefix + self._once_func(self.frontend.expr))
            self._once_func = None
        #print(prefix + str(self.frontend.expr))

    _print_func = str
    _once_func = None

    def set_func(self, func):
        self._print_func = func

    def once_func(self, func):
        self._once_func = func


# Rule Action
class RuleAction(Action):
    def postinit(self):
        self.rule = donothing_rule

    def action(self):
        self.apply_rule_to_multi()


# Assign Rule  Actions
class AssignRuleAction(Action):
    def postinit(self):
        self.rule = AssignRule(frontend=self.frontend)

    def action(self):
        self.apply_rule_to_multi()


class AssignUpdateAction(Action):
    def action(self):
        for expr in self.expr_generator():
            if isinstance(expr, Assign):
                try:
                    self.frontend.assigndict[expr[0]] = expr[1]
                except Exception:
                    ta_logger.log('exception with AssignRule assign method')


# NaturalRule actions
class NaturalUpdateAction(Action):
    def action(self):
        if isContainer(self.frontend.expr, 'Rule', 3):
            rule = NaturalRule(
                predicate_rule=self.frontend.pred_rule,
                vardict=self.frontend.expr[0],
                pattern=self.frontend.expr[1],
                outcome=self.frontend.expr[2],
            )
            self.frontend.naturalrules.append(rule)


class NaturalRuleAction(Action):
    def action(self):
        self.rule = Rules(*self.frontend.naturalrules)
        self.apply_rule_to_multi()
