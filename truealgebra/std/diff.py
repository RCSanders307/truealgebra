
class Diff(RuleBase):
    def __init__(self, vars, rule_classes):
        self.vars = vars
        self.rules = list()
        for cls in rule_clsses:
            self.rules.append(clas(master=self, vars=vars))

    def predicate(self, expr):
        return isCo(expr, name='D') and len(expr) > 1

    def body(self, expr):
        ex = expr[-1]
        dvars = expr[:-1]
        out = expr
        for dv in dvars:
# need way of passing dv as an argumnetn
        pass

    def diff_sym(self, expr):
        if expr.name in self.vars:
            pass


class MiniDiff(ABC):
    def __init__(self, master, vars):
        self.master = master
        self.vars = vars

    def ___call___(self, expr, var):
        if self.predicate(expr):
            return self.body(expr, var)
        else:
            return expr

    @abstractmethod
    def predicate(expr):
        pass

    @abstractmethod
    def body(expr, var):


class SingleArg(Minidiff):
    def __init__(self, expr, vars):
        for key in self.diff_dict:
            self.diff_dict[key] = parse(self.diff_dict[key])
        super().__init__(expr, var)

    diff_dict = {
        'sin': cos(_),
    }

    def predicate(expr):
        return isCo(expr, arity=1) and name in self.diff_dict


    def body(expr, var):
        sub = Substitute(subdict={Symbol('_'): exp})
        out = sub(self.diff_dict[expr.name])
        return out * master.actual_diff(Expr[0], var)




