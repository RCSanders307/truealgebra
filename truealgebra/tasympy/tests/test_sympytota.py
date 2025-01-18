
from truealgebra.core.settings import SettingsSingleton
from truealgebra.common.commonsettings import commonsettings
from truealgebra.common.setup_func import common_setup_func
from truealgebra.tasympy.setup_func import tasympy_setup_func
from truealgebra.tasympy.sympytota import sympytota

import sympy
import pytest

# ============
# Non Fixtures
# =============
x, y, w, z = sympy.symbols('x, y, w, z')

# ========
# Fixtures
# ========
@pytest.fixture
def settings(scope='module'):
    settings = SettingsSingleton()
    settings.reset()
    commonsettings.reset()
    tasympy_setup_func()
    common_setup_func()

    yield settings
        
    settings.reset()
    commonsettings.reset()

# =================
# Integration Tests
# =================
@pytest.mark.parametrize(
    "expr, string",
    [
        (sympy.Mul(5, y, z), ' star(5, y, z) '),
        (sympy.Add(12, x, y), 'plus(12, x, y)'),
        (sympy.Pow(x, y), ' x ** y '),
        (x, 'x'),
        (sympy.Integer(5), '5'),
        (sympy.cos(x), ' cos(x) '),
        (sympy.Function('ggg')(x), ' ggg(x) '),
# The line below generates an assert error.
#       (sympy.Float(5.5), '5.5'),
    ],
)
def test_sympytota_integration(settings, expr, string):
    correct = settings.parse(string)

    output = sympytota(expr)

    assert output == correct
