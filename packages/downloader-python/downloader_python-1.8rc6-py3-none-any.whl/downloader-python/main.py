from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.uic import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import requests
import os
import datetime
import time
from colorama import *
from web import *
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import QT_VERSION_STR
import os
import subprocess
from pip_install import install,uninstall,find_moudles
from load_text import *


init(autoreset=True)

is_Chinese = False
Ui_MainWindow,_ = loadUiType('sources/downloader.ui')
Fast_link,_ = loadUiType('sources/fast_link.ui')
Python_script,_ = loadUiType('sources/python_script.ui')
py_inst,_ = loadUiType('sources/py.ui')

class moudle_installer(QtWidgets.QMainWindow,py_inst):
    def __init__(self):
        super(moudle_installer,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.install)
        self.pushButton_2.clicked.connect(self.uninstall)
        self.pushButton_3.clicked.connect(self.find_moudles)


    def install(self):

        install(self.lineEdit.text())
    def uninstall(self):
        uninstall(self.lineEdit.text())
    def find_moudles(self):
        find_moudles()



class PS(QtWidgets.QMainWindow,Python_script):
    un = pyqtSignal()
    def __init__(self):

        super(PS, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.runs)

    def runs(self):
        self.un.emit()
    def run_script(self):

        s = self.textEdit.toPlainText()
        with open('test.py','w') as f:
            f.write(s)
        with open('run.bat','w') as f:
            f.write('@echo off\n'+f'{sys.executable} test.py')
        subprocess.call('run.bat')

class Fast(QtWidgets.QMainWindow,Fast_link):
    a = pyqtSignal()
    b = pyqtSignal()
    def __init__(self):

        super(Fast, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.a.emit)
        self.pushButton_2.clicked.connect(self.b.emit)
        self.main_timer = QtCore.QTimer()
        self.main_timer.timeout.connect(self.loadd)
        self.main_timer.start(1)



    def load(self,dic):


        self.label.setText(dic['fastlink.label'])
        self.pushButton.setText(dic['fastlink.pushButton'])
        self.pushButton_2.setText(dic['fastlink.pushButton_2'])

    def loadd(self):
        if is_Chinese:
            self.load(load('zh-cn.lang'))
        else:
            self.load(load('en-us.lang'))






