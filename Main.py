import random
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtTest

import utils
from a_star import calculate as aStarCalculate
from breadth_first_search import calculate as bfsCalculate
from depth_first_search import calculate as dfsCalculate
from dijkstras_algorithm import calculate as djkCalculate

qtcreator_file = "mainWindow.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

GRIDSIZE = 64

# dictionary with implemented algorithms, when adding a new one we can update the dict only once
ALGORITHMS = {"Breadth First Search": bfsCalculate,
              "Depth First Search": dfsCalculate,
              "Dijkstra's Algorithm": djkCalculate,
              "A* (Manhattan distance)": aStarCalculate,
              "A* (Euclidean distance)": lambda grid, start, goal: aStarCalculate(grid, start, goal,
                                                                                  heuristic="euclidean")}


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Buttons

        self.runPathFinding.clicked.connect(self.runAlgorithm)
        self.setCoordinates.clicked.connect(self.showCoordinates)
        self.setRandomCoordinates.clicked.connect(self.randomCoordinates)
        self.runPathFinding.setEnabled(False)
        # Combobox
        for algorithm in ALGORITHMS.keys():
            self.chooseAlgorithm.addItem(algorithm)
        # Visual UI
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        # colors
        penGrid = QtGui.QPen(QtCore.Qt.black)

        # Draw Grid
        side = 10
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                r = QtCore.QRectF(QtCore.QPointF(
                    i * side, j * side), QtCore.QSizeF(side, side))
                scene.addRect(r, penGrid)

    def showCoordinates(self):
        # Check if there are values to the boxes.
        # inputs to values
        Xstart = int(self.startXValue.toPlainText())
        Ystart = int(self.startYValue.toPlainText())
        Xgoal = int(self.goalXValue.toPlainText())
        Ygoal = int(self.goalYValue.toPlainText())
        # enable scene to draw
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        # colors
        penGrid = QtGui.QPen(QtCore.Qt.black)
        penPoint = QtGui.QPen(QtCore.Qt.red)
        pointBrushEnd = QtGui.QBrush(QtCore.Qt.green)
        pointBrushStart = QtGui.QBrush(QtCore.Qt.blue)
        # Grid
        side = 10
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                r = QtCore.QRectF(QtCore.QPointF(
                    i * side, j * side), QtCore.QSizeF(side, side))
                scene.addRect(r, penGrid)
        # Draw Start and End node
        scene.addRect(int(Xstart * side), int(Ystart * side),
                      10, 10, penPoint, pointBrushStart)
        scene.addRect(int(Xgoal * side), int(Ygoal * side),
                      10, 10, penPoint, pointBrushEnd)
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
        # enable scene to draw
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        # colors
        penGrid = QtGui.QPen(QtCore.Qt.black)
        penPoint = QtGui.QPen(QtCore.Qt.red)
        pointBrushEnd = QtGui.QBrush(QtCore.Qt.green)
        pointBrushStart = QtGui.QBrush(QtCore.Qt.blue)
        # Grid
        side = 10
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                r = QtCore.QRectF(QtCore.QPointF(
                    i * side, j * side), QtCore.QSizeF(side, side))
                scene.addRect(r, penGrid)
        # Draw Start and End node
        scene.addRect(int(Xstart * side), int(Ystart * side),
                      10, 10, penPoint, pointBrushStart)
        scene.addRect(int(Xgoal * side), int(Ygoal * side),
                      10, 10, penPoint, pointBrushEnd)
        self.runPathFinding.setEnabled(True)

    def runAlgorithm(self):
        self.runPathFinding.setEnabled(False)
        # inputs to values
        Xstart = int(self.startXValue.toPlainText())
        Ystart = int(self.startYValue.toPlainText())
        Xgoal = int(self.goalXValue.toPlainText())
        Ygoal = int(self.goalYValue.toPlainText())
        # assign to variables to run Algo
        startingPoint = (Xstart, Ystart)
        goalPoint = (Xgoal, Ygoal)
        grid = utils.new_grid(GRIDSIZE)
        text = self.chooseAlgorithm.currentText()
        result = ALGORITHMS[text](grid, startingPoint, goalPoint)
        # enable scene to draw
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        penGrid = QtGui.QPen(QtCore.Qt.black)
        penVisited = QtGui.QPen(QtCore.Qt.darkRed)
        penPoint = QtGui.QPen(QtCore.Qt.red)
        pointBrushvisited = QtGui.QBrush(QtCore.Qt.white)
        pointBrushEnd = QtGui.QBrush(QtCore.Qt.green)
        pointBrushStart = QtGui.QBrush(QtCore.Qt.blue)
        # Draw grid
        side = 10
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                r = QtCore.QRectF(QtCore.QPointF(
                    i * side, j * side), QtCore.QSizeF(side, side))
                scene.addRect(r, penGrid)
                # draw path
        pointBrushPath = QtGui.QBrush(QtCore.Qt.black)
        correctPath = result.get("path")
        visited = result.get("visited")
        # print (visited)
        scene.addRect(int(Xstart * side), int(Ystart * side),
                      10, 10, penPoint, pointBrushStart)
        scene.addRect(int(Xgoal * side), int(Ygoal * side),
                      10, 10, penPoint, pointBrushEnd)
        for x, y in visited:
            QtTest.QTest.qWait(5)
            scene.addRect(x * side, y * side, 10, 10,
                          penVisited, pointBrushvisited)
            scene.addRect(int(Xstart * side), int(Ystart * side),
                          10, 10, penPoint, pointBrushStart)
        # print (correctPath)
        for x, y in correctPath:
            scene.addRect(x * side, y * side, 10, 10, penPoint, pointBrushPath)
        # Draw end and start nodes
        scene.addRect(int(Xstart * side), int(Ystart * side),
                      10, 10, penPoint, pointBrushStart)
        scene.addRect(int(Xgoal * side), int(Ygoal * side),
                      10, 10, penPoint, pointBrushEnd)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
