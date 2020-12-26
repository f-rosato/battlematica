import numpy as np

from battlematica.core.geometry_primitives import distance


def closest_to_xy(elems, x, y):
    ds = np.min([distance(x, y, e['x'], e['y']) for e in elems])
    return [e for e in elems if distance(x, y, e['x'], e['y']) == ds][0]


def farthest_from_xy(elems, x, y):
    ds = np.max([distance(x, y, e['x'], e['y']) for e in elems])
    return [e for e in elems if distance(x, y, e['x'], e['y']) == ds][0]
