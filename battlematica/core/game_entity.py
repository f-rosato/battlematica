import uuid
from abc import abstractmethod


class GameEntity:

    state_props = ['x', 'y', 'r', 'hg']

    def __init__(self, x, y, r, hg=None):

        # positional
        self.x = x
        self.y = y
        self.r = r

        # team
        self.hg = hg

        # random unique id
        self.uid = uuid.uuid4().hex

    @property
    def state(self):
        st = {k: getattr(self, k) for k in self.state_props}
        st.update({'id': self.uid})
        return st

    @abstractmethod
    def _chores(self, X, Y):
        """Things that the object can do on its own for updating its state."""
        return []
