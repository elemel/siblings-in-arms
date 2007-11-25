import time, sys
from a_star_search import a_star_search, grid_neighbors, diagonal_distance
from collections import deque
import ui

class Grid:
    def __init__(self, size):
        self.size = size
        width, height = size
        self._slots = [[0] * height for x in xrange(width)]

    def get(self, pos):
        x, y = pos
        return self._slots[x][y]

    def set(self, pos, num):
        x, y = pos
        self._slots[x][y] = num

IDLE = 1
BEFORE_PATH_REQUEST = 2
AFTER_PATH_REQUEST = 3
FOLLOWING_PATH = 4

class Unit:
    _nums = iter(xrange(1, sys.maxint))

    def __init__(self):
        self.num = Unit._nums.next()
        self.pos = (0, 0)
        self.state = IDLE
        self.path = []
        self.waypoints = []
        self.progress = 0
    
    def update(self, dt, engine):
        if self.state == BEFORE_PATH_REQUEST:
            self._request_path(dt, engine)
        elif self.state == FOLLOWING_PATH:
            self._follow_path(dt, engine)

    def add_waypoint(self, waypoint):
        self.waypoints.append(waypoint)
        self.state = BEFORE_PATH_REQUEST

    def set_path(self, path):
        self.path = path
        self.progress = 0
        self.state = FOLLOWING_PATH

    def _request_path(self, dt, engine):
        engine.request_path(self, self.waypoints[0])
        self.state = AFTER_PATH_REQUEST

    def _follow_path(self, dt, engine):
        if self.path:
            self.progress += dt
            if self.progress >= 1:
                engine.move_unit(self, self.path.popleft())
                self.progress = 0
        else:
            self.state = IDLE

class GameEngine:
    def __init__(self):
        self.grid = Grid((60, 20))
        self.units = {}
        self.path_queue = deque()
        
    def update(self, dt):
        if self.path_queue:
            unit, waypoint = self.path_queue.popleft()
            path = self._find_path(unit, waypoint)
            unit.set_path(path)
        for t in self.units.itervalues():
            t.update(dt, self)

    def request_path(self, unit, waypoint):
        self.path_queue.append((unit, waypoint))

    def add_unit(self, unit):
        x, y = unit.pos
        self.units[unit.num] = unit
        self.grid.set(unit.pos, unit.num)

    def remove_unit(self, unit):
        del self.units[unit.num]
        self.grid.set(unit.pos, 0)

    def move_unit(self, unit, pos):
        self.grid.set(pos, unit.num)
        self.grid.set(unit.pos, 0)
        unit.pos = pos

    def _find_path(self, unit, waypoint):
        def neighbors(p):
            def contains(p):
                x, y = p
                width, height = self.grid.size
                return x >= 0 and x < width and y >= 0 and y < height

            def passable(p):
                x, y = p
                return self.grid.get((x, y)) in (0, unit.num)

            return (n for n in grid_neighbors(p) if contains(n) and passable(n))

        def heuristic(p):
            return diagonal_distance(p, waypoint)

        path, nodes = a_star_search(unit.pos, waypoint, neighbors,
                                    diagonal_distance, heuristic)
        d = deque()
        d.extendleft(node.p for node in path)
        return d

MIN_TIME_STEP = 0.01
MAX_TIME_STEP = 0.1

def main():
    engine = GameEngine()
    unit = Unit()
    unit.pos = (2, 3)
    unit.add_waypoint((10, 7))
    engine.add_unit(unit)
    old_time = time.time()
    while True:
        new_time = time.time()
        dt = new_time - old_time
        if dt >= MIN_TIME_STEP:
            if dt > MAX_TIME_STEP:
                print "Skipping frames."
                dt = MAX_TIME_STEP
            old_time = new_time
            engine.update(dt)
            ui.update_screen(engine)

if __name__ == "__main__":
    main()
