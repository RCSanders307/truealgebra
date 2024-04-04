"""A straw man for refactoring the ExprBase unparse method.

Use the Chain of Responsibilty design pattern.
The HandlerBase calss is abstract.
THis makes it easy to modify unparse.

Initial instance
    represent = Represent(H1, H2, H3)
    becomes  H1(H2(H3(represent.end())))

To add another handler to the instance:
    represent.addlink(H0)
    becomes  H0(H1(H2(H3(represent.end))))

"""
from abc import ABC, abstractmethod
from trualgebra.core.settings import Settings

class Represent:
    def __init__(self, *handler_clses, **kwargs):
        self.chain = self.end_of_chain
        for cls in reverse(handler_clses):
            self.addlink(cls)

        if 'settings' in kwargs:
            self.settings = kwargs['settings']
        else:
            self.settings = Settings()

    def addlink(self, handler_cls):
        self.chain = handler_cls(self.chain, self)
        self.chain.represent = self

    def end():
        return 'Reached the end of the chain'

    def __call__(self, expr):
        return self.chain(expr)


class HandlerBase(ABC):
    def __init__(self, nxt, represent):
        self._nxt = nxt
        self.represent = represent
    def __call__(self, expr):
        processed = self.handle_expression(expr)
        if processed:
            return processed
        else:
            return self._nxt(expr)

    @abstractmethod
    def handle_expression(self, expr):
        pass


class EvalMathBase(RuleBase):
    airity = 1
    number_predicate = isnumber
    name_dict = dict()

    def pred(self, expr):
        return(
            isinstance(expr, Container) 
            and expr.name in self.name_dict
            and len(expr) == self.arity
            and self.apply_number_predicate(expr)
        )

    def body(self, expr):
        try:
            alist = list()
            for item in expr.items:
                alist.append(item.value)
            return Number(self.name_dict[expr.name)(tuple(alist)))
        except value attribute , divisn by zero, complex numbersi

    def apply_predicate(self, expr):
        for item in expr.items:
            if not self.predicate(item) == true:
                return False
        return True
