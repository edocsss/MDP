import time

__author__ = 'ECAND_000'

class RobotController:
    arenaMap = None
    robot = None
    algorithm = None
    wifiComm = None
    ui = None

    def __init__(self, completeMap, robot, algorithm, wifiComm, ui):
        # Needed for sensor reading
        self.completeMap = completeMap

        # Other objects needed for reading and sending data and determining the next action
        self.robot = robot
        self.algorithm = algorithm
        self.wifiComm = wifiComm
        self.ui = ui

    def explore(self):
        i = 0
        while True:
            if i == 17:
                break

            print("Reading sensors...")
            updatedGrids = self.robot.readSensors(self.completeMap)

            # Only update the UPDATED GRIDS, based on the sensor reading
            for n in updatedGrids:
                x, y = n[0], n[1]
                self.ui.drawGrid(x, y)

            # This checking must be done here because if not, there will be one extra ROBOT drawing (including one moveForward())
            # If the checking is done in ui.drawRobot(), the moveForward() cannot be prevented although the robot should have stopped already before moving forward
            if self.ui.checkTimeout() == False or self.ui.setMapPercentage() == False:
                break

            self.robot.moveForward()
            self.ui.drawRobot()

            i += 1

        updatedGrids = self.robot.readSensors(self.completeMap)
        # Only update the UPDATED GRIDS, based on the sensor reading
        for n in updatedGrids:
            x, y = n[0], n[1]
            self.ui.drawGrid(x, y)








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
