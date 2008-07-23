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
from math import cos, pi, sqrt


SQRT_2 = sqrt(2)
COS_30 = cos(pi / 6.0)


def rect_from_center_and_size(center, size):
    x, y = center
    width, height = size
    min_p = (x - width / 2.0, y - height / 2.0)
    max_p = (x + width / 2.0, y + height / 2.0)
    return min_p, max_p
    

def rect_contains_point(r, p):
    min_p, max_p = r
    min_x, min_y = min_p
    max_x, max_y = max_p
    x, y = p
    return min_x <= x < max_x and min_y <= y < max_y


def rect_intersects_rect(a, b):
    a_min_x, a_min_y, a_max_x, a_max_y = a[0][0], a[0][1], a[1][0], a[1][1]
    b_min_x, b_min_y, b_max_x, b_max_y = b[0][0], b[0][1], b[1][0], b[1][1]
    return (a_min_x < b_max_x and b_min_x < a_max_x
            and a_min_y < b_max_y and b_min_y < a_max_y)


def normalize_rect(rect):
    (min_x, min_y), (max_x, max_y) = rect
    min_x, max_x = min(min_x, max_x), max(min_x, max_x)
    min_y, max_y = min(min_y, max_y), max(min_y, max_y)
    return (min_x, min_y), (max_x, max_y)


def grid_neighbors(pos):
    x, y = pos
    yield x - 1, y + 1; yield x, y + 1; yield x + 1, y + 1
    yield x - 1, y; pass; yield x + 1, y
    yield x - 1, y - 1; yield x, y - 1; yield x + 1, y - 1


def squared_distance(a, b):
    ax, ay = a
    bx, by = b
    return (ax - bx) ** 2 + (ay - by) ** 2


def manhattan_distance(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)


def diagonal_distance(a, b):
    ax, ay = a
    bx, by = b
    dx = abs(ax - bx)
    dy = abs(ay - by)
    return SQRT_2 * min(dx, dy) + abs(dx - dy)


def vector_add(a, b):
    ax, ay = a
    bx, by = b
    return ax + bx, ay + by


def vector_sub(a, b):
    ax, ay = a
    bx, by = b
    return ax - bx, ay - by


def vector_mul(a, b):
    ax, ay = a
    return ax * b, ay * b


def vector_rmul(a, b):
    return vector_mul(b, a)


def vector_div(a, b):
    ax, ay = a
    return ax / b, ay / b


def vector_abs(v):
    x, y = v
    return sqrt(x ** 2 + y ** 2)


def point_to_hex(point, hex_size=1):
    x, y = point
    n = y / (COS_30 * hex_size)
    m = x / hex_size - 0.5 * n
    return int(round(m)), int(round(n))


def hex_to_point(hex, hex_size=1):
    m, n = hex
    return (m + 0.5 * n) * hex_size, COS_30 * n * hex_size


def hex_neighbors(hex):
    m, n = hex
    yield m - 1, n + 1; yield m, n + 1
    yield m - 1, n; pass; yield m + 1, n
    yield m, n - 1; yield m + 1, n - 1


def hex_distance(start_hex, goal_hex):
    start_m, start_n = min(start_hex, goal_hex)
    goal_m, goal_n = max(start_hex, goal_hex)
    diff_m, diff_n = goal_m - start_m, goal_n - start_n
    return diff_m + diff_n if start_n <= goal_n else max(diff_m, -diff_n)
