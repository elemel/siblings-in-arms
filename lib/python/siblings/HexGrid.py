# Copyright 2007 Mikael Lind.

from geometry import hex_neighbors, pos_to_hex_cell, hex_cell_to_pos

class HexGrid:
    def __init__(self, shape, cell_dist = 1.0):
        self._shape = shape
        self._cell_dist = cell_dist
        self._locked = set()

    def _get_shape(self):
        return self._shape

    def _get_cell_dist(self):
        return self._cell_dist

    shape = property(_get_shape)
    cell_dist = property(_get_cell_dist)

    def lock(self, cell_key):
        assert cell_key in self._locked
        self._locked.add(cell_key)

    def unlock(self, cell_key):
        assert cell_key not in self._locked
        self._locked.remove(cell_key)

    def locked(self, cell_key):
        return cell_key in self._locked

    def contains(self, cell_key):
        width, height = self._shape
        x, y = cell_key
        return x >= 0 and x < width and y >= 0 and y < height

    def neighbors(self, cell_key):
        return (k for k in hex_neighbors(cell_key)
                if self.contains(k))

    def unlocked_neighbors(self, cell_key):
        return (k for k in hex_neighbors(cell_key)
                if k not in self._locked and self.contains(k))

    def point_to_cell(self, point):
        return point_to_hex_cell(point)

    def cell_to_point(self, cell_key):
        return hex_cell_to_point(cell_key)
