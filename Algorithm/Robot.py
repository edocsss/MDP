from RobotOrientation import *

__author__ = 'ECAND_000'

class Robot:
    def __init__(self):
        # (x, y) = (1, 1) because we assume that the robot is 3 x 3 and it is placed right
        # in the middle of the 3 x 3 box
        self.x = 1
        self.y = 1
        self.orientation = RobotOrientation.FRONT
        self.sensors = []

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