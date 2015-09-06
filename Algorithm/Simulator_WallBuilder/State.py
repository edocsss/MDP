from copy import deepcopy
from ArenaMap import *
from Direction import *

class State:
    def __init__(self, robot):
        self.robot = robot

    def __hash__(self):
        return hash(self.robot)
    
    # [(action, next_state), ...]
    def getChildren(self):
        result = []
        for action in Action:
            temp = deepcopy(self.robot)
            temp.do(action)

            for sensor in temp.sensors:
                direction = (temp.orientation.value + sensor.relative_direction + 4) % 4
                
                x, y = sensor.position[0], sensor.position[1]
                if   direction == 1: x, y = -y,  x
                elif direction == 2: x, y = -x, -y
                elif direction == 3: x, y =  y, -x
                x, y = x + temp.x, y + temp.y

                arena = temp.mapKnowledge
                for i in range(1, int(sensor.range / 10) + 1):
                    next_x, next_y = x + i * Direction.dx[direction], y + i * Direction.dy[direction]
                    if arena[next_y][next_x] == GridState.UNEXPLORED or arena[next_y][next_x] == GridState.END_ZONE:
                        arena[next_y][next_x].setGridState(GridState.SEARCHED)
                    elif arena[next_y][next_x] == GridState.WALL:
                        break
            
            child_state = State(temp)
            
            result.append((action, next_state))

        return result

    def isTerminal(self):
        for i in range(ArenaMap.MAP_HEIGHT):
            for j in range(ArenaMap.MAP_WIDTH):
                if self.robot.mapKnowledge[i][j] == GridState.UNEXPLORED or self.robot.mapKnowledge[i][j] == GridState.END_ZONE:
                    return False
        return True
