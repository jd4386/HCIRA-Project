'''
Project Team Members:
1. Jagan Mohan Reddy Dwarampudi (UFID: 9357-2863)
2. Mohammad Shameer Mulla (UFID: 7066-4007)
'''

# Importing the required libraries
import os
import store
import tkinter as tk
import xml.dom.minidom
import xml.etree.ElementTree as ET


# Global variables
Gestures = [
    'triangle',
    'x',
    'rectangle',
    'circle',
    'check',
    'caret',
    'zig-zag',
    'arrow',
    'left_sq_bracket',
    'right_sq_bracket',
    'v',
    'delete_mark',
    'left_curly_brace',
    'right_curly_brace',
    'star',
    'pigtail',
]
DatasetPath = 'Part 5/custom_xml_logs'
CurrentGestureIndex = 0
MaxGestureIndex = len(Gestures)
CurrentSampleCount = 1
MaxSampleCount = 10
CurrentUser = ''


# New window to get user generated data
def datasetWindow(root, getXY, drawLine, clearCanvas):
    # Function to get user name
    initUser()

    # Creating a new window
    datasetWindow = tk.Toplevel(root)
    datasetWindow.title('Create Dataset')
    datasetWindow.geometry('800x600')
    datasetWindow.columnconfigure(0, weight=1)
    datasetWindow.rowconfigure(0, weight=1)

    # Label to display the gesture type
    gestureDisplayText = tk.StringVar()
    gestureDisplayText.set(f'gesture type: {Gestures[CurrentGestureIndex].replace("_", " ").upper()}')
    display = tk.Label(
        datasetWindow,
        textvariable=gestureDisplayText,
        bg='black',
        fg='white',
        anchor='w'
    )
    display.pack(fill=tk.BOTH, padx=3)

    # Label to display the sample count
    countDisplayText = tk.StringVar()
    countDisplayText.set(f'sample #: {CurrentSampleCount}')
    display = tk.Label(
        datasetWindow,
        textvariable=countDisplayText,
        bg='black',
        fg='white',
        anchor='w'
    )
    display.pack(fill=tk.BOTH, padx=3)

    # Canvas initialisation inside the tkinter window
    canvas = tk.Canvas(datasetWindow, bg='#dddddd')
    canvas.pack(expand=True, fill=tk.BOTH)

    # Attaching the left mouse click and mouse motion to the designated functions.
    canvas.bind('<Button-1>', lambda event: getXY(event, canvas, None, False))
    canvas.bind('<B1-Motion>', lambda event: drawLine(event, canvas))

    # Next button that saves the canvas points and moves on to the next gesture
    nextButtonText = tk.StringVar()
    nextButtonText.set(f'Next ({MaxGestureIndex - CurrentGestureIndex - 1} gestures remaining)')
    button = tk.Button(datasetWindow, textvariable=nextButtonText, width=25, command=lambda: nextGesture(
        datasetWindow,
        canvas,
        clearCanvas,
        gestureDisplayText,
        countDisplayText,
        nextButtonText
    ))
    button.pack(pady=5)

    # Clear button that resets the canvas
    button = tk.Button(datasetWindow, text='Clear', width=25, command=lambda: clearCanvas(canvas))
    button.pack(pady=5)

    # Close button that closes the window
    button = tk.Button(datasetWindow, text='Close Window', width=25, command=lambda: closeWindow(datasetWindow))
    button.pack(pady=5)


# Resetting the global variables
def reset():
    global CurrentGestureIndex, CurrentSampleCount

    CurrentGestureIndex = 0
    CurrentSampleCount = 1


# Closing the window
def closeWindow(datasetWindow):
    reset()
    datasetWindow.destroy()
    datasetWindow.update()


# Creatung a new user folder if it doesn't exist already
def initUser():
    global DatasetPath, CurrentUser

    currentUser = 1

    if os.path.exists(os.path.join(DatasetPath, f'User{currentUser:02d}')):
        currentUser = sorted(list(map(lambda x: int(x[4:]), os.listdir(DatasetPath))))[-1] + 1
    
    os.makedirs(os.path.join(DatasetPath, f'User{currentUser:02d}'))

    CurrentUser = f'User{currentUser:02d}'


# Saving the canvas points to an XML file
def nextGesture(datasetWindow, canvas, clearCanvas, gestureDisplayText, countDisplayText, nextButtonText):
    global CurrentGestureIndex, CurrentSampleCount, MaxGestureIndex, MaxSampleCount

    saveToXML(Gestures[CurrentGestureIndex], CurrentSampleCount, store.currentUnistroke)

    clearCanvas(canvas)

    if CurrentGestureIndex == MaxGestureIndex - 1 and CurrentSampleCount == MaxSampleCount:
        closeWindow(datasetWindow)
        return

    updateDisplayTexts(gestureDisplayText, countDisplayText, nextButtonText)


# Updating the prompt text
def updateDisplayTexts(gestureDisplayText, countDisplayText, nextButtonText):
    global CurrentGestureIndex, CurrentSampleCount

    if CurrentSampleCount == MaxSampleCount:
        CurrentGestureIndex = min(CurrentGestureIndex + 1, MaxGestureIndex - 1)
        CurrentSampleCount = 1
    else:
        CurrentSampleCount += 1

    gestureText = Gestures[CurrentGestureIndex].replace('_', ' ').upper()
    gestureDisplayText.set(f'gesture type: {gestureText}')

    countDisplayText.set(f'sample #: {CurrentSampleCount}')

    nextButtonText.set(f'Next ({MaxGestureIndex - CurrentGestureIndex - 1} gestures remaining)')


# Saving the canvas points to an XML file
def saveToXML(name, gesture_count, points):
    global DatasetPath, CurrentUser

    finalPath = os.path.join(DatasetPath, CurrentUser, name + f'{gesture_count:02d}.xml')

    root = ET.Element('Gesture', attrib={
        'Name': f'{gesture_count:02d}',
        'Subject': str(int(CurrentUser[4:])),
        'Number': str(gesture_count),
        'NumPts': str(len(points))
    })

    for point in points:
        ET.SubElement(root, 'Point', X=str(point[0]), Y=str(point[1]))
    
    pretty_xml = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

    with open(finalPath, 'w') as f:
        f.write(pretty_xml)