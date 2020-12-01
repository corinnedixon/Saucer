from tkinter import *
import tkinter.font as font
import RPi.GPIO as GPIO
import time
import sys
import datetime
import threading

#***********************************VARIABLE DECLARATIONS***********************************

# Motor speed
global s1_speed, s2_speed, s3_speed, s4_speed
s1_speed = 50 # Sauce stepper motor 1 speed (default 50)
s2_speed = 50 # Sauce stepper motor 2 speed
s3_speed = 50 # Sauce stepper motor 3 speed
s4_speed = 50 # Sauce stepper motor 4 speed

# Size / Steps
global size
size = -1 # No default size
global sauce_spin_steps
sauce_spin_steps = 1000

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
    print("RUNNING SAUCE\n")

    # Run corresponding saucer pumps
    pumpProgram()
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
def pumpProgram():
    # Create new threads
    pump1 = threading.Thread(target=pumpFunc, args = (S1_STEP, s1_speed,))
    pump2 = threading.Thread(target=pumpFunc, args = (S2_STEP, s2_speed,))
    pump3 = threading.Thread(target=pumpFunc, args = (S3_STEP, s3_speed,))
    pump4 = threading.Thread(target=pumpFunc, args = (S4_STEP, s4_speed,))
    
    # Start new thread
    pump1.start()
    pump2.start()
    pump3.start()
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

#**************************************SETTINGS WINDOW**************************************

# Functions for setting pump speeds based on sauce amount
def setSpeed(new_speed):
    global s1_speed, s2_speed, s3_speed, s4_speed
    s1_speed = new_speed
    s2_speed = new_speed
    s3_speed = new_speed
    s4_speed = new_speed

def setAmount(amt):
    if amt == "light":
        setSpeed(25)
    elif amt == "normal":
        setSpeed(50)
    elif amt == "extra":
        setSpeed(75)

# Function for actual settings window
def settings(screen):
    # Create window for settings
    top = Toplevel()
    top.title("Full Line Settings")
    top.geometry('800x480')
    screen.overrideredirect(0)
    top.overrideredirect(1)
    
    # Font
    subFont = font.Font(family='Helvetica', size=30, weight='normal')
    
    # Sauce amount buttons
    light  = Button(top, text = "Light", font = subFont, fg="black", bg = "white", command = lambda: setAmount("light"), height = 2, width = 6)
    light.place(x=50, y=100)
    normal  = Button(top, text = "Normal", font = subFont, fg="black", bg = "white", command = lambda: setAmount("normal"), height = 2, width = 6)
    normal.place(x=300, y=100)
    extra  = Button(top, text = "Extra", font = subFont, fg="black", bg = "white", command = lambda: setAmount("extra"), height = 2, width = 6)
    extra.place(x=550, y=100)
    
    # Action buttons
    quit  = Button(top, text = "Quit", font = subFont, fg="black", bg = "white", command = screen.destroy, height = 2, width = 6)
    quit.place(x=100, y=350)
    back  = Button(top, text = "Back", font = subFont, fg="black", bg = "white", command = top.destroy, height = 2, width = 6)
    back.place(x=550, y=350)

#*****************************************HELP MENU*****************************************

