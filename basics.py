import math

# More ugly globals

POINT_RADIUS = 3

# A quick class to store points

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, otherPoint):
        self.x = otherPoint.x
        self.y = otherPoint.y

    def distanceTo(self, otherPoint):
        return math.sqrt(pow(self.x - otherPoint.x, 2) + pow(self.y - otherPoint.y, 2))

# Drawing points and lines

def drawPoint(canvas, point, color):
    canvas.create_oval(point.x - POINT_RADIUS, point.y - POINT_RADIUS,
                       point.x + POINT_RADIUS, point.y + POINT_RADIUS,
                       outline=color, fill="white")

def drawLine(canvas, points, color):
    pointCoords = buildCoordinatesListFromPoints(points)
    canvas.create_line(pointCoords, fill=color)

def drawDashedLine(canvas, points, color):
    pointCoords = buildCoordinatesListFromPoints(points)
    canvas.create_line(pointCoords, dash=(4, 4), fill=color)

def buildCoordinatesListFromPoints(points):
    pointCoords = []
    for point in points:
        pointCoords.append(point.x)
        pointCoords.append(point.y)

    return pointCoords

# Returns a point (proportion * 100) percent between the given points, starting from the first

def pointBetweenPoints(point1, point2, proportion):
    xDifference = point2.x - point1.x
    yDifference = point2.y - point1.y

    xOffset = xDifference * proportion
    yOffset = yDifference * proportion

    return Point(point1.x + xOffset, point1.y + yOffset)

# Helper function to keep the given point within the given bounds

def clampPointToBounds(point, boundX, boundY, margin):
    if point.x < 0 + margin:
        point.x = 0 + margin
    elif point.x > boundX - margin:
        point.x = boundX - margin

    if point.y < 0 + margin:
        point.y = 0 + margin
    elif point.y > boundY - margin:
        point.y = boundY - margin

# Ugh floating point

def areFloatsEqual(float1, float2):
    if float1 > (float2 - 0.001) and float1 < (float2 + 0.001):
        return True
    else:
        return False
