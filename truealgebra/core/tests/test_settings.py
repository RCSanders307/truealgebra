from collections import defaultdict
from truealgebra.core.expression import CommAssoc, Assign, Number
from truealgebra.core.settings import SettingsSingleton, bp
import pytest


@pytest.fixture
def settings():
    settings = SettingsSingleton()
    yield settings
    settings.reset()


def test_bp():
    pair = bp(175, 228)

    assert pair.lbp == 175
    assert pair.rbp == 228


def test_settings_init(settings):
    correct_nc = defaultdict(set)
    correct_nc['suchthat']
    correct_nc['forall']

    assert settings.default_bp == bp(250, 250)
    assert settings.custom_bp == dict()
    assert settings.infixprefix == dict()
    assert settings.symbol_operators == dict()
    assert settings.bodied_functions == dict()
    assert settings.sqrtneg1 == ''
    assert settings.container_subclass == dict()
    assert settings.complement == dict()
    assert settings.categories == correct_nc


@pytest.mark.parametrize(
    "lbp, rbp, assignment",
    [
        (300, 400, bp(300, 400)),
        (100, 0, bp(100, 0)),
        (0, 1000, bp(0, 1000)),
    ]
)
def test_set_default_bp(lbp, rbp, assignment, settings):
    settings.set_default_bp(lbp, rbp)

    assert settings.default_bp == assignment


@pytest.mark.parametrize(
    "lbp, rbp, msg",
    [
        (0, 0, 'set_default_bp error\n    lbp and rbp cannot both be 0'),
        (-3, 400, 'set_default_bp error\n    lbp -3 must be a binding power'),
        (
            300, -400,
            'set_default_bp error\n    rbp -400 must be a binding power'
        ),
        (300, 'a', 'set_default_bp error\n    rbp a must be a binding power'),
        ('b', 400, 'set_default_bp error\n    lbp b must be a binding power'),
    ]

)
def test_set_default_bp_error(lbp, rbp, msg, capsys, settings):
    settings.set_default_bp(lbp, rbp)
    output = capsys.readouterr()

    assert msg in output.out
    assert settings.default_bp == bp(250, 250)


@pytest.mark.parametrize(
    "name, lbp, rbp, assignment",
    [
        ('*', 200, 300, {'*': bp(200, 300)}),
        ('+', 0, 300, {'+': bp(0, 300)}),
        ('!', 200, 0, {'!': bp(200, 0)}),
    ]
)
def test_set_custom_bp(name, lbp, rbp, assignment, settings):
    settings.set_custom_bp(name, lbp, rbp)

    assert settings.custom_bp == assignment


@pytest.mark.parametrize(
    "name, lbp, rbp, msg",
    [
        (
            7, 200, 300,
            'set_custom_bp error\n    name 7 must be an operator name.'
        ),
        (
            'abc', 200, 300,
            'set_custom_bp error\n    name abc must be an operator name.'
        ),
        (
            '++', -2, 300,
            'set_custom_bp error\n    lbp -2 must be a binding power'
        ),
        (
            '***', 'a', 300,
            'set_custom_bp error\n    lbp a must be a binding power'
        ),
        (
            '*++', 200, 'b',
            'set_custom_bp error\n    rbp b must be a binding power'
        ),
        (
            '^', 99, -100,
            'set_custom_bp error\n    rbp -100 must be a binding power'
        ),
        (
            '!!', 0, 0,
            'set_custom_bp error\n    lbp and rbp cannot both be 0'
        ),
    ]
)
def test_set_custom_bp_error(name, lbp, rbp, msg, capsys, settings):
    settings.set_custom_bp(name, lbp, rbp)
    output = capsys.readouterr()

    assert msg in output.out
    assert settings.custom_bp == dict()


@pytest.mark.parametrize(
    "name, rbp, assignment, extra",
    [
        ('-', 470, {'-': 470}, ''),
        (
            '--', 470, {'--': 470},
            'settings.custom_bp["--"] = bp(400, 401)'
        ),
    ]
)
def test_set_infixprefix(name, rbp, assignment, extra, settings):
    if extra:
        exec(extra)
    settings.set_infixprefix(name, rbp)

    assert settings.infixprefix == assignment


@pytest.mark.parametrize(
    "name, rbp, extra, msg",
    [
        (
            '+', 0, '',
            'set_infixprefix error\n    '
            'rbp 0 must be a binding power greater than 0',
        ),
        (
            '*', 500, 'settings.custom_bp["*"] = bp(20, 0)',
            'right binding power of * infix form cannot be 0',
        ),
        (
            '**', 500, 'settings.custom_bp["**"] = bp(0, 20)',
            'left binding power of ** infix form cannot be 0',
        ),
    ]
)
def test_set_infixprefix_error(name, rbp, extra, msg, capsys, settings):
    if extra:
        exec(extra)
    settings.set_infixprefix(name, rbp)
    output = capsys.readouterr()

    assert msg in output.out
    assert settings.infixprefix == dict()


def test_set_symbol_operators_0(settings):
    settings.default_bp = bp(101, 102)
    settings.set_symbol_operators('a')

    assert settings.symbol_operators == {'a': bp(101, 102)}


def test_set_symbol_operators_1(settings):
    settings.set_symbol_operators('b', 375, 485)

    assert settings.symbol_operators == {'b': bp(375, 485)}


