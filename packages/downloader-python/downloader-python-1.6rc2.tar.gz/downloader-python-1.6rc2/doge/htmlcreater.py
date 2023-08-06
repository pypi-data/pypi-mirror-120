import sys
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class HTML_creater:
  def __init__(self):
    self.app = QApplication(sys.argv)
    self.windows = QWidget()
    self.windows.setGeometry(300,300,400,400)
    self.windows.setWindowTitle('HTML creater')
    self.grid = QGridLayout()
    self.grid.setSpacing(10)
    self.windows.setLayout(self.grid)

    self.label1 = QLabel('HTML creater')
    self.label1.setFont(QFont('Consolas',21))
    self.grid.addWidget(self.label1,0,0,1,2)

    self.pushbutton1 = QPushButton("HTML")
    self.pushbutton1.setFont(QFont('Consolas',13))
    self.grid.addWidget(self.pushbutton1,1,0,1,2)

    self.textedit1 = QTextEdit()
    self.textedit1.setFont(QFont('Consolas',13))
    self.grid.addWidget(self.textedit1,2,0,1,1)

    self.textedit2 = QTextEdit()
    self.textedit2.setFont(QFont('Consolas',13))
    self.grid.addWidget(self.textedit2,2,1,1,1)

    
    self.pushbutton1.clicked.connect(self.HTML)
    self.windows.show()
    self.app.exec_()

  def HTML(self):
    self.t = self.textedit1.toPlainText()
    self.textedit2.setHtml(self.t)


