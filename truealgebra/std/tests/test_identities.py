from truealgebra.core.settings import settings
from truealgebra.std.stdsettings_function import set_stdsettings
import pytest


@pytest.fixture
def idents(scope='module'):
    set_stdsettings()
    import truealgebra.std.identities as idents
    yield idents

    settings.reset()


@pytest.fixture
def parse(idents, scope='module'):
    return settings.active_parse



def test_trig_ident0(idents, parse):
    ex0 = parse(' sin(x)**2 + cos(x)**2 ')
    ex00 = parse(' cos(x)**2 + sin(x)**2 ')
    ex1 = parse(' 1 ')
    
    out0 = idents.trig_ident0(ex0)
    out00 = idents.trig_ident0(ex00)

    assert out0 == ex1
    assert out00 == ex1
