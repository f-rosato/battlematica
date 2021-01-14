class AnyFilter:
    def __init__(self, filter):
        self.inner_filter = filter

    def __call__(self, *parameters_combos):

        def anycompare(elems):

            anylist = []
            for pc in parameters_combos:
                anylist.append(self.inner_filter(elems, *pc))
        return anycompare
