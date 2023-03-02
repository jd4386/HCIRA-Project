Readme
Project 1 - Part 4


Team:
Jagan Mohan Reddy Dwarampudi
Mohammed Shameer Mulla


Objective check:
export.py and store.py are the new additions to this part of the project. Export contains most of the code that opens a new window for dataset creation and store is used for variables that are common to both the GUI windows.

a. In export.py file, lines 43-105 is the code for managing the new window that takes user input and function saveToXML() on lines 171-189 is used to save the data to the XML file.

b. Prompts are given to the user at 3 different places on the window. Two labels on lines 55-76 show both the gesture name and sample count for the current gesture. The third prompt is given on the next button on the window which gives forecast information of how many gestures are still left for the user to draw. This can be seen on lines 87-97 where the next button is defined.

c. Informed conset forms for the 6 participants are attached in the zip file. Each user's data is anonymous as the application never asks for user's information. All the data is stored in a directory that is named automatically considering the previous user's data. This code can be seen on lines 124-134 inside the initUser() function.

d. The dataset zip file is attached with user consent forms outside the dataset directory to maintain the anonymity of users.