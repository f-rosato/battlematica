import importlib.util
import json
import os.path
from copy import deepcopy
from multiprocessing import Queue, Event

import numpy as np

from .constants import PERIOD_OVER_TOKEN, BLAST_RADIUS, SEED, PORT_TOLERANCE
from .g_artifact import Artifact
from .g_bot import Bot
from .g_bullet import _Bullet
from .g_drop_port import DropPort
from .geometry_primitives import distance
from .score import default_score


class GameEngine:

    def __init__(self):

        """The GameEngine is the object responsible for advancing the state of the game
        and generating the state snapshots."""

        self.X = 0
        self.Y = 0
        self.bots = []
        self.bullets = []
        self.disappearing_bullets = []
        self.disappearing_bots = []
        self.artifacts = []
        self.disappearing_artifacts = []
        self.carried_artifacts = []
        self.drop_ports = []
        self.tick = 0

        self.state_queues = []
        self.sync_signals = []

        self.score = {}
        self.score_fn = None

    @property
    def state(self):

        """The state of the game, that is a dict containing information about
        all the game objects."""

        st = {
            'bots': [],
            'd_bots': [],
            'bullets': [],
            'd_bullets': [],
            'artifacts': [],
            'd_artifacts': [],
            'drop_ports': [],
            'score': deepcopy(self.score),
            'tick': self.tick
        }

        for b in self.bots:
            st['bots'].append(b.state)

        for b in self.bullets:
            st['bullets'].append(b.state)

        for b in self.artifacts:
            st['artifacts'].append(b.state)

        for b in self.disappearing_bots:
            st['d_bots'].append(b.state)

        for b in self.disappearing_bullets:
            st['d_bullets'].append(b.state)

        for b in self.disappearing_artifacts:
            st['d_artifacts'].append(b.state)

        for b in self.drop_ports:
            st['drop_ports'].append(b.state)

        return st

    def give_state_queue(self):

        """Creates and returns a Queue in which the display state snapshots will be put
        during the run of the game."""

        q = Queue()
        self.state_queues.append(q)
        return q

    def give_sync_signal(self):

        """Creates and returns a sync signal that blocks the execution of the next tick
        until it is set again."""

        e = Event()
        self.sync_signals.append(e)
        return e

    def _bots_in_radius(self, x, y, r):
        for bot in self.bots:
            if distance(x, y, bot.x, bot.y) < r:
                yield bot

    def _artifacts_near(self, x, y):
        for a in self.artifacts:
            if distance(x, y, a.x, a.y) < PORT_TOLERANCE:
                yield a

    def _drop_ports_near(self, x, y):
        for dp in self.drop_ports:
            if distance(x, y, dp.x, dp.y) < PORT_TOLERANCE:
                yield dp

    @staticmethod
    def _load_folder_json(folder, basename):
        fn = os.path.join(folder, basename + '.json')
        with open(fn, 'r') as jf:
            cn = json.load(jf)
        return cn

    @staticmethod
    def _load_folder_function(folder, name):
        module_name = os.path.join(folder, name + '.py')
        spec = importlib.util.spec_from_file_location(name, module_name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, name)

    def init_from_files(self, main_game_file):

        """Initializes a game from a json gamefile."""

        # load main game conf
        with open(main_game_file, 'r') as gf:
            game_conf = json.load(gf)

        # build lists from game conf
        bot_list = []
        for _bot_name, bot_conf in game_conf['bots'].items():

            # the parameters file and the AI functions have to be substituted
            bot = bot_conf
            botpars = self._load_folder_json(game_conf['bots_folder'], bot['file'])
            del bot['file']
            botai = self._load_folder_function(game_conf['ai_folder'], bot['ai'])

            xyr = bot['xyr']
            hg = bot['team']
            bot = Bot(*xyr, hg, **botpars)
            bot.set_ai(botai)
            bot_list.append(bot)

        artifact_list = []
        for arp in game_conf['artifacts']:
            ar = Artifact(arp['xy'][0], arp['xy'][1], arp['team'])
            artifact_list.append(ar)

        drop_port_list = []
        for drp in game_conf['drop_ports']:
            dp = DropPort(drp['xy'][0], drp['xy'][1], drp['team'])
            drop_port_list.append(dp)

        # seed
        if 'seed' in game_conf.keys():
            seed = game_conf['seed']
        else:
            seed = SEED

        # instantiate game engine
        self.init_game(*game_conf['battlefield_size'], bot_list, artifact_list, drop_port_list, seed)

    def init_game(self, field_width, field_height, bot_list, artifact_list, drop_port_list, seed=SEED,
                  score_fn=default_score):

        """Initializes a game. The arguments describe the initial condition of the game.

        :param field_width: width of the game arena in u (units-pixels)
        :param field_height: heigth of the game arena in u (units-pixels)
        :param bot_list: a list of dicts containing the attributes of the bots
        :param artifact_list: a list of dicts containing the attributes of the artifacts
        :param drop_port_list: a list of dicts containing the attributes of the drop ports
        :param seed: random seed for np.random. A fixed seed will be used if not passed.

        """

        self.X = field_width
        self.Y = field_height
        self.score_fn = score_fn
        np.random.seed(seed)

        for botj in bot_list:
            self.score[botj.hg] = 0  # activates the keys
            self.bots.append(botj)

        for arp in artifact_list:
            self.artifacts.append(arp)

        for drp in drop_port_list:
            self.drop_ports.append(drp)

    def run_game(self, until_tick):

        """Advances the game until a certain tick number.

        :param until_tick: the tick until which to simulate

        """

        while self.tick < until_tick:

            # wait for sync signals, if any
            for e in self.sync_signals:
                e.wait()
                e.clear()

            self.tick += 1
            print(self.tick)

            new_bullets = []
            self.disappearing_bots.clear()
            self.disappearing_bullets.clear()
            self.disappearing_artifacts.clear()

            # do the bots

            # decision and carry
            for bot in self.bots:
                bot._think(self.state)

            for bot in self.bots:
                stuff = bot._chores(self.X, self.Y)

                for action in stuff:
                    a, params = action

                    if a == 'disappear':
                        self.disappearing_bots.append(bot)

                    elif a == 'fire_round':
                        new_bullets.append(_Bullet(**bot._bullet_params()))

                    elif a == 'pick':
                        for ar in self._artifacts_near(bot.x, bot.y):
                            if ar in self.carried_artifacts:
                                continue  # no stealing

                            if ar.hg is not None and ar.hg != bot.hg:
                                continue

                            bot.carry = ar
                            ar.last_touch = bot.hg
                            ar.is_carried = True
                            self.carried_artifacts.append(ar)

                    elif a == 'drop':
                        ar = bot.carry
                        # note: we only check artifact adsorption here.
                        # the logic is that if an artifact is on a drop port, it MUST be because
                        # a bot brought it there. But be careful if the mechanics is changed
                        # (remotely moving artifacts, etc)

                        if ar is not None:
                            for dp in self._drop_ports_near(ar.x, ar.y):
                                if ar.hg == dp.hg or dp.hg is None:
                                    self.disappearing_artifacts.append(ar)
                                    self.carried_artifacts.remove(ar)
                                    ar.is_carried = False
                                    bot.carry = None
                                    break

            for ar in self.disappearing_artifacts:
                self.artifacts.remove(ar)

            for b in self.disappearing_bots:
                self.bots.remove(b)

            # do the bullets
            for bullet in self.bullets:
                stuff = bullet._chores(self.X, self.Y)
                for action in stuff:
                    a, params = action

                    if a == 'disappear':
                        self.disappearing_bullets.append(bullet)

                    elif a == 'explode':
                        for b in self._bots_in_radius(bullet.x, bullet.y, BLAST_RADIUS):
                            if b.hg != bullet.hg:  # not friendly fire
                                b._take_dmg(bullet.dmg)
                                break
                        self.disappearing_bullets.append(bullet)

            for b in self.disappearing_bullets:
                self.bullets.remove(b)

            self.bullets.extend(new_bullets)

            # scoring
            pst = self.state
            self.score = self.score_fn(pst)

            st = self.state

            for q in self.state_queues:
                q.put(st)

        for q in self.state_queues:
            q.put(PERIOD_OVER_TOKEN)

        return self.score
