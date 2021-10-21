from datetime import datetime
import pytz
import urllib.request 
import numpy as np
from scipy.io.wavfile import read, write # we use SciPy's read function to read WAV file

class Clock:
	def __init__(self, timezone, sample_rate=44100):
		self.timezone = timezone
		self.sample_rate = sample_rate
	
	def find_time(self):
		print(self.timezone)
		return (int(datetime.now(pytz.timezone(self.timezone)).strftime("%H")), int(datetime.now(pytz.timezone(self.timezone)).strftime("%M")))

	
	def change_time_zone(self, timezone):
		self.timezone = timezone
	
	def give_time_zone(self):
		return self.timezone
	
	def tell_time_English(self):
		hours, minutes = self.find_time()
		#WORK IN PROGRESS

	
	
	def create_audio_signal_Dutch(self, hours, minutes):
		#determine whether morning, day or night
		# 0:00 - 5:59 s'nachts
		# 6:00 - 11:59 s'ochtends
		# 12:00 - 17:59 s'middags
		# 18:00 - 23:59 s'avonds
		if hours in range(0,6):
			time_of_day = "nacht"
		elif hours in range(6,12):
			time_of_day = "ochtend"
		elif hours in range(12, 18):
			time_of_day = "middag"
		else:
			time_of_day = "avond"
		
		_, audio_time_of_day = read("Clock/" + time_of_day + ".wav")
		_, audio_het = read("Clock/het.wav")
		_, audio_is = read("Clock/is.wav")
		_, audio_half = read("Clock/half.wav")
		_, audio_voor = read("Clock/voor.wav")
		_, audio_over = read("Clock/over.wav")
		_, audio_uur = read("Clock/uur.wav")
		
		
		converted_hours = int(datetime.strptime(str(hours), "%H").strftime("%I"))
		if converted_hours == 0:
			converted_hours = 12

		
		#take correct minutes
		if minutes == 0:
			_, audio_hours = read(("Clock/" + str(converted_hours) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_hours, audio_uur, audio_time_of_day))
		
		elif minutes == 30:
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1
			
			_, audio_hours = read(("Clock/" + str(converted_hours) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_half, audio_hours, audio_time_of_day))
		
		elif minutes in range(1, 16):
			_, audio_hours = read(("Clock/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Clock/" + str(minutes) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_mins, audio_over, audio_hours, audio_time_of_day))
		
		elif minutes in range(16, 30):
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1
			
			_, audio_hours = read(("Clock/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Clock/" + str(30 - minutes) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_mins, audio_voor, audio_half, audio_hours, audio_time_of_day))
		
		elif minutes in range(31, 45):
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1
			
			_, audio_hours = read(("Clock/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Clock/" + str(minutes%15) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_mins, audio_over, audio_half, audio_hours, audio_time_of_day))
		
		else:
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1
			
			_, audio_hours = read(("Clock/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Clock/" + str(60 - minutes) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_mins, audio_voor, audio_hours, audio_time_of_day))

	def tell_time_Dutch(self):
		hours, minutes = self.find_time()
		return self.create_audio_signal_Dutch(hours, minutes), self.sample_rate
	
	def say_time_Dutch(self, hours, minutes):
		return self.create_audio_signal_Dutch(hours, minutes), self.sample_rate				



	
	
	





from tkinter import *
#import pygame
import sounddevice as sd
#import soundfile as sf



new = Clock(timezone = "CET") 
root = Tk()
root.title('Speaking Clock')
 
root.geometry("500x400")
#root.attributes('-zoomed', True)
#root.attributes('-fullscreen', True)
root.state('zoomed')

#OPTIONS = ["Europe/Amsterdam", "CET", "EET", "EST", "GMT", "Greenwich", "HST", "MET", "MST", "NZ"]
#OPTIONS = ["CET", "Greenwich", "ACST", "AFT", "AKST", "AST", "CAT", "CST", "EAT", "EET", "EST", "MSK", "MST", "PST", "WAT"]
OPTIONS = ["Europe/Amsterdam", "Greenwich", "Australia/Sydney", "Canada/Central", "Europe/Moscow", "Japan", "US/Pacific", "US/Central", "US/Hawaii"]
variable = StringVar(root)
variable.set(OPTIONS[0]) # default value
w = OptionMenu(root, variable, *OPTIONS)
w.pack()

def change_time_zone():
	zone = variable.get()
	new.change_time_zone(zone)

button_time_zone = Button(root, text="OK", command=change_time_zone)
button_time_zone.pack()

#pygame.mixer.init()# initialise the pygame
 
def play_complex():
	audio, sr = new.tell_time_Dutch()
	#write("audio1.wav", sr, audio.astype(np.int16))
	#pygame.mixer.music.load("audio1.wav")
	#pygame.mixer.music.play(loops=0)
	sd.play(audio, sr)
	status = sd.wait()

def play_simple():
	print("do nothing for now")
	#continue
	#audio, sr = new.tell_time_simple()
	#write("audio1.wav", sr, audio.astype(np.int16))
	#pygame.mixer.music.load("audio1.wav")
	#pygame.mixer.music.play(loops=0)
	#sd.play(audio, sr)
	#status = sd.wait()

lab = Label(root)
lab.pack()

def clock():
    #time = datetime.datetime.now().strftime("Time: %H:%M:%S")
	zone = new.give_time_zone()
	time = datetime.now(pytz.timezone(zone)).strftime("%H%M")
	lab.config(text=time)
    #lab['text'] = time
	root.after(1000, clock) # run itself again after 1000 ms

# run first time
clock()


title=Label(root,text="My speaking clock?",bd=9,relief=GROOVE,
			font=("times new roman",50,"bold"),bg="white",fg="Blue")
title.pack(side=TOP,fill=X)


play_button = Button(root, text="Simple time", font=("Helvetica", 32), command=play_simple)
play_button.pack(pady=20)

play_button2 = Button(root, text="Complex time", font=("Helvetica", 32), command=play_complex)
play_button2.pack(pady=20)





# declaring string variable
# for storing name and password
name_var=StringVar()
passw_var=StringVar()
 
  
# defining a function that will
# get the name and password and
# print them on the screen
def submit():
 
	name=name_var.get()
	password=passw_var.get()
	
	audio, sr = new.say_time_Dutch(int(name), int(password))
	write("audio1.wav", sr, audio.astype(np.int16))
	pygame.mixer.music.load("audio1.wav")
	pygame.mixer.music.play(loops=0)
	
	
	#print("The name is : " + name)
	#print("The password is : " + password)
	 
	#name_var.set("")
	#passw_var.set("")
	 
	 
# creating a label for
# name using widget Label
name_label = Label(root, text = 'Hour', font=('calibre',10, 'bold'))
  
# creating a entry for input
# name using widget Entry
name_entry = Entry(root,textvariable = name_var, font=('calibre',10,'normal')).pack()
  
# creating a label for password
passw_label = Label(root, text = 'Minute', font = ('calibre',10,'bold'))
  
# creating a entry for password
passw_entry=Entry(root, textvariable = passw_var, font = ('calibre',10,'normal')).pack()
  
# creating a button using the widget
# Button that will call the submit function
sub_btn=Button(root,text = 'Tell me the given time', command = submit).pack()
  
# placing the label and entry in
# the required position using grid
# method
#name_label.grid(row=0,column=0)
#name_entry.grid(row=0,column=1)
#passw_label.grid(row=1,column=0)
#passw_entry.grid(row=1,column=1)
#sub_btn.grid(row=2,column=1)




root.mainloop()
