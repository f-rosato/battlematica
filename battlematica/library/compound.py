class AnyFilter:

    """AnyFilter is used when there is more than one set of parameters
    acceptable for a base filter: for example, one could want to filter
    bots that are targeting any of several ally bots, not just a particular
    one.

    Instead of being called the first time with a single group of
    parameters, AnyFilter is called with an iterable containing each group of
    acceptable parameters."""

    def __init__(self, filter):
        self.inner_filter = filter

    def __call__(self, *parameters_combos):

        def anycompare(elems):

            anylist = []
            for pc in parameters_combos:
                anylist.append(self.inner_filter(elems, *pc))
        return anycompare
