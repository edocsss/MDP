from Grid import *
from GridState import *

__author__ = 'ECAND_000'

class ArenaMap:
    MAP_WIDTH = 15
    MAP_HEIGHT = 20

    def __init__(self, map):
        self.gridMap = [[None for x in range (0, self.MAP_WIDTH)] for y in range (0, self.MAP_HEIGHT)]

        # Map iterator
        i = 0
        for n in range (0, self.MAP_HEIGHT):
            for m in range (0, self.MAP_WIDTH):
                if map[i] == '0':
                    self.gridMap[n][m] = Grid(n, m, GridState.UNEXPLORED)
                elif map[i] == '1':
                    self.gridMap[n][m] = Grid(n, m, GridState.EXPLORED_NO_OBSTACLE)
                elif map[i] == '2':
                    self.gridMap[n][m] = Grid(n, m, GridState.EXPLORED_WITH_OBSTACLE)

                i += 1

    def getGridMap (self):
        return self.gridMap

    def getGrid (self, x, y):
        return self.gridMap[x][y]

    def updateGrid (self, x, y, state):
        self.getGrid(x, y).setState(state)