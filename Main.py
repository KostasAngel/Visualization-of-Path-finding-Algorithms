import random
import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtTest
from PyQt5.QtGui import QColor, QImage, QPainter

import path_finding_algorithms.utils as utils
from path_finding_algorithms.a_star import calculate as aStarCalculate
from path_finding_algorithms.breadth_first_search import calculate as bfsCalculate
from path_finding_algorithms.depth_first_search import calculate as dfsCalculate
from path_finding_algorithms.dijkstras_algorithm import calculate as djkCalculate

qtcreator_file = "main_window.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)
GRIDSIZE = 64
SIDE = 10

# dictionary with implemented algorithms, when adding a new one we can update the dict only once
ALGORITHMS = {"Breadth First Search": bfsCalculate,
              "Depth First Search": dfsCalculate,
              "Dijkstra's Algorithm": djkCalculate,
              "A* (Manhattan distance)": aStarCalculate,
              "A* (Euclidean distance)": lambda start, goal, gr: aStarCalculate(start, goal, gr,
                                                                                heuristic="euclidean")}
app = QtWidgets.QApplication(sys.argv)
scene = QtWidgets.QGraphicsScene()

penPoint = QtGui.QPen(QtCore.Qt.gray)
pointBrushEnd = QtGui.QBrush(QtCore.Qt.red)
pointBrushStart = QtGui.QBrush(QtCore.Qt.blue)

penGrid = QtGui.QPen(QtCore.Qt.black)
penVisited = QtGui.QPen(QtCore.Qt.lightGray)
pointBrushVisited = QtGui.QBrush(QtCore.Qt.white)
pointBrushPath = QtGui.QBrush(QColor("#5fd7ff"))

