import pyecharts.options as opts

import pandas as pd
from pyecharts.charts import *
from pyecharts.globals import CurrentConfig, NotebookType
import sys
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Charts_render:
    def __init__(self):
        CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_NOTEBOOK
        self.d = []
        self.ds = []
        self.dz = []
        self.fs = []
        
        self.app = QApplication(sys.argv)
        self.windows = QWidget()
        self.windows.setGeometry(300,300,400,600)
        self.windows.setWindowTitle('Charts Render')
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.windows.setLayout(self.grid)

        self.title1 = QLabel('Charts Render')
        self.title1.setAlignment(Qt.AlignCenter)
        self.title1.setFont(QFont('Consolas',45))
        self.grid.addWidget(self.title1,0,0,1,1)
        
        self.pushButton1 = QPushButton("Open file")
        self.pushButton1.setFont(QFont('Consolas',13))
        self.grid.addWidget(self.pushButton1,1,0,1,1)

        self.pushButton2 = QPushButton("Sure")
        self.pushButton2.setFont(QFont('Consolas',13))
        self.grid.addWidget(self.pushButton2,1,1,1,1)

        self.pushButton3 = QPushButton("Clear")
        self.pushButton3.setFont(QFont('Consolas',13))
        self.grid.addWidget(self.pushButton3,1,2,1,1)

        self.lbl = QLabel('Output path:')
        self.lbl.setFont(QFont('Consolas',13))
        self.grid.addWidget(self.lbl,2,0,1,1)

        self.inp = QLineEdit()
        self.inp.setFont(QFont('Consolas',13))
        self.grid.addWidget(self.inp,2,1,1,2)

        self.info1 = QTextBrowser()
        self.info1.setFont(QFont('Consolas',13))
        self.grid.addWidget(self.info1,3,0,1,3)
        self.t = ''

        
                
        

        self.pushButton1.clicked.connect(self.get_file)
        self.pushButton2.clicked.connect(self.main)
        self.pushButton3.clicked.connect(self.clear)
        self.windows.show()
        self.app.exec_()
        
        

    def clear(self):
        self.t = ''
        self.info1.setText(self.t)
        
        
    def main(self):
        try:
            try:
                self.t = ''
                self.info1.setText(self.t)

            
            
            
            
                self.open_file(self.ff)
                self.t += f'Open success\n'
                self.info1.setText(self.t)
            
            
                self.file_style()
                self.t += f'Data styled\n'
                self.info1.setText(self.t)
                
                
                self.model()
                self.t += f'Charts model created\n'
                self.info1.setText(self.t)
                
                
                self.render()
                self.t += f'render seccess\n'
                self.info1.setText(self.t)
            except AssertionError:
                self.t = ''
                self.info1.setText(self.t)
                self.t += 'File open failed'
                self.info1.setText(self.t)
        except AttributeError:
            self.t = ''
            self.info1.setText(self.t)
            self.t += 'File open failed'
            self.info1.setText(self.t)
        
    
    def get_file(self):
        self.t = ''
        self.info1.setText(self.t)
        openfile_name = QFileDialog.getOpenFileName(self.windows,'Choose files','','Excel files(*.xlsx , *.xls)')
        self.t += f"Choose:'{openfile_name[0]}'\n"
        self.info1.setText(self.t)
        self.ff = openfile_name[0]

    
    def open_file(self,f):
        
        self.pdf = pd.read_excel(f)
        
    def file_style(self):
        self.index = []
        self.value = []
        for i in self.pdf:
            self.index.append(i)
            
        for i in range(len(self.index)):
            self.value.append([])
            for j in self.pdf[self.index[i]]:
                self.value[i].append(j)

        
                
        
    
    def model(self):
        self.bar = Line(init_opts=opts.InitOpts(theme='dark',animation_opts=opts.AnimationOpts(animation_delay=500, animation_easing="elasticOut"),width="1400px", height="600px"))
        
        for i in range(len(self.value)):
            if self.index[i] == 'date':
                self.bar.add_xaxis(self.value[i])
            else:
                self.bar.add_yaxis(self.index[i], self.value[i],is_connect_nones=True,is_smooth=True,label_opts = opts.LabelOpts(is_show=False))
        
        
        self.bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    def render(self):
        self.bar.render(self.inp.text())



    



