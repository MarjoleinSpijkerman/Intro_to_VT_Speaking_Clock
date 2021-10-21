from datetime import datetime
import pytz
import urllib.request 
import numpy as np
from scipy.io.wavfile import read, write # we use SciPy's read function to read WAV file
from IPython.display import Audio, display

class Clock:
  #def __init__(self, sample_rate = 44100, timezone = 'Europe/Amsterdam'):	
  def __init__(self, timezone, sample_rate = 44100):
    self.timezone = timezone
    self.sample_rate = 44100
    self.minutes = 0
    self.hours = 0
  
  def print_current_time(self):
    print("Amsterdam time:", datetime.now(pytz.timezone(self.timezone)).strftime("%H:%M"))

  def find_time(self):
    print(self.timezone)
    return (int(datetime.now(pytz.timezone(self.timezone)).strftime("%H")), int(datetime.now(pytz.timezone(self.timezone)).strftime("%M")))

  def create_audio_number(self, number):
    if number < 1 or number > 59:
      print("invalid number")
      return 0
    elif number < 15 or number%10 == 0:
      file = "Clock/" + str(number) + ".wav"
      sr, data = read(file)
      return data
    elif number < 20:
      sr, file1 = read(("Clock/" + str(number%10) + ".wav"))
      sr, file2 = read(("Clock/" + str(int(number/10)*10) + ".wav"))
      return np.concatenate((file1, file2))
    else:
      sr, file1 = read(("Clock/" + str(number%10) + ".wav"))
      sr, file2 = read(("Clock/" + str(int(number/10)*10) + ".wav"))
      sr, file3 = read(("Clock/" + "en" + ".wav"))
      return np.concatenate((file1, file3, file2))

  def create_full_audio_simple(self, hours, minutes):
    sr, file1 = read("Clock/het.wav")
    sr, file2 = read("Clock/is.wav")
    return np.concatenate((file1, file2, hours, minutes))

  def tell_time_simple(self):
    self.hours, self.minutes = self.find_time()
    audio_hours = self.create_audio_number(self.hours)
    if self.minutes != 0:
      audio_minutes = self.create_audio_number(self.minutes)
    else: 
      sr, audio_minutes = read("Clock/uur.wav")
    time = self.create_full_audio_simple(audio_hours, audio_minutes)
    display(Audio(time, rate=self.sample_rate, autoplay=True))
    return time, self.sample_rate

  def tell_time_given_simple(self, hours, minutes):
    audio_hours = self.create_audio_number(hours)
    if minutes > 0:
      audio_minutes = self.create_audio_number(minutes)
    else:
      sr, audio_minutes = read("Clock/uur.wav")
    time = self.create_full_audio_simple(audio_hours, audio_minutes)
    display(Audio(time, rate=self.sample_rate, autoplay=True))
    return time, self.sample_rate
  
  def create_full_audio_complex(self, hours, minutes):
    self.hours = hours
    self.minutes = minutes
    #determine whether morning, day or night
    # 0:00 - 5:59 s'nachts
    # 6:00 - 11:59 s'ochtends
    # 12:00 - 17:59 s'middags
    # 18:00 - 23:59 s'avonds
    if self.hours in range(0,6):
      time_of_day = "nacht"
    elif self.hours in range(6,12):
      time_of_day = "ochtend"
    elif self.hours in range(12, 18):
      time_of_day = "middag"
    else:
      time_of_day = "avond"

    sr, audio1 = read("Clock/het.wav")
    sr, audio2 = read("Clock/is.wav")
    first_words = np.concatenate((audio1, audio2))
    sr, audio_time_of_day = read(("Clock/" + time_of_day + ".wav"))

    #convert hours to 12 hour clock
    converted_hours = int(datetime.strptime(str(self.hours), "%H").strftime("%I"))
    int(converted_hours)

    #take correct minutes
    if self.minutes == 0:
      sr, audio_hours = read(("Clock/" + str(converted_hours) + ".wav"))
      sr, uur = read("Clock/uur.wav")
      final = np.concatenate((first_words, audio_hours, uur, audio_time_of_day))
      display(Audio(final, rate=self.sample_rate, autoplay=True))

    elif self.minutes == 30:
      if converted_hours == 12:
        converted_hours = 1
      else:
        converted_hours +=1
      sr, audio_hours = read(("Clock/" + str(converted_hours) + ".wav"))
      sr, half = read("Clock/half.wav")
      final = np.concatenate((first_words, half, audio_hours, audio_time_of_day))
      display(Audio(final, rate=self.sample_rate, autoplay=True))

    elif self.minutes in range(1,16):
      sr, audio_hours = read(("Clock/" + str(converted_hours) + ".wav"))
      sr, mins = read(("Clock/" + str(self.minutes) + ".wav"))
      sr,over = read("Clock/over.wav")
      final = np.concatenate((first_words, mins, over, audio_hours, audio_time_of_day))
      display(Audio(final, rate=self.sample_rate, autoplay=True))

    elif self.minutes in range(16,30):
      if converted_hours == 12:
        converted_hours = 1
      else:
        converted_hours +=1
      sr, audio_hours = read(("Clock/" + str(converted_hours) + ".wav"))
      sr, mins = read(("Clock/" + str(30 - self.minutes) + ".wav"))
      sr, half = read("Clock/half.wav")
      sr, voor = read("Clock/voor.wav")
      final = np.concatenate((first_words, mins, voor, half, audio_hours, audio_time_of_day))
      display(Audio(final, rate=self.sample_rate, autoplay=True))

    elif self.minutes in range(31, 45):
      if converted_hours == 12:
        converted_hours = 1
      else:
        converted_hours +=1		
      sr, audio_hours = read(("Clock/" + str(converted_hours) + ".wav"))
      sr, mins = read(("Clock/" + str(self.minutes%15) + ".wav"))
      sr, half = read("Clock/half.wav")
      sr, over = read("Clock/over.wav")
      final = np.concatenate((first_words, mins, over, half, audio_hours, audio_time_of_day))      
      display(Audio(final, rate=self.sample_rate, autoplay=True))

    else:
      if converted_hours == 12:
        converted_hours = 1
      else:
        converted_hours +=1	
      #hours = int(converted_hours) + 1
      sr, audio_hours = read(("Clock/" + str(converted_hours) + ".wav"))
      sr, mins = read(("Clock/" + str(60 - self.minutes) + ".wav"))
      sr, voor = read("Clock/voor.wav")
      final = np.concatenate((first_words, mins, voor, audio_hours, audio_time_of_day))
      display(Audio(final, rate=self.sample_rate, autoplay=True))  
    return final
  
  
  def tell_time_given_complex(self, hours, minutes):
    return self.create_full_audio_complex(hours, minutes), self.sample_rate

  def tell_time_complex(self):
    self.hours, self.minutes = self.find_time()
    return self.create_full_audio_complex(self.hours, self.minutes), self.sample_rate

  def new_time_zone(self, timezone):
    self.timezone = timezone
    return




