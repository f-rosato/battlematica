import warnings

from .harvest_then_shoot import harvest_then_shoot
from .shoot_then_harvest import shoot_then_harvest

try:
    import inputs
except ModuleNotFoundError:
    warnings.warn('Optional requirement "inputs" not found. '
                  'You will not be able to use gamepad_ai.')
else:
    from .gamepad_ai import gamepad_ai
