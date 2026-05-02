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
        messagebox.showerror('音频输出器错误',f'错误：未找到 FluidSynth 端口，请确保 FluidSynth 正在运行。\n可用端口：{available_ports}')
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
            if duration[:2]!='附点':
                if '+' not in duration:
                    if '#' not in note:
                        data.append((note[0]+note[-1], int(duration)))
                    else:
                         data.append((note[0]+note[4]+note[-1], int(duration)))
                else:
                    if '#' not in note:
                        data.append((note[0]+note[-1], duration))
                    else:
                        data.append((note[0]+note[4]+note[-1], duration))
            else:
                if '#' not in note:
                    data.append((note[0]+note[-1],duration[2:]+'.'))
                else:
                    data.append((note[0]+note[4]+note[-1],duration[2:]+'.'))
        else:
            if duration[:2]!='附点':
                if '+' not in duration:
                    data.append(('R', int(duration)))
                else:
                    data.append(('R', duration))
            else:
                data.append(('R', duration[2:]+'.'))
    return data

def close():
    if read_all_rows(melody)!=[]:
        do = messagebox.askyesno('退出','如果您还没有保存内容，现在退出可能会丢失您目前编辑的所有内容。确认退出吗？')
        if do==True:
            window.destroy()
    else:
        window.destroy()

def do_openfile():
    if read_all_rows(melody)!=[]:
        do = messagebox.askyesno('打开文件','打开文件将会覆盖您目前编辑的所有内容。确认打开吗？')
        if do==False:
            return
    path = filedialog.askopenfilename()
    if path not in ('',()):
        for item in melody.get_children():
            melody.delete(item)
        with open(path) as f:
            for i in json.loads(f.read()):
                if i[0]=='R' or i[0]=='r':
                    if isinstance(i[1],str):
                        if i[1][-1]=='.':
                            melody.insert('',index=tkinter.END,text='休止',value='附点'+i[1][:-1])
                    else:
                        melody.insert('',index=tkinter.END,text='休止',value=i[1])
                else:
                    map = {'c':'1','d':'2','e':'3','f':'4','g':'5','a':'6','b':'7',
                           'C':'1','D':'2','E':'3','F':'4','G':'5','A':'6','B':'7'}
                    if '#' not in i[0]:
                        item = i[0][0]+'('+str(map[i[0][0]])+')'+i[0][-1]
                    else:
                        item = i[0][0]+'('+str(map[i[0][0]])+')'+i[0][1]+i[0][-1]
                    if isinstance(i[1],str):
                        if i[1][-1]=='.':
                            melody.insert('',index=tkinter.END,text=item,value='附点'+i[1][:-1])
                        else:
                            melody.insert('',index=tkinter.END,text=item,value=i[1])
                    else:
                        melody.insert('',index=tkinter.END,text=item,value=i[1])
 

def do_save():
    path = filedialog.asksaveasfilename()
    if path not in ('',()):
        if not path.endswith('.json'):
            do = messagebox.askyesno('保存文件','本程序需要的扩展名是“.json”。需要自动加入扩展名吗？')
            if do==True:
                path += '.json'
        with open(path,'w') as f:
            f.write(json.dumps(read_all_rows(melody)))
        messagebox.showinfo('保存文件','保存成功！')

def do_play():
    if bpm.get()!='':
        if bpm.get().isdigit():
            mlist = notemidi.translate(read_all_rows(melody),bpm=float(bpm.get()))
            play_midi_notes(mlist)
        else:
            messagebox.showerror('播放错误','每分节拍数(BPM)必须是数字！')
    else:
        messagebox.showerror('播放错误','每分节拍数(BPM)不能为空！')

def do_add():
    if nvar.get()=='休止':
        if dotvar.get()=='有附点':
            melody.insert('',index=tkinter.END,text='休止',value='附点'+dvar.get())
        else:
            melody.insert('',index=tkinter.END,text='休止',value=dvar.get())
    else:
        if dotvar.get()=='有附点':
            melody.insert('',index=tkinter.END,text=nvar.get()+ngvar.get(),value='附点'+dvar.get())
        else:
            melody.insert('',index=tkinter.END,text=nvar.get()+ngvar.get(),value=dvar.get())

