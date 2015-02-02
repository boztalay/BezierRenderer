from basics import *

STEP_SIZE = 1.0 / 100.0;

class BezierCurve():
    intermediateRendering = False
    intermediateStep = 0.50
    intermediateColorPalette = ["green", "red", "blue", "cyan", "magenta"]

    def __init__(self, firstPoint):
        self.points = [firstPoint]
        self.needsRender = True
        self.needsIntermediateRender = True
        self.curvePoints = []
        self.intermediatePoints = []

    def render(self, canvas):
        # Lines between the points
        if len(self.points) > 1:
            drawDashedLine(canvas, self.points, "gray")

        # Actual Bezier curve
        self.renderCurve(canvas)

        # The points
        for point in self.points:
            drawPoint(canvas, point, "black")

        # Intermediates
        self.renderIntermediates(canvas)

    def renderIntermediates(self, canvas):
        if not BezierCurve.intermediateRendering:
            return

        if self.needsIntermediateRender:
            self.intermediatePoints = []
            self.calculateIntermediates(canvas, self.points)
            self.needsIntermediateRender = False

        for intermediates in self.intermediatePoints:
            intermediateColor = BezierCurve.intermediateColorPalette[len(intermediates) % len(BezierCurve.intermediateColorPalette)]

            if len(intermediates) > 1:
                drawLine(canvas, intermediates, intermediateColor)

            for point in intermediates:
                drawPoint(canvas, point, intermediateColor)

    def calculateIntermediates(self, canvas, pointsToRender):
        if len(pointsToRender) <= 0:
            return

        nextIntermediates = []
        for i, point in enumerate(pointsToRender[:-1]):
            newPoint = pointBetweenPoints(point, pointsToRender[i + 1], BezierCurve.intermediateStep)
            nextIntermediates.append(newPoint)

        self.intermediatePoints.append(nextIntermediates)
        self.calculateIntermediates(canvas, nextIntermediates)

    def renderCurve(self, canvas):
        if self.needsRender:
            currentStep = 0.0
            self.curvePoints = []

            while currentStep < 1.0 or areFloatsEqual(currentStep, 1.0):
                pointOnCurve = self.getPointOnCurveAtStep(canvas, self.points, currentStep)
                self.curvePoints.append(pointOnCurve)
                currentStep += STEP_SIZE

            self.curvePoints.append(self.points[-1])
            self.needsRender = False

        drawLine(canvas, self.curvePoints, "black")

    def getPointOnCurveAtStep(self, canvas, points, step):
        if len(points) == 1:
            return points[0]
        else:
            intermediatePoints = []

            for i, point in enumerate(points[:-1]):
                newPoint = pointBetweenPoints(point, points[i + 1], step)
                intermediatePoints.append(newPoint)

            return self.getPointOnCurveAtStep(canvas, intermediatePoints, step)

    def addPoint(self, point):
        self.points.append(point)
        self.setNeedsRender()

    def removeLastPoint(self):
        self.points.pop()
        self.setNeedsRender()

    def setNeedsRender(self):
        self.needsRender = True
        self.setNeedsIntermediateRender()

    def setNeedsIntermediateRender(self):
        self.needsIntermediateRender = True

    def closestPointTo(self, point):
        closestPoint = None
        closestDistance = None

        for curvePoint in self.points:
            distance = curvePoint.distanceTo(point)
            if closestDistance is None or distance < closestDistance:
                closestPoint = curvePoint
                closestDistance = distance

        return (closestPoint, closestDistance)

