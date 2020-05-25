import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt
from depth_first_search import calculate as dfsCalculate
from breadth_first_search import calculate as bfsCalculate
import utils

qtcreator_file  = "mainWindow.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.runPathFinding.clicked.connect(self.showPressed)
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        pen = QtGui.QPen(QtCore.Qt.black)
        side = 10

        for i in range(64):
            for j in range(64):
                r = QtCore.QRectF(QtCore.QPointF(i*side, j*side), QtCore.QSizeF(side, side))
                scene.addRect(r, pen)

    def showPressed(self):
        Xstart = int(self.startXValue.toPlainText())
        Ystart = int(self.startYValue.toPlainText())
        Xgoal = int(self.goalXValue.toPlainText())
        Ygoal = int(self.goalYValue.toPlainText())
        startingPoint= (Xstart,Ystart)
        goalPoint = (Xgoal,Ygoal)
        GRID = utils.new_grid(64) 
        print("button is pressed. The values of the start are x: "+ str(Xstart) +" and Y: "+ str(Ystart))
        result = bfsCalculate(GRID,startingPoint,goalPoint)
        print(len(result["path"]))
       


















if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


