#!/usr/bin/env python3
#------------------------------------------------------------------------------
# liveFire.py -- draws a window allowing live aiming of bean laser turret (BLT)
#   okay, it's just a laser diode and 2 servos on a can of chili
#   left click to toggle aim mode
#------------------------------------------------------------------------------
import pyfirmata
import tkinter
from time import sleep

board = pyfirmata.Arduino('/dev/ttyACM0')
it = pyfirmata.util.Iterator(board)
it.start()

panServo = board.get_pin('d:9:s')
tiltServo = board.get_pin('d:6:s')

# Units based on servo range and multiplier for scaling.
UNITS = 180
MULT = 2

#boolean to track aim mode and helper function
isAiming = False
def toggleAim():
    global isAiming
    isAiming = not isAiming

# Pan and Tilt functions
def move_pan(a):
    panServo.write(a)
def move_tilt(a):
    tiltServo.write(a)

# default position of straight ahead
move_pan(UNITS/2)
move_tilt(UNITS/2)

# Left Mouse Event Handler
def leftClick(event):
    global checkAim
    x, y = event.x, event.y
    toggleAim()
    checkAim.toggle()

# Mouse Movement Event Handler
def motion(event):
    global isAiming
    global xEntry, yEntry


    # check for aim mode
    if (not isAiming):
        return

    # Get current X + Y values and display in entry boxes
    x, y = event.x, event.y
    xEntry.delete(0, tkinter.END)
    yEntry.delete(0, tkinter.END)
    xEntry.insert(0, round(event.x/MULT))
    yEntry.insert(0, round(180 - (event.y/MULT)))

    # Move servo and sleep 15ms for smoothing
    move_pan(UNITS-(x/MULT))
    move_tilt(UNITS-(y/MULT))
    sleep(0.15)

def textAim(event):
    global xEntry, yEntry
    xText = xEntry.get()
    yText = yEntry.get()
    print("X Text: {} - Y Text: {}".format(xText, yText))
    move_pan(180 - int(xText))
    move_tilt(int(yText))

# Init Tkinter Window w/ Title
top = tkinter.Tk()
top.title("Bean Laser Turret")
top.bind('<Return>', textAim)

# Value Frame on Left of Window
valueFrame = tkinter.Frame(top)
valueFrame.pack(side = tkinter.LEFT)

# X Value
xLabel = tkinter.Label(valueFrame, text="X Value: ")
xEntry = tkinter.Entry(valueFrame)
xLabel.pack()
xEntry.pack()

# Y Value
yLabel = tkinter.Label(valueFrame, text="Y Value: ")
yEntry = tkinter.Entry(valueFrame)
yLabel.pack()
yEntry.pack()

# Aim Button
aimButton = tkinter.Button(valueFrame, text="Aim", command=textAim)
aimButton.pack()

# checkButton
checkAim = tkinter.Checkbutton(top, text="Aim Mode", command=toggleAim)

# Aiming Frame
frame = tkinter.Frame(top, bg="red", cursor="cross", width=(UNITS*MULT), height=(UNITS*MULT))
frame.bind("<Button-1>", leftClick)

# Aim Loop
while True:
    if (isAiming):
        frame.bind("<Motion>", motion)
    else:
        frame.unbind("<Motion>")
    frame.pack()
    checkAim.pack()
    top.update_idletasks()
    top.update()
