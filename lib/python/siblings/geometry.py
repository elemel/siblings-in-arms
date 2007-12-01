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
