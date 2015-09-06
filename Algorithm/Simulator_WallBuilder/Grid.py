from GridState import *

__author__ = 'ECAND_000'

class Grid:
    def __init__(self, x, y, state=GridState.UNEXPLORED):
        self.x = x
        self.y = y
        self.state = state

    def __hash__(self):
        return hash(self.state)

    def __str__(self):
        return str(self.state.value)
    
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getGridState(self):
        return self.state

    def setGridState(self, state):
        self.state = state

    def __ne__(self, other):
        assert type(other) == GridState
        return self.state != other

    def __eq__(self, other):
        assert type(other) == GridState
        return self.state == other
