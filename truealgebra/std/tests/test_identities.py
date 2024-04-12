#from truealgebra.std.identities import(
#    trig_ident0,
#)
from truealgebra.std.std_settings import set_stdsettings
from truealgebra.core.parse import Parse
import pytest

parse = Parse()

@pytest.fixture
def tident(scope='module'):
    set_stdsettings()
    from truealgebra.std.identities import(
        trig_ident0,
    )
    yield trig_ident0

    settings.reset()

def test_trig_ident0(tident):
    from truealgebra.std.std_settings import settings
    from truealgebra.std.identities import trig_ident0
    ex0 = parse(' sin(x)**2 + cos(x)**2 ')
    ex00 = parse(' cos(x)**2 + sin(x)**2 ')
    ex1 = parse(' 1 ')
    
    out0 = tident(ex0)
    out00 = tident(ex00)

    assert out0 == ex1
    assert out00 == ex1
