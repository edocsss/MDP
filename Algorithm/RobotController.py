__author__ = 'ECAND_000'

class RobotController:
    arenaMap = None
    robot = None
    algorithm = None
    wifiComm = None

    def __init__(self, arenaMap, robot, algorithm, wifiComm):
        self.arenaMap = arenaMap
        self.robot = robot
        self.algorithm = algorithm
        self.wifiComm = wifiComm


