from sample_ai.shoot_retire import shoot_retire
from sample_ai.harvest import harvest


def shoot_then_harvest(self, state):

    for f in (shoot_retire, harvest):
        a = f(self, state)
        if a is not None:
            return a
    return 'loiter', self.tx, self.ty
