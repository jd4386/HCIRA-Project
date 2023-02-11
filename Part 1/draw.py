#Importing required libraries
import tkinter as tk

#initialising the XY coordinates
presentX, presentY = 0, 0

#function to capture the initial mouse coordinates
def getXY(event):
    global presentX, presentY

    presentX, presentY = event.x, event.y

#function to draw a line from the initial points to the new mouse location and updates the points to the new mouse location
def drawLine(event):
    global presentX, presentY

    canvas.create_line((presentX, presentY, event.x, event.y), width=2)
    presentX, presentY = event.x, event.y

#function to reset the canvas
def clearCanvas():
    canvas.delete("all")

#Tkinter initialisation
root = tk.Tk()
root.title('Canvas')
root.geometry('800x600')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#canvas initialisation inside the tkinter window
canvas = tk.Canvas(root, bg='black')
canvas.pack(expand=True, fill=tk.BOTH)

#Attaching the left mouse click and mouse motion to the designated functions.
canvas.bind('<Button-1>', getXY)
canvas.bind('<B1-Motion>', drawLine)

#Clear button that resets the canvas
button = tk.Button(root, text='Clear', width=25, command=clearCanvas)
button.pack(pady=5)

#Code to keep the window running until closed
root.mainloop()