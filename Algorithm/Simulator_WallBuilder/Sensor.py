__author__ = 'ECAND_000'

class Sensor:
    def __init__(self, orientation, range, position, relative_direction = 0):
        self.orientation = orientation
        self.range = range
        self.position = position
        
        self.relative_direction = relative_direction

    def getPosition(self):
        return self.position

    def getOrientation(self):
        return self.orientation

    def getRange(self):
        return self.range
