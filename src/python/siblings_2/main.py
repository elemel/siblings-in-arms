import time
from siblings.Circle2 import Circle2
from siblings.SparseGrid2 import SparseGrid2
from siblings.Vector2 import Vector2

class PathFinder:
    def __call__(self, grid, from_pos, to_pos):
        pass

class Thing:
    _next_id = 1

    def __init__(self):
        self.id = Thing._next_id
        print "Creating thing #%d." % self.id
        Thing._next_id += 1
        self.position = Vector2(0, 0)
    
    def update(self, dt, game_engine):
        pass

    def set_position(self, position):
        self.position = position

class Shot(Thing):
    pass

IDLE = 1
BEFORE_PATH_REQUEST = 2
AFTER_PATH_REQUEST = 3
FOLLOWING_PATH = 4

class Unit(Thing):
    def __init__(self):
        self.state = IDLE
        self.path = []
        self.waypoints = []
    
    def update(self, dt, game_engine):
        if self.state == BEFORE_PATH_REQUEST:
            self._request_path(dt, game_engine)
        elif self.state == FOLLOWING_PATH:
            self._follow_path(dt, game_engine)

    def add_waypoint(self, waypoint):
        self.waypoints.append(waypoint)
        self.state = BEFORE_PATH_REQUEST

    def set_path(self, path):
        self.path = path
        self.state = FOLLOWING_PATH

    def _request_path(self, dt, game_engine):
        game_engine.request_path(self, self.waypoints[0])
        self.state = AFTER_PATH_REQUEST

    def _follow_path(self, dt, game_engine):
        if len(self.path) == 0:
            self.state = IDLE
        else:
            pass

class Structure(Thing):
    pass

class GameEngine:
    def __init__(self):
        self.grid = SparseGrid2()
        self.things = []
        self.path_queue = []
        
    def update(self, dt):
        for t in self.things:
            t.update(dt, self)

    def request_path(self, unit, waypoint):
        self.path_queue.append((unit, waypoint))

    def update_position(self, thing):
        self.grid.insert(thing.id, Circle2(thing.position, 0.5))

    def add_thing(self, thing):
        self.things.append(thing)
        self.update_position(thing)

    def remove_thing(self, thing):
        self.things.erase(thing)
        self.grid.erase(thing.id)

MIN_TIME_STEP = 0.01
MAX_TIME_STEP = 0.1

def main():
    e = GameEngine()
    t = Thing()
    t.set_position(Vector2(17, 23))
    e.add_thing(t)
    e.update_position(t)
    old_time = time.time()
    while True:
        new_time = time.time()
        dt = new_time - old_time
        if dt >= MIN_TIME_STEP:
            if dt > MAX_TIME_STEP:
                print "Skipping frames."
                dt = MAX_TIME_STEP
            old_time = new_time
            e.update(dt)

if __name__ == "__main__":
    main()
