from SensorPosition import SensorPosition

__author__ = 'ECAND_000'

class Sensor:
    position = None
    range = None

    def __init__(self, orientation, range, position):
        self.orientation = orientation
        self.range = range
        self.position = position

    def getPosition(self):
        return self.position

    def getOrientation(self):
        return self.orientation

    def getRange(self):
        return self.range