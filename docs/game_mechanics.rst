Game Mechanics
==============

Time and space
--------------

The smallest unit of time is the "tick" - the interval between one frame (a state update) and the next. Similarly, we will refer to the lenght unit as "u". In the built-in graphics display, one "u" corresponds to one unit in the arcade_ package.

.. _arcade: https://arcade.academy/

Artifacts and drop ports
------------------------

In the default form of the game, bots compete over :ref:`Artifact` s, inert objects that the Bots can pick up and drop. When an :ref:`Artifact` is dropped in correspondance with a :ref:`DropPort`, the team scores one point.
In Battlematica, there are neutral Artifacts and Drop Ports, that can be used by both teams; but you can choose to have team-specific Artifacts and Drop Ports, that can be used only by a specific team.

The shield
----------

Bots have a shield. Think of automatically rechargeable HP. The shield gets depleted as damage is taken continuously, but recharges up to its max level when damage is not taken for a little bit. Health HP will start to be removed only after the shield is depleted. The only way to inflict permanent damage, therefore, is to hit a bot consistently enough to not give time to its shield to recharge enough to compensate the damage. Quantity, recharging speed, recharging dead time can vary and are among the initialization parameters of a :ref:`Bot`.


Actions
-------

Bots can do one of five things at a time.
 - **move**: the bot will move to a target point.
 - **shoot**: the bullet will shoot bullets to a target point.
 - **pick**: the bot behaves like in move mode, but when the target point is reached, if there is an artifact at that point, the bot picks it up.
 - **drop**: the bot behaves like in move mode, but when the target point is reached, if the bot is carrying an Artifact, it drops it. If the Artifact is dropped over a DropPort, it is absorbed and the bot's team scores a point.
 - **loiter**: the bot stands where it is and rotates to face a target point.

In Battlematica, you write AIs that based on the :ref:`Game State` choose which of the five actions to perform and the relative target. See :ref:`Writing AIs`.