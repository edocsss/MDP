import tkinter
import ArenaMap
import threading
from GridState import *
from RobotOrientation import *

__author__ = 'ECAND_000'

# Solution for threading (so that mainloop() does not block) --> http://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
class MainUI(threading.Thread):
    GRID_EDGE_SIZE = 27
    GRID_BOTTOM_MOST = 560
    MARGIN_LEFT = 50
    MARGIN_RIGHT = 30
    MARGIN_TOP = 50
    MARGIN_BOTTOM = 50

    arenaMap = None
    robot = None
    root = None
    canvas = None

    def __init__(self, arenaMap, robot):
        threading.Thread.__init__(self)
        self.arenaMap = arenaMap
        self.robot = robot
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        self.canvas = tkinter.Canvas(width=800, height=630, bg="white")
        self.canvas.pack()

        self.draw()
        self.root.mainloop()

    def draw(self):
        self.drawMap()
        self.drawRobot()

    # Remember that point (0, 0) is the left bottom most grid
    def drawMap(self):
        gridMap = self.arenaMap.getGridMap()
        for i in range (0, self.arenaMap.MAP_HEIGHT):
            for j in range (0, self.arenaMap.MAP_WIDTH):
                g = gridMap[i][j]

                # Determine the grid color
                if g.getGridState() == GridState.UNEXPLORED:
                    fillColor = "#FF0000"
                elif g.getGridState() == GridState.EXPLORED_NO_OBSTACLE:
                    fillColor = "#FFFFFF"
                elif g.getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
                    fillColor = "#333333"

                self.canvas.create_rectangle(self.MARGIN_LEFT + j * self.GRID_EDGE_SIZE,
                                             self.GRID_BOTTOM_MOST - i * self.GRID_EDGE_SIZE,
                                             self.MARGIN_LEFT + j * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                             self.GRID_BOTTOM_MOST - i * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                             outline="#000000",
                                             fill="" + fillColor)

        self.canvas.pack()

    def drawGrid(self, grid):
        if grid.getGridState() == GridState.UNEXPLORED:
            fillColor = "#FF0000"
        elif grid.getGridState() == GridState.EXPLORED_NO_OBSTACLE:
            fillColor = "#FFFFFF"
        elif grid.getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
            fillColor = "#333333"

        self.canvas.create_rectangle(self.MARGIN_LEFT + grid.getX() * self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - grid.getY() * self.GRID_EDGE_SIZE,
                                     self.MARGIN_LEFT + grid.getX() * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - grid.getY() * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                     outline="#000000",
                                     fill="" + fillColor)
        return

    # NEED A WAY SUCH THAT WHEN THE ROBOT IS DRAWN, ONLY THE MAP RELATED TO THE ROBOT IS REDRAWN, NOT THE ENTIRE MAP!!
    def drawRobot(self):
        robotOrientation = self.robot.getOrientation()
        fillFront = fillLeft = fillRight = fillBack = "#FF0000"
        trailX = trailY = -1

        # DRAW WHITE RECTANGLES FOR THE ROBOT TRAIL --> ROBOT_CENTER.ROW - 2
        if robotOrientation == RobotOrientation.FRONT:
            fillFront = "#00FF00"

            if (self.robot.getPositionY() - 2) >= 0:
                self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() - 1) * self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 2) * self.GRID_EDGE_SIZE,
                                         self.MARGIN_LEFT + (self.robot.getPositionX() - 1) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 2) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                         outline="#000000",
                                         fill="#FFFFFF")

                self.canvas.create_rectangle(self.MARGIN_LEFT + self.robot.getPositionX() * self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 2) * self.GRID_EDGE_SIZE,
                                         self.MARGIN_LEFT + self.robot.getPositionX() * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 2) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                         outline="#000000",
                                         fill="#FFFFFF")

                self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() + 1) * self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 2) * self.GRID_EDGE_SIZE,
                                         self.MARGIN_LEFT + (self.robot.getPositionX() + 1) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 2) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                         outline="#000000",
                                         fill="#FFFFFF")

        # DRAW WHITE RECTANGLES FOR THE ROBOT TRAIL --> ROBOT_CENTER.ROW + 2
        elif robotOrientation == RobotOrientation.BACK:
            fillBack = "#00FF00"

            if (self.robot.getPositionY() + 2) >= ArenaMap.ArenaMap.MAP_HEIGHT - 1:
                self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() - 1) * self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 2) * self.GRID_EDGE_SIZE,
                                         self.MARGIN_LEFT + (self.robot.getPositionX() - 1) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 2) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                         outline="#000000",
                                         fill="#FFFFFF")

                self.canvas.create_rectangle(self.MARGIN_LEFT + self.robot.getPositionX() * self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 2) * self.GRID_EDGE_SIZE,
                                         self.MARGIN_LEFT + self.robot.getPositionX() * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 2) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                         outline="#000000",
                                         fill="#FFFFFF")

                self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() + 1) * self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 2) * self.GRID_EDGE_SIZE,
                                         self.MARGIN_LEFT + (self.robot.getPositionX() + 1) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 2) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                         outline="#000000",
                                         fill="#FFFFFF")

        # DRAW WHITE RECTANGLES FOR THE ROBOT TRAIL --> ROBOT_CENTER.COL + 2
        elif robotOrientation == RobotOrientation.LEFT:
            fillLeft = "#00FF00"

            if (self.robot.getPositionX() + 2) >= ArenaMap.ArenaMap.MAP_WIDTH - 1:
                self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() + 2) * self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 1) * self.GRID_EDGE_SIZE,
                                         self.MARGIN_LEFT + (self.robot.getPositionX() + 2) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 1) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                         outline="#000000",
                                         fill="#FFFFFF")

                self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() + 2) * self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - self.robot.getPositionY() * self.GRID_EDGE_SIZE,
                                         self.MARGIN_LEFT + (self.robot.getPositionX() + 2) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - self.robot.getPositionY()  * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                         outline="#000000",
                                         fill="#FFFFFF")

                self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() + 2) * self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 1) * self.GRID_EDGE_SIZE,
                                         self.MARGIN_LEFT + (self.robot.getPositionX() + 2) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 1) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                         outline="#000000",
                                         fill="#FFFFFF")

        # DRAW WHITE RECTANGLES FOR THE ROBOT TRAIL --> ROBOT_CENTER.COL - 2
        elif robotOrientation == RobotOrientation.RIGHT:
            fillRight = "#00FF00"

            if (self.robot.getPositionX() - 2) >= 0:
                self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() - 2) * self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 1) * self.GRID_EDGE_SIZE,
                                         self.MARGIN_LEFT + (self.robot.getPositionX() - 2) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 1) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                         outline="#000000",
                                         fill="#FFFFFF")

                self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() - 2) * self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - self.robot.getPositionY() * self.GRID_EDGE_SIZE,
                                         self.MARGIN_LEFT + (self.robot.getPositionX() - 2) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - self.robot.getPositionY() * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                         outline="#000000",
                                         fill="#FFFFFF")

                self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() - 2) * self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 1) * self.GRID_EDGE_SIZE,
                                         self.MARGIN_LEFT + (self.robot.getPositionX() - 2) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                         self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 1) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                         outline="#000000",
                                         fill="#FFFFFF")

        # Draw center
        self.canvas.create_rectangle(self.MARGIN_LEFT + self.robot.getPositionX() * self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - self.robot.getPositionY() * self.GRID_EDGE_SIZE,
                                     self.MARGIN_LEFT + self.robot.getPositionX() * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - self.robot.getPositionY() * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                     outline="#000000",
                                     fill="#FF0000")

        # Draw left
        self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() - 1) * self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - self.robot.getPositionY() * self.GRID_EDGE_SIZE,
                                     self.MARGIN_LEFT + (self.robot.getPositionX() - 1) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - self.robot.getPositionY() * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                     outline="#000000",
                                     fill=fillLeft)

        # Draw upper left
        self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() - 1) * self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 1) * self.GRID_EDGE_SIZE,
                                     self.MARGIN_LEFT + (self.robot.getPositionX() - 1) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 1) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                     outline="#000000",
                                     fill="#FF0000")

        # Draw up
        self.canvas.create_rectangle(self.MARGIN_LEFT + self.robot.getPositionX() * self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 1) * self.GRID_EDGE_SIZE,
                                     self.MARGIN_LEFT + self.robot.getPositionX() * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 1) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                     outline="#000000",
                                     fill=fillFront)

        # Draw upper right
        self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() + 1) * self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 1) * self.GRID_EDGE_SIZE,
                                     self.MARGIN_LEFT + (self.robot.getPositionX() + 1) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - (self.robot.getPositionY() + 1) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                     outline="#000000",
                                     fill="#FF0000")

        # Draw right
        self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() + 1) * self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - self.robot.getPositionY() * self.GRID_EDGE_SIZE,
                                     self.MARGIN_LEFT + (self.robot.getPositionX() + 1) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - self.robot.getPositionY() * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                     outline="#000000",
                                     fill=fillRight)

        # Draw bottom right
        self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() + 1) * self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 1) * self.GRID_EDGE_SIZE,
                                     self.MARGIN_LEFT + (self.robot.getPositionX() + 1) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 1) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                     outline="#000000",
                                     fill="#FF0000")

        # Draw bottom
        self.canvas.create_rectangle(self.MARGIN_LEFT + self.robot.getPositionX() * self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 1) * self.GRID_EDGE_SIZE,
                                     self.MARGIN_LEFT + self.robot.getPositionX() * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 1) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                     outline="#000000",
                                     fill=fillBack)

        # Draw bottom left
        self.canvas.create_rectangle(self.MARGIN_LEFT + (self.robot.getPositionX() - 1) * self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 1) * self.GRID_EDGE_SIZE,
                                     self.MARGIN_LEFT + (self.robot.getPositionX() - 1) * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                     self.GRID_BOTTOM_MOST - (self.robot.getPositionY() - 1) * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                     outline="#000000",
                                     fill="#FF0000")