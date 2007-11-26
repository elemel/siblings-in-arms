from math import floor

def intersects(a, b):
    a_min, a_max = a
    a_left, a_bottom = a_min
    a_right, a_top = a_max

    b_min, b_max = b
    b_left, b_bottom = b_min
    b_right, b_top = b_max

    return (a_left < b_right and b_left < a_right
            and a_bottom < b_top and b_bottom < a_top)

def concat(outer):
    for inner in outer:
        for element in inner:
            yield element

class Grid(object):
    class _Entry(object):
        def __init__(self, bounds, indices):
            self.bounds = bounds
            self.indices = indices
    
    def __init__(self, grid_width, grid_height, cell_size = 1):
        self._grid_size = (grid_width, grid_height)
        self._cell_size = cell_size
        self._cells = [[set() for y in xrange(grid_height)]
                       for x in xrange(grid_width)]
        self._entries = {}

    def __len__(self):
        return len(self._entries)

    def __setitem__(self, key, bounds):
        entry = self._entries.get(key, None)
        if entry is None:
            self._insert(key, bounds)
        else:
            self._update(key, bounds, entry)

    def __getitem__(self, key):
        return self._entries[key].bounds

    def __delitem__(self, key):
        for x, y in self._indices.pop(key):
            self._cells[x][y].remove(key)
        del self._bounds[key]

    def __contains__(self, key):
        return key in self._entries

    def intersect(self, bounds):
        result = set()
        cells = (self._cells[x][y] for x, y in self._indices(bounds))
        result.update(key for key in concat(cells)
                      if intersects(self[key], bounds))
        return result

    def grid_size(self):
        return self._grid_size

    def cell_size(self):
        return self._cell_size

    def _indices(self, bounds):
        min_p, max_p = bounds
        min_x, min_y = min_p
        max_x, max_y = max_p
        h = lambda v: int(v / self._cell_size)
        return ((x, y) for x in xrange(h(min_x), h(max_x) + 1)
                for y in xrange(h(min_y), h(max_y) + 1))

    def _insert(self, key, bounds):
        indices = frozenset(self._indices(bounds))
        self._add_to_cells(key, indices)
        self._entries[key] = Grid._Entry(bounds, indices)

    def _update(self, key, bounds, entry):
        entry.bounds = bounds
        indices = frozenset(self._indices(bounds))
        if indices != entry.indices:
            self._remove_from_cells(key, entry.indices - indices)
            self._add_to_cells(key, indices - entry.indices)
            entry.indices = indices

    def _add_to_cells(self, key, indices):
        for x, y in indices:
            self._cells[x][y].add(key)

    def _remove_from_cells(self, key, indices):
        for x, y in indices:
            self._cells[x][y].remove(key)

def test():
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
