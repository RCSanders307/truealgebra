""" Test Parse factory methods"""

from truealgebra.core.parse import Parse
from truealgebra.core.expressions import (
    CommAssoc, Number, Container, Symbol, Restricted, Assign
)
import pytest


def test_integer_factory(conftest_settings):
    parse = Parse()
    parse.buf = '37'

    out = parse.integer_factory()

    assert out == Number(37)
    assert type(out.value) == int


# test real_factory - Done
def test_real_factory(conftest_settings):
    parse = Parse()
    parse.buf = '674.23'

    out = parse.real_factory()

    assert out == Number(674.23)
    assert type(out.value) == float


@pytest.mark.parametrize(
    'buf, inst',
    [
        (':=', Assign(':=')),
        ('star', CommAssoc('*')),
        ('and', Container('and')),
    ]
)
def test_make_conatiner_instance(buf, inst, conftest_settings):
    parse = Parse()
    parse.buf = buf

    out = parse.make_container_instance()

    assert out == inst


# test operator_factory method - Done
@pytest.mark.parametrize(
    'buf, token, lbp, rbp',
    [
        ('*', CommAssoc('*'), 1000, 999),
        ('^^', Container('^^'), 251, 252),
        ('!!', CommAssoc('+'), 251, 252),
    ]
)
def test_operator_factory(buf, token, lbp, rbp, conftest_settings):
    parse = Parse()
    parse.buf = buf

    out = parse.operator_factory()

    assert out == token
    assert out.lbp == lbp
    assert out.rbp == rbp


# test function_form_factory - Done
@pytest.mark.parametrize(
    'buf, token, rbp',
    [
        ('D', Container('D'), 481),
        ('star', CommAssoc('*'), 0),
        ('Rule', Restricted('Rule'), 0),
    ]
)
def test_function_form_factory(buf, token, rbp, conftest_settings):
    parse = Parse()
    parse.buf = buf

    out = parse.function_form_factory()

    assert out == token
    assert out.lbp == 0
    assert out.rbp == rbp


def test_symbol_operator_factory(conftest_settings):
    parse = Parse()
    parse.buf = 'and'

    out = parse.symbol_operator_factory()

    assert out == Container('and')
    assert out.lbp == 75
    assert out.rbp == 76


def test_symbol_factory(conftest_settings):
    parse = Parse()
    parse.buf = 'symbol'

    out = parse.symbol_factory()

    assert out == Symbol('symbol')
    assert out.lbp == 0
    assert out.rbp == 0
