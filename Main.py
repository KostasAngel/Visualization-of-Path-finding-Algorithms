import random
import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtTest
from PyQt5.QtGui import QColor, QImage, QPainter

import path_finding_algorithms.utils as utils
from path_finding_algorithms.a_star import calculate as a_star_calculate
from path_finding_algorithms.breadth_first_search import calculate as bfs_calculate
from path_finding_algorithms.depth_first_search import calculate as dfs_calculate
from path_finding_algorithms.dijkstras_algorithm import calculate as djk_calculate

qtcreator_file = "main_window.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)
GRIDSIZE = 64
SIDE = 10

# dictionary with implemented algorithms
ALGORITHMS = {"Breadth First Search": bfs_calculate,
              "Depth First Search": dfs_calculate,
              "Dijkstra's Algorithm": djk_calculate,
              "A* (Manhattan distance)": a_star_calculate,
              "A* (Euclidean distance)": lambda st, goal, gr: a_star_calculate(st, goal, gr, heuristic="euclidean")}

app = QtWidgets.QApplication(sys.argv)

penPoint = QtGui.QPen(QtCore.Qt.gray)
pointBrushEnd = QtGui.QBrush(QtCore.Qt.red)
pointBrushStart = QtGui.QBrush(QtCore.Qt.blue)

penGrid = QtGui.QPen(QtCore.Qt.black)
penVisited = QtGui.QPen(QtCore.Qt.lightGray)
pointBrushVisited = QtGui.QBrush(QtCore.Qt.white)
pointBrushPath = QtGui.QBrush(QColor("#5fd7ff"))

wallBrush = QtGui.QBrush(QtCore.Qt.darkYellow)
gridBrush = QtGui.QBrush(QtCore.Qt.lightGray)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, record=False):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.scene = QtWidgets.QGraphicsScene()
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

        self.maze = False
        self.grid = utils.Grid()

        # GridDraw
        self.draw_grid(self.scene, penGrid, SIDE)

        # For recording UI for demo GIFs
        self.record = record
        self.frame = QImage(int(self.scene.sceneRect().width()), int(self.scene.sceneRect().height()),
                            QImage.Format_ARGB32_Premultiplied)
        self.painter = QPainter(self.frame)

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
        window.draw_grid(self.scene, penGrid, SIDE)
        window.draw_start_end_nodes(Xstart, Ystart, Xgoal, Ygoal, penPoint, pointBrushStart, pointBrushEnd)
        self.runPathFinding.setEnabled(True)

    def random_coordinates(self):
        # check if there is a maze generated
        if self.maze:
            start = (random.randint(0, 64), random.randint(0, 64))
            while start not in self.grid.get_maze_history():
                start = (random.randint(0, 64), random.randint(0, 64))
            goal = (random.randint(0, 64), random.randint(0, 64))
            while goal not in self.grid.get_maze_history():
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
        window.draw_grid(self.scene, penGrid, SIDE)
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
        result = ALGORITHMS[text](startingPoint, goalPoint, self.grid)
        # enable scene to draw
        window.draw_grid(self.scene, penGrid, SIDE)
        # Draw grid
        window.draw_start_end_nodes(Xstart, Ystart, Xgoal, Ygoal, penPoint, pointBrushStart, pointBrushEnd)
        # Get paths
        correctPath = result.get("path")
        visited = result.get("visited")
        # GridDrawVisited
        window.draw_visited(Xstart, Ystart, Xgoal, Ygoal, penPoint, pointBrushStart, pointBrushEnd, penVisited,
                            pointBrushVisited, visited, correctPath, SIDE)
        if not self.maze:
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
                if self.grid.to_ndarray()[y, x] == self.grid.WALL:
                    # print wall
                    scene.addRect(y * SIDE, x * SIDE, 10, 10, penPoint, wallBrush)
                else:
                    # print path
                    pass

    def draw_start_end_nodes(self, Xstart, Ystart, Xgoal, Ygoal, penPoint, pointBrushStart, pointBrushEnd):
        self.scene.clear()
        window.draw_grid(self.scene, penGrid, SIDE)
        self.scene.addRect(int(Xstart * SIDE), int(Ystart * SIDE), 10, 10, penPoint, pointBrushStart)
        self.scene.addRect(int(Xgoal * SIDE), int(Ygoal * SIDE), 10, 10, penPoint, pointBrushEnd)

    def draw_visited(self, Xstart, Ystart, Xgoal, Ygoal, penPoint, pointBrushStart, pointBrushEnd, penVisited,
                     pointBrushvisited, visited, correctPath, SIDE):
        self.scene.addRect(int(Xstart * SIDE), int(Ystart * SIDE), 10, 10, penPoint, pointBrushStart)
        self.scene.addRect(int(Xgoal * SIDE), int(Ygoal * SIDE), 10, 10, penPoint, pointBrushEnd)
        algo_name = self.get_current_algorithm_name()
        i = 0
        for y, x in visited:
            if not self.record:
                QtTest.QTest.qWait(5)
            self.scene.addRect(y * SIDE, x * SIDE, 10, 10, penVisited, pointBrushvisited)
            self.scene.addRect(int(Xstart * SIDE), int(Ystart * SIDE), 10, 10, penPoint, pointBrushStart)
            if self.record:
                self.render_and_save_frame(algo_name, i)
            i += 1
        for y, x in correctPath:
            self.scene.addRect(y * SIDE, x * SIDE, 10, 10, penPoint, pointBrushPath)
            if self.record:
                self.render_and_save_frame(algo_name, i)
        self.scene.addRect(int(Xstart * SIDE), int(Ystart * SIDE), 10, 10, penPoint, pointBrushStart)
        self.scene.addRect(int(Xgoal * SIDE), int(Ygoal * SIDE), 10, 10, penPoint, pointBrushEnd)

    def generate_maze(self):
        self.runPathFinding.setEnabled(False)
        window.setCoordinates.setEnabled(False)
        window.setRandomCoordinates.setEnabled(False)
        window.generateMaze.setEnabled(False)
        self.maze = True
        self.grid = utils.Grid(create_maze=True, size=GRIDSIZE)
        for y in range(GRIDSIZE):
            for x in range(GRIDSIZE):
                self.scene.addRect(x * SIDE, y * SIDE, 10, 10, penPoint, wallBrush)
        for i, (x, y) in enumerate(self.grid.get_maze_history()):
            QtTest.QTest.qWait(2)
            self.scene.addRect(x * SIDE, y * SIDE, 10, 10, penPoint, gridBrush)
            if self.record:
                self.render_and_save_frame("maze", i)
        window.setRandomCoordinates.setEnabled(True)

    def render_and_save_frame(self, dir_name: str, frame_number: int):
        path = Path("/home/marios/Downloads/generate_maze") / dir_name
        if not path.is_dir():
            path.mkdir(parents=True)
        self.scene.render(self.painter)
        self.frame.save(str(path / f"frame{frame_number:05d}.png"))

    def get_current_algorithm_name(self) -> str:
        algo = str(self.chooseAlgorithm.currentText()).replace("*", " star").replace(" ", "_")
        algo = "".join(c.lower() for c in algo if c not in "'()")
        return algo


if __name__ == "__main__":
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
