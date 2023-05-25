'''
Project Team Members:
1. Jagan Mohan Reddy Dwarampudi (UFID: 9357-2863)
2. Mohammad Shameer Mulla (UFID: 7066-4007)
'''

# Importing required libraries
import math
import time
from icecream import ic


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Unistroke:
    def __init__(self, name, useBoundedRotationInvariance, points):
        self.name = name

        # ic(name)
        
        self.points = resample(points, NumPoints)
        radians = indicativeAngle(self.points)
        self.points = rotateBy(self.points, -radians)
        self.points = scaleDimTo(self.points, SquareSize, OneDThreshold)
        if useBoundedRotationInvariance:
            self.points = rotateBy(self.points, +radians)
        self.points = translateTo(self.points, Origin)

        self.startUnitVector = calcStartUnitVector(self.points, StartAngleIndex)


class Multistroke:
    def __init__(self, name, useBoundedRotationInvariance, strokes):
        self.name = name
        self.numStrokes = len(strokes)

        order = list(range(self.numStrokes))
        orders = []
        heapPermute(self.numStrokes, order, orders)

        unistrokes = makeUnistrokes(strokes, orders)
        self.unistrokes = [Unistroke(name, useBoundedRotationInvariance, unistroke) for unistroke in unistrokes]


class Result:
    def __init__(self, name, score, ms):
        self.name = name
        self.score = score
        self.time = ms


def heapPermute(n, order, orders):
    if n == 1:
        orders.append(order.copy())
    else:
        for i in range(n):
            heapPermute(n - 1, order, orders)
            if n % 2 == 1:
                order[0], order[n - 1] = order[n - 1], order[0]
            else:
                order[i], order[n - 1] = order[n - 1], order[i]


def makeUnistrokes(strokes, orders):
    unistrokes = []
    
    for order in orders:
        for b in range(2 ** len(order)):
            unistroke = []

            for i in range(len(order)):
                pts = strokes[order[i]].copy()
                if ((b >> i) & 1) == 1:
                    pts = strokes[order[i]][::-1]

            for pt in pts:
                unistroke.append(pt)

            unistrokes.append(unistroke)

    return unistrokes


# NumMultistrokes = 16;
NumPoints = 96
SquareSize = 250.0
OneDThreshold = 0.25
Origin = Point(0, 0)
Diagonal = math.sqrt(SquareSize * SquareSize + SquareSize * SquareSize)
HalfDiagonal = 0.5 * Diagonal
AngleRange = math.radians(45.0)
AnglePrecision = math.radians(2.0)
Phi = 0.5 * (-1.0 + math.sqrt(5.0))
StartAngleIndex = int(NumPoints / 8)
AngleSimilarityThreshold = math.radians(30.0)

useBoundedRotationInvariance = False


def recognize(strokes, useBoundedRotationInvariance, requireSameNoOfStrokes, multistrokes=None):
    global Multistrokes
    multistrokes = multistrokes if multistrokes else Multistrokes
    t0 = time.time()
    points = combineStrokes(strokes)
    candidate = Unistroke("", useBoundedRotationInvariance, points)

    u = -1
    b = float("inf")

    for i in range(len(multistrokes)):
        if not requireSameNoOfStrokes or len(strokes) == multistrokes[i].numStrokes:
            for j in range(len(multistrokes[i].unistrokes)):
                if angleBetweenUnitVectors(candidate.startUnitVector, multistrokes[i].unistrokes[j].startUnitVector) <= AngleSimilarityThreshold:
                    d = distanceAtBestAngle(candidate.points, multistrokes[i].unistrokes[j], -AngleRange, +AngleRange, AnglePrecision)
                    if d < b:
                        b = d
                        u = i

    t1 = time.time()

    return Result('No match.', 0.0, t1 - t0) if u == -1 else Result(multistrokes[u].name, 1.0 - b / HalfDiagonal, t1 - t0)
    # return Result('No match.', 0.0, 0)


