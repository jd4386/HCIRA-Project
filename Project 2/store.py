'''
Project Team Members:
1. Jagan Mohan Reddy Dwarampudi (UFID: 9357-2863)
2. Mohammad Shameer Mulla (UFID: 7066-4007)
'''

currentUnistroke = []
currentMultistroke = []
multistrokeExport = True
multistrokeFlag = False if not multistrokeExport else True
resetCanvasFlag = False

def resetCurrentUnistroke():
    global currentUnistroke
    currentUnistroke = []

def updateCurrentUnistroke(x, y):
    global currentUnistroke
    currentUnistroke.append([x, y])

def resetCurrentMultistroke():
    global currentMultistroke
    currentMultistroke = []

def updateCurrentMultistroke():
    global currentMultistroke, currentUnistroke
    currentMultistroke.append(currentUnistroke)
    resetCurrentUnistroke()

# TempGestures = [
#     'T',
#     'N',
#     'D',
#     'P',
#     'X',
#     'H',
#     'I',
#     'exclamation_point',
#     'line',
#     'five_point_star',
#     'null',
#     'arrowhead',
#     # 'pitchfork',
#     'null',
#     'six_point_star',
#     'asterisk',
#     'half_note'
    
# ]

# counter = 0