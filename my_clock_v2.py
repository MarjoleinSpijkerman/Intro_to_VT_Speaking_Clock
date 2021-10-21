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
import sounddevice as sd

new = Clock(timezone = "Europe/Amsterdam") 
root = Tk()
root.title('Speaking Clock')
root.state('zoomed')

#Create our label
title=Label(root,text="My speaking clock!",bd=9,relief=GROOVE,
			font=("times new roman",50,"bold"),bg="white",fg="Blue")
title.pack(side=TOP,fill=X)


lab = Label(root)
lab.pack()

#Print the current time and Time zone
def print_time():
	zone = new.give_time_zone()
	time = datetime.now(pytz.timezone(zone)).strftime("%H:%M:%S")
	current_text = f"The current time is {time}\n The current time zone is: {zone} \n" 
	lab.config(text=current_text)
	root.after(1000, print_time) # run itself again after 1000 ms

# run first time
print_time()



#Creating the time zones and possibility to change time zone
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


#Play the audio for the time 
 
def play_Dutch():
	audio, sr = new.tell_time_Dutch()
	sd.play(audio, sr)
	#status = sd.wait()

def play_English():
	print("do nothing for now")
	#audio, sr = new.tell_time_simple()
	#sd.play(audio, sr)
	#status = sd.wait()

play_button = Button(root, text="What is the time?", font=("Helvetica", 32), command=play_English)
play_button.pack(pady=20)

play_button2 = Button(root, text="Hoe laat is het?", font=("Helvetica", 32), command=play_Dutch)
play_button2.pack(pady=20)	
	
	
	
	
#Create the code to say the time in a specific language 
# declaring string variable for the hour and minute
hour_var=StringVar()
minute_var=StringVar()
 
def submit():
	language = variable1.get()
	hour=hour_var.get()
	minute=minute_var.get()
	
	if language == "English":
		print("Add functionality for English")
	else:
		audio, sr = new.say_time_Dutch(int(hour), int(minute))
		sd.play(audio, sr)
	
 
hour_entry = Entry(root,textvariable = hour_var, font=('calibre',10,'normal')).pack()
minute_entry=Entry(root, textvariable = minute_var, font = ('calibre',10,'normal')).pack()
sub_btn=Button(root,text = 'Tell me the given time', command = submit).pack()
  
#Creating the time zones and possibility to change time zone
OPTIONS = ["Dutch", "English"]
variable1 = StringVar(root)
variable1.set(OPTIONS[0]) # default value
w = OptionMenu(root, variable1, *OPTIONS)
w.pack()




root.mainloop()
