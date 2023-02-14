Readme
Project 1 - Part 2

Team:
Jagan Mohan Reddy Dwarampudi
Mohammed Shameer Mulla

Objective check:
a. The list currentUnistroke defined on Line 18 in draw.py is used to store the captured points made by the user.
b. Lines 5-22 in recognizer.py show the dictionary Unistrokes that stores all the template gestures with key as the name of the gesture and value as the list of points that make up the gesture.
c. Several functions and other supporting functions are defined in recognizer.py that are used to preprocess the user's gesture points and compare them with the template gestures. Futher, the complete $1 recognizer algorithm is implemented in this file taking the javascript implementation as a reference. The 4 specific steps mentioned for the algorithm can be found at the following lines.
    1. Resampling: Lines 144-183 in recognizer.py contains the core functionality for resampling the points in the resample() function.
    2. Rotation: rotateBy() function in lines 70-83 use other supporting functions for the rotation step.
    3. Scaling + Translation: scaleTo() and translateTo() functions defined in lines 204-215 and 236-246 respectively use other functions to scale anf translate the points.
    4. Matching process: Lines 86-121 in draw.py preprocess the user's input strokes and calls distanceAtBestAngle() function defined in lines 33-58 in recognizer.py. These lines basically compare the user's stroke and each templeate for a distance score which is them used to find out the best matching template and returns it as the matched result.
d. The final result i.e., the matched template's name, score out of 1 using the halfDiagonal value, and the execution time are displayed on the GUI window after user finishes drawing the gesture and the $1 recognizer algorithm is run. This display code can be found in canvas.py recognize function in lines 72-132. More clearly, Lines 100, 126, and 129 contain the code for displaying the result to the user.