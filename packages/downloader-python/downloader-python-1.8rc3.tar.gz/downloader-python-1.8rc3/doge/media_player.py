import sys
import subprocess
import os
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from easygui import *
import cv2
import numpy as np
from tkinter import *
import time

class Media_player:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.windows = QWidget()
        self.windows.setGeometry(300, 300, 400, 400)
        self.windows.setWindowTitle('Media player')
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.windows.setLayout(self.grid)

        self.lb1 = QLabel("Media player")
        self.lb1.setFont(QFont('Consolas',21))
        self.grid.addWidget(self.lb1,0,0,1,1)

        self.pushButton1 = QPushButton("Open file")
        self.pushButton1.setFont(QFont('Consolas',13))
        self.grid.addWidget(self.pushButton1,1,0,1,1)

        self.pushButton1.clicked.connect(self.play)

        self.windows.show()
        self.app.exec_()
        


    def play(self):
        file, filetype = QFileDialog.getOpenFileName(self.windows,
                  "Choose files",
                  "./",
                  "MP4 Files (*.mp4);;MOV Files (*.mov)")
        self.aa = Tk()
        self.lbl100000000 = Label(self.aa, text="Loading...", font=("Consolas", 13))
        self.lbl100000000.grid(column=0,row=0)
        self.aa.mainloop()
        
        
        cap = cv2.VideoCapture(file)

        while (cap.isOpened()):
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(40) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


        






