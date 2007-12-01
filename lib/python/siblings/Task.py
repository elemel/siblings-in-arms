# Copyright 2007 Mikael Lind.

from geometry import *

def interpolate_pos(old_p, new_p, progress):
    return vector_add(vector_mul(old_p, 1 - progress),
                      vector_mul(new_p, progress))

class Task:
    """Task for deferred execution by a unit.

    Tasks follow the Command pattern; their execution can be deferred until
    later. Tasks are enqueued in units and executed in FIFO order. Tasks can
    also be created and executed by other tasks.
    
    Tasks provide cooperative multiprocessing using generators. It is generally
    simpler to implement a complex task as a generator than as a state machine.
    For tracking purposes, tasks yield their current progress as a float in the
    range [0.0, 1.0].
    """
    
    def __init__(self):
        self._result = None
        self._aborting = False

    def _get_result(self): return self._result
    def _get_aborting(self): return self._aborting

    result = property(_get_result, doc = "The result of the task.")
    aborting = property(_get_aborting, doc = "Is the task aborting?")

    def run(self, facade):
        """Create generator for execution.

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
        distance = diagonal_distance(old_pos, self.pos)
        progress = 0.0
        while True:
            progress += facade.dt * facade.unit.speed / distance
            if progress >= 1.0:
                break
            facade.unit.pos = interpolate_pos(old_pos, self.pos, progress)
            yield progress
        facade.unit.pos = self.pos

class FollowPathTask(Task):
    def __init__(self, path):
        Task.__init__(self)
        self.path = list(path)
        self.move_task = None

    def run(self, facade):
        for i, pos in zip(xrange(len(self.path)), self.path):
            if not facade.lock_cell(pos):
                self._result = False
                return
            old_pos = facade.unit.pos
            self.move_task = MoveTask(pos)
            for progress in self.move_task.run(facade):
                yield (i + progress) / len(self.path)
            self.move_task = None
            facade.unlock_cell(old_pos)
        self._result = True

class WaypointTask(Task):
    def __init__(self, waypoint):
        Task.__init__(self)
        self.waypoint = waypoint
        self.follow_path_task = None
        self.path = None
    
    def run(self, facade):
        while True:
            if facade.unit.pos == self.waypoint:
                break
            facade.find_path(self.waypoint, self._set_path)
            while self.path is None:
                yield 0.0
            if not self.path:
                break
            self.follow_path_task = FollowPathTask(self.path)
            self.path = None
            for progress in self.follow_path_task.run(facade):
                yield progress

    def _set_path(self, path):
        self.path = path

class BuildTask(Task):
    def __init__(self, key):
        self.key = key

    def run(self, facade):
        progress = 0.0
        while True:
            progress += facade.dt / facade.get_build_time(key)
            if progress >= 1.0:
                break
            yield progress
        facade.create_unit(key)
