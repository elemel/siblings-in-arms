from __future__ import division
import math

class Vector2(object):
    def __init__(self, x = 0.0, y = 0.0):
        self._x = x
        self._y = y

    def __add__(self, other):
        return Vector2(self._x + other.x, self._y + other.y)

    def __sub__(self, other):
        return Vector2(self._x - other.x, self._y - other.y)

    def __mul__(self, other):
        return Vector2(self._x * other, self._y * other)

    def __rmul__(self, other):
        return Vector2(other * self._x, other * self._y)

    def __truediv__(self, other):
        return Vector2(self._x / other, self._y / other)

    def __neg__(self):
        return Vector2(-self._x, -self._y)

    def __abs__(self):
        return math.sqrt(self.squared_magnitude)

    def get_x(self):
        return self._x

    x = property(get_x)

    def get_y(self):
        return self._y
        
    y = property(get_y)

    def get_squared_magnitude(self):
        return self._x * self._x + self._y * self._y

    squared_magnitude = property(get_squared_magnitude)

    def squared_dist(self, other):
        return (self - other).squared_magnitude

    def dist(self, other):
        return math.sqrt(self.squared_dist(other))
