from __future__ import division
import math

class Vector2(object):
    def __init__(self, x = 0.0, y = 0.0):
        self._x = float(x)
        self._y = float(y)

    def __add__(self, other):
        return Vector2(self._x + float(other.x), self._y + float(other.y))

    def __sub__(self, other):
        return Vector2(self._x - float(other.x), self._y - float(other.y))

    def __mul__(self, other):
        return Vector2(self._x * float(other), self._y * float(other))

    def __rmul__(self, other):
        return Vector2(float(other) * self._x, float(other) * self._y)

    def __truediv__(self, other):
        return Vector2(self._x / float(other), self._y / float(other))

    def __neg__(self):
        return Vector2(-self._x, -self._y)

    def __abs__(self):
        return sqrt(self.sqabs())

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = float(x)
        
    x = property(get_x, set_x)

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = float(y)
        
    y = property(get_y, set_y)

    def sqabs(self):
        return self._x * self._x + self._y * self._y

    def sqdist(self, other):
        return (self - other).sqabs()

    def dist(self, other):
        return math.sqrt(self.sqdist(other))
