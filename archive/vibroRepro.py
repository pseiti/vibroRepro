import pyaudio 
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import time
import random
import numpy as np
import conditions_exp2_1 as cx
import pandas as pd
import os

def quadFx(Hz,a=0.000082585,b=-0.027730656,c=3.144860541):
		return(a*Hz**2 + b*Hz + c)

def playVib(vol,dur,Hz):

	    p = pyaudio.PyAudio()
	 
	    volume = vol  # range [0.0, 1.0]
	    fs = 44100  # sampling rate, Hz, must be integer
	    duration = dur  # in seconds, may be float
	    f = Hz  # sine frequency, Hz, may be float

	    # generate samples, note conversion to float32 array
	    samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
	    # print(len(samples))

	    # per @yahweh comment explicitly convert to bytes sequence
	    output_bytes = (volume * samples).tobytes()

	    # for paFloat32 sample values must be in range [-1.0, 1.0]
	    stream = p.open(format=pyaudio.paFloat32,
	                    channels=1,
	                    rate=fs,
	                    output=True)

	    # play. May repeat with different volume values (if done interactively)
	    start_time = time.time()
	    stream.write(output_bytes)
	    # print("Played sound for {:.2f} seconds".format(time.time() - start_time))

	    stream.stop_stream()
	    stream.close()

	    p.terminate()

def newWindow(title,geom):
	Window = tk.Toplevel()
	Window.title(title)
	Window.geometry(geom)
	frame = tk.Frame(Window, height=300, width=600)
	frame.pack()

def text_fx(field_name,txt,configureState,state):
	field_name['text'] = txt
	field_name.pack(fill=Y)
	if configureState:
		field_name.configure(state)

# def clear_content(field_names):
# 	for x in range(len(field_names)):
# 		field_names[x].delete("1.0",END)
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
	LoG = globals()
	if LoG["btns_active"]:
		LoG["btns_active"] = False
		Cue = cur_stim.get("resp_T")
		LoG["F1"] = F1
		LoG["F2"] = F2
		LoG["F3"] = F3
		LoG["Cue"] = Cue
		display_frame.after(1,turn_off_P)
		display_frame.after(500,forget([StimInfo]))
		display_frame.after(1000,present_trialStims,F1,F2,F3,Cue)

# rating_keys = ["1","2","3","4","5","6"]
# def get_keypress_rating():
#	display.bind("<Key>",compute_rating)
# def compute_rating(event):
# 	included = False
# 	response = event.char
# 	print(response)
# 	for x in rating_keys:
# 		if response==x:
# 			included = True
# 			break
# 	if included==True:
# 		trial_fx(False)

def submit_response():
	LoG = globals()
	if LoG["btns_active"]:
		slider.set(np.random.randint(1,300))
		# LoG[""]
		LoG["i"]=1
		LoG["track"]+=1
		LoG["btns_active"] = False
		LoG["P_is_on"] = False
		df.to_csv(logfile_name)
		display_frame.after(1, forget, [StimInfo])
		display_frame.after(1, text_fx, StimInfo, """
Prepare for next stimulus!""", False, None)
		display_frame.after(2000, forget, [StimInfo])
		display_frame.after(3000, trial_fx, False)

def change_hz(val):
	global cur_hz
	LoG = globals()
	df = LoG["df"]
	cur_hz = slider.get()
	# columns = ["track","i","condition","PTS","Position","F1","F2","F3","Cue","adjustments"]
	if LoG["P_is_on"]:
		LoG["i"] += 1
		cur_stim = LoG["cur_stim"]
		df.loc[len(df.index),["track","i","condition","PTS","Position",
		"F1","F2","F3","Cue","adjustment"]] = [LoG["track"],LoG["i"],cur_stim.get("condition"),
		cur_stim.get("Same_or_Diff"),cur_stim.get("seqPos"),
		LoG["F1"],LoG["F2"],LoG["F3"],LoG["Cue"],cur_hz]
		if btns_active:
			tone_fx(cur_hz)
		LoG["df"] = df
		print(df)

def tone_fx(cur_hz):
	cur_amp = quadFx(cur_hz)
	playVib(cur_amp,1,cur_hz)

def switchToTest():
	LoG = globals()
	LoG["practice"] = False

def make_btns_active():
	global btns_active
	if P_is_on:
		btns_active = True

def play_probe():
	global cur_hz, P_is_on, btns_active
	if P_is_on:
		btns_active = True
		cur_amp = quadFx(cur_hz)
		playVib(cur_amp,1,cur_hz)

def slider_release(val):
    slider.bind("<ButtonRelease-1>", change_hz)
 
def trial_fx(firstCall):
	LoG = globals()
	ts_cur = time.time()
	if not LoG["P_is_on"]:
		if firstCall:
			LoG["track"]=1
			if LoG["practice"]:
				LoG["stim_list"] = cx.conditions_practice
			else:
				LoG["stim_list"] = cx.conditions_test
		# if (ts_cur-LoG["ts_init"])>duration_break:
		# 	mb = messagebox.showinfo(parent=menu,message="Zeit für eine Pause?\nAber bitte Vorsicht - Drücken Sie die 'Enter'-Taste oder klicken Sie 'OK' erst dann, wenn Sie ausreichend konzentriert sind: Durch das Schließen des Fensters beginnt nämlich schon der nächste Durchgang.")
		# 	LoG["ts_init"] = time.time()
		if len(LoG["stim_list"])>len(LoG["df"].index):
			print(len(LoG["stim_list"]),len(LoG["df"].index))
			cur_stim = LoG["stim_list"][len(LoG["df"].index)]
			LoG["cur_stim"] = cur_stim
			F1 = cur_stim.get("T1_hz")
			F2 = cur_stim.get("T2_hz")
			F3 = cur_stim.get("T3_hz")
			Cue = cur_stim.get("resp_T")
			LoG["F1"] = F1
			LoG["F2"] = F2
			LoG["F3"] = F3
			LoG["Cue"] = Cue
			present_trialStims(F1,F2,F3,Cue)
		else:
			text_fx(StimInfo, """
Thank you for your participation. You have passed the test session too.""",False,None)

