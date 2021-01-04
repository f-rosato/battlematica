from functools import wraps

import numpy as np

from battlematica.core.geometry_primitives import distance


def _selector(f):
    @wraps(f)
    def wrapped_f(elems):
        if len(elems) == 0:
            return None
        else:
            return f(elems)
    return wrapped_f


def s_closest_to_xy(x, y):

    @_selector
    def _s_closest_to_xy(elems):
        ds = np.min([distance(x, y, e['x'], e['y']) for e in elems])
        return [e for e in elems if distance(x, y, e['x'], e['y']) == ds][0]

    return _s_closest_to_xy


def s_farthest_from_xy(x, y):

    @_selector
    def _s_farthest_from_xy(elems):
        ds = np.max([distance(x, y, e['x'], e['y']) for e in elems])
        return [e for e in elems if distance(x, y, e['x'], e['y']) == ds][0]

    return _s_farthest_from_xy


def s_lowest_abs_health():  # absolute!

    @_selector
    def _s_lowest_abs_health(elems):
        ds = np.min([e['health'] for e in elems])
        return [e for e in elems if e['health'] == ds][0]
    return _s_lowest_abs_health


def s_lowest_abs_shield():  # absolute!

    @_selector
    def _s_lowest_abs_shield(elems):
        ds = np.min([e['shield'] for e in elems])
        return [e for e in elems if e['shield'] == ds][0]

    return _s_lowest_abs_shield