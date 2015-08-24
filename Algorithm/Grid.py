from GridState import *

__author__ = 'ECAND_000'

class Grid:
    GRID_SIZE = 1;

    def __init__(self, x, y, state=GridState.UNEXPLORED):
        self.x = x
        self.y = y
        self.state = state

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getGridState(self):
        return self.state

    def setGridState(self, state):
        self.state = state