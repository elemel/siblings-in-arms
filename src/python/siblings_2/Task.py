# Copyright 2007 Mikael Lind.

from a_star_search import diagonal_distance

def interpolate_pos(old_p, new_p, progress):
    old_x, old_y = old_p
    new_x, new_y = new_p
    x = old_x * (1.0 - progress) + new_x * progress
    y = old_y * (1.0 - progress) + new_y * progress
    return (x, y)

class TaskError(Exception):
    def __init__(self, message):
        self.message = message

class Task:
    """Task for deferred execution by a unit.

    Tasks follow the Command pattern; their execution can be deferred until
    later. Tasks are enqueued in units and executed in FIFO order. Tasks can
    also be created and executed by other tasks.
    
    Tasks provide cooperative multiprocessing using Python generators. It is
    generally simpler to implement a complex task as a generator than as a
    state machine. For tracking purposes, tasks yield their current progress as
    a float in the range [0.0, 1.0].
    """
    
    def __init__(self):
        self._result = None
        self._aborting = False

    def _get_result(self): return self._result
    def _get_aborting(self): return self._aborting

    result = property(_get_result, doc = "The result of the task.")
    aborting = property(_get_aborting, doc = "Is the task aborting?")

    def run(self, facade):
        """Create generator for cooperative multiprocessing.

        To be implemented by subclasses.
        """
        raise NotImplementedException()

    def abort(self):
        """Request the task to abort."""
        self._aborting = True

class MoveTask(Task):
    def __init__(self, pos):
        Task.__init__(self)
        self.pos = pos

    def run(self, facade):
        old_pos = facade.unit.pos
        required = diagonal_distance(old_pos, self.pos) / facade.unit.speed
        elapsed = 0.0
        while True:
            elapsed += facade.dt
            if elapsed >= required:
                facade.unit.pos = self.pos
                break
            progress = elapsed / required
            facade.unit.pos = interpolate_pos(old_pos, self.pos, progress)
            yield progress

class FollowPathTask(Task):
    def __init__(self, path):
        Task.__init__(self)
        self.path = list(path)
        self.move_task = None

    def run(self, facade):
        for i, pos in zip(xrange(len(self.path)), self.path):
            if not facade.reserve_cell(pos):
                return
            facade.unit.cells.add(pos)
            self.move_task = MoveTask(pos)
            for progress in self.move_task.run(facade):
                yield (i + progress) / len(self.path)
            self.move_task = None
            while facade.unit.cells:
                p = facade.unit.cells.pop()
                if p != pos:
                    facade.release_cell(p)
            facade.unit.cells.add(pos)

class WaypointTask(Task):
    def __init__(self, waypoint):
        Task.__init__(self)
        self.waypoint = waypoint
        self.follow_path_task = None
    
    def run(self, facade):
        while True:
            path_future = facade.find_path(self.waypoint)
            while not path_future[0]:
                yield 0.0
            path = path_future[1]
            if not path:
                break
            self.follow_path_task = FollowPathTask(path)
            for progress in self.follow_path_task.run(facade):
                yield progress
            self.follow_path_task = None
            if facade.unit.pos == self.waypoint:
                break
