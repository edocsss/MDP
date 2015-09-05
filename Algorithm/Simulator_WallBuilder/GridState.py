from enum import Enum

__author__ = 'ECAND_000'

class GridState(Enum):
    UNEXPLORED = 0
    EXPLORED_NO_OBSTACLE = 1
    EXPLORED_WITH_OBSTACLE = 2
    START_ZONE = 4
    END_ZONE = 5
    END_ZONE_EXPLORED = 6