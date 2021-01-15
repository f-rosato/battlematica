Writing AIs
===========

.. Tip::

    It is highly suggested that you read :ref:`Game Mechanics` and :ref:`Game State` before this section.

Writing AIs is the core task in Battlematica. An AI directly usable by the Battlematica core code is simply a function of this form:

.. code-block:: python

    def my_ai(self: Bot, state: dict):

        # do stuff

        return action, target_x, target_y

`action` is a string, one of the ones listed in :ref:`Actions`.
`target_x`, `target_y` are floats, representing the target of the action.

Once you have your function, you assign it to a `Bot` instance through the metod `set_ai`.

If the function happens to return `None` (e.g., when the end of the function is reached without hitting a `return` statement at all), the Bot will loiter in place.

You are free to write whatever you like inside the function! You can write bots that use machine learning, neural networks...

In addition to this bare-bones, maximum freedom method, which will be most palatable to anyone that wants to use Battlematica for research and experiments, Battlematica offers also more immediacy through the purpose-built languace, BATTLANG.

Using BATTLANG
''''''''''''''

BATTLANG is a small language that can be used to specify `behavior trees`_. Battlematica is able, through the :ref:`battlang` subpackage, to turn BATTLANG into a straight Python function of the form above that can be, then, used in your scripts.

.. _`behavior trees`: https://en.wikipedia.org/wiki/Behavior_tree_(artificial_intelligence,_robotics_and_control)


BATTLANG is designed to offer the most natural way of expression possible. You can write conditions, and the block of conditional statements to be executed under this condition is identified through 4-space indentation, similarly to Python itself. Comments are introduced by "#".

.. Important::

    Only 4-space indentation is supported: do not use `tab`.

Here is an example of a program written in BATTLANG, showcasing its flavour and structure:

.. literalinclude:: ../sample_battlang_ai/ultimate.blng
  :language: text

Structure
---------

The essential structure of the statements is:

.. code-block:: text

    ? [not] (one identifier and zero or more filters)

Introduced by `? [not]`, the condition activates a conditional block if any object specified by the identifier and the filter exists (or not).

.. code-block:: text

    command + (one selector, one identifier and zero or more filters)

If any object specified by the identifier and the filter exists, it selects one with the selector and makes it the target of the command. If none exist, the command is not emitted and the program continues. **The first valid command encountered is executed and the program stops**.

Nesting
-------
The grammar should cleanly support nesting for those constructs that support it - essentially filters that have a spatial parameter, for example:

.. code-block:: text

    ? move to nearest enemy bot shooting with_target nearest ally bot health_level(0,25)

This statement is a command, but since the `with_target` filter needs a spatial parameter, this spatial parameter can be specified by nesting the descriptor of an object collocated in space: in this case, `nearest ally bot health_level(0,25)`.

    - command: move [to]
    - selector: nearest
    - identifier: bot
    - filter: enemy, with_target (one selector, one identifier and zero or more filters)

The grammar should support any level of nesting, but more than one should seldom be needed.
Nesting can *optionally* be visually aided with the use of parentheses.

Misc
----
The spatial parameter can also be filled with `here`, meaning the position of the bot executing the function.

Frequently, one wants to use such parametric filters accepting any object from a group. This is possible by using the keyword `any` to form an "anyfilter". For example:

.. code-block:: text

    ? shoot least_health enemy bot shooting with_target any ally bot

.. Note::

    For the technical user, the BATTLANG language is defined ad parsed on-the-fly according to a BNF grammar that you can find under `battlematica/battlang`.


.. Note::

    The lexer-parser used by BATTLANG is directly taken from the pynetree_ package. The package is no longer mantained and, since the version on Pypi presented import issues in some cases, the MIT-licensed code is directly included in Battlematica instead of using pynetree as a requirement. Nevertheless, all credit for this part natuarlly goes to the original author, Jan Max Meyer.

.. _pynetree: https://pypi.org/project/pynetree/#history


Using the library directly
''''''''''''''''''''''''''

BATTLANG, under the hood, is translated against a :ref:`library` of primitives that you can naturally access directly. If you want, you can write Python code leveraging these functions. This could be seen as a mixed method that offers a handy baseline of primitives but still offers you the possibility to use whatever Python tool you want.

We'll use a very basic AI, `shoot_retire` (included in the `sample_ai` submodule) to illustrate this method. The purpose of this AI is simply to go towards the nearest enemy and shoot at it. When the shield level drops under 20%, the Bot will flee away from the nearest enemy that is targeting it.

.. literalinclude:: ../battlematica/sample_ai/shoot_retire.py
  :language: python

You operate by using the functions found in the :ref:`library` submodule and :ref:`StateQuerier`. These are used to get one or more objects from the field (enemies, artifacts, allies...) according to a set of criterions that "sieve" the state. The functions contained in the :ref:`library` submodule are divided in identifiers, filters and selectors.

A sequence of functions from these are passed as arguments of calls to the instance of :ref:`StateQuerier`.

.. Important::

    You must begin with an identifier, then apply zero or more filters, and optionally finish with a selector.

.. Important::

    If you do not finish with a selector, you are returned a list of states of objects, possibly empty. If you finish with a selector, you are returned either the selected object state or `None`.

When the filter or selector requires parameters to make sense (example: if you want to select the object closest to X, Y, you must pass those coordinates), you pass them as arguments according to the signature.

An object state is just one of the dicts nested into the :ref:`Game State`, so naturally you can access its properties by square bracket indexing.

This should be enough to get started with writing AIs!