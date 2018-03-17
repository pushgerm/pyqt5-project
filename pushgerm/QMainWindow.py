import sys

from PyQt5.QtWidgets import * #import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.title = 'FFT project'
        self.width = 1500
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

        label = QLabel(self)
        pixmap = QPixmap('image.JPG')
        label.setPixmap(pixmap)
        label.move(34, 50)
        label.resize(638, 410)

        btn1 = QPushButton('Load Data', self)
        btn1.move(250, 550)
        btn1.resize(200, 50)
        btn1.clicked.connect(self.loadData)  #클릭시 csv파일 선택해 열기

        btn2 = QPushButton('Transform', self)
        btn2.move(250, 650)
        btn2.resize(200, 50)

        self.m = PlotCanvas(self, width=8, height=8)
        self.m.move(700, 0)

        self.show()

    def loadData(self):
        fname = QFileDialog.getOpenFileName(self)[0]
        file_extension = fname.split('.')[-1]

        self.canOpenData = True
        input = np.loadtxt(fname, delimiter = ',', dtype = np.float32)
        print(fname[-8:-4])
        if(fname[-7:-4] =="acc"):
            self.time = input[:, 6:7]
            self.x = input[:, 4:5]
            self.m.plot_acc(self.time, self.x)
        elif(fname[-8:-4]=="temp"):
            self.time = input[:, 5:6]
            self.x = input[:, 4:5]
            self.m.plot_temp(self.time, self.x)

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.ax1 = self.figure.add_subplot(211)
        self.ax2 = self.figure.add_subplot(212)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot_acc(self, time1, x):

        self.ax1.plot(time1, x, label = 'x acceleration')
        #self.ax1.plot(time1, y, label = 'y acceleration')
        self.ax1.hold(False)
        self.draw()

    def plot_temp(self, time, x):
        self.ax1.plot(time, x, label = 'temp')
        self.ax1.hold(False)
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())