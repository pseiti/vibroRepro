import os
import wave
import contextlib
from psychopy import sound
from psychopy.visual import Window, TextStim, Rect, ImageStim  
from psychopy.core import wait, Clock, quit   
import random 
from psychopy.event import waitKeys, getKeys, clearEvents
import time 
from tkinter import *
import module_waveforms as wf
import conditions_exp2_1 as cx
import sounddevice as sd
import numpy as np

def quit_exp():
    
    quit_question = TextStim( win, wrapWidth = 2, text = "Sind Sie sicher, dass Sie das Experiment beenden möchten?" +
        "\nWenn Sie das Experiment beenden möchten, drücken Sie nochmals die Taste Q." +
        "\nWenn Sie mit dem Experiment fortfahren möchten, drücken Sie die Leertaste.", color = 'black')
    quit_question.draw()
    win.flip()
    pressed = waitKeys(keyList = ['q', 'space'])
    if 'q' in pressed:
        quit_text = TextStim( win, wrapWidth = 2, text = "Vielen Dank für die Teilnahme.", color = 'black')
        quit_text.draw()
        win.flip()
        wait(1)
        quit()
        
def getKeys_check_quit(keyList):
    pressed = getKeys(keyList = keyList)
    if 'q' in pressed:
        quit_exp()
    return pressed 
        
def waitKeys_check_quit(keyList):
    pressed = waitKeys(keyList = keyList)
    if 'q' in pressed: 
        quit_exp()
    return pressed 
        
def tone_fx(vibHz):    
    sd.play(vibHz,44100)
    sd.wait() 
        
def show_instruction(instruction_text, min_wait = 0.1):
    instruction_page.setText(instruction_text)
    instruction_page.draw()
    win.flip()
    wait( min_wait ) 
   
    waitKeys_check_quit(keyList = ['space', 'q'])
    wait(1)
    
def change_hz(val):
    global cur_Hz
    cur_Hz.append(int(round(np.exp(slider.get()))))
    cur_Hz_string.append(str(int(round(np.exp(slider.get())))))
    print(cur_Hz)
    play_probe()
    close_btn["state"] = NORMAL
    
def slider_resp(val):
    slider.bind("<ButtonRelease-1>", change_hz)
    
def quadFx(Hz,a=0.000082585,b=-0.027730656,c=3.144860541):
    return(a*Hz**2 + b*Hz + c)
    
def play_probe():
    cur_Amp = quadFx(Hz=cur_Hz[-1])
    vibHz = wf.soundGene2(44100,1,fq=cur_Hz[-1],amp=cur_Amp)
    sd.play(vibHz,44100)
    sd.wait(0)


F = [51,55,60,70,82,96,112,132,154,180,195,211]

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
    

    

win = Window([800, 600], color = "white", screen = 1, fullscr = False)


# PRACTICE SLIDER

instruction_page = TextStim(win, wrapWidth = 1.7, height = 0.08, color = 'black') 
show_instruction("In the following experiment you are again presented with tactile stimuli. The experiment will take about … minutes. " + 
"Several breaks are included. The experiment consists of two practice sessions and one experimental session. In short, the task of the experimental session is to adjust " + 
"one vibration frequency to match another vibration frequency by using a slider. In the first practice session you will practice the use of the slider and in the second practice " + 
"session you will practice the experimental task. A detailed explanation of the task occurs before each session. Please wear the ear plugs and ear muffs during all sessions but " + 
"of course you can remove them during the breaks. \n\nPlease press the space bar to read the instructions of the first practice session.")

instruction_page = TextStim(win, wrapWidth = 1.7, height = 0.07, color = 'black') 
show_instruction("SLIDER PRACTICE SESSION \n\nIn the experimental task you will have to use a slider in order to match tactile vibration frequencies." + 
"Therefore, in the current practice session, you will practice the use of the slider first. For that purpose, please put the ear plugs and ear muffs on and the index finger of your " + 
"non-dominant hand on the vibration device in the box. Again, please just rest your finger on it and don’t exert any pressure. In each trial, you will receive one single vibration impulse. " + 
"Your task is to move the slider (which represents a range of frequencies) up or down until the frequency you adjusted with it matches the frequency given at the beginning of each trial. " + 
"If you move the slider up the frequency becomes higher, if you move it down the frequency becomes lower. If you think you adjusted the slider correctly press the ‘Submit’ button. " + 
"You then get feedback about how close you matched the frequency. The feedback is given as the distance of your adjustment to the target in percent. The goal is to reach below 40% distance. " +
"Please try to adjust the frequency as exact as possible. \n:-) \n\nIf you're ready please press the space bar to start the practice session.") 


