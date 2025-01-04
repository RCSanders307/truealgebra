""" Test Parse tokenizer methods

Methods Tested
==============

    # init_tokenizer
    # symbol_tokenizer
    # sform_tokenizer
    # function_form tokenizer
    # real_tokenizer
    # oper_tokenizer
    # integer_tokenizer
    # parenthesis_tokenizer
"""

from truealgebra.core.parse import Parse
from truealgebra.core.expressions import (
    Number, Container, Symbol, null, end
)
import pytest


@pytest.fixture
def create_parse_tok(conftest_settings):
    """ Fixture Used in testing tokenizer methods

    This fixture creates a Parse instance with init_parse emulation.
    init_parse output is from a generator that uses delim_tup and token_tup.
    """

    class PyTestParse(Parse):
        def init_parse(self, delims):
            return next(self.gen)

        def make_generator(self, delim_tup, token_tup):
            def tmp_thing(delim_tuple, token_tuple):
                d_iter = iter(delim_tuple)
                t_iter = iter(token_tuple)

                while True:
                    self.char = next(d_iter)
                    yield next(t_iter)

            self.gen = tmp_thing(delim_tup, token_tup)

        gen = iter(())

    def create_parse(
        char='(',
        buf='abc',
        string='1+2',
        token_tup=(Number(5), Number(6), Number(8)),
        delim_tup=(',', ',', ')'),
    ):
        parse = PyTestParse()
        parse.buf = buf
        parse.char = char
        parse.string = string
        parse.string_iterator = iter(string)
        parse.make_generator(delim_tup, token_tup)
        return parse

    return create_parse


# Perform Tests

# Test init_tokenizer - Done
@pytest.mark.parametrize(
    'char, string, token',
    [
        (')', '3.4',  end),
        ('1', '34',  Number(134)),
        ('a', 'bc',  Symbol('abc')),
        ('.', '13',  Number(0.13)),
        ('*', '++', Container('*++', ())),
    ]
)
def test_init_tokenizer_0(char, string, token, create_parse_tok):
    parse = create_parse_tok(
        char=char,
        string=string,
    )

    out = parse.init_tokenizer(delims=')')

    assert out == token


def test_init_tokenizer_1(create_parse_tok):
    parse = create_parse_tok(
        char='(',
        buf='',
        string='4)',
        delim_tup=(')', 'end'),
        token_tup=(Number(4), end)
    )

    out = parse.init_tokenizer(delims=(')', 'end'))

    assert out == Number(4)


def test_init_tokenizer_error(create_parse_tok, capsys):
    parse = create_parse_tok(
        char='#',
        buf='',
        string='4)',
        delim_tup=(')', 'end'),
        token_tup=(Number(4), end)
    )
    msg = 'unrecognized character: #'

    out = parse.init_tokenizer(delims=(')', 'end'))
    output = capsys.readouterr()

    assert out == null
    assert msg in output.out


# Test integer_tokenizer - Done
@pytest.mark.parametrize(
    'char, string, token',
    [
        ('2', '3.4', Number(23.4)),
        ('2', '354', Number(2354)),
        ('2', 'e3', Number(2000.0)),
        ('2', 'E3', Number(2000.0)),
    ]
)
def test_integer_tokenizer(char, string, token, create_parse_tok):
    parse = create_parse_tok(
        char=char,
        buf='',
        string=string,
    )

    out = parse.integer_tokenizer()

    assert out == token


# Test real_tokenizer - Done
@pytest.mark.parametrize(
    'buf, char, string, token',
    [
        ('123', '.', '456', Number(123.456)),
        ('5', '.', '3E2', Number(530.0)),
    ]
)
def test_real_tokenizer(buf, char, string, token, create_parse_tok):
    parse = create_parse_tok(
        char=char,
        buf=buf,
        string=string,
    )

    out = parse.real_tokenizer()

    assert out == token


def test_real_tokenizer_error(create_parse_tok, capsys):
    parse = create_parse_tok(
        char='.',
        buf='',
        string=' * b',
    )
    msg = 'real number with "." requires a digit'

    out = parse.real_tokenizer()
    output = capsys.readouterr()

    assert out == null
    assert msg in output.out


# Test sform_tokezer - Done
@pytest.mark.parametrize(
    'char, buf, string, token',
    [
        ('e', '3', '10a',  Number(30000000000.0)),
        ('E', '2.0', '2',  Number(200.0)),
        ('E', '2.0', '+2',  Number(200.0)),
        ('E', '2.0', '-2',  Number(0.02)),
    ]
)
def test_sform_tokenizer(char, buf, string, token, create_parse_tok):
    parse = create_parse_tok(
        char=char,
        buf=buf,
        string=string,
    )

    out = parse.sform_tokenizer()

    assert out == token


def test_sform_tokenizer_error(capsys, create_parse_tok):
    parse = create_parse_tok(
        char='e',
        buf='2.3',
        string='abc'
    )
    msg = 'scientific notation requires a digit after the e or E'

    out = parse.sform_tokenizer()
    output = capsys.readouterr()

    assert out == null
    assert msg in output.out


# Test function_form_tokenizer - Done
@pytest.mark.parametrize(
    'delim_tup, string, token',
    [
        (
            (',', ',', ')'), '*2',
            Container('abc', (Number(5), Number(6), Number(8))),
        ),
        ((), ')*2', Container('abc', ()),),
        ((), '  \t)*2', Container('abc', ()),)
    ]
)
def test_function_form_tokenizer(delim_tup, string, token, create_parse_tok):
    parse = create_parse_tok(
        string=string,
        delim_tup=delim_tup
    )
    out = parse.function_form_tokenizer()

    assert out == token


def test_function_form_tokenizer_error(capsys, create_parse_tok):
    parse = create_parse_tok(
        string='+2',
        delim_tup=(',', 'end', ')'),
    )
    msg = 'Missing right parenthesis: )'

    out = parse.function_form_tokenizer()
    output = capsys.readouterr()

    assert out == null
    assert msg in output.out


# Test parenthesis_tokenizer - Done
def test_parenthesis_tokenizer(create_parse_tok):
    parse = create_parse_tok(
        buf='',
        string=' 1+2',
        delim_tup=(')', 'end'),
    )

    out = parse.parenthesis_tokenizer()

    assert out == Number(5)


def test_parenthesis_tokenizer_error(create_parse_tok, capsys):
    parse = create_parse_tok(
        buf='',
        string=' 1+2',
        delim_tup=('end',),
    )
    msg = 'Missing right parenthesis: )'

    out = parse.parenthesis_tokenizer()
    output = capsys.readouterr()

    assert out == null
    assert msg in output.out


# Test oper_tokenizer - Done
def test_oper_tokenizer(create_parse_tok):
    parse = create_parse_tok(
        char='*',
        buf='',
        string='**',
    )

    out = parse.oper_tokenizer()

    assert out == Container('***', ())


# Test symbol_tokenizer - Done
@pytest.mark.parametrize(
    'char, string, token',
    [
        ('a', 'nd true',  Container('and', ())),
        ('f', '(5,6,8)',  Container('f', (Number(5), Number(6), Number(8)))),
        ('s', 'ymbol',  Symbol('symbol')),
    ]
)
def test_symbol_tokenizer(char, string, token, create_parse_tok):
    parse = create_parse_tok(
        char=char,
        buf='',
        string=string,
    )

    out = parse.symbol_tokenizer()

    assert out == token
