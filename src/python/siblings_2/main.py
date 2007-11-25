import time, sys
from a_star_search import a_star_search, grid_neighbors, diagonal_distance
from collections import deque
import ui
from ui import QuitEvent, MoveEvent, SelectEvent

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
REQUEST_PATH = 2
WAIT_FOR_PATH = 3
START_MOVING = 4
MOVE = 5

class Unit:
    _nums = iter(xrange(1, sys.maxint))

    def __init__(self):
        self.num = Unit._nums.next()
        self.old_pos = (0, 0)
        self.new_pos = self.old_pos
        self.state = IDLE
        self.path = deque()
        self.waypoints = deque()
        self.progress = 0
        self.cost = 1
        self.slots = set()
        self.speed = 5

    def get_pos(self):
        if self.old_pos == self.new_pos:
            return self.old_pos
        else:
            old_x, old_y = self.old_pos
            new_x, new_y = self.new_pos
            new_weight = min(float(self.progress) / self.cost, 1.0)
            x = old_x * (1 - new_weight) + new_x * new_weight
            y = old_y * (1 - new_weight) + new_y * new_weight
            return (x, y)

    pos = property(get_pos)
    
    def update(self, dt, game):
        if self.state == IDLE:
            if self.path:
                self.state = START_MOVING
            elif self.waypoints:
                self.state = REQUEST_PATH
        if self.state == REQUEST_PATH:
            self._request_path(dt, game)
        if self.state == MOVE:
            self._move(dt, game)
        if self.state == START_MOVING:
            self._start_moving(dt, game)

    def stop(self):
        self.waypoints.clear()
        self.path.clear()

    def add_waypoint(self, waypoint):
        self.waypoints.append(waypoint)

    def set_waypoint(self, waypoint):
        self.stop()
        self.add_waypoint(waypoint)

    def set_path(self, path):
        if self.state == WAIT_FOR_PATH:
            self.path = path
            self.state = IDLE

    def _request_path(self, dt, game):
        game.request_path(self, self.waypoints.popleft())
        self.state = WAIT_FOR_PATH

    def _start_moving(self, dt, game):
        pos = self.path.popleft()
        if game.reserve_slot(self, pos):
            self.slots.add(pos)
            self.new_pos = pos
            self.progress = 0
            self.cost = diagonal_distance(self.old_pos, self.new_pos)
            self.state = MOVE
        else:
            self.path.clear()
            self.state = IDLE

    def _move(self, dt, game):
        self.progress += dt * self.speed
        if self.progress >= self.cost:
            if self.old_pos in self.slots:
                game.release_slot(self, self.old_pos)
                self.slots.remove(self.old_pos)
            self.old_pos = self.new_pos
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

    def add_unit(self, unit, pos):
        self.units[unit.num] = unit
        unit.old_pos = unit.new_pos = pos
        if self.grid.get(unit.pos) == 0:
            self.grid.set(unit.pos, unit.num)

    def remove_unit(self, unit):
        del self.units[unit.num]
        self.grid.set(unit.pos, 0)

    def reserve_slot(self, unit, pos):
        if self.grid.get(pos) == 0:
            self.grid.set(pos, unit.num)
            print "Grid: Reserved slot %s for unit #%d." % (pos, unit.num)
            return True
        else:
            return False

    def release_slot(self, unit, pos):
        assert self.grid.get(pos) == unit.num
        self.grid.set(pos, 0)
        print "Grid: Unit #%d released slot %s." % (unit.num, pos)

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
        d.extendleft(node.p for node in path if node.p != unit.pos)
        return d

MIN_TIME_STEP = 0.01
MAX_TIME_STEP = 0.1
A_STAR_SEARCH_LIMIT = 1000

def main():
    game = GameEngine()
    game.add_unit(Unit(), (2, 3))
    game.add_unit(Unit(), (7, 4))
    game.add_unit(Unit(), (6, 5))
    game.add_unit(Unit(), (3, 7))
    game.add_unit(Unit(), (8, 2))
    game.add_unit(Unit(), (5, 6))
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
                    print "Selected unit #%d." % selected.num
                elif isinstance(e, MoveEvent):
                    if selected is not None:
                        x, y = e.pos
                        pos = (int(x + 0.5), int(y + 0.5))
                        selected.set_waypoint(pos)
                        print ("Set waypoint %s for unit #%d."
                               % (pos, selected.num))
                elif isinstance(e, QuitEvent):
                    sys.exit(0)
            game.update(dt)
            ui.update_screen(game)

if __name__ == "__main__":
    main()
