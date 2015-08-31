import Algorithm
import ArenaMap
import MainUI
import MapDescriptor
import Robot
import WifiComm
import RobotController
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
mapDescriptor = MapDescriptor.MapDescriptor("MapDescriptor.in")
completeMap = ArenaMap.ArenaMap(mapDescriptor.getTranslatedMap())
completeMap2 = ArenaMap.ArenaMap()
initialMap = ArenaMap.ArenaMap()

# Other object initialization
robot = Robot.Robot(initialMap)

ui = MainUI.MainUI(initialMap, robot)
algorithm = None
wifiComm = WifiComm.WifiComm(host, port)
robotController = RobotController.RobotController(completeMap, robot, algorithm, wifiComm, ui)

while ui.isStartExplore() == False:
    # Do nothing
    time.sleep(0.2)

# When the EXPLORE button has been pressed, start exploration by initiating RobotController
robotController.explore()