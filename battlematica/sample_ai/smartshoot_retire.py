import math

from battlematica import StateQuerier
from battlematica import library as lib
from battlematica.core.geometry_primitives import angle, distance


def smartshoot_retire(self, state):

    # this version of shoot retire includes predictive shooting and is much, much more
    # effective against bots that move smoothly

    query = StateQuerier(state)

    closest_enemy = query(lib.i_bots(),
                          lib.f_not_of_teams(self.hg),
                          lib.s_closest_to_xy(self.x, self.y))

    closest_enemy_nc = query(lib.i_bots(),
                             lib.f_not_of_teams(self.hg),
                             lib.f_has_target(self.x, self.y),
                             lib.s_closest_to_xy(self.x, self.y))

    # if shield is low, flee
    if self.shield/self.max_shield < 0.2:
        if closest_enemy_nc is not None:
            return 'move', 2 * self.x - closest_enemy_nc['x'], 2 * self.y - closest_enemy_nc['y']
        else:
            return 'loiter', self.x, self.y

    # shoot enemy well into range (80% of firing range)
    tg = query(lib.i_bots(),
               lib.f_not_of_teams(self.hg),
               lib.f_position_in_circle(self.x, self.y, self.bullet_range * .8),
               lib.s_closest_to_xy(self.x, self.y))
    if tg is not None:

        # smart ballistics
        if tg['ca'] in ('move', 'pick', 'drop'):
            enemy_walk_speed = tg['crawl_speed'] if tg['is_carrying'] else tg['walk_speed']
            enemy_walk_angle = math.radians(angle(tg['x'], tg['y'], tg['tx'], tg['ty']))
            enemy_distance = distance(self.x, self.y, tg['x'], tg['y'])
            bullet_fly_ticks = enemy_distance / self.bullet_speed

            predicted_x = tg['x'] + enemy_walk_speed * bullet_fly_ticks * math.cos(enemy_walk_angle)
            predicted_y = tg['y'] + enemy_walk_speed * bullet_fly_ticks * math.sin(enemy_walk_angle)

            return 'shoot', predicted_x, predicted_y

        else:
            return 'shoot', tg['x'], tg['y']

    # go to nearest enemy
    if closest_enemy is not None:
        return 'move', closest_enemy['x'], closest_enemy['y']


