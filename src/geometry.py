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
from math import sqrt


SQRT_2 = sqrt(2)


def rect_from_center_and_size(center, size):
    x, y = center
    width, height = size
    return (x - width / 2, y - height / 2), (x + width / 2, y + height / 2)
    

def rect_contains_point(rect, point):
    (min_x, min_y), (max_x, max_y) = rect
    x, y = point
    return min_x <= x < max_x and min_y <= y < max_y


def rect_intersects_rect(rect_a, rect_b):
    (min_ax, min_ay), (max_ax, max_ay) = rect_a
    (min_bx, min_by), (max_bx, max_by) = rect_b
    return (min_ax < max_bx and min_bx < max_ax
            and min_ay < max_by and min_by < max_ay)


def normalize_rect(rect):
    (min_x, min_y), (max_x, max_y) = rect
    min_x, max_x = min(min_x, max_x), max(min_x, max_x)
    min_y, max_y = min(min_y, max_y), max(min_y, max_y)
    return (min_x, min_y), (max_x, max_y)


def square_neighbors(square):
    m, n = square
    yield m - 1, n - 1
    yield m - 1, n
    yield m - 1, n + 1
    yield m, n - 1
    yield m, n + 1
    yield m + 1, n - 1
    yield m + 1, n
    yield m + 1, n + 1


def squared_dist(p, q):
    px, py = p
    qx, qy = q
    return (qx - px) ** 2 + (qy - py) ** 2


def manhattan_dist(p, q):
    px, py = p
    qx, qy = q
    return abs(qx - px) + abs(qy - py)


def diagonal_dist(p, q):
    px, py = p
    qx, qy = q
    dx = abs(qx - px)
    dy = abs(qy - py)
    return SQRT_2 * min(dx, dy) + abs(dx - dy)
