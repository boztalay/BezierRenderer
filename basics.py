import math

POINT_RADIUS = 3

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, otherPoint):
        self.x = otherPoint.x
        self.y = otherPoint.y

    def distanceTo(self, otherPoint):
        return math.sqrt(pow(self.x - otherPoint.x, 2) + pow(self.y - otherPoint.y, 2))

def drawPoint(canvas, point, color):
    canvas.create_oval(point.x - POINT_RADIUS, point.y - POINT_RADIUS,
                       point.x + POINT_RADIUS, point.y + POINT_RADIUS,
                       outline=color, fill="white")

def buildCoordinatesListFromPoints(points):
    pointCoords = []
    for point in points:
        pointCoords.append(point.x)
        pointCoords.append(point.y)

    return pointCoords

def drawLine(canvas, points, color):
    pointCoords = buildCoordinatesListFromPoints(points)
    canvas.create_line(pointCoords, fill=color)

def drawDashedLine(canvas, points, color):
    pointCoords = buildCoordinatesListFromPoints(points)
    canvas.create_line(pointCoords, dash=(4, 4), fill=color)

def pointBetweenPoints(point1, point2, proportion):
    xDifference = point2.x - point1.x
    yDifference = point2.y - point1.y

    xOffset = xDifference * proportion
    yOffset = yDifference * proportion

    return Point(point1.x + xOffset, point1.y + yOffset)

def clampPointToBounds(point, boundX, boundY, margin):
    if point.x < 0 + margin:
        point.x = 0 + margin
    elif point.x > boundX - margin:
        point.x = boundX - margin

    if point.y < 0 + margin:
        point.y = 0 + margin
    elif point.y > boundY - margin:
        point.y = boundY - margin

def areFloatsEqual(float1, float2):
    if float1 > float2 - 0.001 and float1 < float2 + 0.001:
        return True
    else:
        return False
