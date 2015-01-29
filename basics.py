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

def drawLine(canvas, point1, point2, color):
    canvas.create_line(point1.x, point1.y, point2.x, point2.y, fill=color)

def drawDashedLine(canvas, point1, point2, color):
    canvas.create_line(point1.x, point1.y, point2.x, point2.y, dash=(4, 4), fill=color)

