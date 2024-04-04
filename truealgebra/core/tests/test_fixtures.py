from truealgebra.core.expression import (
    CommAssoc, Number, Container, Symbol,
    null, true, false, any__
)
import pytest


@pytest.fixture
def exx():
    class MakeEx:
        sa = Symbol('a')
        sb = Symbol('b')
        i1 = Number(1)
        i2 = Number(2)
        in1 = Number(-1)
    return MakeEx()


