from tkinter import *
import tkinter.font as font
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
import time
import sys
import datetime
import threading
import pyfireconnect
import urllib.request
import os

#**************************************FIREBASE SET UP**************************************

#Check for internet connection
def checkInternet():
  internet = True
  try:
    urllib.request.urlopen('https://smart-saucer.firebaseio.com/')
  except:
    internet = False
  return internet

time.sleep(1)
hasInternet = checkInternet()

#Set timezone
os.environ['TZ'] = 'US/Eastern'
time.tzset()

#pyfire set up if internet is connected
if(hasInternet):
  config = {
    "apiKey" : "AIzaSyBq-3aOFMlc-9IcSV-X2ZvrIceH5Uvz-U4",
    "authDomain" : "smart-saucer.firebaseapp.com",
    "databaseURL" : "https://smart-saucer.firebaseio.com/",
    "storageBucket" : "smart-saucer.appspot.com"
  }

  firebase = pyfireconnect.initialize(config)
  db = firebase.database()

#***********************************VARIABLE DECLARATIONS***********************************

# Light, normal, extra sauce speeds
lt = 25
med = 50
ext = 75

# Motor speed
global s1_speed, s2_speed, s3_speed, s4_speed
s1_speed = med # Sauce stepper motor 1 speed (default to normal / medium)
s2_speed = med # Sauce stepper motor 2 speed
s3_speed = med # Sauce stepper motor 3 speed
s4_speed = med # Sauce stepper motor 4 speed

# Size / Steps / Sauce Amount
global size
size = -1 # No default size
global sauce_spin_steps
sauce_spin_steps = 1000
global amount
amount = med #normal amount at start

# Double click
global click
click = 0

#***************************************MOTOR SET UP****************************************

# Sauce stepper motor set up (pumps)
S1_DIR = 36   # Direction GPIO Pin
S1_STEP = 38  # Step GPIO Pin
S2_DIR = 31   # Direction GPIO Pin
S2_STEP = 33  # Step GPIO Pin
S3_DIR = 29   # Direction GPIO Pin
S3_STEP = 32  # Step GPIO Pin
S4_DIR = 21   # Direction GPIO Pin
S4_STEP = 23  # Step GPIO Pin

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(S1_DIR, GPIO.OUT)
GPIO.setup(S1_STEP, GPIO.OUT)
GPIO.setup(S2_DIR, GPIO.OUT)
GPIO.setup(S2_STEP, GPIO.OUT)
GPIO.setup(S3_DIR, GPIO.OUT)
GPIO.setup(S3_STEP, GPIO.OUT)
GPIO.setup(S4_DIR, GPIO.OUT)
GPIO.setup(S4_STEP, GPIO.OUT)

# Big stepper motor set up (spins)
T6_DIR = 13   # Direction GPIO Pin
T6_STEP = 15  # Step GPIO Pin

GPIO.setup(T6_DIR, GPIO.OUT)
GPIO.setup(T6_STEP, GPIO.OUT)

#*************************************BUTTON FUNCTIONS**************************************

def setSize(new_size):
    global click
    global size
    if size == new_size:
        click = click + 1
    else:
        click = 0
        size = new_size
    if click == 1:
        runSaucer()

#************************************SAUCER FUNCTIONS***************************************

#Function for running saucer
def runSaucer():
    print("SPEED: " + str(s1_speed))
    print("SIZE: " + str(size))
    print("RUNNING SAUCE\n")

    # Run corresponding saucer pumps
    pumpProgram(size)
    spinFunc(25, sauce_spin_steps)
    stopPumping()
    stopSpinning()

#Functions for starting and stopping spin
def spinProgram(speed):
    # Create new thread
    spin = threading.Thread(target=spinFunc, args=(speed,1,))
    # Start new thread
    spin.start()

def spinFunc(speed, steps):
  global spinning  #create global
  spinning = True
  
  spin_delay = (100-speed)/50000
  while spinning and steps > 0:
    if spinning == False:
      break
    else:
      GPIO.output(T6_STEP, GPIO.HIGH)
      time.sleep(spin_delay)
      GPIO.output(T6_STEP, GPIO.LOW)
      time.sleep(spin_delay)
      steps = steps - 1

