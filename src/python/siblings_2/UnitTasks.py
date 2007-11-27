class Task:
    def __init__(self):
        self.progress = 0
        self.done = False
        self.success = False

class MoveTask:
    def __init__(self, pos):
        self.pos = pos

    def run(self, facade):

class WaypointTask:
    def __init__(self, waypoint):
        self.waypoint = waypoint
    
    def run(self, facade):
        path_future = facade.request_path(self.waypoint)
        while not path_future:
            yield
        path = path_future.value
        
        while path:

    def update(self):

    def abort(self):

    def _set_path(self, path):
        self.path = path
    
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