wallBrush = QtGui.QBrush(QtCore.Qt.darkYellow)
gridBrush = QtGui.QBrush(QtCore.Qt.lightGray)
maze = False
grid = utils.Grid()


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, record=False):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Buttons
        self.runPathFinding.clicked.connect(self.run_algorithm)
        self.setCoordinates.clicked.connect(self.show_coordinates)
        self.setRandomCoordinates.clicked.connect(self.random_coordinates)
        self.generateMaze.clicked.connect(self.generate_maze)
        self.runPathFinding.setEnabled(False)
        self.startXValue.setPlainText("0")
        self.startYValue.setPlainText("0")
        self.goalXValue.setPlainText("63")
        self.goalYValue.setPlainText("63")
        # Combobox
        for algorithm in ALGORITHMS.keys():
            self.chooseAlgorithm.addItem(algorithm)
        # GridDraw
        self.draw_grid(scene, penGrid, SIDE)

    def show_coordinates(self):
        # Check if there are values to the boxes.
        # inputs to values
        if not 0 <= int(self.startXValue.toPlainText()) < 64:
            self.startXValue.setPlainText("0")
        if not 0 <= int(self.startYValue.toPlainText()) < 64:
            self.startYValue.setPlainText("0")
        if not 0 <= int(self.goalXValue.toPlainText()) < 64:
            self.goalXValue.setPlainText("63")
        if not 0 <= int(self.goalYValue.toPlainText()) < 64:
            self.goalYValue.setPlainText("63")
        if self.startXValue.toPlainText() == self.goalXValue.toPlainText() and \
                self.startYValue.toPlainText() == self.goalYValue.toPlainText():
            self.goalXValue.setPlainText(str(int(random.uniform(0, 64))))
            self.goalYValue.setPlainText(str(int(random.uniform(0, 64))))
        Xstart = int(self.startXValue.toPlainText())
        Ystart = int(self.startYValue.toPlainText())
        Xgoal = int(self.goalXValue.toPlainText())
        Ygoal = int(self.goalYValue.toPlainText())
        # GridDraw
        window.draw_grid(scene, penGrid, SIDE)
        window.draw_start_end_nodes(Xstart, Ystart, Xgoal, Ygoal, penPoint, pointBrushStart, pointBrushEnd)
        self.runPathFinding.setEnabled(True)

    def random_coordinates(self):
        # check if there is a maze generated
        if maze:
            start = (random.randint(0, 64), random.randint(0, 64))
            while start not in maze_history:
                start = (random.randint(0, 64), random.randint(0, 64))
            goal = (random.randint(0, 64), random.randint(0, 64))
            while goal not in maze_history:
                goal = (random.randint(0, 64), random.randint(0, 64))
            Xstart = start[0]
            Ystart = start[1]
            Xgoal = goal[0]
            Ygoal = goal[1]
        else:
            # Chose Random value
            Xstart = random.randint(0, 64)
            Ystart = random.randint(0, 64)
            Xgoal = random.randint(0, 64)
            Ygoal = random.randint(0, 64)
            if Xstart == Xgoal and Ystart == Ygoal:
                Xgoal = random.randint(0, 64)
                Ygoal = random.randint(0, 64)
        # add Random value to text inputs
        self.startXValue.setPlainText(str(Xstart))
        self.startYValue.setPlainText(str(Ystart))
        self.goalXValue.setPlainText(str(Xgoal))
        self.goalYValue.setPlainText(str(Ygoal))
        # Draw
        window.draw_grid(scene, penGrid, SIDE)
        window.draw_start_end_nodes(Xstart, Ystart, Xgoal, Ygoal, penPoint, pointBrushStart, pointBrushEnd)
        self.runPathFinding.setEnabled(True)

    def run_algorithm(self):
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
        window.draw_grid(scene, penGrid, SIDE)
        # Draw grid
        window.draw_start_end_nodes(Xstart, Ystart, Xgoal, Ygoal, penPoint, pointBrushStart, pointBrushEnd)
        # Get paths
        correctPath = result.get("path")
        visited = result.get("visited")
        # GridDrawVisited
        window.draw_visited(Xstart, Ystart, Xgoal, Ygoal, penPoint, pointBrushStart, pointBrushEnd, penVisited,
                            pointBrushVisited, visited, correctPath, SIDE)
        if maze == False:
            window.setCoordinates.setEnabled(True)
        window.setRandomCoordinates.setEnabled(True)
        self.runPathFinding.setEnabled(True)

    def draw_grid(self, scene, penGrid, SIDE):
        self.graphicsView.setScene(scene)
        for y in range(GRIDSIZE):
            for x in range(GRIDSIZE):
                r = QtCore.QRectF(QtCore.QPointF(y * SIDE, x * SIDE), QtCore.QSizeF(SIDE, SIDE))
                scene.addRect(r, penGrid)
        for y in range(GRIDSIZE):
            for x in range(GRIDSIZE):
                scene.addRect(y * SIDE, x * SIDE, 10, 10, penPoint, gridBrush)
        for y in range(GRIDSIZE):
            for x in range(GRIDSIZE):
                if grid.to_ndarray()[y, x] == grid.WALL:
                    # print wall
                    scene.addRect(y * SIDE, x * SIDE, 10, 10, penPoint, wallBrush)
                else:
                    # print path
                    pass

    def draw_start_end_nodes(self, Xstart, Ystart, Xgoal, Ygoal, penPoint, pointBrushStart, pointBrushEnd):
        scene.clear()
        window.draw_grid(scene, penGrid, SIDE)
        scene.addRect(int(Xstart * SIDE), int(Ystart * SIDE), 10, 10, penPoint, pointBrushStart)
        scene.addRect(int(Xgoal * SIDE), int(Ygoal * SIDE), 10, 10, penPoint, pointBrushEnd)

    def draw_visited(self, Xstart, Ystart, Xgoal, Ygoal, penPoint, pointBrushStart, pointBrushEnd, penVisited,
                     pointBrushvisited, visited, correctPath, SIDE):
        scene.addRect(int(Xstart * SIDE), int(Ystart * SIDE), 10, 10, penPoint, pointBrushStart)
        scene.addRect(int(Xgoal * SIDE), int(Ygoal * SIDE), 10, 10, penPoint, pointBrushEnd)
        for y, x in visited:
            QtTest.QTest.qWait(5)
            scene.addRect(y * SIDE, x * SIDE, 10, 10, penVisited, pointBrushvisited)
            scene.addRect(int(Xstart * SIDE), int(Ystart * SIDE), 10, 10, penPoint, pointBrushStart)
        for y, x in correctPath:
            scene.addRect(y * SIDE, x * SIDE, 10, 10, penPoint, pointBrushPath)
        scene.addRect(int(Xstart * SIDE), int(Ystart * SIDE), 10, 10, penPoint, pointBrushStart)
        scene.addRect(int(Xgoal * SIDE), int(Ygoal * SIDE), 10, 10, penPoint, pointBrushEnd)

    def generate_maze(self):
        self.runPathFinding.setEnabled(False)
        window.setCoordinates.setEnabled(False)
        window.setRandomCoordinates.setEnabled(False)
        window.generateMaze.setEnabled(False)
        global maze
        maze = True
        global grid
        grid = utils.Grid(create_maze=True, size=GRIDSIZE)
        global maze_history
        maze_history = grid.get_maze_history()
        for y in range(GRIDSIZE):
            for x in range(GRIDSIZE):
                scene.addRect(x * SIDE, y * SIDE, 10, 10, penPoint, wallBrush)
        im = QImage(int(scene.sceneRect().width()), int(scene.sceneRect().height()),
                    QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(im)
        for i, (x, y) in enumerate(maze_history):
            QtTest.QTest.qWait(2)
            scene.addRect(x * SIDE, y * SIDE, 10, 10, penPoint, gridBrush)
            if False:
                scene.render(painter)
                im.save(str(Path("/home/marios/Downloads/generate_maze") / f"frame{i:05d}.png"))
        painter.end()
        window.setRandomCoordinates.setEnabled(True)


if __name__ == "__main__":
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
