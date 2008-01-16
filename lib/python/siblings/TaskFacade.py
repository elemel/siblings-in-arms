# Copyright 2007 Mikael Lind.

from geometry import rectangle_from_center_and_size

class TaskFacade:
    def __init__(self, game_engine):
        self._game_engine = game_engine
        self.dt = 0.0
        self.actor = None
        self.aborting = False

    def request_path(self, unit, waypoint, callback):
        self._game_engine.pathfinder.request_path(unit, waypoint, callback)

    def remove_path_request(self, unit):
        pass    

    def lock_cell(self, unit, cell_key):
        return self._game_engine.gridlocker.lock(cell_key, unit)

    def unlock_cell(self, unit, cell_key):
        self._game_engine.gridlocker.unlock(cell_key)

    def is_cell_locked(self, cell_key):
        return self._game_engine.gridlocker.locked(cell_key)

    def get_build_time(self, name):
        return self._game_engine.unit_manager.get_build_time(name)

    def create_unit(self, name, player):
        return self._game_engine.unit_manager.create_unit(name, player)

    def add_unit(self, unit, pos):
        self._game_engine.add_unit(unit, pos)

    def set_pos(self, unit, pos):
        unit.pos = pos
        rect = rectangle_from_center_and_size(unit.pos, unit.size)
        self._game_engine.proximity_grid[unit.key] = rect

    def request_task(self, unit, callback):
        pass

    def remove_task_request(self, unit):
        pass

    def get_damage_factor(self, attacker, defender):
        return self._game_engine.get_damage_factor(attacker, defender)
