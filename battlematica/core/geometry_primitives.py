import numpy as np


def the_correct_turn(a_start, a_target):
    base_diff = a_target % 360 - a_start % 360
    reverse_diff = (base_diff - 360) % 360

    if reverse_diff == base_diff:
        reverse_diff = base_diff - 360

    if np.abs(reverse_diff) < np.abs(base_diff):
        return reverse_diff
    else:
        return base_diff


def angle(x, y, tx, ty):
    delta_x = tx - x
    delta_y = ty - y
    theta_radians = np.arctan2(delta_y, delta_x)
    return np.rad2deg(theta_radians)


def distance(x, y, tx, ty):
    delta_x = tx - x
    delta_y = ty - y
    return np.sqrt(delta_x**2 + delta_y**2)


def move_towards(x, y, tx, ty, speed):

    r = angle(x, y, tx, ty)

    dx = tx - x
    # dy = ty - y

    nx = x + speed * np.cos(np.deg2rad(r))
    ny = y + speed * np.sin(np.deg2rad(r))

    ndx = tx - nx
    # ndy = ty - ny

    if np.sign(dx) != np.sign(ndx):
        nx = tx
        ny = ty

    return nx, ny
