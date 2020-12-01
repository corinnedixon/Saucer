from tkinter import *
import tkinter.font as font
import RPi.GPIO as GPIO
import time
import sys
import datetime
import threading
import screens

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
settingsButton  = Button(screen, text = "Settings", font = myFont, bg = "grey", command = lambda: screens.settings(screen), height = 1, width = 4)
settingsButton.place(x=50, y=300)

helpButton  = Button(screen, text = "Help", font = myFont, bg = "grey", command = lambda: screens.help(screen), height = 1, width = 4)
helpButton.place(x=500, y=300)

mainloop()
