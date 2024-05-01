from abc import ABC, abstractmethod
from truealgebra.core.settings import settings
from truealgebra.core.expression import (
    Number, Symbol, Container, CommAssoc, Null, End
)
from truealgebra.core.constants import isoperatorname, issymbolname


class ReadableString:
    def __init__(self, *handlers):
        self.chain = self.last_handler
        for cls in reversed(handlers):
            self.addhandler(cls)

    def addhandler(self, handler_cls):
        self.chain = handler_cls(self.chain, self)
        self.chain.represent = self

    def last_handler(self, expr):
        return str(expr)

    def __call__(self, expr):
        return self.chain(expr)

    def tlbp(self, expr):
        """Token Left Binding Power, which is
        the left binding power of top level of expression
        as if it is a newly created parsing token.

        expr :truealgebra expression

        returns
        -------
        non-negative int
            left binding power, see docs
        """
        if isinstance(expr, Container):
            if isoperatorname(expr.name):
                if expr.name in settings.custom_bp:
                    return settings.custom_bp[expr.name].lbp
                else:
                    return settings.default_bp.lbp
            elif expr.name in settings.bodied_functions:
                return 0
            elif expr.name in settings.symbol_operators:
                return settings.symbol_operators[expr.name].lbp
            else:
                return 0
        else:
            return 0

    def trbp(self, expr):
        """Token Right Binding Power, which is
        the right binding power of top level of expression
        as if it is a newly created parsing token.

        expr :truealgebra expression

        returns
        -------
        non-negative int
            left binding power, see docs
        """
        if isinstance(expr, Container):
            if isoperatorname(expr.name):
                if expr.name in settings.custom_bp:
                    return settings.custom_bp[expr.name].rbp
                else:
                    return settings.default_bp.rbp
            elif expr.name in settings.bodied_functions:
                return settings.bodied_functions[expr.name]
            elif expr.name in settings.symbol_operators:
                return settings.symbol_operators[expr.name].rbp
            else:
                return 0
        else:
            return 0
    
    def funct_form(self, name, items):
        outstr = name + '('
        for item in items[:1]:
            outstr += self(item)
        for item in items[1:]:
            outstr += ', ' + self(item)
        outstr += ')'
        return outstr

    def llbp(self, expr):
        """ Least Left Binding Power

        The minimum non-zero left binding power in left side.
        This function recusively searches all expression layers.
        """
        least = self.tlbp(expr)
        if least > 0 and len(expr) > 0:
            lower_layer_least = self.llbp(expr[0])
            if lower_layer_least > 0 and lower_layer_least < least:
                return lower_layer_least
            else:
                return least
        else:
            return 0

    def lrbp(self, expr):
        """ Least Right Binding Power

        The minimum non-zero left binding power in Right side.
        This function recusively searches all expression layers.
        """
        least = self.trbp(expr)
        if least > 0 and len(expr) > 0:
            lower_layer_least = self.lrbp(expr[-1])
            if lower_layer_least > 0 and lower_layer_least < least:
                return lower_layer_least
            else:
                return least
        else:
            return 0

    def need_parenthesis_on_left(self, lbp, leftarg):
        arg_lrbp = self.lrbp(leftarg)
        return arg_lrbp > 0 and lbp > arg_lrbp

    def need_parenthesis_on_right(self, rbp, rightarg):
        arg_llbp = self.llbp(rightarg)
        # In parsing, with (left op) (token) (right op),
        # the rbp of the left operator wins all ties with
        # the lbp of the right operator.
        # That is why the >= comparison is used below
        return arg_llbp > 0 and rbp >= arg_llbp

    def deal_with_left(self, lbp, leftarg):
        argstr = self(leftarg)
        if self.need_parenthesis_on_left(lbp, leftarg):
            return '(' + argstr + ') '
        else:
            return argstr + ' '

    def deal_with_right(self, rbp, rightarg):
        argstr = self(rightarg)
        if self.need_parenthesis_on_right(rbp, rightarg):
            return ' (' + argstr + ')'
        else:
            return ' ' + argstr


class ReadableHandlerBase(ABC):
    def __init__(self, nxt, parent):
        self._nxt = nxt
        self.parent = parent

    def __call__(self, expr):
        str_out = self.handle_expr(expr)
        if str_out:
            return str_out
        else:
            return self._nxt(expr)

    @abstractmethod
    def handle_expr(self, expr):
        pass


class UnparseSymbol(ReadableHandlerBase):
    def handle_expr(self, expr):
        if isinstance(expr, Symbol):
            return expr.name


class UnparseNumber(ReadableHandlerBase):
    def handle_expr(self, expr):
        if isinstance(expr, Number):
            return str(expr.value)


class UnparseOperator(ReadableHandlerBase):
    def handle_expr(self, expr):
        if (
            isinstance(expr, Container)
            and (
                isoperatorname(expr.name)
                or expr.name in settings.symbol_operators
            )
        ):
            outstr = ''
            lbp = self.parent.tlbp(expr)
            if lbp:
                leftstr = self.parent.deal_with_left(lbp, expr[0])
                outstr += leftstr

            outstr += expr.name

            rbp = self.parent.trbp(expr)
            if rbp:
                rightstr = self.parent.deal_with_right(rbp, expr[-1])
                outstr += rightstr
            return outstr


class UnparseFunctForm(ReadableHandlerBase):
    def handle_expr(self, expr):
        if isinstance(expr, Container) and issymbolname(expr.name):
            return self.parent.funct_form(expr.name, expr.items)


class UnparseBodiedFunct(ReadableHandlerBase):
    def handle_expr(self, expr):
        if (
            isinstance(expr, Container)
            and expr.name in settings.bodied_functions
        ):
            outstr = self.parent.funct_form(expr.name, expr.items[:-1])
            rbp = self.parent.trbp(expr)
            if rbp:
                rightstr = self.parent.deal_with_right(rbp, expr[-1])
                outstr += rightstr
            return outstr


class UnparseCommAssoc(ReadableHandlerBase):
    def handle_expr(self, expr):
        if isinstance(expr, CommAssoc):
            if not expr.items:
                return expr.name + '()'
            elif len(expr.items) == 1:
                arg = self.parent(expr.items[0])
                return expr.name + '(' + arg + ')'

            lbp = self.parent.tlbp(expr)
            rbp = self.parent.trbp(expr)
            outstr = ''

            leftstr = self.parent.deal_with_left(lbp, expr.items[0])
            outstr += leftstr

            for item in expr.items[1:-1]:
                argstr = self.parent(item)
                if (
                    self.parent.need_parenthesis_on_left(lbp, item)
                    or self.parent.need_parenthesis_on_right(rbp, item)
                ):
                    outstr += expr.name + ' (' + argstr + ') '
                else:
                    outstr += expr.name + ' ' + argstr + ' '

            rightstr = self.parent.deal_with_right(rbp, expr.items[-1])
            outstr += expr.name + rightstr
            return outstr


class UnparseNull(ReadableHandlerBase):
    def handle_expr(self, expr):
        if isinstance(expr, Null):
            return '<NULL>'


class UnparseEnd(ReadableHandlerBase):
    def handle_expr(self, expr):
        if isinstance(expr, End):
            return '<END>'


unparse = ReadableString(
    UnparseNumber,
    UnparseCommAssoc,
    UnparseOperator,
    UnparseBodiedFunct,
    UnparseFunctForm,
    UnparseSymbol,
    UnparseNull,
    UnparseEnd,
)
