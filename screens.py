from tkinter import *
import tkinter.font as font

#*************************************HELPER FUNCTIONS**************************************

def sos():
    # Fonts
    answerFont = font.Font(family='Helvetica', size=30, weight='normal')
    questionFont = font.Font(family='Helvetica', size=20, weight='normal')
    
    # Questions
    q1 = Text(top, font=questionFont, height=1, width=10)
    q1.insert(INSERT, "Is it saucing the 14 Inch Pizza?")
    q1.place(x=25, y=20)
    
    q2 = Text(top, font=questionFont, height=1, width=10)
    q2.insert(INSERT, "Is it saucing the 12 Inch Pizza?")
    q2.place(x=25, y=60)
    
    q3 = Text(top, font=questionFont, height=1, width=10)
    q3.insert(INSERT, "Is it saucing the 10 Inch Pizza?")
    q3.place(x=25, y=100)
    
    q4 = Text(top, font=questionFont, height=1, width=10)
    q4.insert(INSERT, "Is it saucing the 7 Inch Pizza?")
    q4.place(x=25, y=140)
    
    q5 = Text(top, font=questionFont, height=1, width=10)
    q5.insert(INSERT, "Do intake tubes have air bubbles?")
    q5.place(x=25, y=180)
    
    q6 = Text(top, font=questionFont, height=1, width=10)
    q6.insert(INSERT, "Is the turntable motor shaft spinning?")
    q6.place(x=25, y=220)
    
    q7 = Text(top, font=questionFont, height=1, width=10)
    q7.insert(INSERT, "Is it saucing the 14 Inch Pizza?")
    q7.place(x=25, y=260)
    
    q5 = Text(top, font=questionFont, height=1, width=10)
    q5.insert(INSERT, "Do intake tubes have air bubbles?")
    q5.place(x=25, y=300)
    
    q6 = Text(top, font=questionFont, height=1, width=10)
    q6.insert(INSERT, "Is the turntable motor shaft spinning?")
    q6.place(x=25, y=340)
    
    q7 = Text(top, font=questionFont, height=1, width=10)
    q7.insert(INSERT, "Is the screen functioning properly?")
    q7.place(x=25, y=380)
    
    q8 = Text(top, font=questionFont, height=1, width=10)
    q8.insert(INSERT, "Can you hear any grinding noise?")
    q8.place(x=25, y=420)
    
    q9 = Text(top, font=questionFont, height=1, width=10)
    q9.insert(INSERT, "Can you hear any high pitched noise?")
    q9.place(x=25, y=460)
    
    q10 = Text(top, font=questionFont, height=1, width=10)
    q10.insert(INSERT, "Did this problem just start?")
    q10.place(x=25, y=500)

    print("SOS\n")
    
    
def setAmount(amt):
    global s1_speed, s2_speed, s3_speed, s4_speed
    if amt == "light":
        s1_speed = 25
        s2_speed = 25
        s3_speed = 25
        s4_speed = 25
    elif amt == "normal":
        s1_speed = 50
        s2_speed = 50
        s3_speed = 50
        s4_speed = 50
    elif amt == "extra":
        s1_speed = 75
        s2_speed = 75
        s3_speed = 75
        s4_speed = 75

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
