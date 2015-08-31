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
        # Do a INFINITE WHILE loop until exploration finishes --> inside the WHILE loop, call the ALGORITHM, generate
        # actions, update the robot (for simulator, just update the robot)

        i = 0
        while True:
            if i == 7:
                break
            print("Reading sensors...")
            updatedGrids = self.robot.readSensors(self.completeMap)

            # Only update the UPDATED GRIDS, based on the sensor reading
            for n in updatedGrids:
                x, y = n[0], n[1]
                self.ui.drawGrid(x, y)

            time.sleep(0.1)
            self.robot.moveForward()
            self.ui.drawRobot()

            i += 1

        #     print("Determining next move...")
        #     print("Robot is in action...")