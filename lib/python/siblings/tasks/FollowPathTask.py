# Copyright 2007 Mikael Lind.

from MoveTask import MoveTask

class FollowPathTask:
    def __init__(self, path):
        self.path = list(path)
        self.move_task = None

    def run(self, facade):
        for i, pos in zip(xrange(len(self.path)), self.path):
            if facade.aborting or facade.get_cell_locker(pos):
                return
            facade.lock_cell(facade.actor.key, pos)
            old_pos = facade.actor.pos
            self.move_task = MoveTask(pos)
            for progress in self.move_task.run(facade):
                yield (i + progress) / len(self.path)
            self.move_task = None
            facade.unlock_cell(facade.actor.key, old_pos)
