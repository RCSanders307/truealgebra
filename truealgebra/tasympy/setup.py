from truealgebra.core.settings import settings
from truealgebra.common.commonsettings import commonsettings
from truealgebra.tasympy.setup_func import tasympy_setup_func
from truealgebra.common.setup_func import common_setup_func


settings.reset()
commonsettings.reset()
common_setup_func()
tasympy_setup_func()

