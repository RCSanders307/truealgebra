from truealgebra.core.unparse import (
    ReadableString, UnparseNumber, UnparseOperator, UnparseBodiedFunct,
    UnparseFunctForm, UnparseSymbol, UnparseNull, ReadableHandlerBase
)
from truealgebra.core.expressions import (
    isCommAssoc, isContainer, isNumber, CommAssoc, Container
)


class UnparseCommAssocPlus(ReadableHandlerBase):
    def handle_expr(self, expr):
        if isCommAssoc(expr, name = '+'):
            if not expr.items:
                return expr.name + '()'
            elif len(expr.items) == 1:
                arg = self.parent(expr.items[0])
                return expr.name + '(' + arg + ')'

            lbp = self.parent.tlbp(expr)
            rbp = self.parent.trbp(expr)
            outstr = self.parent.deal_with_left(lbp, expr.items[0])

            for item in expr.items[1:-1]:
                if isContainer(item, name='-', arity=1):
                    outstr = self.parent.middle_item_CA(
                        item[0], '-', lbp, rbp, outstr
                    )
                else:
                    outstr = self.parent.middle_item_CA(
                        item, '+', lbp, rbp, outstr
                    )

            item = expr.items[-1]
            if isContainer(item, name='-', arity=1):
                outstr += '-' + self.parent.deal_with_right(rbp, item[0])
            else:
                outstr += '+' + self.parent.deal_with_right(rbp, item)
            return outstr


class UnparseCommAssocStar(ReadableHandlerBase):
    def handle_expr(self, expr):
        if isCommAssoc(expr, name = '*'):
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
                    item, '*', lbp, rbp, outstr
                )

            outstr += expr.name + self.parent.deal_with_right(
                rbp, expr.items[-1]
            )
            return outstr
