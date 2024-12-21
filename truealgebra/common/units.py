from truealgebra.core.expressions import (
    Container, Restricted, CommAssoc, Restricted, Symbol, Number,
    isNumber, isContainer, isCommAssoc, isRestricted
)
from truealgebra.core.rules import Rule, Rules, JustOneBU
from truealgebra.common.commonsettings import commonsettings as comset

from truealgebra.common.utility import (
    mulnums, subnums, negnum, pwrnums, divnums, addnums, create_starCA,
    create_plusCA,
)
from truealgebra.common.simplify import simplify
from truealgebra.core.err import TrueAlgebraError
from IPython import embed


def isunitexpr(expr):
    return isRestricted(expr, name='`', arity=2)

def create_unitexpr(num, units):
    """ assumption is that num is a Number object
    and that units has been simplifyed with simplify.
    """
    if isNumber(units):
        return mulnums(num, units)
    elif isCommAssoc(units, name='*') and isNumber(units[0]):
        # because of simplify, len(units)is >= 2
        return Restricted('`', (
            mulnums(num, units.items[0]),
            create_starCA(units.items[1:])
        ))
    elif (
        isContainer(units, name='/', arity = 2)
        and isNumber(units[0])
        and units[0] != comset.num1
    ):
        return Restricted('`', (
            mulnums(num, units[0]),
            Container('/', (comset.num1, units[1]))
        ))
    elif (
        isContainer(units, name='/', arity = 2)
        and isCommAssoc(units[0], name='*')
        and isNumber(units[0][0])
    ):
        return Restricted('`', (
            mulnums(num, units[0][0]),
            Container('/',(create_starCA(units[0][1:]), units[1]))
        ))
    else:
       return Restricted('`', (num, units))


class SimplifyUnits(Rule):
    def predicate(self, expr):
        return isunitexpr(expr)
    def body(self, expr):
        num = expr[0]
        units = simplify(expr[1])
        return create_unitexpr(num, units)


simplifyunits = SimplifyUnits()
simplifyunitsbu = SimplifyUnits(bottomup=True)


class EvalUnitSub(Rule):
    def predicate(self, expr):
        return isContainer(expr, name='-', arity=2)

    def body(self, expr):
        if (
            isContainer(expr[0], name='`', arity=2)
            and isContainer(expr[1], name='`', arity=2)
            and expr[0][1] == expr[1][1]
        ):
            num = subnums(expr[0][0], expr[1][0])
            units = expr[0][1]
#           xxx = 100; embed()
            return create_unitexpr(num, units)
        else:
            return expr


evalunitsub = EvalUnitSub()


class EvalUnitNeg(Rule):
    def predicate(self, expr):
        return isContainer(expr, name='-', arity=1)

    def body(self, expr):
        if isunitexpr(expr[0]):
            num = negnum(expr[0][0])
            units = expr[0][1]
            return create_unitexpr(num, units)
        else:
            return expr


evalunitneg = EvalUnitNeg()


class EvalUnitPwr(Rule):
    def predicate(self, expr):
        return isContainer(expr, name='**', arity=2)

    def body(self, expr):
        if isunitexpr(expr[0]) and isNumber(expr[1]):
            num = pwrnums(expr[0][0], expr[1])
            units = simplify(Container('**', (expr[0][1], expr[1])))
            return create_unitexpr(num, units)
        else:
            return expr


evalunitpwr = EvalUnitPwr()


class EvalUnitDiv(Rule):
    def predicate(self, expr):
        return isContainer(expr, name='/', arity=2)

    def body(self, expr):
        if isunitexpr(expr[0]) and isunitexpr(expr[1]):

            num = divnums(expr[0][0], expr[1][0])
            units = simplify(Container('/', (expr[0][1], expr[1][1])))
            return create_unitexpr(num, units)
        elif isunitexpr(expr[0]) and isNumber(expr[1]):
            num = divnums(expr[0][0], expr[1])
            units = expr[0][1]
            return create_unitexpr(num, units)
        elif isNumber(expr[0]) and isunitexpr(expr[1]):
            num = divnums(expr[0], expr[1][0])
            units = simplify(Container('/', (comset.num1, expr[1][1])))
            return create_unitexpr(num, units)
        else:
            return expr


evalunitdiv = EvalUnitDiv()


class EvalUnitMul(Rule):
    def predicate(self, expr):
        return isCommAssoc(expr, name='*')


    def body(self, expr):
        num_list = list()
        other_list = list()
        units_list = list()
        for item in expr:
            if isunitexpr(item):
                units_list.append(item[1])
                num_list.append(item[0])
            elif isNumber(item):
                num_list.append(item)
            else:
                other_list.append(item)
        if units_list:
            units = simplify(create_starCA(units_list))
            num = comset.evalnum(create_starCA(num_list))
            other_list.insert(0, create_unitexpr(num, units))
            return create_starCA(other_list)
        else:
            return expr


