from Tkinter import *
from dataTypes import *

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

POINT_RADIUS = 3

STATE_IDLE = 0
STATE_PLACING = 1
STATE_MOVING = 2
state = STATE_IDLE

curveBeingPlaced = None
curveBeingMoved = None
pointTypeBeingMoved = None

master = Tk()
master.resizable(width=False, height=False)
canvas = Canvas(master, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

bezierCurves = []

def drawPoint(point, color):
    canvas.create_oval(point.x - POINT_RADIUS, point.y - POINT_RADIUS,
                       point.x + POINT_RADIUS, point.y + POINT_RADIUS,
                       outline=color, fill="white")

def drawLine(point1, point2, color):
    canvas.create_line(point1.x, point1.y, point2.x, point2.y, fill=color)

def drawDashedLine(point1, point2, color):
    canvas.create_line(point1.x, point1.y, point2.x, point2.y, dash=(4, 4), fill=color)

def renderBezierCurve(bezierCurve):
    if bezierCurve.origin1 is not None and bezierCurve.origin2 is not None:
        drawDashedLine(bezierCurve.origin1, bezierCurve.origin2, "gray")
    if bezierCurve.origin1 is not None and bezierCurve.handle1 is not None:
        drawLine(bezierCurve.origin1, bezierCurve.handle1, "blue")
    if bezierCurve.origin2 is not None and bezierCurve.handle2 is not None:
        drawLine(bezierCurve.origin2, bezierCurve.handle2, "blue")

    if bezierCurve.origin1 is not None:
        drawPoint(bezierCurve.origin1, "black")
    if bezierCurve.origin2 is not None:
        drawPoint(bezierCurve.origin2, "black")
    if bezierCurve.handle1 is not None:
        drawPoint(bezierCurve.handle1, "black")
    if bezierCurve.handle2 is not None:
        drawPoint(bezierCurve.handle2, "black")

    #if bezierCurve.isReadyToRender():
        #print "rendercurve"

def renderAll():
    canvas.delete("all")
    for bezierCurve in bezierCurves:
        renderBezierCurve(bezierCurve)

def getNearbyBezierCurve(clickPoint):
    closestCurve = None
    closestDistance = None
    closestPointType = None

    for bezierCurve in bezierCurves:
        distance, pointType = bezierCurve.closestPointTo(clickPoint)
        if closestDistance is None or distance < closestDistance:
            closestCurve = bezierCurve
            closestDistance = distance
            closestPointType = pointType

    if closestDistance is not None and closestDistance < 5:
        return (closestCurve, closestPointType)
    else:
        return (None, None)

def placeNewBezierCurve(clickPoint):
    global state
    global curveBeingPlaced

    state = STATE_PLACING

    newCurve = BezierCurve(clickPoint)
    bezierCurves.append(newCurve)

    curveBeingPlaced = newCurve
    renderAll()

def stopPlacingNewBezierCurve(clickPoint):
    global state
    global curveBeingPlaced

    curveBeingPlaced.handle1 = Point(curveBeingPlaced.origin1.x, curveBeingPlaced.origin1.y - 30)
    curveBeingPlaced.handle2 = Point(curveBeingPlaced.origin2.x, curveBeingPlaced.origin2.y - 30)

    state = STATE_IDLE
    curveBeingPlaced = None

    renderAll()

def startMovingBezierCurve(bezierCurve, pointType):
    global state
    global curveBeingMoved
    global pointTypeBeingMoved

    state = STATE_MOVING
    curveBeingMoved = bezierCurve
    pointTypeBeingMoved = pointType

def stopMovingBezierCurve(clickPoint):
    global state
    global curveBeingMoved
    global pointTypeBeingMoved

    state = STATE_IDLE
    curveBeingMoved = None
    pointTypeBeingMoved = None

def mouseClicked(event):
    clickPoint = Point(event.x, event.y)

    if state is STATE_IDLE:
        bezierCurve, pointType = getNearbyBezierCurve(clickPoint)
        if bezierCurve is None:
            placeNewBezierCurve(clickPoint)
        else:
            startMovingBezierCurve(bezierCurve, pointType)
    elif state is STATE_PLACING:
        stopPlacingNewBezierCurve(clickPoint)
    elif state is STATE_MOVING:
        stopMovingBezierCurve(clickPoint)

def mouseMoved(event):
    global curveBeingPlaced
    global curveBeingMoved
    global pointTypeBeingMoved

    mousePos = Point(event.x, event.y)

    if state is STATE_PLACING:
        curveBeingPlaced.origin2 = mousePos
    elif state is STATE_MOVING:
        pointToMove = curveBeingMoved.getPointOfType(pointTypeBeingMoved)
        pointToMove.set(mousePos)

    renderAll()

def clear(event):
    del(bezierCurves[:])
    renderAll()

def quit(event):
    master.quit()

master.bind("<Button-1>", mouseClicked)
master.bind("<Motion>", mouseMoved)
master.bind("c", clear)
master.bind("q", quit)
mainloop()
