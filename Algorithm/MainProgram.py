import Algorithm
import ArenaMap
import MainUI
import MapDescriptor
import Robot
import RobotOrientation
import Sensor
import WifiComm

__author__ = 'ECAND_000'

mapDescriptor =MapDescriptor.MapDescriptor("MapDescriptor.in")
arenaMap = ArenaMap.ArenaMap(mapDescriptor.getTranslatedMap())