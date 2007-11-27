from Grid import intersects, concat, Grid

def test_intersects_when_equal():
    a = ((1, 2), (3, 4))
    assert intersects(a, a)

def test_intersects_when_overlap():
    a = ((1, 2), (5, 6))
    b = ((3, 4), (7, 8))
    assert intersects(a, b)

def test_intersects_when_a_contains_b():
    a = ((1, 2), (7, 8))
    b = ((3, 4), (5, 6))
    assert intersects(a, b)

def test_intersects_when_b_contains_a():
    a = ((3, 4), (5, 6))
    b = ((1, 2), (7, 8))
    assert intersects(a, b)

def test_intersects_when_disjoint():
    a = ((1, 2), (3, 4))
    b = ((5, 6), (7, 8))
    assert not intersects(a, b)

def test_concat():
    assert (tuple(concat(((1, 2), (), (3,), (4, 5, 6), (7,))))
            == (1, 2, 3, 4, 5, 6, 7))

def test():
    print
    print "Running Grid test suite..."
    
    print "Testing intersects function..."
    test_intersects_when_equal()
    test_intersects_when_overlap()
    test_intersects_when_a_contains_b()
    test_intersects_when_b_contains_a()
    test_intersects_when_disjoint()
    
    print "Testing concat function..."
    test_concat()
    
    print "Testing Grid class..."
    grid = Grid(10, 7, 3)
    assert grid.grid_size() == (10, 7)
    assert grid.cell_size() == 3
    assert len(grid) == 0
    green_bounds = ((1.5, 2.1), (2.3, 2.7))
    yellow_bounds = ((2.2, 2.9), (2.5, 3.4))
    grid["green"] = green_bounds
    grid["yellow"] = yellow_bounds
    assert "green" in grid
    assert grid["green"] == green_bounds
    assert grid.intersect(((1.3, 2.3), (3.1, 2.5))) == set(["green"])

if __name__ == "__main__":
    test()
