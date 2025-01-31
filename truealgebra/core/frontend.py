from truealgebra.core.rules import Rule, Rules, RulesBU, donothing_rule
from truealgebra.core.naturalrules import NaturalRule
from truealgebra.core.parse import meta_parser
from truealgebra.core.expressions import (
    Assign, Container, isContainer, MultiExprs
)
from truealgebra.core.err import ta_logger
from truealgebra.core.abbrv import isNu
from truealgebra.core.settings import settings

from IPython import embed


#class HistoryRule(Rule):
#    bottomup = True
#
#    def __init__(self, *args, **kwargs):
#        self.frontend = kwargs['frontend']
#
#        super().__init__(*args, **kwargs)
#
#    def predicate(self, expr):
#        return (
#            isinstance(expr, Container)
#            and expr.name == self.frontend.history_name
#            and len(expr) == 1
#            and isNu(expr[0])
## Perhaps the line is not required
##           and isinstance(expr[0].value, int)
#            and abs(expr[0].value) < len(self.frontend.history)
#        )
#
#    def body(self, expr):
#        try:
#            if  isinstance(expr[0], Container) and expr[0].name == '-':
#                num = - expr[0][0].value
#            else:
#                num = expr[0].value
#            return self.frontend.history[num]
#        except Exception:
#            ta_logger.log('exception with History_Rule instance')
#            return expr
#
#
#class AssignRule(Rule):
#    bottomup = True
#
#    def __init__(self, *args, **kwargs):
#        self.frontend = kwargs['frontend']
#        self.assign_dict = dict()
#        self.active = False
#
#        super().__init__(*args, **kwargs)
#
#    def predicate(self, expr):
#        return expr in self.assign_dict
#
#    def body(self, expr):
#        return self.assign_dict[expr]
#
#    def assign(self, expr):
#        if isinstance(expr, Assign):
#            try:
#                self.assign_dict[expr[0]] = expr[1]
#            except Exception:
#                ta_logger.log('exception with AssignRule assign method')
#
#    def activate(self):
#        for rule in self.frontend.assign_rules:
#            rule.active = False
#        self.active = True
#        self.frontend.active_assign_rule = self
#
#
#class FrontEnd():
#    def __init__(
#        self, history_name='Ex', default_rule=donothing_rule,
#        hold_default=False, hold_assign=False, hold_session=False,
#        hold_all=False, mute=False
#    ):
#        self.history_name = history_name
#        self.history_counter = 0
#        self.history = list()
#        self.history_rule = HistoryRule(frontend=self)
#
#        self.parse = settings.parse
#
##       if parse is None:
##           self.parse = Parse()
##       else:
##           self.parse = parse
#
#        self.assign_rules = [AssignRule(frontend=self),]
#        self.assign_rules[0].active = True
#        self.active_assign_rule = self.assign_rules[0]
#        self.default_rule = default_rule
#        self.mute = mute
#
#        self.session_rules = RulesBU()
#
#        class SessionRule(NaturalRule):
#            parse = self.parse
#
#        self.SessionRule = SessionRule
#        self.hold_assign = hold_assign  # If True, hold assign_rules.
#        self.hold_default = hold_default  # If True, hold default_rules.
#        self.hold_session = hold_session  # If True, hold session_rules.
#        self.hold_all = hold_all  # If True, hold all rules.
#
#    def create_session_rule(self, *args, **kwargs):
#        """ parse should NOT be a parameter
#        """
#        natural_rule = self.SessionRule(*args, **kwargs)
#        self.session_rules.rule_list.append(natural_rule)
#
#    def __call__(
#        self, txt, hold_assign=False, hold_default=False, hold_session=False,
#        hold_all=False, mute=False, apply=None
#    ):
#        mp = meta_parser(txt)
#        for ex in mp:
#            self.post_parser(
#                ex, hold_assign, hold_default, hold_session, hold_all,
#                mute, apply,
#            )
#
#    def post_parser(
#            self, expr, hold_assign, hold_default, hold_session, hold_all,
#            mute, apply,
#    ):
#        expr = self.history_rule(expr)
#
#        if (
#            not self.hold_assign
#            and not hold_assign
#            and not self.hold_all
#            and not hold_all
#        ):
#            expr = self.active_assign_rule(expr)
#
#        if (
#            not self.hold_default
#            and not hold_default
#            and not self.hold_all
#            and not hold_all
#        ):
#            expr = self.default_rule(expr)
#
#        if (
#            not self.hold_session
#            and not hold_session
#            and not self.hold_all
#            and not hold_all
#        ):
#            expr = self.session_rules(expr)
#
#        if apply is not None:
#            expr = apply(expr)
#
#        self.active_assign_rule.assign(expr)
#        self.history.append(expr)
#        if not self.mute and not mute:
#            self.print_expr(expr)
#
#    def print_expr(self, expr):
#        prefix = ("Ex(" + str(self.history_counter) + "):    ")
#        self.history_counter += 1
#        print(prefix + str(expr))
#
#    def make_assign_rule(self):
#        self.assign_rules.append(AssignRule(frontend=self))


