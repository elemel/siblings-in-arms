# Copyright (c) 2007 Mikael Lind
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from geometry import (diagonal_distance, hex_neighbors, point_to_hex_cell,
                      hex_cell_to_point)


class HexGrid:

    def __init__(self, size, cell_dist = 1.0):
        self.size = size
        self.cell_dist = cell_dist

    def contains(self, cell_key):
        width, height = self.size
        x, y = cell_key
        return x >= 0 and x < width and y >= 0 and y < height

    def neighbors(self, cell_key):
        return (k for k in hex_neighbors(cell_key)
                if self.contains(k))

    def point_to_cell(self, point):
        return point_to_hex_cell(point, self.cell_dist)

    def cell_to_point(self, cell_key):
        return hex_cell_to_point(cell_key, self.cell_dist)

    def distance(self, point_a, point_b):
        return diagonal_distance(point_a, point_b)
