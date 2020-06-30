import random
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtTest

import path_finding_algorithms.utils as utils
from path_finding_algorithms.a_star import calculate2 as aStarCalculate
from path_finding_algorithms.breadth_first_search import calculate2 as bfsCalculate
from path_finding_algorithms.depth_first_search import calculate2 as dfsCalculate
from path_finding_algorithms.dijkstras_algorithm import calculate2 as djkCalculate

qtcreator_file = "main_window.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)
GRIDSIZE = 64
SIDE = 10

# dictionary with implemented algorithms, when adding a new one we can update the dict only once
ALGORITHMS = {"Breadth First Search": bfsCalculate,
              "Depth First Search": dfsCalculate,
              "Dijkstra's Algorithm": djkCalculate,
              "A* (Manhattan distance)": aStarCalculate,
              "A* (Euclidean distance)": lambda grid, start, goal: aStarCalculate(grid, start, goal,
                                                                                  heuristic="euclidean")}
app = QtWidgets.QApplication(sys.argv)
scene = QtWidgets.QGraphicsScene()
penPoint = QtGui.QPen(QtCore.Qt.red)
pointBrushEnd = QtGui.QBrush(QtCore.Qt.green)
pointBrushStart = QtGui.QBrush(QtCore.Qt.blue)
penGrid = QtGui.QPen(QtCore.Qt.black)
penVisited = QtGui.QPen(QtCore.Qt.darkRed)
pointBrushvisited = QtGui.QBrush(QtCore.Qt.white)
pointBrushPath = QtGui.QBrush(QtCore.Qt.black)
wallBrush = QtGui.QBrush(QtCore.Qt.darkYellow)
gridBrush = QtGui.QBrush(QtCore.Qt.lightGray)
maze = False
grid = utils.Grid()


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Buttons
        self.runPathFinding.clicked.connect(self.runAlgorithm)
        self.setCoordinates.clicked.connect(self.showCoordinates)
        self.setRandomCoordinates.clicked.connect(self.randomCoordinates)
        self.generateMaze.clicked.connect(self.generateMazes)
        self.runPathFinding.setEnabled(False)
        self.startXValue.setPlainText("0")
        self.startYValue.setPlainText("0")
        self.goalXValue.setPlainText("63")
        self.goalYValue.setPlainText("63")
        # Combobox
        for algorithm in ALGORITHMS.keys():
            self.chooseAlgorithm.addItem(algorithm)
        # GridDraw
        self.drawGrid(scene, penGrid, SIDE)

    def showCoordinates(self):
        # Check if there are values to the boxes.
        # inputs to values
        if not(int(self.startXValue.toPlainText()) >= 0 and int(self.startXValue.toPlainText()) < 64):
            self.startXValue.setPlainText("0")
        if not(int(self.startYValue.toPlainText()) >= 0 and int(self.startYValue.toPlainText()) < 64):
            self.startYValue.setPlainText("0")
        if not(int(self.goalXValue.toPlainText()) >= 0 and int(self.goalXValue.toPlainText()) < 64):
            self.goalXValue.setPlainText("63")
        if not(int(self.goalYValue.toPlainText()) >= 0 and int(self.goalYValue.toPlainText()) < 64):
            self.goalYValue.setPlainText("63")
        Xstart = int(self.startXValue.toPlainText())
        Ystart = int(self.startYValue.toPlainText())
        Xgoal = int(self.goalXValue.toPlainText())
        Ygoal = int(self.goalYValue.toPlainText())
        # GridDraw
        window.drawGrid(scene, penGrid, SIDE)
        window.drawStartEndNodes(Xstart, Ystart, Xgoal, Ygoal,
                                 penPoint, pointBrushStart, pointBrushEnd)
        self.runPathFinding.setEnabled(True)

    def randomCoordinates(self):
        # Chose Random value
        Xstart = int(random.uniform(0, 64))
        Ystart = int(random.uniform(0, 64))
        Xgoal = int(random.uniform(0, 64))
        Ygoal = int(random.uniform(0, 64))
        # add Random value to text inputs
        self.startXValue.setPlainText(str(Xstart))
        self.startYValue.setPlainText(str(Ystart))
        self.goalXValue.setPlainText(str(Xgoal))
        self.goalYValue.setPlainText(str(Ygoal))
        # Draw
        window.drawGrid(scene, penGrid, SIDE)
        window.drawStartEndNodes(Xstart, Ystart, Xgoal, Ygoal,
                                 penPoint, pointBrushStart, pointBrushEnd)
        self.runPathFinding.setEnabled(True)

    def runAlgorithm(self):
        self.runPathFinding.setEnabled(False)
        window.setCoordinates.setEnabled(False)
        window.setRandomCoordinates.setEnabled(False)
        window.generateMaze.setEnabled(False)
        # inputs to values
        Xstart = int(self.startXValue.toPlainText())
        Ystart = int(self.startYValue.toPlainText())
        Xgoal = int(self.goalXValue.toPlainText())
        Ygoal = int(self.goalYValue.toPlainText())
        # assign to variables to run Algo
        startingPoint = (Xstart, Ystart)
        goalPoint = (Xgoal, Ygoal)
        text = self.chooseAlgorithm.currentText()
        result = ALGORITHMS[text](startingPoint, goalPoint, grid)
        # enable scene to draw
        window.drawGrid(scene, penGrid, SIDE)
        # Draw grid
        window.drawStartEndNodes(Xstart, Ystart, Xgoal, Ygoal,
                                 penPoint, pointBrushStart, pointBrushEnd)
        # Get paths
        correctPath = result.get("path")
        visited = result.get("visited")
        # GridDrawVisited
        window.drawVisited(Xstart, Ystart, Xgoal, Ygoal,
                           penPoint, pointBrushStart, pointBrushEnd, penVisited, pointBrushvisited, visited, correctPath, SIDE)
        self.runPathFinding.setEnabled(True)
        window.setCoordinates.setEnabled(True)
        window.setRandomCoordinates.setEnabled(True)
        window.generateMaze.setEnabled(True)

    def drawGrid(self, scene, penGrid, SIDE):
        self.graphicsView.setScene(scene)
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                r = QtCore.QRectF(QtCore.QPointF(
                    i * SIDE, j * SIDE), QtCore.QSizeF(SIDE, SIDE))
                scene.addRect(r, penGrid)
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                scene.addRect(j * SIDE, i * SIDE, 10, 10,
                              penPoint, gridBrush)
        for y in range(GRIDSIZE):
            for x in range(GRIDSIZE):
                if grid.to_ndarray()[y, x] == grid.WALL:
                    # print wall
                    scene.addRect(x * SIDE, y * SIDE, 10, 10,
                                  penPoint, wallBrush)
                else:
                    # print path
                    pass

    def drawStartEndNodes(self, Xstart, Ystart, Xgoal, Ygoal, penPoint, pointBrushStart, pointBrushEnd):
        scene.clear()
        window.drawGrid(scene, penGrid, SIDE)
        scene.addRect(int(Xstart * SIDE), int(Ystart * SIDE),
                      10, 10, penPoint, pointBrushStart)
        scene.addRect(int(Xgoal * SIDE), int(Ygoal * SIDE),
                      10, 10, penPoint, pointBrushEnd)

    def drawVisited(self, Xstart, Ystart, Xgoal, Ygoal,
                    penPoint, pointBrushStart, pointBrushEnd, penVisited, pointBrushvisited, visited, correctPath, SIDE):
        scene.addRect(int(Xstart * SIDE), int(Ystart * SIDE),
                      10, 10, penPoint, pointBrushStart)
        scene.addRect(int(Xgoal * SIDE), int(Ygoal * SIDE),
                      10, 10, penPoint, pointBrushEnd)
        for x, y in visited:
            QtTest.QTest.qWait(5)
            scene.addRect(x * SIDE, y * SIDE, 10, 10,
                          penVisited, pointBrushvisited)
            scene.addRect(int(Xstart * SIDE), int(Ystart * SIDE),
                          10, 10, penPoint, pointBrushStart)
        for x, y in correctPath:
            scene.addRect(x * SIDE, y * SIDE, 10, 10, penPoint, pointBrushPath)
        scene.addRect(int(Xstart * SIDE), int(Ystart * SIDE),
                      10, 10, penPoint, pointBrushStart)
        scene.addRect(int(Xgoal * SIDE), int(Ygoal * SIDE),
                      10, 10, penPoint, pointBrushEnd)

    def generateMazes(self):
        global maze
        maze = True
        global grid
        grid = utils.Grid(create_maze=True, size=GRIDSIZE)
        maze_history = grid.get_maze_history()
        for y in range(GRIDSIZE):
            for x in range(GRIDSIZE):
                scene.addRect(x * SIDE, y * SIDE, 10, 10,
                              penPoint, wallBrush)
        for x, y in maze_history:
            QtTest.QTest.qWait(3)
            scene.addRect(y * SIDE, x * SIDE, 10, 10,
                          penPoint, gridBrush)


if __name__ == "__main__":
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
