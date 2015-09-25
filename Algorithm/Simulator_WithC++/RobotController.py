import copy
import time
import subprocess
from ArenaMap import *

__author__ = 'ECAND_000'

class RobotController:
    UPDATE_MAP = 10

    def __init__(self, completeMap, robot, algorithm, wifiComm, ui):
        # Needed for sensor reading
        self.completeMap = completeMap

        # Other objects needed for reading and sending data and determining the next action
        self.robot = robot
        self.algorithm = algorithm
        self.wifiComm = wifiComm
        self.ui = ui
        self.goalReached = False

    def explore(self):
        # Start WiFi
        self.wifiComm.start()


        # Wait for Android initialization
        #while self.wifiComm.read() != 'S':
        #    print("WRONG EXPLORATION START CODE!")
        #    time.sleep(0.01)


        stop = False
        updateMapCounter = 0

######################################################################################################################

        # Initial sensor read
        #sensorReading = self.wifiComm.read()
        #self.robot.placeObstaclesFromRobotReading(sensorReading, self.completeMap)
        #updatedGrids = self.robot.readSensors(self.completeMap)
        #for n in updatedGrids:
            #x, y = n[0], n[1]
            #self.ui.drawGrid(x, y)

######################################################################################################################

        # Probably before going into the loop, tell the robot to do self adjustment
        while True:
            # Data sent --> (x, y, orientation, mapKnowledge)
            #actions = subprocess.Popen(["search", str(self.robot.x), str(self.robot.y), str(self.robot.orientation.value), self.robot.mapKnowledge.translateAlgorithm()], stdout=subprocess.PIPE).communicate()[0].decode().strip()
            # actions = subprocess.Popen(["search", str(self.robot.x), str(self.robot.y), str(self.robot.orientation.value), self.robot.mapKnowledge.translateAlgorithm(), "--ganteng"], stdout=subprocess.PIPE).communicate()[0].decode().strip()

            actions = self.wifiComm.read()
            if len(actions) == 0:
                break


            # Iterating the action list
            for action in actions:
                # The robot simulator does the action
                r = self.robot.do(action)
                if r == False:
                    updatedGrids = self.robot.readSensors(self.completeMap)
                    for n in updatedGrids:
                        x, y = n[0], n[1]
                        self.ui.drawGrid(x, y)
                    print("FALSE!!")
                    break

                # Redraw robot
                self.ui.drawRobot()


                # Check whether the robot has ever reached goal zone
                self.checkGoalReached()


                # Send action to Arduino
                #self.wifiComm.write("1" + action)


                # Update map counter
                updateMapCounter += 1


                # Send the map to Android after UPDATE_MAP actions
                # if updateMapCounter >= self.UPDATE_MAP:
                    # print("Sending Robot's map knowledge to Android...")
                    # updateMapCounter = 0
                    # self.wifiComm.write("2" + self.robot.mapKnowledge.translateAndroid())


                # Read sensors reading from Arduino
                # Read after the map update because the Arduino needs some time to execute the action. Meanwhile, the simulator can send the whole 75 hex to Android --> don't waste time
                sensorReading = self.wifiComm.read()
                self.robot.placeObstaclesFromRobotReading(sensorReading, self.completeMap)

                # Only update the UPDATED GRIDS, based on the sensor reading
                updatedGrids = self.robot.readSensors(self.completeMap)
                for n in updatedGrids:
                    x, y = n[0], n[1]
                    self.ui.drawGrid(x, y)


                # This checking must be done here because if not, there will be one extra ROBOT drawing (including one moveForward())
                # If the checking is done in ui.drawRobot(), the moveForward() cannot be prevented although the robot should have stopped already before moving forward
                if self.ui.checkTimeout() == False or self.ui.setMapPercentage() == False:
                    stop = True
                    break


            # Stop the whole looping because we have reached the targeted TIMEOUT or PERCENTAGE
            if stop == True:
                break


        # Last sensor reading & update
        # Read sensors reading from Arduino
        sensorReading = self.wifiComm.read()
        self.robot.placeObstaclesFromRobotReading(sensorReading, self.completeMap)
        updatedGrids = self.robot.readSensors(self.completeMap)
        for n in updatedGrids:
            x, y = n[0], n[1]
            self.ui.drawGrid(x, y)


        # Last percentage update
        self.ui.setMapPercentage()


        # Ending message
        print("Robot exploration done!")


        # RUN FASTEST PATH ALGORITHM HERE TO END ZONE (ArenaMap.MAP_WIDTH - 1, ArenaMap.MAP_HEIGHT - 1)
        if self.goalReached == True:
            print("Going back to start zone only because we have not reached the goal zone...")
            self.fastestPathRun(1, 1)
        else:
            print("Going to end zone if not reached yet...")
            self.fastestPathRun(ArenaMap.MAP_WIDTH - 2, ArenaMap.MAP_HEIGHT - 2)

            # RUN FASTEST PATH ALGORITHM HERE TO GO BACK TO (1,1) --> ROBOT'S CENTRAL POSITION
            time.sleep(0.1)
            print("Going back to start zone...")
            self.fastestPathRun(1, 1)


    def fastestPathRun(self, targetX, targetY):
        print("Running fastest path algorithm...")

        actions = subprocess.Popen(["search", str(self.robot.x), str(self.robot.y), str(self.robot.orientation.value), self.robot.mapKnowledge.translateAlgorithm(), str(targetX), str(targetY)], stdout=subprocess.PIPE).communicate()[0].decode().strip()
        for action in actions:
            self.robot.do(action)

            # Send action to Arduino
            self.wifiComm.write("1" + action)

            self.ui.drawRobot()

        # Probably before going into the loop, tell the robot to do self adjustment
        # The algorithm runs once and only once
        # The algorithm must return a bunch of actions from the Start zone to the End Zone all at once
        return


    def checkGoalReached(self):
        if self.goalReached == False and self.robot.x == ArenaMap.MAP_WIDTH - 2 and self.robot.y == ArenaMap.MAP_HEIGHT - 2:
            self.goalReached = True
