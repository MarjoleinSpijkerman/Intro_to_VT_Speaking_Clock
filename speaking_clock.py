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
	
	def create_audio_signal_English(self, hours, minutes):
		if hours in range(0,6):
			time_of_day = "in_the_morning"
		elif hours in range(6,12):
			time_of_day = "in_the_morning"
		elif hours in range(12, 18):
			time_of_day = "in_the_afternoon"
		else:
			time_of_day = "in_the_evening"
	
		converted_hours = int(datetime.strptime(str(hours), "%H").strftime("%I"))
		if converted_hours == 0:
			converted_hours = 12

		_, audio_time_of_day = read("Audio_English/" + time_of_day + ".wav")
		_, audio_it = read("Audio_English/it.wav")
		_, audio_is = read("Audio_English/is.wav")
		_, audio_half_past = read("Audio_English/half_past.wav")
		_, audio_quarter_past = read("Audio_English/quarter_past.wav")
		_, audio_quarter_to = read("Audio_English/quarter_to.wav")
		_, audio_past = read("Audio_English/past.wav")
		_, audio_in_the_morning = read("Audio_English/in_the_morning.wav")
		_, audio_in_the_evening = read("Audio_English/in_the_evening.wav")
		_, audio_in_the_afternoon = read("Audio_English/in_the_afternoon.wav")
		_, audio_to = read("Audio_English/to.wav")
	

		if minutes == 0:
			_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))
			return np.concatenate((audio_it, audio_is, audio_hours, audio_time_of_day))
		
		if minutes == 15:
			_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))
			return np.concatenate((audio_it, audio_is, audio_quarter_past, audio_hours, audio_time_of_day))
	
		elif minutes == 30:
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1
			
			_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))
			return np.concatenate((audio_it, audio_is, audio_half_past, audio_hours, audio_time_of_day))
	
		elif minutes == 45:
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1
			
			_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))
			return np.concatenate((audio_it, audio_is, audio_quarter_to, audio_hours, audio_time_of_day))
		
		elif minutes in range(1, 21):
			_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Audio_English/" + str(minutes) + ".wav"))
			return np.concatenate((audio_it, audio_is, audio_mins, audio_past, audio_hours, audio_time_of_day))
	
		elif minutes%10 == 0:
			if minutes <= 40:
				_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))
				_, audio_mins = read(("Audio_English/" + str(minutes) + ".wav"))
				return np.concatenate((audio_it, audio_is, audio_mins, audio_past, audio_hours, audio_time_of_day))
				
			else:
				if converted_hours == 12:
					converted_hours = 1
				else:
					converted_hours +=1
				
				minutes = 60 - minutes
				_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))
				_, audio_mins = read(("Audio_English/" + str(minutes) + ".wav"))
				return np.concatenate((audio_it, audio_is, audio_mins, audio_to, audio_hours, audio_time_of_day))
	  
		elif minutes in range(21, 41):
			tens = minutes//10 * 10
			mins = minutes%10

			_, audio_tens = read(("Audio_English/" + str(tens) + ".wav"))
			_, audio_mins = read(("Audio_English/" + str(mins) + ".wav"))
			_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))

			return np.concatenate((audio_it, audio_is, audio_tens, audio_mins, audio_past, audio_hours, audio_time_of_day))
			
		else:
			minutes = 60 - minutes
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1

			_, audio_mins = read(("Audio_English/" + str(minutes) + ".wav"))
			_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))

			return np.concatenate((audio_it, audio_is, audio_mins, audio_to, audio_hours, audio_time_of_day))		

	def say_time_English(self, hours, minutes):
		#based on the inserted hours and minutes, create the signal and return it
		return self.create_audio_signal_English(hours, minutes), self.sample_rate	

	def tell_time_English(self):
		#based on actual time
		hours, minutes = self.find_time()
		return self.create_audio_signal_English(hours, minutes), self.sample_rate	

	
	
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
		
		_, audio_time_of_day = read("Audio_Dutch/" + time_of_day + ".wav")
		_, audio_het = read("Audio_Dutch/het.wav")
		_, audio_is = read("Audio_Dutch/is.wav")
		_, audio_half = read("Audio_Dutch/half.wav")
		_, audio_voor = read("Audio_Dutch/voor.wav")
		_, audio_over = read("Audio_Dutch/over.wav")
		_, audio_uur = read("Audio_Dutch/uur.wav")
		
		
		converted_hours = int(datetime.strptime(str(hours), "%H").strftime("%I"))
		if converted_hours == 0:
			converted_hours = 12

		
		#take correct minutes
		if minutes == 0:
			_, audio_hours = read(("Audio_Dutch/" + str(converted_hours) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_hours, audio_uur, audio_time_of_day))
		
		elif minutes == 30:
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1
			
			_, audio_hours = read(("Audio_Dutch/" + str(converted_hours) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_half, audio_hours, audio_time_of_day))
		
		elif minutes in range(1, 16):
			_, audio_hours = read(("Audio_Dutch/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Audio_Dutch/" + str(minutes) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_mins, audio_over, audio_hours, audio_time_of_day))
		
		elif minutes in range(16, 30):
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1
			
			_, audio_hours = read(("Audio_Dutch/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Audio_Dutch/" + str(30 - minutes) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_mins, audio_voor, audio_half, audio_hours, audio_time_of_day))
		
		elif minutes in range(31, 45):
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1
			
			_, audio_hours = read(("Audio_Dutch/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Audio_Dutch/" + str(minutes%15) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_mins, audio_over, audio_half, audio_hours, audio_time_of_day))
		
		else:
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1
			
			_, audio_hours = read(("Audio_Dutch/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Audio_Dutch/" + str(60 - minutes) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_mins, audio_voor, audio_hours, audio_time_of_day))

	def tell_time_Dutch(self):
		hours, minutes = self.find_time()
		return self.create_audio_signal_Dutch(hours, minutes), self.sample_rate
	
	def say_time_Dutch(self, hours, minutes):
		return self.create_audio_signal_Dutch(hours, minutes), self.sample_rate				



	
	
	





