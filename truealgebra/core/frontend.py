from truealgebra.core.rules import Rule, RulesBU, donothing_rule
from truealgebra.core.naturalrules import NaturalRule
from truealgebra.core.parse import Parse, meta_parser
from truealgebra.core.expression import Assign, Container
from truealgebra.core.err import ta_logger
from truealgebra.core.abbrv import isNu


class HistoryRule(Rule):
    bottomup = True

    def __init__(self, *args, **kwargs):
        self.frontend = kwargs['frontend']

        super().__init__(*args, **kwargs)

    def predicate(self, expr):
        return (
            expr.name == self.frontend.history_name
            and isinstance(expr, Container)
            and len(expr) == 1
            and isNu(expr[0])
            and isinstance(expr[0].value, int)
            and abs(expr[0].value) < len(self.frontend.history)
        )

    def body(self, expr):
        try:
            if expr[0].name == '-' and isinstance(expr[0], Container):
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
        self.active = False

        super().__init__(*args, **kwargs)

    def predicate(self, expr):
        return expr in self.assign_dict

    def body(self, expr):
        return self.assign_dict[expr]

    def assign(self, expr):
        if isinstance(expr, Assign):
            try:
                self.assign_dict[expr[0]] = expr[1]
            except Exception:
                ta_logger.log('exception with AssignRule assign method')

    def activate(self):
        for rule in self.frontend.assign_rules:
            rule.active = False
        self.active = True
        self.frontend.active_assign_rule = self


class FrontEnd():
    def __init__(
        self, history_name='Ex', parse=None, default_rule=donothing_rule,
        hold_default=False, hold_assign=False, hold_session=False,
        hold_all=False, mute=False
    ):
        self.history_name = history_name
        self.history_counter = 0
        self.history = list()
        self.history_rule = HistoryRule(frontend=self)

        if parse is None:
            self.parse = Parse()
        else:
            self.parse = parse

        self.assign_rules = [AssignRule(frontend=self),]
        self.assign_rules[0].active = True
        self.active_assign_rule = self.assign_rules[0]
        self.default_rule = default_rule
        self.mute = mute

        self.session_rules = RulesBU()

        class SessionRule(NaturalRule):
            parse = self.parse

        self.SessionRule = SessionRule
        self.hold_assign = hold_assign  # If True, hold assign_rules.
        self.hold_default = hold_default  # If True, hold default_rules.
        self.hold_session = hold_session  # If True, hold session_rules.
        self.hold_all = hold_all  # If True, hold all rules.

    def create_session_rule(self, *args, **kwargs):
        """ parse should NOT be a parameter
        """
        natural_rule = self.SessionRule(*args, **kwargs)
        self.session_rules.rule_list.append(natural_rule)

    def __call__(
        self, txt, hold_assign=False, hold_default=False, hold_session=False,
        hold_all=False, mute=False, apply=None
    ):
        mp = meta_parser(txt)
        for ex in mp:
            self.post_parser(
                ex, hold_assign, hold_default, hold_session, hold_all,
                mute, apply,
            )

    def post_parser(
            self, expr, hold_assign, hold_default, hold_session, hold_all,
            mute, apply,
    ):
        expr = self.history_rule(expr)

        if (
            not self.hold_assign
            and not hold_assign
            and not self.hold_all
            and not hold_all
        ):
            expr = self.active_assign_rule(expr)

        if (
            not self.hold_default
            and not hold_default
            and not self.hold_all
            and not hold_all
        ):
            expr = self.default_rule(expr)

        if (
            not self.hold_session
            and not hold_session
            and not self.hold_all
            and not hold_all
        ):
            expr = self.session_rules(expr)

        if apply is not None:
            expr = apply(expr)

        self.active_assign_rule.assign(expr)
        self.history.append(expr)
        if not self.mute and not mute:
            self.print_expr(expr)

    def print_expr(self, expr):
        prefix = ("Ex(" + str(self.history_counter) + "):    ")
        self.history_counter += 1
        print(prefix + str(expr))

    def make_assign_rule(self):
        self.assign_rules.append(AssignRule(frontend=self))
