"""These functions identify a group of GameEntities from a State."""


def allies(self, state):
    bots = state['bots']
    ally_bots = [x for x in bots if x['hg'] == self.hg]
    return ally_bots


def enemies(self, state):
    bots = state['bots']
    enemy_bots = [x for x in bots if x['hg'] != self.hg]
    return enemy_bots


def artifacts(self, state):
    af = state['artifacts']
    return af


def artifacts_ally(self, state):
    af = state['artifacts']
    af_mine = [x for x in af if (x['hg'] == self.hg or x['hg'] is None) and not x['is_carried']]
    return af_mine


def artifacts_enemy(self, state):
    af = state['artifacts']
    af_mine = [x for x in af if (x['hg'] != self.hg or x['hg'] is None) and not x['is_carried']]
    return af_mine


def artifacts_ally_only(self, state):
    af = state['artifacts']
    af_mine = [x for x in af if x['hg'] == self.hg and not x['is_carried']]
    return af_mine


def artifacts_enemy_only(self, state):
    af = state['artifacts']
    af_mine = [x for x in af if x['hg'] != self.hg and not x['is_carried']]
    return af_mine


def artifacts_neutral(self, state):
    af = state['artifacts']
    af_mine = [x for x in af if x['hg'] is None and not x['is_carried']]
    return af_mine


def drop_ports(self, state):
    af = state['drop_ports']
    return af


def drop_ports_ally(self, state):
    af = state['drop_ports']
    af_mine = [x for x in af if x['hg'] == self.hg or x['hg'] is None]
    return af_mine


def drop_ports_enemy(self, state):
    af = state['drop_ports']
    af_mine = [x for x in af if x['hg'] != self.hg or x['hg'] is None]
    return af_mine


def drop_ports_ally_only(self, state):
    af = state['drop_ports']
    af_mine = [x for x in af if x['hg'] == self.hg]
    return af_mine


def drop_ports_enemy_only(self, state):
    af = state['drop_ports']
    af_mine = [x for x in af if x['hg'] != self.hg]
    return af_mine


def drop_ports_neutral(self, state):
    af = state['drop_ports']
    af_mine = [x for x in af if x['hg'] is None]
    return af_mine