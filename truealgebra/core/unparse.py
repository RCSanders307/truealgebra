from abc import ABC, abstractmethod
from truealgebra.core.settings import settings
from truealgebra.core.expressions import (
    Number, Symbol, Container, CommAssoc, NullSingleton, isCommAssoc,
    MultiExprs,
)
from truealgebra.core.constants import isoperatorname, issymbolname

from IPython import embed


class ReadableString:
    def __init__(self, *handlers):
        self.chain = self.last_handler
        for cls in reversed(handlers):
            self.addhandler(cls)

    def addhandler(self, handler_cls):
        self.chain = handler_cls(self.chain, self)
        self.chain.represent = self

    def last_handler(self, expr):
        return repr(expr)

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
                if expr.name in settings.infixprefix and len(expr) == 1:
                    return 0
                elif expr.name in settings.custom_bp:
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
                if expr.name in settings.infixprefix and len(expr) == 1:
                    return settings.infixprefix[expr.name]
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
        if (
            self.need_parenthesis_on_left(lbp, leftarg)
            or self.does_num_need_paren(leftarg)
        ):
            return '(' + argstr + ') '
        else:
            return argstr + ' '

    def deal_with_right(self, rbp, rightarg):
        argstr = self(rightarg)
        if (
            self.need_parenthesis_on_right(rbp, rightarg)
            or self.does_num_need_paren(rightarg)
        ):
            return ' (' + argstr + ')'
        else:
            return ' ' + argstr

    def middle_item_CA(self, item, name, lbp, rbp, outstr):
        argstr = self(item)
        if (
            self.need_parenthesis_on_left(lbp, item)
            or self.need_parenthesis_on_right(rbp, item)
            or self.does_num_need_paren(item)
        ):
            outstr += name + ' (' + argstr + ') '
        else:
            outstr += name + ' ' + argstr + ' '
        return outstr

    def does_num_need_paren(self, item):
        return False



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
        if isCommAssoc(expr):
            if not expr.items:
                return expr.name + '()'
            elif len(expr.items) == 1:
                arg = self.parent(expr.items[0])
                return expr.name + '(' + arg + ')'

            lbp = self.parent.tlbp(expr)
            rbp = self.parent.trbp(expr)

            outstr = self.parent.deal_with_left(lbp, expr.items[0])

            for item in expr.items[1:-1]:
                outstr = self.parent.middle_item_CA(
                    item, expr.name, lbp, rbp, outstr
                )

            outstr += expr.name + self.parent.deal_with_right(
                rbp, expr.items[-1]
            )
            return outstr


class UnparseMultiExprs(ReadableHandlerBase):
    def handle_expr(self, multiexprs):
        if isinstance(multiexprs, MultiExprs):
            outstr = ''
            for expr in multiexprs.exprs[:1]:
                outstr += self.parent(expr)
            for expr in multiexprs.exprs[1:]:
                outstr += '; ' + self.parent(expr)
            return outstr


class UnparseNull(ReadableHandlerBase):
    def handle_expr(self, expr):
        if isinstance(expr, NullSingleton):
            return '<NULL>'


unparse = ReadableString(
    UnparseNumber,
    UnparseCommAssoc,
    UnparseOperator,
    UnparseBodiedFunct,
    UnparseFunctForm,
    UnparseSymbol,
    UnparseNull,
    UnparseMultiExprs,
)

