Readme
Project 1 - Part 1

Team:
Jagan Mohan Reddy Dwarampudi
Mohammed Shameer Mulla

Objective check:
1. The project environment is set in Python 3.11.1 using the Visual Studio Code editor. Tkinter library is used for GUI development. Lines 2, 25-29, and 44 show the import and initialization of GUI window.
2. Lines 32, 33 show the creation of a blank canvas which is added to the Tkinter instance.
3. Lines 36, 37 add the mouse click down and mouse movement to the functions getXY() and drawLine() defined in lines 8-11 and 14-18 respectively.
4. Lines 40, 41 add the reset canvas feature that invokes function clearCanvas() in lines 21, 22.

Explanation:
-> Each left mouse button click calls the getXY() function which store the current mouse pointer coordinates.
-> Whenever the mouse is moved with a click, drawLine() function updates the points to the new mouse location coordinates every frame and draws a line joining the old and the new coordinates until the click is released.
-> Clear button simply clears all the drawn lines and resets the canvas.