import Algorithm as Algorithm
import ArenaMap
import MainUI
import Robot
import WifiComm
import RobotController
import MapDescriptor
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
algorithm = None
wifiComm = WifiComm.WifiComm(host, port)
mapDescriptor = MapDescriptor.MapDescriptor()
ui = MainUI.MainUI(initialMap, obstacleMap, robot)
robotController = RobotController.RobotController(obstacleMap, robot, algorithm, wifiComm, ui)

ui.open()
while ui.isStartExplore() == False:
    # Do nothing
    time.sleep(0.2)

# When the EXPLORE button has been pressed, start exploration by initiating RobotController
robotController.explore()

# Once done, generate the Map Descriptor file based on the last Robot's Explored Map knowledge
mapDescriptor.writeMapDescription(robot.getMapKnowledge())

# Since the exploration is done, get ready for Fastest Path Run
robotController.fastestPathRun()