def stopSpinning():
  global spinning
  spinning = False
  GPIO.output(T6_STEP, GPIO.LOW)

#Functions for starting and stopping sauce
def pumpProgram(size):
    # Create new threads
    pump1 = threading.Thread(target=pumpFunc, args = (S1_STEP, s1_speed,))
    pump2 = threading.Thread(target=pumpFunc, args = (S2_STEP, s2_speed,))
    pump3 = threading.Thread(target=pumpFunc, args = (S3_STEP, s3_speed,))
    pump4 = threading.Thread(target=pumpFunc, args = (S4_STEP, s4_speed,))
    
    # Start new thread
    pump1.start()
    if size >= 10:
        pump2.start()
    if size >= 12:
        pump3.start()
    if size >= 14:
        pump4.start()
    
def pumpFunc(motor_pin, speed):
  global pumping  #create global
  pumping = True
    
  while pumping:
    if pumping == False:
      break
    else:
      delay = (100-speed)/40000
      GPIO.output(motor_pin, GPIO.HIGH)
      time.sleep(delay)
      GPIO.output(motor_pin, GPIO.LOW)
      time.sleep(delay)

def stopPumping():
  global pumping
  pumping = False

#**************************************CLEAN AND PRIME**************************************

# Function to clean
def clean():
    print("Cleaning\n")

# Function to prime
def prime():
        print("Priming\n")

#**************************************SETTINGS WINDOW**************************************

# Functions for setting pump speeds based on sauce amount
def setSpeed():
    global s1_speed, s2_speed, s3_speed, s4_speed, amount
    s1_speed = amount
    s2_speed = amount
    s3_speed = amount
    s4_speed = amount

def setColor(color):
    fourteenButton["bg"] = color
    twelveButton["bg"] = color
    tenButton["bg"] = color
    sevenButton["bg"] = color

def setAmount(amt):
    global amount
    if amt == amount or amt == "normal":
        amount = med
        setColor("lime green")
    elif amt == "light":
        amount = lt
        setColor("orange")
    elif amt == "extra":
        amount = ext
        setColor("DarkOrange1")
    setSpeed()

# Function for actual settings window
def settings():
    # Create window for settings
    top = Toplevel()
    top.title("Saucer Settings")
    top.geometry('800x480')
    top.configure(bg="gray30")
    top.overrideredirect(1)
    
    # Font
    otherFont = font.Font(family='Helvetica', size=35, weight='normal')

    # Sauce amount buttons
    light  = Button(top, text = "LIGHT", font = otherFont, bg = "gray40", fg = "white", command = lambda: setAmount("light"), height = 2, width = 7)
    light.place(x=30, y=30)
    normal  = Button(top, text = "NORMAL", font = otherFont, bg = "gray40", fg = "white", command = lambda: setAmount("normal"), height = 2, width = 7)
    normal.place(x=290, y=30)
    extra  = Button(top, text = "EXTRA", font = otherFont, bg = "gray40", fg = "white", command = lambda: setAmount("extra"), height = 2, width = 7)
    extra.place(x=560, y=30)
    
    # Action buttons
    quit  = Button(top, text = "QUIT", font = otherFont, bg = "gray40", fg = "white", command = screen.destroy, height = 2, width = 6)
    quit.place(x=75, y=310)
    back  = Button(top, text = "BACK", font = otherFont, bg = "gray40", fg = "white", command = top.destroy, height = 2, width = 6)
    back.place(x=550, y=310)

#*****************************************HELP MENU*****************************************

# Function for changing button text based on answer
def change(button):
    if button['text'] == "NO":
        button['text'] = "YES"
    else:
        button['text'] = "NO"

# Function for sending sos menu data to Firebase
def send(answers):
    str = "Answers:"
    for button in answers:
        str = str + " " + button['text']
    if(hasInternet):
      db.push(str)
    print(str)
    print("Sending data to Firebase")

