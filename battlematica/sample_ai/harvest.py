from battlematica import StateQuerier
from battlematica import library as lib


def harvest(self, state):

    sq = StateQuerier(state)

    # take nearest available artifact
    if self.carry is None:
        tg = sq(lib.i_artifacts(),
                lib.f_of_teams(self.hg, None),
                lib.s_closest_to_xy(self.x, self.y))
        if tg is not None:
            return 'pick', tg['x'], tg['y']

    else:
        tg = sq(lib.i_drop_ports(),
                lib.f_of_teams(self.hg, None),
                lib.s_closest_to_xy(self.x, self.y))
        if tg is not None:
            return 'drop', tg['x'], tg['y']
