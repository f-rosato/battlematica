.. _standalone:

Using files
===========

The game can be initialized with files, using the method `init_from_files`.
Here we will see how to do it.


Write a bot file
''''''''''''''''

The first thing you will want to do is to define one or more bot .json files. Each file defines a class of bot and contains all the information about the physical properties (the body of the bot). The keys are essentially the same as the arguments passed to `Bot.__init__` (see :ref:`Bot`). A couple of example files are included in the source code. Here's one, `balanced_bot.json`.

.. literalinclude:: ../sample_bots/balanced_bot.json
  :language: JSON

graphics bot settings
---------------------

This section of the json file is used to define properties that have no effect on the progress and outcome of the game, but are included in the state just for use inside the graphical display. It can be left empty if the engine is used without any graphical display attached; only the graphical display looks for those keys. The keys ending in `type` are integers representing the file to select in the archive described in :ref:`The asset archive`.

      - `body_type`: integer that selects the sprite for the bot as `/bots/team_*/...{body_type}.png`
      - `bullet_type`: integer that selects the sprite for the bullet fired by the bot as `/bullets/...{bullet_type}.png`
      - `bullet_blast_type`: integer that selects the sprite for the bullet blast as `/blasts/...{blast_type}.png`
      - `bullet_size`: floating point scaling factor for the bullet sprite

Write a game .json file
'''''''''''''''''''''''

TBD

Start the game
''''''''''''''

You can start a game with files by using the dedicated method:
TBD

Or you can also start the game from the shell by running the run_game.py script:
TBD