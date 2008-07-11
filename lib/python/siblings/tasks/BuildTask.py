# Copyright 2007 Mikael Lind.

class BuildTask:
    def __init__(self, cls):
        self.cls = cls

    def run(self, facade):
        progress = 0.0
        while not facade.aborting:
            progress += facade.dt / self.cls.build_time
            if progress >= 1.0:
                break
            yield progress
        facade.add_unit(self.cls(facade.actor.player), facade.actor.pos)
