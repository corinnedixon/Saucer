from tkinter import *
import tkinter.font as font

#*************************************HELPER FUNCTIONS**************************************

def sos():
    print("SOS\n")

#**************************************SETTINGS WINDOW**************************************

def settings(screen):
    # Create window for settings
    top = Toplevel()
    top.title("Full Line Settings")
    top.geometry('800x480')
    screen.overrideredirect(0)
    top.overrideredirect(1)
    
    # Font
    subFont = font.Font(family='Helvetica', size=30, weight='normal')
    
    # Action buttons
    quit  = Button(top, text = "Quit", font = subFont, fg="black", bg = "white", command = screen.destroy, height = 2, width = 6)
    quit.place(x=100, y=350)
    back  = Button(top, text = "Back", font = subFont, fg="black", bg = "white", command = top.destroy, height = 2, width = 6)
    back.place(x=550, y=350)

#*****************************************HELP MENU*****************************************

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
    txt = Text(top, font = subFont, height=1, width=15)
    txt.insert(INSERT, "Welcome to the help menu!")
    txt.place(x=25,y=25)
    
    # Action buttons
    quit  = Button(top, text = "SOS", font = subFont, fg="black", bg = "white", command = sos, height = 2, width = 6)
    quit.place(x=100, y=350)
    back  = Button(top, text = "Back", font = subFont, fg="black", bg = "white", command = top.destroy, height = 2, width = 6)
    back.place(x=550, y=350)
