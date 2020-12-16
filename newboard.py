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

import serial

#*************************************START CONNECTION**************************************

# Open UART serial connection
ser = serial.Serial("/dev/ttyS0", 115200)  # opens port with baud rate

#**************************************FIREBASE SET UP**************************************

#Check for internet connection
#def checkInternet():
#  internet = True
#  try:
#    urllib.request.urlopen('https://smart-saucer.firebaseio.com/')
#  except:
#    internet = False
#  return internet
#
#time.sleep(1)
#hasInternet = checkInternet()
#
##Set timezone
#os.environ['TZ'] = 'US/Eastern'
#time.tzset()
#
##pyfire set up if internet is connected
#if(hasInternet):
#  config = {
#    "apiKey" : "AIzaSyBq-3aOFMlc-9IcSV-X2ZvrIceH5Uvz-U4",
#    "authDomain" : "smart-saucer.firebaseapp.com",
#    "databaseURL" : "https://smart-saucer.firebaseio.com/",
#    "storageBucket" : "smart-saucer.appspot.com"
#  }
#
#  firebase = pyfireconnect.initialize(config)
#  db = firebase.database()

#***********************************VARIABLE DECLARATIONS***********************************

# Light, normal, extra sauce speeds
lt = 40000
med = 50000
ext = 60000

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
    if click >= 1:
        click = 0
        runSaucer()
        size = -1

#************************************SAUCER FUNCTIONS***************************************

#Function for running saucer
def runSaucer():
    print("SPEED: " + str(s1_speed))
    print("SIZE: " + str(size))
    print("RUNNING SAUCE")

    # Run corresponding saucer pumps
    global sauce_spin_steps
    pumpProgram(size)
    spinFunc()
    time.sleep(3)
    stopPumping()
    stopSpinning()

#Functions for starting and stopping spin
def spinFunc():
  spin = "$STEPPER_START,TURNTABLE,FORWARD,30000,0\r\n"
  ser.write(spin.encode())

def stopSpinning():
  stop = "$STEPPER_STOP,TURNTABLE\r\n"
  ser.write(stop.encode())

#Functions for starting and stopping sauce
def pumpProgram(size):
    # Start pumping infinitely based on size
    start1 = "$STEPPER_START,PUMP1,FORWARD," + str(s1_speed) + ",0\r\n"
    ser.write(start1.encode())
    if size >= 10:
        start2 = "$STEPPER_START,PUMP2,FORWARD," + str(s2_speed) + ",0\r\n"
        ser.write(start2.encode())
    if size >= 12:
        start3 = "$STEPPER_START,PUMP3,FORWARD," + str(s3_speed) + ",0\r\n"
        ser.write(start3.encode())
    if size >= 14:
        start4 = "$STEPPER_START,PUMP4,FORWARD," + str(s4_speed) + ",0\r\n"
        ser.write(start4.encode())

def stopPumping():
  global pumping
  pumping = False
  stop1 = "$STEPPER_STOP,PUMP1\r\n"
  ser.write(stop1.encode())
  stop2 = "$STEPPER_STOP,PUMP2\r\n"
  ser.write(stop2.encode())
  stop3 = "$STEPPER_STOP,PUMP3\r\n"
  ser.write(stop3.encode())
  stop4 = "$STEPPER_STOP,PUMP4\r\n"
  ser.write(stop4.encode())

#**************************************CLEAN AND PRIME**************************************

# Function to clean
def clean():
    print("Cleaning\n")

# Function to prime
def prime():
        print("Priming\n")

#*************************************CHANGE SAUCE AMT**************************************

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
    if amt == amount or amt == med:
        amount = med
        setColor("lime green")
        extra["bg"] = "gray20"
        light["bg"] = "gray20"
    elif amt == lt:
        amount = lt
        setColor("orange")
        light["bg"] = "orange"
        extra["bg"] = "gray20"
    elif amt == ext:
        amount = ext
        setColor("DarkOrange2")
        extra["bg"] = "DarkOrange2"
        light["bg"] = "gray20"
    setSpeed()

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
    sosMenu.configure(bg="gray20")
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
    done  = Button(sosMenu, text = "DONE", font = otherFont, bg = "gray20", fg = "white", command = lambda: send(answers), height = 2, width = 4)
    done.place(x=500, y=350)
    back  = Button(sosMenu, text = "BACK", font = otherFont, bg = "gray20", fg = "white", command = sosMenu.destroy, height = 2, width = 4)
    back.place(x=650, y=350)

    print("SOS\n")

