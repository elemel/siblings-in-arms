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


from geometry import (diagonal_distance, hex_neighbors, pos_to_hex_cell,
                      hex_cell_to_pos)


class HexGrid:

    def __init__(self, cell_size = 1):
        self.cell_size = cell_size

    def pos_to_cell(self, point):
        return pos_to_hex_cell(point, self.cell_size)

    def cell_to_pos(self, cell):
        return hex_cell_to_pos(cell, self.cell_size)

    def cell_distance(self, from_cell, to_cell):
        return diagonal_distance(hex_cell_to_pos(from_cell),
                                 hex_cell_to_pos(to_cell))

    def neighbors(self, cell):
        return hex_neighbors(cell)

    def neighbor_distance(self, from_cell, to_cell):
        return self.cell_size
