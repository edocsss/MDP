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
        if self.state == GridState.UNEXPLORED or self.state== GridState.END_ZONE:
            return "?"
        elif self.state == GridState.EXPLORED_WITH_OBSTACLE:
            return "#"
        elif self.state == GridState.EXPLORED_NO_OBSTACLE or self.state == GridState.START_ZONE or self.state == GridState.END_ZONE_EXPLORED:
            return "."
        elif self.state == GridState.SEARCHED:
            return "*"
    
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
        if type(other) == Grid:
            return self.state == other.state
        elif type(other) == GridState:
            return self.state == other
        raise ValueError()
