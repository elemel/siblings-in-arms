import math

SQRT_2 = math.sqrt(2)

def rectangle_from_center_and_size(center, size):
    x, y = center
    width, height = size
    min_p = (x - width / 2, y - height / 2)
    max_p = (x + width / 2, y + height / 2)
    return (min_p, max_p)
    
def rectangle_contains_point(r, p):
    min_p, max_p = r
    min_x, min_y = min_p
    max_x, max_y = max_p
    x, y = p
    return x >= min_x and y >= min_y and x <= max_x and y <= max_y

def grid_neighbors(p):
    x, y = p
    yield x - 1, y + 1; yield x + 0, y + 1; yield x + 1, y + 1
    yield x - 1, y + 0;                     yield x + 1, y + 0
    yield x - 1, y - 1; yield x + 0, y - 1; yield x + 1, y - 1

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
