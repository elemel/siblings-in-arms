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


from __future__ import division
from math import cos, pi


COS_30 = cos(pi / 6)


class HexGrid:

    def __init__(self, cell_size=1):
        self.cell_size = cell_size

    def point_to_cell(self, point):
        x, y = point
        m = x / (COS_30 * self.cell_size)
        n = y / self.cell_size - m / 2
        return int(round(m)), int(round(n))

    def cell_to_point(self, cell):
        m, n = cell
        return COS_30 * m * self.cell_size, (n + m / 2) * self.cell_size

    def cell_dist(self, start, goal):
        start_m, start_n = min(start, goal)
        goal_m, goal_n = max(start, goal)
        diff_m, diff_n = goal_m - start_m, goal_n - start_n
        return self.cell_size * (diff_m + diff_n if start_n <= goal_n
                                 else max(diff_m, -diff_n))

    def neighbors(self, cell):
        m, n = cell
        yield m - 1, n
        yield m - 1, n + 1
        yield m, n - 1
        yield m, n + 1
        yield m + 1, n - 1
        yield m + 1, n

    def neighbor_dist(self, start, goal):
        return self.cell_size
