""" unit Tests for truealgebra.core.err"""

from truealgebra.core.err import TrueAlgebraError, ta_logger
import pytest

def fixture_function(name):
    if name != 'correct':
        ta_logger.log('Name error message')

complete_message = 'TRUEALGEBRA ERROR!\nName error message'


def test_errors_0():
    ta_logger.set_make_exception()

    with pytest.raises(TrueAlgebraError) as TAerror:
        fixture_function('incorrect')

    assert str(TAerror.value) == complete_message

    ta_logger.clear_make_exception()


def test_errors_1(capsys):
    fixture_function('incorrect')
    output = capsys.readouterr()

    assert output.out == complete_message + '\n'