def distanceAtBestAngle(points, T, a, b, threshold):
    x1 = Phi * a + (1.0 - Phi) * b
    f1 = distanceAtAngle(points, T, x1)
    x2 = (1.0 - Phi) * a + Phi * b
    f2 = distanceAtAngle(points, T, x2)

    while abs(b - a) > threshold:
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = Phi * a + (1.0 - Phi) * b
            f1 = distanceAtAngle(points, T, x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = (1.0 - Phi) * a + Phi * b
            f2 = distanceAtAngle(points, T, x2)

    return min(f1, f2)


def distanceAtAngle(points, T, radians):
    newpoints = rotateBy(points, radians)
    
    return pathDistance(newpoints, T.points)


def pathDistance(pts1, pts2):
    d = 0.0

    for i in range(len(pts1)):
        d += distance(pts1[i], pts2[i])

    return d / len(pts1)


def angleBetweenUnitVectors(v1, v2):
    n = v1.x * v2.x + v1.y * v2.y
    c = max(-1, min(1, n))

    return math.acos(c)


def combineStrokes(strokes):
    points = []

    for stroke in strokes:
        for pt in stroke:
            points.append(Point(pt[0], pt[1]))

    return points


# Function to scale the points to the given size
def resample(points, n):
    # Get the length of the path
    I = pathLength(points) / float(n-1)
    newPoints = [points[0]]
    # Distance traveled
    D = 0.0

    # Loop through the points
    i = 1
    while i < len(points):
        # Get the distance between the current point and the previous point
        d = distance(points[i - 1], points[i])

        # If the distance and the distance traveled is greater than or equal to the interval
        if D + d >= I:
            # if d == 0:
            #     i += 1
            #     continue
            # else:
            # Get the point between the current point and the previous point
            delta_distance = float((I - D) / d)

            qx = points[i - 1].x + delta_distance * (points[i].x - points[i - 1].x)
            qy = points[i - 1].y + delta_distance * (points[i].y - points[i - 1].y)

            # Add the point to the list
            q = Point(qx, qy)
            newPoints.append(q)
            points.insert(i, q)

            # Reset the distance traveled
            D = 0.0
        else:
            # Add the distance to the distance traveled if the distance and the distance traveled is less than the interval
            D += d
        
        # Increment the index
        i += 1

    # If the number of points is less than the number of points to resample to
    if len(newPoints) == n - 1:
        # Add the last point to the list
        lastPointObject = Point(points[len(points) - 1].x, points[len(points) - 1].y)
        newPoints.append(lastPointObject)
    
    return newPoints


# Function to return the length of the path
def pathLength(points):
    d = 0

    # Loop through the points and add the distance between the current point and the previous point
    for i in range(1, len(points)):
        d += distance(points[i - 1], points[i])

    return d


# Function to return the distance between two points
def distance(p1, p2):
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)


# Function to return the angle of the points
def indicativeAngle(points):
    c = centroid(points)
    return math.atan2(c.y - points[0].y, c.x - points[0].x)


# Function to return the centroid of the points
def centroid(points):
    x = 0
    y = 0

    # Loop through the points and add them to the total
    for i in range(len(points)):
        x += points[i].x
        y += points[i].y

    # Divide by the number of points to get the average
    x /= len(points)
    y /= len(points)

    # Return the centroid
    return Point(x, y)


# Function to rotate the points by the given angle
def rotateBy(points, radians):
    c = centroid(points)
    cos = math.cos(radians)
    sin = math.sin(radians)
    newpoints = []

    # Loop through the points and rotate each one
    for i in range(len(points)):
        qx = (points[i].x - c.x) * cos - (points[i].y - c.y) * sin + c.x
        qy = (points[i].x - c.x) * sin + (points[i].y - c.y) * cos + c.y
        newpoints.append(Point(qx, qy))

    # Return the rotated points
    return newpoints


# Function to scale the points to the given size
def scaleDimTo(points, size, ratio1D):
    # Get the bounding box of the figure
    B = boundingBox(points)
    # uniformly = False

    # # avoid divide by zero
    # if B.width == 0 or B.height == 0:
    #     uniformly = 0 <= ratio1D
    # else:
    uniformly = min(B.width / B.height, B.height / B.width) <= ratio1D

    newpoints = []

    # Loop through the points and scale them to the given size
    for i in range(len(points)):
        qx = points[i].x * (size / max(B.width, B.height)) if uniformly else points[i].x * (size / B.width)
        qy = points[i].y * (size / max(B.width, B.height)) if uniformly else points[i].y * (size / B.height)
        newpoints.append(Point(qx, qy))

    return newpoints


# Function to return the bounding box of the figure
def boundingBox(points):
    minX = +float('inf')
    maxX = -float('inf')
    minY = +float('inf')
    maxY = -float('inf')

    # Loop through the points and get the minimum and maximum x and y values
    for i in range(len(points)):
        minX = min(minX, points[i].x)
        minY = min(minY, points[i].y)
        maxX = max(maxX, points[i].x)
        maxY = max(maxY, points[i].y)

    small = 0.0000000001

    # Return the bounding box
    return Rectangle(minX, minY, max(maxX - minX, small), max(maxY - minY, small))


# Function to translate the points to the given point
def translateTo(points, pt):
    c = centroid(points)
    newpoints = []

    # Loop through the points and translate them to the given point
    for i in range(len(points)):
        qx = points[i].x + pt.x - c.x
        qy = points[i].y + pt.y - c.y
        newpoints.append(Point(qx, qy))

    return newpoints


def calcStartUnitVector(points, index):
    # if index >= len(points):
    #     return Point(0, 0)
    
    v = Point(points[index].x - points[0].x, points[index].y - points[0].y)
    length = math.sqrt(v.x * v.x + v.y * v.y)

    return Point(v.x / length, v.y / length)


