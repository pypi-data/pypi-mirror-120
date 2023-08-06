from tkinter import messagebox,filedialog;import easygui
def ask(message,title="询问一件事 - guiBuilder",buttons=("确定","取消"),type="simple"):
    if type=="simple":
        bool=easygui.ccbox(message,title=title,choices=buttons)
    elif type=="okcancel":
        bool=messagebox.askokcancel(title,message)
    else:
        bool=messagebox.askyesnocancel(title,message)
    return bool
def show(message,title="信息提醒 - guiBuilder",button="确定",type="simple",image=None):
    if type=="simple":
        easygui.msgbox(message,title=title,ok_button=button,image=image)
    elif type=="info":
        messagebox.showinfo(title,message)
    elif type=="warning":
        messagebox.showwarning(title,message)
    else:
        messagebox.showerror(title,message)
    return None
from tkPlus import functions;from guiMaker import windows
import tkinter
def asktoentry(message,title="输入内容 - guiMaker"):
    '''输入内容，新增'''
    win=windows.createMainwindow()
    win.title(title)
    txt=tkinter.Label(win,text=str(message))
    txt.pack()
    etr=functions.EntryWithPlaceholder(win,placeholder="输入有关“"+str(message)+"”的内容......")
    etr.pack()
    bool=ask("输入完成后请点击确定！",title="请先在弹出的输入框中输入",buttons=("确定","取消"),type="okcancel")
    if bool:
        return etr.get()
    else:
        pass
    return None