class window(QtWidgets.QMainWindow,Ui_MainWindow):
    signal = pyqtSignal()
    fast_link = pyqtSignal()
    version = '1.8pre6'
    def __init__(self):




        super(window,self).__init__()
        with open('log/log.log', 'w') as f:
            f.write('')
        self.log(f'[{time.ctime()}][main/Info] loading')

        self.user_name = ''
        while True:
            self.user_name = input('Your name is:')
            if self.user_name != '':
                break
            else:
                self.log(f'[{time.ctime()}][main/WARN] user name is Null,please try again',color=Fore.YELLOW)

        self.log(f'[{time.ctime()}][main/INFO] Setting user:{self.user_name}')

        self.setupUi(self)
        self.pushButton.clicked.connect(self.download)
        self.te = ''
        self.progressBar.setValue(0)
        self.pushButton_2.clicked.connect(self.fwa)
        self.pushButton_3.clicked.connect(self.fast)
        self.wdw = ''



        self.setWindowIcon(QIcon('sources/icon.bmp'))
        self.log(f'[{time.ctime()}][main/Info] icon loaded')

        try:
            self.load()
            self.log(f'[{time.ctime()}][main/Info] load settings.properties sucsess')
        except BaseException as e:


            self.log(f'[{time.ctime()}][main/Error] error in initlazing:{e}',Fore.RED)

            self.log(r'*\**:( Downloader Crashed! ):**/*',Fore.RED)
            sys.exit(self.show())

        self.timer = QTimer()
        self.timer.timeout.connect(self.write)
        self.timer.start(1)
        self.log(f'[{time.ctime()}][main/Info] timer initlazing sucsess')
        self.log(
            f'[{time.ctime()}][main/Info] backend library:PyQt5 version {PYQT_VERSION_STR} build on Qt {QT_VERSION_STR}')


    def loadt(self,dic):

        self.groupBox.setTitle(dic['groupBox'])
        self.label.setText(dic['label'])
        self.label_2.setText(dic['label_2'])
        self.pushButton.setText(dic['pushButton'])
        self.groupBox_2.setTitle(dic['groupBox_2'])
        self.label_3.setText(dic['label_3'])
        self.label_4.setText(dic['label_4'])
        self.pushButton_2.setText(dic['pushButton_2'])
        self.label_5.setText(dic['label_5']+self.version)
        self.groupBox_3.setTitle(dic['groupBox_3'])
        self.checkBox.setText(dic['checkBox'])
        self.groupBox_4.setTitle(dic['groupBox_4'])
        self.checkBox_2.setText(dic['checkBox_2'])
        self.checkBox_3.setText(dic['checkBox_3'])
        self.groupBox_5.setTitle(dic['groupBox_5'])
        self.groupBox_6.setTitle(dic['groupBox_6'])
        self.pushButton_3.setText(dic['pushButton_3'])
        self.setWindowTitle(self.user_name+dic['title'])
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), dic['tab_win.tab'])
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), dic['tab_win.tab_2'])
        self.tabWidget_2.setTabText(self.tabWidget.indexOf(self.tab), dic['tab_win2.tab'])
        self.tabWidget_2.setTabText(self.tabWidget.indexOf(self.tab_2), dic['tab_win2.tab_2'])
        self.checkBox_4.setText(dic['checkBox_4'])

    def fast(self):
        self.log(
            f'[{time.ctime()}][main/Info] fast link started')
        self.fast_link.emit()
    def log(self,text,color=Fore.RESET):
        print(color+text)
        try:
            self.wdw += '\n' + text
            self.textBrowser_2.setText(self.wdw)
        except BaseException:
            self.wdw = ''
            self.wdw += text + '\n'
            self.tab_4 = QtWidgets.QWidget()
            self.tab_4.setObjectName("tab_4")
            self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab_4)
            self.textBrowser_2.setGeometry(QtCore.QRect(5, 1, 761, 221))
            self.textBrowser_2.setObjectName("textBrowser_2")
            self.textBrowser_2.setText(self.wdw)
        with open('log/log.log','a') as f:
            f.write(text+'\n')

    def opencmd(self):
        os.system('cmd')
    def fwa(self):
        self.close()
    def print(self):
        self.log(f'[{time.ctime()}][main/Info] stopping!')

    def load(self):

        a = open('properties/settings.properties')

        dicss = a.read()
        dicss = eval(dicss)


        if dicss['no useragent']:
            self.checkBox.toggle()
        if dicss['no speed']:
            self.checkBox_2.toggle()
        if dicss['no error']:
            self.checkBox_3.toggle()
        self.lineEdit.setText(dicss['url'])
        self.lineEdit_2.setText(dicss['locate'])
        if dicss['Chinese']:
            is_Chinese == True
            self.checkBox_4.toggle()

    def closeEvent(self,event):
        if is_Chinese:
            result = QtWidgets.QMessageBox.question(self,'关闭','是否关闭?',QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        else:
            result = QtWidgets.QMessageBox.question(self, 'close', 'Close?',
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            self.print()
            event.accept()

        else:
            event.ignore()
    def write(self):
        self.timer.stop()
        self.timer.start(self.horizontalSlider.value())
        if self.checkBox_4.isChecked():
            self.lang = load('zh-cn.lang')
            self.loadt(self.lang)
            is_Chinese == True


        else:
            self.lang = load('en-us.lang')
            self.loadt(self.lang)
            is_Chinese == False


        a = open('properties/settings.properties','w')
        #dic = [None,None,None,None,None,None]
        dics = {'no useragent':None,
               'no speed':None,
               'no error':None,
               'url':None,
               'locate':None,
               'Chinese':None}

        dics['no useragent'] = self.checkBox.isChecked()
        dics['no speed'] = self.checkBox_2.isChecked()
        dics['no error'] = self.checkBox_3.isChecked()
        dics['url'] = self.lineEdit.text()
        dics['locate'] = self.lineEdit_2.text()
        dics['Chinese'] = self.checkBox_4.isChecked()




        a.write(str(dics))


    def download(self):
        self.log(f'[{time.ctime()}][main/Info] Downloading')
        self.u(0)
        a = datetime.datetime.now()
        self.u(1)
        self.te = ''
        self.u(3)
        self.textBrowser.setText(self.te)
        self.u(4)
        self.update('initlazing')
        self.u(5)

        try:
            self.u(10)
            self.update('getting')
            self.u(20)
            if not self.checkBox.isChecked():
                if self.lineEdit_3.text() == '':
                    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78'}
                else:
                    header = header = {'user-agent':self.lineEdit_3.text()}

                r = requests.get(self.lineEdit.text(),headers = header)
            else:
                r = requests.get(self.lineEdit.text())
            self.u(30)
            con = r.content
            self.u(40)
            text = self.lineEdit.text().split('/')
            self.u(50)
            self.update('downloading')
            self.u(60)
            if self.lineEdit_2.text() != '':
                aaaaa = self.lineEdit_2.text()+'/'+text[-1].replace('/','')\
            .replace(r'\\', '')\
            .replace(':', '')\
            .replace('*', '')\
            .replace('?', '')\
            .replace('"','') \
            .replace('<', '') \
            .replace('>', '') \
            .replace('|', '')
            else:
                aaaaa = text[-1].replace('/', '') \
                    .replace(r'\\', '') \
                    .replace(':', '') \
                    .replace('*', '') \
                    .replace('?', '') \
                    .replace('"', '') \
                    .replace('<', '') \
                    .replace('>', '') \
                    .replace('|', '')


            aaa = str(time.time())
            with open(aaaaa,'ab+') as f:
                self.u(70)
                self.update('writing')
                self.u(80)
                f.write(con)
                self.u(90)
            self.u(101)
            b = datetime.datetime.now()
            x = b-a
            x = x.total_seconds()
            if not self.checkBox_2.isChecked():
                print(f'[{time.ctime()}][main/Info] Download from {self.lineEdit.text()} sucsess')
                size = float(os.path.getsize(aaaaa))
                if size >= 1024 and size <= 1024*1024:
                    self.update(f'sucsess in {x}s({size/1024}KB,{size/1024/x}KB/s)')
                elif size >= 1024*1024 and size <= 1024*1024*1024:
                    self.update(f'sucsess in {x}s({size/1024/1024}MB,{size/1024/1024/x}MB/s)')
                elif size >= 1024*1024*1024 and size <= 1024*1024*1024*1024:
                    self.update(f'sucsess in {x}s({size/1024/1024/1024}GB,{size/1024/1024/1024/x}GB/s)')
                elif size >= 1024*1024*1024*1024:
                    self.update(f'sucsess in {x}s({size/1024/1024/1024/1024}TB,{size/1024/1024/1024/1024/x}TB/s)')
                else:
                    self.update(f'sucsess in {x}s({size}B,{size/x}B/s)')
            else:
                self.update(f'sucsess in {x}s')
                self.log(f'[{time.ctime()}][main/Info] Download from {self.lineEdit.text()} sucsess')

        except BaseException as e:
            self.u(0)
            if not self.checkBox_3.isChecked():
                self.update(f'error:{e}')
            else:
                self.update(f'failed')


            self.log(f'[{time.ctime()}][main/Warn] error in download:{e},ignored',Fore.YELLOW)







    def update(self,t):
        self.te += t + '\n'
        self.textBrowser.setText(self.te)
    def u(self,v):
        a = self.progressBar.value()
        if v > a:
            for i in range(a,v):
                self.progressBar.setValue(i)
                time.sleep(0.001)
        else:

            self.progressBar.setValue(v)
class Main:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.d = moudle_installer()
        self.a = PS()
        self.fast = Fast()
        self.window = window()
    def connect_windows(self):
        self.a.un.connect(self.a.run_script)

        self.fast.a.connect(self.a.show)
        self.fast.b.connect(self.d.show)
        self.window.fast_link.connect(self.fast.show)
    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())
if __name__ == '__main__':
    main = Main()
    main.connect_windows()
    main.run()






else:
    print(f'[{time.ctime()}][main/Info] now varbile "__name__"={__name__},run in web mode')
    run('1.3')



