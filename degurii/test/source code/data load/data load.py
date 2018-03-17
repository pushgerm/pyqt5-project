import sys
import numpy as np
from PyQt5.QtWidgets import *

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(600, 200, 500, 300)
        self.setWindowTitle("Data Load v0.1")

        self.pushButton = QPushButton("File Open")
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.pushButton)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self)[0]
        file_extension = fname.split('.')[-1]

        if file_extension == "csv":
            self.label.setText(fname)
        else:
            self.label.setText("Failed to load data.\ncsv file(.csv) only")
            return;


        input = np.loadtxt(fname, delimiter = ',', dtype = np.float32)

        x = input[:, 3:4]
        y = input[:, 4:5]



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()