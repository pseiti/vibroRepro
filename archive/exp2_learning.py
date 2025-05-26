import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import module_waveforms as wf
import sounddevice as sd
import time
import random
import numpy as np
import pandas as pd
import matplotlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import (vlines,xticks)

def newWindow(title,geom):
    Window = tk.Toplevel()
    Window.title(title)
    Window.geometry(geom)
    frame = tk.Frame(Window, height=300, width=300)
    frame.pack()

def text_fx(field_name,txt,state,fg,pady):
    field_name.tag_configure("center",justify="center")
    field_name.pack(pady=pady)
    field_name.insert(1.0,txt)
    field_name.configure(state=state,fg=fg)
    field_name.tag_add("center","1.0","end")

def clear_content(field_names):
    for x in range(len(field_names)):
        field_names[x].delete("1.0",END)
def forget(objects):
    for x in objects:
        x.pack_forget()
def remember(objects,pady_objects):
    for x in range(len(objects)):
        objects[x].pack(pady=pady_objects[x])

def submit_response():
    global nTrials, cur_hz_set, slider_touched, nSliderAlt, submit_trace, nInARow
    submit_trace.append(nSliderAlt-1)
    diagramFun()
    nTrials += 1
    clear_content([StimInfo])
    cur_delta = DistanceToTarget(Hz_subj=cur_hz_set,Hz_target=T_hz)
    progressTrace.append(cur_delta)
    if len(progressTrace)>2:
        last3 = progressTrace[-3:]
        nInARow=0
        for x in last3:
            if x < 50: nInARow+=1
    forget([slider,submit_btn])
    FeedbackFun(cur_delta)
    slider_touched = False

def FeedbackFun(cur_delta):
    global Stop, progressTrace, nInARow, shuffle, T_hz
    Stop = True
    if shuffle==True:
        random.shuffle(F_target)
        T_hz = F_target[0]
    message = ""
    toRemember = [continue_btn]; toRemember_pady = [130]
    if cur_delta<50:
        if shuffle==False:
            if len(progressTrace)>2:
                if nInARow==3:
                    message = "You are done. Press 'Stop', if you want."
                    toRemember = [continue_btn,stop_btn]; toRemember_pady = [130,10]
        cur_fg = "green"
    else:
        cur_fg = "red"
        toRemember = [continue_btn]; toRemember_pady = [130]
    text_fx(field_name=StimInfo,txt="Distance: " + str(int(cur_delta)) + "%. \n" + message,
        state="normal",fg=cur_fg,pady=60)
    remember(toRemember,toRemember_pady)

def sliderFun(val):
    slider.bind("<ButtonRelease-1>", set_hz)

def set_hz(val):
    global cur_hz_set, df, nRuns, nSliderAlt, shuffle
    nSliderAlt += 1
    cur_hz_set = int(round(np.exp(slider.get())))
    cur_delta = DistanceToTarget(Hz_subj=cur_hz_set,Hz_target=T_hz)
    df = df.append({"Code":code,"Shuffle":shuffle,"Run":(nRuns+1),"TargetHz":T_hz,
        "Trial":(nTrials+1),"SubjHz":cur_hz_set,"Distance":cur_delta},ignore_index=True)
    print(df)
    play_Hz(freq=cur_hz_set)
    if slider_touched==False:
        remember([submit_btn],[0])
        LoG = globals()
        LoG["slider_touched"]=True

def slider_contPosition():
    position = np.random.randint(low=F[0],high=F[len(F)-1])
    slider.set(int(round(np.log(position))))

F = [51,55,60,70,82,96,112,132,154,180,195,211]
F_target = [60,70,82,96,112,132,154,180]

def DistanceToTarget(Hz_subj,Hz_target):
    Delta = Hz_subj - Hz_target
    if Delta == 0:
        Distance_in_percent = 0
    else:
        i_Hz_target = F.index(Hz_target)
        Hz_nextTarget = F[(i_Hz_target+1)] if Delta > 0 else F[(i_Hz_target-1)]
        Delta_max = abs(Hz_target-Hz_nextTarget)
        Distance_in_percent = np.round((Delta*100)/Delta_max)
        Distance_in_percent = abs(Distance_in_percent)
    return(Distance_in_percent)

