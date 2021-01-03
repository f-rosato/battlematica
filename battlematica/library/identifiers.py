from .partializer import partializable

"""These functions identify a group of GameEntities from a State."""


@partializable
def i_bots(state):
    bts = state['bots']
    return bts


@partializable
def i_artifacts(state):
    af = state['artifacts']
    af_free = [x for x in af if not x['is_carried']]
    return af_free


@partializable
def i_drop_ports(state):
    af = state['drop_ports']
    return af
