Writing AIs
===========

.. Tip::

    It is highly suggested that you read :ref:`Game Mechanics` and :ref:`Game State` before this section.

Writing AIs is the core task in Battlematica. To write an AI, you must write a function of this form:


.. code-block:: python

    def my_ai(self: Bot, state: dict):

        # do stuff

        return action, target_x, target_y

`action` is a string, one of the ones listed in :ref:`Actions`.
`target_x`, `target_y` are floats, representing the target of the action.

Once you have your function, you assign it to a `Bot` instance through the metod `set_ai`.

If the function happens to return `None` (e.g., when the end of the function is reached without hitting a `return` statement at all), the Bot will loiter in place.

You are free to write whatever you like inside the function! You can write bots that use machine learning, neural networks...

You can also write AIs according to a logic similar to the one found in Gladiabots.  The Gladiabots philosophy is great and strikes a good balance between fun, power, interpretability and conceptualization ease. Very generally, you write in descending priority and according to a conditional control flow a series of object selections and, if a suitable element is found, execute actions on it.

We'll use a very basic AI, `shoot_retire` (included in the :ref:`sample_ai` submodule) to illustrate this method. The purpose of this AI is simply to go towards the nearest enemy and shoot at it. When the shield level drops under 20%, the Bot will flee away from the nearest enemy that is targeting it.

.. literalinclude:: ../battlematica/sample_ai/shoot_retire.py
  :language: python

You operate by using the functions found in the :ref:`library` submodule and :ref:`StateQuerier`. These are used to get one or more objects from the field (enemies, artifacts, allies...) according to a set of criterions that "sieve" the state. The functions contained in the :ref:`library` submodule are divided in identifiers, filters and selectors.

    - **identifiers** have prefix `i_` and select the class of objects you want to query: bots, artifacts or drop ports.
    - **filters** have prefix `f_` and are functions that narrow down a list of objects. A sequence of filters is applied to the totality of the objects contained in the :ref:`Game State` in order to get a list of suitable objects.
    - **selectors** have prefix `s_` and their purpose is to select exactly one element from a list according to the minimization or maximization of some criterion; if a selector is applied to an already empty list, the empty list just passes through.

A sequence of functions from these are passed as arguments of calls to the instance of :ref:`StateQuerier`.

.. Important::

    You must begin with an identifier, then apply zero or more filters, and optionally finish with a selector.

.. Important::

    If you do not finish with a selector, you are returned a list of states of objects, possibly empty. If you finish with a selector, you are returned either the selected object state or `None`.

When the filter or selector requires parameters to make sense (example: if you want to select the object closest to X, Y, you must pass those coordinates), you pass them as arguments according to the signature.

An object state is just one of the dicts nested into the :ref:`Game State`, so naturally you can access its properties by square bracket indexing.

This should be enough to get started with writing AIs!