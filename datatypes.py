class PieceMove(object):
    def __init__(self, start, end):
        """
        :param PieceCoord|tuple start:
        :param PieceCoord|tuple end:
        """
        if type(start) is tuple:
            start = PieceCoord(*start)

        if type(end) is tuple:
            end = PieceCoord(*end)

        self.start = start
        self.end = end

    def __str__(self):
        return chr(int(self.start.x)+97) + str(int(self.start.y + 1)) + chr(int(self.end.x)+97) + str(int(self.end.y)+1)

    __repr__ = __str__

    def toString(self):
        return chr(self.start.x+97-3) + chr(self.start.y) + chr(self.end.x+97-3) + chr(self.end.y)


class PieceCoord(object):
    def __init__(self, x, y):
        """
        :param int x: x-coordinate on the play field:
            x=0 is leftmost square in graveyard, x=3 is the leftmost square on the board
        :param int y: y-coordinate on the play field
        """
        self.y = y
        self.x = x

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    __repr__ = __str__

    def as_tuple(self):
        return self.x, self.y


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

    @classmethod
    def GotoCoord(cls, coord: PieceCoord):
        action = cls()
        action.coord = coord
        return action

    def __str__(self):
        if self.up:
            return "Pen Up"
        elif self.down:
            return "Pen Down"
        elif self.coord is not None:
            return "Move to ({},{})".format(self.coord.x, self.coord.y)
