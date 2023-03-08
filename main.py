import tkinter as tk
import pyautogui as pg
from random import randint
from win32api import GetMonitorInfo, MonitorFromPoint

#gets monitor informations
monitor_info=GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area=monitor_info.get('Work')
screen_width=work_area[2] 
work_height=work_area[3] 

#for randomization of the pet movements
idle_num =[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] 
sleep_num = [19, 20, 21, 22, 23, 24, 25]
walk_left = [13, 14, 15]
walk_right = [16, 17, 18]

class Fox:
    def __init__(self):
        #create a tkinter window to put the gifs
        self.window=tk.Tk()

        #get the gifs and make them repeat frame by frame (uses an array)
        self.idle = [tk.PhotoImage(file='C:\\your\\path\\to\\file',format = 'gif -index %i' %(i)) for i in range(5)] #(5 frames)
        
        self.idle_to_sleep = [tk.PhotoImage(file='C:\\your\\path\\to\\file',format = 'gif -index %i' %(i)) for i in range(4)] #(4 frames)

        self.sleep = [tk.PhotoImage(file='C:\\your\\path\\to\\file',format = 'gif -index %i' %(i)) for i in range(3)] #(3 frames)
        
        self.sleep_to_idle = [tk.PhotoImage(file='C:\\your\\path\\to\\file',format = 'gif -index %i' %(i)) for i in range(4)]#sleep to idle gif (4 frames)

        self.walk_positive = [tk.PhotoImage(file='C:\\your\\path\\to\\file',format = 'gif -index %i' %(i)) for i in range(4)]#walk to left gif (4 frames)

        self.walk_negative = [tk.PhotoImage(file='C:\\your\\path\\to\\file',format = 'gif -index %i' %(i)) for i in range(4)]#walk to right gif (4 frames)

        self.x=int(screen_width*0.8)
        self.y=work_height-82

        self.i_frame=0
        self.state=1
        self.event_number=randint(1, 3)

        self.frame=self.idle[0]

        #adjust the gifs/window color to get rid of the background of the pet
        self.window.config(highlightbackground='black')
        self.label = tk.Label(self.window,bd=0,bg='black')
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor','black')

        self.label.pack()

        self.window.after(1, self.update, self.i_frame, self.state, self.event_number, self.x)
        self.window.mainloop()

    #make the event change (probability and when to do an action)
    def event(self, i_frame, state, event_number, x):
        if self.event_number in idle_num:
            self.state=0
            self.window.after(400, self.update, self.i_frame, self.state, self.event_number, self.x)
        elif self.event_number==12:
            self.state=1
            self.window.after(100, self.update, self.i_frame, self.state, self.event_number, self.x)
        elif self.event_number in walk_left:
            self.state=4
            self.window.after(100, self.update, self.i_frame, self.state, self.event_number, self.x)
        elif self.event_number in walk_right:
            self.state=5
            self.window.after(100, self.update, self.i_frame, self.state, self.event_number, self.x)
        elif self.event_number in sleep_num:
            self.state=2
            self.window.after(400,self.update, self.i_frame, self.state, self.event_number, self.x)
        elif self.event_number == 26:
            self.state = 3
            self.window.after(100, self.update, self.i_frame, self.state, self.event_number, self.x)

    #function to make the gif work and randomize the pet actions
    def animate(self, i_frame, array, event_number, a, b):
        if self.i_frame<len(array)-1:
            self.i_frame+=1
        else:
            self.i_frame=0
            self.event_number=randint(a, b)
        return self.i_frame, self.event_number

    #update the pet movements with its previous actions assigned numbers
    def update(self, i_frame, state, event_number, x):
    
        if self.state == 0:
            self.frame=self.idle[self.i_frame]
            self.i_frame, self.event_number=self.animate(self.i_frame, self.idle, self.event_number, 1, 18)
        elif state == 1:
            self.frame = self.idle_to_sleep[self.i_frame]
            self.i_frame, self.event_number = self.animate(self.i_frame, self.idle_to_sleep, self.event_number,19, 19)
        elif self.state == 2:
            self.frame = self.sleep[self.i_frame]
            self.i_frame, self.event_number = self.animate(self.i_frame, self.sleep, self.event_number, 19, 26)
        elif self.state == 3:
            self.frame = self.sleep_to_idle[self.i_frame]
            self.i_frame, self.event_number=self.animate(self.i_frame, self.sleep_to_idle, self.event_number, 1, 1)
        elif self.state == 4 and self.x>0:
            self.frame=self.walk_positive[self.i_frame]
            self.i_frame, self.event_number=self.animate(self.i_frame, self.walk_positive, self.event_number, 1, 18)
            self.x-=3
        elif self.state == 5 and x<(screen_width-72):
            self.frame=self.walk_negative[self.i_frame]
            self.i_frame, self.event_number=self.animate(self.i_frame, self.walk_negative, self.event_number, 1, 18)
            self.x+=3

        self.window.geometry('180x100+'+str(self.x)+'+'+str(self.y))
        self.label.configure(image=self.frame)
        self.window.after(1, self.event, self.i_frame, self.state, self.event_number, self.x)

fox=Fox() 