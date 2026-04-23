import tkinter
from tkinter import ttk

window = tkinter.Tk()
window.title('GUI SCAMP')

melody = ttk.Treeview(window,columns=('duration'))
melody.heading('#0',text='音符')
melody.heading('#1',text='时值')

result = tkinter.Text()

buttons = tkinter.Frame(window)

file_buttons = tkinter.Frame(buttons)

copy = tkinter.Button(file_buttons,text='复制')
save = tkinter.Button(file_buttons,text='保存')
clear = tkinter.Button(file_buttons,text='清空')

melody_buttons = tkinter.Frame(buttons)

add = tkinter.Button(melody_buttons,text='添加')

copy.pack(side=tkinter.LEFT)
save.pack(side=tkinter.LEFT)
clear.pack(side=tkinter.LEFT)

file_buttons.pack(side=tkinter.LEFT)

add.pack(side=tkinter.LEFT)

melody_buttons.pack(side=tkinter.LEFT,padx=10)

buttons.pack(anchor=tkinter.NW)

melody.pack(side=tkinter.LEFT,anchor=tkinter.W,fill=tkinter.Y)
result.pack(side=tkinter.LEFT,anchor=tkinter.E)

window.mainloop()
