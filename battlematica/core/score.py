from .geometry_primitives import distance
from .constants import PORT_TOLERANCE


def default_score(state):
    prev_score = state['score']
    new_score = prev_score
    for da in state['d_artifacts']:
        ax = da['x']
        ay = da['y']

        if da['hg'] is None:
            team_c = da['last_touch']
        else:
            team_c = da['hg']

        for dp in state['drop_ports']:
            dx = dp['x']
            dy = dp['y']

            if dp['hg'] is None or dp['hg'] == team_c:

                if distance(ax, ay, dx, dy) < PORT_TOLERANCE:
                    new_score[team_c] += 1

    return new_score