############ New ########
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

    def apply_rule_to_multi(self):
        if isinstance(self.frontend.expr, MultiExprs):
            multilist = list()
            for expr in self.frontend.expr.exprs:
                multilist.append(self.rule(expr))
            self.frontend.expr = MultiExprs(multilist)
        else:
            self.frontend.expr = self.rule(self.frontend.expr)
         
         
# show action order
class FrontEnd:
    rules = tuple()

    def __init__(
        self, *Action_pairs, history_name='Ex', pred_rule=donothing_rule, **kwargs
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


#       ndex = -1 
#       if 'names' in kwargs:
#           names = kwargs['names']
#       else:
#           names = None
#       for i, Action in enumerate(Actions):
#           ndex =+ 1
#           action = Action(self, ndex)
#           self.actions.append(action)
#           if names is not None:
#               string = "self." + names[i] + ' = action'
#               exec(string)

    def __call__( self, txt, *rules):
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
        return (
            isinstance(expr, Container)
            and expr.name == self.frontend.history_name
            and len(expr) == 1
            and isNu(expr[0])
# Perhaps the line is not required
#           and isinstance(expr[0].value, int)
            and abs(expr[0].value) < len(self.frontend.history)
        )

    def body(self, expr):
        try:
            if  isinstance(expr[0], Container) and expr[0].name == '-':
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

# every entry into the frontend will be called an event

# StatementRuleAction    
class EventRuleAction(Action):
    def action(self):
        self.rule = Rules(*self.frontend.rules)
        self.apply_rule_to_multi()

# ##i######
class HistoryUpdateAction(Action):
    def action(self):
        self.frontend.history.append(self.frontend.expr)

class HistoryRuleAction(Action):
    def postinit(self):
        self.rule = HistoryRule(frontend=self.frontend)

    def action(self):
        self.apply_rule_to_multi()

# ##i######
class PrintAction(Action):
    def action(self):
        index_str = str(len(self.frontend.history) - 1)
        prefix = (self.frontend.history_name + "(" + index_str + "):    ")
        print(prefix + str(self.frontend.expr))
        #print(self.frontend.expr)

# ##i######
class RuleAction(Action):
    def postinit(self):
        self.rule = donothing_rule

    def action(self):
        self.apply_rule_to_multi()

## ##i######

class AssignRuleAction(Action):
    def postinit(self):
        self.rule = AssignRule(frontend=self.frontend)

    def action(self):
        self.apply_rule_to_multi()


class AssignUpdateAction(Action):
    def action(self):
        expr = self.frontend.expr
        if isinstance(expr, Assign):
            try:
                self.frontend.assigndict[expr[0]] = expr[1]
            except Exception:
                ta_logger.log('exception with AssignRule assign method')

##i######
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


