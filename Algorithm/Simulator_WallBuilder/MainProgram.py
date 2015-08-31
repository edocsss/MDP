import Simulator_WallBuilder.Algorithm as Algorithm
import Simulator_WallBuilder.ArenaMap as ArenaMap
import Simulator_WallBuilder.MainUI as MainUI
import Simulator_WallBuilder.Robot as Robot
import Simulator_WallBuilder.WifiComm as WifiComm
import Simulator_WallBuilder.RobotController as RobotController
import Simulator_WallBuilder.WallBuilder as WallBuilder
import time

__author__ = 'ECAND_000'

def startExploration():
    global startExplore
    startExplore = True

# Wi-Fi HOST & PORT
host = "192.168.7.7"
port = 7777

# Status variable
startExplore = False

# Different ArenaMap for different testing
obstacleMap = ArenaMap.ArenaMap()
initialMap = ArenaMap.ArenaMap()

# Other object initialization
robot = Robot.Robot(initialMap)
# wallBuilder = WallBuilder.WallBuilder(obstacleMap)
algorithm = None
wifiComm = WifiComm.WifiComm(host, port)
ui = MainUI.MainUI(initialMap, obstacleMap, robot)
robotController = RobotController.RobotController(obstacleMap, robot, algorithm, wifiComm, ui)

# while wallBuilder.isStartExplorationWindow() == False:
#     # Do nothing
#     time.sleep(0.2)

ui.open()
while ui.isStartExplore() == False:
    # Do nothing
    time.sleep(0.2)

# When the EXPLORE button has been pressed, start exploration by initiating RobotController
robotController.explore()