#***********************************OTHER SCREEN SET UP*************************************

def moreScreen():
    # Create window for more menu
    other = Toplevel()
    other.title("More Buttons")
    other.geometry('800x480')
    other.configure(bg="gray20")
    other.overrideredirect(1)
    
    # Fonts for screen
    stopFont = font.Font(family='Helvetica', size=50, weight='bold')
    otherFont = font.Font(family='Helvetica', size=24, weight='normal')
    headingFont = font.Font(family='Helvetica', size=20, weight='normal')
    
    # Other screen buttons
    helpButton  = Button(other, text = "HELP", font = stopFont, bg = "red2", fg = "white", command = sos, height = 1, width = 8)
    helpButton.place(x=460, y=20)
    home  = Button(other, text = "HOME", font = otherFont, bg = "gray20", fg = "white", command = other.destroy, height = 2, width = 10)
    home.place(x=575, y=380)
    
    #TEMPORARY QUIT
    quitButton  = Button(other, text = "QUIT", font = otherFont, bg = "gray20", fg = "white", command = screen.destroy, height = 2, width = 10)
    quitButton.place(x=200, y=200)
    
    # Text on screen
    calib = Text(other, font = headingFont, bd = -2, bg = "gray20", fg = "white", height=1, width=27)
    calib.insert(INSERT, "SAUCE WEIGHT CALIBRATION")
    calib.place(x=10,y=10)
    
    diag = Text(other, font = headingFont, bd = -2, bg = "gray20", fg = "white", height=1, width=21)
    diag.insert(INSERT, "MACHINE DIAGNOSTICS")
    diag.place(x=460,y=125)

#**************************************TKINTER SET UP***************************************

# TK screen set up
screen = Tk()
screen.overrideredirect(1)
screen.geometry('800x480')
screen.configure(bg="gray20")
screen.title("Sm^rt Saucer")

# Fonts for screen
sizeFont = font.Font(family='Helvetica', size=60, weight='bold')
stopFont = font.Font(family='Helvetica', size=50, weight='bold')
otherFont = font.Font(family='Helvetica', size=24, weight='normal')

# Size buttons
fourteenButton  = Button(screen, text = "14\"", font = sizeFont, bg = "lime green", fg = "white", command = lambda: setSize(14), height = 2 , width = 3)
fourteenButton.place(x=615, y=25)

twelveButton  = Button(screen, text = "12\"", font = sizeFont, bg = "lime green", fg = "white", command = lambda: setSize(12), height = 2 , width = 3)
twelveButton.place(x=415, y=25)

tenButton  = Button(screen, text = "10\"", font = sizeFont, bg = "lime green", fg = "white", command = lambda: setSize(10), height = 2 , width = 3)
tenButton.place(x=215, y=25)

sevenButton  = Button(screen, text = "7\"", font = sizeFont, bg = "lime green", fg = "white", command = lambda: setSize(7), height = 2 , width = 3)
sevenButton.place(x=15, y=25)

# Donatos Image
path = "Saucer/donatoswhite.png"
img = ImageTk.PhotoImage(Image.open(path).resize((114,38), Image.ANTIALIAS))
logo = Label(screen, image = img, bg="gray20")
logo.place(x=45, y=275)

# Function button
stopButton  = Button(screen, text = "STOP", font = stopFont, bg = "red2", fg = "white", command = stopPumping, height = 1, width = 9)
stopButton.place(x=215, y=255)

moreButton  = Button(screen, text = "...", font = stopFont, bg = "gray20", fg = "white", command = moreScreen, height = 1, width = 3)
moreButton.place(x=625, y=255)

cleanButton  = Button(screen, text = "CLEAN", font = otherFont, bg = "gray20", fg = "white", command = clean, height = 2, width = 10)
cleanButton.place(x=15, y=380)

primeButton  = Button(screen, text = "PRIME", font = otherFont, bg = "gray20", fg = "white", command = prime, height = 2, width = 10)
primeButton.place(x=575, y=380)

extra  = Button(screen, text = "EXTRA\nSAUCE", font = otherFont, bg = "gray20", fg = "white", command = lambda: setAmount(ext), height = 2, width = 5)
extra.place(x=260, y=380)

light  = Button(screen, text = "LESS\nSAUCE", font = otherFont, bg = "gray20", fg = "white", command = lambda: setAmount(lt), height = 2, width = 5)
light.place(x=420, y=380)

mainloop()
