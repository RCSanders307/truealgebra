from truealgebra.core.abbrv import Sy, Nu, Co, Asn
from truealgebra.core.expression import CommAssoc, Assign, true, false
from truealgebra.core.frontend import FrontEnd, AssignRule, HistoryRule
from truealgebra.core.rulebase import RuleBase, placebo_rule
from truealgebra.core.rule import RulesBU, NaturalRule
from truealgebra.core.parse import Parse
from truealgebra.core.settings import SettingsSingleton
import pytest


@pytest.fixture
def settings(scope='module'):
    settings = SettingsSingleton()

    settings.set_custom_bp("=", 50, 50)
    settings.set_custom_bp("*", 1000, 1000)
    settings.set_infixprefix('-', 200)

    settings.set_container_subclass("*", CommAssoc)
    settings.set_container_subclass(":=", Assign)
    settings.set_complement('star', '*')

    settings.set_categories('suchthat', '|')
    settings.set_categories('suchthat', 'suchthat')
    settings.set_categories('forall', '@')
    settings.set_categories('forall', 'forall')

    yield settings
    settings.reset()


parse = Parse()


class IsInt(RuleBase):
    def predicate(self, expr):
        return (
            expr.name == 'isint'
            and isinstance(expr, Co)
            and len(expr) == 1
        )

    def body(self, expr):
        if isinstance(expr[0], Nu) and isinstance(expr[0].value, int):
            return true
        else:
            return false


isint = IsInt()


class Rule0(NaturalRule):
    parse = parse
    predicate_rule = isint
    var_defn = NaturalRule.create_var_dict(
        ' @x | isint(x); @y | isint(y); @z | isint(z) ', parse
    )


rule0 = Rule0(
    pattern=' star(x, y, z) ',
    outcome=' star(y, x, z) ',
)


# Test HistoryRule
# ================
def test_HistoeyRule_postinit():
    fe = FrontEnd()

    hr = HistoryRule(frontend=fe)

    assert hr.frontend == fe
    assert hr.bottomup is True  # Not really part of postinit method


@pytest.mark.parametrize(
    'expr, correct',
    [
        (Co('Ex', (Nu(3),)), True),
        (Co('Expr', (Nu(3),)), False),
        (Sy('y'), False),
        (Co('Expr', ()), False),
    ]
)
def test_HistoryRule_predicate(expr, correct):
    fe = FrontEnd(parse=parse)
    syms = [Sy('w'), Sy('x'), Sy('y'), Sy('z')]
    fe.history.extend(syms)
    hr = HistoryRule(frontend=fe)

    out = hr.predicate(expr)

    assert out == correct


def test_HistoryRule_body():
    fe = FrontEnd(parse=parse)
    hr = HistoryRule(frontend=fe)
    hr.frontend.history.append(Sy('x'))
    hr.frontend.history.append(Sy('y'))

    out0 = hr.body(Co('Ex', (Nu(0),)))
    out1 = hr.body(Co('Ex', (Co('-', (Nu(1),)),)))

    assert out0 == Sy('x')
    assert out1 == Sy('y')


def test_HistoryRule_body_error(capsys):
    fe = FrontEnd(parse=parse)
    hr = HistoryRule(frontend=fe)
    hr.frontend.history.append(Sy('x'))

    out = hr.body(Co('Ex', (Nu(3),)))
    err = capsys.readouterr()

    assert out == Co('Ex', (Nu(3),))
    assert 'exception with History_Rule instance' in err.out


# Test AssignRule
# ===============
def test_AssignRule_postinit():
    fe = FrontEnd()

    ar = AssignRule(frontend=fe)

    assert ar.frontend == fe
    assert ar.bottomup is True  # Not really part of postinit method
    assert ar.assign_dict == dict()
    assert ar.active is False


@pytest.mark.parametrize(
    'expr, correct',
    [
        (Sy('x'), True),
        (Sy('y'), False),
    ]
)
def test_AssignRule_predicate(expr, correct):
    fe = FrontEnd(parse=parse)
    ar = AssignRule(frontend=fe)
    ar.assign_dict[Sy('x')] = Nu(4)

    out = ar.predicate(expr)

    assert out == correct


def test_AssignRule_body():
    fe = FrontEnd(parse=parse)
    ar = AssignRule(frontend=fe)
    ar.assign_dict[Sy('x')] = Nu(4)

    out = ar.body(Sy('x'))

    assert out == Nu(4)


