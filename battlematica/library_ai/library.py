import inspect
import types
from itertools import chain

from . import selectors, identifiers, filters

# The class is dynamically populated with inspect and accessed through __getattr__.
# This allows to write intuitive functions in the modules and to wrap them with a "partializer"
# on the fly.
# Admittedly not the cleanest, most transparent and most robust approach.
# In the future it might be a cleaner/better idea to just have the library functions
# as methods.


class Library:
    def __init__(self):
        """Library is a helper class whose methods return functions that you can use in a
        StateQuerier. The methods might accept parameters (typical example: x, y in functions
        like closest_to) that will be built in into the returned function.

        It's easier to use than to explain.

        """

        self.library = {}
        for _n, o in chain(inspect.getmembers(filters),
                           inspect.getmembers(identifiers),
                           inspect.getmembers(selectors)):
            if isinstance(o, types.FunctionType):
                self.library[o.__name__] = o

    def __getattr__(self, item):

        fn = self.library[item]

        def partializer_fn(*partialized_args):
            def partialized_fn(*dynamic_args):
                nonlocal fn
                return fn(*dynamic_args, *partialized_args)
            return partialized_fn
        return partializer_fn


