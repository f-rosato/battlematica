"""These functions identify a group of GameEntities from a State."""


def i_bots(calling_bot, state):
    bts = state['bots']
    return bts


def i_artifacts(calling_bot, state):
    af = state['artifacts']
    af_free = [x for x in af if not x['is_carried']]
    return af_free


def i_drop_ports(calling_bot, state):
    af = state['drop_ports']
    return af
