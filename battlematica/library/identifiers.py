"""These functions identify a group of GameEntities from a State."""


def i_bots():
    def _i_bots(state):
        bts = state['bots']
        return bts

    return _i_bots


def i_artifacts():
    def _i_artifacts(state):
        af = state['artifacts']
        af_free = [x for x in af if not x['is_carried']]
        return af_free
    return _i_artifacts


def i_drop_ports():
    def _i_drop_ports(state):
        af = state['drop_ports']
        return af

    return _i_drop_ports
