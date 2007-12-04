# Copyright 2007 Mikael Lind.

class TaskFacade:
    def __init__(self):
        self.game_engine = None
        self.dt = 0.0
        self.unit = None

    def find_path(self, waypoint, callback):
        self.game_engine.find_path(self.unit, waypoint, callback)

    def lock_cell(self, pos):
        return self.game_engine.lock_cell(self.unit, pos)

    def unlock_cell(self, pos):
        self.game_engine.unlock_cell(self.unit, pos)

    def get_build_time(self, name):
        return self.game_engine.get_build_time(name)

    def create_unit(self, name):
        self.game_engine.create_unit(name, self.unit.pos)
