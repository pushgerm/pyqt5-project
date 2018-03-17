import sys

from PyQt5.QtWidgets import * #import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import random


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 1000
        self.height = 800

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')

        loadButton = QAction('load', self)
        loadButton.triggered.connect(self.loadData)

        exitButton = QAction(QIcon('a.png'), 'Exit', self)
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(loadButton)
        fileMenu.addAction(exitButton)

        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        btn1 = QPushButton('Load Data', self)
        btn1.move(50, 600)
        btn1.resize(200, 50)
        btn1.clicked.connect(self.loadData)  #클릭시 csv파일 선택해 열기

        btn2 = QPushButton('Transform', self)
        btn2.move(50, 700)
        btn2.resize(200, 50)

        self.m = PlotCanvas(self, width=7, height=8)
        self.m.move(300, 0)

        self.show()

    def loadData(self):
        fname = QFileDialog.getOpenFileName(self)[0]
        file_extension = fname.split('.')[-1]

        self.canOpenData = True
        input = np.loadtxt(fname, delimiter = ',', dtype = np.float32)

        self.x = input[:, 3:4]
        self.y = input[:, 4:5]
        self.m.plot(self.x, self.y)

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.ax1 = self.figure.add_subplot(211)
        self.ax2 = self.figure.add_subplot(212)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, x, y):

        self.m.ax1.plot(x, y)
        self.m.ax1.hold(False)
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())