from tkinter import *
#import pygame
import sounddevice as sd
#import soundfile as sf



new = Clock("CET") 
root = Tk()
root.title('Speaking Clock')
 
root.geometry("500x400")
#root.attributes('-zoomed', True)

#OPTIONS = ["Europe/Amsterdam", "CET", "EET", "EST", "GMT", "Greenwich", "HST", "MET", "MST", "NZ"]
#OPTIONS = ["CET", "Greenwich", "ACST", "AFT", "AKST", "AST", "CAT", "CST", "EAT", "EET", "EST", "MSK", "MST", "PST", "WAT"]
OPTIONS = ["Europe/Amsterdam", "Greenwich", "Australia/Sydney", "Canada/Central", "Europe/Moscow", "Japan", "US/Pacific", "US/Central", "US/Hawaii"]
variable = StringVar(root)
variable.set(OPTIONS[0]) # default value
w = OptionMenu(root, variable, *OPTIONS)
w.pack()

def change_time_zone():
    zone = variable.get()
    new.new_time_zone(zone)

button_time_zone = Button(root, text="OK", command=change_time_zone)
button_time_zone.pack()

#pygame.mixer.init()# initialise the pygame
 
def play_complex():
    audio, sr = new.tell_time_complex()
    #write("audio1.wav", sr, audio.astype(np.int16))
    #pygame.mixer.music.load("audio1.wav")
    #pygame.mixer.music.play(loops=0)
    sd.play(audio, sr)
    status = sd.wait()

def play_simple():
    audio, sr = new.tell_time_simple()
    #write("audio1.wav", sr, audio.astype(np.int16))
    #pygame.mixer.music.load("audio1.wav")
    #pygame.mixer.music.play(loops=0)
    sd.play(audio, sr)
    status = sd.wait()




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
    
    audio, sr = new.tell_time_given_complex(int(name), int(password))
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
