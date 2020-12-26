from sample_ai.harvest import harvest
from sample_ai.shoot_retire import shoot_retire


def harvest_then_shoot(self, state):
    for f in (harvest, shoot_retire):
        a = f(self, state)
        if a is not None:
            return a
    return 'loiter', self.tx, self.ty
