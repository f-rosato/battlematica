from functools import wraps

import numpy as np

from battlematica.core.geometry_primitives import distance
from .partializer import partializable


def _selector(f):
    @wraps(f)
    def wrapped_f(elems, *args):
        if len(elems) == 0:
            return None
        else:
            return f(elems, *args)
    return wrapped_f


@partializable
@_selector
def s_closest_to_xy(elems, x, y):
    ds = np.min([distance(x, y, e['x'], e['y']) for e in elems])
    return [e for e in elems if distance(x, y, e['x'], e['y']) == ds][0]


@partializable
@_selector
def s_farthest_from_xy(elems, x, y):
    ds = np.max([distance(x, y, e['x'], e['y']) for e in elems])
    return [e for e in elems if distance(x, y, e['x'], e['y']) == ds][0]
