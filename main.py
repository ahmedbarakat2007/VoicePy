import tkinter
#ProjectGurukul's Voice recorder
#Import necessary modules
import sounddevice as sd
from tkinter import *
import queue
import soundfile as sf
import threading
from tkinter import messagebox

#Functions to play, stop and record audio in Python voice recorder
#The recording is done as a thread to prevent it being the main process
def threading_rec(x):
   if x == 1:
       #If recording is selected, then the thread is activated
       t1=threading.Thread(target= record_audio)
       t1.start()
   elif x == 2:
       #To stop, set the flag to false
       global recording
       recording = False
       messagebox.showinfo(message="Recording finished")
       q.status.set("")
   elif x == 3:
       #To play a recording, it must exist.
       if file_exists:
           #Read the recording if it exists and play it
           data, fs = sf.read("audio.wav", dtype='float32')
           sd.play(data,fs)
           sd.wait()
       else:
           #Display and error if none is found
           messagebox.showerror(message="Record something to play") 
    

#Fit data into queue
def callback(indata, frames, time, status):
   q.put(indata.copy())

#Recording function
def record_audio():
   #Declare global variables   
   global recording
   #Set to True to record
   recording= True  
   global file_exists
   #Create a file to save the audio
   q.status.set("-Recording")
   with sf.SoundFile("audio.wav", mode='w', samplerate=44100,
                       channels=2) as file:
   #Create an input stream to record audio without a preset time
           with sd.InputStream(samplerate=44100, channels=2, callback=callback):
               while recording == True:
                   #Set the variable to True to allow playing the audio later
                   file_exists =True
                   #write into file
                   file.write(q.get())

#Define the user interface for Voice Recorder using Python
voice_rec = Tk()
voice_rec.geometry("315x70")
voice_rec.title("AudiPy (Made By Ahmed Barakat)")
voice_rec.config(bg="#061d4f")
#Create a queue to contain the audio data
q = queue.Queue()
q.track = StringVar()
q.status = StringVar()
#Declare variables and initialise them
recording = False
file_exists = False
 
#Button to record audio
record_btn = Button(voice_rec, text="Record Audio", command=lambda m=1:threading_rec(m), bg="#21396e",fg="white", borderwidth=0)
#Stop button
stop_btn = Button(voice_rec, text="Stop Recording", command=lambda m=2:threading_rec(m), bg="#21396e",fg="white", borderwidth=0)
#Play button
play_btn = Button(voice_rec, text="Play Recording", command=lambda m=3:threading_rec(m), bg="#21396e",fg="white", borderwidth=0)
trackstatus = Label(voice_rec,textvariable=q.status,font=("arial",16,"bold"),bg="#061d4f",fg="white").place(x=95,y=0)
#Position buttons
record_btn.place(x=10,y=35)
stop_btn.place(x=110,y=35)
play_btn.place(x=220,y=35)
voice_rec.resizable(False, False)
photo = PhotoImage(file = "icon.png")
voice_rec.iconphoto(False, photo)
voice_rec.mainloop()