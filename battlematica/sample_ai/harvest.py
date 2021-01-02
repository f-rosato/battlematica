from battlematica import Library, StateQuerier


def harvest(self, state):

    lib = Library()
    sq = StateQuerier(self, state)

    # take nearest available artifact
    if self.carry is None:
        tg = sq(lib.i_artifacts(),
                lib.f_of_teams(self.hg),
                lib.s_closest_to_xy(self.x, self.y))
        if tg:
            return 'pick', tg['x'], tg['y']

    else:
        tg = sq(lib.i_drop_ports(),
                lib.f_of_teams(self.hg),
                lib.s_closest_to_xy(self.x, self.y))
        return 'drop', tg['x'], tg['y']