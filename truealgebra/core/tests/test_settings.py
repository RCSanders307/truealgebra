from collections import defaultdict
from truealgebra.core.expressions import CommAssoc, Assign, Number
from truealgebra.core.settings import SettingsSingleton, bp, noparse
import pytest


@pytest.fixture
def settings():
    settings = SettingsSingleton()
#   settings.reset()
    yield settings
    settings.reset()


def test_bp():
    pair = bp(175, 228)

    assert pair.lbp == 175
    assert pair.rbp == 228


def test_settings_init(settings):
    correct_nc = defaultdict(set)
    correct_nc['suchthat'].add('suchthat')
    correct_nc['forall'].add('forall')

    assert settings.default_bp == bp(250, 250)
    assert settings.custom_bp == dict()
    assert settings.infixprefix == dict()
    assert settings.symbol_operators == dict()
    assert settings.bodied_functions == dict()
    assert settings.container_subclass == dict()
    assert settings.complement == dict()
    assert settings.categories == correct_nc
    assert settings.parse == noparse
    assert settings.unparse == None


