# Copyright 2007 Mikael Lind.

class TaskFacade:
    def __init__(self, game_engine):
        self._game_engine = game_engine
        self.dt = 0.0
        self.actor = None
        self.aborting = False

    def find_path(self, waypoint, callback):
        self._game_engine.pathfinder.find_path(self.actor, waypoint, callback)

    def lock_cell(self, pos):
        return self._game_engine.path_grid.lock_cell(self.actor.key, pos)

    def unlock_cell(self, pos):
        self._game_engine.path_grid.unlock_cell(self.actor.key, pos)

    def get_build_time(self, name):
        return self._game_engine.unit_manager.get_build_time(name)

    def create_unit(self, name):
        self._game_engine.unit_manager.create_unit(name, self.actor.pos)
