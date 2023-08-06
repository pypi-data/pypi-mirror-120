import sys
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Text_creater:
  def __init__(self):
    self.app = QApplication(sys.argv)
    self.windows = QWidget()
    self.windows.setGeometry(300,300,400,400)
    self.windows.setWindowTitle('Text creater')
    self.grid = QGridLayout()
    self.grid.setSpacing(10)
    self.windows.setLayout(self.grid)

    self.textedit1 = QTextEdit()
    self.textedit1.setFont(QFont('Consolas',13))
    self.grid.addWidget(self.textedit1,2,0,1,3)

    self.label2 = QLabel('')
    self.label2.setFont(QFont('Consolas',13))
    self.grid.addWidget(self.label2,3,0,1,1)

    self.timer = QTimer(self.app)
    self.timer.timeout.connect(self.get_number)
        
    self.timer.start(1)

    self.label1 = QLabel('Text creater')
    self.label1.setFont(QFont('Consolas',21))
    self.grid.addWidget(self.label1,0,0,1,1)





    


    
    



    
   
    
    
    
    
    self.windows.show()
    self.app.exec_()





    
        
  def get_number(self):
   
    self.label2.setText(f"text number:{str(len(self.textedit1.toPlainText()))}")


    

    
