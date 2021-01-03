import numpy as np

from battlematica.core.game_entity import GameEntity
from battlematica.core.geometry_primitives import angle, move_towards, distance


class _Bullet(GameEntity):

    state_props = [
        'x',
        'y',
        'tx',
        'ty',
        'hg',
        'r',
        'speed',
        'range',
        'dmg',
        'sprite',
        'size',
        'blast_sprite',
        'spread',
        'target_reached',
        'out_of_range'
    ]

    def __init__(
            self,
            x,
            y,
            tx,
            ty,
            hg,
            speed,
            range,
            dmg,
            sprite,
            size,
            blast_sprite,
            spread):

        super().__init__(x, y, 0.0, hg)

        self.speed = speed
        self.range = range
        self.dmg = dmg
        self.sprite = sprite
        self.size = size
        self.blast_sprite = blast_sprite
        self.spread = spread

        exact_angle = angle(x, y, tx, ty)
        dist = distance(x, y, tx, ty)
        realized_angle = exact_angle + 2*(np.random.rand()-.5) * self.spread

        realized_tx = x + dist * np.cos(np.deg2rad(realized_angle))
        realized_ty = y + dist * np.sin(np.deg2rad(realized_angle))

        self.tx = realized_tx
        self.ty = realized_ty

        self.r = realized_angle

        self.target_reached = False
        self.out_of_range = False

        self.original_x = x
        self.original_y = y

    def _chores(self, X, Y):
        if self.target_reached or self.out_of_range:
            raise ValueError('bullet was not removed after the end of its story')

        x, y = move_towards(self.x, self.y, self.tx, self.ty, self.speed)
        self.x = x
        self.y = y

        if distance(self.x, self.y, self.original_x, self.original_y) > self.range:
            self.out_of_range = True

        if np.isclose(self.x, self.tx) and np.isclose(self.y, self.ty):
            self.target_reached = True

        if self.out_of_range:
            return [('disappear', {})]

        if self.target_reached:
            return [('explode', {})]

        return []
