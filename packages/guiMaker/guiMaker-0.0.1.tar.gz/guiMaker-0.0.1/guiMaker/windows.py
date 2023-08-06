from tkinter import *;from tkinter import ttk,messagebox,filedialog;import tkinter
from guiMaker import errors
class createMainwindow(tkinter.Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("guiMaker - mainwindow")
    def setTitle(self,title):
        self.title(title)
    def setIcon(self,iconName):
        self.iconbitmap(str(iconName))
    def start(self):
        self.mainloop()
    def startOnlyInMain(self):
        if __name__ == '__main__':
            self.start()
        else:
            print("This program only works in main.py.")
        pass
    def close(self):
        self.withdraw()
    def exit(self):
        self.destroy()
    pass
class createLittlewindow(tkinter.Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("guiMaker - littlewindow #1")
    def setTitle(self,title):
        self.title(title)
    def setIcon(self,iconName):
        self.iconbitmap(str(iconName))
    def start(self):
        raise errors.RunError("Can't run program with little window!")
    def startOnlyInMain(self):
        raise errors.RunError("Can't run program with little window!")
    def close(self):
        self.withdraw()
    def exit(self):
        self.destroy()
    pass