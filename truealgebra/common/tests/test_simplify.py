from truealgebra.core.settings import SettingsSingleton
from truealgebra.common.commonsettings import commonsettings
from truealgebra.std.setup_func import std_setup_func
from truealgebra.common.setup_func import common_setup_func

from truealgebra.common.simplify import simplify
import pytest
from IPython import embed


@pytest.fixture
def settings(scope='module'):
    settings = SettingsSingleton()
    settings.reset()
    commonsettings.reset()
    std_setup_func()
    common_setup_func()

    yield settings
        
    settings.reset()
    commonsettings.reset()


#These is are integration tests 
@pytest.mark.parametrize(
    "expr, correct",
    [
        ('star(x, 2 * x, y/x, x**2, y**3)', 'star(2, x**3, y**4)'),
        ('star(x, 5, plus( -y, y))', '0'),
        ('star(x/x, y)', 'y'),
        ('star(x/x, y/y)', '1'),
        ('plus(x, -x, y, z, -z)', 'y'),
        ('plus(x, -x, y, -1 * y)', '0'),
        ('x * y/x**2 * (x/2 + x/2)/y', '1'),
        (' (x * y)/(y * x**(-2)) ', ' x**3 '),
        ('star(2, 4, 1/3, 3 ** 2)', '24'),
        ('plus(2, 4, 1/3, 2/3)', '7'),
        ('plus(x, y-x, y, z, -z)', '2*y'),
        ('plus(x, y-x, y, z, - - -z)', '2*y'),
        ('- 5', '-5'),
        ('7-3', '4'),
    ],
    ids=[
        "star function",
        "star with plus function",
        "star with num1 coef",
        "star with two num1",
        "plus with two num0 and y",
        "plus with two num0",
        "star with x's and y's",
        "star with more x's and y's",
        "star with integer math",
        "plus with integer math",
        "plus with '-' operators",
        "plus with more '-' operators",
        "neagative number",
        "subtract number",
    ]
)
def test_integration_simplify(settings, expr, correct):
    output = simplify(settings.parse(expr))
    correct_expr  = settings.parse(correct)

    assert output == correct_expr


#This is an integration test 
def test_real_number_simlify(settings):
    expr = 'star(7.0, 3.5 - 5.7, - 2.1, 1.5 ** 2.1, 4.7 / 3.6, 1.2 + 3.5)'
    output = simplify(settings.parse(expr))
    correct = 464.96993758661546
#   xxx = 105; embed()

    assert output.value == pytest.approx(correct)