#high = [154,180,195,211] *50 
#mid = [82,96,112,132] *50
#low = [51,55,60,70] *50
#
#fq_lists = [high, mid, low]

fq_list = [51,55,60,70,82,96,112,132,154,180,195,211] *50

trial_nr = 0
n_success = 0
    
with open('p_code.txt') as p:
    p_code = p.read()

with open(str(p_code) + "_scale_practice.csv", 'a') as practice_result_file: 
    
    practice_result_file.write("p_code;trial_nr;fq_hz;fq_amp;init_slider_pos;set_fq;resp_diff;resp_diff_percent;resp_time\n")
    
#    for fq_list in fq_lists: 
#        
#        random.shuffle(fq_list)
#        
#        n_success = 0
#        
#        if fq_list == high: 
#            fq_range = "high"
#            instruction_page = TextStim(win, wrapWidth = 1.7, height = 0.08, color = 'black') 
#            show_instruction("For this practice block, frequencies are divided into high, middle, and low frequencies. In this first block you will practice the high frequencies. " + 
#                "If you're ready, start the practice block by pressing the space bar.")
#                
#        elif fq_list == mid:
#            fq_range = "mid"
#            instruction_page = TextStim(win, wrapWidth = 1.7, height = 0.08, color = 'black') 
#            show_instruction("Now you do the second block in which you will practice the middle frequencies. Note that the spaces between the frequencies on the slider are now somewhat smaller " + 
#                "than in the last block so you should be more careful in adjusting them. If you're ready, start the practice block by pressing the space bar.")
#        
#        else:
#            fq_range = "low"
#            instruction_page = TextStim(win, wrapWidth = 1.7, height = 0.08, color = 'black') 
#            show_instruction("Now you continue with the third block in which you will practice the low frequencies. The spaces between the frequencies on the slider are now even smaller. " + 
#                "Please be as careful and exact as you can in adjusting them. If you're ready, start the practice block by pressing the space bar.")

    for fq in fq_list:

        random.shuffle(fq_list)
        
        trial_nr += 1
        
        cur_Hz = []
        cur_Hz_string = []
        
        fq_amp = quadFx(fq)
        
        pressed = getKeys(keyList = ['q', 'space'])
        if 'q' in pressed:
            quit_exp() 
        
        wait(1)
        fq_text = TextStim(win, wrapWidth = 1.8, color = "black", text = "((( )))")
        fq_text.draw()
        win.flip()
        tone_fx(wf.soundGene2(44100,1,fq,quadFx(fq)))

        slider_win = Tk()
        slider_win.title("Slider")
        win_frame = Frame(slider_win, height=500, width=300)
        win_frame.pack()
        
        text = Label(slider_win, text="Please use the slider to adjust \nthe current frequency on it. \nPress the button to submit your decision.")
        text.place(x=50,y=30)
        
        slider = Scale(slider_win, from_=np.log(211), to=np.log(51), resolution=(np.log(211)-np.log(51))/(211-51), length=400, showvalue=0,
        command=slider_resp)
                
        init_slider_pos = np.log(random.randrange(51,211))

        slider.set(init_slider_pos)
        slider.place(relx=.5,rely=.2)
        
        timer = Clock()
        
        close_btn = Button(slider_win, text = "Submit", state = DISABLED, command = slider_win.destroy)
        close_btn.pack(side=BOTTOM,pady=20)
        close_btn.pack(side=RIGHT, padx=10)
        
        mainloop()
        
        resp_time = -1            
        resp_time = timer.getTime()
        
        resp_diff = fq - cur_Hz[-1]
        
        Distance_in_percent = DistanceToTarget(cur_Hz[-1], fq)
        
        practice_result_file.write(str(p_code) + ";" + str(trial_nr) + ";" + str(fq) + ";" + str(fq_amp) + ";" + 
            str(np.exp(init_slider_pos)) + ";" + ' '.join(cur_Hz_string) + ";" + str(resp_diff) + ";" + str(Distance_in_percent) + ";" + str(resp_time*1000) + ";" + "\n")
        
        feedback = TextStim(win, wrapWidth = 1.8, color = "black", text = "The distance between the given frequency and the one you adjusted is " + 
            str(Distance_in_percent) + "%. \n\nPress the space bar to continue.") 
        feedback.draw()
        win.flip()
        waitKeys(keyList = ['space'])
                
        if Distance_in_percent < 40: 
                n_success += 1 
                
        if n_success > 30:
            break
                
            
    instruction_page = TextStim(win, wrapWidth = 1.8, height = 0.08, color = 'black') 
    show_instruction("Thank you! You successfully completed the first practice part. Please press the space bar to continue.")


