# Copyright 2007 Mikael Lind.

from FollowPathTask import FollowPathTask

class WaypointTask:
    def __init__(self, waypoint):
        self.waypoint = waypoint
        self.follow_path_task = None
        self.path = None
    
    def run(self, facade):
        while not facade.aborting:
            if facade.actor.pos == self.waypoint:
                break
            facade.find_path(facade.actor, self.waypoint, self._set_path)
            while self.path is None:
                yield 0.0
            if not self.path:
                break
            if not facade.aborting:
                self.follow_path_task = FollowPathTask(self.path)
                self.path = None
                for progress in self.follow_path_task.run(facade):
                    yield progress

    def _set_path(self, path):
        self.path = path
