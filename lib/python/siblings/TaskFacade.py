# Copyright 2007 Mikael Lind.

class TaskFacade:
    def __init__(self, game_engine):
        self._game_engine = game_engine
        self.dt = 0.0
        self.actor = None
        self.aborting = False

    def request_path(self, unit, waypoint, callback):
        self._game_engine.pathfinder.request_path(unit, waypoint, callback)

    def lock_cell(self, unit, pos):
        return self._game_engine.path_grid.lock_cell(unit, pos)

    def unlock_cell(self, unit, pos):
        self._game_engine.path_grid.unlock_cell(unit, pos)

    def is_cell_locked(self, pos):
        return self._game_engine.path_grid.is_cell_locked(pos)

    def get_build_time(self, name):
        return self._game_engine.unit_manager.get_build_time(name)

    def create_unit(self, name, player):
        return self._game_engine.unit_manager.create_unit(name, player)

    def add_unit(self, unit, pos):
        self._game_engine.add_unit(unit, pos)
