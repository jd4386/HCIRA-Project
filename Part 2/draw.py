#Importing required libraries
import tkinter as tk

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#initialising the XY coordinates
presentX, presentY = 0, 0

#function to capture the initial mouse coordinates
def getXY(event):
    canvas.delete("all")

    global presentX, presentY
    presentX, presentY = event.x, event.y

    box_len = 3
    canvas.create_rectangle(
        presentX - box_len,
        presentY - box_len,
        presentX + box_len,
        presentY + box_len,
        fill='#0000d8',
        outline=''
    )

    global display_text
    display_text.set('Recording unistroke...')

    

#function to draw a line from the initial points to the new mouse location and updates the points to the new mouse location
def drawLine(event):
    global presentX, presentY

    canvas.create_line(
        (presentX, presentY, event.x, event.y),
        width=2,
        fill='#0000d8'
    )

    presentX, presentY = event.x, event.y


def recognize(event):
    global display_text
    display_text.set('Finished')


#function to reset the canvas
def clearCanvas():
    canvas.delete("all")


#Tkinter initialisation
root = tk.Tk()
root.title('Canvas')
root.geometry('800x600')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

display_text = tk.StringVar()
display = tk.Label(
    root,
    textvariable=display_text,
    bg='#ffff98',
    fg='#0000d8',
    anchor='w'
)
display.pack(fill=tk.BOTH, padx=3)

#canvas initialisation inside the tkinter window
canvas = tk.Canvas(root, bg='#dddddd')
canvas.pack(expand=True, fill=tk.BOTH)

#Attaching the left mouse click and mouse motion to the designated functions.
canvas.bind('<Button-1>', getXY)
canvas.bind('<B1-Motion>', drawLine)
canvas.bind('<ButtonRelease-1>', recognize)

#Clear button that resets the canvas
button = tk.Button(root, text='Clear', width=25, command=clearCanvas)
button.pack(pady=5)

#Code to keep the window running until closed
root.mainloop()