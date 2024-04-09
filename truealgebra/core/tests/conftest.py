from truealgebra.core.expression import (
    CommAssoc, Number, Container, Symbol, Assign, Restricted,
    null, true, false, any__
)
from truealgebra.core.settings import SettingsSingleton
import pytest


@pytest.fixture
def ex():
    class MakeEx:
        sa = Symbol('a')
        sb = Symbol('b')
        sc = Symbol('c')
        se = Symbol('e')
        sf = Symbol('f')
        s_ = Symbol('_')
        sx = Symbol('x')
        sy = Symbol('y')
        sz = Symbol('z')

        i0 = Number(0)
        i1 = Number(1)
        i2 = Number(2)

        in1 = Number(-1)

        r3 = Number(3.0)
        r9 = Number(9.0)

        @property
        def trig0(self):
            cosx = Container('cos', (self.sx,))
            cosx_2 = Container('**', (cosx, self.i2))
            siny = Container('sin', (self.sy,))
            siny_2 = Container('**', (siny, self.i2))
            return Container('-', (cosx_2, siny_2))

        @property
        def trig1(self):
            star2x = CommAssoc('*', (self.i2, self.sx))
            return Container('cos', (star2x,))

        @property
        def trig2(self):
            cos2 = Container('cos', (self.i2,))
            cos2_2 = Container('**', (cos2, self.i2))
            sin2 = Container('sin', (self.i2,))
            sin2_2 = Container('**', (sin2, self.i2))
            return Container('-', (cos2_2, sin2_2))

        @property
        def trig3(self):
            cosx = Container('cos', (self.sx,))
            cosx_2 = Container('**', (cosx, self.i2))
            sinx = Container('sin', (self.sx,))
            sinx_2 = Container('**', (sinx, self.i2))
            return Container('-', (cosx_2, sinx_2))

        @property
        def trig4(self):
            sinx = Container('sin', (self.sx,))
            return Container('**', (sinx, self.i2))

    return MakeEx()


@pytest.fixture
def conftest_settings():
    settings = SettingsSingleton()
    settings.set_default_bp(251, 252)
    settings.set_custom_bp('!', 2000, 0)
    settings.set_custom_bp('!!!', 3000, 0)
    settings.set_custom_bp('/', 1100, 1100)
    settings.set_custom_bp('**', 1251, 1250)
    settings.set_custom_bp('*', 1000, 999)
    settings.set_custom_bp('+', 500, 500)
    settings.set_custom_bp("@", 0, 3000)
    settings.set_custom_bp("%", 0, 10)

    settings.set_bodied_functions('D', 481)
    settings.set_symbol_operators("and", 75, 76)
    settings.set_symbol_operators("E")
    settings.set_symbol_operators("jj")
    settings.set_infixprefix("-", 999)
    settings.set_container_subclass('+', CommAssoc)
    settings.set_container_subclass('*', CommAssoc)
    settings.set_container_subclass(':=', Assign)
    settings.set_container_subclass('Rule', Restricted)

    settings.set_sqrtneg1('j')
    settings.set_complement('star', '*')
    settings.set_complement('!!', '+')


    return settings




