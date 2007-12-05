# Copyright 2007 Mikael Lind.

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
