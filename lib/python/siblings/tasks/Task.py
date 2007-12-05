# Copyright 2007 Mikael Lind.

from geometry import *

def interpolate_pos(old_p, new_p, progress):
    return vector_add(vector_mul(old_p, 1 - progress),
                      vector_mul(new_p, progress))

class MoveTask:
    def __init__(self, pos):
        self.pos = pos

    def run(self, facade, abort):
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

class FollowPathTask:
    def __init__(self, path):
        self.path = list(path)
        self.move_task = None

    def run(self, facade, abort):
        for i, pos in zip(xrange(len(self.path)), self.path):
            if abort or not facade.lock_cell(pos):
                return
            old_pos = facade.unit.pos
            self.move_task = MoveTask(pos)
            for progress in self.move_task.run(facade, abort):
                yield (i + progress) / len(self.path)
            self.move_task = None
            facade.unlock_cell(old_pos)

class WaypointTask:
    def __init__(self, waypoint):
        self.waypoint = waypoint
        self.follow_path_task = None
        self.path = None
    
    def run(self, facade, abort):
        while not abort:
            if facade.unit.pos == self.waypoint:
                break
            facade.find_path(self.waypoint, self._set_path)
            while self.path is None:
                yield 0.0
            if not self.path:
                break
            if not abort:
                self.follow_path_task = FollowPathTask(self.path)
                self.path = None
                for progress in self.follow_path_task.run(facade, abort):
                    yield progress

    def _set_path(self, path):
        self.path = path

class BuildTask:
    def __init__(self, name):
        self.name = name

    def run(self, facade, abort):
        progress = 0.0
        time = facade.get_build_time(self.name)
        while not abort:
            progress += facade.dt / time
            if progress >= 1.0:
                break
            yield progress
        facade.create_unit(self.name)
