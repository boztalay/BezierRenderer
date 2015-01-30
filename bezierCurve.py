from basics import *

STEP_SIZE = 1.0 / 100.0;

class BezierCurve():
    def __init__(self, firstPoint):
        self.points = [firstPoint]
        self.needsRender = True

    def render(self, canvas):
        # Actual Bezier curve
        if self.shouldRender():
            self.renderCurve(canvas)

        # Lines between the points
        if len(self.points) > 1:
            drawDashedLine(canvas, self.points, "gray")

        # The points
        for point in self.points:
            drawPoint(canvas, point, "black")

    def renderCurve(self, canvas):
        currentStep = 0.0
        pointsOnCurve = []

        while currentStep <= 1.0:
            pointOnCurve = self.getPointOnCurveAtStep(self.points, currentStep)
            pointsOnCurve.append(pointOnCurve)
            currentStep += STEP_SIZE
        pointsOnCurve.append(self.points[-1])

        drawLine(canvas, pointsOnCurve, "black")

    def getPointOnCurveAtStep(self, points, step):
        if len(points) == 1:
            return points[0]
        else:
            intermediatePoints = []

            for i, point in enumerate(points[:-1]):
                newPoint = pointBetweenPoints(point, points[i + 1], step)
                intermediatePoints.append(newPoint)

            return self.getPointOnCurveAtStep(intermediatePoints, step)

    def shouldRender(self):
        return (self.needsRender and self.isReadyToRender())

    def setNeedsRender(self):
        self.needsRender = True

    def isReadyToRender(self):
        return (len(self.points) > 1)

    def closestPointTo(self, point):
        closestPoint = None
        closestDistance = None

        for curvePoint in self.points:
            distance = curvePoint.distanceTo(point)
            if closestDistance is None or distance < closestDistance:
                closestPoint = curvePoint
                closestDistance = distance

        return (closestPoint, closestDistance)