def amplitudeFun(Hz,a=0.000082585,b=-0.027730656,c=3.144860541):
    return(a*Hz**2 + b*Hz + c)
def play_Hz(freq):
    amp_of_freq = amplitudeFun(freq)
    vibHz = wf.soundGene2(44100,1,fq=freq,amp=amp_of_freq)
    sd.play(vibHz,44100)
    sd.wait(0)

def stop():
    global Start, Stop, cur_btn_id, hz_buttons_dict, nRuns
    if Stop:
        nRuns += 1
        hz_buttons_dict[cur_btn_id]["state"] = "disabled"
        Start = True
        clear_content([StimInfo])#StimInfo.destroy()
        text_fx(field_name=StimInfo,txt="Wait for Instructions...",state="normal",fg="black",pady=60)
        forget([continue_btn,stop_btn])

def shuffle_run():
        global Start, Stop, shuffle, cur_btn_id
        shuffle = True
        cur_btn_id = "Shuffle"
        if Start:
            random.shuffle(F_target)
            T_hz = F_target[0]
            StimInfo.destroy()
            trial_fx(True, T_hz)
            Start = False

def trial_fx(firstCall, btn_hz):
    global T_hz
    T_hz = btn_hz
    if firstCall==True:
        global nTrials, slider_touched, progressTrace
        nTrials=0; progressTrace=[]
        slider_touched=False
        global StimInfo 
        StimInfo = Text(display_frame,height=4, highlightthickness=0, borderwidth=0, 
            font=("Arial bold",20))
    else:
        forget([continue_btn,stop_btn])
        clear_content([StimInfo])
    
    present_trialStims()

def present_trialStims():
    slider_contPosition()
    display_frame.after(1000, text_fx, StimInfo, "((( T )))","normal", "black", 60)
    display_frame.after(1010, play_Hz, T_hz)
    display_frame.after(2000, clear_content, [StimInfo])
    display_frame.after(3000, text_fx, StimInfo, "Reproduce...", "normal", "black", 60)
    display_frame.after(3001, remember, [slider], [50])

def diagramFun():
    global df, submit_trace, shuffle, T_hz
    distances = df["Distance"]
    if shuffle==False:
        if len(distances)>2:
            run_trace = df["Run"]
            targets_trace = df["TargetHz"]
            pos_newRun = []; freqs_presented = [targets_trace[0]]
            for i in list(range(1,len(run_trace))):
                if run_trace[i] is not run_trace[i-1]:
                    pos_newRun.append(i+.5)
                    freqs_presented.append(targets_trace[i])
            x = list(range(1,(len(distances)+1)))
            ax.clear()
            ax.set_ylim(0,400)
            ax.plot(x,distances,'--g',marker="o",fillstyle='none')
            submit_trace2 = []
            for i in range(len(submit_trace)):
                submit_trace2.append(submit_trace[i]+1)
            ax.scatter(submit_trace2,distances[submit_trace],marker="o",color="green")
            ax.hlines([50],xmin=0,xmax=len(x),colors="red",linestyles='solid')
            if len(pos_newRun)>0:
                ax.vlines([pos_newRun],ymin=0,ymax=400,colors="black")
            ax.text(1.5,200,str(freqs_presented[0]),size='x-large')
            for i in list(range(1,len(freqs_presented))):
                ax.text((pos_newRun[(i-1)])+.5,200,str(freqs_presented[i]),size='x-large')
            ax.xaxis.set_ticks([])
            canvas.draw()
    else:
        TargetHz_trace = df["TargetHz"]
        shuffle_trace = df["Shuffle"]
        shuffle_rows = []
        for srow in range(len(shuffle_trace)):
            if shuffle_trace[srow]==True: shuffle_rows.append(srow)
        #unique_THz_soFar = np.unique()

        T_hz_positions = []
        for srow in shuffle_rows:
            if TargetHz_trace[srow]==T_hz:
                T_hz_positions.append(srow)

            
    #canvas.draw()
## Global variables
ts_init = time.time()
padding_y = 10
Start = True
Stop = False
nRuns = 0
columns = ["Code","Shuffle","Run","TargetHz","Trial","SubjHz","Distance"]
df = pd.DataFrame(columns=columns)
code = "xyz"
nSliderAlt = 0
submit_trace = []

