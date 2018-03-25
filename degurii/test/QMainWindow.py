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
        self.canvas = None

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

        # 사진파일 load
        label = QLabel(self)
        pixmap = QPixmap('image.JPG')
        label.setPixmap(pixmap)
        label.move(34, 50)
        label.resize(638, 410)

        # 버튼
        btn1 = QPushButton('Load Data', self)
        btn1.move(250, 550)
        btn1.resize(200, 50)
        btn1.clicked.connect(self.loadData)  #클릭시 csv파일 선택해 열기

        btn2 = QPushButton('Transform', self)
        btn2.move(250, 650)
        btn2.resize(200, 50)


        self.canvas = PlotCanvas(self, width=8, height=8)
        self.canvas.move(700, 0)

        self.show()

    def loadData(self):
        fname = QFileDialog.getOpenFileName(self)[0]
        file_extension = fname.split('.')[-1]

        # .csv파일이 아니면 에러창 띄움
        if file_extension != "csv":
            PopUpWindow()
            return

        input = np.loadtxt(fname, delimiter = ',', dtype = np.float32)

        # ndata : 행의 갯수
        ndata = input.shape[0]

        # x축을 시간의 경과에 따라 1~데이터 갯수만큼으로 지정
        self.x = np.array([[x] for x in range(1, ndata+1)])
        self.y = input[:, -1:]
        self.canvas.plot(self.x, self.y)

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

        self.ax1.plot(x, y)
        self.ax1.hold(False)
        self.draw()

class PopUpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        fg = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

        buttonReply = QMessageBox.question(self, "Error", "Failed to load data.\ncsv file (.csv) only", QMessageBox.Yes)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())