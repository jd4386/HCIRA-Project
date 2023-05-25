'''
Project Team Members:
1. Jagan Mohan Reddy Dwarampudi (UFID: 9357-2863)
2. Mohammad Shameer Mulla (UFID: 7066-4007)
'''

# Skeleton code similar to code from Project 1

# Importing the required libraries
import tkinter as tk
import store
import ndollarrecognizer
from icecream import ic

def nDollarWindow(root, getXY, drawLine):
    store.resetCurrentMultistroke()
    store.multistrokeFlag = True

    # Creating a new window
    nDollarWindow = tk.Toplevel(root)
    nDollarWindow.title('Multistroke Recognizer')
    nDollarWindow.geometry('800x600')
    nDollarWindow.rowconfigure(0, weight=1)

    # Label to display the multistroke
    displayText = tk.StringVar()
    display = tk.Label(
        nDollarWindow,
        textvariable=displayText,
        bg='#ffff98',
        fg='#0000d8',
        anchor='w'
    )
    display.pack(fill=tk.BOTH, padx=3)

    # Canvas to draw the multistroke
    canvas = tk.Canvas(nDollarWindow, bg='#dddddd')
    canvas.pack(expand=True, fill=tk.BOTH)

    # Bind mouse events to the canvas
    canvas.bind('<Button-1>', lambda event: getXY(event, canvas, displayText))
    canvas.bind('<B1-Motion>', lambda event: drawLine(event, canvas))
    canvas.bind('<ButtonRelease-1>', lambda event: release(event, displayText))

    useBoundedRotationInvariance = tk.BooleanVar()
    useBoundedRotationInvariance.set(False)
    boundedRotationInvariance = tk.Checkbutton(
        nDollarWindow,
        text='Use Bounded Rotation Invariance',
        variable=useBoundedRotationInvariance,
        onvalue=True,
        offvalue=False
    )
    boundedRotationInvariance.pack(pady=5)

    requireSameNoOfStrokes = tk.BooleanVar()
    requireSameNoOfStrokes.set(False)
    sameNoOfStrokes = tk.Checkbutton(
        nDollarWindow,
        text='Require same no. of strokes',
        variable=requireSameNoOfStrokes,
        onvalue=True,
        offvalue=False
    )
    sameNoOfStrokes.pack(pady=5)

    # Recognize button to recognize the multistroke
    recognizeButton = tk.Button(
        nDollarWindow,
        text='Recognize',
        width=25,
        command=lambda: recognize(displayText, useBoundedRotationInvariance.get(), requireSameNoOfStrokes.get())
    )
    recognizeButton.pack(pady=5)

    # Clear button to clear the canvas
    clear = tk.Button(
        nDollarWindow,
        text='Clear',
        width=25,
        command=lambda: clearCanvas(canvas, displayText)
    )
    clear.pack(pady=5)

    # Create dataset button to open the dataset window
    # createDataset = tk.Button(
    #     nDollarWindow,
    #     text='Create Dataset',
    #     width=25,
    #     command=lambda: export.datasetWindow(nDollarWindow, getXY, drawLine, clearCanvas)
    # )
    # createDataset.pack(pady=5)

    # Close button to close the window
    close = tk.Button(
        nDollarWindow,
        text='Close Window',
        width=25,
        command=lambda: closeWindow(nDollarWindow)
    )
    close.pack(pady=5)


def closeWindow(window):
    store.multistrokeFlag = False
    window.destroy()
    window.update()


def release(event, displayText=None):
    store.updateCurrentMultistroke()

    if displayText:
        displayText.set(f'Stroke #{len(store.currentMultistroke)} recorded.')


def clearCanvas(canvas, displayText=None):
    store.resetCurrentUnistroke()
    store.resetCurrentMultistroke()

    canvas.delete("all")

    if displayText:
        displayText.set('Canvas cleared.')


def recognize(displayText, useBoundedRotationInvariance, requireSameNoOfStrokes):
    result = ndollarrecognizer.recognize(store.currentMultistroke, useBoundedRotationInvariance, requireSameNoOfStrokes)
    displayText.set(f'Result: {result.name} ({round(result.score, 2)}) in {round(result.time * 100)} ms.')
    # displayText.set(f'Result: {store.TempGestures[store.counter % len(store.TempGestures)]} ({round(result.score, 2)}) in {round(result.time * 100)} ms.')
    # store.counter += 1

    store.resetCanvasFlag = True