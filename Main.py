import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt
from depth_first_search import calculate as dfsCalculate
from breadth_first_search import calculate as bfsCalculate
import utils
import random

qtcreator_file  = "mainWindow.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

GRIDSIZE = 64

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #Buttons
        self.runPathFinding.clicked.connect(self.runAlgorithm)
        self.setCoordinates.clicked.connect(self.showCoordinates)
        self.setRandomCoordinates.clicked.connect(self.randomCoordinates)
        #Visual UI
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        #colors
        penGrid = QtGui.QPen(QtCore.Qt.black)
        penPoint = QtGui.QPen(QtCore.Qt.red)
        pointBrushEnd = QtGui.QBrush(QtCore.Qt.green)
        pointBrushStart = QtGui.QBrush(QtCore.Qt.blue)
        #Draw Grid
        side = 10
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                r = QtCore.QRectF(QtCore.QPointF(i*side, j*side), QtCore.QSizeF(side, side))
                scene.addRect(r, penGrid)
 
    def showCoordinates(self):
        #inputs to values
        Xstart = int(self.startXValue.toPlainText())
        Ystart = int(self.startYValue.toPlainText())
        Xgoal = int(self.goalXValue.toPlainText())
        Ygoal = int(self.goalYValue.toPlainText())
        #enable scene to draw
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        #colors
        penGrid = QtGui.QPen(QtCore.Qt.black)
        penPoint = QtGui.QPen(QtCore.Qt.red)
        pointBrushEnd = QtGui.QBrush(QtCore.Qt.green)
        pointBrushStart = QtGui.QBrush(QtCore.Qt.blue)
        #Grid
        side = 10
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                r = QtCore.QRectF(QtCore.QPointF(i*side, j*side), QtCore.QSizeF(side, side))
                scene.addRect(r, penGrid)
        #Draw Start and End node
        scene.addRect( int(Xstart * side), int( Ystart * side), 10,10 ,penPoint ,pointBrushStart)
        scene.addRect( int(Xgoal * side),int( Ygoal * side), 10,10 ,penPoint ,pointBrushEnd)
        
    def randomCoordinates(self):
        Xstart = int(random.uniform(0,64))
        Ystart = int(random.uniform(0,64))
        Xgoal = int(random.uniform(0,64))
        Ygoal = int(random.uniform(0,64)) 
        self.startXValue.setPlainText(str(Xstart))
        self.startYValue.setPlainText(str(Ystart))
        self.goalXValue.setPlainText(str(Xgoal))
        self.goalYValue.setPlainText(str(Ygoal))
        #enable scene to draw
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        #colors
        penGrid = QtGui.QPen(QtCore.Qt.black)
        penPoint = QtGui.QPen(QtCore.Qt.red)
        pointBrushEnd = QtGui.QBrush(QtCore.Qt.green)
        pointBrushStart = QtGui.QBrush(QtCore.Qt.blue)
        #Grid
        side = 10
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                r = QtCore.QRectF(QtCore.QPointF(i*side, j*side), QtCore.QSizeF(side, side))
                scene.addRect(r, penGrid)
        #Draw Start and End node
        scene.addRect( int(Xstart * side), int( Ystart * side), 10,10 ,penPoint ,pointBrushStart)
        scene.addRect( int(Xgoal * side),int( Ygoal * side), 10,10 ,penPoint ,pointBrushEnd)


    def runAlgorithm(self):
        #inputs to values 
        Xstart = int(self.startXValue.toPlainText())
        Ystart = int(self.startYValue.toPlainText())
        Xgoal = int(self.goalXValue.toPlainText())
        Ygoal = int(self.goalYValue.toPlainText())        
        #assign to variables to run Algo
        startingPoint= (Xstart,Ystart)
        goalPoint = (Xgoal,Ygoal)
        grid = utils.new_grid(GRIDSIZE) 
        #Call Path Algorithm
        result = bfsCalculate(grid,startingPoint,goalPoint)
        
        #enable scene to draw
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        penGrid = QtGui.QPen(QtCore.Qt.black)
        penVisited = QtGui.QPen(QtCore.Qt.darkMagenta)
        penPoint = QtGui.QPen(QtCore.Qt.red)
        pointBrushEnd = QtGui.QBrush(QtCore.Qt.green)
        pointBrushStart = QtGui.QBrush(QtCore.Qt.blue)
        #Draw grid
        side = 10
        for i in range(GRIDSIZE):
            for j in range(GRIDSIZE):
                r = QtCore.QRectF(QtCore.QPointF(i*side, j*side), QtCore.QSizeF(side, side))
                scene.addRect(r, penGrid)        
        #draw path
        pointBrushPath = QtGui.QBrush(QtCore.Qt.black)
        correctPath = result.get("path")
        visited = result.get("visited")
        #print (visited)
        for x,y in visited:
            scene.addRect( x*side, y*side , 10,10 ,penVisited ,pointBrushPath)
        #print (correctPath)
        for x,y in correctPath:
            scene.addRect( x*side, y*side , 10,10 ,penPoint ,pointBrushPath)
        #Draw end and start nodes
        scene.addRect( int(Xstart * side), int( Ystart * side), 10,10 ,penPoint ,pointBrushStart)
        scene.addRect( int(Xgoal * side),int( Ygoal * side), 10,10 ,penPoint ,pointBrushEnd)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