# PRACTICE EXPERIMENT

image_path = "C:/Users/augstenm90/Documents/PhD/CAT-CIM/Experimente/Experiment 2/Experiment 2.1/Code/confidence_scale.jpg"

random.shuffle(cx.conditions_test)

instruction_page = TextStim(win, wrapWidth = 1.8, height = 0.08, color = 'black') 
show_instruction("PRACTICE SESSION \n\nNow you continue to the task practice session. You need the ear protection during the whole experiment and your finger again rests on the device. " +
    "The experimental task is as follows: In each trial, you will feel three successive vibration impulses (targets) on your finger (T1, T2, and T3). Your task is to adjust " + 
    "one of the three targets on the slider. The instruction regarding which target to adjust appears after the presentation of T3. " + 
    "When you finished adjusting the instructed target on the slider press the ‘Submit’ button. After that, you are presented with a 5-point rating scale on which you rate how confident " +
    "you are regarding your adjustment (0% - 100% sure). Before the experiment starts, you are presented with ten practice trials which you can repeat as often as you like. " + 
    "In this practice session, you again receive feedback on how close your adjustment matched the given target. Again, a distance below 40% should be reached." +
    "\n\nIf you're ready to start the practice session please press the space bar.")

with open(str(p_code) + "_dms_adjust.csv", 'a') as main_result_file: 
    
    main_result_file.write("p_code;trial_nr;practice;condition;seqPos;Same_or_Diff;resp_T;T1_hz;T1_amp;T2_hz;T2_amp;T3_hz;T3_amp;init_slider_pos;set_fq;resp_diff;resp_diff_percent;rating;resp_time\n") 
    
    n_success = 0    
    trial_nr = 0
    
    for condi in cx.conditions_test:
        
        trial_nr += 1
        
        cur_Hz = []
        cur_Hz_string = []
        
        practice = True 
        condition = condi.get("condition")
        seqPos = condi.get("seqPos")
        Same_or_Diff = condi.get("Same_or_Diff")
        T1_hz = condi.get("T1_hz")
        T1_amp = quadFx(condi.get("T1_hz"))
        T2_hz = condi.get("T2_hz")
        T2_amp = quadFx(condi.get("T2_hz"))
        T3_hz = condi.get("T3_hz")
        T3_amp = quadFx(condi.get("T3_hz"))
        resp_T = condi.get("resp_T")
                    
        pressed = getKeys(keyList = ['q', 'space'])
        if 'q' in pressed:
            quit_exp() 
        
        stim_text = TextStim(win, text = "((( T1 )))", color = 'black')
        stim_text.draw()
        win.flip()
        tone_fx(wf.soundGene2(44100,1,condi.get("T1_hz"),quadFx(condi.get("T1_hz"))))
        wait(1)
        
        stim_text = TextStim(win, text = "((( T2 )))", color = 'black')
        stim_text.draw()
        win.flip()
        tone_fx(wf.soundGene2(44100,1,condi.get("T2_hz"),quadFx(condi.get("T2_hz"))))
        wait(1)

        stim_text = TextStim(win, text = "((( T3 )))", color = 'black')
        stim_text.draw()
        win.flip()
        tone_fx(wf.soundGene2(44100,1,condi.get("T3_hz"),quadFx(condi.get("T3_hz"))))
        
        pos_text = TextStim(win, color = "black", text = "Adjust T" + str(resp_T) + " on the slider.")
        pos_text.draw()
        win.flip()
        
        slider_win = Tk()
        slider_win.title("Slider")
        win_frame = Frame(slider_win, height=500, width=300)
        win_frame.pack()
        
        text = Label(slider_win, text="Press the 'Submit' button to submit \nand to start the next trial.")
        text.place(x=60,y=30)
        
        slider = Scale(slider_win, from_=np.log(211), to=np.log(51), resolution=(np.log(211)-np.log(51))/(211-51), length=400, showvalue=0,
        command=slider_resp)
        
        init_slider_pos = np.log(random.randrange(51,211))

        slider.set(init_slider_pos)
        slider.place(relx=.5,rely=.2)
        
        timer = Clock()
        
        close_btn = Button(slider_win, text = "Submit", state = DISABLED, command = slider_win.destroy)
        close_btn.pack(side=BOTTOM,pady=20)
        close_btn.pack(side=RIGHT, padx=10)
        
        mainloop()
        
        resp_time = -1
        resp_time = timer.getTime()
        
        if resp_T == 1:
            resp_diff = condi.get("T1_hz") - cur_Hz[-1]
            abs_diff = abs(condi.get("T1_hz") - cur_Hz[-1])
            fq = condi.get("T1_hz")
        elif resp_T == 2:
            resp_diff = condi.get("T2_hz") - cur_Hz[-1]
            abs_diff = abs(condi.get("T2_hz") - cur_Hz[-1])
            fq = condi.get("T2_hz")
        else:
            resp_diff = condi.get("T3_hz") - cur_Hz[-1]
            abs_diff = abs(condi.get("T3_hz") - cur_Hz[-1])
            fq = condi.get("T3_hz")
            
        rating_text = TextStim(win, pos = (0, 0.5), wrapWidth = 1.8, text = "How confident are you about your adjustment? \nPlease press the corresponding key.", color = "black")
        rating_scale = ImageStim(win, pos = (0, -0.5), size = (1.8, 0.6), image = image_path)
        rating_text.draw()
        rating_scale.draw()
        win.flip()
        rating = waitKeys(keyList = ["1", "2", "3", "4", "5"])
        wait(1)
        
        Distance_in_percent = DistanceToTarget(cur_Hz[-1], fq) 

        feedback = TextStim(win, wrapWidth = 1.8, color = "black", text = "The distance between the frequency of the target and the one you adjusted is " + 
            str(Distance_in_percent) + "%. \n\nPress the space bar to continue.") 
        feedback.draw()
        win.flip()
        waitKeys(keyList = ['space'])
         
        main_result_file.write(str(p_code) + ";" + str(trial_nr) + ";" + str(practice) + ";" + str(condition) + ";" + str(seqPos) + ";" + str(Same_or_Diff) + ";" + 
            str(resp_T) + ";" + str(T1_hz) + ";" + str(T1_amp) + ";" + str(T2_hz) + ";" + str(T2_amp) + ";" + str(T3_hz) + ";" + str(T3_amp) + ";" + 
            str(np.exp(init_slider_pos)) + ";" + ' '.join(cur_Hz_string) + ";" + str(resp_diff) + ";" + str(Distance_in_percent) + ";" + rating[0] + ";" + 
            str(resp_time*1000) + ";" + "\n")
        
        if Distance_in_percent < 40: 
            n_success += 1 
            
        if n_success > 10: 
            quest = TextStim(win, color = "black", text = "Do you want to repeat the practice session or continue to the main experiment?" + 
                "\n\nPress 'R' for 'Repeat' and 'C' for 'Continue'.")
            quest.draw()
            win.flip()
            wait(1)
            
            answer = waitKeys(keyList = ["r", "c"])
            if answer[0] == "r":
                n_success = 0
            else:
                break
                
    instruction_page = TextStim(win, wrapWidth = 1.8, height = 0.08, color = 'black') 
    show_instruction("Thank you! You successfully completed the second practice part. \n\nYou now go on to the longest but final part of the experiment. Everything remains similar to the " +
        "second practice session except that you will not receive feedback on your adjustments. You can have a break after every 50 trials. Please use the breaks to gain back your concentration " +
        "and to relax your arm (you can remove it from the box and stretch if you like). \n\nIf you're ready please press the space bar to start the experiment.")
            

