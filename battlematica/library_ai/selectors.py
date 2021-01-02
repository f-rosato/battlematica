import numpy as np
from functools import wraps
from battlematica.core.geometry_primitives import distance


def _selector(f):
    @wraps(f)
    def wrapped_f(elems, *args):
        if not elems:
            return None
        else:
            return f(elems, *args)
    return wrapped_f


@_selector
def s_closest_to_xy(elems, x, y):
    ds = np.min([distance(x, y, e['x'], e['y']) for e in elems])
    return [e for e in elems if distance(x, y, e['x'], e['y']) == ds][0]


@_selector
def s_farthest_from_xy(elems, x, y):
    ds = np.max([distance(x, y, e['x'], e['y']) for e in elems])
    return [e for e in elems if distance(x, y, e['x'], e['y']) == ds][0]
