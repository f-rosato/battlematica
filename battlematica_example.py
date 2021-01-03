from battlematica import *
from battlematica.sample_ai import shoot_then_harvest


TEAM_1 = 1
TEAM_2 = 2
TEAM_NEUTRAL = None

FIELD_SIZE = [800, 700]

BOT_GRAPHICS = {
      "body_type": 2,
      "bullet_type": 3,
      "bullet_size": 0.7,
      "bullet_blast_type": 1
  }

if __name__ == '__main__':

    ### example of a two-bot battle over 4 artifacts:
    ### 2 neutral and 1 team specific each.

    # declare bot_1 and bot_2 with default parameters at their respective positions
    bot_1 = Bot(200, 200, 45, TEAM_1, graphics=BOT_GRAPHICS)
    bot_1.set_ai(shoot_then_harvest)

    bot_2 = Bot(600, 500, 45 + 180, TEAM_2, graphics=BOT_GRAPHICS)
    bot_2.set_ai(shoot_then_harvest)

    # in order to prevent symmetry, we alter the attributes of bot_2
    bot_2.max_shield = 300.0  # better than default
    bot_2.bullet_dmg = 60  # worse than default

    # artifacts
    artifact_low = Artifact(400, 100, TEAM_2)
    artifact_high = Artifact(400, 600, TEAM_1)
    artifact_ml = Artifact(350, 350, TEAM_NEUTRAL)
    artifact_mr = Artifact(450, 350, TEAM_NEUTRAL)

    # declare a neutral drop port in the middle
    drop_port = DropPort(400, 350, TEAM_NEUTRAL)

    # instantiate the engine and initialize the game
    engine = GameEngine()
    engine.init_game(*FIELD_SIZE,
                     [bot_1, bot_2],
                     [artifact_high, artifact_low, artifact_ml, artifact_mr],
                     [drop_port])

    # we want to display the game, so we use a BMDisplayProcess
    displayer = GameDisplayProcess(engine, speed=1.0)
    displayer.start()

    # run the game
    _final_score = engine.run_game(until_tick=1200)

    # end the displayer process cleanly
    displayer.join()
