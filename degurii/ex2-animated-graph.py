from __future__ import print_function

import sys

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import *

ITERS = 1000

import random as rd
import numpy as np
import time

class BlitQT(FigureCanvas):

    def __init__(self):
        FigureCanvas.__init__(self, Figure())

        self.ax = self.figure.add_subplot(111)
        self.ax.grid()
        self.draw()

        self.input = np.loadtxt('temp.csv', delimiter=',', dtype=np.float32)

        self.old_size = self.ax.bbox.width, self.ax.bbox.height
        self.ax_background = self.copy_from_bbox(self.ax.bbox)
        self.cnt = 0

        self.ndata = self.input.shape[0] - 1
        self.y = self.input[:, 4:5]

        self.x = np.arange(0, self.ndata + 1, 1)
        self.line, = self.ax.plot(self.x, self.y, animated=True)
        self.draw()

        self.tstart = time.time()
        self.startTimer(10)

    def timerEvent(self, evt):
        current_size = self.ax.bbox.width, self.ax.bbox.height
        if self.old_size != current_size:
            self.old_size = current_size
            self.ax.clear()
            self.ax.grid()
            self.draw()
            self.ax_background = self.copy_from_bbox(self.ax.bbox)

        self.restore_region(self.ax_background)

        # update the data
      #  self.line_set_xdata(self.x)
        # self.line.set_ydata(np.sin(self.x + self.cnt / 10.0))
        # self.line_set_xdaya(self.x)
        self.line_set_xdata(np.arange(0,self.cnt+1,1))
        self.line.set_ydata(self.input[:self.cnt, 4:5])

        # just draw the animated artist
        self.ax.draw_artist(self.line)

        # just redraw the axes rectangle
        self.blit(self.ax.bbox)

        if self.cnt == 0:
            # TODO: this shouldn't be necessary, but if it is excluded the
            # canvas outside the axes is not initially painted.
            self.draw()

        if self.cnt == self.ndata:
            # print the timing info and quit
            print('FPS:', ITERS / (time.time() - self.tstart))
            sys.exit()
        else:
            self.cnt += 1

app = QApplication(sys.argv)
widget = BlitQT()
widget.show()

sys.exit(app.exec_())