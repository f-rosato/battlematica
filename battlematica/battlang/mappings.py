import battlematica.library as lib

selectors_map = {
    'WEAKEST': (1, lib.s_lowest_abs_health.__name__, ''),
    'MOST_HEALTH': (1, lib.s_highest_abs_health.__name__, ''),
    'NEAREST': (1, lib.s_closest_to_xy.__name__, 'self.x, self.y'),
    'LEAST_SHIELD': (1, lib.s_lowest_abs_shield.__name__, ''),
    'MOST_SHIELD': (1, lib.s_highest_abs_shield.__name__, ''),
    'CLOSEST_TO': (2, lib.s_closest_to_xy.__name__, '{cnodes_1}'),
    'FARTHEST_FROM': (2, lib.s_closest_to_xy.__name__, '{cnodes_1}')
}

filters_map = {
    'CARRYING': (1, lib.f_is_carrying.__name__, ''),
    'SHOOTING': (1, lib.f_current_action.__name__, '"shoot"'),
    'LOITERING': (1, lib.f_current_action.__name__, '"loiter"'),
    'PICKING': (1, lib.f_current_action.__name__, '"pick"'),
    'WITH_TARGET': (2, lib.f_has_target.__name__, '{cnodes_1}'),
    'ENEMY': (1, lib.f_not_of_teams.__name__, 'self.hg, None'),
    'ALLY': (1, lib.f_of_teams.__name__, 'self.hg, None'),
    'IN_RANGE': (2, lib.f_position_in_ring.__name__, 'self.x, self.y, {cnodes_1}'),
    'OUT_OF_RANGE': (1, lib.f_position_out_of_circle.__name__, 'self.x, self.y, {cnodes_1}'),
    'SHIELD_LEVEL': (2, lib.f_shield_between_pct.__name__, '{d100nodes_1}'),
    'HEALTH_LEVEL': (2, lib.f_health_between_pct.__name__, '{d100nodes_1}'),
    'ME': (1, lib.f_has_uid.__name__, 'self.uid')
}

identifiers_map = {
    'BOT': (1, lib.i_bots.__name__, ''),
    'PORT': (1, lib.i_drop_ports.__name__, ''),
    'ARTIFACT': (1, lib.i_artifacts.__name__, ''),
}
