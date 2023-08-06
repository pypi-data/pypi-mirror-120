from tkinter import *
from charts_render import *
from textcreater import *
from htmlcreater import *
from python_stript import *
from media_player import *
import os
import subprocess
import time
import sys
from datetime import datetime
from PIL import Image,ImageTk


class Init_OS:
    def __init__(self):
        pass
    def init(self):



        self.btn_list = []
        for i in range(10):
            self.btn_list.append([])
        for i in range(10):
            for j in range(10):
                self.btn_list[i].append([])
        return self.btn_list

        



class DogHead_OS:

    version = 'DogHead OS beta 0.1.7'
    icon_path = 'icon.ico'

    msettings = open('/settings/main.setting')
    msettings = eval(msettings.read())


    def __init__(self):



        self.window = Tk()
        self.window.title("DogHead OS")
        self.window.iconbitmap(self.icon_path)

        self.l = Label(self.window, text="", font=("Consolas", 20))
        self.l.grid(column=0, row=0)
        self.f()
        

        self.window.mainloop()


        
        
        self.window = Tk()
        self.window.title("DogHead OS")
        self.window.iconbitmap(self.icon_path)
        
        
        self.btn_list = Init_OS().init()
        for i in range(10):
            for j in range(10):
                self.btn_list[i][j] = Button(self.window, text="None", command=None, font=("Consolas", 13))
                self.btn_list[i][j].grid(column=j, row=i+1)

        self.btn_name = ["Charts Render","explorer",
                    "text creater", "HTML creater",
                    "Settings","Close",
                         "notepad","regedit",
                         "command","calc",
                         "PCL2","Python stript",
                         "Media player"]
        self.btn_commands = [self.app1,self.app2,
                        self.app3,self.app4,
                        self.set1,self.cl,
                        self.app6,self.app7,
                        self.app8,self.app9,
                        self.app10,self.app11,
                        self.app12]
        self.index = 0
        self.y = 0

        
        for i in zip(self.btn_name,self.btn_commands):
            self.btn_list[self.y][self.index] = Button(self.window, text=i[0], command=i[1], font=("Consolas", 13))
            self.btn_list[self.y][self.index].grid(column=self.y, row=self.index+1)
            if self.index == 9:
                self.index = 0
                self.y += 1
            else:
                self.index += 1

            if self.y == 9 and self.index == 9:
                
                continue
        
        self.lbl100000000 = Label(self.window, text="D", font=("Consolas", 50))
        self.lbl100000000.grid(column=0,row=0)
        self.lbl100000001 = Label(self.window, text="o", font=("Consolas", 50))
        self.lbl100000001.grid(column=1,row=0)
        self.lbl100000002 = Label(self.window, text="g", font=("Consolas", 50))
        self.lbl100000002.grid(column=2,row=0)
        self.lbl100000003 = Label(self.window, text="H", font=("Consolas", 50))
        self.lbl100000003.grid(column=3,row=0)
        self.lbl100000004 = Label(self.window, text="e", font=("Consolas", 50))
        self.lbl100000004.grid(column=4,row=0)
        self.lbl100000005 = Label(self.window, text="a", font=("Consolas", 50))
        self.lbl100000005.grid(column=5,row=0)
        self.lbl100000006 = Label(self.window, text="d", font=("Consolas", 50))
        self.lbl100000006.grid(column=6,row=0)
        self.lbl100000007 = Label(self.window)
        self.lbl100000007.grid(column=7,row=0)
        img_open = Image.open('icon (2).gif')
        img=ImageTk.PhotoImage(img_open)
        self.lbl100000007.config(image=img)
        
        self.lbl100000008 = Label(self.window, text="O", font=("Consolas", 50))
        self.lbl100000008.grid(column=8,row=0)
        self.lbl100000009 = Label(self.window, text="S", font=("Consolas", 50))
        self.lbl100000009.grid(column=9,row=0)
        
        
                
        self.lbl4 = Label(self.window, text="", font=("Consolas", 13))
        self.lbl4.grid(column=11, row=11)
        self.refresh()
        self.is_timing = False

        self.window.mainloop()
    def f(self):
        self.window.after(100,self.d)
        
        
        
    def d(self):
        for i in range(10):
            for j in range(4):
                
                self.l = Label(self.window, text="Welcome"+i*'.', font=("Consolas", 20))
                self.l.grid(column=0, row=0)
        


        
        
    def cl(self):
        self.window.destroy()
    
    def refresh(self):
        self.app5()
        self.window.after(1,self.refresh)
        
    

    def app1(self):
        a = Charts_render()
    def app2(self):
        subprocess.call('C:/Windows/explorer.exe')
    def app3(self):
        b = Text_creater()
    def app4(self):
        c = HTML_creater()
    def app5(self):
        #print(type(self.msettings))
        if self.msettings['time_mode'] == 'time mode 1':
            self.lbl4['text'] = time.ctime()
        if self.msettings['time_mode'] == 'time mode 2':
            self.lbl4['text'] = time.strftime('%Y-%m-%d %H:%M:%S')
        if self.msettings['time_mode'] == 'time mode 3':
            self.lbl4['text'] = round(time.time(),1)
    def app6(self):
        subprocess.call('C:/Windows/notepad.exe')
    def app7(self):
        subprocess.call("C:/Windows/regedit.exe")
    def app8(self):
        os.system('cmd')
    def app9(self):
        subprocess.call("C:/Windows/System32/calc.exe")

    def app10(self):
        subprocess.call("Plain Craft Launcher 2.exe")
    def app11(self):
        a = Python_stript()
    def app12(self):
        a = Media_player()
    def set1(self):
            
        self.settings = Tk()
        self.settings.title("DogHead OS Settings")
        self.lbl100 = Label(self.settings, text=f"Version:{self.version}", font=("Consolas", 21))
        self.lbl100.grid(column=0, row=0)
        self.btn = Button(self.settings, text="about", command=self.set2, font=("Consolas", 13))
        self.btn.grid(column=0, row=1)
        self.btn7 = Button(self.settings, text="time set", command=self.set3, font=("Consolas", 13))
        self.btn7.grid(column=0, row=2)
            
        self.settings.mainloop()
    def set2(self):
        self.about = Tk()
        self.about.title("About")
        self.lbl3 = Label(self.about, text='writers e-mail:guoxiuchen20170402@163.com\npython:3.9.5\nlibs:PyQt5,Tkinter', font=("Consolas", 13))
        self.lbl3.grid(column=0, row=0)

        self.about.mainloop()
    def set3(self):
        self.time = Tk()
        self.time.title("time set")
        self.lbl6 = Label(self.time, text='Time', font=("Consolas", 21))
        self.lbl6.grid(column=0, row=0)

        self.lbl5 = Label(self.time, text='Time Mode:', font=("Consolas", 16))
        self.lbl5.grid(column=0, row=1)

        self.btn2 = Button(self.time, text="time mode 1", command=self.set4, font=("Consolas", 13))
        self.btn2.grid(column=1, row=2)
        self.btn3 = Button(self.time, text="time mode 2", command=self.set5, font=("Consolas", 13))
        self.btn3.grid(column=1, row=3)
        self.btn3 = Button(self.time, text="time mode 3", command=self.set6, font=("Consolas", 13))
        self.btn3.grid(column=1, row=4)
        

        self.lbl7 = Label(self.time, text=f"Now time Mode:{self.msettings['time_mode']}", font=("Consolas", 16))
        self.lbl7.grid(column=1, row=5)
        
        self.time.mainloop()
    def set4(self):
        self.time_format = 'time mode 1'
        self.lbl7['text'] = f'Now time Mode:{self.time_format}'
        self.msettings['time_mode'] = 'time mode 1'
        open('/settings/main.setting','w').write(str(self.msettings))
        msettings = open('/settings/main.setting')
        msettings = eval(msettings.read())
        

            
    def set5(self):
        self.time_format = 'time mode 2'
        self.lbl7['text'] = f'Now time Mode:{self.time_format}'
        self.msettings['time_mode'] = 'time mode 2'
        open('/settings/main.setting','w').write(str(self.msettings))
        msettings = open('/settings/main.setting')
        msettings = eval(msettings.read())

    def set6(self):
        self.time_format = 'time mode 3'
        self.lbl7['text'] = f'Now time Mode:{self.time_format}'
        self.msettings['time_mode'] = 'time mode 3'
        open('/settings/main.setting','w').write(str(self.msettings))
        msettings = open('/settings/main.setting')
        msettings = eval(msettings.read())
    

a = DogHead_OS()
#This is a test.


    