evalunitmul = EvalUnitMul()


class NewEvalUnitMul(Rule):
    """ This is a only a test. This rule uses data attributes to exchange
        between the predicate and body methods. This works here and should 
        work as long as a method does not call itself.
        While this works it is longer and less clear than EvalUnitMul
        which basically does the same thing
    """
    num_list = None
    units_list = None
    other_list = None

    def predicate(self, expr):
        if isCommAssoc(expr, name='*'):
            self.num_list = list()
            self.other_list = list()
            self.units_list = list()
            for item in expr:
                if isunitexpr(item):
                    self.units_list.append(item[1])
                    self.num_list.append(item[0])
                elif isNumber(item):
                    self.num_list.append(item)
                else:
                    self.other_list.append(item)
            if self.units_list:
                return True
            else:
                return False
        else:
            return False


    def body(self, expr):
        units = simplify(create_starCA(self.units_list))
        num = comset.evalnum(create_starCA(self.num_list))
        self.other_list.insert(0, create_unitexpr(num, units))
        out = create_starCA(self.other_list)

        self.num_list = None
        self.units_list = None
        self.other_list = None
        return out



_neweval = NewEvalUnitMul()
_newevalbu = NewEvalUnitMul(bottomup=True)


class EvalUnitPlus(Rule):
    def predicate(self, expr):
        return isCommAssoc(expr, name='+')

    units_dict = None

    def add_unitexpr_to_dict(self, unitexpr):
        if unitexpr[1] in self.units_dict:
            self.units_dict[unitexpr[1]] = addnums(
                self.units_dict[unitexpr[1]],
                unitexpr[0]
            )
        else:
            self.units_dict[unitexpr[1]] = unitexpr[0]

    def convert_dict_to_list(self):
        ulist = list()
        for units in self.units_dict:
            ulist.append(create_unitexpr(self.units_dict[units], units))
        self.units_dict = None
        return ulist

    def body(self, expr):
        self.units_dict = dict()
        other_list = list()
        for item in expr:
            if isunitexpr(item):
                self.add_unitexpr_to_dict(item)
            else:
                other_list.append(item)
        return create_plusCA(self.convert_dict_to_list() + other_list)

evalunitplus = EvalUnitPlus()

evalunitexpr = Rules( 
    comset.evalnumbu,
    JustOneBU(
        evalunitmul, evalunitdiv, evalunitpwr, evalunitplus, evalunitsub,
        evalunitneg,
    )
)


class UnitDimension:
    def __init__(self):
        self.convdict = dict
        self.basis = ''

length_dimension = UnitDimension()

length_dimension.basis = 'm'
length_dimension.convdict = {
    Symbol('m'): comset.num1,
    Symbol('cm'): Number(0.01),
    Symbol('km'): Number(1000),
    Symbol('in'): Number(0.003937),
}


class ConvertDimension(Rule):
    def __init__(self, *rules, **kwargs):
        try:
            self.target = kwargs['target']
        except:
            raise TrueAlgebraError(
               'ConvertDimension instantiation requres a target argument'
            )

        try:
            self.dimension = kwargs['dimension']
        except:
            raise TrueAlgebraError(
               'ConvertDimension instantiation requres a dimension argument'
            )

            # need to raise an errror
        self.coef = self.dimension.convdict[self.target]
        self.replace = self.__class__.Replace(parent=self)

        super().__init__(*rules, **kwargs)

    def predicate(self, expr):
        return isunitexpr(expr)

    def body(self, expr):
        newunits = simplify(self.replace(expr[1]))
        return create_unitexpr(expr[0], newunits)
    
    class Replace(Rule):
        def __init__(self, *args, **kwargs):
            if 'parent' in kwargs:
                self.parent = kwargs['parent']
            super().__init__(*args, **kwargs)
        def predicate(self, expr):
            return expr in self.parent.dimension.convdict
        def body(self, expr):
            ratio = divnums(
                self.parent.dimension.convdict[expr], 
                self.parent.coef
            )
            return CommAssoc('*', (ratio, self.parent.target))
        bottomup=True


class ConvertUnity(Rule):
    def __init__(self, *rules, **kwargs):
        try:
            self.unity = kwargs['unity']
        except:
            raise TrueAlgebraError(
               'ConvertUnity instantiation requres a unity argument'
            )
            # need to raise an errror
        super().__init__(*rules, **kwargs)

    def predicate(self, expr):
        return isunitexpr(expr)

    def body(self, expr):
        newunits = simplify(CommAssoc('*', (self.unity, expr[1])))
        return create_unitexpr(expr[0], newunits)

