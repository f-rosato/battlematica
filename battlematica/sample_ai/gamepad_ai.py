import math
import threading as thr

from inputs import get_gamepad

import battlematica.library as lib
from battlematica import StateQuerier

DEAD_D = .3

LOCK_HALF_ANGLE = 30


def gamepad_ai(self, state):

    """
    This AI actually is an interface to a gamepad through the inputs module.
    The first gamepad found available will be read for input.
    For this to work as expected, the GameDisplayProcess must be initialized with sync=True.

    You move with the left stick.

    Pressing RL puts you in "pick/drop mode", i.e., with RL pressed your movement direction
    will snap to artifacts and drop ports - and you will pick and drop the artifact.
    If RL is released while carrying an artifact, it will be dropped immediately.

    You stop and shoot with B.
    You stop and loiter with X.

    """

    # assign gamepad
    if not hasattr(self, 'gamepad_started') or not self.gamepad_started:
        self.gamepad_started = True
        self.gamepad = Gamepad()

    intent, raw_angle_deg = self.gamepad.raw_action

    if raw_angle_deg is None:
        return 'loiter', self.tx, self.ty

    raw_angle = math.radians(raw_angle_deg)

    sx = self.x
    sy = self.y

    sq = StateQuerier(state)

    tx_def = sx + math.cos(raw_angle) * self.walk_speed * 2
    ty_def = sy + math.sin(raw_angle) * self.walk_speed * 2

    # action conversion
    if intent == 'grab' and self.carry is None:
        action = 'pick'
    elif intent == 'grab' and self.carry is not None:
        action = 'drop'
    else:
        action = intent

    # insta drop
    if intent != 'grab' and self.carry is not None:
        return 'drop', sx, sy

    # action management
    if action == 'loiter':
        return 'loiter', tx_def, ty_def
    elif action == 'move':
        return 'move', tx_def, ty_def
    elif action == 'shoot':
        ne = sq(lib.i_bots(),
                lib.f_not_of_teams(self.hg),
                lib.f_position_in_cone(sx, sy, raw_angle_deg, LOCK_HALF_ANGLE),
                lib.s_closest_to_xy(sx, sy))

        if ne is not None:
            return 'shoot', ne['x'], ne['y']
        else:
            return 'shoot', sx + math.cos(raw_angle) * self.bullet_range, sy + math.sin(raw_angle) * self.bullet_range

    elif action == 'pick':
        ne = sq(lib.i_artifacts(),
                lib.f_of_teams(self.hg, None),
                lib.f_position_in_cone(sx, sy, raw_angle_deg, LOCK_HALF_ANGLE),
                lib.s_closest_to_xy(sx, sy))

        if ne is not None:
            return 'pick', ne['x'], ne['y']
        else:
            return 'pick', tx_def, ty_def

    elif action == 'drop':
        ne = sq(lib.i_drop_ports(),
                lib.f_of_teams(self.hg, None),
                lib.f_position_in_cone(sx, sy, raw_angle_deg, LOCK_HALF_ANGLE),
                lib.s_closest_to_xy(sx, sy))

        if ne is not None:
            return 'drop', ne['x'], ne['y']
        else:
            return 'drop', tx_def, ty_def


class Gamepad:

    def __init__(self, daemonic=True):
        self.current_intent = 'move'
        self.axis_x = 0
        self.axis_y = 0

        self.axis_rz_pressed = 0

        self.action_angle_raw = None
        self.poll_thread = thr.Thread(target=self._constant_watcher)
        self.poll_thread.daemon = daemonic
        self.poll_thread.start()

    @property
    def raw_action(self):
        return self.current_intent, self.action_angle_raw

    def _constant_watcher(self):

        def assign_intent(a, s):
            nonlocal self
            if s == 1:
                self.current_intent = a
            elif s == 0:
                self.current_intent = 'move'

        while True:
            events = get_gamepad()
            for event in events:

                # movement of target point
                if event.code == 'ABS_X':
                    self.axis_x = event.state/32768

                if event.code == 'ABS_Y':
                    self.axis_y = event.state/32768

                direction_vector_l = math.sqrt(self.axis_x**2 + self.axis_y**2)
                if direction_vector_l < DEAD_D:
                    self.action_angle_raw = None
                else:
                    self.action_angle_raw = math.degrees(math.atan2(self.axis_y, self.axis_x))

                # grabbing intent
                if event.code == 'ABS_RZ':
                    assign_intent('grab', int(event.state > 0))

                # shoots
                if event.code == 'BTN_EAST':
                    assign_intent('shoot', event.state)

                # loiters explicitly
                if event.code == 'BTN_WEST':
                    assign_intent('loiter', event.state)


if __name__ == '__main__':
    import time

    g = Gamepad(daemonic=False)

    while True:
        time.sleep(0.5)
        print(g.raw_action)