from tkinter import *
import tkinter.font as font
import sounddevice as sd

new = Clock(timezone = "Europe/Amsterdam") 
root = Tk()
root.title('Speaking Clock')
root.state('zoomed')

#Create our label
title=Label(root,text="My speaking clock!",bd=9,relief=GROOVE,
			font=("times new roman",50,"bold"),bg="white",fg="Blue")
title.pack(side=TOP,fill=X)

my_font = font.Font(size=25, weight="bold")
lab = Label(root, font = my_font, fg='#6c3e83')
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
	#print("do nothing for now")
	audio, sr = new.tell_time_English()
	sd.play(audio, sr)
	#status = sd.wait()

play_button = Button(root, text="What is the time?", font=("Helvetica", 32), command=play_English)
play_button.pack(pady=20)

play_button2 = Button(root, text="Hoe laat is het?", font=("Helvetica", 32), command=play_Dutch)
play_button2.pack(pady=20)	
	
	
import nltk	
from nltk.tokenize import sent_tokenize
	
#Create the code to say the time in a specific language 
# declaring string variable for the hour and minute
hour_var=StringVar()
minute_var=StringVar()
 
def submit():
	language = variable1.get()
	hour=hour_var.get()
	minute=minute_var.get()
	
	has_errors = False 
	#check whether input even is a integer number 
	if hour.isdigit() == False or minute.isdigit() == False:
		has_errors = True
		
	#if it's a number, make sure it's a correct number
	elif int(minute) < 0 or int(minute) > 59 or int(hour) < 0 or int(hour) > 23:
		has_errors = True
	
	#Ok the input has an error, thus create the error message 
	if has_errors == True: 
		#create error message 
		error_message = Toplevel() #create a new pop up screen 
		text_message = "This is an invalid input. \n For hours: insert a number between 0 and 23. \n For minutes: insert a number between 0 and 59."
		sentences = sent_tokenize(text_message)
		
		#create the error message 
		for i in range(len(sentences)):
			if i == 0:
				my_font = font.Font(size=15, weight="bold")
			else:
				my_font = font.Font(size=12)
			label2 = Label(error_message, text=sentences[i], font=my_font) #add the created text message to the pop up screen 
			label2.pack(side= TOP, anchor="w")
		
		closing_button = Button(error_message, text = 'ok', command = error_message.destroy).pack()

	else:
		if language == "English":
			audio, sr = new.say_time_English(int(hour), int(minute))
			sd.play(audio, sr)
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