# Function for sos menu
def sos(top):
    # Create window for help menu
    sosMenu = Toplevel()
    sosMenu.title("Full Line Help Menu")
    sosMenu.geometry('800x480')
    top.overrideredirect(0)
    sosMenu.overrideredirect(1)
    
    # Fonts
    subFont = font.Font(family='Helvetica', size=30, weight='normal')
    answerFont = font.Font(family='Helvetica', size=30, weight='normal')
    questionFont = font.Font(family='Helvetica', size=14, weight='normal')
    
    # Questions
    q1 = Text(sosMenu, font=questionFont, height=1, width=60)
    q1.insert(INSERT, "Is it saucing the 14 Inch Pizza?")
    q1.place(x=25, y=20)
    
    q2 = Text(sosMenu, font=questionFont, height=1, width=60)
    q2.insert(INSERT, "Is it saucing the 12 Inch Pizza?")
    q2.place(x=25, y=50)
    
    q3 = Text(sosMenu, font=questionFont, height=1, width=60)
    q3.insert(INSERT, "Is it saucing the 10 Inch Pizza?")
    q3.place(x=25, y=80)
    
    q4 = Text(sosMenu, font=questionFont, height=1, width=60)
    q4.insert(INSERT, "Is it saucing the 7 Inch Pizza?")
    q4.place(x=25, y=110)
    
    q5 = Text(sosMenu, font=questionFont, height=1, width=60)
    q5.insert(INSERT, "Do intake tubes have air bubbles?")
    q5.place(x=25, y=140)
    
    q6 = Text(sosMenu, font=questionFont, height=1, width=60)
    q6.insert(INSERT, "Is the turntable motor shaft spinning?")
    q6.place(x=25, y=170)
    
    q7 = Text(sosMenu, font=questionFont, height=1, width=60)
    q7.insert(INSERT, "Is it saucing the 14 Inch Pizza?")
    q7.place(x=25, y=200)
    
    q5 = Text(sosMenu, font=questionFont, height=1, width=60)
    q5.insert(INSERT, "Do intake tubes have air bubbles?")
    q5.place(x=25, y=230)
    
    q8 = Text(sosMenu, font=questionFont, height=1, width=60)
    q8.insert(INSERT, "Is the turntable motor shaft spinning?")
    q8.place(x=25, y=260)
    
    q9 = Text(sosMenu, font=questionFont, height=1, width=60)
    q9.insert(INSERT, "Is the screen functioning properly?")
    q9.place(x=25, y=290)
    
    q10 = Text(sosMenu, font=questionFont, height=1, width=60)
    q10.insert(INSERT, "Can you hear any grinding noise?")
    q10.place(x=25, y=320)
    
    q11 = Text(sosMenu, font=questionFont, height=1, width=60)
    q11.insert(INSERT, "Can you hear any high pitched noise?")
    q11.place(x=25, y=350)
    
    q12 = Text(sosMenu, font=questionFont, height=1, width=60)
    q12.insert(INSERT, "Did this problem just start?")
    q12.place(x=25, y=380)
    
    # Back button
    back  = Button(sosMenu, text = "Back", font = subFont, fg="black", bg = "white", command = sosMenu.destroy, height = 2, width = 6)
    back.place(x=550, y=350)

    print("SOS\n")

# Function for help menu
def help(screen):
    # Create window for help menu
    top = Toplevel()
    top.title("Full Line Help Menu")
    top.geometry('800x480')
    screen.overrideredirect(0)
    top.overrideredirect(1)
    
    # Font
    subFont = font.Font(family='Helvetica', size=30, weight='normal')
    
    # Text
    txt = Text(top, font = subFont, height=1, width=20)
    txt.insert(INSERT, "Welcome to the help menu!")
    txt.place(x=25,y=25)
    
    # Action buttons
    quit  = Button(top, text = "SOS", font = subFont, fg="black", bg = "white", command = lambda: sos(top), height = 2, width = 6)
    quit.place(x=100, y=350)
    back  = Button(top, text = "Back", font = subFont, fg="black", bg = "white", command = top.destroy, height = 2, width = 6)
    back.place(x=550, y=350)
    
#**************************************TKINTER SET UP***************************************

# TK screen set up
screen = Tk()
screen.overrideredirect(1)
screen.geometry('800x480')
screen.title("Sm^rt Saucer")

# Fonts for screen
myFont = font.Font(family='Helvetica', size=36, weight='bold')
myFontLarge = font.Font(family='Helvetica', size=50, weight='bold')

# Size buttons
fourteenButton  = Button(screen, text = "14 in.", font = myFont, bg = "white", command = lambda: setSize(14), height = 2 , width = 4)
fourteenButton.place(x=575, y=5)

twelveButton  = Button(screen, text = "12 in.", font = myFont, bg = "white", command = lambda: setSize(12), height = 2 , width = 4)
twelveButton.place(x=400, y=5)

tenButton  = Button(screen, text = "10 in.", font = myFont, bg = "white", command = lambda: setSize(10), height = 2 , width = 4)
tenButton.place(x=225, y=5)

sevenButton  = Button(screen, text = "7 in.", font = myFont, bg = "white", command = lambda: setSize(7), height = 2 , width = 4)
sevenButton.place(x=50, y=5)

# Function buttons
stopButton  = Button(screen, text = "STOP", font = myFontLarge, bg = "red", command = stopPumping, height = 2, width = 6)
stopButton.place(x=300, y=160)

# Other screen buttons
settingsButton  = Button(screen, text = "Settings", font = myFont, bg = "grey", command = lambda: settings(screen), height = 1, width = 4)
settingsButton.place(x=50, y=380)

helpButton  = Button(screen, text = "Help", font = myFont, bg = "grey", command = lambda: help(screen), height = 1, width = 4)
helpButton.place(x=500, y=380)

mainloop()
