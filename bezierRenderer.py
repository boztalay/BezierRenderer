import time
from Tkinter import *

from basics import *
from bezierCurve import *

# Some ugly constants to control some behavior

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

TARGET_FRAME_TIME = 20

MOVEMENT_CLICK_RADIUS = 7
BORDER_MARGIN = 5

# Keeping track of the ugly global state

STATE_IDLE = 0
STATE_PLACING = 1
STATE_MOVING = 2
state = STATE_IDLE

# Some ugly globals

bezierCurves = []

curveBeingPlaced = None
curveBeingMoved = None
pointBeingMoved = None

# Set up the window and put a canvas in it

master = Tk()
master.resizable(width=False, height=False)
canvas = Canvas(master, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
canvas.pack()

# Rendering the curves

def renderAll():
    global canvas
    global bezierCurves

    startTime = time.time()

    canvas.delete("all")
    for bezierCurve in bezierCurves:
        bezierCurve.render(canvas)

    # Some frame duration management to keep a consistent framerate
    secondsElapsed = time.time() - startTime
    millisecondsElapsed = int(round(secondsElapsed))
    frameTime = max(0, TARGET_FRAME_TIME - millisecondsElapsed)

    # Continue the loop by starting another timer
    master.after(frameTime, renderAll)

# Handling mouse input

def mouseClicked(event):
    global state

    clickPoint = Point(event.x, event.y)
    clampPointToBounds(clickPoint, WINDOW_WIDTH, WINDOW_HEIGHT, BORDER_MARGIN)

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
    clampPointToBounds(mousePos, WINDOW_WIDTH, WINDOW_HEIGHT, BORDER_MARGIN)

    if state is STATE_PLACING:
        curveBeingPlaced.removeLastPoint()
        curveBeingPlaced.addPoint(mousePos)
    elif state is STATE_MOVING:
        pointBeingMoved.set(mousePos)
        curveBeingMoved.setNeedsRender()

# A helper function to get a nearby point on a curve to move if the user clicks near it

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

    if closestDistance is not None and closestDistance < MOVEMENT_CLICK_RADIUS:
        return (closestPoint, closestCurve)
    else:
        return (None, None)

# Handling placing new curves

def startPlacingNewBezierCurve(clickPoint):
    global state
    global bezierCurves
    global curveBeingPlaced

    state = STATE_PLACING

    newCurve = BezierCurve(clickPoint)
    newCurve.addPoint(Point(clickPoint.x, clickPoint.y))

    bezierCurves.append(newCurve)
    curveBeingPlaced = newCurve

def continuePlacingNewBezierCurve(clickPoint):
    global curveBeingPlaced

    curveBeingPlaced.addPoint(Point(clickPoint.x, clickPoint.y))

def placeKeyPressed(event):
    if state is STATE_PLACING:
        stopPlacingNewBezierCurve()

def stopPlacingNewBezierCurve():
    global state
    global curveBeingPlaced

    if curveBeingPlaced is not None:
        curveBeingPlaced.removeLastPoint()

    state = STATE_IDLE
    curveBeingPlaced = None

# Handling moving points on existing curves

def startMovingPointOnCurve(point, curve):
    global state
    global pointBeingMoved
    global curveBeingMoved

    state = STATE_MOVING
    pointBeingMoved = point
    curveBeingMoved = curve

def stopMovingPointOnCurve():
    global state
    global curveBeingMoved
    global pointTypeBeingMoved

    state = STATE_IDLE
    curveBeingMoved = None
    pointBeingMoved = None

# Controlling whether and where the intermediate lines are drawn

def toggleIntermediateRendering(event):
    global bezierCurves

    BezierCurve.intermediateRendering = not BezierCurve.intermediateRendering
    for bezierCurve in bezierCurves:
        bezierCurve.setNeedsIntermediateRender()

def moveIntermediates(event):
    if event.keysym == "Right":
        BezierCurve.intermediateStep += 0.01
    elif event.keysym == "Left":
        BezierCurve.intermediateStep -= 0.01

    if BezierCurve.intermediateStep < 0.0:
        BezierCurve.intermediateStep = 0.0;
    elif BezierCurve.intermediateStep > 1.0:
        BezierCurve.intermediateStep = 1.0

    for bezierCurve in bezierCurves:
        bezierCurve.setNeedsIntermediateRender()

# Clearing the screen and quitting

def clear(event):
    global bezierCurves

    if state is STATE_IDLE:
        del(bezierCurves[:])

def quit(event):
    master.quit()

# Bind some I/O

master.bind("<Button-1>", mouseClicked)
master.bind("<Motion>", mouseMoved)
master.bind("p", placeKeyPressed)
master.bind("i", toggleIntermediateRendering)
master.bind("<Left>", moveIntermediates)
master.bind("<Right>", moveIntermediates)
master.bind("c", clear)
master.bind("q", quit)

# Start rendering things

master.after(TARGET_FRAME_TIME, renderAll)

mainloop()
