Readme
Project 1 - Part 3


Team:
Jagan Mohan Reddy Dwarampudi
Mohammed Shameer Mulla


Objective check:
A new file template.py is created which contains the code for Part 3 of the project. Each objective is implemented in a separate function. The main function calls each of the functions in the order of the objectives.

a. The XML dataset is downloaded and stored in the local directory. The XML file is parsed using the ElementTree library and the data is stored in a dictionary. This can be seen in the readDataset() function on lines 44-64. The functions has nested for loops to iterate through each user, speed, gesture, and example. The key for the dictionary is the user, speed, gesture, and example. The value is a from the XML file. The dictionary is returned.

b. Function preprocessDataset() on lines 68-69 simply calls the preprocess function from recognizer.py in Part 2. The function returns the preprocessed dataset.

c. Function testing() on lines 73-184 contains the major part of the code. The function takes the preprocessed dataset as input. The function first creates a dictionary to store the results. Loops similar to readDataset() are implemented with additional loop for multiple random iterations for better testing. Each test value, result is stored and the average is calculated. The results are stored in a dictionary and returned. NBest lists are also created for each user, speed, gesture, and example. They are sorted and only the top 50 are written to the log file.

d. Function outputResults() on lines 188-192 takes the results variables as input and writes the results to the log file in a csv fromat. The log file follows the format specified in the project description and similar to the sample log file.


Notes:
Testing is run for all the users, medium speed, all gestures, for upto 9 examples, and 10 iterations each as mentioned in the project description. The code also supports testing for all the speeds but it was decreased for faster testing. There are many accuracy scores and each correspond to each user, speed, examples, and gesture.