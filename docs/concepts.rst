General concepts
================

In this page a few fundamental concepts of how Battlematica works are explained briefly.
Battlematica is not a lot of code, so if you want a finer and more technical understanding,
the easiest thing to do is probably to just refer to the source.


Game mechanics
''''''''''''''

Time and space
--------------

The smallest unit of time is the "tick" - the interval between one frame (a state update) and the next.
Similarly, we will refer to the lenght unit as "u". In the built-in graphics display, one "u" corresponds to one unit
in the arcade_ package.

.. _arcade: https://arcade.academy/

Artifacts and drop ports
------------------------

TBD

The shield
----------

TBD


Architecture
''''''''''''

The :ref:`GameEngine` is a fixed time simulator that produces consecutive snapshots of the state of the game.
The game engine is decoupled from the graphics. It has a method `GameEngine.give_state_queue()` to create and return a `multiprocessing.Queue` in which it
puts the state snapshots as they are produced. The built-in graphics :ref:`GameDisplayProcess` is a separate `Process` that displays these states as "frames" of the game.
The :ref:`GameEngine`, therefore, can be used "headless" if for any reason (training reiforcement learning,
sampling results, etc.) games can/should be run in batch. For the analysis-oriented users, grabbing a `Queue`
from the game engine with `GameEngine.give_state_queue()` is the preferred way to get all the info you could possibly want from the simulation
in order to do analyses to any desired level of detail.