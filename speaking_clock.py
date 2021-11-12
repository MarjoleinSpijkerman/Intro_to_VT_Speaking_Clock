from datetime import datetime
import pytz
import numpy as np
from scipy.io.wavfile import read
from tkinter import *
import tkinter.font as font
import sounddevice as sd
from nltk.tokenize import sent_tokenize

#The main code for the speaking clock
#For easier access to the clock and it's functions, we made it into an object 
class Clock:
	#initialize the timezone and we use a sample_rate of 44100 as we recorded all our audio at this sample_rate 
	def __init__(self, timezone, sample_rate=44100):
		self.timezone = timezone
		self.sample_rate = sample_rate
	
	#returns the time in hours and minutes at the current timezone 
	def find_time(self):
		return (int(datetime.now(pytz.timezone(self.timezone)).strftime("%H")), int(datetime.now(pytz.timezone(self.timezone)).strftime("%M")))
	
	#change the current timezone 
	def change_time_zone(self, timezone):
		self.timezone = timezone
	
	#returns the currrent timezone 
	def give_time_zone(self):
		return self.timezone
	
	#This is used to create the english audio signal, based on a specific time 
	def create_audio_signal_English(self, hours, minutes):
		#determine if it's morning, afternoon or evening 
		if hours in range(0,12):
			time_of_day = "in_the_morning"
		elif hours in range(12, 18):
			time_of_day = "in_the_afternoon"
		else:
			time_of_day = "in_the_evening"
		
		#Change the hours to a 12 hour scale 
		converted_hours = int(datetime.strptime(str(hours), "%H").strftime("%I"))
		if converted_hours == 0:
			converted_hours = 12
		
		#read all the necessary audio bits that we'll need to create our sentences 
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
	
		
		#we're first going over our edge cases at XX:00, XX:15, XX:30 and XX:45
		if minutes == 0:
			_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))
			return np.concatenate((audio_it, audio_is, audio_hours, audio_time_of_day))
		
		if minutes == 15:
			_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))
			return np.concatenate((audio_it, audio_is, audio_quarter_past, audio_hours, audio_time_of_day))
	
		elif minutes == 30:
			#at XX:30 etc, we start saying 30 to XX+1. So we need to change the hour to match up with this
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
		
		#Since the numbers 1-20 are irregular, we have recorded these previously
		elif minutes in range(1, 21):
			_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Audio_English/" + str(minutes) + ".wav"))
			return np.concatenate((audio_it, audio_is, audio_mins, audio_past, audio_hours, audio_time_of_day))
		
		#For the numbers 10, 20, 30, 40, and 50. We can also just use the prerecorded audio 
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
		
		#For the regular numbers between 20 and 40, we are using the format "minute" past "hour"
		elif minutes in range(21, 41):
			tens = minutes//10 * 10
			mins = minutes%10

			_, audio_tens = read(("Audio_English/" + str(tens) + ".wav"))
			_, audio_mins = read(("Audio_English/" + str(mins) + ".wav"))
			_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))

			return np.concatenate((audio_it, audio_is, audio_tens, audio_mins, audio_past, audio_hours, audio_time_of_day))
		
		#For the last cases, between 41 and 59, we use the format "minute" before "hour" 
		else:
			minutes = 60 - minutes
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1

			_, audio_mins = read(("Audio_English/" + str(minutes) + ".wav"))
			_, audio_hours = read(("Audio_English/" + str(converted_hours) + ".wav"))

			return np.concatenate((audio_it, audio_is, audio_mins, audio_to, audio_hours, audio_time_of_day))		
	
	#This creates an audio signal based on a specified time 
	def say_time_English(self, hours, minutes):
		#based on the inserted hours and minutes, create the signal and return it
		return self.create_audio_signal_English(hours, minutes), self.sample_rate	
	
	#This creates an audio signal based on the current time in the current timezone 
	def tell_time_English(self):
		#based on actual time
		hours, minutes = self.find_time()
		return self.create_audio_signal_English(hours, minutes), self.sample_rate	

	
	#Here we do the same thing but for Dutch. Since Dutch works a little different in comparison to English,
	#we use a slightly different function 
	def create_audio_signal_Dutch(self, hours, minutes):
		#determine whether morning, day or night
		# 0:00 - 5:59 --> s'nachts
		# 6:00 - 11:59 --> s'ochtends
		# 12:00 - 17:59 --> s'middags
		# 18:00 - 23:59 --> s'avonds
		if hours in range(0,6):
			time_of_day = "nacht"
		elif hours in range(6,12):
			time_of_day = "ochtend"
		elif hours in range(12, 18):
			time_of_day = "middag"
		else:
			time_of_day = "avond"
		
		#save the necessary audio files 
		_, audio_time_of_day = read("Audio_Dutch/" + time_of_day + ".wav")
		_, audio_het = read("Audio_Dutch/het.wav")
		_, audio_is = read("Audio_Dutch/is.wav")
		_, audio_half = read("Audio_Dutch/half.wav")
		_, audio_voor = read("Audio_Dutch/voor.wav")
		_, audio_over = read("Audio_Dutch/over.wav")
		_, audio_uur = read("Audio_Dutch/uur.wav")
		
		#Convert the hours from 24 to 12 hour scale 
		converted_hours = int(datetime.strptime(str(hours), "%H").strftime("%I"))
		if converted_hours == 0:
			converted_hours = 12

		
		#First we go over the cases of XX:00 and XX:30
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
		
		#We have four different cases XX:01 - XX:15, XX:16-XX:29, XX:31-XX:44, and XX:46-XX:59
		#For the case XX:01 - XX:15, we use the format "minute" past "hour"
		elif minutes in range(1, 16):
			_, audio_hours = read(("Audio_Dutch/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Audio_Dutch/" + str(minutes) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_mins, audio_over, audio_hours, audio_time_of_day))
		
		#For the case XX:16-XX:29, we use the format "minute" before half (before) "hour+1"
		elif minutes in range(16, 30):
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1
			
			_, audio_hours = read(("Audio_Dutch/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Audio_Dutch/" + str(30 - minutes) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_mins, audio_voor, audio_half, audio_hours, audio_time_of_day))
		
		#For the case XX:31-XX:44, we use the format "minute" past half (before) "hour+1"
		elif minutes in range(31, 45):
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1
			
			_, audio_hours = read(("Audio_Dutch/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Audio_Dutch/" + str(minutes%15) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_mins, audio_over, audio_half, audio_hours, audio_time_of_day))
		
		#For the case XX:46-XX:59, we use the format "minute" before "hour+1" 
		else:
			if converted_hours == 12:
				converted_hours = 1
			else:
				converted_hours +=1
			
			_, audio_hours = read(("Audio_Dutch/" + str(converted_hours) + ".wav"))
			_, audio_mins = read(("Audio_Dutch/" + str(60 - minutes) + ".wav"))
			return np.concatenate((audio_het, audio_is, audio_mins, audio_voor, audio_hours, audio_time_of_day))
	
	#This function returns the audio signal for the current time in current timezone 
	def tell_time_Dutch(self):
		hours, minutes = self.find_time()
		return self.create_audio_signal_Dutch(hours, minutes), self.sample_rate
	
	#This function returns the audio signal for a specific time 
	def say_time_Dutch(self, hours, minutes):
		return self.create_audio_signal_Dutch(hours, minutes), self.sample_rate				



