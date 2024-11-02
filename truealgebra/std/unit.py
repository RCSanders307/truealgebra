from truealgebra.core.rules import Rule 
from truealgebra.core.expressions import (
    Container, CommAssoc, Restricted, Number, Symbol, null
)
#from truealgebra.core.settings import Settings
from truealgebra.core.parse import Parse
from truealgebra.core.err import ta_logger


class UnitForm():
    def __init__(self, coeff=1, units=None):
        if units is None:
            self.units = dict()
        else:
            self.units = units
        self.coeff = coeff


class SimplifyUnits(Rule):
    def postinit(self, *args, **kwargs):
        self.name = args[0]

    def predicate(self, expr):
        return isinstance(expr, Restricted) and expr.name == '`'

    def body(self, expr):
        try:
            unitform = self.make_eval(expr[1])
        except IndexError:
            ta_logger.log('Unit expression must have two items')
            return null
        upstairs, downstairs = self.cleanup(unitform)
        units = self.make_units(upstairs, downstairs)
        try:
            num = Number(expr[0].value * unitform.coeff)
        except TypeError:
            ta_logger.log('First item unit expression must be a number.')
            return null
        if units == Number(1):
            return num
        else:
            return Restricted(self.name, (num, units))

    def make_eval(self, expr):
        if expr.name == '/' and isinstance(expr, Container):
            return self.eval_div(expr)
        elif expr.name == '**' and isinstance(expr, Container):
            return self.eval_power(expr)
        elif expr.name == '*' and isinstance(expr, CommAssoc):
            return self.eval_mul(expr)
        elif isinstance(expr, Number):
            return self.eval_num(expr)
        else:
            return self.eval_sym(expr)

    def eval_power(self, expr):
        uf = UnitForm()
        if isinstance(expr[0], Number) and isinstance(expr[1], Number):
            uf.coeff = expr[0].value ** expr[1].value
        elif isinstance(expr[1], Number):
            base_unitform = self.make_eval(expr[0])
            num = expr[1].value
            for key in base_unitform.units.keys():
                uf.units[key] = base_unitform.units[key] * num
            uf.coeff = base_unitform.coeff ** num
        else:
            uf.units[expr] = 1
        return uf

    def eval_div(self, expr):
        uf = self.make_eval(expr[0])
        lower_uf = self.make_eval(expr[1])
        for key in lower_uf.units.keys():
            if key in uf.units.keys():
                uf.units[key] = uf.units[key] - lower_uf.units[key]
            else:
                uf.units[key] = -lower_uf.units[key]
        uf.coeff = uf.coeff / lower_uf.coeff
        return uf

    def eval_mul(self, expr):
        uf = UnitForm()
        for item in expr.items:
            item_uf = self.make_eval(item)
            for key in item_uf.units.keys():
                if key in uf.units.keys():
                    uf.units[key] = uf.units[key] + item_uf.units[key]
                else:
                    uf.units[key] = item_uf.units[key]
            uf.coeff = uf.coeff * item_uf.coeff
        return uf

    def eval_num(self, expr):
        uf = UnitForm()
        uf.coeff = expr.value
        return uf

    def eval_sym(self, expr):
        uf = UnitForm()
        uf.units[expr] = 1
        return uf

    def cleanup(self, unitform):
        upstairs = list()
        downstairs = list()
        for key in unitform.units.keys():
            num = unitform.units[key]
            try:
                if num == 1:
                    upstairs.append(key)
                elif num > 0:
                    upstairs.append(Container('**', (key, Number(num))))
                elif num == -1:
                    downstairs.append(key)
                elif num < 0:
                    downstairs.append(Container('**', (key, Number(-num))))
                # cases where num == 0 are ignored
            except TypeError:
                ta_logger.log('Units cannot have complex numbers as exponent')
                return ([null], list())
                
        return (upstairs, downstairs)

    def make_units(self, upstairs, downstairs):
        if not len(upstairs) and not len(downstairs):
            return Number(1)

        if len(upstairs) == 0:
            up = Number(1)
        elif len(upstairs) == 1:
            up = upstairs[0]
        else:
            up = CommAssoc('*', upstairs)

        if len(downstairs):
            if len(downstairs) == 1:
                down = downstairs[0]
            else:
                down = CommAssoc('*', downstairs)
            return Container('/', (up, down))
        else:
            return up

class ConvertToBasis(Rule):
    """Convert units of a certain type to a specifird unit.

    unit_dict: dict
        Dictioary of unit conversion factors.
        The keys are strings.
        The basis has a converion factor of 1
        Example 'm': 1 ; 'm' is the basis
        Example 'cm: 0.1 ; means unit m can be replaced by 0.1 cm
    """
    def postinit(self, *args, **kwargs):
        try:
            toname = args[0]
        except:
            # print error message and do something
            pass

        self.innerrule = self.InnerRule(self.unit_dict, toname)

    unit_dict = dict() # replace key with (basis * value)
                        # the dict value is a Number instance
                        # the dict key is a string

    def predicate(self, expr):
        return expr.name == '`' and isinstance(expr, Restricted)

    def body(self, expr):
        try:
            newunits = self.innerrule(expr[1])
            return Restricted('`', (expr[0], newunits))
        except IndexError:
            ta_logger.log('units expression requires two items')
            return null

    class InnerRule(Rule):
        def postinit(self, *args, **kwargs):
            self.unit_dict = args[0]
            toname = args[1]

            self.tonum = Number(self.unit_dict[toname])
            self.tounit = Symbol(toname)

        bottomup=True

        def predicate(self, expr):
            return isinstance(expr, Symbol) and expr.name in self.unit_dict

        def body(self, expr):
            up = CommAssoc('*', (self.tounit, Number(self.unit_dict[expr.name])))
            return Container('/', (up, self.tonum))


class MultiplyUnitsByBasis(Rule):
    parse = Parse()

    def postinit(self, *args, **kwargs):
        if 'parse' in kwargs:
            self.parse = kwargs['parse']
        self.factor = self.parse(args[0])

    def predicate(self, expr):
        return expr.name == '`' and isinstance(expr, Restricted)

    def body(self, expr):
        try:
            newunits = CommAssoc('*', (self.factor, expr[1]))
            return Restricted('`', (expr[0], newunits))
        except IndexError:
            ta_logger.log('units expression requires two items')
            return null

class AffineConvert(Rule):
    def postinit(self, *args, **kwargs):
        self.from_unit = Symbol(kwargs['from_unit'])
        self.to_unit = Symbol(kwargs['to_unit'])

        if 'from_offset' in kwargs:
            self.from_offset = kwargs['from_offset']
        else:
            self.from_offset = 0

        if 'to_offset' in kwargs:
            self.to_offset = kwargs['to_offset']
        else:
            self.to_offset = 0

        if 'factor' in kwargs:
            self.factor = kwargs['factor']
        else:
            self.factor = 1

    def predicate(self, expr):
        try:
            return (
                expr.name == '`'
                and isinstance(expr, Restricted)
                and expr[1] == self.from_unit
            )
        except IndexError:
            ta_logger('Unit expression requires two items')
            return False
    
    def body(self, expr):
        from_num = expr[0].value  # may need a try/except statement here
        to_num = self.factor * (from_num + self.from_offset) + self.to_offset
        return Restricted('`', (Number(to_num), self.to_unit))

