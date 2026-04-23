import tkinter
from tkinter import ttk

def do_copy():
    pass

def do_save():
    pass

def do_clear():
    pass

def do_add():
    pass

def do_remove():
    pass

window = tkinter.Tk()
window.title('GUI SCAMP')

melody = ttk.Treeview(window,columns=('duration'))
melody.heading('#0',text='音符')
melody.heading('#1',text='时值')

result = tkinter.Text(state='disabled')

buttons = tkinter.Frame(window)

file_buttons = tkinter.Frame(buttons)

copy = tkinter.Button(file_buttons,text='复制',command=do_copy)
save = tkinter.Button(file_buttons,text='保存',command=do_save)
clear = tkinter.Button(file_buttons,text='清空',command=do_clear)

melody_buttons = tkinter.Frame(buttons)

add = tkinter.Button(melody_buttons,text='添加',command=do_add)
remove = tkinter.Button(melody_buttons,text='删除',command=do_remove)

copy.pack(side=tkinter.LEFT)
save.pack(side=tkinter.LEFT)
clear.pack(side=tkinter.LEFT)

file_buttons.pack(side=tkinter.LEFT)

add.pack(side=tkinter.LEFT)
remove.pack(side=tkinter.LEFT)

melody_buttons.pack(side=tkinter.LEFT,padx=10)

buttons.pack(anchor=tkinter.NW)

melody.pack(side=tkinter.LEFT,anchor=tkinter.W,fill=tkinter.Y)
result.pack(side=tkinter.LEFT,anchor=tkinter.E)

window.mainloop()
