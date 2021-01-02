class StateQuerier:
    def __init__(self, state):

        """The StateQuerier is initialized with a Bot instance and a state snapshot.
        You then call it with a sequence of functions."""

        self.state = state

    def __call__(self, *args):

        """The first argument must be an identifier ex: Library.enemies(), Library.artifacts()...

         the following ones must be filters ex: Library.health_between(low, high)...

         the last one can optionally be a selector ex: Library.closest_to_xy(X,Y)...

         Returns a list containing the states of the selected object(s). The list can be empty if
         no object meets all conditions.

         """

        result = args[0](self.state)

        for passage in args[1:]:
            if result is None:
                break
            else:
                result = passage(result)

        return result