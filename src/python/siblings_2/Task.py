from a_star_search import diagonal_distance

def interpolate_pos(old_p, new_p, progress):
    old_x, old_y = old_p
    new_x, new_y = new_p
    x = old_x * (1.0 - progress) + new_x * progress
    y = old_y * (1.0 - progress) + new_y * progress
    return (x, y)

class Task:
    def __init__(self):
        self.facade = None
        self.progress = 0.0
        self.aborted = False
        self.completed = False

    def run(self):
        raise NotImplementedError()

class MoveTask(Task):
    def __init__(self, pos):
        Task.__init__(self)
        self.pos = pos

    def run(self):
        old_pos = self.facade.unit.pos
        required = (diagonal_distance(old_pos, self.pos)
                    / self.facade.unit.speed)
        elapsed = 0.0
        while True:
            elapsed += self.facade.dt
            if elapsed >= required:
                self.facade.unit.pos = self.pos
                break
            progress = elapsed / required
            self.facade.unit.pos = interpolate_pos(old_pos, self.pos, progress)
            self._progress = progress
            yield

class FollowPathTask(Task):
    def __init__(self, path):
        Task.__init__(self)
        self.path = list(path)

    def run(self):
        for i, pos in zip(xrange(len(self.path)), self.path):
            if not self.facade.reserve_cell(pos):
                return
            self.facade.unit.cells.add(pos)
            move_task = MoveTask(pos)
            move_task.facade = self.facade
            for dummy in move_task.run():
                self._progress = (i + move_task.progress) / len(self.path)
                yield
            while self.facade.unit.cells:
                p = self.facade.unit.cells.pop()
                if p != pos:
                    self.facade.release_cell(p)
            self.facade.unit.cells.add(pos)

class WaypointTask(Task):
    def __init__(self, waypoint):
        Task.__init__(self)
        self.waypoint = waypoint
    
    def run(self):
        while True:
            path_future = self.facade.find_path(self.waypoint)
            while not path_future[0]:
                yield 0.0
            path = path_future[1]
            if not path:
                break
            follow_path_task = FollowPathTask(path)
            follow_path_task.facade = self.facade
            for dummy in follow_path_task.run():
                self._progress = follow_path_task.progress
                yield
            if self.facade.unit.pos == self.waypoint:
                break