###########################################################
#Now we create the graphical interface for the clock

#we create our clock object and set the default timezone to Amsterdam, as we are currently in the Netherlands 
new = Clock(timezone = "Europe/Amsterdam") 
#Initialize our GUI
root = Tk()
root.title('Speaking Clock')
root.state('zoomed')

#Create the name of the clock 
title=Label(root,text="My speaking clock!",bd=9,relief=GROOVE,
			font=("times new roman",50,"bold"),bg="white",fg="Blue")
title.pack(side=TOP,fill=X)


#Print the current time and Time zone
my_font = font.Font(size=25, weight="bold") #define the font we're using 
lab = Label(root, font = my_font, fg='#6c3e83') #create the label that displays the time and timezone 
lab.pack() #add it to the GUI

def print_time():
	zone = new.give_time_zone() #save timezone 
	time = datetime.now(pytz.timezone(zone)).strftime("%H:%M:%S") #save current time exactly 
	current_text = f"The current time is {time}\n The current time zone is: {zone} \n" #initialize the text we're displaying 
	lab.config(text=current_text) #replace the text in the label with the current text
	root.after(1000, print_time) # run itself again after 1000 ms, this way it gets updated every second. Making it able to display the clock at the second exact 

#Intialize running the print_time function. It will now keep running untill the program gets closed 
print_time()


#Creating the time zones and possibility to change time zone (It is possible to add more timezones to this list) 
OPTIONS = ["Europe/Amsterdam", "Greenwich", "Australia/Sydney", "Canada/Central", "Europe/Moscow", "Japan", "US/Pacific", "US/Central", "US/Hawaii"]
variable = StringVar(root)
variable.set(OPTIONS[0]) # default value
w = OptionMenu(root, variable, *OPTIONS)
w.pack()

#Create the button that allows us to change the time zone, pick item from list --> click button --> timezone gets changed 
def change_time_zone():
	zone = variable.get()
	new.change_time_zone(zone)

button_time_zone = Button(root, text="OK", command=change_time_zone)
button_time_zone.pack()


#Play the audio for the current time in current time zone 
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
	

	
#Create the code to say the time in a specific language 

hour_var=StringVar() # declaring string variable for the hour
minute_var=StringVar() # declaring string variable for the minute
 
def submit():
	language = variable1.get() #find language from menu 
	hour=hour_var.get() #find hour from text box 
	minute=minute_var.get() #find minute from text box 
	
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
		text_message = "This is an invalid input. \n For hours: insert a number between 0 and 23 in the first text box. \n For minutes: insert a number between 0 and 59 in the second text box."
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
	
	#No errors, we can create the audio based on these numbers 
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

#The main loop of the code, keep on looping 
root.mainloop()
