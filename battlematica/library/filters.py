import numpy as np

from ..core.geometry_primitives import the_correct_turn


# team

def f_of_teams(*acceptable_teams):
    def _f_of_teams(elems):
        return [x for x in elems if x['hg'] in acceptable_teams]

    return _f_of_teams


def f_not_of_teams(*unacceptable_teams):
    def _f_not_of_teams(elems):
        return [x for x in elems if x['hg'] not in unacceptable_teams]

    return _f_not_of_teams


# positional

def f_position_in_ring(x, y, r1, r2):
    def _f_position_in_ring(elems):
        inr2 = f_position_in_circle(x, y, r2)(elems)
        outr1 = f_position_out_of_circle(x, y, r1)(elems)
        return list(set(inr2).intersection(set(outr1)))

    return _f_position_in_ring


def f_position_in_rectangle(l, r, t, b):
    def _f_position_in_rectangle(elems):
        return [e for e in elems if l <= e['x'] <= r and b <= e['y'] <= t]

    return _f_position_in_rectangle


def f_position_in_circle(x, y, r):
    def _f_position_in_circle(elems):
        def e_in_c(e):
            x2 = e['x']
            y2 = e['y']
            return np.sqrt((x2 - x) ** 2 + (y2 - y) ** 2) <= r

        return [e for e in elems if e_in_c(e)]

    return _f_position_in_circle


def f_position_in_cone(x, y, angle, a_half_range):
    def _f_position_in_cone(elems):

        in_cone_elems = []
        for e in elems:
            e_angle = np.rad2deg(np.angle(e['x'] - x + 1j * (e['y'] - y)))

            if np.abs(the_correct_turn(angle, e_angle)) < a_half_range:
                in_cone_elems.append(e)
        return in_cone_elems

    return _f_position_in_cone


def f_position_out_of_circle(x, y, r):
    def _f_position_out_of_circle(elems):

        pic = f_position_in_circle(x, y, r)
        return [e for e in elems if e not in pic(elems)]

    return _f_position_out_of_circle


def f_position_out_of_rectangle(l, r, t, b):
    def _f_position_out_of_rectangle(elems):

        pir = f_position_in_rectangle(l, r, t, b)
        return list(set(elems) - set(pir(elems)))

    return _f_position_out_of_rectangle


# health

def f_health_between(h1, h2):
    def _f_health_between(elems):
        return [e for e in elems if h1 <= e['health'] <= h2]

    return _f_health_between


def f_shield_between(s1, s2):
    def _f_shield_between(elems):
        return [e for e in elems if s1 <= e['shield'] <= s2]

    return _f_shield_between


def f_health_between_pct(h1, h2):
    def _f_health_between_pct(elems):
        return [e for e in elems if h1 <= e['health'] / e['max_health'] <= h2]

    return _f_health_between_pct


def f_shield_between_pct(s1, s2):
    def _f_shield_between_pct(elems):
        return [e for e in elems if s1 <= e['shield'] / e['max_shield'] <= s2]

    return _f_shield_between_pct


# generic properties

def f_property_between(prop, p1, p2):
    def _f_property_between(elems):
        return [e for e in elems if p1 <= e[prop] <= p2]

    return _f_property_between


# behavioral

def f_has_target(x, y):
    def _f_has_target(elems):
        return [e for e in elems if e['tx'] is not None and np.isclose(e['tx'], x) and np.isclose(e['ty'], y)]

    return _f_has_target


def f_current_action(ca):
    def _f_current_action(elems):
        return [e for e in elems if e['ca'] == ca]

    return _f_current_action


def f_is_not_carrying():
    def _f_is_not_carrying(elems):
        return [e for e in elems if not e['is_carrying']]

    return _f_is_not_carrying


def f_is_carrying():
    def _f_is_carrying(elems):
        return [e for e in elems if e['is_carrying']]

    return _f_is_carrying
