import ArenaMap
import MainUI
import Robot
import WifiComm
import RobotController
import MapDescriptor
import time
import atexit

__author__ = 'ECAND_000'

# try:
# Wi-Fi HOST & PORT
host = "192.168.7.7"
port = 5005

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


def onExit ():
    robotController.wifiComm.end()

atexit.register(onExit)

ui.open()
while ui.isStartExplore() == False:
    # Do nothing
    time.sleep(0.2)

# Start explore
robotController.explore()

# Once done, generate the Map Descriptor file based on the last Robot's Explored Map knowledge
mapDescriptor.writeMapDescription(robot.getMapKnowledge())

# START FASTEST PATH RUN
##    while wifiComm.read() != "P":
##         print("WRONG FASTEST PATH RUN CODE!")
##         time.sleep(0.01)

# LAST RUN!! Wait for Android
if robotController.goalReached == True:
    robotController.fastestPathRun(ArenaMap.ArenaMap.MAP_WIDTH - 2, ArenaMap.ArenaMap.MAP_HEIGHT - 2)
else:
    print("Impossible to do fastest path run since we have not reached the goal zone yet!")
#
# except Exception as e:
#     print(e)
