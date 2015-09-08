import tkinter
import ArenaMap
import MapDescriptor
import threading
import time
from GridState import *
from RobotOrientation import *

__author__ = 'ECAND_000'

# Solution for threading (so that mainloop() does not block) --> http://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop

# THIS MAINUI CLASS IS USEFUL WHEN YOU WANT TO USE AN EXISTING MAP DESCRIPTOR TO INITIALIZE WHERE THE WALLS ARE
class MainUI(threading.Thread):
    GRID_EDGE_SIZE = 27
    GRID_BOTTOM_MOST = 560
    MARGIN_LEFT = 490
    MARGIN_RIGHT = 30
    MARGIN_TOP = 50
    MARGIN_BOTTOM = 50

    arenaMap = None
    robot = None
    root = None
    canvas = None
    rectangles = [[None for x in range (0, ArenaMap.ArenaMap.MAP_WIDTH)] for y in range (0, ArenaMap.ArenaMap.MAP_HEIGHT)]
    obstacleRectangles = [[None for x in range (0, ArenaMap.ArenaMap.MAP_WIDTH)] for y in range (0, ArenaMap.ArenaMap.MAP_HEIGHT)]
    startExploration = False

    def __init__(self, arenaMap, obstacleMap, robot):
        threading.Thread.__init__(self)
        self.arenaMap = arenaMap
        self.obstacleMap = obstacleMap
        self.robot = robot
        self.robotSpeed = 0.1
        self.maxPercentage = 100.00
        self.maxTime = 1000.00 # In seconds
        self.startTime = time.time() # Any initial time --> does not really matter since the starting time will be overwritten in self.startExplore()

    def open(self):
        self.start()

    def callback(self):
        self.root.quit()

    def startExplore(self):
        self.startExploration = True

        # Start timer
        self.startTime = time.time()

    def startExplorationWindow(self):
        self.canvas.delete("all")
        self.saveButton.destroy()
        self.loadMapButton.destroy()
        self.openExplorationWindow()

    def loadMapFromDisk(self):
        # Local mapDescriptor for obstacle initialization purpose
        mapDescriptor = MapDescriptor.MapDescriptor("MapDescriptor.in")

        # Since obstacleMap is initially empty (because it is initially for WallBuilder purpose), now we have to populate using the translated map
        self.obstacleMap.updateEntireMap(mapDescriptor.getTranslatedMap())
        self.startExplorationWindow()

    def run(self):
        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.wm_state('zoomed')

        self.canvas = tkinter.Canvas(width=self.root.winfo_screenwidth(), height=600, bg="white")
        self.canvas.pack()

        # Define Maze
        self.buildWall()
        self.root.mainloop()

    def buildWall(self):
        self.saveButton = tkinter.Button(self.root, text="Save Obstacles!", command=self.startExplorationWindow)
        self.saveButton.pack(side=tkinter.LEFT, ipadx=10, ipady=10, padx=10, pady=20)

        self.loadMapButton = tkinter.Button(self.root, text="Load Map!", command=self.loadMapFromDisk)
        self.loadMapButton.pack(side=tkinter.LEFT, ipadx=10, ipady=10, pady=20)

        # Initialize rectangles
        for i in range (0, ArenaMap.ArenaMap.MAP_HEIGHT):
            for j in range (0, ArenaMap.ArenaMap.MAP_WIDTH):
                self.obstacleRectangles[i][j] = self.canvas.create_rectangle(self.MARGIN_LEFT+ j * self.GRID_EDGE_SIZE,
                                                                     self.GRID_BOTTOM_MOST - i * self.GRID_EDGE_SIZE,
                                                                     self.MARGIN_LEFT + j * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                                                     self.GRID_BOTTOM_MOST - i * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                                                     outline="#000000",
                                                                     fill="#FFFFFF")

                self.canvas.tag_bind(self.obstacleRectangles[i][j], '<ButtonPress-1>', self.onGridClick)

    def openExplorationWindow(self):
        # Add Textbox for X moves / second here --> user selects X
        self.movesPerSecondBox = tkinter.Entry(self.root, width=5)
        self.movesPerSecondBox.pack(side=tkinter.LEFT, padx=20)
        self.movesPerSecondButton = tkinter.Button(self.root, text="Change Speed!", command=self.changeRobotSpeed)
        self.movesPerSecondButton.pack(side=tkinter.LEFT)

        # Initially it's 3.00 % since the start zone is basically already explored
        self.percentageLabel = tkinter.Label(self.root, text="3.00%")
        self.percentageLabel.pack(side=tkinter.LEFT, padx=10, ipadx=20)
        self.percentageStopBox = tkinter.Entry(self.root, width=7)
        self.percentageStopBox.pack(side=tkinter.LEFT, padx=20)
        self.percentageButton = tkinter.Button(self.root, text="Set Percentage!", command=self.setMaxPercentage)
        self.percentageButton.pack(side=tkinter.LEFT, padx=10)

        # Timer box
        self.timerStopBox = tkinter.Entry(self.root, width=7)
        self.timerStopBox.pack(side=tkinter.LEFT, padx=20)
        self.timerStopButton = tkinter.Button(self.root, text="Set Timeout!", command=self.setTimeout)
        self.timerStopButton.pack(side=tkinter.LEFT, padx=10)

        # Start Exploration button
        self.startButton = tkinter.Button(self.root, text="Explore!", command=self.startExplore)
        self.startButton.pack(ipadx=10, ipady=10, padx=200, pady=20, side=tkinter.LEFT)

        # Add button to save the user selectable X moves / second here

        # Initialize rectangles
        for i in range (0, ArenaMap.ArenaMap.MAP_HEIGHT):
            for j in range (0, ArenaMap.ArenaMap.MAP_WIDTH):
                self.rectangles[i][j] = self.canvas.create_rectangle(self.MARGIN_LEFT+ j * self.GRID_EDGE_SIZE,
                                                                     self.GRID_BOTTOM_MOST - i * self.GRID_EDGE_SIZE,
                                                                     self.MARGIN_LEFT + j * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                                                     self.GRID_BOTTOM_MOST - i * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                                                     outline="#000000",
                                                                     fill="#DDDDDD")

        self.draw()

    def onGridClick(self, event):
        mouseX = event.x
        mouseY = event.y

        posX = int((mouseX - self.MARGIN_LEFT) / self.GRID_EDGE_SIZE)
        posY = int((self.GRID_BOTTOM_MOST - mouseY) / self.GRID_EDGE_SIZE)

        if self.obstacleMap.getGridMap()[posY][posX].getGridState() == GridState.UNEXPLORED:
            self.obstacleMap.getGridMap()[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
        elif self.obstacleMap.getGridMap()[posY][posX].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
            self.obstacleMap.getGridMap()[posY][posX].setGridState(GridState.UNEXPLORED)

        self.drawObstacleGrid(posX, posY)

    def isStartExplore(self):
        return self.startExploration

    def changeRobotSpeed(self):
        read = self.movesPerSecondBox.get()
        if len(read) > 0:
            self.robotSpeed = 1 / int(read)

    def setMaxPercentage(self):
        read = self.percentageStopBox.get()
        if len(read) > 0:
            self.maxPercentage = int(read)

    def setMapPercentage(self):
        currentPercentage = self.arenaMap.getPercentageExploredGrids()
        self.percentageLabel["text"] = "{:.2f}%".format(self.arenaMap.getPercentageExploredGrids())

        # Stop whenever the current percentage is reached
        if currentPercentage >= self.maxPercentage:
            return False

        return True

    def setTimeout(self):
        read = self.timerStopBox.get()
        if len(read) > 0:
            self.maxTime = int(read)

    def checkTimeout(self):
        now = time.time()
        if (now - self.startTime) >= self.maxTime:
            return False

        return True

    def draw(self):
        self.drawMap()
        self.drawRobot()

    # Remember that point (0, 0) is the left bottom most grid
    def drawMap(self):
        for i in range (0, self.arenaMap.MAP_HEIGHT):
            for j in range (0, self.arenaMap.MAP_WIDTH):
                self.drawGrid(j, i)

    def drawGrid(self, x, y):
        gridState = self.arenaMap.getGridMap()[y][x].getGridState()
        if gridState == GridState.UNEXPLORED:
            fillColor = "#DDDDDD"
        elif gridState == GridState.EXPLORED_NO_OBSTACLE:
            fillColor = "#FFFFFF"
        elif gridState == GridState.EXPLORED_WITH_OBSTACLE:
            fillColor = "#333333"
        elif gridState == GridState.START_ZONE:
            fillColor = "#00FF00"
        elif gridState == GridState.END_ZONE or gridState == GridState.END_ZONE_EXPLORED:
            fillColor = "#FF0000"

        self.canvas.itemconfig(self.rectangles[y][x], fill=fillColor)

        return

    def drawObstacleGrid(self, x, y):
        gridState = self.obstacleMap.getGridMap()[y][x].getGridState()
        if gridState == GridState.UNEXPLORED:
            fillColor = "#FFFFFF"
        elif gridState == GridState.EXPLORED_WITH_OBSTACLE:
            fillColor = "#333333"

        self.canvas.itemconfig(self.obstacleRectangles[y][x], fill=fillColor)

    def drawRobot(self):
        robotOrientation = self.robot.getOrientation()
        # self.setMapPercentage()
        # timeoutStop = self.checkTimeout()
        time.sleep(self.robotSpeed)

        # DRAW WHITE RECTANGLES FOR THE ROBOT TRAIL --> ROBOT_CENTER.ROW - 2
        if robotOrientation == RobotOrientation.FRONT:
            positionX = self.robot.getPositionX()
            positionY = self.robot.getPositionY()

            if (self.robot.getPositionY() - 2) >= 0\
                and self.arenaMap.getGrid(positionY - 2, positionX - 1).getGridState() != GridState.EXPLORED_WITH_OBSTACLE\
                and self.arenaMap.getGrid(positionY - 2, positionX).getGridState() != GridState.EXPLORED_WITH_OBSTACLE\
                and self.arenaMap.getGrid(positionY - 2, positionX + 1).getGridState() != GridState.EXPLORED_WITH_OBSTACLE:

                for i in range (-1, 2):
                    fillColor = ""
                    if self.arenaMap.getGridMap()[positionY - 2][positionX + i].getGridState() == GridState.UNEXPLORED:
                        fillColor = "#DDDDDD"
                    elif self.arenaMap.getGridMap()[positionY - 2][positionX + i].getGridState() == GridState.EXPLORED_NO_OBSTACLE:
                        fillColor = "#FFFFFF"
                    elif self.arenaMap.getGridMap()[positionY - 2][positionX + i].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                        fillColor = "#333333"
                    elif self.arenaMap.getGridMap()[positionY - 2][positionX + i].getGridState() == GridState.START_ZONE:
                        fillColor = "#00FF00"
                    elif self.arenaMap.getGridMap()[positionY - 2][positionX + i].getGridState() == GridState.END_ZONE\
                         or self.arenaMap.getGridMap()[positionY - 2][positionX + i].getGridState() == GridState.END_ZONE_EXPLORED:
                        fillColor = "#FF0000"

                    self.canvas.itemconfig(self.rectangles[positionY - 2][positionX + i], fill=fillColor)

        # DRAW WHITE RECTANGLES FOR THE ROBOT TRAIL --> ROBOT_CENTER.ROW + 2
        elif robotOrientation == RobotOrientation.BACK:
            positionX = self.robot.getPositionX()
            positionY = self.robot.getPositionY()

            if (self.robot.getPositionY() + 2) <= ArenaMap.ArenaMap.MAP_HEIGHT - 1\
                and self.arenaMap.getGrid(positionY + 2, positionX - 1).getGridState() != GridState.EXPLORED_WITH_OBSTACLE\
                and self.arenaMap.getGrid(positionY + 2, positionX).getGridState() != GridState.EXPLORED_WITH_OBSTACLE\
                and self.arenaMap.getGrid(positionY + 2, positionX + 1).getGridState() != GridState.EXPLORED_WITH_OBSTACLE:

                for i in range (-1, 2):
                    fillColor = ""
                    if self.arenaMap.getGridMap()[positionY + 2][positionX + i].getGridState() == GridState.UNEXPLORED:
                        fillColor = "#DDDDDD"
                    elif self.arenaMap.getGridMap()[positionY + 2][positionX + i].getGridState() == GridState.EXPLORED_NO_OBSTACLE:
                        fillColor = "#FFFFFF"
                    elif self.arenaMap.getGridMap()[positionY + 2][positionX + i].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                        fillColor = "#333333"
                    elif self.arenaMap.getGridMap()[positionY + 2][positionX + i].getGridState() == GridState.START_ZONE:
                        fillColor = "#00FF00"
                    elif self.arenaMap.getGridMap()[positionY + 2][positionX + i].getGridState() == GridState.END_ZONE\
                         or self.arenaMap.getGridMap()[positionY + 2][positionX + i].getGridState() == GridState.END_ZONE_EXPLORED:
                        fillColor = "#FF0000"

                    self.canvas.itemconfig(self.rectangles[positionY + 2][positionX + i], fill=fillColor)

        # DRAW WHITE RECTANGLES FOR THE ROBOT TRAIL --> ROBOT_CENTER.COL + 2
        elif robotOrientation == RobotOrientation.LEFT:
            positionX = self.robot.getPositionX()
            positionY = self.robot.getPositionY()

            if (self.robot.getPositionX() + 2) <= ArenaMap.ArenaMap.MAP_WIDTH - 1\
                and self.arenaMap.getGrid(positionY - 1, positionX + 2).getGridState() != GridState.EXPLORED_WITH_OBSTACLE\
                and self.arenaMap.getGrid(positionY, positionX + 2).getGridState() != GridState.EXPLORED_WITH_OBSTACLE\
                and self.arenaMap.getGrid(positionY + 1, positionX + 2).getGridState() != GridState.EXPLORED_WITH_OBSTACLE:

                for i in range (-1, 2):
                    fillColor = ""
                    if self.arenaMap.getGridMap()[positionY + i][positionX + 2].getGridState() == GridState.UNEXPLORED:
                        fillColor = "#DDDDDD"
                    elif self.arenaMap.getGridMap()[positionY + i][positionX + 2].getGridState() == GridState.EXPLORED_NO_OBSTACLE:
                        fillColor = "#FFFFFF"
                    elif self.arenaMap.getGridMap()[positionY + i][positionX + 2].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                        fillColor = "#333333"
                    elif self.arenaMap.getGridMap()[positionY + i][positionX + 2].getGridState() == GridState.START_ZONE:
                        fillColor = "#00FF00"
                    elif self.arenaMap.getGridMap()[positionY + i][positionX + 2].getGridState() == GridState.END_ZONE \
                         or self.arenaMap.getGridMap()[positionY + i][positionX + 2].getGridState() == GridState.END_ZONE_EXPLORED:
                        fillColor = "#FF0000"

                    self.canvas.itemconfig(self.rectangles[positionY + i][positionX + 2], fill=fillColor)

        # DRAW WHITE RECTANGLES FOR THE ROBOT TRAIL --> ROBOT_CENTER.COL - 2
        elif robotOrientation == RobotOrientation.RIGHT:
            positionX = self.robot.getPositionX()
            positionY = self.robot.getPositionY()

            if (self.robot.getPositionX() - 2) >= 0\
                and self.arenaMap.getGrid(positionY - 1, positionX - 2).getGridState() != GridState.EXPLORED_WITH_OBSTACLE\
                and self.arenaMap.getGrid(positionY, positionX - 2).getGridState() != GridState.EXPLORED_WITH_OBSTACLE\
                and self.arenaMap.getGrid(positionY + 1, positionX - 2).getGridState() != GridState.EXPLORED_WITH_OBSTACLE:

                for i in range (-1, 2):
                    fillColor = ""
                    if self.arenaMap.getGridMap()[positionY + i][positionX - 2].getGridState() == GridState.UNEXPLORED:
                        fillColor = "#DDDDDD"
                    elif self.arenaMap.getGridMap()[positionY + i][positionX - 2].getGridState() == GridState.EXPLORED_NO_OBSTACLE:
                        fillColor = "#FFFFFF"
                    elif self.arenaMap.getGridMap()[positionY + i][positionX - 2].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                        fillColor = "#333333"
                    elif self.arenaMap.getGridMap()[positionY + i][positionX - 2].getGridState() == GridState.START_ZONE:
                        fillColor = "#00FF00"
                    elif self.arenaMap.getGridMap()[positionY + i][positionX - 2].getGridState() == GridState.END_ZONE\
                         or self.arenaMap.getGridMap()[positionY + i][positionX - 2].getGridState() == GridState.END_ZONE_EXPLORED:
                        fillColor = "#FF0000"

                    self.canvas.itemconfig(self.rectangles[positionY + i][positionX - 2], fill=fillColor)

        # Draw ROBOT
        for i in range (-1, 2):
            for j in range (-1, 2):
                self.canvas.itemconfig(self.rectangles[self.robot.getPositionY() + i][self.robot.getPositionX() + j], fill="#0000FF")

        # Draw the robot orientation
        robotOrientation = self.robot.getOrientation()
        if robotOrientation == RobotOrientation.FRONT:
            self.canvas.itemconfig(self.rectangles[self.robot.getPositionY() + 1][self.robot.getPositionX()], fill="#9FDDEC")
        elif robotOrientation == RobotOrientation.BACK:
            self.canvas.itemconfig(self.rectangles[self.robot.getPositionY() - 1][self.robot.getPositionX()], fill="#9FDDEC")
        elif robotOrientation == RobotOrientation.LEFT:
            self.canvas.itemconfig(self.rectangles[self.robot.getPositionY()][self.robot.getPositionX() - 1], fill="#9FDDEC")
        elif robotOrientation == RobotOrientation.RIGHT:
            self.canvas.itemconfig(self.rectangles[self.robot.getPositionY()][self.robot.getPositionX() + 1], fill="#9FDDEC")