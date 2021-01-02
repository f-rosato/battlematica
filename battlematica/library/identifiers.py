from functools import wraps

"""These functions identify a group of GameEntities from a State."""


def _thru(f):
    @wraps(f)
    def just_f():
        return f
    return just_f


@_thru
def i_bots(state):
    bts = state['bots']
    return bts


@_thru
def i_artifacts(state):
    af = state['artifacts']
    af_free = [x for x in af if not x['is_carried']]
    return af_free


@_thru
def i_drop_ports(state):
    af = state['drop_ports']
    return af
