import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import module_waveforms as wf
import sounddevice as sd
import time
import random

def newWindow(title,geom):
	Window = tk.Toplevel()
	Window.title(title)
	Window.geometry(geom)
	frame = tk.Frame(Window, height=HEIGHT, width=WIDTH)
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
def remember(objects):
	for x in objects:
		x.pack()

def turn_off_P():
	global P_is_on
	P_is_on = False

def repeat_trial():
	global btns_active
	if btns_active:
		btns_active = False
		display_frame.after(1,turn_off_P)
		display_frame.after(500,clear_content([StimInfo]))
		display_frame.after(1000,present_trialStims)

def get_keypress_rating():
	controlr_frame.bind("<Key>",compute_rating)
def compute_rating(event):
	#LoG = globals()
	#locked = LoG["locked"]
	included = False
	response = event.char
	for x in rating_keys:
		if response==x:
			included = True
			break
	if included==True:
		menu.destroy()

	
def submit_response():
	global btns_active
	if btns_active:
		btns_active = False
		display_frame.after(1,turn_off_P)
		display_frame.after(2,clear_content([StimInfo]))
		display_frame.after(3,text_fx, StimInfo, "How confident are you?","normal", "black", 20)
		display_frame.after(4,remember, [rating_label])
		display_frame.after(5,get_keypress_rating)

def quadFx(Hz,a=0.000082585,b=-0.027730656,c=3.144860541):
	return(a*Hz**2 + b*Hz + c)


def change_hz(val):
	global cur_hz
	cur_hz = slider.get()
	play_probe()

def tone_fx(vibHz):
	sd.play(vibHz,44100)
	sd.wait()

def play_probe():
	global cur_hz, P_is_on, btns_active
	if P_is_on:
		btns_active = True
		vibHz = wf.soundGene2(44100,1,fq=cur_hz,amp=quadFx(Hz=cur_hz))
		sd.play(vibHz,44100)
		sd.wait(0)
		display_frame.after(500,play_probe)

def trial_fx(firstCall):
	LoG = globals()
	ts_cur = time.time()
	if (ts_cur-LoG["ts_init"])>duration_break:
		mb = messagebox.showinfo(parent=win,message="Zeit für eine Pause?\nAber bitte Vorsicht - Drücken Sie die 'Enter'-Taste oder klicken Sie 'OK' erst dann, wenn Sie ausreichend konzentriert sind: Durch das Schließen des Fensters beginnt nämlich schon der nächste Durchgang.")
		LoG["ts_init"] = time.time()
	if firstCall==True:
		global nTrials
		nTrials = 0
	global StimInfo	
	StimInfo = Text(display_frame,height=4, highlightthickness=0, borderwidth=0, 
		font=("Arial bold",20))
	present_trialStims()

def present_trialStims():
	global P_is_on
	P_is_on = True
	T1_hz = wf.soundGene2(44100,1,fq=138,amp=1)
	T2_hz = wf.soundGene2(44100,1,fq=170,amp=1)
	cur_message = "Adjust P towards " + crit_target + "."
	display_frame.after(1000, text_fx, StimInfo, "((( T1 )))","normal", "black", 120)
	display_frame.after(1010, tone_fx, T1_hz)
	display_frame.after(2000, clear_content, [StimInfo])
	display_frame.after(3000, text_fx, StimInfo, "((( T2 )))", "normal", "black", 120)
	display_frame.after(3010, tone_fx, T2_hz)
	display_frame.after(4000, clear_content, [StimInfo])
	#display_frame.after(5000, text_fx, StimInfo, "((( P )))", "normal", "black", 120)
	display_frame.after(5000, text_fx, StimInfo, cur_message, "normal", "black", 120)
	display_frame.after(5010, play_probe)

## Global variables
ts_init = time.time()
padding_y = 10
duration_break = 1*60 # x minutes times 60 seconds
cur_hz = 154# 154
P_is_on = True
btns_active = False

targets = ["T1","T2"]; random.shuffle(targets)
crit_target = targets[0]
print(crit_target)

menu = tk.Tk()
menu.title("Menu")
menu_frame = tk.Frame(menu, height=300, width=200)
menu_frame.pack()

display = tk.Toplevel()
display.title("Display")
display.geometry('650x300+400+50')
display_frame = tk.Frame(display, height=300, width=500)
display_frame.pack()

controlr = tk.Toplevel()
controlr.title("Controller")
controlr.geometry('650x300+400+450')
controlr_frame = tk.Frame(controlr, height=300, width=500)
controlr_frame.pack()

button_practice = tk.Button(menu, text = "Practice", bg="White", fg="Black", 
	font=("Arial",15), padx=7, pady=10, height=1, width=8)
button_practice.place(relx=.3, rely=.4)
button_test = tk.Button(menu, text = "Test", bg="White", fg="Black", 
	font=("Arial",15), padx=7, pady=10, height=1, width=8)
button_instr = tk.Button(menu, text = "Instruction", bg="White", fg="Black", 
	font=("Arial",15), padx=7, pady=10, height=1, width=8,
	command=lambda: newWindow("Instruction",'900x300+5+500'))
button_instr.place(relx=.3, rely=.2)
button_practice.place(relx=.3, rely=.4)
button_test.place(relx=.3, rely=.6)

slider = Scale(controlr_frame, from_=383, to=50, length=200, showvalue=0, 
	command=change_hz)
#slider.set((383-50)/2+50)
slider.set(cur_hz)
slider.place(relx=.5,rely=.2)
repeat_btn = Button(controlr_frame, text = "Repeat", command = repeat_trial,
	bg="White", fg="Black", font=("Arial",15), padx=7, pady=10, height=1, width=8)
repeat_btn.place(relx=0.1,rely=.4)
submit_btn = Button(controlr_frame, text = "Submit", command = submit_response,
	bg="White", fg="Black", font=("Arial",15), padx=7, pady=10, height=1, width=8)
submit_btn.place(relx=0.75,rely=.4)

rating_image = ImageTk.PhotoImage(Image.open("rating_scale.png"))
rating_label = Label(display_frame, image=rating_image)

trial_fx(firstCall=True)

menu.mainloop()