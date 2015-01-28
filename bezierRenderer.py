from Tkinter import *

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y

class BezierCurve():
    def __init__(self, origin1):
        self.origin1 = origin1
        self.origin2 = None
        self.handle1 = None
        self.handle2 = None

    def isReadyToRender(self):
        return (self.origin1 is not None and self.origin2 is not None and self.handle1 is not None and self.handle2 is not None)

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
POINT_RADIUS = 3

master = Tk()
master.resizable(width=False, height=False)
canvas = Canvas(master, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

bezierCurves = []

def renderAll(event=None):
    canvas.delete("all")
    for bezierCurve in bezierCurves:
        canvas.create_oval(bezierCurve.origin1.x - POINT_RADIUS, bezierCurve.origin1.y - POINT_RADIUS,
                           bezierCurve.origin1.x + POINT_RADIUS, bezierCurve.origin1.y + POINT_RADIUS,
                           outline="black")

def mouseClicked(event):
    bezierCurves.append(BezierCurve(Point(event.x, event.y)))
    renderAll()

def clear(event):
    del(bezierCurves[:])
    renderAll()

def quit(event):
    master.quit()

def removeAllChildren(widget):
    for child in widget.winfo_children():
        child.destroy()

master.bind("r", renderAll)
master.bind("<Button-1>", mouseClicked)
master.bind("c", clear)
master.bind("q", quit)
mainloop()
