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


from Grid import intersects, concat, Grid


def test_intersects_when_equal():
    a = ((1, 2), (3, 4))
    assert intersects(a, a)


def test_intersects_when_overlap():
    a = ((1, 2), (5, 6))
    b = ((3, 4), (7, 8))
    assert intersects(a, b)
    assert intersects(b, a)


def test_intersects_when_contained():
    a = ((1, 2), (7, 8))
    b = ((3, 4), (5, 6))
    assert intersects(a, b)
    assert intersects(b, a)


def test_intersects_when_disjoint():
    a = ((1, 2), (3, 4))
    b = ((5, 6), (7, 8))
    assert not intersects(a, b)
    assert not intersects(b, a)


def test_concat():
    assert (tuple(concat(((1, 2), (), (3,), (4, 5, 6), (7,))))
            == (1, 2, 3, 4, 5, 6, 7))


def test_getitem_when_absent():
    g = Grid()
    try:
        g["a"]
    except KeyError, e:
        pass
    else:
        assert False


def test_getitem_when_present():
    g = Grid()    
    g["a"] = ((1, 2), (3, 4))
    assert g["a"] == ((1, 2), (3, 4))


def test_setitem_when_absent():
    g = Grid()
    g["a"] = ((1, 2), (3, 4))
    assert g["a"] == ((1, 2), (3, 4))


def test_setitem_when_present():
    g = Grid()    
    g["a"] = ((1, 2), (3, 4))
    g["a"] = ((5, 6), (7, 8))
    assert g["a"] == ((5, 6), (7, 8))


def test_delitem_when_absent():
    g = Grid()
    try:
        del g["a"]
    except KeyError, e:
        pass
    else:
        assert False


def test_delitem_when_present():
    g = Grid()    
    g["a"] = ((1, 2), (3, 4))
    del g["a"]
    assert "a" not in g
    assert not g


def test_contains_when_absent():
    g = Grid()
    assert "a" not in g
    g["a"] = ((1, 2), (3, 4))
    assert "b" not in g


def test_contains_when_present():
    g = Grid()
    g["a"] = ((1, 2), (3, 4))
    assert "a" in g


def test_len_when_empty():
    g = Grid()
    assert not g
    assert len(g) == 0


def test_len():
    g = Grid()
    g["a"] = ((1, 2), (3, 4))
    g["b"] = ((5, 6), (7, 8))
    g["c"] = ((9, 10), (11, 12))
    assert g
    assert len(g) == 3


def test_default_cell_size():
    g = Grid()
    assert g.cell_size() == 1


def test_cell_size():
    g = Grid(3)
    assert g.cell_size() == 3


def test_intersect():
    g = Grid()
    g["a"] = ((1, 2), (3, 4))
    g["b"] = ((5, 6), (7, 8))
    assert(g.intersect(((1, 5), (2, 6))) == set())
    assert(g.intersect(((2, 3), (2, 3))) == set(["a"]))
    assert(g.intersect(((6, 7), (6, 7))) == set(["b"]))
    assert(g.intersect(((2, 3), (6, 7))) == set(["a", "b"]))


def test():

    print
    print "Running Grid test suite..."
    
    print "Testing intersects function..."
    test_intersects_when_equal()
    test_intersects_when_overlap()
    test_intersects_when_contained()
    test_intersects_when_disjoint()
    
    print "Testing concat function..."
    test_concat()
    
    print "Testing Grid class..."
    test_getitem_when_absent()
    test_getitem_when_present()
    test_setitem_when_absent()
    test_setitem_when_present()
    test_delitem_when_absent()
    test_delitem_when_present()
    test_contains_when_absent()
    test_contains_when_present()
    test_len_when_empty()
    test_len()
    test_default_cell_size()
    test_cell_size()
    test_intersect()


if __name__ == "__main__":
    test()
