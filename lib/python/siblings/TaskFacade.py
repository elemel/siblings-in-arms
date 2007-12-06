# Copyright 2007 Mikael Lind.

class TaskFacade:
    def __init__(self, game_engine):
        self._game_engine = game_engine
        self.dt = 0.0
        self.actor = None
        self.aborting = False

    def find_path(self, unit, waypoint, callback):
        self._game_engine.pathfinder.find_path(unit, waypoint, callback)

    def lock_cell(self, key, pos):
        return self._game_engine.path_grid.lock_cell(key, pos)

    def unlock_cell(self, key, pos):
        self._game_engine.path_grid.unlock_cell(key, pos)

    def get_cell_locker(self, pos):
        return self._game_engine.path_grid.get_cell_locker(pos)

    def get_build_time(self, name):
        return self._game_engine.unit_manager.get_build_time(name)

    def create_unit(self, name, player):
        return self._game_engine.unit_manager.create_unit(name, player)

    def add_unit(self, unit, pos):
        self._game_engine.unit_manager.add_unit(unit, pos)
