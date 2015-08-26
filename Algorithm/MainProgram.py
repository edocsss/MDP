import Algorithm
import ArenaMap
import MainUI
import MapDescriptor
import Robot
import RobotOrientation
import Sensor
import WifiComm
import tkinter
import time

__author__ = 'ECAND_000'

mapDescriptor =MapDescriptor.MapDescriptor("MapDescriptor.in")
arenaMap = ArenaMap.ArenaMap(mapDescriptor.getTranslatedMap())
robot = Robot.Robot()
ui = MainUI.MainUI(arenaMap, robot)

time.sleep(0.5)
robot.moveForward()
ui.drawRobot()

time.sleep(0.5)
robot.rotateRight()
ui.drawRobot()

time.sleep(0.5)
robot.moveForward()
ui.drawRobot()

time.sleep(0.5)
robot.moveForward()
ui.drawRobot()

time.sleep(0.5)
robot.moveForward()
ui.drawRobot()

time.sleep(0.5)
robot.moveForward()
ui.drawRobot()

time.sleep(0.5)
robot.moveForward()
ui.drawRobot()