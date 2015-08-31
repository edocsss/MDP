from enum import Enum

__author__ = "Edwin Candinegara"

class SensorRange(Enum):
    # Range is in CENTIMETER!!
    SHORT_SENSOR = 30
    LONG_SENSOR = 50

    def getValue(self):
        return self.value