@pytest.mark.parametrize(
    "name, lbp, rbp, extra, msg",
    [
        (
            '+', 370, 480, '',
            'set_symbol_operator error\n    '
            'name + must be a symbol name.'
        ),
        (
            'c', 365, 475, 'settings.bodied_functions["c"] = 190',
            'name c cannot be key in bodied_functions'
        ),
        (
            'd', -365, 475, '',
            'lbp -365 must be a binding power'
        ),
        (
            'e', 365, -475, '',
            'rbp -475 must be a binding power'
        ),
        (
            'f', 'ss', 475, '',
            'lbp ss must be a binding power'
        ),
        (
            'g', 475, 'ss', '',
            'rbp ss must be a binding power'
        ),
        (
            'h', 0, 0, '',
            'lbp and rbp cannot both be 0'
        ),
    ]
)
def test_set_symbol_operators_errors(
    name, lbp, rbp, extra, msg, capsys, settings
 ):
    if extra:
        exec(extra)
    settings.set_symbol_operators(name, lbp, rbp)
    output = capsys.readouterr()

    assert msg in output.out
    assert settings.symbol_operators == dict()


def test_set_bodied_functions_0(settings):
    settings.default_bp = bp(101, 102)
    settings.set_bodied_functions('a')

    assert settings.bodied_functions == {'a': 102}


def test_set_bodied_functions_1(settings):
    settings.set_bodied_functions('b', 47)

    assert settings.bodied_functions == {'b': 47}


@pytest.mark.parametrize(
    "name, rbp, extra, msg",
    [
        (
            '+', 47, '',
            'set_bodied_functions error\n    '
            'name + must be a symbol name.'
        ),
        (
            'c', 370, 'settings.symbol_operators["c"] = bp(200, 209)',
            'name c cannot be key in symbol_operators',
        ),
        (
            'd', 'aa', '',
            'rbp aa must be a positive binding power',
        ),
        (
            'e', '-5', '',
            'rbp -5 must be a positive binding power',
        ),
        (
            'f', '0', '',
            'rbp 0 must be a positive binding power',
        ),
    ]
)
def test_set_bodied_functionss_errors(
    name, rbp, extra, msg, capsys, settings
):
    if extra:
        exec(extra)
    settings.set_bodied_functions(name, rbp)
    output = capsys.readouterr()

    assert msg in output.out
    assert settings.bodied_functions == dict()


@pytest.mark.parametrize("a_string", ['i', 'j', ''])
def test_set_sqrtneg1(a_string, settings):
    settings.set_sqrtneg1(a_string)
    assert settings.sqrtneg1 == a_string


def test_set_sqrtneg1_error(capsys, settings):
    settings.set_sqrtneg1('m')
    output = capsys.readouterr()

    assert 'a_string m cannot be used for square root of -1' in output.out
    assert settings.sqrtneg1 == ''


@pytest.mark.parametrize(
    "name, cls",
    [
        ('abc', Assign),
        ('**', CommAssoc),
    ]
)
def test_set_container_subclass(name, cls, settings):
    settings.set_container_subclass(name, cls)

    assert settings.container_subclass == {name: cls}


@pytest.mark.parametrize(
    "name, cls, msg",
    [
        (
            '1', CommAssoc,
            'set_container_subclass error\n    '
            'name 1 must b a symbol or operator name',
        ),
        (
            '***', Number,
            'cls ' + str(Number) + ' is not a Container subclass',
        ),
    ]
)
def test_set_container_subclass_error(name, cls, msg, capsys, settings):
    settings.set_container_subclass(name, cls)
    output = capsys.readouterr()

    assert msg in output.out
    assert settings.container_subclass == dict()


@pytest.mark.parametrize(
    "complementname, targetname",
    [
        ('abc', 'def',),
        ('**', '^^'),
    ]
)
def test_set_complement(complementname, targetname, settings):
    settings.set_complement(complementname, targetname)

    assert settings.complement == {complementname: targetname}


@pytest.mark.parametrize(
    "complementname, targetname, msg",
    [
        (
            'abc', 5,
            'set_complement error\n    '
            'targetname 5 must be a symbol or operator name',
        ),
        ('*b', '^^', 'complementname *b must be a symbol or operator name',),
    ]
)
def test_set_complement_error(
    complementname, targetname, msg, capsys, settings
):
    settings.set_complement(complementname, targetname)
    output = capsys.readouterr()

    assert msg in output.out
    assert settings.complement == dict()


@pytest.mark.parametrize(
    'category, name, catdict',
    [
        ('forall', '^^', {'forall': {'^^'}, 'suchthat': set()}),
        (
            'abc1%', 'abc',
            {'forall': set(), 'suchthat': set(), 'abc1%': {'abc'}}
        ),
        ('abc1%', '', {'forall': set(), 'suchthat': set(), 'abc1%': set()}),
    ]
)
def test_set_category(category, name, catdict, settings):
    if name:
        settings.set_categories(category, name)
    else:
        settings.set_categories(category)

    assert settings.categories == catdict


@pytest.mark.parametrize(
    'category, name, msg',
    [
        (
            5, 'abc',
            'set_categories error\n    '
            'category 5 must be a string instance'
        ),
        ('abc', '##', 'name ## must be an operator name or symbol name'),
    ]
)
def test_set_category_error(category, name, msg, capsys, settings):
    cat_dict = defaultdict(set)
    cat_dict['forall']
    cat_dict['suchthat']

    settings.set_categories(category, name)
    output = capsys.readouterr()

    assert msg in output.out
    assert settings.categories == cat_dict
