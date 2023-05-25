'''
Project Team Members:
1. Jagan Mohan Reddy Dwarampudi (UFID: 9357-2863)
2. Mohammad Shameer Mulla (UFID: 7066-4007)
'''

currentUnistroke = []

def resetCurrentUnistroke():
    global currentUnistroke
    currentUnistroke = []

def updateCurrentUnistroke(x, y):
    global currentUnistroke
    currentUnistroke.append([x, y])