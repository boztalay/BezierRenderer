from basics import *

STEP_SIZE = 1.0 / 100.0;

class BezierCurve():
    intermediateRendering = False
    intermediateColorPalette = ["green", "red", "blue", "cyan", "magenta"]

    def __init__(self, firstPoint):
        self.points = [firstPoint]
        self.needsRender = True
        self.curvePoints = []

    def render(self, canvas):
        # Actual Bezier curve
        self.renderCurve(canvas)

        # Lines between the points
        if len(self.points) > 1:
            drawDashedLine(canvas, self.points, "gray")

        # The points
        for point in self.points:
            drawPoint(canvas, point, "black")

    def renderCurve(self, canvas):
        if self.shouldRender():
            currentStep = 0.0
            self.curvePoints = []

            while currentStep <= 1.0:
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

            if step > 0.499 and step < 0.501 and BezierCurve.intermediateRendering and len(intermediatePoints) > 1:
                intermediateColor = BezierCurve.intermediateColorPalette[len(intermediatePoints) % len(BezierCurve.intermediateColorPalette)]
                drawLine(canvas, intermediatePoints, intermediateColor)
                for point in intermediatePoints:
                    drawPoint(canvas, point, intermediateColor)

            return self.getPointOnCurveAtStep(canvas, intermediatePoints, step)

    def shouldRender(self):
        return (self.needsRender and self.isReadyToRender())

    def setNeedsRender(self):
        self.needsRender = True

    def isReadyToRender(self):
        return (len(self.points) > 1)

    def toggleIntermediateRendering(self):
        self.intermediateRendering = not self.intermediateRendering

    def closestPointTo(self, point):
        closestPoint = None
        closestDistance = None

        for curvePoint in self.points:
            distance = curvePoint.distanceTo(point)
            if closestDistance is None or distance < closestDistance:
                closestPoint = curvePoint
                closestDistance = distance

        return (closestPoint, closestDistance)
