import ArenaMap as ArenaMap
import Sensor as Sensor
from RobotOrientation import *
from GridState import *
from SensorPosition import *
from SensorRange import *
from Direction import *

__author__ = 'ECAND_000'

class Robot:
    START_ZONE_COORDINATES = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

    def __init__(self, initialMap):
        # (x, y) = (1, 1) because we assume that the robot is 3 x 3 and it is placed right
        # in the middle of the 3 x 3 box
        self.x = 12
        self.y = 18
        self.orientation = RobotOrientation.RIGHT

        # For sensor reading simplicity, the POSITION of the sensor is as if the sensor is placed in the front and then rotated
        self.sensors = [
            Sensor.Sensor(SensorPosition.FRONT_SENSOR, SensorRange.SHORT_SENSOR, (-1, 1)),
            Sensor.Sensor(SensorPosition.FRONT_SENSOR, SensorRange.SHORT_SENSOR, (0, 1)),
            Sensor.Sensor(SensorPosition.FRONT_SENSOR, SensorRange.SHORT_SENSOR, (1, 1)),
            # Sensor.Sensor(SensorPosition.LEFT_SENSOR, SensorRange.SHORT_SENSOR, (-1, 1)),
            Sensor.Sensor(SensorPosition.LEFT_SENSOR, SensorRange.SHORT_SENSOR, (1, 1)),
            Sensor.Sensor(SensorPosition.RIGHT_SENSOR, SensorRange.LONG_SENSOR, (-1, 1))
        ]

        self.mapKnowledge = initialMap

        # Wherever the robot is, that 3x3 square of the robot is infered as EXPLORED_NO_OBSTACLE (EXCEPT IF THE ROBOT'S MIDDLE IS AT (1, 1))
        for i in range (-1, 2):
            for j in range (-1, 2):
                if (self.x + j, self.y + i) in self.START_ZONE_COORDINATES:
                    self.mapKnowledge.gridMap[self.y + i][self.x + j].setGridState(GridState.START_ZONE_EXPLORED)
                else:
                    self.mapKnowledge.gridMap[self.y + i][self.x + j].setGridState(GridState.EXPLORED_NO_OBSTACLE)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.orientation == other.orientation and self.mapKnowledge == other.mapKnowledge

    def __hash__(self):
        return hash((self.x, self.y, self.orientation, self.mapKnowledge))
    
    def getPositionX(self):
        return self.x

    def getPositionY(self):
        return self.y

    def getOrientation(self):
        return self.orientation

    def setPositionX(self, x):
        self.x = x

    def setPositionY(self, y):
        self.y = y

    def setOrientation(self, orientation):
        self.orientation = orientation

    def getMapKnowledge(self):
        return self.mapKnowledge

    def moveForward(self):
        if self.orientation == RobotOrientation.FRONT or self.orientation == RobotOrientation.BACK:
            counter = 3
            for i in range(-1, 2):
                x, y = self.x + i, self.y + 2 * Direction.dy[self.orientation.value]
                if x < 0 or x >= ArenaMap.ArenaMap.MAP_WIDTH or y < 0 or y >= ArenaMap.ArenaMap.MAP_HEIGHT or self.mapKnowledge[y][x] == GridState.EXPLORED_WITH_OBSTACLE:
                    counter -= 1

            if counter == 3:
                self.y += Direction.dy[self.orientation.value]
                return True
            else:
                return False

        elif self.orientation == RobotOrientation.RIGHT or self.orientation == RobotOrientation.LEFT:
            counter = 3
            for i in range(-1, 2):
                y, x = self.y + i, self.x + 2 * Direction.dx[self.orientation.value]
                if x < 0 or x >= ArenaMap.ArenaMap.MAP_WIDTH or y < 0 or y >= ArenaMap.ArenaMap.MAP_HEIGHT or self.mapKnowledge[y][x] == GridState.EXPLORED_WITH_OBSTACLE:
                    counter -= 1

            if counter == 3:
                self.x += Direction.dx[self.orientation.value]
                return True
            else:
                return False


    def moveBackward(self):
        if self.orientation == RobotOrientation.FRONT:
            self.y -= 1
        elif self.orientation == RobotOrientation.LEFT:
            self.x += 1
        elif self.orientation == RobotOrientation.RIGHT:
            self.x -= 1
        elif self.orientation == RobotOrientation.BACK:
            self.y += 1

    def rotateLeft(self):
        if self.orientation == RobotOrientation.FRONT:
            self.orientation = RobotOrientation.LEFT
        elif self.orientation == RobotOrientation.LEFT:
            self.orientation = RobotOrientation.BACK
        elif self.orientation == RobotOrientation.RIGHT:
            self.orientation = RobotOrientation.FRONT
        elif self.orientation == RobotOrientation.BACK:
            self.orientation = RobotOrientation.RIGHT

    def rotateRight(self):
        if self.orientation == RobotOrientation.FRONT:
            self.orientation = RobotOrientation.RIGHT
        elif self.orientation == RobotOrientation.LEFT:
            self.orientation = RobotOrientation.FRONT
        elif self.orientation == RobotOrientation.RIGHT:
            self.orientation = RobotOrientation.BACK
        elif self.orientation == RobotOrientation.BACK:
            self.orientation = RobotOrientation.LEFT

    def do(self, action):
        if action == 'F':
            return self.moveForward()
        elif action == 'L':
            self.rotateLeft()
        elif action == 'R':
            self.rotateRight()

    # Returns the Grid position where it should be updated
    def readSensors(self, completeMap):
        result = []
        gridMap = completeMap.getGridMap()

        for sensor in self.sensors:
            sensorPosition = sensor.getPosition()
            sensorRange = int(sensor.getRange().value / 10) + 1

            # Need to consider all 16 possibilities
            if sensor.getOrientation() == SensorPosition.FRONT_SENSOR:
                if self.orientation == RobotOrientation.FRONT:
                    for i in range (1, sensorRange):
                        if self.y + i + sensorPosition[1] >= ArenaMap.ArenaMap.MAP_HEIGHT:
                            break

                        if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.END_ZONE:

                            # For the sake of counting COMPLETION PERCENTAGE (easier than changing the whole map system)
                            if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.END_ZONE:
                                self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.END_ZONE_EXPLORED)

                            if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.START_ZONE:
                                self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.START_ZONE_EXPLORED)

                            break

                        # Assume that those grids are empty at first
                        self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.EXPLORED_NO_OBSTACLE)

                        # Indicate which grids need to be updated
                        result.append((self.x + sensorPosition[0], self.y + i + sensorPosition[1]))

                        # Check whether there is an obstacle (check with the complete map)
                        if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.BACK:
                    for i in range (1, sensorRange):
                        if self.y - i - sensorPosition[1] < 0:
                            break

                        if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.END_ZONE:

                            if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.END_ZONE:
                                self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.END_ZONE_EXPLORED)

                            if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.START_ZONE:
                                self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.START_ZONE_EXPLORED)

                            break

                        self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x - sensorPosition[0], self.y - i - sensorPosition[1]))
                        if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.LEFT:
                    for i in range (1, sensorRange):
                        if self.x - i - sensorPosition[1] < 0:
                            break

                        if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.END_ZONE:

                            if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.END_ZONE:
                                self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.END_ZONE_EXPLORED)

                            if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.START_ZONE:
                                self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.START_ZONE_EXPLORED)

                            break

                        self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x - i - sensorPosition[1], self.y + sensorPosition[0]))
                        if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.RIGHT:
                    for i in range (1, sensorRange):
                        if self.x + sensorPosition[1] + i >= ArenaMap.ArenaMap.MAP_WIDTH:
                            break

                        if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.END_ZONE:

                            if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.END_ZONE:
                                self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.END_ZONE_EXPLORED)

                            if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.START_ZONE:
                                self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.START_ZONE_EXPLORED)
                                
                            break

                        self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x + sensorPosition[1] + i, self.y - sensorPosition[0]))
                        if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

            elif sensor.getOrientation() == SensorPosition.LEFT_SENSOR:
                if self.orientation == RobotOrientation.FRONT:
                    for i in range (1, sensorRange):
                        if self.x - i - sensorPosition[1] < 0:
                            break

                        if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.END_ZONE:

                            if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.END_ZONE:
                                gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.END_ZONE_EXPLORED)

                            if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.START_ZONE:
                                gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.START_ZONE_EXPLORED)

                            break

                        self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x - i - sensorPosition[1], self.y + sensorPosition[0]))
                        if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.BACK:
                    for i in range (1, sensorRange):
                        if self.x + sensorPosition[1] + i >= ArenaMap.ArenaMap.MAP_WIDTH:
                            break

                        if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.END_ZONE:
                            
                            if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.END_ZONE:
                                self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.END_ZONE_EXPLORED)

                            if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.START_ZONE:
                                self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.START_ZONE_EXPLORED)

                            break

                        self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x + sensorPosition[1] + i, self.y - sensorPosition[0]))
                        if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.LEFT:
                    for i in range (1, sensorRange):
                        if self.y - i - sensorPosition[1] < 0:
                            break

                        if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.END_ZONE:

                            if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.END_ZONE:
                                self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.END_ZONE_EXPLORED)

                            if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.START_ZONE:
                                self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.START_ZONE_EXPLORED)
                                
                            break

                        self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x - sensorPosition[0], self.y - i - sensorPosition[1]))
                        if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.RIGHT:
                    for i in range (1, sensorRange):
                        if self.y + i + sensorPosition[1] >= ArenaMap.ArenaMap.MAP_HEIGHT:
                            break

                        if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.END_ZONE:

                            if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.END_ZONE:
                                self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.END_ZONE_EXPLORED)

                            if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.START_ZONE:
                                self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.START_ZONE_EXPLORED)

                            break

                        self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x + sensorPosition[0], self.y + i + sensorPosition[1]))
                        if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

            elif sensor.getOrientation() == SensorPosition.RIGHT_SENSOR:
                if self.orientation == RobotOrientation.FRONT:
                    for i in range (1, sensorRange):
                        if self.x + sensorPosition[1] + i >= ArenaMap.ArenaMap.MAP_WIDTH:
                            break

                        if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.END_ZONE:                            

                            if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.END_ZONE:
                                self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.END_ZONE_EXPLORED)

                            if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.START_ZONE:
                                self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.START_ZONE_EXPLORED)

                            break

                        self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x + sensorPosition[1] + i, self.y - sensorPosition[0]))
                        if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.BACK:
                    for i in range (1, sensorRange):
                        if self.x - i - sensorPosition[1] < 0:
                            break

                        if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.END_ZONE:

                            if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.END_ZONE:
                                self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.END_ZONE_EXPLORED)

                            if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.START_ZONE:
                                self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.START_ZONE_EXPLORED)

                            break

                        self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x - i - sensorPosition[1], self.y + sensorPosition[0]))
                        if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.LEFT:
                    for i in range (1, sensorRange):
                        if self.y + i + sensorPosition[1] >= ArenaMap.ArenaMap.MAP_HEIGHT:
                            break

                        if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.END_ZONE:

                            # For the sake of counting COMPLETION PERCENTAGE (easier than changing the whole map system)
                            if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.END_ZONE:
                                self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.END_ZONE_EXPLORED)

                            if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.START_ZONE:
                                self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.START_ZONE_EXPLORED)

                            break

                        # Assume that those grids are empty at first
                        self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.EXPLORED_NO_OBSTACLE)

                        # Indicate which grids need to be updated
                        result.append((self.x + sensorPosition[0], self.y + i + sensorPosition[1]))

                        # Check whether there is an obstacle (check with the complete map)
                        if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.RIGHT:
                    for i in range (1, sensorRange):
                        if self.y - i - sensorPosition[1] < 0:
                            break

                        if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.END_ZONE:

                            if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.END_ZONE:
                                self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.END_ZONE_EXPLORED)

                            if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.START_ZONE:
                                self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.START_ZONE_EXPLORED)

                            break

                        self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x - sensorPosition[0], self.y - i - sensorPosition[1]))
                        if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

        # Return result in the form of list of (updatedGrid.x, updatedGrid.y)
        return result

    def placeObstaclesFromRobotReading(self, sensorReading, dummyMap):
        # This GridMap is only for updating the OBSTACLE MAP
        # Then the robot will use this OBSTACLE MAP AS IF it is a simulation, the wall obstacle is put into the obstacle map during the real run
        # When reading the sensor, the robot will ACTUALLY UPDATE its knowledge
        gridMap = dummyMap.getGridMap()
        stateException = [GridState.EXPLORED_WITH_OBSTACLE, GridState.EXPLORED_NO_OBSTACLE, GridState.START_ZONE, GridState.END_ZONE, GridState.START_ZONE_EXPLORED, GridState.END_ZONE_EXPLORED]
        for i in range (0, len(self.sensors)):
            reading = int(sensorReading[i].strip())
            sensor = self.sensors[i]

            # If the sensor reading from arduino is the maximum range, then assume there is no obstacle
            if reading == sensor.range.value / 10:
                continue

            sensorPosition = sensor.getPosition()
            if sensor.getOrientation() == SensorPosition.FRONT_SENSOR:
                if self.orientation == RobotOrientation.FRONT:
                    posY = self.y + sensorPosition[1] + reading + 1
                    posX = self.x + sensorPosition[0]

                    if posY < ArenaMap.ArenaMap.MAP_HEIGHT and posY >= 0 and posX < ArenaMap.ArenaMap.MAP_WIDTH and posX >= 0 and gridMap:
                        if self.mapKnowledge.gridMap[posY][posX].state in stateException:
                            continue
                        
                        gridMap[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)

                elif self.orientation == RobotOrientation.BACK:
                    posY = self.y - sensorPosition[1] - reading - 1
                    posX = self.x - sensorPosition[0]

                    if posY < ArenaMap.ArenaMap.MAP_HEIGHT and posY >= 0 and posX < ArenaMap.ArenaMap.MAP_WIDTH and posX >= 0:
                        if self.mapKnowledge.gridMap[posY][posX].state in stateException:
                            continue
                        
                        gridMap[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)

                elif self.orientation == RobotOrientation.LEFT:
                    posY = self.y + sensorPosition[0]
                    posX = self.x - sensorPosition[1] - reading - 1

                    if posY < ArenaMap.ArenaMap.MAP_HEIGHT and posY >= 0 and posX < ArenaMap.ArenaMap.MAP_WIDTH and posX >= 0:
                        if self.mapKnowledge.gridMap[posY][posX].state in stateException:
                            continue
                        
                        gridMap[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)

                elif self.orientation == RobotOrientation.RIGHT:
                    posY = self.y - sensorPosition[0]
                    posX = self.x + sensorPosition[1] + reading + 1

                    if posY < ArenaMap.ArenaMap.MAP_HEIGHT and posY >= 0 and posX < ArenaMap.ArenaMap.MAP_WIDTH and posX >= 0:
                        if self.mapKnowledge.gridMap[posY][posX].state in stateException:
                            continue
                        
                        gridMap[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)

            elif sensor.getOrientation() == SensorPosition.LEFT_SENSOR:
                if self.orientation == RobotOrientation.FRONT:
                    posY = self.y + sensorPosition[0]
                    posX = self.x - sensorPosition[1] - reading - 1

                    if posY < ArenaMap.ArenaMap.MAP_HEIGHT and posY >= 0 and posX < ArenaMap.ArenaMap.MAP_WIDTH and posX >= 0:
                        if self.mapKnowledge.gridMap[posY][posX].state in stateException:
                            continue
                        
                        gridMap[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)

                elif self.orientation == RobotOrientation.BACK:
                    posY = self.y - sensorPosition[0]
                    posX = self.x + sensorPosition[1] + reading + 1

                    if posY < ArenaMap.ArenaMap.MAP_HEIGHT and posY >= 0 and posX < ArenaMap.ArenaMap.MAP_WIDTH and posX >= 0:
                        if self.mapKnowledge.gridMap[posY][posX].state in stateException:
                            continue
                        
                        gridMap[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)

                elif self.orientation == RobotOrientation.LEFT:
                    posY = self.y - sensorPosition[1] - reading - 1
                    posX = self.x - sensorPosition[0]

                    if posY < ArenaMap.ArenaMap.MAP_HEIGHT and posY >= 0 and posX < ArenaMap.ArenaMap.MAP_WIDTH and posX >= 0:
                        if self.mapKnowledge.gridMap[posY][posX].state in stateException:
                            continue
                        
                        gridMap[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)

                elif self.orientation == RobotOrientation.RIGHT:
                    posY = self.y + sensorPosition[1] + reading + 1
                    posX = self.x + sensorPosition[0]

                    if posY < ArenaMap.ArenaMap.MAP_HEIGHT and posY >= 0 and posX < ArenaMap.ArenaMap.MAP_WIDTH and posX >= 0:
                        if self.mapKnowledge.gridMap[posY][posX].state in stateException:
                            continue
                        
                        gridMap[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)

            elif sensor.getOrientation() == SensorPosition.RIGHT_SENSOR:
                if self.orientation == RobotOrientation.FRONT:
                    posY = self.y - sensorPosition[0]
                    posX = self.x + sensorPosition[1] + reading + 1

                    if posY < ArenaMap.ArenaMap.MAP_HEIGHT and posY >= 0 and posX < ArenaMap.ArenaMap.MAP_WIDTH and posX >= 0:
                        if self.mapKnowledge.gridMap[posY][posX].state in stateException:
                            continue
                        
                        gridMap[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)

                elif self.orientation == RobotOrientation.BACK:
                    posY = self.y + sensorPosition[0]
                    posX = self.x - sensorPosition[1] - reading - 1

                    if posY < ArenaMap.ArenaMap.MAP_HEIGHT and posY >= 0 and posX < ArenaMap.ArenaMap.MAP_WIDTH and posX >= 0:
                        if self.mapKnowledge.gridMap[posY][posX].state in stateException:
                            continue
                        
                        gridMap[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)

                elif self.orientation == RobotOrientation.LEFT:
                    posY = self.y + sensorPosition[1] + reading + 1
                    posX = self.x + sensorPosition[0]

                    if posY < ArenaMap.ArenaMap.MAP_HEIGHT and posY >= 0 and posX < ArenaMap.ArenaMap.MAP_WIDTH and posX >= 0:
                        if self.mapKnowledge.gridMap[posY][posX].state in stateException:
                            continue
                        
                        gridMap[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)

                elif self.orientation == RobotOrientation.RIGHT:
                    posY = self.y - sensorPosition[1] - reading - 1
                    posX = self.x - sensorPosition[0]

                    if posY < ArenaMap.ArenaMap.MAP_HEIGHT and posY >= 0 and posX < ArenaMap.ArenaMap.MAP_WIDTH and posX >= 0:
                        if self.mapKnowledge.gridMap[posY][posX].state in stateException:
                            continue
                        
                        gridMap[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
