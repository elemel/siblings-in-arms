def constrain(value, interval):
    min_v, max_v = interval
    value = max(value, min_v)
    value = min(value, max_v)
    return value

def fraction(value):
    return constrain(float(value), (0.0, 1.0))

class TaskError(Exception):
    def __init__(self, task, message):
        self.task = task
        self.message = message

class MoveTask(Task):
    def __init__(self, pos):
        self.pos = pos

    def run(self, facade):
        pass

class FollowPathTask(Task):
    def __init__(self, path):
        self.path = list(path)

    def run(self, facade):
        for i, pos in zip(xrange(len(self.path)), self.path):
            if not facade.reserve_cell(pos):
                raise TaskError(self, "could not reserve cell %s" % pos)
            facade.unit.cells.add(pos)
            for progress in MoveTask(pos).run(facade):
                yield (i + progress) / len(self.path)
            for p in facade.unit.cells:
                if p != pos:
                    facade.release_cell(p)
                    facade.unit.cells.remove(p)

class WaypointTask:
    def __init__(self, waypoint):
        self.waypoint = waypoint
    
    def run(self, facade):
        path_future = facade.request_path(self.waypoint)
        while not path_future:
            yield 0.0
        path = path_future.value
        for progress in FollowPathTask(path).run(facade):
            yield progress
