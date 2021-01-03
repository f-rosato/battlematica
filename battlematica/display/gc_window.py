from itertools import product
from time import sleep

import arcade as ad
import numpy as np

from battlematica.core.constants import PERIOD_OVER_TOKEN
from .sprite_m90 import SpriteM90

SCREEN_TITLE = "Bots that beat the shit out of each other"


# this sprite uses angles with the convention that 0 points right


class GCWindow(ad.Window):
    def __init__(self, X, Y, q, asset_container, sync_signal=None, update_rate=1 / 60):
        super().__init__(X, Y, SCREEN_TITLE)
        self.limits = [X, Y]
        self.ids = []
        self.sprite_list = ad.SpriteList()
        self.blast_list = ad.SpriteList()
        self.artifact_list = ad.SpriteList()
        self.dp_list = ad.SpriteList()
        self.spritedict = {}
        self.traces = []
        self.bar_drawers = []
        self.q = q
        self.background = None
        self.is_over = False
        self.ur = update_rate
        self.ac = asset_container
        self.current_score = {}
        self.current_tick = 0
        self.sync_signal = sync_signal

    def setup(self):
        self.background = ad.load_texture(self.ac.background())
        self.set_mouse_visible(False)
        self.set_update_rate(self.ur)

    def on_update(self, delta_time: float):

        if self.is_over:
            raise ValueError()

        disp_state = self.q.get()
        # CLOSING
        if disp_state == PERIOD_OVER_TOKEN:
            self.is_over = True
            sleep(0.5)  # not to be abrupt
            ad.finish_render()
            self.clear()
            self.close()
            return

        present_ids = []

        # update score
        sc = disp_state['score']
        self.current_score = sc
        self.current_tick = disp_state['tick']

        # update bots
        for b in disp_state['bots']:
            g = b['graphics']
            team = b['hg']
            present_ids.append(b['id'])
            if b['id'] not in self.ids:
                self.ids.append(b['id'])
                bot_sprite = SpriteM90(self.ac.bot(team, g['body_type']), g['size'])
                self.sprite_list.append(bot_sprite)
                self.spritedict[b['id']] = bot_sprite
            else:
                bot_sprite = self.spritedict[b['id']]

            bot_sprite.center_x = b['x']
            bot_sprite.center_y = b['y']
            bot_sprite.angle = b['r']

            if b['ca'] != 'loiter':
                self.traces.append((b['x'], b['y'], b['tx'], b['ty'], ad.color.RED_DEVIL, 2))
            bd = self.make_bar_drawer(b)
            self.bar_drawers.append(bd)

        # update artifacts
        for arty in disp_state['artifacts']:
            team = arty['hg']
            present_ids.append(arty['id'])
            if arty['id'] not in self.ids:
                self.ids.append(arty['id'])
                arti_sprite = SpriteM90(self.ac.artifact(team), .55)
                self.artifact_list.append(arti_sprite)
                self.spritedict[arty['id']] = arti_sprite
            else:
                arti_sprite = self.spritedict[arty['id']]

            arti_sprite.center_x = arty['x']
            arti_sprite.center_y = arty['y']
            arti_sprite.angle = arty['r']

        # update dp
        for dp in disp_state['drop_ports']:
            present_ids.append(dp['id'])
            if dp['id'] not in self.ids:
                team = dp['hg']
                self.ids.append(dp['id'])
                drop_sprite = SpriteM90(self.ac.drop_port(team), .6)
                self.dp_list.append(drop_sprite)
                self.spritedict[dp['id']] = drop_sprite
            else:
                drop_sprite = self.spritedict[dp['id']]

            drop_sprite.center_x = dp['x']
            drop_sprite.center_y = dp['y']
            drop_sprite.angle = dp['r']

        # update bullets
        for blt in disp_state['bullets']:
            present_ids.append(blt['id'])
            if blt['id'] not in self.ids:
                self.ids.append(blt['id'])
                bullet_sprite = SpriteM90(self.ac.bullet(blt['sprite']), blt['size'])
                self.sprite_list.append(bullet_sprite)
                self.spritedict[blt['id']] = bullet_sprite
            else:
                bullet_sprite = self.spritedict[blt['id']]
            bullet_sprite.center_x = blt['x']
            bullet_sprite.center_y = blt['y']
            bullet_sprite.angle = blt['r']

        # draw blasts
        for d_blt in disp_state['d_bullets']:
            blast_id = d_blt['id'] + 'blast'
            present_ids.append(blast_id)
            if blast_id not in self.ids:
                self.ids.append(blast_id)
                blast_sprite = SpriteM90(self.ac.blast(d_blt['blast_sprite']), .5)
                self.blast_list.append(blast_sprite)
                self.spritedict[blast_id] = blast_sprite
            else:
                raise ValueError()
            blast_sprite.center_x = d_blt['x']
            blast_sprite.center_y = d_blt['y']
            blast_sprite.angle = d_blt['r']

        # remove old sprites
        diff_ids = set(self.ids) - set(present_ids)
        for disappeared in diff_ids:
            self.spritedict[disappeared].kill()  # removes it from spritelists
            del self.spritedict[disappeared]
        self.ids = present_ids

    @staticmethod
    def make_bar_drawer(bot_params):
        cx = bot_params['x']
        cy = bot_params['y']
        he = bot_params['health'] / bot_params['max_health']
        sh = bot_params['shield'] / bot_params['max_shield']
        re = bot_params['reload_time_pct']

        heigth = 5

        width = 80
        x_base = cx - width / 2

        h_width = width * he
        s_width = width * sh
        r_width = width * re

        health_base_y = 35
        shield_base_y = 42
        reload_base_y = - 40

        def bar_drawer():
            # helf
            ad.draw_lrtb_rectangle_filled(x_base, x_base + width, cy + health_base_y + heigth, cy + health_base_y,
                                          ad.color.BLACK)

            ad.draw_lrtb_rectangle_filled(x_base, x_base + h_width, cy + health_base_y + heigth, cy + health_base_y,
                                          ad.color.RED)

            # shield
            ad.draw_lrtb_rectangle_filled(x_base, x_base + width, cy + shield_base_y + heigth, cy + shield_base_y,
                                          ad.color.BLACK)

            ad.draw_lrtb_rectangle_filled(x_base, x_base + s_width, cy + shield_base_y + heigth, cy + shield_base_y,
                                          ad.color.WHITE)

            # reload
            ad.draw_lrtb_rectangle_filled(x_base, x_base + width, cy + reload_base_y + heigth, cy + reload_base_y,
                                          ad.color.BLACK)

            ad.draw_lrtb_rectangle_filled(x_base, x_base + r_width, cy + reload_base_y + heigth, cy + reload_base_y,
                                          ad.color.CANARY_YELLOW)

        return bar_drawer

    def on_draw(self):
        """ Draw everything """

        if self.is_over:
            return

        ad.start_render()

        # background
        for x, y in product(np.arange(0, self.limits[0], self.ac.background_L()), np.arange(0, self.limits[1],
                                                                                            self.ac.background_L())):
            ad.draw_lrwh_rectangle_textured(x + 0, y + 0, self.ac.background_L(), self.ac.background_L(),
                                            self.background)

        # draw drop ports
        self.dp_list.draw()

        # draw tracelines
        for t in self.traces:
            ad.draw_line(*t)
        self.traces.clear()

        # draw sprites
        self.sprite_list.draw()
        self.blast_list.draw()
        self.artifact_list.draw()

        # draw bars
        for bd in self.bar_drawers:
            bd()
        self.bar_drawers.clear()

        # draw score
        score_str = '\n'.join([f'team {t}: {s}' for t, s in self.current_score.items()])
        ad.draw_text(score_str, 30, self.height - 30*len(self.current_score), ad.color.WHITE, 16)

        # draw tick
        tick_str = f'tick: {self.current_tick}'
        ad.draw_text(tick_str, 30, 30, ad.color.DARK_YELLOW, 14)

        # set signal
        if self.sync_signal is not None:
            self.sync_signal.set()