@pytest.mark.parametrize(
    'expr, a_dict',
    [
        (Asn(':=', (Sy('x'), Nu(4))), {Sy('x'): Nu(4)}),
        (Co('==', (Sy('x'), Nu(4))), dict()),
    ]
)
def test_AssignRule_assign(expr, a_dict):
    fe = FrontEnd(parse=parse)
    ar = AssignRule(frontend=fe)

    ar.assign(expr)

    assert ar.assign_dict == a_dict


def test_AssignRule_assign_error(capsys):
    fe = FrontEnd(parse=parse)
    ar = AssignRule(frontend=fe)
    expr = Asn(':=', (Sy('x'),))

    ar.assign(expr)
    err = capsys.readouterr()

    assert ar.assign_dict == dict()
    assert 'exception with AssignRule assign method' in err.out


def test_AssignRule_activate():
    fe = FrontEnd(parse=parse)
    ar = AssignRule(frontend=fe)
    fe.assign_rules.append(ar)

    ar.activate()

    assert ar.active is True
    assert fe.active_assign_rule == ar
    assert fe.assign_rules[0].active is False


# Test FrontEnd init
# ==================
def test_frontend_init_default():
    fe = FrontEnd()

    assert fe.history_name == 'Ex'
    assert fe.history_counter == 0
    assert fe.history == list()
    assert isinstance(fe.history_rule, HistoryRule)
    assert fe.history_rule.frontend is fe
    assert isinstance(fe.parse, Parse)
    assert isinstance(fe.assign_rules, list)
    assert isinstance(fe.assign_rules[0], AssignRule)
    assert fe.assign_rules[0].frontend == fe
    assert fe.assign_rules[0].active is True
    assert fe.active_assign_rule == fe.assign_rules[0]
    assert fe.default_rule == placebo_rule
    assert fe.mute is False
    assert fe.session_rules.rule_list == list()
    assert isinstance(fe.session_rules, RulesBU)
    assert issubclass(fe.SessionRule, NaturalRule)
    assert fe.SessionRule.parse is fe.parse
    assert fe.hold_assign is False
    assert fe.hold_default is False
    assert fe.hold_session is False
    assert fe.hold_all is False


@pytest.mark.parametrize(
    'attribute, argument,',
    [
        ('history_name', '"Expr"'),
        ('parse', 'parse'),
        ('default_rule', 'rule0'),
        ('hold_default', 'True'),
        ('hold_assign', 'True'),
        ('hold_session', 'True'),
        ('hold_all', 'True'),
        ('mute', 'True'),
    ]
)
def test_frontend_init(argument, attribute):
    exec('fe = FrontEnd(' + attribute + '=' + argument + ')')

    exec('assert fe.' + attribute + ' == ' + argument)


# Test FrontEnd make_assign_rule
# ==============================
def test_frontend_make_assign_rule():
    fe = FrontEnd(parse=parse)

    fe.make_assign_rule()

    assert isinstance(fe.assign_rules[1], AssignRule)


# Test FrontEnd print_expr
# ========================
def test_frontend_print_expr(capsys):
    fe = FrontEnd(parse=parse)
    expr = Co('=', (Co('+', (Nu(1), Nu(1))), Nu(2)))

    fe.print_expr(expr)
    err = capsys.readouterr()

    assert 'Ex(0):    =(+(1, 1), 2)' in err.out
    assert fe.history_counter == 1


# Test FrontEnd init hold Parameters
# ==================================
# In these tests:
#    assign_rule chages Symbol 'a' to 'aa'
#    session_rule chages Symbol 's' to 'ss'
#    default_rule changes Symbol 'd'  to 'dd'
#    Each test shows what rule(s) a hold parameter controls
class Default(RuleBase):
    """ RuleBase subclass used for tests."""
    bottomup = True

    def postinit(self, targetname, replacename):
        self.targetname = targetname
        self.replacename = replacename

    def predicate(self, expr):
        return isinstance(expr, Sy) and expr.name == self.targetname

    def body(self, expr):
        return Sy(self.replacename)


# rule changes Symbol('d') to Symbol('dd')
default0 = Default('d', 'dd')


def test_frontend_init_no_hold(settings):
    """ All hold attributes set False;
    the assign_rule, session_rule, and default_rule are all used.
    """
    fe = FrontEnd(parse=parse, default_rule=default0,)
    fe.create_session_rule(pattern='s', outcome='ss')
    fe(' a := aa ')
    string = ' f(a, s, d) '

    fe(string)

    assert fe.history[1] == parse('f(aa, ss, dd)')


