from Grid import *
from GridState import *

__author__ = 'ECAND_000'

class ArenaMap:
    MAP_WIDTH = 15
    MAP_HEIGHT = 20

    def __init__(self, map=""):
        # self.gridMap = ((None for x in range (0, self.MAP_WIDTH)) for y in range (0, self.MAP_HEIGHT))
        self.gridMap = tuple(tuple(Grid(x, y) for x in range (0, ArenaMap.MAP_WIDTH)) for y in range (0, ArenaMap.MAP_HEIGHT))
        # Need to use IF since there cannot be > 1 constructor
        if len(map) > 0:
            self.updateEntireMap(map)
        # else:
        #     for n in range (0, self.MAP_HEIGHT):
        #         for m in range (0, self.MAP_WIDTH):
        #             self.gridMap[n][m] = Grid(n, m)

        self.setStartEndZone()

    def __hash__(self):
        # return hash(''.join(''.join(map(str, row)) for row in self.gridMap))
        return hash(self.gridMap)

    def __str__(self):
        return '\n'.join(''.join(map(str, row)) for row in reversed(self.gridMap))

    def __eq__(self, other):
        return self.gridMap == other.gridMap

    def getGridMap (self):
        return self.gridMap

    def getGrid (self, x, y):
        return self.gridMap[x][y]

    def updateEntireMap(self, map):
        # Map iterator
        i = 0
        for n in range (0, self.MAP_HEIGHT):
            for m in range (0, self.MAP_WIDTH):
                if map[i] == '0':
                    self.gridMap[n][m].setGridState(GridState.UNEXPLORED)
                elif map[i] == '1':
                    self.gridMap[n][m].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                elif map[i] == '2':
                    self.gridMap[n][m].setGridState(GridState.EXPLORED_WITH_OBSTACLE)

                i += 1

        self.setStartEndZone()

    def setStartEndZone(self):
        # Determine where the START and END zone are
        for i in range (0, 3):
            for j in range (0, 3):
                self.gridMap[i][j].setGridState(GridState.START_ZONE)
                self.gridMap[self.MAP_HEIGHT - i - 1][self.MAP_WIDTH - j - 1].setGridState(GridState.END_ZONE)

    def updateGrid (self, x, y, state):
        self.getGrid(x, y).setState(state)

    def __getitem__(self, key):
        return self.gridMap[key]

    def countExploredGrids(self):
        count = 0
        for m in range (0, self.MAP_HEIGHT):
            for n in range (0, self.MAP_WIDTH):
                if self.gridMap[m][n].getGridState() == GridState.START_ZONE \
                   or self.gridMap[m][n].getGridState() == GridState.EXPLORED_NO_OBSTACLE \
                   or self.gridMap[m][n].getGridState() == GridState.EXPLORED_WITH_OBSTACLE\
                   or self.gridMap[m][n].getGridState() == GridState.END_ZONE_EXPLORED:
                    count += 1

        return count

    def getPercentageExploredGrids(self):
        return 100 * self.countExploredGrids() / (self.MAP_HEIGHT * self.MAP_WIDTH)
