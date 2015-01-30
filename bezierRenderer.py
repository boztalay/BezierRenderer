from Tkinter import *

from basics import *
from bezierCurve import *

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

STATE_IDLE = 0
STATE_PLACING = 1
STATE_MOVING = 2
state = STATE_IDLE

curveBeingPlaced = None
curveBeingMoved = None
pointBeingMoved = None

master = Tk()
master.resizable(width=False, height=False)
canvas = Canvas(master, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
canvas.pack()

bezierCurves = []

def renderAll():
    global canvas
    global bezierCurves

    canvas.delete("all")
    for bezierCurve in bezierCurves:
        bezierCurve.render(canvas)

def getNearbyBezierCurve(clickPoint):
    global bezierCurves

    closestCurve = None
    closestDistance = None
    closestPoint = None

    for bezierCurve in bezierCurves:
        point, distance = bezierCurve.closestPointTo(clickPoint)
        if closestDistance is None or distance < closestDistance:
            closestCurve = bezierCurve
            closestDistance = distance
            closestPoint = point

    if closestDistance is not None and closestDistance < 7:
        return (closestPoint, closestCurve)
    else:
        return (None, None)

def startPlacingNewBezierCurve(clickPoint):
    global state
    global bezierCurves
    global curveBeingPlaced

    state = STATE_PLACING

    newCurve = BezierCurve(clickPoint)
    newCurve.points.append(Point(clickPoint.x, clickPoint.y))
    bezierCurves.append(newCurve)

    curveBeingPlaced = newCurve
    renderAll()

def continuePlacingNewBezierCurve(clickPoint):
    global curveBeingPlaced

    curveBeingPlaced.points.append(Point(clickPoint.x, clickPoint.y))
    curveBeingPlaced.setNeedsRender()

    renderAll()

def stopPlacingNewBezierCurve():
    global state
    global curveBeingPlaced

    if curveBeingPlaced is not None:
        curveBeingPlaced.points.pop()
        curveBeingPlaced.setNeedsRender()

    state = STATE_IDLE
    curveBeingPlaced = None

    renderAll()

def startMovingPointOnCurve(point, curve):
    global state
    global pointBeingMoved
    global curveBeingMoved

    state = STATE_MOVING
    pointBeingMoved = point
    curveBeingMoved = curve

    renderAll()

def stopMovingPointOnCurve():
    global state
    global curveBeingMoved
    global pointTypeBeingMoved

    state = STATE_IDLE
    curveBeingMoved = None
    pointBeingMoved = None

    renderAll()

def placeKeyPressed(event):
    if state is STATE_PLACING:
        stopPlacingNewBezierCurve()

def mouseClicked(event):
    global state

    clickPoint = Point(event.x, event.y)
    clampPointToBounds(clickPoint, WINDOW_WIDTH, WINDOW_HEIGHT, 5)

    if state is STATE_IDLE:
        point, bezierCurve = getNearbyBezierCurve(clickPoint)
        if bezierCurve is not None:
            startMovingPointOnCurve(point, bezierCurve)
        else:
            startPlacingNewBezierCurve(clickPoint)
    elif state is STATE_PLACING:
        continuePlacingNewBezierCurve(clickPoint)
    elif state is STATE_MOVING:
        stopMovingPointOnCurve()

def mouseMoved(event):
    global state
    global curveBeingPlaced
    global curveBeingMoved
    global pointBeingMoved

    mousePos = Point(event.x, event.y)
    clampPointToBounds(mousePos, WINDOW_WIDTH, WINDOW_HEIGHT, 5)

    if state is STATE_PLACING:
        curveBeingPlaced.points.pop()
        curveBeingPlaced.points.append(mousePos)
        curveBeingPlaced.setNeedsRender()
    elif state is STATE_MOVING:
        pointBeingMoved.set(mousePos)
        curveBeingMoved.setNeedsRender()

    renderAll()

def clear(event):
    global bezierCurves

    del(bezierCurves[:])
    renderAll()

def quit(event):
    master.quit()

master.bind("<Button-1>", mouseClicked)
master.bind("<Motion>", mouseMoved)
master.bind("p", placeKeyPressed)
master.bind("c", clear)
master.bind("q", quit)
mainloop()
