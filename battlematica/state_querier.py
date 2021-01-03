class StateQuerier:
    def __init__(self, state):

        """The StateQuerier is initialized with a Bot instance and a state snapshot.
        You then call it with a sequence of functions created with battlematica.library."""

        self.state = state

    def __call__(self, *args):

        """The first argument must be an identifier ex: battlematica.library.bots()...

         The following ones must be filters ex: battlematica.library.health_between(low, high)...

         The last one can optionally be a selector ex: battlematica.library.closest_to_xy(X,Y)...

         If the last argument is a selector, it returns either the state of the selected object or None
         if no object meet all filter conditions.

         Otherwise, it returns a list containing the state(s) of the selected object(s). The list can be empty if
         no object meets all conditions.

         """

        result = args[0](self.state)

        for passage in args[1:]:
            if result is None:
                break
            else:
                result = passage(result)

        return result