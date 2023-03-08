'''
Project Team Members:
1. Jagan Mohan Reddy Dwarampudi (UFID: 9357-2863)
2. Mohammad Shameer Mulla (UFID: 7066-4007)
'''

# Importing required libraries
import math
import time
import recognizer
import tkinter as tk
import testing
import export
import store

# Variable to control whether the GUI is displayed or not
guiFlag = True

# If guiFlag is False, run the testing function
if not guiFlag:
    testing.main()

# Preprocessing the template unistrokes
unistrokes = {key: recognizer.preprocess(value) for key, value in recognizer.Unistrokes.items()}

# Initialising the XY coordinates
presentX, presentY = 0, 0


# Function to capture the initial mouse coordinates
def getXY(event, canvas, displayText, displayTextFlag=True):
    canvas.delete("all")

    # Updating the initial mouse coordinates
    global presentX, presentY
    presentX, presentY = event.x, event.y

    # Adding the initial mouse coordinates to the user's unistroke
    store.updateCurrentUnistroke(presentX, presentY)

    # Drawing a box at the initial mouse coordinates
    box_len = 3
    canvas.create_rectangle(
        presentX - box_len,
        presentY - box_len,
        presentX + box_len,
        presentY + box_len,
        fill='#0000d8',
        outline=''
    )

    # Updating the display text
    if displayTextFlag:
        displayText.set('Recording unistroke...')

    
# Function to draw a line from the initial points to the new mouse location and updates the points to the new mouse location
def drawLine(event, canvas):
    global presentX, presentY

    # Drawing a line from the previous mouse coordinates to the new mouse coordinates
    canvas.create_line(
        (presentX, presentY, event.x, event.y),
        width=2,
        fill='#0000d8'
    )

    # Updating the previous mouse coordinates to the new mouse coordinates
    presentX, presentY = event.x, event.y

    # Adding the new mouse coordinates to the user's unistroke
    store.updateCurrentUnistroke(presentX, presentY)


# Function to recognize the unistroke
def recognize(event, displayText):

    # Checking if the user's unistroke is empty
    if len(store.currentUnistroke) <= 1:
        displayText.set('Too few points made. Please try again.')
        return

    # Starting the timer
    start_time = time.time()

    # Recognizing the user's unistroke
    u, b = recognizer.recognize(store.currentUnistroke, unistrokes)

    # Timer ends
    end_time = time.time()

    # Updating the display text
    displayText.set('Result: ' + u + ' (' + b + ') in ' + str(round((end_time - start_time) * 1000)) + ' ms.')

    # Resetting the user's unistroke
    store.resetCurrentUnistroke()


# Function to reset the canvas
def clearCanvas(canvas):
    # Resetting the user's unistroke
    store.resetCurrentUnistroke()

    # Resetting the drawing canvas
    canvas.delete("all")


# Tkinter initialisation
root = tk.Tk()
root.title('Canvas')
root.geometry('800x600')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Label initialisation inside the tkinter window
displayText = tk.StringVar()
display = tk.Label(
    root,
    textvariable=displayText,
    bg='#ffff98',
    fg='#0000d8',
    anchor='w'
)
display.pack(fill=tk.BOTH, padx=3)

# Canvas initialisation inside the tkinter window
canvas = tk.Canvas(root, bg='#dddddd')
canvas.pack(expand=True, fill=tk.BOTH)

# Attaching the left mouse click and mouse motion to the designated functions.
canvas.bind('<Button-1>', lambda event: getXY(event, canvas, displayText))
canvas.bind('<B1-Motion>', lambda event: drawLine(event, canvas))
canvas.bind('<ButtonRelease-1>', lambda event: recognize(event, displayText))

# Clear button that resets the canvas
button = tk.Button(root, text='Clear', width=25, command=lambda: clearCanvas(canvas))
button.pack(pady=5)

# Create dataset button that opens a new window
button = tk.Button(root, text='Create Dataset', width=25, command=lambda: export.datasetWindow(root, getXY, drawLine, clearCanvas))
button.pack(pady=5)

# Code to keep the window running until closed
# If guiFlag is False, the window will not be displayed
root.mainloop() if guiFlag else None