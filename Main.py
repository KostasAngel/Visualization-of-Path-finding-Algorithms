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
pointBrushEnd = QtGui.QBrush(QtCore.Qt.green)
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
        self.goalXValue.setPlainText(str(GRIDSIZE - 1))
        self.goalYValue.setPlainText(str(GRIDSIZE - 1))

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
        # check if there are values in the input boxes
        if not 0 <= int(self.startXValue.toPlainText()) < GRIDSIZE:
            self.startXValue.setPlainText("0")
        if not 0 <= int(self.startYValue.toPlainText()) < GRIDSIZE:
            self.startYValue.setPlainText("0")
        if not 0 <= int(self.goalXValue.toPlainText()) < GRIDSIZE:
            self.goalXValue.setPlainText(str(GRIDSIZE - 1))
        if not 0 <= int(self.goalYValue.toPlainText()) < GRIDSIZE:
            self.goalYValue.setPlainText(str(GRIDSIZE - 1))

        if self.startXValue.toPlainText() == self.goalXValue.toPlainText() and \
                self.startYValue.toPlainText() == self.goalYValue.toPlainText():
            self.goalXValue.setPlainText(str(random.randint(0, GRIDSIZE - 1)))
            self.goalYValue.setPlainText(str(random.randint(0, GRIDSIZE - 1)))

        # inputs to values
        start_x, start_y = int(self.startXValue.toPlainText()), int(self.startYValue.toPlainText())
        goal_x, goal_y = int(self.goalXValue.toPlainText()), int(self.goalYValue.toPlainText())

        # draw grid
        window.draw_grid(self.scene, penGrid, SIDE)
        window.draw_start_end_nodes(start_x, start_y, goal_x, goal_y, penPoint, pointBrushStart, pointBrushEnd)
        self.runPathFinding.setEnabled(True)

    def random_coordinates(self):
        grid_size = GRIDSIZE - 1
        # check if there is a maze generated
        if self.maze:
            start = (random.randint(0, grid_size), random.randint(0, grid_size))
            while start not in self.grid.get_maze_history():
                start = (random.randint(0, grid_size), random.randint(0, grid_size))
            goal = (random.randint(0, grid_size), random.randint(0, grid_size))
            while goal not in self.grid.get_maze_history():
                goal = (random.randint(0, grid_size), random.randint(0, grid_size))
            start_x, start_y = start
            goal_x, goal_y = goal
        else:
            # choose Random value
            start_x, start_y = random.randint(0, grid_size), random.randint(0, grid_size)
            goal_x, goal_y = random.randint(0, grid_size), random.randint(0, grid_size)
            while start_x == goal_x and start_y == goal_y:
                goal_x, goal_y = random.randint(0, grid_size), random.randint(0, grid_size)

        # add Random value to text inputs
        self.startXValue.setPlainText(str(start_x))
        self.startYValue.setPlainText(str(start_y))
        self.goalXValue.setPlainText(str(goal_x))
        self.goalYValue.setPlainText(str(goal_y))

        # Draw
        window.draw_grid(self.scene, penGrid, SIDE)
        window.draw_start_end_nodes(start_x, start_y, goal_x, goal_y, penPoint, pointBrushStart, pointBrushEnd)
        self.runPathFinding.setEnabled(True)

    def run_algorithm(self):
        self.runPathFinding.setEnabled(False)
        window.setCoordinates.setEnabled(False)
        window.setRandomCoordinates.setEnabled(False)
        window.generateMaze.setEnabled(False)

        # inputs to values
        start_x = int(self.startXValue.toPlainText())
        start_y = int(self.startYValue.toPlainText())
        goal_x = int(self.goalXValue.toPlainText())
        goal_y = int(self.goalYValue.toPlainText())

        # assign to variables to run Algo
        starting_point = (start_x, start_y)
        goal_point = (goal_x, goal_y)
        text = self.chooseAlgorithm.currentText()
        result = ALGORITHMS[text](starting_point, goal_point, self.grid)

        # enable scene to draw
        window.draw_grid(self.scene, penGrid, SIDE)

        # Draw grid
        window.draw_start_end_nodes(start_x, start_y, goal_x, goal_y, penPoint, pointBrushStart, pointBrushEnd)

        # Get paths
        correct_path = result.get("path")
        visited = result.get("visited")

        # GridDrawVisited
        window.draw_visited(start_x, start_y, goal_x, goal_y, penPoint, pointBrushStart, pointBrushEnd, penVisited,
                            pointBrushVisited, visited, correct_path, SIDE)
        if not self.maze:
            window.setCoordinates.setEnabled(True)
        window.setRandomCoordinates.setEnabled(True)
        self.runPathFinding.setEnabled(True)

    def draw_grid(self, scene, pen_grid, SIDE):
        self.graphicsView.setScene(scene)
        for y in range(GRIDSIZE):
            for x in range(GRIDSIZE):
                r = QtCore.QRectF(QtCore.QPointF(y * SIDE, x * SIDE), QtCore.QSizeF(SIDE, SIDE))
                scene.addRect(r, pen_grid)
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

    def draw_start_end_nodes(self, start_x, start_y, goal_x, goal_y, pen_point, point_brush_start, point_brush_end):
        self.scene.clear()
        window.draw_grid(self.scene, penGrid, SIDE)
        self.scene.addRect(int(start_x * SIDE), int(start_y * SIDE), 10, 10, pen_point, point_brush_start)
        self.scene.addRect(int(goal_x * SIDE), int(goal_y * SIDE), 10, 10, pen_point, point_brush_end)

    def draw_visited(self, start_x, start_y, goal_x, goal_y, pen_point, point_brush_start, point_brush_end, pen_visited,
                     point_brush_visited, visited, correct_path, SIDE):
        self.scene.addRect(int(start_x * SIDE), int(start_y * SIDE), 10, 10, pen_point, point_brush_start)
        self.scene.addRect(int(goal_x * SIDE), int(goal_y * SIDE), 10, 10, pen_point, point_brush_end)
        algo_name = self.get_current_algorithm_name()
        i = 0
        for y, x in visited[1:-1]:  # skips start and goal
            if not self.record:
                QtTest.QTest.qWait(5)
            self.scene.addRect(y * SIDE, x * SIDE, 10, 10, pen_visited, point_brush_visited)
            if self.record:
                self.render_and_save_frame(i, algo_name)
            i += 1
        for y, x in correct_path[1:-1]:  # skips start and goal
            if not self.record:
                QtTest.QTest.qWait(2)
            self.scene.addRect(y * SIDE, x * SIDE, 10, 10, pen_point, pointBrushPath)
            if self.record:
                self.render_and_save_frame(i, algo_name)
            i += 1

    def generate_maze(self):
        self.runPathFinding.setEnabled(False)
        window.setCoordinates.setEnabled(False)
        window.setRandomCoordinates.setEnabled(False)
        window.generateMaze.setEnabled(False)
        self.maze = True
        self.grid = utils.Grid(create_maze=True, size=GRIDSIZE, random_seed=42 if self.record else None)
        for y in range(GRIDSIZE):
            for x in range(GRIDSIZE):
                self.scene.addRect(x * SIDE, y * SIDE, 10, 10, penPoint, wallBrush)
        for i, (x, y) in enumerate(self.grid.get_maze_history()):
            QtTest.QTest.qWait(2)
            self.scene.addRect(x * SIDE, y * SIDE, 10, 10, penPoint, gridBrush)
            if self.record:
                self.render_and_save_frame(i, "maze")
        window.setRandomCoordinates.setEnabled(True)

    def render_and_save_frame(self, frame_number: int, dir_name: str):
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
    window = MyWindow(record=False)
    window.show()
    sys.exit(app.exec_())
