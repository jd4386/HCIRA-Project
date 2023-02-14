# Importing required libraries
import math
import time
import recognizer
import tkinter as tk
from pprint import pprint


# Preprocessing the template unistrokes
Unistrokes = {key: recognizer.preprocess(value) for key, value in recognizer.Unistrokes.items()}

# Initialising the angle range and precision
angleRange = math.radians(45)
anglePrecision = math.radians(2)
halfDiagonal = 0.5 * recognizer.Diagonal

# Variable to store the user's unistroke
currentUnistroke = []

# Initialising the XY coordinates
presentX, presentY = 0, 0


# Function to capture the initial mouse coordinates
def getXY(event):
    canvas.delete("all")

    # Updating the initial mouse coordinates
    global presentX, presentY
    presentX, presentY = event.x, event.y

    # Adding the initial mouse coordinates to the user's unistroke
    global currentUnistroke
    currentUnistroke.append([presentX, presentY])

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
    global displayText
    displayText.set('Recording unistroke...')

    
# Function to draw a line from the initial points to the new mouse location and updates the points to the new mouse location
def drawLine(event):
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
    global currentUnistroke
    currentUnistroke.append([presentX, presentY])


# Function to recognize the unistroke
def recognize(event):
    global currentUnistroke, displayText

    # Printing the user's unistroke
    print('User\'s unistroke')
    pprint(currentUnistroke)
    print()

    # Checking if the user's unistroke is empty
    if len(currentUnistroke) <= 1:
        displayText.set('Too few points made. Please try again.')
        return

    # Starting the timer
    start_time = time.time()

    #recognize the unistroke
    global Unistrokes, angleRange, anglePrecision

    try:
        # Preprocessing the user's unistroke
        preProcessedCurrentUnistroke = recognizer.preprocess(currentUnistroke)
    except ZeroDivisionError:
        # If the user's unistroke is a straight line then the preprocessing will throw a ZeroDivisionError
        # Timer ends
        end_time = time.time()

        # Updating the display text
        displayText.set('Result: No match. (0) in ' + str(round((end_time - start_time) * 1000)) + ' ms.')
        
        # Resetting the user's unistroke
        currentUnistroke = []
        return

    # Initialising the best distance and unistroke
    u = None
    b = float('inf')

    # Looping through the template unistrokes
    for key in Unistrokes:
        # Calculating the distance between the user's unistroke and the template unistroke
        d = recognizer.distanceAtBestAngle(preProcessedCurrentUnistroke, Unistrokes[key], -angleRange, +angleRange, anglePrecision)

        # Updating the best distance and unistroke
        if d < b:
            b = d
            u = key

    # Timer ends
    end_time = time.time()

    # Checking if unistroke is found
    if u:
        # Updating the display text
        displayText.set('Result: ' + u.replace('_', ' ') + ' (' + str(round((1.0 - b / halfDiagonal), 2)) + ') in ' + str(round((end_time - start_time) * 1000)) + ' ms.')
    else:
        # Updating the display text
        displayText.set('Result: No match. (0) in ' + str(round((end_time - start_time) * 1000)) + ' ms.')

    # Resetting the user's unistroke
    currentUnistroke = []


# Function to reset the canvas
def clearCanvas():
    # Resetting the user's unistroke
    global currentUnistroke
    currentUnistroke = []

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
canvas.bind('<Button-1>', getXY)
canvas.bind('<B1-Motion>', drawLine)
canvas.bind('<ButtonRelease-1>', recognize)

# Clear button that resets the canvas
button = tk.Button(root, text='Clear', width=25, command=clearCanvas)
button.pack(pady=5)

# Code to keep the window running until closed
root.mainloop()