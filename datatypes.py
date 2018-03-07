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
        :param int x: x-coordinate on the play field:
            x=0 is leftmost square in graveyard, x=3 is the leftmost square on the board
        :param int y: y-coordinate on the play field
        """
        self.y = y
        self.x = x


class Action(object):
    def __init__(self):
        self.up = False
        self.down = False
        self.coord = None

    @classmethod
    def PenUp(cls):
        action = cls()
        action.up = True
        return action

    @classmethod
    def PenDown(cls):
        action = cls()
        action.down = True
        return action

    @classmethod
    def Goto(cls, x, y):
        """
        :type coords: PieceCoord
        """
        action = cls()
        action.coord = PieceCoord(x, y)
        return action
