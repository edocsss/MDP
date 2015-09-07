from copy import deepcopy
from Action import *
from Direction import *
from Robot import *
from ArenaMap import *
import time

class State:
    def __init__(self, robot):
        self.robot = robot

    def __hash__(self):
        return hash(self.robot)

    def __eq__(self, other):
        return self.robot == other.robot

    def __lt__(self, other):
        return True

    # [(action, next_state), ...]
    def getChildren(self):
        result = []
        for action in Action:
            temp = deepcopy(self.robot)
            temp.do(action)

            arena = temp.mapKnowledge
            for sensor in temp.sensors:
                direction = (temp.orientation.value + sensor.relative_direction + 4) % 4
                
                x, y = sensor.position[0], sensor.position[1]
                if   direction == 3: x, y = -y,  x
                elif direction == 2: x, y = -x, -y
                elif direction == 1: x, y =  y, -x
                x, y = x + temp.x, y + temp.y

                # print('Direction:', direction)
                for i in range(1, int(sensor.range.value / 10) + 1):
                    next_x, next_y = x + i * Direction.dx[direction], y + i * Direction.dy[direction]
                    # print(next_x, next_y)
                    if next_x < 0 or next_x >= ArenaMap.MAP_WIDTH or next_y < 0 or next_y >= ArenaMap.MAP_HEIGHT:
                        break

                    if arena[next_y][next_x] == GridState.UNEXPLORED or arena[next_y][next_x] == GridState.END_ZONE:
                        arena[next_y][next_x].setGridState(GridState.SEARCHED)
                    elif arena[next_y][next_x] == GridState.EXPLORED_WITH_OBSTACLE:
                        break

            # print(arena)
            # print("XXXXXXXXXXXXX")
            # time.sleep(1)
            child_state = State(temp)
            result.append((action, child_state))

        return result

    def isTerminal(self):
        for i in range(ArenaMap.MAP_HEIGHT):
            for j in range(ArenaMap.MAP_WIDTH):
                if self.robot.mapKnowledge[i][j] == GridState.UNEXPLORED or self.robot.mapKnowledge[i][j] == GridState.END_ZONE:
                    return False
        return True
