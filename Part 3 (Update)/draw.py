# Importing required libraries
import math
import time
import recognizer
import tkinter as tk
import testing

# Variable to control whether the GUI is displayed or not
guiFlag = False

# If guiFlag is False, run the testing function
if not guiFlag:
    testing.main()

# Preprocessing the template unistrokes
unistrokes = {key: recognizer.preprocess(value) for key, value in recognizer.Unistrokes.items()}

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

    # Checking if the user's unistroke is empty
    if len(currentUnistroke) <= 1:
        displayText.set('Too few points made. Please try again.')
        return

    # Starting the timer
    start_time = time.time()

    u, b = recognizer.recognize(currentUnistroke, unistrokes)

    # Timer ends
    end_time = time.time()

    # Updating the display text
    displayText.set('Result: ' + u + ' (' + b + ') in ' + str(round((end_time - start_time) * 1000)) + ' ms.')

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
# If guiFlag is False, the window will not be displayed
root.mainloop() if guiFlag else None