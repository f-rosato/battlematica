from collections import defaultdict
from functools import wraps

import numpy as np

from battlematica.core.game_entity import GameEntity
from battlematica.core.geometry_primitives import angle, the_correct_turn, move_towards, distance
from battlematica.core.constants import PORT_TOLERANCE


def _loiter_default_wrap(fn):

    @wraps(fn)
    def loiter_default_fn(self, *args, **kwargs):
        result = fn(self, *args, **kwargs)
        if result is None:
            return 'loiter', self.tx, self.ty
        else:
            return result

    return loiter_default_fn


class Bot(GameEntity):

    state_props = [

        "x", "y", "r", "hg",

        "max_health",
        "max_shield",
        "size",
        "firing_period",
        "bullet_spread",
        "bullet_speed",
        "bullet_range",
        "bullet_dmg",
        "walk_speed",
        "crawl_speed",
        "rotation_speed",
        "shield_reload_speed",
        "shield_reload_dead_time",

        "graphics",

        "health",
        "shield",
        "dead",

        "ca",
        "tx",
        "ty",

        'is_carrying',
        'shield_dead_time_pct',
        'reload_time_pct',

    ]

    def __init__(
            self,
            x, y, r, hg,
            max_health=400.0,
            max_shield=200.0,
            size=0.5,
            firing_period=10.0,
            bullet_spread=4,
            bullet_speed=80.0,
            bullet_range=300.0,
            bullet_dmg=12.0,
            walk_speed=3.0,
            crawl_speed=1.5,
            rotation_speed=7.0,
            shield_reload_speed=3.0,
            shield_reload_dead_time=40.0,
            graphics={}):
        
        """
        The Bot is the fighter of Battlematica.

        :param x: x coordinate of the bot
        :param y: y coordinate of the bot
        :param r: rotation of the bot in degrees (0 points right)
        :param hg: the team of the bot (integer)
        :param max_health: it's the total HP of the bot.
        :param max_shield: it's the total shield of the bot.
        :param size: a float indicating the phisical size of the bot (influences hitbox).
        :param firing_period: it's the amount of ticks that the bot needs to load the next shot.
        :param bullet_spread: angular spread of the bullets. A spread of 0 means perfect aim.
        :param bullet_speed: the speed in u/tick at which the bullet moves
        :param bullet_range: distance in u before the fired bullet becomes ineffective
        :param bullet_dmg: hp/shield damage inflicted by one bullet
        :param walk_speed: walking speed in u/tick
        :param crawl_speed: walking speed in u/tick when carrying an artifact
        :param rotation_speed: body rotation speed in degrees/tick
        :param shield_reload_speed: shield reload speed in HP/tick
        :param shield_reload_dead_time: ticks that must pass without receiving damage for the shield to start reloading
        :param graphics: dict of graphic parameters for display (see guide). Can be an empty dict if no display is used.

        """

        super(Bot, self).__init__(x, y, r, hg)

        # static properties
        self.max_health = max_health
        self.max_shield = max_shield
        self.firing_period = firing_period
        self.bullet_spread = bullet_spread
        self.bullet_speed = bullet_speed
        self.bullet_range = bullet_range
        self.bullet_dmg = bullet_dmg
        self.walk_speed = walk_speed
        self.crawl_speed = crawl_speed
        self.rotation_speed = rotation_speed
        self.shield_reload_speed = shield_reload_speed
        self.shield_reload_dead_time = shield_reload_dead_time
        self.graphics = graphics
        self.size = size

        # health
        self.health = self.max_health
        self.shield = self.max_shield

        # operating
        self.last_hit_ticks_ago = 1e9
        self.last_fire_ticks_ago = 1e9
        self.dead = False

        # decision
        self.ca = 'loiter'
        self.tx = self.x
        self.ty = self.y

        # artifact carry
        self.carry = None

        # ai
        self.ai = lambda _self, _state: ('loiter', self.x, self.y)

    def set_ai(self, ai):

        """Sets the Bot's AI function.

        :param ai: a function that accepts (bot_instance, state) and returns
         a tuple (action, target_x, target_y).

        """

        self.ai = _loiter_default_wrap(ai)

    @property
    def is_carrying(self):
        return self.carry is not None

    @property
    def shield_dead_time_pct(self):
        return min(self.last_hit_ticks_ago/self.shield_reload_dead_time, 1.0)

    @property
    def reload_time_pct(self):
        return min(self.last_fire_ticks_ago/self.firing_period, 1.0)

    @property
    def shield_pct(self):
        return self.shield / self.max_shield

    @property
    def health_pct(self):
        return self.health / self.max_health

    def distance_from(self, x, y):
        return distance(self.x, self.y, x, y)

    def _bullet_params(self):

        """Returns all the params needed to initialized a bulled fired in the current moment"""

        g = defaultdict(lambda: None)
        g.update(self.graphics)

        bullet_params = {
            'x': self.x,
            'y': self.y,
            'tx': self.tx,
            'ty': self.ty,
            'hg': self.hg,
            'speed': self.bullet_speed,
            'range': self.bullet_range,
            'dmg': self.bullet_dmg,
            'sprite': g['bullet_type'],
            'size': g['bullet_size'],
            'blast_sprite': g['bullet_blast_type'],
            'spread': self.bullet_spread}

        return bullet_params

    def _chores(self, X, Y):

        actions = []

        if self.dead:
            return [('drop', {}), ('disappear', {})]

        # rotate; rotation is free and happens in any case
        t_a = angle(self.x, self.y, self.tx, self.ty)
        target_rotation = the_correct_turn(self.r, t_a)
        sn = np.sign(target_rotation)
        self.r = self.r + sn * np.minimum(np.abs(target_rotation), self.rotation_speed)

        # advance to target location
        if self.ca in ('move', 'pick', 'drop'):
            self.last_fire_ticks_ago = 0

            if self.carry is not None:
                speed = self.crawl_speed
            else:
                speed = self.walk_speed

            xy = move_towards(self.x, self.y, self.tx, self.ty, speed)
            x = xy[0]
            y = xy[1]
            self.x = np.clip(x, 0, X)
            self.y = np.clip(y, 0, Y)

            if self.carry is not None:
                self.carry.x = self.x
                self.carry.y = self.y

            # pick and unpick
            if self.ca in ('pick', 'drop'):
                if distance(self.x, self.y, self.tx, self.ty) < PORT_TOLERANCE:
                    actions = [(self.ca, {})]

        # shoot/reload
        elif self.ca == 'shoot':

            if self.carry is None:
                can_shoot = self.reload_time_pct >= 1.0  # and np.isclose(target_rotation, 0.0, rtol=4.e-1)
                if can_shoot:
                    self.last_fire_ticks_ago = 0
                    g = defaultdict(lambda: None)
                    g.update(self.graphics)

                    actions = [('fire_round', {})]
                self.last_fire_ticks_ago += 1

            else:
                # cannot shoot while carrying
                pass

        elif self.ca == 'loiter':
            self.last_fire_ticks_ago = 0

        else:
            raise ValueError(f'unknown action "{self.ca}"')

        # reshield
        self.last_hit_ticks_ago += 1
        can_reshield = self.shield_dead_time_pct >= 1.0
        if can_reshield:
            self.shield = min(self.max_shield, self.shield + self.shield_reload_speed)

        return actions

    def _take_dmg(self, dmg):

        self.last_hit_ticks_ago = 0
        excess_dmg = max(0, dmg - self.shield)
        self.shield = max(0, self.shield - dmg)
        self.health = max(0, self.health - excess_dmg)
        if self.health <= 0:
            self.dead = True

    def _think(self, state):
        self.ca, self.tx, self.ty = self.ai(self, state)