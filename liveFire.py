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
MULT = 3

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

# Event Handlers
def leftClick(event):
    x, y = event.x, event.y
    toggleAim()
    print("Clicked at: {}, {} - isAiming: {}".format(x,y,isAiming))


def motion(event):
    x, y = event.x, event.y
    print("Aiming: {}, {}".format(x,y))
    move_pan(UNITS-(x/MULT))
    move_tilt(UNITS-(y/MULT))

# Display aim window
top = tkinter.Tk()
frame = tkinter.Frame(top, width=(UNITS*MULT), height=(UNITS*MULT))
frame.bind("<Button-1>", leftClick)

# Aim Loop
while True:
    if (isAiming):
        frame.bind("<Motion>", motion)
    else:
        frame.unbind("<Motion>")
    frame.pack()
    top.update_idletasks()
    top.update()
    sleep(0.15)
