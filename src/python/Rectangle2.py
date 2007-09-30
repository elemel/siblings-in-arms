from Vector2 import Vector2

class Rectangle2(object):
    def __init__(self, min_point, max_point):
        self._min_x = min_point.x
        self._min_y = min_point.y
        self._max_x = max_point.x
        self._max_y = max_point.y

    def get_min_x(self):
        return self._min_x

    min_x = property(get_min_x)

    def get_min_y(self):
        return self._min_y

    min_y = property(get_min_y)

    def get_max_x(self):
        return self._max_x

    max_x = property(get_max_x)

    def get_max_y(self):
        return self._max_y

    max_y = property(get_max_y)

    def get_min_point(self):
        return Vector2(self._min_x, self._min_y)

    min_point = property(get_min_point)

    def get_max_point(self):
        return Vector2(self._max_x, self._max_y)

    max_point = property(get_max_point)

    def get_bounding_box(self):
        return self

    bounding_box = property(get_bounding_box)

    def contains_point(self, point):
        return (point.x >= self.min_x and point.x <= self.max_x
                and point.y >= self.min_y and point.y <= self.max_y)
