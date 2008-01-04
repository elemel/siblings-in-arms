# Copyright 2007 Mikael Lind.

import math

SQRT_2 = math.sqrt(2)
COS_30 = math.cos(math.pi / 6.0)

def rectangle_from_center_and_size(center, size):
    x, y = center
    width, height = size
    min_p = (x - width / 2.0, y - height / 2.0)
    max_p = (x + width / 2.0, y + height / 2.0)
    return (min_p, max_p)
    
def rectangle_contains_point(r, p):
    min_p, max_p = r
    min_x, min_y = min_p
    max_x, max_y = max_p
    x, y = p
    return x >= min_x and y >= min_y and x <= max_x and y <= max_y

def rectangle_intersects_rectangle(a, b):
    a_min_x, a_min_y, a_max_x, a_max_y = a[0][0], a[0][1], a[1][0], a[1][1]
    b_min_x, b_min_y, b_max_x, b_max_y = b[0][0], b[0][1], b[1][0], b[1][1]
    return (a_min_x < b_max_x and b_min_x < a_max_x
            and a_min_y < b_max_y and b_min_y < a_max_y)

def normalize_rectangle(r):
    min_p, max_p = r
    min_x, min_y = min_p
    max_x, max_y = max_p
    min_x, max_x = min(min_x, max_x), max(min_x, max_x)
    min_y, max_y = min(min_y, max_y), max(min_y, max_y)
    return ((min_x, min_y), (max_x, max_y))

def grid_neighbors(pos):
    x, y = pos
    yield x - 1, y + 1; yield x + 0, y + 1; yield x + 1, y + 1
    yield x - 1, y + 0;                     yield x + 1, y + 0
    yield x - 1, y - 1; yield x + 0, y - 1; yield x + 1, y - 1

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
    return min(dx, dy) * SQRT_2 + abs(dx - dy)

def vector_add(a, b):
    ax, ay = a
    bx, by = b
    return (ax + bx, ay + by)

def vector_mul(a, b):
    ax, ay = a
    return (ax * b, ay * b)

def vector_rmul(a, b):
    return vector_mul(b, a)

def point_to_hex_cell(point, cell_dist = 1.0):
    x, y = point
    column = int(round(x / (cell_dist * COS_30)))
    row = int(round(y / cell_dist - 0.5 * (column % 2)))
    return (key_x, key_y)

def hex_cell_to_point(cell_key, cell_dist = 1.0):
    column, row = cell_key
    x = column * cell_dist * COS_30
    y = (row + 0.5 * (column % 2)) * cell_dist
    return (x, y)

def hex_neighbors(cell_key):
    x, y = cell_key
    if x % 2:
        yield x - 1, y + 1; yield x + 0, y + 1; yield x + 1, y + 1
        yield x - 1, y + 0; yield x + 0, y - 1; yield x + 1, y + 0
    else:
        yield x - 1, y + 0; yield x + 0, y + 1; yield x + 1, y + 0
        yield x - 1, y - 1; yield x + 0, y - 1; yield x + 1, y - 1