Multistrokes = [
    Multistroke("T", useBoundedRotationInvariance, [
		[Point(30, 7), Point(103, 7)],
		[Point(66, 7), Point(66, 87)]
    ]),
    Multistroke("N", useBoundedRotationInvariance, [
		[Point(177, 92), Point(177, 2)],
		[Point(182, 1), Point(246, 95)],
		[Point(247, 87), Point(247, 1)]
    ]),
    Multistroke("D", useBoundedRotationInvariance, [
		[Point(345, 9), Point(345, 87)],
		[Point(351, 8), Point(363, 8), Point(372, 9), Point(380, 11), Point(386, 14), Point(391, 17), Point(394, 22), Point(397, 28), Point(399, 34), Point(400, 42), Point(400, 50), Point(400, 56), Point(399, 61), Point(397, 66), Point(394, 70), Point(391, 74), Point(386, 78), Point(382, 81), Point(377, 83), Point(372, 85), Point(367, 87), Point(360, 87), Point(355, 88), Point(349, 87)]
    ]),
    Multistroke("P", useBoundedRotationInvariance, [
		[Point(507, 8), Point(507, 87)],
		[Point(513, 7), Point(528, 7), Point(537, 8), Point(544, 10), Point(550, 12), Point(555, 15), Point(558, 18), Point(560, 22), Point(561, 27), Point(562, 33), Point(561, 37), Point(559, 42), Point(556, 45), Point(550, 48), Point(544, 51), Point(538, 53), Point(532, 54), Point(525, 55), Point(519, 55), Point(513, 55), Point(510, 55)]
    ]),
    Multistroke("X", useBoundedRotationInvariance, [
		[Point(30, 146), Point(106, 222)],
		[Point(30, 225), Point(106, 146)]
    ]),
    Multistroke("H", useBoundedRotationInvariance, [
		[Point(188, 137), Point(188, 225)],
		[Point(188, 180), Point(241, 180)],
		[Point(241, 137), Point(241, 225)]
	]),
    Multistroke("I", useBoundedRotationInvariance, [
		[Point(371, 149), Point(371, 221)],
		[Point(341, 149), Point(401, 149)],
		[Point(341, 221), Point(401, 221)]
	]),
    # Multistroke("exclamation", useBoundedRotationInvariance, [
	# 	[Point(526, 142), Point(526, 204)],
	# 	[Point(526, 221)]
	# ]),
    Multistroke("line", useBoundedRotationInvariance, [
		[Point(12, 347), Point(119, 347)]
	]),
    Multistroke("five-point star", useBoundedRotationInvariance, [
		[Point(177, 396), Point(223, 299), Point(262, 396), Point(168, 332), Point(278, 332), Point(184, 397)]
	]),
    Multistroke("null", useBoundedRotationInvariance, [
		[Point(382, 310), Point(377, 308), Point(373, 307), Point(366, 307), Point(360, 310), Point(356, 313), Point(353, 316), Point(349, 321), Point(347, 326), Point(344, 331), Point(342, 337), Point(341, 343), Point(341, 350), Point(341, 358), Point(342, 362), Point(344, 366), Point(347, 370), Point(351, 374), Point(356, 379), Point(361, 382), Point(368, 385), Point(374, 387), Point(381, 387), Point(390, 387), Point(397, 385), Point(404, 382), Point(408, 378), Point(412, 373), Point(416, 367), Point(418, 361), Point(419, 353), Point(418, 346), Point(417, 341), Point(416, 336), Point(413, 331), Point(410, 326), Point(404, 320), Point(400, 317), Point(393, 313), Point(392, 312)],
		[Point(418, 309), Point(337, 390)]
	]),
    Multistroke("arrowhead", useBoundedRotationInvariance, [
		[Point(506, 349), Point(574, 349)],
		[Point(525, 306), Point(584, 349), Point(525, 388)]
	]),
    Multistroke("pitchfork", useBoundedRotationInvariance, [
		[Point(38, 470), Point(36, 476), Point(36, 482), Point(37, 489), Point(39, 496), Point(42, 500), Point(46, 503), Point(50, 507), Point(56, 509), Point(63, 509), Point(70, 508), Point(75, 506), Point(79, 503), Point(82, 499), Point(85, 493), Point(87, 487), Point(88, 480), Point(88, 474), Point(87, 468)],
		[Point(62, 464), Point(62, 571)]
	]),
    Multistroke("six-point star", useBoundedRotationInvariance, [
		[Point(177, 554), Point(223, 476), Point(268, 554), Point(183, 554)],
		[Point(177, 490), Point(223, 568), Point(268, 490), Point(183, 490)]
	]),
    Multistroke("asterisk", useBoundedRotationInvariance, [
		[Point(325, 499), Point(417, 557)],
		[Point(417, 499), Point(325, 557)],
		[Point(371, 486), Point(371, 571)]
	]),
    Multistroke("half-note", useBoundedRotationInvariance, [
		[Point(546, 465), Point(546, 531)],
		[Point(540, 530), Point(536, 529), Point(533, 528), Point(529, 529), Point(524, 530), Point(520, 532), Point(515, 535), Point(511, 539), Point(508, 545), Point(506, 548), Point(506, 554), Point(509, 558), Point(512, 561), Point(517, 564), Point(521, 564), Point(527, 563), Point(531, 560), Point(535, 557), Point(538, 553), Point(542, 548), Point(544, 544), Point(546, 540), Point(546, 536)]
    ])
]