# MAIN EXPERIMENT

    random.shuffle(cx.conditions_test)

    trial_nr = 0

    for condi in cx.conditions_test:
        
        trial_nr += 1
        
        cur_Hz = []
        cur_Hz_string = []
        
        practice = False 
        condition = condi.get("condition")
        seqPos = condi.get("seqPos")
        Same_or_Diff = condi.get("Same_or_Diff")
        T1_hz = condi.get("T1_hz")
        T1_amp = quadFx(condi.get("T1_hz"))
        T2_hz = condi.get("T2_hz")
        T2_amp = quadFx(condi.get("T2_hz"))
        T3_hz = condi.get("T3_hz")
        T3_amp = quadFx(condi.get("T3_hz"))
        resp_T = condi.get("resp_T")
                    
        pressed = getKeys(keyList = ['q', 'space'])
        if 'q' in pressed:
            quit_exp() 
        
        stim_text = TextStim(win, text = "((( T1 )))", color = 'black')
        stim_text.draw()
        win.flip()
        tone_fx(wf.soundGene2(44100,1,condi.get("T1_hz"),quadFx(condi.get("T1_hz"))))
        wait(1)
        
        stim_text = TextStim(win, text = "((( T2 )))", color = 'black')
        stim_text.draw()
        win.flip()
        tone_fx(wf.soundGene2(44100,1,condi.get("T2_hz"),quadFx(condi.get("T2_hz"))))
        wait(1)

        stim_text = TextStim(win, text = "((( T3 )))", color = 'black')
        stim_text.draw()
        win.flip()
        tone_fx(wf.soundGene2(44100,1,condi.get("T3_hz"),quadFx(condi.get("T3_hz"))))
        
        pos_text = TextStim(win, color = "black", text = "Adjust T" + str(resp_T) + " on the slider.")
        pos_text.draw()
        win.flip()
        
        slider_win = Tk()
        slider_win.title("Slider")
        win_frame = Frame(slider_win, height=500, width=300)
        win_frame.pack()
        
        text = Label(slider_win, text="Press the button to submit \nand to start the next trial.")
        text.place(x=60,y=30)
        
        slider = Scale(slider_win, from_=np.log(211), to=np.log(51), resolution=(np.log(211)-np.log(51))/(211-51), length=400, showvalue=0,
        command=slider_resp)
        
        init_slider_pos = np.log(random.randrange(51,211))

        slider.set(init_slider_pos)
        slider.place(relx=.5,rely=.2)
        
        timer = Clock()
        
        close_btn = Button(slider_win, text = "Submit", state = DISABLED, command = slider_win.destroy)
        close_btn.pack(side=BOTTOM,pady=20)
        close_btn.pack(side=RIGHT, padx=10)
        
        mainloop()
        
        resp_time = -1
        resp_time = timer.getTime()
        
        if resp_T == 1:
            resp_diff = condi.get("T1_hz") - cur_Hz[-1]
            fq = condi.get("T1_hz")
        elif resp_T == 2:
            resp_diff = condi.get("T2_hz") - cur_Hz[-1]
            fq = condi.get("T2_hz")
        else:
            resp_diff = condi.get("T3_hz") - cur_Hz[-1]
            fq = condi.get("T3_hz")

        Distance_in_percent = DistanceToTarget(cur_Hz[-1], fq)
        
        rating_text = TextStim(win, pos = (0, 0.5), wrapWidth = 1.8, text = "How confident are you about your adjustment? \nPlease press the corresponding key.", color = "black")
        rating_scale = ImageStim(win, pos = (0, -0.5), size = (1.8, 0.6), image = image_path)
        rating_text.draw()
        rating_scale.draw()
        win.flip()
        rating = waitKeys(keyList = ["1", "2", "3", "4", "5"])
        wait(1)
        
        main_result_file.write(str(p_code) + ";" + str(trial_nr) + ";" + str(practice) + ";" + str(condition) + ";" + str(seqPos) + ";" + str(Same_or_Diff) + ";" + 
            str(resp_T) + ";" + str(T1_hz) + ";" + str(T1_amp) + ";" + str(T2_hz) + ";" + str(T2_amp) + ";" + str(T3_hz) + ";" + str(T3_amp) + ";" + 
            str(np.exp(init_slider_pos)) + ";" + ' '.join(cur_Hz_string) + ";" + str(resp_diff) + ";" + str(Distance_in_percent) + ";" + rating[0] + ";" + 
            str(resp_time*1000) + ";" + "\n")
        
        if trial_nr % 50 == 0: 
            
            break_text = TextStim(win, color = "black", text = "Time to have a break." + 
                "\n\nPlease continue only if you feel sufficiently concentrated and relaxed. \n\nPress the space bar to continue.")
            break_text.draw()
            win.flip()
            wait(1)
            
            waitKeys(keyList = ["space"])
            
thanks = TextStim(win, color = "black", text = "The experiment is finished. \n\nThank you for your participation! :)") 
thanks.draw()
win.flip()
wait(5)








