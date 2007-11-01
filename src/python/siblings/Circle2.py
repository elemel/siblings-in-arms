from Rectangle2 import Rectangle2
from Vector2 import Vector2

class Circle2(object):
    def __init__(self, center, radius):
        self._center = center
        self._radius = radius
        self._bounding_box = Rectangle2(center - Vector2(radius, radius),
                                        center + Vector2(radius, radius))

    def get_center(self):
        return self._center

    center = property(get_center)

    def get_radius(self):
        return self._radius

    radius = property(get_radius)

    def get_bounding_box(self):
        return self._bounding_box

    bounding_box = property(get_bounding_box)

    def contains_point(self, point):
        return point.squared_dist(self.center) <= self._radius * self._radius
