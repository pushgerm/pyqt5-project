import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # window property
        self.left = 100#윈도우창 x축 위치
        self.top = 100#윈도우창 y축 위치
        self.title = 'FFT project'#윈도우창 이름
        self.width = 1500#윈도우창 너비
        self.height = 900#윈도우창 높이

        # data statistics
        self.average = None
        self.variance = None
        self.deviation = None

        # graph
        self.canvas = None

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
        self.setWindowTitle(self.title) #윈도우창 타이틀
        self.move(self.left, self.top)  #전체 윈도우 창 위치 및 크기
        self.setFixedSize(self.width, self.height)

        image = QLabel(self)    #사진 넣을 공간 마련
        pixmap = QPixmap('image.JPG')   # 사진 불러오기
        image.setPixmap(pixmap) # 레이블에 사진 삽입
        image.move(175, 50) #사진위치조정
        image.resize(478, 307)  #사진 크기조정(실제사이즈=638x410)

        self.setinfo()      #평균, 분산 등 정보 생성

        self.setButton()    #버튼 생성
        self.inputLabel()   #입력 창 생성

        self.canvas_1 = PlotCanvas(self, width=8, height=3)   #윈도우창에 그래프 삽입
        self.canvas_1.move(700, 0)    #그래프 위치
        self.canvas_2 = PlotCanvas(self, width=8, height=3)  # 윈도우창에 그래프 삽입
        self.canvas_2.move(700, 300)
        self.canvas_3 = PlotCanvas(self, width=8, height=3)   #윈도우창에 그래프 삽입
        self.canvas_3.move(700, 600)
        self.show()



    def inputLabel(self):
        #input_1
        input_1 = QLabel("input_1 : ",self)
        input_1.move(200, 400)
        input_1.resize(200, 30)
        self.getIn_1 = QLineEdit("", self)
        self.getIn_1.move(270, 400)

        #input_2
        input_2 = QLabel("input_2 : ",self)
        input_2.move(200, 460)
        input_2.resize(200, 30)
        self.getIn_2 = QLineEdit("", self)
        self.getIn_2.move(270, 460)

        #input_3
        input_3 = QLabel("input_3 : ",self)
        input_3.move(200, 520)
        input_3.resize(200, 30)
        self.getIn_3 = QLineEdit("", self)
        self.getIn_3.move(270, 520)

        pushButton = QPushButton("send", self)
        pushButton.move(270, 580)
        pushButton.resize(100, 30)

    def setinfo(self):
        #평균
        info1 = QLabel("평균 : ",self)
        info1.move(500, 400)
        info1.resize(200, 30)
        self.average = QLabel("", self)
        self.average.move(570, 400)

        #분산
        info2 = QLabel("분산 : ",self)
        info2.move(500, 460)
        info2.resize(200, 30)
        self.variance = QLabel("", self)
        self.variance.move(570, 460)

        #표준편차
        info3 = QLabel("표준편차 : ",self)
        info3.move(500, 520)
        info3.resize(200, 30)
        self.deviation = QLabel("", self)
        self.deviation.move(570, 520)


    def setButton(self):
        # 첫 번째 버튼 위치
        first_btn_left = 0
        first_btn_top = 30

        # 버튼 크기
        btn_width = 120
        btn_height = 50

        num_btn = 2  # 버튼의 개수
        space_btn = 5  # 버튼 사이의 간격

        btn = [QPushButton(self) for i in range(0, num_btn)]

        # set button text
        btn[0].setText('Load Data')
        btn[1].setText('Transform')

        # set button size, position
        for i in range(0, num_btn):
            # 버튼의 위치: 처음 버튼 + (i번째)*(버튼 간격 + 버튼 높이)
            btn[i].move(first_btn_left, first_btn_top + i * (space_btn + btn_height))
            btn[i].resize(btn_width, btn_height)

        # connect to slot
        btn[0].clicked.connect(self.loadData)  # 클릭시 csv파일 선택해 열기


    def loadData(self):

        fpath = QFileDialog.getOpenFileName(self)[0]    # 파일의 절대경로를 받아온다
        fname = fpath.split('/')[-1]    # 절대경로를 '/' 기준으로 슬라이싱 해서 파일 이름만 받아옴
        file_extension = fname.split('.')[-1]   # 파일이름을 '.' 으로 슬라이싱해서 확장자명을 받아옴

        # 아무 파일도 선택하지 않고 취소 눌렀을 때
        if fpath == "":
            return

        # .csv파일이 아니면 에러창 띄움
        if file_extension != "csv":
            PopUpWindow()
            return

        input = np.loadtxt(fpath, delimiter = ',', dtype = np.float32)  # 파일의 절대경로를 넣어준다
        ndata = input.shape[0]

        self.time = np.array([[x] for x in range(1, ndata +1 )])
        if(fname[0:3] =="acc"):
            self.x = input[:, 4:5]#x가속도 데이터
            self.y = input[:, 5:6]#y가속도 데이터@@@@@일단 x가속도만 가지고 계산하자
            self.canvas_1.plot_acc(self.time, self.x, self.y)#acc.csv그래프 그리기
            self.getInfo()

        elif(fname[0:4]=="temp"):
            self.x = input[:, 4:5]#온도
            self.canvas_2.plot_temp(input)#temp.csv그래프 그리기
            self.getInfo()

    def getInfo(self):
        #평균
        n = len(self.x)
        sum = 0
        for num in self.x:
            sum += num
        avg = sum / n
        s =str(avg)
        self.average.setText(s)

        #분산
        x2 = self.x**2
        sum = 0
        for num in x2:
            sum += num
        avg2 = sum/n
        var = avg2 - avg**2
        s = str(var)
        self.variance.setText(s)

        #표준편차
        dev = var**0.5
        s = str(dev)
        self.deviation.setText(s)



