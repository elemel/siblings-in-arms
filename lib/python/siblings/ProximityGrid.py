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


from itertools import chain


def intersects(a, b):

    """Test two bounding boxes for intersection."""
    
    a_min, a_max = a
    a_left, a_bottom = a_min
    a_right, a_top = a_max

    b_min, b_max = b
    b_left, b_bottom = b_min
    b_right, b_top = b_max

    return (a_left < b_right and b_left < a_right
            and a_bottom < b_top and b_bottom < a_top)


class ProximityGrid(object):

    """Sparse planar grid for fast proximity searches."""
    
    def __init__(self, cell_size=1):

        """Initialize the grid."""

        self.__cell_size = cell_size
        self.__cells = {}
        self.__entries = {}

    def __getitem__(self, key):

        """Return the bounding box for the given key."""

        return self.__entries[key].bounds

    def __setitem__(self, key, bounds):

        """Insert or update an entry for the given key."""

        entry = self.__entries.get(key)
        if entry is None:
            self.__insert(key, bounds)
        else:
            self.__update(key, bounds, entry)

    def __delitem__(self, key):

        """Delete the entry for the given key."""

        entry = self.__entries.pop(key)
        self.__remove_from_cells(key, entry.indices)

    def __contains__(self, key):

        """Test whether there is an entry for the given key."""

        return key in self.__entries

    def __len__(self):

        """Return the number of entries."""

        return len(self.__entries)

    def cell_size(self):

        """Return the cell size."""

        return self.__cell_size

    def intersect(self, bounds):

        """Return keys for entries that intersect the given bounding box."""

        cells = (self.__cells.get(p, ()) for p in self.__indices(bounds))
        return set(key for key in chain(*cells)
                   if intersects(self[key], bounds))

    def __indices(self, bounds):
        min_p, max_p = bounds
        min_x, min_y = min_p
        max_x, max_y = max_p

        def hash(value):
            return int(value / self.__cell_size)

        return ((x, y) for x in xrange(hash(min_x), hash(max_x) + 1)
                for y in xrange(hash(min_y), hash(max_y) + 1))

    def __insert(self, key, bounds):
        indices = frozenset(self.__indices(bounds))
        self.__add_to_cells(key, indices)
        self.__entries[key] = _GridEntry(bounds, indices)

    def __update(self, key, bounds, entry):
        entry.bounds = bounds
        indices = frozenset(self.__indices(bounds))
        if indices != entry.indices:
            self.__remove_from_cells(key, entry.indices - indices)
            self.__add_to_cells(key, indices - entry.indices)
            entry.indices = indices

    def __add_to_cells(self, key, indices):
        for p in indices:
            cells = self.__cells.get(p)
            if cells is None:
                cells = self.__cells[p] = set()
            cells.add(key)

    def __remove_from_cells(self, key, indices):
        for p in indices:
            cells = self.__cells[p]
            cells.remove(key)
            if not cells:
                del self.__cells[p]


class _GridEntry(object):
    def __init__(self, bounds, indices):
        self.bounds = bounds
        self.indices = indices
