from truealgebra.core.rules import RulesBU, donothing_rule
from truealgebra.core.expressions import Number

class CommonSettingsSingleton():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommonSettingsSingleton, cls).__new__(cls)
            cls._instance.reset()
        return cls._instance

    def reset(self):
        self.evalnum = donothing_rule
        self.evalnumbu = RulesBU(donothing_rule)
        self.num0 = Number(0)
        self.num1 = Number(1)


commonsettings = CommonSettingsSingleton()
