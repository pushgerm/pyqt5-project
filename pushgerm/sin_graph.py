# https://stackoverflow.com/questions/40372103/make-dynamic-graph-with-pyqt5-and-matplotlib
import sys, os, random
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation


class AnimationWidget(QWidget):
    def __init__(self):
        QMainWindow.__init__(self)

        vbox = QVBoxLayout()
        self.canvas = MyMplCanvas(self, width=5, height=4, dpi=100)
        vbox.addWidget(self.canvas)

        hbox = QHBoxLayout()
        self.start_button = QPushButton("start", self)
        self.stop_button = QPushButton("stop", self)
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.x = np.linspace(0, 5*np.pi, 10)
        print(self.x)
        self.p = 0.0
        self.y = np.sin(self.x + self.p)
        print(self.y)
        self.line, = self.canvas.axes.plot(self.x, self.y, animated=True, lw=10)#list of Line2D반환
        print(self.line)

    def update_line(self, i):
        self.p += 0.1
        y = np.sin(self.x + self.p)
        print(y)
        self.line.set_ydata(y)
        return [self.line]

    def on_start(self):
        self.ani = animation.FuncAnimation(self.canvas.figure, self.update_line,
                                 blit=True, interval=25)

    def on_stop(self):
        self.ani._stop()


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=10):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.cla()
        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

    def compute_initial_figure(self):
        pass



if __name__ == "__main__":
    qApp = QApplication(sys.argv)
    aw = AnimationWidget()
    aw.show()
    sys.exit(qApp.exec_())