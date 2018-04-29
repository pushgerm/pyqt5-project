import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import *
from matplotlib.figure import Figure


class popUpGraph(QMainWindow):
    def __init__(self):
        super().__init__()

        # window property
        self.left = 100#윈도우창 x축 위치
        self.top = 100#윈도우창 y축 위치
        self.title = 'FFT project'#윈도우창 이름
        self.width = 1500#윈도우창 너비
        self.height = 900#윈도우창 높이


        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title) #윈도우창 타이틀
        self.move(self.left, self.top)  #전체 윈도우 창 위치 및 크기
        self.setFixedSize(self.width, self.height)


        fig, ax = plt.subplots( )
        print(fig)
        print(ax)
        ax.set_xlim((13075, 15991))
        ax.set_ylim((156, 170))
        ax.grid(True)

        line, = ax.plot([], [], lw =1)
        print(line)
        input = np.loadtxt('temp.csv', delimiter=',', dtype=np.float32)  # 파일의 절대경로를 넣어준다
        ndata = input.shape[0]



        def init():
            line.set_data(([], []))
            return (line, )

        def animate(t):
            time = [i for i in range(13075, t+13075)]
            print(time[:10])
            x = input[:t, 4:5]
            line.set_data(time, x)

            return line,

        ani = animation.FuncAnimation(fig=fig, func=animate, init_func=init, interval=20, blit=True)

        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = popUpGraph()
    sys.exit(app.exec_())