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
        self.trackPosition = [[False for i in range (0, ArenaMap.MAP_WIDTH)] for j in range (0, ArenaMap.MAP_HEIGHT)]
        self.trackOrientation = [[[False, False, False, False] for i in range (0, ArenaMap.MAP_WIDTH)] for j in range (0, ArenaMap.MAP_HEIGHT)]
        self.checkTracking = True

        self.initialX = self.robot.x
        self.initialY = self.robot.y
        self.checkTrackingCounter = 0

    def robotReadSensor(self):
        sensorReading = self.wifiComm.read()
        self.robot.placeObstaclesFromRobotReading(sensorReading, self.completeMap)

        updatedGrids = self.robot.readSensors(self.completeMap)
        for n in updatedGrids:
            x, y = n[0], n[1]
            self.ui.drawGrid(x, y)


    def checkTrack(self):
        if self.trackPosition[self.robot.y][self.robot.x] == True and self.trackOrientation[self.robot.y][self.robot.x][self.robot.orientation.value] == True:
            return False
        else:
            self.trackPosition[self.robot.y][self.robot.x] = True
            self.trackOrientation[self.robot.y][self.robot.x][self.robot.orientation.value] = True
            return True

    def moveToOuterWall(self):
        # Assumption --> robot is looking at WEST direction
        # for i in range (0, 3):
        #     self.checkGoalReached()
        #     self.robot.do('R')
        #     self.robotReadSensor()
        #     self.ui.drawRobot()
        #     self.wifiComm.write("1R")

        # Go downward
        temp = True
        while temp == True:
            self.checkGoalReached()
            temp = self.robot.do('F')
            self.robotReadSensor()
            self.ui.drawRobot()
            self.wifiComm.write("1F")

            # The statement inside the IF will not be executed
            # This statement only updates the Percentage mainly
            if self.ui.checkTimeout() == False or self.ui.setMapPercentage() == False:
                break

        # Prepare for Wall Hugging
        self.checkGoalReached()
        self.robot.do('R')
        self.robotReadSensor()
        self.ui.drawRobot()
        self.wifiComm.write("1R")

    # def subAlgo(self):
    #     if self.checkTracking == True and self.checkTrack() == False:
    #         # Go forward until it hits a wall
    #         temp = True
    #         while temp == True:
    #             self.checkGoalReached()
    #             temp = self.robot.do('F')
    #             self.robotReadSensor()
    #             self.ui.drawRobot()
    #             self.wifiComm.write("1F")
    #
    #             # The statement inside the IF will not be executed
    #             # This statement only updates the Percentage mainly
    #             if self.ui.checkTimeout() == False or self.ui.setMapPercentage() == False:
    #                 return False
    #
    #         self.checkGoalReached()
    #         self.robot.do('R')
    #         self.robotReadSensor()
    #         self.ui.drawRobot()
    #         self.wifiComm.write("1R")
    #
    #         # Only check whether the robot has passed the same position as before once and only once (ASSUMPTION!)
    #         self.checkTracking = False

    def isFinished(self):
        if self.robot.x == self.initialX and self.robot.y == self.initialY:
            self.checkTrackingCounter += 1

        if self.checkTrackingCounter == 2:
            return False
        else:
            return True
        # return self.checkTrack()

    def explore(self):
        # Start WiFi
        self.wifiComm.start()


        # Wait for Android initialization
        while self.wifiComm.read() != 'S':
            print("WRONG EXPLORATION START CODE!")
            time.sleep(0.01)


        stop = False

######################################################################################################################

        # Initial sensor read
        self.robotReadSensor()

######################################################################################################################

        # Initial pre-defined movement --> going for down ward, then turn left
        # self.moveToOuterWall()

######################################################################################################################

        # Probably before going into the loop, tell the robot to do self adjustment
        while True:
            # A*
            # actions = subprocess.Popen(["search", str(self.robot.x), str(self.robot.y), str(self.robot.orientation.value), self.robot.mapKnowledge.translateAlgorithm()], stdout=subprocess.PIPE).communicate()[0].decode().strip() 

            # Wall hugging
            actions = subprocess.Popen(["search", str(self.robot.x), str(self.robot.y), str(self.robot.orientation.value), self.robot.mapKnowledge.translateAlgorithm(), "--ganteng"], stdout=subprocess.PIPE).communicate()[0].decode().strip()

            # Manual test
            # actions = self.wifiComm.read()

            # actions = []
            if len(actions) == 0:
                break


            # Iterating the action list
            for action in actions:
                # Check whether the robot has ever reached goal zone
                self.checkGoalReached()

                # Check whether the robot has done 1 full round
                # ONLY FOR WALL HUGGING ALGORITHM
                if action == 'F' and self.isFinished() == False:
                    print()
                    print("Robot has do one round! Stopping...")
                    stop = True
                    break



                # Check whether the robot has gone through that particular grid
                # DO THIS ONLY FOR WALL HUGGING
                # Only track when it is moving forward, not when it is rotating
                # if self.subAlgo() == False:
                #    break

                
                
                # The robot simulator does the action
                r = self.robot.do(action)
                if r == False:
                    print()
                    print("Robot is banging to the outer wall!")
                    # self.robotReadSensor()
                    break


                # Send action to Arduino
                self.wifiComm.write("1" + action)


                # Redraw robot
                self.ui.drawRobot()


                # Read sensor
                self.robotReadSensor()


                # This checking must be done here because if not, there will be one extra ROBOT drawing (including one moveForward())
                # If the checking is done in ui.drawRobot(), the moveForward() cannot be prevented although the robot should have stopped already before moving forward
                if self.ui.checkTimeout() == False or self.ui.setMapPercentage() == False:
                    print()
                    print("TIMEOUT / PERCENTAGE AUTOMATIC TERMINATION!")
                    stop = True
                    break


            # Stop the whole looping because we have reached the targeted TIMEOUT or PERCENTAGE
            if stop == True:
                break


        # Last sensor reading & update
        # Read sensors reading from Arduino
        # self.robotReadSensor()


        # Last percentage update
        self.ui.setMapPercentage()


        # Ending message
        print("Robot exploration done!")


        # RUN FASTEST PATH ALGORITHM HERE TO END ZONE (ArenaMap.MAP_WIDTH - 1, ArenaMap.MAP_HEIGHT - 1)
        # This is only useful for A* based algorithm
        # For Wall Hugging, we can assume that the robot always steps into the goal zone once and only once
        if self.goalReached == True:
            print("Going back to start zone only because we have reached the goal zone...")
            self.fastestPathRun(1, 1)
        else:
            # Check whether the 3x3 goal zone has been explored all
            if self.robot.mapKnowledge.isGoalZoneExplored() == True:            
                print("Going to end zone if not reached yet...")
                self.fastestPathRun(ArenaMap.MAP_WIDTH - 2, ArenaMap.MAP_HEIGHT - 2)

                # RUN FASTEST PATH ALGORITHM HERE TO GO BACK TO (1,1) --> ROBOT'S CENTRAL POSITION
                print("Going back to start zone...")
                self.fastestPathRun(1, 1)
            else:
                print("Goal zone has not been explored! Impossible to do a fastest path run to end zone")
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
        if self.goalReached == False and self.robot.mapKnowledge.isGoalZoneExplored() == True:
            self.goalReached = True
