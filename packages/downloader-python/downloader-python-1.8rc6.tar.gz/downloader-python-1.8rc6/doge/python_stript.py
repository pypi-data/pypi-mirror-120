import sys
import subprocess
import os
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
class Python_stript:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.windows = QWidget()
        self.windows.setGeometry(300,300,400,400)
        self.windows.setWindowTitle('Python Stript')
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.windows.setLayout(self.grid)

        self.title = QLabel('Python stript')
        self.title.setFont(QFont('Consolas',21))
        self.grid.addWidget(self.title,0,0,1,1)

        self.button = QPushButton("Run")
        self.button.setFont(QFont('Consolas',13))
        self.grid.addWidget(self.button,1,0,1,1)

        self.textedit1 = QTextEdit()
        self.textedit1.setFont(QFont('Consolas',13))
        self.grid.addWidget(self.textedit1,2,0,1,1)

        self.button.clicked.connect(self.run)

        self.windows.show()
        self.app.exec_()

    def run(self):
        t = self.textedit1.toPlainText()
        f = open('test.py','w')
        f.write(t)
        f.close()
        os.system("I:\py3.9\pythonw.exe test.py")
        


