from truealgebra.core.settings import SettingsSingleton
from truealgebra.common.commonsettings import commonsettings
from truealgebra.common.setup_func import common_setup_func
from truealgebra.tasympy.setup_func import tasympy_setup_func
from truealgebra.tasympy.tatosympy import tatosympy
from truealgebra.tasympy.calculas import diff, integrate

import sympy
import pytest

from IPython import embed

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


# ======================
# Diff Integration Tests
# ======================
@pytest.mark.parametrize(
    "exprstring, correctstring",
    [
        (' D(x) c*x ', 'c'),
        (' D(x) x**2 ', ' 2 * x'),
        (
            ' D(x) star(cos(x), x**3) ',
            ' plus(star(-1, sin(x), x**3), star(3, cos(x), x**2)) '
        ),
    ],
)

def test_diff_integration(settings, exprstring, correctstring):
    expr = settings.parse(exprstring)
    correct = settings.parse(correctstring)

    output = diff(expr)
    assert output == correct


# ===========================
# Integrate Integration Tests
# ===========================
@pytest.mark.parametrize(
    "exprstring, correctstring",
    [
        (' I(x) x**3 ', ' star(1/4, x**4) '),
        (' I(x) plus(3, cos(x)) ', ' plus(3*x, sin(x)) '),
        (' I(x) star(sin(x), cos(x)) ', ' star(1/2, sin(x)**2) '),
    ],
)
def test_integrate_integration(settings, exprstring, correctstring):
    expr = settings.parse(exprstring)
    correct = settings.parse(correctstring)

    output = integrate(expr)
    assert output == correct
