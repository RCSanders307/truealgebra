from truealgebra.core.rulebase import RuleBase
from truealgebra.core.expression import (
    Container, CommAssoc, Restricted, Number, Symbol, null
)
from truealgebra.core.settings import Settings
from truealgebra.core.parse import Parse
from truealgebra.core.err import ta_logger



class UnitData:
    """ Store data for unit affine conversions

    unit_base: Symbol
        string should be a symolname
        is the basis of the conversion data
        BUT is for information to user only
        It is used for nothing

    unit_dict: dict
        unit conversion data
        init_dict key: should be a Symbol instance
        init_dict value: should be a Number instance
        the key can be replaced with Container('*', (value, self.unit_base))
        
    """
    unit_dict = dict()
    base_unit = ''

    def __init__(self, unit):
        try:
            self.unit = unit
            self.factor = CommAssoc('*', (self.unit_dict[unit], unit))
        except:
            print('Houston something went wrong')


class _InnerAffineConvert(RuleBase):
    bottomup = True
    def __init__(self, *unit_data):
        self.unit_data = unit_data
        super().__init__(*args, **kwargs)
    def predicate(self, expr):
        return True
    def body(self.expr):
        for unit_datum in unit_data:
            if expr in unit_datum.unit_dict:
                newexpr = Container('/', (
                    unit_datum.factor, 
                    unit_datum.unit_dict[expr]
                )) 
                return newexpr
        return expr


class AffineConvert(RuleBase):
    bottomup = True
    def __init__(self, *unit_data, **kwargs):
        self.inner_rule = _InnerAffineConvert(*unit_data)
        super().__init__(*unit_data, **kwargs)


    def predicate(self, expr):
        return expr.name == '`' and isinstance(expr, Restricted)

    def body(self, expr):
        try:
            newunits = self.inner_rule(expr[1])
            return Restricted('`', (expr[0], newunits))
        except IndexError:
            ta_logger.log('units expression requires two items')
            return null

class MultiplyUnitsByOne(RuleBase):
    pass
     

