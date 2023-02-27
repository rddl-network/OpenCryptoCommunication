# Import module
from tkinter import *

import serial
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()


# Create object
root = Tk()

# Adjust size
root.geometry( "400x200" )

# Change the label text
def show():
    label.config( text = clicked.get() )
    root.destroy()

# Dropdown menu options
options = []
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))
    options.append(port)

# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set( options[0] )

# Create Dropdown menu
drop = OptionMenu( root , clicked , *options )
drop.pack()

# Create button, it will change label text
button = Button( root , text = "Connect" , command = show ).pack()

# Create Label
label = Label( root , text = " " )
label.pack()

# Execute tkinter
root.mainloop()