def do_insert():
    if not melody.selection():
        return
    
    pos = melody.index(melody.selection()[0])+1
    
    if nvar.get()=='休止':
        if dotvar.get()=='有附点':
            melody.insert('',index=pos,text='休止',value='附点'+dvar.get())
        else:
            melody.insert('',index=pos,text='休止',value=dvar.get())
    else:
        if dotvar.get()=='有附点':
            melody.insert('',index=pos,text=nvar.get()+ngvar.get(),value='附点'+dvar.get())
        else:
            melody.insert('',index=pos,text=nvar.get()+ngvar.get(),value=dvar.get())


def do_adddur():
    if melody.selection()!=():
        if adddurvar.get()!='不加时值':
            item = melody.selection()[0]
            print(melody.item(item,'values'))
            if melody.item(item,'values')[0][0:2]!='附点':
                melody.item(item,values=(melody.item(item,'values')[0]+'+'+adddurvar.get(),))
            else:
                messagebox.showerror('时值错误','附点和加时值不能放在一起！')

def do_remove():
    if melody.selection()!=():
        melody.delete(melody.selection())

window = tkinter.Tk()
window.title('Tiiiny Music')
window.protocol('WM_DELETE_WINDOW',close)

melody = ttk.Treeview(window,columns=('duration',))
melody.heading('#0',text='音符')
melody.heading('#1',text='时值')

choice = tkinter.Frame(window)

nvar = tkinter.StringVar(choice)
nvar.set('C(1)')
note = tkinter.OptionMenu(choice,nvar,'C(1)','C(1)#','D(2)','D(2)#','E(3)','F(4)','F(4)#','G(5)','G(5)#','A(6)','A(6)#','B(7)','休止')
ngvar = tkinter.StringVar(choice)
ngvar.set('4')
note_group = tkinter.OptionMenu(choice,ngvar,'1','2','3','4','5','6','7','8')
dvar = tkinter.StringVar(choice)
dvar.set('4')
dur = tkinter.OptionMenu(choice,dvar,'1','2','4','8','16','32')
dotvar = tkinter.StringVar(choice)
dotvar.set('无附点')
dot = tkinter.OptionMenu(choice,dotvar,'有附点','无附点')
adddurvar = tkinter.StringVar(choice)
adddurvar.set('不加时值')
adddurmenu = tkinter.OptionMenu(choice,adddurvar,'不加时值','1','2','4','8','16','32')


buttons = tkinter.Frame(window)

file_buttons = tkinter.Frame(buttons)

openfile = tkinter.Button(file_buttons,text='打开',command=do_openfile)
save = tkinter.Button(file_buttons,text='保存',command=do_save)

melody_buttons = tkinter.Frame(buttons)

add = tkinter.Button(melody_buttons,text='添加',command=do_add)
insert = tkinter.Button(melody_buttons,text='插入',command=do_insert)
adddur = tkinter.Button(melody_buttons,text='加时值',command=do_adddur)
remove = tkinter.Button(melody_buttons,text='删除',command=do_remove)
play = tkinter.Button(melody_buttons,text='播放',command=do_play)
bpmmsg = tkinter.Label(melody_buttons,text='BPM')
bpm = tkinter.Entry(melody_buttons)
bpm.insert(0,'120')

openfile.pack(side=tkinter.LEFT)
save.pack(side=tkinter.LEFT)

file_buttons.pack(side=tkinter.LEFT)

add.pack(side=tkinter.LEFT)
insert.pack(side=tkinter.LEFT)
adddur.pack(side=tkinter.LEFT)
remove.pack(side=tkinter.LEFT)
play.pack(side=tkinter.LEFT)
bpmmsg.pack(side=tkinter.LEFT)
bpm.pack(side=tkinter.LEFT)


melody_buttons.pack(side=tkinter.LEFT,padx=10)

buttons.pack(side=tkinter.TOP)

note.pack(side=tkinter.LEFT)
note_group.pack(side=tkinter.LEFT)
dur.pack(side=tkinter.LEFT)
dot.pack(side=tkinter.LEFT)
adddurmenu.pack(side=tkinter.LEFT)

choice.pack()

melody.pack()

window.mainloop()