class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)#what does this instruction mean?
        self.ax = self.figure.add_subplot(111, xlim=(0,1), ylim=(0,1), autoscale_on=False)# make a subplot1
        self.line, = self.ax.plot([], [], lw = 1)

        scale = 1.1 # size how much the graph would be zoomed
        zp_ax = ZoomPan()
        figZoom_ax = zp_ax.zoom_factory(self.ax, base_scale=scale)   #can zoome the graph
        figPan_ax = zp_ax.pan_factory(self.ax)   #can move the graph
        #FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        #FigureCanvas.updateGeometry(self)


    def plot_acc(self, time1, x, y):
        self.ax.cla()  #erase graph before draw a new one
        self.ax.plot(time1, x, label='x acceleration')#why doesn't the label show up?
        self.ax.plot(time1, y, label = 'y acceleration')
        self.ax.set_xlabel('time')#name of x axe
        self.ax.set_ylabel('acceleration')#name of y axe
        #self.ax.hold(False)#data reset when the new data come
        self.draw()

    def plot_temp(self, input):
        self.ax.set_xlim((0, 3000))
        self.ax.set_ylim((156, 170))
        self.ax.grid(True)
        line, = self.ax.plot([], [], lw=1)
        def init():
            line.set_data(([], []))
            return (line,)

        def animate(t):
            time = [i for i in range(0, t)]
            x = input[:t, 4:5]
            line.set_data(time, x)
            return line,

        ani = animation.FuncAnimation(fig=self.figure, func=animate, init_func=init, interval=5, blit=True)
        self.draw()
        plt.show()

        """
        self.ax.cla()   #erase graph before draw a new one
        self.ax.plot(time, x, label = 'temp')
        self.ax.set_xlabel('time')#name of x axe
        self.ax.set_ylabel('temperature')#name of y axe
        #self.ax.hold(False)#data reset when the new data come
        self.draw()
        """


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



class ZoomPan:  #This class can make graph zoomed and move
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None


    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print (event.button)

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom


    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())