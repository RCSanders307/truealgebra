
class ChainProcessor:
    def __init__(self, *handlers):
        self.chain = self.last_handler
        for cls in reversed(handlers):
            self.addhandler(cls)

    def addhandler(self, handler_cls):
        self.chain = handler_cls(self.chain, self)
        self.chain.represent = self

    def last_handler(self, expr):
        return expr

    def __call__(self, expr):
        return self.chain(expr)





    class PostHandler(ABC):
        """Base method for detailed specific changes to StarPwr instance.
        """

        def __init__(self, nxt):
            self._nxt = nxt

        def handle(self, expr):
            out = self.process_expr(expr)
            if out is None:
                return self._nxt(expr)
            else:
                return out

        @abstractmethod
        def process_expr(self, expr):
            pass

