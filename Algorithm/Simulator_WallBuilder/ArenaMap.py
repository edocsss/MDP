from Simulator_WallBuilder.Grid import *
from Simulator_WallBuilder.GridState import *

__author__ = 'ECAND_000'

class ArenaMap:
    MAP_WIDTH = 15
    MAP_HEIGHT = 20

    def __init__(self, map=""):
        self.gridMap = [[None for x in range (0, self.MAP_WIDTH)] for y in range (0, self.MAP_HEIGHT)]

        # Need to use IF since there cannot be > 1 constructor
        if len(map) > 0:
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

        else:
            for n in range (0, self.MAP_HEIGHT):
                for m in range (0, self.MAP_WIDTH):
                    self.gridMap[n][m] = Grid(n, m)

        # Determine where the START and END zone are
        for i in range (0, 3):
            for j in range (0, 3):
                self.gridMap[i][j].setGridState(GridState.START_ZONE)
                self.gridMap[self.MAP_HEIGHT - i - 1][self.MAP_WIDTH - j - 1].setGridState(GridState.END_ZONE)

    def getGridMap (self):
        return self.gridMap

    def getGrid (self, x, y):
        return self.gridMap[x][y]

    def updateGrid (self, x, y, state):
        self.getGrid(x, y).setState(state)

    def countExploredGrids(self):
        count = 0
        for m in range (0, self.MAP_HEIGHT):
            for n in range (0, self.MAP_WIDTH):
                if self.gridMap[m][n].getGridState() == GridState.EXPLORED_NO_OBSTACLE or self.gridMap[m][n].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                    count += 1

        return count