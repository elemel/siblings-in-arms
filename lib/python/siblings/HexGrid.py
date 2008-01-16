# Copyright 2007 Mikael Lind.

from geometry import hex_neighbors, point_to_hex_cell, hex_cell_to_point

class HexGrid:
    def __init__(self, size, cell_dist = 1.0):
        self._size = size
        self._cell_dist = cell_dist

    def _get_size(self):
        return self._size

    def _get_cell_dist(self):
        return self._cell_dist

    size = property(_get_size)
    cell_dist = property(_get_cell_dist)

    def contains(self, cell_key):
        width, height = self._size
        x, y = cell_key
        return x >= 0 and x < width and y >= 0 and y < height

    def neighbors(self, cell_key):
        return (k for k in hex_neighbors(cell_key)
                if self.contains(k))

    def point_to_cell(self, point):
        return point_to_hex_cell(point, self._cell_dist)

    def cell_to_point(self, cell_key):
        return hex_cell_to_point(cell_key, self._cell_dist)