# Function for sos menu
def sos():
    # Create window for help menu
    sosMenu = Toplevel()
    sosMenu.title("Saucer Help Menu")
    sosMenu.geometry('800x480')
    sosMenu.configure(bg="gray30")
    sosMenu.overrideredirect(1)
    
    # Fonts
    otherFont = font.Font(family='Helvetica', size=35, weight='normal')
    questionFont = font.Font(family='Helvetica', size=14, weight='normal')
    
    # Questions
    q1 = Text(sosMenu, font=questionFont, height=1, width=35)
    q1.insert(INSERT, "Is it saucing the 14 Inch Pizza?")
    q1.place(x=25, y=20)
    
    b1  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b1), height = 1, width = 2)
    b1.place(x=400, y=20)
    
    q2 = Text(sosMenu, font=questionFont, height=1, width=35)
    q2.insert(INSERT, "Is it saucing the 12 Inch Pizza?")
    q2.place(x=25, y=60)
    
    b2  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b2), height = 1, width = 2)
    b2.place(x=400, y=60)
    
    q3 = Text(sosMenu, font=questionFont, height=1, width=35)
    q3.insert(INSERT, "Is it saucing the 10 Inch Pizza?")
    q3.place(x=25, y=100)
    
    b3 = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b3), height = 1, width = 2)
    b3.place(x=400, y=100)
    
    q4 = Text(sosMenu, font=questionFont, height=1, width=35)
    q4.insert(INSERT, "Is it saucing the 7 Inch Pizza?")
    q4.place(x=25, y=140)
    
    b4  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b4), height = 1, width = 2)
    b4.place(x=400, y=140)
    
    q5 = Text(sosMenu, font=questionFont, height=1, width=35)
    q5.insert(INSERT, "Do intake tubes have air bubbles?")
    q5.place(x=25, y=180)
    
    b5  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b5), height = 1, width = 2)
    b5.place(x=400, y=180)
    
    q6 = Text(sosMenu, font=questionFont, height=1, width=35)
    q6.insert(INSERT, "Is the turntable motor shaft spinning?")
    q6.place(x=25, y=220)
    
    b6  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b6), height = 1, width = 2)
    b6.place(x=400, y=220)
    
    q7 = Text(sosMenu, font=questionFont, height=1, width=35)
    q7.insert(INSERT, "Is the screen functioning properly?")
    q7.place(x=25, y=260)
    
    b7  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b7), height = 1, width = 2)
    b7.place(x=400, y=260)
    
    q8 = Text(sosMenu, font=questionFont, height=1, width=35)
    q8.insert(INSERT, "Can you hear any grinding noise?")
    q8.place(x=25, y=300)
    
    b8  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b8), height = 1, width = 2)
    b8.place(x=400, y=300)
    
    q9 = Text(sosMenu, font=questionFont, height=1, width=35)
    q9.insert(INSERT, "Can you hear any high pitched noise?")
    q9.place(x=25, y=340)
    
    b9  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b9), height = 1, width = 2)
    b9.place(x=400, y=340)
    
    q10 = Text(sosMenu, font=questionFont, height=1, width=35)
    q10.insert(INSERT, "Did this problem just start?")
    q10.place(x=25, y=380)
    
    b10  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b10), height = 1, width = 2)
    b10.place(x=400, y=380)
    
    answers = [b1,b2,b3,b4,b5,b6,b7,b8,b9,b10]
    
    # Back button
    done  = Button(sosMenu, text = "DONE", font = otherFont, bg = "gray40", fg = "white", command = lambda: send(answers), height = 2, width = 4)
    done.place(x=500, y=350)
    back  = Button(sosMenu, text = "BACK", font = otherFont, bg = "gray40", fg = "white", command = sosMenu.destroy, height = 2, width = 4)
    back.place(x=650, y=350)

    print("SOS\n")

