API reference
=============

GameEngine
----------

.. autoclass:: battlematica.GameEngine
   :members:
   :special-members:
   :exclude-members: __weakref__


GameDisplayProcess
------------------

.. autoclass:: battlematica.GameDisplayProcess
   :members:
   :special-members:
   :exclude-members: __weakref__

Bot
---

.. autoclass:: battlematica.Bot
   :members:
   :special-members:
   :exclude-members: __weakref__

Artifact
------------------

.. autoclass:: battlematica.Artifact
   :members:
   :special-members:
   :exclude-members: __weakref__

DropPort
------------------

.. autoclass:: battlematica.DropPort
   :members:
   :special-members:
   :exclude-members: __weakref__


StateQuerier
------------

.. autoclass:: battlematica.StateQuerier
   :members:
   :special-members:
   :exclude-members: __weakref__


library
-------

The library submodule contains a collections of higher level functions used in writing AIs together with a StateQuerier. The functions are divided in identifiers, filters and selectors.

    - **identifiers** have prefix `i_` and select the class of objects you want to query: bots, artifacts or drop ports.
    - **filters** have prefix `f_` and are functions that narrow down a list of objects. A sequence of filters is applied to the totality of the objects contained in the :ref:`Game State` in order to get a list of suitable objects.
    - **selectors** have prefix `s_` and their purpose is to select exactly one element from a list according to the minimization or maximization of some criterion; if a selector is applied to an already empty list, the selector returns `None`.

.. automodule:: battlematica.library
   :imported-members:
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: distance, wraps, the_correct_turn


battlang
--------

.. automodule:: battlematica.battlang
   :imported-members:
   :undoc-members:
   :members:
