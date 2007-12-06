# Copyright 2007 Mikael Lind.

from MoveTask import MoveTask

class FollowPathTask:
    def __init__(self, path):
        self.path = list(path)
        self.move_task = None

    def run(self, facade, abort):
        for i, pos in zip(xrange(len(self.path)), self.path):
            if abort or not facade.lock_cell(pos):
                return
            old_pos = facade.actor.pos
            self.move_task = MoveTask(pos)
            for progress in self.move_task.run(facade, abort):
                yield (i + progress) / len(self.path)
            self.move_task = None
            facade.unlock_cell(old_pos)
