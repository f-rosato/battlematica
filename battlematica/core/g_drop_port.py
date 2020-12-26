from battlematica.core.game_entity import GameEntity


class DropPort(GameEntity):
    def __init__(self, x, y, hg=0):

        """
        The DropPort is the object where the Bots can deposit Artifacts to score points.

        :param x: x coordinate of the drop port
        :param y: y coordinate of the drop port
        :param hg: the team that can use the drop port; 0 for a drop port that can be used
         by all teams (integer)

        """

        super().__init__(x, y, 0.0, hg)

    def _chores(self, X, Y):
        raise ValueError('DropPort does not have chores to accomplish')