menu = tk.Tk()
menu.title("Menu")
menu_frame = tk.Frame(menu)
menu_frame.pack()

display = tk.Toplevel()
display.title("Events & Instructions")
display.geometry('450x200+500+5')
display_frame = tk.Frame(display, height=300, width=500)
display_frame.pack()
StimInfo = Text(display_frame,height=4, highlightthickness=0, borderwidth=0, font=("Arial bold",20))
text_fx(field_name=StimInfo,txt="Wait for Instructions...",state="normal",fg="black",pady=60)

controlr = tk.Toplevel()
controlr.title("Controller")
controlr.geometry('200x600+250+5')
controlr_frame = tk.Frame(controlr, height=450, width=200)
controlr_frame.pack()

display2 = tk.Toplevel()
display2.title("Experimenter's Display")
display2.geometry('600x500+600+280')
diagram = Figure(figsize=(5,4),dpi=100)
canvas = FigureCanvasTkAgg(diagram, master=display2)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
ax = diagram.add_subplot(111)
ax.set_ylim(0,400)
ax.xaxis.set_ticks([])

# display3 = tk.Toplevel()
# display2.title("Experimenter's Display (Shuffle)")
# display2.geometry('600x500+600+280')
# diagram_shuffle = Figure(figsize=(5,4),dpi=100)
# canvas_shuffle = FigureCanvasTkAgg(diagram_shuffle, master=display3)  # A tk.DrawingArea.
# canvas_shuffle.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
# ax_shuffle = diagram_shuffle.add_subplot(111)
# ax_shuffle.set_ylim(0,400)
# ax_shuffle.xaxis.set_ticks([])

slider = Scale(controlr_frame, from_=np.log(211), to=np.log(51),
    resolution=(np.log(211)-np.log(51))/(211-51),
    length=400, showvalue=0, command=sliderFun)

hz_buttons_labels = list(range(1,9))
random.shuffle(hz_buttons_labels)
hz_buttons_dict={}
for btn_i in range(len(hz_buttons_labels)):
    def start_run(btn_i_freq=F_target[hz_buttons_labels[btn_i]-1],btn_id=btn_i):
        global Start, Stop, cur_btn_id, shuffle
        shuffle = False
        cur_btn_id = btn_id
        if Start:
            StimInfo.destroy()
            trial_fx(True, btn_i_freq)
            Start = False
    hz_buttons_dict[btn_i]=tk.Button(menu, text=str(btn_i+1), command= start_run,
        fg="Black", font=("Arial",15), padx=7, pady=10, height=1, width=4)
    hz_buttons_dict[btn_i].pack(padx=60,pady=5)

submit_btn = Button(controlr_frame, text = "Submit", command = submit_response,
    bg="White", fg="Black", font=("Arial",15), padx=7, pady=10, height=1, width=8)
continue_btn = Button(controlr_frame, text = "Continue", 
    command = lambda: trial_fx(firstCall=False, btn_hz=T_hz),
    bg="White", fg="Black", font=("Arial",15), padx=7, pady=10, height=1, width=8)
stop_btn = tk.Button(controlr_frame, text = "Stop", bg="White", fg="Black", 
    font=("Arial",15), padx=7, pady=10, height=1, width=8,
    command=stop)
shuffle_btn = tk.Button(menu, text = "Shuffle", bg="White", fg="Black", 
    font=("Arial",15), padx=7, pady=10, height=1, width=8, command=shuffle_run)
shuffle_btn.pack(padx=60,pady=20)

# instr_btn = tk.Button(menu, text = "Instruction", bg="White", fg="Black", 
#     font=("Arial",15), padx=7, pady=10, height=1, width=8,
#     command=lambda: newWindow("Instruction",'900x300+5+500'))
# start_btn = tk.Button(menu, text = "Start", bg="White", fg="Black", 
#     font=("Arial",15), padx=7, pady=10, height=1, width=8, command = start)

# instr_btn.place(relx=.3, rely=.2)
# start_btn.place(relx=.3, rely=.4)

menu.mainloop()






