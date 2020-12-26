from battlematica.core.game_entity import GameEntity


class Artifact(GameEntity):

    state_props = ['x', 'y', 'r', 'hg', 'is_carried', 'last_touch']

    def __init__(self, x, y, hg=0):
        """
        The Artifact is picked up by Bots and deposited in a DropPort for points.

        :param x: x coordinate of the artifact
        :param y: y coordinate of the artifact
        :param hg: the team that can score points with the artifact; 0 for an artifact that can be used
         by all teams (integer)

        """

        super().__init__(x, y, 45.0, hg)
        self.is_carried = False
        self.last_touch = None

    def _chores(self, X, Y):
        raise ValueError('Artifact does not have chores to accomplish')