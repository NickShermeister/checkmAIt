class PieceMove(object):
    def __init__(self, start, end):
        """
        :param PieceCoord start:
        :param PieceCoord end:
        """
        self.start = start
        self.end = end


class PieceCoord(object):
    def __init__(self, x, y):
        """
        :param int x: x-coordinate on the play field
        :param int y: y-coordinate on the play field
        """
        self.y = y
        self.x = x


class Action(object):
    def __init__(self):
        self._up = False
        self._down = False
        self._coords = None

    @classmethod
    def PenUp(cls):
        action = cls()
        action._up = True
        return action

    @classmethod
    def PenDown(cls):
        action = cls()
        action._down = True
        return action

    @classmethod
    def Goto(cls, x, y):
        """
        :type coords: PieceCoord
        """
        action = cls()
        action._coords = PieceCoord(x, y)
        return action
