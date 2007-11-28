from a_star_search import diagonal_distance

def constrain(value, interval):
    min_v, max_v = interval
    value = max(value, min_v)
    value = min(value, max_v)
    return value

def fraction(value):
    return constrain(float(value), (0.0, 1.0))

def scale(pos, factor):
    x, y = pos
    return (x * factor, y * factor)

class Task:
    def __init__(self, path):
        self._progress = 0.0
        self._aborted = False

    def progress(self):
        return self._progress

    def abort(self):
        self._aborted = True

    def run(self):
        raise NotImplementedError()

class TaskError(Exception):
    def __init__(self, task, message):
        self.task = task
        self.message = message

class MoveTask(Task):
    def __init__(self, pos):
        self.pos = pos

    def run(self, facade):
        old_pos = facade.unit.pos
        required = diagonal_distance(old_pos, self.pos) / facade.unit.speed
        elapsed = 0.0
        while True:
            elapsed += facade.dt
            if elapsed >= total:
                facade.unit.pos = self.pos
                break
            progress = elapsed / required
            facade.unit.pos = (scale(old_pos, 1.0 - progress)
                               + scale(self.pos * progress))
            self._progress = progress
            yield

class FollowPathTask(Task):
    def __init__(self, path):
        self.path = list(path)

    def run(self, facade):
        for i, pos in zip(xrange(len(self.path)), self.path):
            if not facade.reserve_cell(pos):
                raise TaskError(self, "could not reserve cell %s" % pos)
            facade.unit.cells.add(pos)
            for progress in MoveTask(pos).run(facade):
                self._progress = (i + progress) / len(self.path)
                yield
            for p in facade.unit.cells:
                if p != pos:
                    facade.release_cell(p)
                    facade.unit.cells.remove(p)

class WaypointTask(Task):
    def __init__(self, waypoint):
        self.waypoint = waypoint
    
    def run(self, facade):
        while True:
            path_future = facade.request_path(self.waypoint)
            while not path_future:
                yield 0.0
            path = path_future.value
            try:
                follow_path_task = FollowPathTask(path)
                for dummy in follow_path_task.run(facade):
                    self._progress = follow_path_task.progress()
                    yield
                break
            except TaskError:
                pass
