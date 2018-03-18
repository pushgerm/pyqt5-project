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
        self.left = 100#윈도우창 x축 위치
        self.top = 100#윈도우창 y축 위치
        self.title = 'FFT project'#윈도우창 이름
        self.width = 1500#윈도우창 너비
        self.height = 800#윈도우창 높이

        mainMenu = self.menuBar()#메뉴바 생성
        fileMenu = mainMenu.addMenu('File')#메뉴바에 File 메뉴 추가

        loadSub = QAction('load', self)#File메뉴에 sub메뉴 생성
        loadSub.triggered.connect(self.loadData)#누르면 데이터 불러오기 생성

        exitButton = QAction(QIcon('a.png'), 'Exit', self)#exit
        exitButton.triggered.connect(self.close)#누르면 나가짐
        fileMenu.addAction(loadSub)
        fileMenu.addAction(exitButton)

        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)#윈도우창 타이틀
        self.setGeometry(self.left, self.top, self.width, self.height)#전체 윈도우 창 위치 및 크기

        label = QLabel(self)#사진 넣을 공간 마련
        pixmap = QPixmap('image.JPG') # 사진 불러오기
        label.setPixmap(pixmap)# 레이블에 사진 삽입
        label.move(34, 50)#사진위치조정
        label.resize(638, 410)#사진 크기조정(실제사이즈)

        btn1 = QPushButton('Load Data', self)#데이터 불러오기 버튼
        btn1.move(250, 550)#버튼 위치
        btn1.resize(200, 50)#버튼 크기
        btn1.clicked.connect(self.loadData)  #클릭시 csv파일 선택해 열기

        btn2 = QPushButton('Transform', self)#FFT변환 버튼
        btn2.move(250, 650)#버튼 위치
        btn2.resize(200, 50)#버튼 크기

        self.canvas = PlotCanvas(self, width=8, height=8)#윈도우창에 그래프 삽입
        self.canvas.move(700, 0)#그래프 위치

        self.show()

    def loadData(self):
        fpath = QFileDialog.getOpenFileName(self)[0]    # 파일의 절대경로를 받아온다
        fname = fpath.split('/')[-1]    # 절대경로를 '/' 기준으로 슬라이싱 해서 파일 이름만 받아옴
        file_extension = fname.split('.')[-1]   # 파일이름을 '.' 으로 슬라이싱해서 확장자명을 받아옴

        # .csv파일이 아니면 에러창 띄움
        if file_extension != "csv":
            PopUpWindow()
            return

        input = np.loadtxt(fpath, delimiter = ',', dtype = np.float32)  # 파일의 절대경로를 넣어준다
        ndata = input.shape[0]
        self.time = np.array([[x] for x in range(1, ndata + 1)])

        if(fname[0:3] =="acc"):
            self.x = input[:, 4:5]#x가속도 데이터
            self.y = input[:, 5:6]#y가속도 데이터
            self.canvas.plot_acc(self.time, self.x, self.y)#acc.csv그래프 그리기
        elif(fname[0:4]=="temp"):
            self.x = input[:, 4:5]#온도
            self.canvas.plot_temp(self.time, self.x)#temp.csv그래프 그리기

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)#what does this instruction mean?
        self.ax1 = self.figure.add_subplot(211)# make a subplot1
        self.ax2 = self.figure.add_subplot(212)# make a subplot 2

        #FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        #FigureCanvas.updateGeometry(self)

    def plot_acc(self, time1, x, y):

        self.ax1.plot(time1, x, label='x acceleration')#why doesn't the label show up?
        self.ax1.plot(time1, y, label = 'y acceleration')
        self.ax1.set_xlabel('time')#name of x axe
        self.ax1.set_ylabel('acceleration')#name of y axe
        self.ax1.hold(False)#data reset when the new data come
        self.draw()

    def plot_temp(self, time, x):
        self.ax1.plot(time, x, label = 'temp')
        self.ax1.set_xlabel('time')#name of x axe
        self.ax1.set_ylabel('temperature')#name of y axe
        self.ax1.hold(False)#data reset when the new data come
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

        QMessageBox.question(self, "Error", "Failed to load data.\ncsv file (.csv) only", QMessageBox.Yes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())