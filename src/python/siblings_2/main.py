import time, sys
from a_star_search import a_star_search, grid_neighbors, diagonal_distance
from collections import deque
import ui
from ui import QuitEvent, MoveEvent, SelectEvent

A_STAR_SEARCH_LIMIT = 1000

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
        self.path = deque()
        self.waypoints = deque()
        self.progress = 0
    
    def update(self, dt, game):
        if self.state == IDLE:
            if self.waypoints:
                self.state = BEFORE_PATH_REQUEST

        if self.state == BEFORE_PATH_REQUEST:
            self._request_path(dt, game)
        elif self.state == FOLLOWING_PATH:
            self._follow_path(dt, game)

    def stop(self):
        self.waypoints.clear()
        self.path.clear()

    def add_waypoint(self, waypoint):
        waypoint = (int(waypoint[0]), int(waypoint[1]))
        self.waypoints.append(waypoint)

    def set_waypoint(self, waypoint):
        self.stop()
        self.add_waypoint(waypoint)

    def set_path(self, path):
        if self.state == AFTER_PATH_REQUEST:
            self.path = path
            self.progress = 0
            self.state = FOLLOWING_PATH

    def _request_path(self, dt, game):
        game.request_path(self, self.waypoints.popleft())
        self.state = AFTER_PATH_REQUEST

    def _follow_path(self, dt, game):
        if self.path:
            self.progress += dt * 5
            if self.progress >= 1:
                game.move_unit(self, self.path.popleft())
                self.progress = 0
        else:
            self.state = IDLE

class GameEngine:
    def __init__(self):
        self.grid = Grid((100, 100))
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
                                    diagonal_distance, heuristic,
                                    A_STAR_SEARCH_LIMIT)
        print "A* search: Examined %d node(s)." % len(nodes)
        d = deque()
        d.extendleft(node.p for node in path)
        return d

MIN_TIME_STEP = 0.01
MAX_TIME_STEP = 0.1

def main():
    game = GameEngine()
    unit = Unit()
    unit.pos = (2, 3)
    game.add_unit(unit)
    old_time = time.time()
    selected = None
    while True:
        new_time = time.time()
        dt = new_time - old_time
        if dt >= MIN_TIME_STEP:
            if dt > MAX_TIME_STEP:
                print "Skipping frames."
                dt = MAX_TIME_STEP
            old_time = new_time
            for e in ui.poll_events(game):
                if isinstance(e, SelectEvent):
                    selected = e.unit
                elif isinstance(e, MoveEvent):
                    if selected is not None:
                        selected.set_waypoint(e.pos)
                elif isinstance(e, QuitEvent):
                    sys.exit(0)
            game.update(dt)
            ui.update_screen(game)

if __name__ == "__main__":
    main()
