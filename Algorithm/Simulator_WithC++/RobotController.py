import copy
import time
import subprocess
from ArenaMap import *

__author__ = 'ECAND_000'

class RobotController:
    def __init__(self, completeMap, robot, algorithm, wifiComm, ui):
        # Needed for sensor reading
        self.completeMap = completeMap

        # Other objects needed for reading and sending data and determining the next action
        self.robot = robot
        self.algorithm = algorithm
        self.wifiComm = wifiComm
        self.ui = ui

    def explore(self):
        start = time.time()
        stop = False

        # Connect to WiFi
        # self.wifiComm.start()

        # Probably before going into the loop, tell the robot to do self adjustment
        while True:
            # Data sent --> (x, y, orientation, mapKnowledge)
            actions = subprocess.Popen(["demo", str(self.robot.x), str(self.robot.y), str(self.robot.orientation.value), self.robot.mapKnowledge.translate()], stdout=subprocess.PIPE).communicate()[0].decode().strip()
            if len(actions) == 0:
                break

            # actions = self.wifiComm.read()
            for action in actions:
                # Read sensors reading from Arduino
                # sensorReading = self.wifiComm.read()
                # for reading in sensorReading:
                #     # DO SOMETHING WITH THE READING
                #     # WHAT TO DO DEPENDS ON HOW THE READING IS COMMUNICATED
                #     # UPDATE THE ROBOT'S MAP KNOWLEDGE USING THOSE READINGS
                #     # UPDATE THE UI USING THOSE READINGS
                #     pass

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

                r = self.robot.do(action)
                if r == False:
                    break

                # Send the action to the Arduino --> since if there is a break, that action is then not transferred
                # Basically each action is tested using the simulator's robot first and the actual robot sensor readings
                # self.wifiComm.write(r)
                self.ui.drawRobot()

            if stop == True:
                break

        # Last sensor reading & update
        # Only update the UPDATED GRIDS, based on the sensor reading
        updatedGrids = self.robot.readSensors(self.completeMap)
        for n in updatedGrids:
            x, y = n[0], n[1]
            self.ui.drawGrid(x, y)

        # Last percentage update
        self.ui.setMapPercentage()

        end = time.time()
        print("RUNNING TIME:", end - start)
        print("Robot exploration done!")

        # RUN FASTEST PATH ALGORITHM HERE TO END ZONE (ArenaMap.MAP_WIDTH - 1, ArenaMap.MAP_HEIGHT - 1)
        time.sleep(0.1)
        print("Going to end zone...")
        self.fastestPathRun(ArenaMap.MAP_WIDTH - 2, ArenaMap.MAP_HEIGHT - 2)

        # RUN FASTEST PATH ALGORITHM HERE TO GO BACK TO (1,1) --> ROBOT'S CENTRAL POSITION
        time.sleep(0.1)
        print("Going back to start zone...")
        self.fastestPathRun(1, 1)

        # START FASTEST PATH RUN
        self.fastestPathRun(ArenaMap.MAP_WIDTH - 2, ArenaMap.MAP_HEIGHT - 2)

        # PROBABLY USE A BLOCKING WI-FI READING SINCE THERE IS NO POINT IN CONTINUING THE WHILE LOOP IF THERE IS NO INCOMING DATA!!
        #
        # while self.robot.wifiComm.read() != "S":
        #   time.sleep(0.1)
        #
        # while True:
        #   Use ALGORITHM to determine the next move (probably the ALGORITHM will return a bunch of moves) --> at this point in time, assume that there is NO OBSTACLE at all
        #   For each move:
        #       Read sensors (using the robot's readSensors() method) --> inside here, there should be a MAP UPDATE (based on the sensor reading, like the simulation right now)
        #       Update the ROBOT GRIDMAP
        #       Do the move!! (send to Arduino + simulator) --> at this point
        #           --> there should be a logic which check whether it is possible to do THIS MOVE before sending message!! --> probably the logic can be put inside the self.robot --> inside the moveForward() method, return FALSE if not possible
        #           --> if not, BREAK, then go to the next loop of the WHILE LOOP (search for bunch of moves based on the sensor readings just now)
        #
        #       Remove the move!! (by list.pop(0))


    def fastestPathRun(self, targetX, targetY):
        print("Running fastest path algorithm...")

        actions = subprocess.Popen(["demo", str(self.robot.x), str(self.robot.y), str(self.robot.orientation.value), self.robot.mapKnowledge.translate(), str(targetX), str(targetY)], stdout=subprocess.PIPE).communicate()[0].decode().strip()
        for action in actions:
            self.robot.do(action)
            self.ui.drawRobot()

        # Probably before going into the loop, tell the robot to do self adjustment
        # The algorithm runs once and only once
        # The algorithm must return a bunch of actions from the Start zone to the End Zone all at once
        return
