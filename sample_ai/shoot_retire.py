from battlematica import Library, StateQuerier


def shoot_retire(self, state):

    lib = Library()
    query = StateQuerier(self, state)

    closest_enemy = query(lib.enemies(),
                          lib.closest_to_xy(self.x, self.y))

    closest_enemy_nc = query(lib.enemies(),
                             lib.has_target(self.x, self.y),
                             lib.closest_to_xy(self.x, self.y))

    # if shield is low, flee
    if self.shield/self.max_shield < 0.2:
        if closest_enemy_nc:
            return 'move', 2 * self.x - closest_enemy_nc['x'], 2 * self.y - closest_enemy_nc['y']
        else:
            return 'loiter', self.x, self.y

    # shoot enemy in range 450
    tg = query(lib.enemies(),
               lib.position_in_circle(self.x, self.y, 450),
               lib.closest_to_xy(self.x, self.y))
    if tg:
        return 'shoot', tg['x'], tg['y']

    # go to nearest enemy
    if closest_enemy:
        return 'move', closest_enemy['x'], closest_enemy['y']


