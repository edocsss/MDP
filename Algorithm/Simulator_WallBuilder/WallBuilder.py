import tkinter
import ArenaMap as ArenaMap
import threading
import RobotController as RobotController
from GridState import *
from RobotOrientation import *

__author__ = 'ECAND_000'

# Solution for threading (so that mainloop() does not block) --> http://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop

# THIS MAINUI CLASS IS USEFUL WHEN YOU WANT TO USE AN EXISTING MAP DESCRIPTOR TO INITIALIZE WHERE THE WALLS ARE
class WallBuilder(threading.Thread):
    GRID_EDGE_SIZE = 27
    GRID_BOTTOM_MOST = 560
    MARGIN_LEFT = 50
    MARGIN_RIGHT = 30
    MARGIN_TOP = 50
    MARGIN_BOTTOM = 50

    root = None
    canvas = None
    rectangles = [[None for x in range (0, ArenaMap.ArenaMap.MAP_WIDTH)] for y in range (0, ArenaMap.ArenaMap.MAP_HEIGHT)]
    next = False

    def __init__(self, obstacleMap):
        threading.Thread.__init__(self)
        self.obstacleMap = obstacleMap
        self.start()

    def callback(self):
        self.alive = False
        self.root.quit()

    def startExplorationWindow(self):
        self.next = True
        self.alive = False
        self.root.quit()

    def run(self):
        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        self.canvas = tkinter.Canvas(width=510, height=600, bg="white")
        self.canvas.grid(column=0, row=0)

        saveButton = tkinter.Button(self.root, text="Save Obstacles!", command=self.startExplorationWindow)
        saveButton.grid(row=2, columnspan=5, ipadx=10, ipady=10, pady=20)

        # Initialize rectangles
        for i in range (0, ArenaMap.ArenaMap.MAP_HEIGHT):
            for j in range (0, ArenaMap.ArenaMap.MAP_WIDTH):
                self.rectangles[i][j] = self.canvas.create_rectangle(self.MARGIN_LEFT+ j * self.GRID_EDGE_SIZE,
                                                                     self.GRID_BOTTOM_MOST - i * self.GRID_EDGE_SIZE,
                                                                     self.MARGIN_LEFT + j * self.GRID_EDGE_SIZE + self.GRID_EDGE_SIZE,
                                                                     self.GRID_BOTTOM_MOST - i * self.GRID_EDGE_SIZE - self.GRID_EDGE_SIZE,
                                                                     outline="#000000",
                                                                     fill="#FFFFFF")

                self.canvas.tag_bind(self.rectangles[i][j], '<ButtonPress-1>', self.onGridClick)

        self.root.mainloop()

    def isStartExplorationWindow(self):
        return self.next

    def onGridClick(self, event):
        mouseX = event.x
        mouseY = event.y

        posX = int((mouseX - self.MARGIN_LEFT) / self.GRID_EDGE_SIZE)
        posY = int((self.GRID_BOTTOM_MOST - mouseY) / self.GRID_EDGE_SIZE)

        if self.obstacleMap.getGridMap()[posY][posX].getGridState() == GridState.UNEXPLORED:
            self.obstacleMap.getGridMap()[posY][posX].setGridState(GridState.EXPLORED_WITH_OBSTACLE)
        elif self.obstacleMap.getGridMap()[posY][posX].getGridState() == GridState.EXPLORED_WITH_OBSTACLE:
            self.obstacleMap.getGridMap()[posY][posX].setGridState(GridState.UNEXPLORED)

        self.drawGrid(posX, posY)

    def drawGrid(self, x, y):
        gridState = self.obstacleMap.getGridMap()[y][x].getGridState()
        if gridState == GridState.UNEXPLORED:
            fillColor = "#FFFFFF"
        elif gridState == GridState.EXPLORED_WITH_OBSTACLE:
            fillColor = "#333333"

        self.canvas.itemconfig(self.rectangles[y][x], fill=fillColor)