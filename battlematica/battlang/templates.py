HEAD = \
"""# generated code


def {name}(self, state, sq, lib):

    def validate_command(c):
        if c[1] is not None:
            return c
        else:
            return None

    query = sq(state)
    {prog}
"""


XY_QUAL_LIST = """
# {comment}
def target_{n}():
    tg_{n} = query(\n        {series})
    if tg_{n} is not None:
        tgx_{n}, tgy_{n} = tg_{n}['x'], tg_{n}['y']
    else:
        tgx_{n}, tgy_{n} = None, None
    return tgx_{n}, tgy_{n}"""


XY_QUAL_LIST_AWAY = """
# {comment}
def target_{n}():
    tg_{n} = query(\n        {series})
    if tg_{n} is not None:
        tgx_{n}, tgy_{n} = tg_{n}['x'], tg_{n}['y']
        tgx_{n}, tgy_{n} = 2 * self.x - tgx_{n}, 2 * self.y - tgy_{n}
    else:
        tgx_{n}, tgy_{n} = None, None
    return tgx_{n}, tgy_{n}"""


COND_LIST = """
# {comment}
def exists_{n}():
    cl_{n} = query(\n        {series})
    cl_exists_{n} = len(cl_{n}) > 0
    if {flip}:
        cl_exists_{n} = not cl_exists_{n}
    return cl_exists_{n}"""
