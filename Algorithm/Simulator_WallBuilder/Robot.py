import ArenaMap as ArenaMap
import Sensor as Sensor
from RobotOrientation import *
from GridState import *
from SensorPosition import *
from SensorRange import *

__author__ = 'ECAND_000'

class Robot:
    def __init__(self, initialMap):
        # (x, y) = (1, 1) because we assume that the robot is 3 x 3 and it is placed right
        # in the middle of the 3 x 3 box
        self.x = 1
        self.y = 1
        self.orientation = RobotOrientation.FRONT

        # For sensor reading simplicity, the POSITION of the sensor is as if the sensor is placed in the front and then rotated
        self.sensors = [
            Sensor.Sensor(SensorPosition.FRONT_SENSOR, SensorRange.SHORT_SENSOR, (-1, 1)),
            Sensor.Sensor(SensorPosition.FRONT_SENSOR, SensorRange.SHORT_SENSOR, (0, 1)),
            Sensor.Sensor(SensorPosition.FRONT_SENSOR, SensorRange.SHORT_SENSOR, (1, 1)),
            Sensor.Sensor(SensorPosition.RIGHT_SENSOR, SensorRange.SHORT_SENSOR, (-1, 1)),
            Sensor.Sensor(SensorPosition.RIGHT_SENSOR, SensorRange.SHORT_SENSOR, (0, 1)),
            Sensor.Sensor(SensorPosition.RIGHT_SENSOR, SensorRange.SHORT_SENSOR, (1, 1))
        ]
        self.mapKnowledge = initialMap

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

    def moveForward(self):
        if self.orientation == RobotOrientation.FRONT:
            self.y += 1
        elif self.orientation == RobotOrientation.LEFT:
            self.x -= 1
        elif self.orientation == RobotOrientation.RIGHT:
            self.x += 1
        elif self.orientation == RobotOrientation.BACK:
            self.y -= 1

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
            self.orientation = RobotOrientation.RIGHT

    # Returns the Grid position where it should be updated
    def readSensors(self, completeMap):
        result = []
        gridMap = completeMap.getGridMap()

        for sensor in self.sensors:
            sensorPosition = sensor.getPosition()
            sensorRange = int(sensor.getRange().getValue() / 10) + 1

            # Need to consider all 16 possibilities
            # May not need the BACK_SENSOR though --> TODO LIST
            if sensor.getOrientation() == SensorPosition.FRONT_SENSOR:
                if self.orientation == RobotOrientation.FRONT:
                    for i in range (1, sensorRange):
                        if self.y + i + sensorPosition[1] >= ArenaMap.ArenaMap.MAP_HEIGHT \
                            or gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.END_ZONE:
                            break

                        self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x + sensorPosition[0], self.y + i + sensorPosition[1]))
                        if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.BACK:
                    for i in range (1, sensorRange):
                        if self.y - i - sensorPosition[1] < 0\
                            or gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.END_ZONE:
                            break

                        self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x - sensorPosition[0], self.y - i - sensorPosition[1]))
                        if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.LEFT:
                    for i in range (1, sensorRange):
                        if self.x - i - sensorPosition[1] < 0\
                            or gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.END_ZONE:
                            break

                        self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x - i - sensorPosition[1], self.y + sensorPosition[0]))
                        if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.RIGHT:
                    for i in range (1, sensorRange):
                        if self.x + sensorPosition[1] + i >= ArenaMap.ArenaMap.MAP_WIDTH\
                            or gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.END_ZONE:
                            break

                        self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x + sensorPosition[1] + i, self.y - sensorPosition[0]))
                        if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

            elif sensor.getOrientation() == SensorPosition.LEFT_SENSOR:
                if self.orientation == RobotOrientation.FRONT:
                    for i in range (1, sensorRange):
                        if self.x - i - sensorPosition[1] < 0\
                            or gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.END_ZONE:
                            break

                        self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x - i - sensorPosition[1], self.y + sensorPosition[0]))
                        if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.BACK:
                    for i in range (1, sensorRange):
                        if self.x + sensorPosition[1] + i >= ArenaMap.ArenaMap.MAP_WIDTH\
                            or gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.END_ZONE:
                            break

                        self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x + sensorPosition[1] + i, self.y - sensorPosition[0]))
                        if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.LEFT:
                    for i in range (1, sensorRange):
                        if self.y - i - sensorPosition[1] < 0\
                            or gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.END_ZONE:
                            break

                        self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x - sensorPosition[0], self.y - i - sensorPosition[1]))
                        if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.RIGHT:
                    for i in range (1, sensorRange):
                        if self.y + i + sensorPosition[1] >= ArenaMap.ArenaMap.MAP_HEIGHT \
                            or gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.END_ZONE:
                            break

                        self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x + sensorPosition[0], self.y + i + sensorPosition[1]))
                        if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

            elif sensor.getOrientation() == SensorPosition.RIGHT_SENSOR:
                if self.orientation == RobotOrientation.FRONT:
                    for i in range (1, sensorRange):
                        if self.x + sensorPosition[1] + i >= ArenaMap.ArenaMap.MAP_WIDTH\
                            or gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.END_ZONE:
                            break

                        self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x + sensorPosition[1] + i, self.y - sensorPosition[0]))
                        if gridMap[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y - sensorPosition[0]][self.x + sensorPosition[1] + i].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.BACK:
                    for i in range (1, sensorRange):
                        if self.x - i - sensorPosition[1] < 0\
                            or gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.END_ZONE:
                            break

                        self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x - i - sensorPosition[1], self.y + sensorPosition[0]))
                        if gridMap[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y + sensorPosition[0]][self.x - i - sensorPosition[1]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.LEFT:
                    for i in range (1, sensorRange):
                        if self.y + i + sensorPosition[1] >= ArenaMap.ArenaMap.MAP_HEIGHT \
                            or gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.END_ZONE:
                            break

                        self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x + sensorPosition[0], self.y + i + sensorPosition[1]))
                        if gridMap[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y + i + sensorPosition[1]][self.x + sensorPosition[0]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

                elif self.orientation == RobotOrientation.RIGHT:
                    for i in range (1, sensorRange):
                        if self.y - i - sensorPosition[1] < 0\
                            or gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.START_ZONE\
                            or gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.END_ZONE:
                            break

                        self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.EXPLORED_NO_OBSTACLE)
                        result.append((self.x - sensorPosition[0], self.y - i - sensorPosition[1]))
                        if gridMap[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                            self.mapKnowledge.getGridMap()[self.y - i - sensorPosition[1]][self.x - sensorPosition[0]].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
                            break

        # Return result in the form of list of (updatedGrid.x, updatedGrid.y)
        return result