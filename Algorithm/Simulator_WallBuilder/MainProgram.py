import Algorithm as Algorithm
import ArenaMap as ArenaMap
import MainUI as MainUI
import Robot as Robot
import WifiComm as WifiComm
import RobotController as RobotController
import WallBuilder as WallBuilder
import time

__author__ = 'ECAND_000'

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

ui.open()
while ui.isStartExplore() == False:
    # Do nothing
    time.sleep(0.2)

# When the EXPLORE button has been pressed, start exploration by initiating RobotController
robotController.explore()