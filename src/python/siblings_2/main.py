class GridBucket:
    def __init__(self):
        self.things = []
        self.blocked = False

class Grid:
    def __init__(self):
        self.buckets = []
        for x in range(100):
            self.buckets[x] = []
            for y in range(100):
                self.buckets[x].append(GridBucket())

class PathFinder:
    def __call__(self, grid, from_pos, to_pos)

class Thing:
    _next_id = 1

    def __init__(self):
        self.id = _next_id++
    
    def update(self, dt, game_engine):
        pass

class Shot(Thing):
    pass

IDLE = 1
BEFORE_PATH_REQUEST = 2
AFTER_PATH_REQUEST = 3

class Unit(Thing):
    def __init__(self):
        self.state = IDLE
        self.path = []
        self.waypoints = []
    
    def update(self, dt, game_engine):
        if self.state == BEFORE_PATH_REQUEST:
            game_engine.request_path(self, self.waypoints[0])
            self.state = AFTER_PATH_REQUEST

    def add_waypoint(self, waypoint):
        self.waypoints.append(waypoint)
        self.state = BEFORE_PATH_REQUEST

class Structure(Thing):
    pass

class GameEngine:
    def __init__(self):
        self.things = []
        self.path_queue = []
        
    def update(self, dt):
        for t in self.things:
            t.update(dt, self)

    def request_path(self, unit, destination):
        path_queue.append((unit, destination))

def main():
    e = GameEngine()
    while True:
        e.update()

if __name__ == "__main__":
    main()
