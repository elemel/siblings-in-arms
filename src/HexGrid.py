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


from geometry import hex_distance, hex_neighbors, point_to_hex, hex_to_point


class HexGrid:

    def __init__(self, cell_size=1):
        self.cell_size = cell_size

    def point_to_cell(self, point):
        return point_to_hex(point, self.cell_size)

    def cell_to_point(self, cell):
        return hex_to_point(cell, self.cell_size)

    def cell_distance(self, from_cell, to_cell):
        return hex_distance(from_cell, to_cell) * self.cell_size

    def neighbors(self, cell):
        return hex_neighbors(cell)

    def neighbor_distance(self, from_cell, to_cell):
        return self.cell_size
