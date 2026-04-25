# Tiiiny Music->main.py
# Copyright (c) 2026 DreamFunction

import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import notemidi
import time
import mido
import json

def play_midi_notes(notes_data):
    """
    一个简单的MIDI播放器，使用 Mido 强制 ALSA 后端。
    notes_data: notemidi.translate() 的输出，如 [(60, 0.5, 80), ...]
    """
    # 1. 核心：强制使用 ALSA 后端，彻底摆脱 JACK
    mido.set_backend('mido.backends.rtmidi/LINUX_ALSA')
    
    # 2. 获取所有可用的输出端口
    available_ports = mido.get_output_names()
    
    if not available_ports:
        print("错误：未找到任何 MIDI 输出端口。")
        return

    # 3. 查找 FluidSynth 端口
    fluid_port_name = None
    for port in available_ports:
        if 'FLUID' in port or 'Synth' in port:
            fluid_port_name = port
            break
    
    if fluid_port_name is None:
        print("错误：未找到 FluidSynth 端口，请确保 FluidSynth 正在运行。")
        print("可用端口：", available_ports)
        return
    
    # 4. 打开找到的 FluidSynth 端口
    print(f"已连接到 MIDI 设备: {fluid_port_name}")
    midi_out = mido.open_output(fluid_port_name)
    
    # 5. 播放
    for note, duration, velocity in notes_data:
        if note is None: # 休止符
            time.sleep(duration)
            continue
       
        # 使用 Mido 的消息格式
        note_on = mido.Message('note_on', note=note, velocity=velocity)
        note_off = mido.Message('note_off', note=note)
       
        midi_out.send(note_on)
        time.sleep(duration)
        midi_out.send(note_off)

    # 6. 关闭端口
    midi_out.close()
    del midi_out

def read_all_rows(tree):
    """遍历 Treeview 的所有行，返回数据列表"""
    data = []
    for item in tree.get_children():  # get_children() 返回所有行ID
        # 获取音符（第一列，列名为 #0）
        note = tree.item(item, 'text')
        # 获取时值（第二列，columns 里的第一列）
        duration = tree.item(item, 'values')[0]  # values 是元组，索引0是第一个自定义列
        if note!='休止':
            data.append((note[0]+note[4], float(duration)))
        else:
            data.append(('r',float(duration)))
    return data

def do_openfile():
    if read_all_rows(melody)!=[]:
        do = messagebox.askyesno('打开文件','打开文件将会覆盖您目前编辑的所有内容。确认打开吗？')
        if do==False:
            return 
    path = filedialog.askopenfilename()
    if path!='':
        
        with open(path) as f:
            for i in json.loads(f.read()):
                if i[0]=='休止':
                    melody.insert('',index=tkinter.END,text='休止',value=i[1])
                else:
                    map = {'c':1,'d':2,'e':3,'f':4,'g':5,'a':6,'b':7}
                    item = i[0][0]+'('+str(map[i[0][0]])+')'+i[0][1]
                    melody.insert('',index=tkinter.END,text=item,value=i[1])
 

def do_save():
    path = filedialog.asksaveasfilename()
    if path!='':
        with open(path,'w') as f:
            f.write(json.dumps(read_all_rows(melody)))

def do_play():
    mlist = notemidi.translate(read_all_rows(melody))
    play_midi_notes(mlist)

def do_add():
    if nvar.get()=='休止':
        ngvar.set('休止')
        melody.insert('',index=tkinter.END,text='休止',value=dvar.get())
    elif ngvar.get()=='休止':
        nvar.set('休止')
        melody.insert('',index=tkinter.END,text='休止',value=dvar.get())
    else:
        melody.insert('',index=tkinter.END,text=nvar.get()+ngvar.get(),value=dvar.get())

def do_remove():
    if melody.selection()!=():
        melody.delete(melody.selection())

window = tkinter.Tk()
window.title('Tiiiny Music')

melody = ttk.Treeview(window,columns=('duration',))
melody.heading('#0',text='音符')
melody.heading('#1',text='时值')

choice = tkinter.Frame(window)

nvar = tkinter.StringVar(choice)
nvar.set('c(1)')
note = tkinter.OptionMenu(choice,nvar,'c(1)','d(2)','e(3)','f(4)','g(5)','a(6)','b(7)','休止')
ngvar = tkinter.StringVar(choice)
ngvar.set('4')
note_group = tkinter.OptionMenu(choice,ngvar,'1','2','3','4','5','6','7','8')
dvar = tkinter.StringVar(choice)
dvar.set('4')
dur = tkinter.OptionMenu(choice,dvar,'1','2','4','8','16','32')


buttons = tkinter.Frame(window)

file_buttons = tkinter.Frame(buttons)

openfile = tkinter.Button(file_buttons,text='打开',command=do_openfile)
save = tkinter.Button(file_buttons,text='保存',command=do_save)

melody_buttons = tkinter.Frame(buttons)

add = tkinter.Button(melody_buttons,text='添加',command=do_add)
remove = tkinter.Button(melody_buttons,text='删除',command=do_remove)
play = tkinter.Button(melody_buttons,text='播放',command=do_play)

openfile.pack(side=tkinter.LEFT)
save.pack(side=tkinter.LEFT)

file_buttons.pack(side=tkinter.LEFT)

add.pack(side=tkinter.LEFT)
remove.pack(side=tkinter.LEFT)
play.pack(side=tkinter.LEFT)


melody_buttons.pack(side=tkinter.LEFT,padx=10)

buttons.pack(side=tkinter.TOP)

note.pack(side=tkinter.LEFT)
note_group.pack(side=tkinter.LEFT)
dur.pack(side=tkinter.LEFT)

choice.pack()

melody.pack()

window.mainloop()
