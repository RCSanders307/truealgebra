from truealgebra.core.constants import (
    DIGITS, LETTERS, WHITE_SPACE, OPERATORS, META_DELIMITERS,
    isbindingpower, issymbolname, isoperatorname,
)


def test_digits():
    digits = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

    assert DIGITS == digits


def test_letters():
    letters = set([
        '_',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ])

    assert LETTERS == letters


def test_white_space():
    white_space = set([' ', '\t'])

    assert WHITE_SPACE == white_space


def test_operators():
    operators = set([
        ':',  '\\', '*', '+', '-', '"', '^', '&', '%', '@', '!', '~',
        '/', '?', '<', '>', '=', '`', '|'
    ])

    assert OPERATORS == operators


def test_meta_delimiters():
    meta_delimiters = set(["\n", ";"])

    assert META_DELIMITERS == meta_delimiters


def test_isbindingpower():
    assert isbindingpower(700)
    assert isbindingpower(0)
    assert not isbindingpower(-1)
    assert not isbindingpower(1.0)


def test_issymbolname():
    assert issymbolname('abc')
    assert issymbolname('ABC1')
    assert not issymbolname('2ABC1')
    assert not issymbolname('**')
    assert not issymbolname('AB C1')
    assert not issymbolname(786)


def test_isoperatorname():
    assert isoperatorname('*+')
    assert not isoperatorname('* +')
    assert not isoperatorname(456)
    assert not isoperatorname('asd')
