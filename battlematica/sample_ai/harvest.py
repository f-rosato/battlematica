from battlematica import Library, StateQuerier


def harvest(self, state):

    lib = Library()
    sq = StateQuerier(self, state)

    # take nearest available artifact
    if self.carry is None:
        tg = sq(lib.artifacts_ally(),
                lib.closest_to_xy(self.x, self.y))
        if tg:
            return 'pick', tg['x'], tg['y']

    else:
        tg = sq(lib.drop_ports_ally(), lib.closest_to_xy(self.x, self.y))
        return 'drop', tg['x'], tg['y']