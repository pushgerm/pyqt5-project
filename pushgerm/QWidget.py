import sys
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


class FFTWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Fast Fourier Transformation")   #창 title
        self.setGeometry(400, 100, 1000, 800)  #창의 위치 및 사이즈(x, y, width, height)
        self.setupUI()

    def setupUI(self):

        #버튼 구성
        self.btn1 = QPushButton("Load Data", self)  #데이터 불러오는 버튼 생성
        self.btn1.move(100, 550)
        self.btn1.resize(300, 50)
        self.btn1.clicked.connect(self.loadData)  #클릭시 csv파일 선택해 열기

        self.btn2 = QPushButton("Transform", self)  #fft로 변환하는 버튼 생성
        self.btn2.move(100, 650)
        self.btn2.resize(300, 50)
        #self.btn2.clocked.connect(datatransform()) # 클릭시 fft로 변환

        #그래프 구성
        self.fig = plt.Figure()
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        self.canvas = FigureCanvas(self.fig)



        #레이아웃 구성
        upLayout = QHBoxLayout()

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.canvas)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.btn1)
        leftLayout.addWidget(self.btn2)
        leftLayout.addStretch(1)

        bottomLayout = QHBoxLayout()
        bottomLayout.addLayout(leftLayout)
        bottomLayout.addLayout(rightLayout)
        bottomLayout.setStretchFactor(leftLayout, 1)
        bottomLayout.setStretchFactor(rightLayout, 5)

        layout = QVBoxLayout()
        layout.addLayout(upLayout)
        layout.addLayout(bottomLayout)

        self.setLayout(layout)

    def loadData(self):
        fname = QFileDialog.getOpenFileName(self)[0]
        file_extension = fname.split('.')[-1]

        input = np.loadtxt(fname, delimiter = ',', dtype = np.float32)

        x = input[:, 3:4]
        y = input[:, 4:5]
        self.ax1.plot(x, y)
        self.ax1.hold(False)
        self.canvas.draw()

    def datatransform(self):
        # 위 데이터를 변환해서 밑에 그래프에 구현
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FFTWindow()
    window.show()
    app.exec_()