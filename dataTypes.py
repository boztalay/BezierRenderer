import math

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, otherPoint):
        self.x = otherPoint.x
        self.y = otherPoint.y

    def distanceTo(self, otherPoint):
        return math.sqrt(pow(self.x - otherPoint.x, 2) + pow(self.y - otherPoint.y, 2))

CURVE_ORIGIN_1 = 0
CURVE_ORIGIN_2 = 1
CURVE_HANDLE_1 = 2
CURVE_HANDLE_2 = 3

class BezierCurve():
    def __init__(self, origin1):
        self.origin1 = origin1
        self.origin2 = None
        self.handle1 = None
        self.handle2 = None

    def isReadyToRender(self):
        return (self.origin1 is not None and self.origin2 is not None and self.handle1 is not None and self.handle2 is not None)

    def closestPointTo(self, point):
        if self.origin1 is not None:
            origin1Distance = self.origin1.distanceTo(point)
        else:
            origin1Distance = 999999999

        if self.origin2 is not None:
            origin2Distance = self.origin2.distanceTo(point)
        else:
            origin2Distance = 999999999

        if self.handle1 is not None:
            handle1Distance = self.handle1.distanceTo(point)
        else:
            handle1Distance = 999999999

        if self.handle2 is not None:
            handle2Distance = self.handle2.distanceTo(point)
        else:
            handle2Distance = 999999999

        if origin1Distance < origin2Distance and origin1Distance < handle1Distance and origin1Distance < handle2Distance:
            return (origin1Distance, CURVE_ORIGIN_1)
        elif origin2Distance < handle1Distance and origin2Distance < handle2Distance:
            return (origin2Distance, CURVE_ORIGIN_2)
        elif handle1Distance < handle2Distance:
            return (handle1Distance, CURVE_HANDLE_1)
        else:
            return (handle2Distance, CURVE_HANDLE_2)

    def getPointOfType(self, pointType):
        if pointType is CURVE_ORIGIN_1:
            return self.origin1
        elif pointType is CURVE_ORIGIN_2:
            return self.origin2
        elif pointType is CURVE_HANDLE_1:
            return self.handle1
        elif pointType is CURVE_HANDLE_2:
            return self.handle2
        else:
            return None