def present_trialStims(F1,F2,F3,Cue):
	# global P_is_on, StimInfo
	LoG = globals()
	LoG["P_is_on"] = True
	StimInfo = LoG["StimInfo"]
	# StimInfo = Label(display_frame, font=("Arial bold",20))
	# T1_hz = 138
	# T2_hz = 170
	adjustP_message = """
Adjust P towards """ + str(Cue) 
	# t0 = time.time()
	# while time.time()-t0 < 2:
	# 	pass
	# text_fx(StimInfo,"((( T1 )))",False,None)
	display_frame.after(990, text_fx, StimInfo, """
((( T1 )))""",False,None)
	display_frame.after(1000, tone_fx, F1)
	display_frame.after(2000, forget, [StimInfo])
	display_frame.after(2990, text_fx, StimInfo, """
((( T2 )))""",False,None)
	display_frame.after(3000, tone_fx, F2)
	display_frame.after(4000, forget, [StimInfo])
	display_frame.after(4990, text_fx, StimInfo, """
((( T3 )))""",False,None)
	display_frame.after(5000, tone_fx, F3)
	display_frame.after(6000, forget, [StimInfo])
	display_frame.after(7000, text_fx, StimInfo, """
Adjust P towards T"""+ str(Cue) + ".",False,None)
	display_frame.after(7000, make_btns_active)

## Global objects
ts_init = time.time()
# duration_break = 1*60 # x minutes times 60 seconds
P_is_on = False
btns_active = False
practice = True
i = 0
columns = ["track","i","condition","PTS","Position","F1","F2","F3","Cue","adjustment"]
df = pd.DataFrame(columns=columns)
cur_stim = None

pcodefile = open("p_code.txt","r")
pcode = pcodefile.read()
pcodefile.close()

curwd = os.getcwd() + "/"
logfile_name = "{}vibroRepro_{}.csv".format(curwd, pcode)

## GUI 
menu = tk.Tk()
menu.title("Menu")
menu.geometry('200x300+1200+355')
menu_frame = tk.Frame(menu, height=300, width=200)
menu_frame.pack()

display = tk.Toplevel()
display.title("Display")
display.geometry('650x300+400+5')
display_frame = tk.Frame(display, height=300, width=500)
display_frame.pack()

StimInfo = Label(display_frame,font=("Arial",20))
StimInfo.pack()
StimInfo["text"] = """
Start by reading the instruction.
"""

controlr = tk.Toplevel()
controlr.title("Controller")
controlr.geometry('650x300+400+400')
controlr_frame = tk.Frame(controlr, height=300, width=500)
controlr_frame.pack()

button_practice = tk.Button(menu, text = "Practice", bg="White", fg="Black", 
	font=("Arial",15), padx=7, pady=10, height=1, width=8, command=lambda: trial_fx(True))
button_test = tk.Button(menu, text = "Test", bg="White", fg="Black", 
	font=("Arial",15), padx=7, pady=10, height=1, width=8, command=lambda: [switchToTest(), trial_fx(True)])
button_instr = tk.Button(menu, text = "Instruction", bg="White", fg="Black", 
	font=("Arial",15), padx=7, pady=10, height=1, width=8,
	command=lambda: newWindow("Instruction",'900x300+5+500'))
button_instr.place(relx=.3, rely=.2)
button_practice.place(relx=.3, rely=.4)
button_test.place(relx=.3, rely=.6)

slider = Scale(controlr_frame, from_= np.log(211), to=np.log(51),
	resolution=(np.log(211)-np.log(51))/(211-51), 
	length=400, showvalue=0, command=slider_release)
#slider.set((383-50)/2+50)
cur_hz = np.log(np.random.randint(51,211))
slider.set(cur_hz)
slider.place(relx=.5,rely=.2)
repeat_btn = Button(controlr_frame, text = "Repeat", command = repeat_trial,
	bg="White", fg="Black", font=("Arial",15), padx=7, pady=10, height=1, width=8)
repeat_btn.place(relx=0.1,rely=.6)
submit_btn = Button(controlr_frame, text = "Submit", command = submit_response,
	bg="White", fg="Black", font=("Arial",15), padx=7, pady=10, height=1, width=8)
submit_btn.place(relx=0.75,rely=.6)
play_btn = Button(controlr_frame, text = "Play P", command = play_probe,
	bg="White", fg="Darkgreen", font=("Arial",15,"bold"), padx=7, pady=10, height=1, width=8)
play_btn.place(relx=0.1,rely=.3)
# rating_image = ImageTk.PhotoImage(Image.open("rating_scale.png"))
# rating_label = Label(display_frame, image=rating_image)

menu.mainloop()