# Function for help menu
def help():
    # Create window for help menu
    top = Toplevel()
    top.title("Saucer Help Menu")
    top.geometry('800x480')
    top.configure(bg="gray30")
    top.overrideredirect(1)
    
    # Font
    otherFont = font.Font(family='Helvetica', size=40, weight='normal')
    
    # Text
    txt = Text(top, font = otherFont, height=1, width=22)
    txt.insert(INSERT, "Welcome to the help menu!")
    txt.place(x=25,y=25)
    
    # Action buttons
    sosButton  = Button(top, text = "SOS", font = otherFont, bg = "gray40", fg = "white", command = sos, height = 2, width = 6)
    sosButton.place(x=100, y=320)
    back  = Button(top, text = "BACK", font = otherFont, bg = "gray40", fg = "white", command = top.destroy, height = 2, width = 6)
    back.place(x=510, y=320)

#***********************************OTHER SCREEN SET UP*************************************

def moreScreen():
    # Create window for more menu
    other = Toplevel()
    other.title("More Buttons")
    other.geometry('800x480')
    other.configure(bg="gray30")
    other.overrideredirect(1)
    
    # Fonts for screen
    otherFont = font.Font(family='Helvetica', size=35, weight='normal')
    
    # Other screen buttons
    settingsButton  = Button(other, text = "SETTINGS", font = otherFont, bg = "gray40", fg = "white", command = settings, height = 1, width = 8)
    settingsButton.place(x=20, y=350)

    helpButton  = Button(other, text = "HELP", font = otherFont, bg = "gray40", fg = "white", command = help, height = 1, width = 8)
    helpButton.place(x=280, y=350)
    back  = Button(other, text = "BACK", font = otherFont, bg = "gray40", fg = "white", command = other.destroy, height = 1, width = 8)
    back.place(x=550, y=350)

#**************************************TKINTER SET UP***************************************

# TK screen set up
screen = Tk()
screen.overrideredirect(1)
screen.geometry('800x480')
screen.configure(bg="gray30")
screen.title("Sm^rt Saucer")

# Fonts for screen
sizeFont = font.Font(family='Helvetica', size=64, weight='bold')
stopFont = font.Font(family='Helvetica', size=50, weight='bold')
otherFont = font.Font(family='Helvetica', size=40, weight='normal')

# Size buttons
fourteenButton  = Button(screen, text = "14\"", font = sizeFont, bg = "lime green", fg = "white", command = lambda: setSize(14), height = 1 , width = 3)
fourteenButton.place(x=610, y=25)

twelveButton  = Button(screen, text = "12\"", font = sizeFont, bg = "lime green", fg = "white", command = lambda: setSize(12), height = 1 , width = 3)
twelveButton.place(x=415, y=25)

tenButton  = Button(screen, text = "10\"", font = sizeFont, bg = "lime green", fg = "white", command = lambda: setSize(10), height = 1 , width = 3)
tenButton.place(x=220, y=25)

sevenButton  = Button(screen, text = "7\"", font = sizeFont, bg = "lime green", fg = "white", command = lambda: setSize(7), height = 1 , width = 3)
sevenButton.place(x=25, y=25)

# Donatos Image
path = "Saucer/donatoswhite.png"
img = ImageTk.PhotoImage(Image.open(path).resize((120,50), Image.ANTIALIAS))
logo = Label(screen, image = img, bg="gray30")
logo.place(x=15, y=210)

# Function button
stopButton  = Button(screen, text = "STOP", font = stopFont, bg = "red", fg = "white", command = stopPumping, height = 1, width = 11)
stopButton.place(x=170, y=190)

cleanButton  = Button(screen, text = "CLEAN", font = otherFont, bg = "gray40", fg = "white", command = clean, height = 2, width = 6)
cleanButton.place(x=25, y=320)

primeButton  = Button(screen, text = "PRIME", font = otherFont, bg = "gray40", fg = "white", command = prime, height = 2, width = 6)
primeButton.place(x=295, y=320)

moreButton  = Button(screen, text = "...", font = otherFont, bg = "gray40", fg = "white", command = moreScreen, height = 2, width = 6)
moreButton.place(x=565, y=320)

mainloop()
