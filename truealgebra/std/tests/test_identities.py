print("howdy")
from truealgebra.std.identities import(
    trig_ident0,
)
from truealgebra.std.std_settings import parse
import pytest

def test_trig_ident0():
    ex0 = parse(' sin(x)**2 + cos(x)**2 ')
    ex00 = parse(' cos(x)**2 + sin(x)**2 ')
    ex1 = parse(' 1 ')
    
    out0 = trig_ident0(ex0)
    out00 = trig_ident0(ex00)

    assert out0 == ex1
    assert out00 == ex1
