import numpy as np


# team
def f_of_teams(elems, *acceptable_teams):
    return [x for x in elems if x['hg'] in acceptable_teams]


def f_not_of_teams(elems, *unacceptable_teams):
    return [x for x in elems if x['hg'] not in unacceptable_teams]


# positional
def f_position_in_ring(elems, x, y, r1, r2):
    inr2 = f_position_in_circle(elems, x, y, r2)
    outr1 = f_position_out_of_circle(elems, x, y, r1)
    return list(set(inr2).intersection(set(outr1)))


def f_position_in_rectangle(elems, l, r, t, b):
    return [e for e in elems if l <= e['x'] <= r and b <= e['y'] <= t]


def f_position_in_circle(elems, x, y, r):

    def e_in_c(e):
        x2 = e['x']
        y2 = e['y']
        return np.sqrt((x2 - x)**2 + (y2 - y)**2) <= r

    return [e for e in elems if e_in_c(e)]


def f_position_out_of_circle(elems, x, y, r):
    return [e for e in elems if e not in f_position_in_circle(elems, x, y, r)]


def f_position_out_of_rectangle(elems, l, r, t, b):
    return list(set(elems) - set(f_position_in_rectangle(elems, l, r, t, b)))


# health
def f_health_between(elems, h1, h2):
    return [e for e in elems if h1 <= e['health'] <= h2]


def f_shield_between(elems, s1, s2):
    return [e for e in elems if s1 <= e['shield'] <= s2]


def f_health_between_pct(elems, h1, h2):
    return [e for e in elems if h1 <= e['health']/e['max_health'] <= h2]


def f_shield_between_pct(elems, s1, s2):
    return [e for e in elems if s1 <= e['shield']/e['max_shield'] <= s2]


# generic properties
def f_property_between(elems, prop, p1, p2):
    return [e for e in elems if p1 <= e[prop] <= p2]


# behavior
def f_has_target(elems, x, y):
    return [e for e in elems if e['tx'] is not None and
            np.isclose(e['tx'], x) and np.isclose(e['ty'], y)]


def f_current_action(elems, ca):
    return [e for e in elems if e['ca'] == ca]


def f_is_not_carrying(elems):
    return [e for e in elems if not e['is_carrying']]


def f_is_carrying(elems):
    return [e for e in elems if e['is_carrying']]