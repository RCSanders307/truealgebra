from truealgebra.core.settings import SettingsSingleton
from truealgebra.common.commonsettings import commonsettings
from truealgebra.common.setup_func import common_setup_func
from truealgebra.tasympy.setup_func import tasympy_setup_func
from truealgebra.tasympy.tatosympy import tatosympy

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
    "string, correct",
    [
        ('star(x, z, 3, 4, y)', sympy.Mul(x, z, 12, y)),
        ('plus(x, z, 3, 4, y)', sympy.Add(7, x, z, y)),
        (' x ** 2 ', sympy.Pow(x, 2)),
        ('x/y', sympy.Mul(x, sympy.Pow(y,-1))),
        ('-x', sympy.Mul(-1, x)),
        ('x-y', sympy.Add(x, sympy.Mul(-1, y))),
        ('x', x),
        ('3567', sympy.core.numbers.Integer('3567')),
        ('cos(x)', sympy.cos(x)),
        ('undefined(x, y, z)', sympy.Function('undefined')(x, y, z)),
    ],
)
def test_tatosympy_integration(settings, string, correct):
    expr = settings.parse(string)

    output =tatosympy(expr)

    assert output == correct



