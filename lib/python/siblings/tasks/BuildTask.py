# Copyright 2007 Mikael Lind.

class BuildTask:
    def __init__(self, name):
        self.name = name

    def run(self, facade):
        progress = 0.0
        time = facade.get_build_time(self.name)
        while not facade.aborting:
            progress += facade.dt / time
            if progress >= 1.0:
                break
            yield progress
        product = facade.create_unit(self.name, facade.actor.player)
        facade.add_unit(product, facade.actor.pos)
