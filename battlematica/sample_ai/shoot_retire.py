from battlematica import Library, StateQuerier


def shoot_retire(self, state):

    lib = Library()
    query = StateQuerier(self, state)

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
    if tg:
        return 'shoot', tg['x'], tg['y']

    # go to nearest enemy
    if closest_enemy is not None:
        return 'move', closest_enemy['x'], closest_enemy['y']


