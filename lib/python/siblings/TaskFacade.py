# Copyright 2007 Mikael Lind.

class TaskFacade:
    def __init__(self, game_engine):
        self._game_engine = game_engine
        self.dt = 0.0
        self.unit = None

    def find_path(self, waypoint, callback):
        self._game_engine.find_path(self.unit, waypoint, callback)

    def lock_cell(self, pos):
        return self._game_engine.lock_cell(self.unit, pos)

    def unlock_cell(self, pos):
        self._game_engine.unlock_cell(self.unit, pos)

    def get_build_time(self, name):
        return self._game_engine.get_build_time(name)

    def create_unit(self, name):
        self._game_engine.create_unit(name, self.unit.pos)
