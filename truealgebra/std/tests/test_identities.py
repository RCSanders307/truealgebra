from truealgebra.core.settings import SettingsSingleton
from truealgebra.common.commonsettings import commonsettings

from truealgebra.std.setup_func import std_setup_func
from truealgebra.common.setup_func import common_setup_func

#from truealgebra.std.identities import trig_ident0

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


@pytest.fixture
def identities(settings, scope='module'):
    from truealgebra.std import identities
    return identities


def test_trig_ident0(settings, identities):
#   xxx = 100; embed()
    ex0 = settings.parse(' sin(x)**2 + cos(x)**2 ')
    ex00 = settings.parse(' cos(x)**2 + sin(x)**2 ')
    ex1 = settings.parse(' 1 ')
    
    out0 = identities.trig_ident0(ex0)
    out00 = identities.trig_ident0(ex00)

    assert out0 == ex1
    assert out00 == ex1