def test_frontend_init_hold_assign():
    """instance attribute hold_assign set to True;
    the assign_rule is not used.
    """
    fe = FrontEnd(parse=parse, default_rule=default0, hold_assign=True)
    fe.create_session_rule(pattern='s', outcome='ss')
    fe(' a := aa ')
    string = ' f(a, s, d) '

    fe(string)

    assert fe.history[1] == parse('f(a, ss, dd)')


def test_frontend_init_hold_session(settings):
    """instance attribute hold_session set to True;
    the session_rule is not used.
    """
    fe = FrontEnd(parse=parse, default_rule=default0, hold_session=True)
    fe.create_session_rule(pattern='s', outcome='ss')
    fe(' a := aa ')
    string = ' f(a, s, d) '

    fe(string)

    assert fe.history[1] == parse('f(aa, s, dd)')


def test_frontend_init_hold_default(settings):
    """instance attribute hold_default set to True;
    the default_rule is not used.
    """
    fe = FrontEnd(parse=parse, default_rule=default0, hold_default=True)
    fe.create_session_rule(pattern='s', outcome='ss')
    fe(' a := aa ')
    string = ' f(a, s, d) '

    fe(string)

    assert fe.history[1] == parse('f(aa, ss, d)')


def test_frontend_init_hold_all(settings):
    """instance attribute hold_all set to True
    none of the rules are used.
    """
    fe = FrontEnd(parse=parse, default_rule=default0, hold_all=True)
    fe.create_session_rule(pattern='s', outcome='ss')
    fe(' a := aa ')
    string = ' f(a, s, d) '

    fe(string)

    assert fe.history[1] == parse('f(a, s, d)')


# Test FrontEnd call hold Parameters
# ==================================
# These tests are done in a similar manner as the previous four tests.
#  The difference is the hold parameters are for the __call__ method.
def test_frontend_call_hold_assign():
    """instance attribute hold_assign set to True;
    the assign_rule is not used.
    """
    fe = FrontEnd(parse=parse, default_rule=default0)
    fe.create_session_rule(pattern='s', outcome='ss')
    fe(' a := aa ')
    string = ' f(a, s, d) '

    fe(string, hold_assign=True)

    assert fe.history[1] == parse('f(a, ss, dd)')


def test_frontend_call_hold_session(settings):
    """instance attribute hold_session set to True;
    the session_rule is not used.
    """
    fe = FrontEnd(parse=parse, default_rule=default0)
    fe.create_session_rule(pattern='s', outcome='ss')
    fe(' a := aa ')
    string = ' f(a, s, d) '

    fe(string, hold_session=True)

    assert fe.history[1] == parse('f(aa, s, dd)')


def test_frontend_call_hold_default(settings):
    """instance attribute hold_default set to True;
    the default_rule is not used.
    """
    fe = FrontEnd(parse=parse, default_rule=default0)
    fe.create_session_rule(pattern='s', outcome='ss')
    fe(' a := aa ')
    string = ' f(a, s, d) '

    fe(string, hold_default=True)

    assert fe.history[1] == parse('f(aa, ss, d)')


def test_frontend_call_hold_all(settings):
    """instance attribute hold_all set to True
    none of the rules are used.
    """
    fe = FrontEnd(parse=parse, default_rule=default0)
    fe.create_session_rule(pattern='s', outcome='ss')
    fe(' a := aa ')
    string = ' f(a, s, d) '

    fe(string, hold_all=True)

    assert fe.history[1] == parse('f(a, s, d)')


# Test FrontEnd post_parser method Sequence of Statements.
apply0 = Default('d', 'e')
default1 = Default('b', 'c')


def test_frontend_post_parser_sequence(capsys, settings):
    """Test the sequence of statements in the post_parser method.

    The staements must be executed in a specific order.

    The assign_rule changes Symbol('a') to Symbol('b').
    The next rule changes the symbol to a Symbol('c').
    And so on until it becomes a Symbol('e').
    Then the assign rule is assigned, the history list appended and
    the final expression printed out.
    """
    fe = FrontEnd(parse=parse, default_rule=default1)
    fe.create_session_rule(pattern='c', outcome='d')

    fe(' a := b ')
    fe('a', hold_all=True)
    fe('x := Ex(1)', apply=apply0)
    err = capsys.readouterr()

    assert fe.history[2] == Asn(':=', (Sy('x'), Sy('e')))
    assert fe.assign_rules[0].assign_dict[Sy('x')] == Sy('e')
    assert 'Ex(2):    :=(x, e)' in err.out
